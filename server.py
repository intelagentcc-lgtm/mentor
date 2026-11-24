"""Serve Mentor and its local SQLite profile API on a loopback address."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import tempfile
from urllib.parse import parse_qs, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parent
SCOPES = {"student", "maya", "alex"}
FIELDS = set("""name grade goal grades activities school hours budget target
    gradeReports interests courses subjects experience notes preferredColleges constraints""".split())
ASSETS = {"/", "/index.html", "/local-ai.html", "/app.js", "/styles.css", "/profile.js", "/profile.css"}
FILE_LIMIT = 12 * 1024 * 1024
ENTRY_LIMIT = 4000
BATCH_LIMIT = 100


@contextmanager
def database(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def initialize(path):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.touch(mode=0o600)
    with database(path) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS profile_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scope TEXT NOT NULL,
                field TEXT NOT NULL,
                value TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS profile_entries_scope ON profile_entries(scope, id);
            CREATE TABLE IF NOT EXISTS initialized_profiles (scope TEXT PRIMARY KEY);
            CREATE TABLE IF NOT EXISTS chat_turns (
                id INTEGER PRIMARY KEY,
                fingerprint TEXT NOT NULL UNIQUE,
                recorded_at TEXT,
                exchange TEXT NOT NULL
            );
        """)


def validate_entry(entry):
    if not isinstance(entry, dict) or not isinstance(entry.get("field"), str) or entry["field"] not in FIELDS:
        raise ValueError("Choose a profile field.")
    value = entry.get("value")
    if not isinstance(value, str) or not 0 < len(value.strip()) <= ENTRY_LIMIT:
        raise ValueError(f"Each entry needs 1–{ENTRY_LIMIT} characters.")
    return entry["field"], value.strip()


def native_text(payload, suffix):
    with tempfile.TemporaryDirectory(prefix="mentor-import-") as folder:
        path = Path(folder) / ("import" + suffix)
        path.write_bytes(payload)
        if suffix == ".doc":
            command = ["/usr/bin/textutil", "-convert", "txt", "-stdout", str(path)]
        else:
            command = ["/usr/bin/swift", str(ROOT / "profile_ocr.swift"), str(path)]
        result = subprocess.run(command, capture_output=True, timeout=120, check=False)
        if result.returncode:
            raise ValueError("Could not extract text. PDF and image imports require macOS Swift command-line tools.")
        return result.stdout.decode("utf-8")


def extract_text(filename, payload):
    suffix = Path(filename).suffix.lower()
    if suffix in {".txt", ".md", ".csv", ".tsv"}:
        return payload.decode("utf-8-sig")
    if suffix in {".pdf", ".png", ".jpg", ".jpeg", ".heic", ".tif", ".tiff", ".bmp", ".webp", ".doc"}:
        return native_text(payload, suffix)
    if suffix in {".xlsx", ".docx"}:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            if sum(item.file_size for item in archive.infolist()) > 40 * 1024 * 1024:
                raise ValueError("The expanded document exceeds the import size limit.")
    if suffix == ".xlsx":
        import openpyxl
        book = openpyxl.load_workbook(io.BytesIO(payload), read_only=True, data_only=True)
        try:
            return spreadsheet_text(sheet.values for sheet in book)
        finally:
            book.close()
    if suffix == ".xls":
        import xlrd
        book = xlrd.open_workbook(file_contents=payload, on_demand=True)
        try:
            return spreadsheet_text(sheet.get_rows() for sheet in book.sheets())
        finally:
            book.release_resources()
    if suffix == ".docx":
        from docx import Document
        document = Document(io.BytesIO(payload))
        return "\n".join(
            paragraph.text if hasattr(paragraph, "text") else
            "\n".join(" | ".join(cell.text for cell in row.cells) for row in paragraph.rows)
            for paragraph in document.iter_inner_content()
        )
    raise ValueError("Choose a supported text, Word, Excel, PDF, or image file.")


