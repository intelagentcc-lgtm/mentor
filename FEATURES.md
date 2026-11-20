# Mentor features

Mentor is a browser-based study and exploration assistant for high school students. See the [README](README.md) for local setup.

## Mentoring modes

| Mode | What it supports |
| --- | --- |
| **Ask Mentor** | Discuss schoolwork, study habits, interests, and next steps. Follow up on earlier work even after switching topics or reloading the page. |
| **Plan my week** | Get a suggested goal and two or three actions. Use **Use as weekly plan** to place a reviewed suggestion in the planner, where you can edit and save it. |
| **Weekly check-in** | Review completed actions, discuss what got in the way, and choose a next step. Start from the mode menu or the saved plan. |
| **Get a hint** | Get a next-step hint designed to leave the final answer for the student to work out. |
| **See a worked example** | Walk through a practice problem or a similar example for a graded assignment, with steps and checks. |
| **Practice with a quiz** | Get one question at a time, submit an attempt, and get feedback and a next question. **New quiz** resets the active question, which is held in the current page session. |
| **Ask about class materials** | Ask questions about an imported or pasted assignment, rubric, or study guide. Citations point to line ranges in the supplied text. |
| **Explore courses and careers** | Explore courses, clubs, careers, and projects based on interests and experience. A supplied school catalog supports cited answers about local offerings and prerequisites. |

## Profile, planner, and materials

- **Student profile.** Save an optional name, grade level from 9 through 12, courses, marks, selected subjects, hobbies and goals, and current experience or skill levels. Course and grade fields accept year-labeled history as text.
- **Profile notes.** Paste or import UTF-8 TXT, CSV, or Markdown notes up to 1,500 characters. Review the imported text before saving it with the profile.
- **Weekly planner.** Keep one dated plan with a goal, up to three editable actions, and completion checkboxes. Save the plan to make progress available at the next check-in.
- **Class materials and catalog.** Paste or import one class-material entry and one course catalog, each up to 24,000 characters. Both fields support UTF-8 TXT, CSV, and Markdown. Saving keeps them available after a reload. PDF, Excel workbooks, and image files require extracting their text before import.

## Conversation memory

- Mentor stores screened exchanges and an editable summary in browser storage. It uses clues from the latest message, saved questions, and earlier replies to retrieve up to three related exchanges, even after intervening topics or a reload.
- The current question guides the reply when interests change. A textbook or rubric follow-up can recover an earlier exchange and consult the supplied material again.
- **Mentoring memory** lets the student read, edit, and download the summary as text. **Pause chat memory** stops chat from using or updating the saved history and summary. **Delete chat memory** clears both. Profile, materials, and planner data have separate controls.

## Review, references, and local operation

- **Local models.** Choose Qwen 2.5 3B by default or the lighter Qwen 2.5 1.5B. The header shows whether the selected model is available. Drafting and review run through Ollama on the laptop.
- **Safety and answer review.** Mentor screens requests and checks drafts, summaries, quiz questions, and proposed actions before displaying or saving them. The review checks age appropriateness, factual claims, calculations, and citations. Safety concerns can trigger a prompt to contact a trusted adult or emergency services. Model checks can still miss errors or inappropriate content.
- **Study checks.** Some clear practice cases use fixed rules before review, including simple 4/4 rhythm counting, serving-ratio hints, zero-iteration Python loops, paper-folding fractions, and single-path circuits.
- **Public reference fallback.** A failed draft can get one retry. For predefined public topics, Mentor can look up Wikipedia excerpts and cite them when used. Only the predefined topic label is sent for that lookup. Profile information, chat text, and uploads stay local. When Mentor cannot give a reviewed answer, it asks a follow-up question.
- **Browser interface.** Collapsible profile, plan, materials, and memory panels are available alongside chat. On narrow screens, the profile opens in a separate panel. Press Enter to send or Shift+Enter to add a line.

The repository includes [fictional student test cases, transcripts, and evaluations](test-cases/README.md) covering topic changes, indirect follow-ups, multi-year coursework, and the app's mentoring modes.
