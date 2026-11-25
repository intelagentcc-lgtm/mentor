# Mentor

A high school mentorship app with a guided Studio demo and an Ollama-powered local workspace.

See the [feature guide](FEATURES.md) for the full list of supported capabilities.

The app defaults to **Qwen3-4B-Instruct-2507**, a
[2.5 GB quantized download](https://ollama.com/library/qwen3/tags).
**Qwen 2.5 1.5B** is a lighter option, and **Qwen 2.5 3B** remains available
for research or evaluation under its [license](https://huggingface.co/Qwen/Qwen2.5-3B-Instruct/blob/main/LICENSE).
Inference also uses memory for context and runtime. Drafting and review run sequentially
with the same model on Ollama's loopback API. **My profile** supports multiple entries per field. Add an entry by hand or import a file, review the extracted text, and choose the field before saving.

Mentor screens student requests before drafting. A separate review pass checks the
draft and summary for age appropriateness, factual accuracy, calculations, and
faithfulness to student-provided information. A failed draft gets one retry and
must pass the same review. When a public reference could help, Mentor searches
Wikipedia using a predefined topic label and cites references it uses. The lookup
sends only the public topic label. Profile fields, uploaded material, and chat
text stay on your laptop. School-specific questions use the supplied school
materials. If the retry fails, Mentor asks a question specific to the selected
mode. The model can still miss factual errors or unsuitable content.

The high-school content policy blocks sexual content, nudity, violence, weapons,
drugs, alcohol, tobacco, vaping, gambling, and other inappropriate content.
All generated replies, summaries, quiz questions, and plan actions pass through
a local keyword filter and an Ollama review before display or saving.

Mentor saves screened exchanges with their date and time in the local SQLite
database and keeps a short editable summary in browser storage. Existing browser
history is imported when you open the local AI workspace at the same address.
Mentor reads your saved profile and retrieves up to three related exchanges,
even if other topics came up in between or the page was
reloaded. It looks for clues in the current wording and in past questions and
replies, so a student can pick up an earlier task without naming the session.
When several earlier topics fit, Mentor is instructed to ask a focused question.
A new rubric lookup focuses on the supplied assignment rather than
unrelated chat. Select
**Download summary** for a text copy of the summary, or **Delete chat memory**
to remove both the summary and saved exchanges.

## Set up on this Mac

1. Install Ollama for macOS from [ollama.com/download](https://ollama.com/download)
   and open it.
2. Download the default model:

   ```sh
   ollama pull qwen3:4b-instruct-2507-q4_K_M
   ```

   Download either of the other models if you plan to select it:

   ```sh
   ollama pull qwen2.5:3b
   ollama pull qwen2.5:1.5b
   ```

3. In this folder, start the app:

   ```sh
   python3 -m venv .venv
   .venv/bin/python -m pip install -r requirements.txt
   .venv/bin/python server.py
   ```

4. Visit [http://localhost:4173](http://localhost:4173) for the Studio demo. Switch
   between Maya and Alex to explore the guided workflows without Ollama.
5. Select **Open local AI mentor** or visit [the local AI workspace](http://localhost:4173/local-ai.html)
   for Ollama chat. Its header shows whether Ollama and the model are available.

The browser connects directly to Ollama's local API at `localhost:11434`. If your
Ollama installation blocks the page's origin, allow `http://localhost:4173` in its
`OLLAMA_ORIGINS` setting and restart Ollama.

## Profile storage and imports

- Use **My profile** to add, view, edit, or delete individual entries. A file import
  extracts text into an editable preview. Each nonempty line becomes its own entry
  in the selected field when saved. Check OCR results and spreadsheet values first.
- Supported files include PDF, common image formats (including JPEG, PNG, and HEIC),
  Excel (.xlsx, .xls), Word (.docx, .doc), and UTF-8 text (.txt, .md, .csv, .tsv).
  PDF and image extraction uses local Apple frameworks through the Swift
  command-line tools. Run `xcode-select --install` if those tools are missing.
- The default database is `~/Library/Application Support/College Mentor/profiles.sqlite3`.
  Existing browser profiles are imported once when you open the app at the same
  address you used before. The Studio's Maya and Alex profiles stay separate from
  the local AI profile. Plans and the editable chat summary use browser storage.
- Profile editing and document imports require the local Python server. The static
  GitHub Pages deployment can display the Studio demo and its example profiles.

## Studio demo

The Studio demo provides guided questions, project ideas and reflections, an
admissions plan draft you can approve, and progress tracking. Its fictional
student profiles and browser-saved data are separate from the Ollama workspace.

## Local AI workspace

- **Mentor** opens the active conversation and connects to Ollama.
- **My projects** lets you choose a conversation, save work and a next action, and reopen the thread.
- **College plan** holds your weekly plan and starts progress check-ins.
- **My profile** holds your student profile, school materials, and mentoring memory.

## Mentoring modes

- **Plan my week** suggests two or three actions. Select **Use as weekly plan**
  to move a reviewed suggestion into the planner, then edit and save it. The
  planner holds one dated plan at a time. Mark actions complete and save before
  opening **Weekly check-in**, which uses saved progress to help adjust the plan.
- **Get a hint**, **See a worked example**, and **Practice with a quiz** provide
  different kinds of practice. Quiz mode gives one question at a time, reviews
  your answer, and suggests what to practice next. The active question stays
  available until you reload the page or start a new topic in quiz mode.
- **Ask about class materials** searches the text you paste or import under
  **My profile** for relevant passages. References such as `[S1]` point to line
  numbers in the text shown under **My profile**. Import UTF-8 TXT, CSV, or Markdown,
  up to 24,000 characters per field. Use **Save materials** to keep them across
  reloads.
- **Explore courses and careers** uses your interests and experience to suggest
  courses, clubs, careers, and projects. Add your school's catalog under **My profile**
  for local offerings and prerequisites with line references.
- **Mentoring memory** lets you read, edit, and download the summary. Pausing
  stops Mentor from using or updating the summary and recent exchanges during
  chat. The profile, weekly plan, and materials have their own save controls.
