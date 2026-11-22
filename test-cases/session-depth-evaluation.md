# Session-depth evaluation

The expanded suite covers 12 fictional students, 79 sessions, and 115 prompts.
Each case adds a focused task, a deeper follow-up in the same app instance, and
a message asking about two topics. Avery also switches topics across later
sessions and returns to two earlier topics in session 10. The student profile
is loaded from saved browser storage, and the harness reloads the app between
sessions while keeping the student's history.

The live run used Qwen 2.5 3B through local Ollama. Separate app checks verified
that a two-topic question can retrieve both a current-session exchange and an
older one, that an implicit reference can use the latest in-session turn, and
that a computed answer for one question does not skip the other question.
The app also requires a separate answer for each clearly signposted question
and reviews the combined reply before displaying it. A recalled rubric can
carry a question number to keep its requirements attached to the right task.

The run was followed by targeted rechecks as defects became apparent. This
includes the mixed music and gardening question, the garden and flipbook
question, the Python range example, and the recipe and room-layout question.

## Results

All 115 prompts matched their fixtures and have a recorded reply. The run
produced 96 substantive replies and 19 fallbacks. Of the 13 questions that
combined two subjects, nine received an answer to both and four received a
fallback. Eleven of the 12 deeper follow-ups received a substantive reply.
These are coverage counts. Some replies still missed details or gave weak
advice.

| Case | What the transcripts show |
| --- | --- |
| [Avery](responses/09-01.md) | Session 10 covered the poster headline and the bridge span. The reply unnecessarily tied the poster to bridge design. The earlier fair-test follow-up could have specified a fixed load position more clearly. |
| [Jordan](responses/09-02.md) | Mentor gave one criterion for editing the article opening and separately suggested atmospheric perspective for the stage sketch. |
| [Morgan](responses/09-03.md) | The rhythm follow-up gave a next tempo step. The combined rhythm and plant question was initially redirected and still fell back after the screening recheck. |
| [Casey](responses/09-04.md) | The recheck gave distinct garden and flipbook advice. The placement of the rubric citation could still make its scope clearer. |
| [Riley](responses/10-01.md) | The rechecked follow-up correctly says that a loop over `range(1)` prints `0`. The combined zero-input and photography question still fell back. |
| [Taylor](responses/10-02.md) and [Cameron](responses/10-03.md) | Both deeper follow-ups received advice. The combined questions fell back. Taylor's reply also called the podcast a presentation. |
| [Drew](responses/10-04.md) | The rechecked compound question gave two numbered answers, with the correct 3/4 cup amount and separate measurements for a room sketch. |
| [Alex](responses/11-01.md) | Mentor correctly identified the single path as series and gave a separate animation idea. The suggested frame order could be clearer. |
| [Parker](responses/11-02.md), [Quinn](responses/11-03.md), and [Skyler](responses/11-04.md) | Each received two numbered answers covering the requested topics. Skyler's preceding follow-up also used the paper-folding context to distinguish quarters from halves. |

The biggest remaining gaps in this run are generic fallbacks on some mixed
academic messages and occasional cross-topic references. The numbered answer
format prevents a draft with a missing answer from being shown in clearly
signposted multi-question messages. Accuracy still depends on the local review.
