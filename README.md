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

Mentor saves screened exchanges and a short editable summary
in browser storage for the current site address, as space allows. It retrieves up to three
related exchanges, even if other topics came up in between or the page was
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
- **Mentoring memory** lets you read, edit, and download the summary. Pausing
  stops Mentor from using or updating the summary and recent exchanges during
  chat. The profile, weekly plan, and materials have their own save controls.
