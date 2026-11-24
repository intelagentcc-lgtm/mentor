"use strict";

const ProfileEntries = (() => {
  const accept = ".pdf,.png,.jpg,.jpeg,.heic,.tif,.tiff,.bmp,.webp,.xlsx,.xls,.docx,.doc,.txt,.md,.csv,.tsv";
  const profiles = new Map();

  async function request(url, options = {}) {
    let response;
    try {
      response = await fetch(url, options);
    } catch {
      throw new Error("Open Mentor through the local Python server to use SQLite profiles.");
    }
    if (!response.headers.get("Content-Type")?.includes("application/json")) {
      throw new Error("Open Mentor through the local Python server to use SQLite profiles.");
    }
    const result = await response.json();
    if (!response.ok) throw new Error(result.error);
    return result;
  }

  function load(scope, fields, initial, onChange) {
    if (profiles.has(scope)) return profiles.get(scope);
    const endpoint = `/api/profile?scope=${encodeURIComponent(scope)}`;
    const json = (method, value) => ({
      method, headers: { "Content-Type": "application/json" }, body: JSON.stringify(value),
    });
    const seed = Object.keys(fields).flatMap((field) => {
      const value = initial[field];
      return (Array.isArray(value) ? value : [value]).filter((item) =>
        typeof item === "string" && item.trim() || typeof item === "number"
      ).map((item) => ({ field, value: String(item) }));
    });
    let entries = [];
    function update(result) {
      entries = result.entries;
      const grouped = {};
      for (const { field, value } of entries) (grouped[field] ||= []).push(value);
      onChange(grouped);
    }
    const ready = request(endpoint, json("POST", { entries: seed, seed: true })).then(update);
    ready.catch(() => {});

    const profile = {
      mount(root) {
        root.innerHTML = `
          <form class="entry-form entry-card">
            <h2 id="entry-form-heading">Add a profile entry</h2>
            <label for="entry-field">Profile field</label>
            <select id="entry-field" required></select>
            <label for="entry-value">Entry</label>
            <textarea id="entry-value" rows="4" required></textarea>
            <div class="entry-import">
              <label for="entry-file">Import text from a file</label>
              <input id="entry-file" type="file" accept="${accept}" />
              <p>Choose a field before saving. Review the extracted text and put each item on its own line.</p>
            </div>
            <div class="entry-actions">
              <button class="entry-primary" type="submit">Add entry</button>
              <button class="entry-cancel" type="button" hidden>Cancel</button>
            </div>
          </form>
          <p class="entry-status" role="status"></p>
          <div class="entry-list"></div>`;
        const form = root.querySelector("form");
        const title = root.querySelector("h2");
        const field = form.querySelector("select");
        const value = form.querySelector("textarea");
        const file = root.querySelector("#entry-file");
        const importControls = root.querySelector(".entry-import");
        const save = form.querySelector("[type=submit]");
        const cancel = root.querySelector(".entry-cancel");
        const status = root.querySelector(".entry-status");
        const list = root.querySelector(".entry-list");
        let entryId = null;
        let importing = false;
        let busy = true;

        for (const [key, label] of Object.entries(fields)) {
          field.add(new Option(label, key));
        }

        function setBusy(state) {
          busy = state;
          form.querySelectorAll("input, select, textarea, button").forEach((control) => { control.disabled = state; });
          list.querySelectorAll("button").forEach((button) => { button.disabled = state; });
        }

        function prepare(label, text, id = null) {
          entryId = id;
          importing = false;
          if (label) field.value = label;
          value.value = text;
          title.textContent = id ? "Edit profile entry" : "Add a profile entry";
          save.textContent = id ? "Save changes" : "Add entry";
          cancel.hidden = !id;
          importControls.hidden = Boolean(id);
        }

        function render() {
          list.replaceChildren();
          for (const [key, label] of Object.entries(fields)) {
            const section = document.createElement("section");
            section.className = "entry-card";
            const heading = document.createElement("h3");
            heading.textContent = label;
            section.append(heading);
            const items = entries.filter((entry) => entry.field === key);
            if (!items.length) {
              const empty = document.createElement("p");
              empty.textContent = "No entries yet.";
              section.append(empty);
            }
            for (const entry of items) {
              const row = document.createElement("div");
              row.className = "entry-row";
              const text = document.createElement("p");
              text.textContent = entry.value;
              const actions = document.createElement("div");
              actions.className = "entry-actions";
              const edit = document.createElement("button");
              edit.type = "button";
              edit.textContent = "Edit";
              edit.setAttribute("aria-label", `Edit ${label} entry`);
              edit.onclick = () => { prepare(entry.field, entry.value, entry.id); value.focus(); };
              const remove = document.createElement("button");
              remove.type = "button";
              remove.textContent = "Delete";
              remove.setAttribute("aria-label", `Delete ${label} entry`);
              remove.onclick = () => {
                if (!confirm("Delete this profile entry?")) return;
                return run(async () => {
                  update(await request(`${endpoint}&id=${entry.id}`, { method: "DELETE" }));
                  if (entry.id === entryId) prepare(null, "");
                  render();
                  status.textContent = "Entry deleted.";
                }).then(() => (list.querySelector("button") || value).focus());
              };
              actions.append(edit, remove);
              row.append(text, actions);
              section.append(row);
            }
            list.append(section);
          }
        }

        async function run(action) {
          if (busy) return;
          setBusy(true);
          try {
            await action();
          } catch (error) {
            status.textContent = error.message;
          } finally {
            setBusy(false);
          }
        }

        cancel.onclick = () => { prepare(null, ""); value.focus(); };
        file.onchange = () => {
          const selected = file.files[0];
          if (!selected) return;
          if (value.value.trim() && !confirm("Replace the unsaved entry with text from this file?")) {
            file.value = "";
            return;
          }
          run(async () => {
            status.textContent = "Reading file…";
            const extension = selected.name.match(/\.[a-z0-9]+$/i)?.[0] || "";
            const result = await request(`/api/profile/import?name=upload${encodeURIComponent(extension)}`, {
              method: "POST", headers: { "Content-Type": "application/octet-stream" }, body: selected,
            });
            importing = true;
            value.value = result.text;
            save.textContent = "Save imported entries";
            status.textContent = result.truncated ? "Preview limited to the first 40,000 characters. Review before saving." :
              "Review the extracted text before saving.";
          }).finally(() => { file.value = ""; value.focus(); });
        };
        form.onsubmit = (event) => {
          event.preventDefault();
          event.stopPropagation();
          run(async () => {
            const values = (importing ? value.value.split(/\r?\n/) : [value.value]).map((text) => text.trim()).filter(Boolean);
            if (!values.length || values.length > 100 || values.some((text) => text.length > 4000)) {
              throw new Error("Enter 1–100 items, up to 4,000 characters per item. Review or split longer imports before saving.");
            }
            const batch = values.map((text) => ({ field: field.value, value: text }));
            const result = entryId
              ? await request(`${endpoint}&id=${entryId}`, json("PUT", batch[0]))
              : await request(endpoint, json("POST", { entries: batch }));
            update(result);
            render();
            prepare(null, "");
            status.textContent = values.length === 1 ? "Entry saved." : `${values.length} entries saved.`;
          }).then(() => value.focus());
        };
        setBusy(true);
        ready.then(() => {
          if (!root.isConnected) return;
          render();
          setBusy(false);
        }).catch((error) => { status.textContent = error.message; });
        return {
          propose(key, text) { prepare(key, text); value.focus(); },
          async refresh() {
            await ready;
            if (busy) return;
            const result = await request(endpoint);
            if (busy) return;
            update(result);
            render();
          },
        };
      },
    };
    profiles.set(scope, profile);
    return profile;
  }

  return { load };
})();
