# Mentor

A responsive high school student mentor powered by a local open-weight language model.

The app defaults to the open-weight **Qwen 2.5 3B** on this Apple M1 MacBook Air
with 8 GB of unified memory. Choose **Qwen 2.5 1.5B** if you need quicker replies
or more memory for other apps. Ollama lists the quantized downloads at
[1.9 GB and 986 MB](https://ollama.com/library/qwen2.5/tags). Inference also
uses memory for context and runtime. Drafting and review run sequentially
with the same model on Ollama's loopback API. The optional profile includes
grade level, courses, recent grades, subjects,
interests, goals, and experience. You can also import UTF-8 TXT, CSV, or Markdown
notes up to 1,500 characters and review them before saving. Avoid adding identifying
or sensitive information.

Mentor screens student requests before drafting. A separate review pass checks the
draft and summary for age appropriateness, factual accuracy, calculations, and
faithfulness to student-provided information. The reviewer can return one corrected
draft, which must pass another review and a final appropriateness check. When a
draft cannot pass, Mentor asks for more context. Students can paste a short excerpt
from their class materials for the reviewer to use. The app performs all inference
locally and makes no web searches. The model can still miss errors or unsuitable
content, especially when it lacks a reliable source.

The high-school content policy blocks sexual content, nudity, violence, weapons,
drugs, alcohol, tobacco, vaping, gambling, and other inappropriate content.
All generated replies, summaries, quiz questions, and plan actions pass through
a local keyword filter and an Ollama safety classifier before display or saving.

After each exchange, Mentor updates a short summary of goals and next steps or
records a generic outcome. The profile and summary persist in browser storage
for the current browser and site address. Mentor uses the summary when answering
later questions. Select **Download mentoring summary** in the profile to save a
text copy. The summary replaces the need to store a full chat transcript.

## Set up on this Mac

1. Install Ollama for macOS from [ollama.com/download](https://ollama.com/download)
   and open it.
2. Download the recommended models:

   ```sh
   ollama pull qwen2.5:3b
   ollama pull qwen2.5:1.5b
   ```

3. In this folder, start the app:

   ```sh
   python3 -m http.server 4173 --bind 127.0.0.1
   ```

4. Visit [http://localhost:4173](http://localhost:4173). The page shows whether
   Ollama and the model are available.

The browser connects directly to Ollama's local API at `localhost:11434`. If your
Ollama installation blocks the page's origin, allow `http://localhost:4173` in its
`OLLAMA_ORIGINS` setting and restart Ollama.

## Mentoring modes

- **Plan my week** suggests two or three actions. Select **Use as weekly plan**
  to move a reviewed suggestion into the planner, then edit and save it. The
  planner holds one dated plan at a time. Mark actions complete and save before
  opening **Weekly check-in**, which uses saved progress to help adjust the plan.
- **Get a hint**, **See a worked example**, and **Practice with a quiz** provide
  different kinds of practice. Quiz mode gives one question at a time, reviews
  your answer, and suggests what to practice next. The active question stays
  available until you reload the page or start a new topic in quiz mode.
- **Ask about class materials** searches the text you paste or import in the
  sidebar for relevant passages. References such as `[S1]` point to line
  numbers in the text shown in the sidebar. Import UTF-8 TXT, CSV, or Markdown,
  up to 24,000 characters per field. Use **Save materials** to keep them across
  reloads.
- **Explore courses and careers** uses your interests and experience to suggest
  courses, clubs, careers, and projects. Add your school's catalog in the sidebar
  for local offerings and prerequisites with line references.
- **Mentoring memory** lets you read, edit, download, delete, or pause the chat
  summary. Pausing stops the app from reading and updating the summary during
  chat. The profile, weekly plan, and materials have their own save controls.