def spreadsheet_text(sheets):
    lines = []
    for sheet in sheets:
        for row in sheet:
            values = [str(getattr(cell, "value", cell)) for cell in row if getattr(cell, "value", cell) not in (None, "")]
            if values:
                lines.append(" | ".join(values))
            if len(lines) >= 1000:
                return "\n".join(lines)
    return "\n".join(lines)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def allowed_host(self):
        port = self.server.server_port
        return self.headers.get("Host") in {f"localhost:{port}", f"127.0.0.1:{port}"}

    def reply(self, status, content):
        encoded = json.dumps(content).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def contents(self, limit):
        size = int(self.headers.get("Content-Length", "0"))
        if not 0 < size <= limit:
            raise ValueError("The request is empty or exceeds the import size limit.")
        return self.rfile.read(size)

    def do_GET(self):
        if self.path.startswith("/api/"):
            return self.api()
        if not self.allowed_host() or urlsplit(self.path).path not in ASSETS:
            return self.send_error(HTTPStatus.NOT_FOUND)
        super().do_GET()

    def do_HEAD(self):
        if not self.allowed_host() or urlsplit(self.path).path not in ASSETS:
            return self.send_error(HTTPStatus.NOT_FOUND)
        super().do_HEAD()

    def do_POST(self):
        self.api()

    def do_PUT(self):
        self.api()

    def do_DELETE(self):
        self.api()

    def api(self):
        if not self.allowed_host() or self.headers.get("Origin") not in {None, f"http://{self.headers.get('Host')}"}:
            return self.reply(HTTPStatus.FORBIDDEN, {"error": "Open Mentor using its local address."})
        url = urlsplit(self.path)
        params = parse_qs(url.query)
        try:
            if url.path == "/api/chat":
                return self.chat_history()
            if url.path == "/api/profile/import" and self.command == "POST":
                if self.headers.get("Content-Type") != "application/octet-stream":
                    raise ValueError("Invalid upload request.")
                text = extract_text(params.get("name", [""])[0], self.contents(FILE_LIMIT)).strip()
                if not text:
                    raise ValueError("No readable text was found.")
                return self.reply(HTTPStatus.OK, {"text": text[:40000], "truncated": len(text) > 40000})
            if url.path != "/api/profile":
                return self.reply(HTTPStatus.NOT_FOUND, {"error": "Unknown endpoint."})
            if self.command in {"POST", "PUT"} and self.headers.get_content_type() != "application/json":
                raise ValueError("Expected a JSON request.")
            scope = params.get("scope", [""])[0]
            if scope not in SCOPES:
                raise ValueError("Unknown profile.")
            self.change_profile(scope, params)
        except subprocess.TimeoutExpired:
            self.reply(HTTPStatus.BAD_REQUEST, {"error": "Text extraction timed out. Try a smaller file."})
        except ImportError:
            self.reply(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "Install the document dependencies from requirements.txt."})
        except (ValueError, OSError, zipfile.BadZipFile) as error:
            message = str(error) if isinstance(error, ValueError) else "Could not read the file."
            self.reply(HTTPStatus.BAD_REQUEST, {"error": message[:250]})
        except sqlite3.Error:
            self.reply(HTTPStatus.SERVICE_UNAVAILABLE, {"error": "The Mentor database is unavailable."})
        except Exception:
            self.reply(HTTPStatus.BAD_REQUEST, {"error": "Could not process the file or request."})

    def chat_history(self):
        if self.command == "POST":
            if self.headers.get_content_type() != "application/json":
                raise ValueError("Expected a JSON request.")
            turns = json.loads(self.contents(1024 * 1024))
            if not isinstance(turns, list) or not 1 <= len(turns) <= 50:
                raise ValueError("Expected 1–50 chat exchanges.")
            rows = []
            for turn in turns:
                if not isinstance(turn, dict):
                    raise ValueError("Invalid chat exchange.")
                exchange = {key: turn.get(key, "") for key in
                            ("student", "mentor", "mode", "outcome", "sessionId", "projectId", "recordedAt")}
                if any(not isinstance(value, str) or len(value) > 5000 for value in exchange.values()):
                    raise ValueError("Invalid chat exchange.")
                if not exchange["student"] or not exchange["mentor"]:
                    raise ValueError("An exchange requires a student message and mentor reply.")
                recorded_at = exchange["recordedAt"]
                if recorded_at:
                    timestamp = datetime.fromisoformat(recorded_at.replace("Z", "+00:00"))
                    if timestamp.tzinfo is None:
                        raise ValueError("Chat timestamps require a timezone.")
                    exchange["recordedAt"] = timestamp.astimezone(timezone.utc).isoformat(timespec="milliseconds")
                serialized = json.dumps(exchange, sort_keys=True)
                fingerprint = hashlib.sha256(serialized.encode()).hexdigest()
                rows.append((fingerprint, exchange["recordedAt"] or None, serialized))
            with database(self.server.profile_path) as db:
                db.executemany("INSERT INTO chat_turns(fingerprint, recorded_at, exchange) VALUES (?, ?, ?) "
                               "ON CONFLICT(fingerprint) DO NOTHING", rows)
        elif self.command == "DELETE":
            with database(self.server.profile_path) as db:
                db.execute("DELETE FROM chat_turns")
        elif self.command == "GET":
            with database(self.server.profile_path) as db:
                turns = [json.loads(row["exchange"]) for row in
                         db.execute("SELECT exchange FROM chat_turns ORDER BY recorded_at, id")]
            return self.reply(HTTPStatus.OK, {"turns": turns})
        else:
            return self.reply(HTTPStatus.METHOD_NOT_ALLOWED, {"error": "Unsupported chat request."})
        self.reply(HTTPStatus.OK, {})

    def change_profile(self, scope, params):
        missing_entry = False
        with database(self.server.profile_path) as db:
            if self.command == "POST":
                payload = json.loads(self.contents(2 * 1024 * 1024))
                if not isinstance(payload, dict) or not isinstance(payload.get("entries"), list):
                    raise ValueError("Provide a list of profile entries.")
                if len(payload["entries"]) > BATCH_LIMIT or (not payload["entries"] and payload.get("seed") is not True):
                    raise ValueError("Save between 1 and 100 entries.")
                entries = [validate_entry(entry) for entry in payload["entries"]]
                initialized = db.execute("INSERT OR IGNORE INTO initialized_profiles VALUES (?)", (scope,)).rowcount
                if payload.get("seed") is not True or initialized:
                    db.executemany(
                        "INSERT INTO profile_entries(scope, field, value) VALUES (?, ?, ?)",
                        ((scope, field, value) for field, value in entries),
                    )
            elif self.command in {"PUT", "DELETE"}:
                entry_id = int(params.get("id", ["0"])[0])
                if self.command == "PUT":
                    field, value = validate_entry(json.loads(self.contents(32768)))
                    change = db.execute("UPDATE profile_entries SET field=?, value=? WHERE scope=? AND id=?",
                                        (field, value, scope, entry_id))
                else:
                    change = db.execute("DELETE FROM profile_entries WHERE scope=? AND id=?", (scope, entry_id))
                missing_entry = not change.rowcount
            entries = [dict(row) for row in db.execute(
                "SELECT id, field, value FROM profile_entries WHERE scope=? ORDER BY id", (scope,)
            )]
        if missing_entry:
            return self.reply(HTTPStatus.NOT_FOUND, {"error": "This entry no longer exists. Reload My profile."})
        self.reply(HTTPStatus.OK, {"entries": entries})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=4173)
    parser.add_argument("--database", type=Path, default=Path.home() / "Library/Application Support/College Mentor/profiles.sqlite3")
    options = parser.parse_args()
    initialize(options.database)
    with ThreadingHTTPServer(("127.0.0.1", options.port), Handler) as server:
        server.profile_path = options.database
        print(f"Mentor is running at http://localhost:{server.server_port}", flush=True)
        server.serve_forever()
