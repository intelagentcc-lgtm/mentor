# Implicit-recall evaluation

The expanded suite contains 12 fictional student profiles, 64 sessions, and
76 prompts. Each profile adds a new interest on a later visit, then asks about
earlier work using indirect clues. Twelve existing return prompts also omit
the earlier session name. Each prompt still includes relevant courses from
every grade year in the student's record.

The live rerun used Qwen 2.5 3B on local Ollama. The harness exercised Mentor's
chat handler and kept the same storage during a session. Between sessions it
started a new app instance with the same student's saved browser data.

Mentor ranks prior exchanges using clues in both the student messages and
Mentor replies. Uncommon matching words and related terms can bring an older
exchange back into context even when several topics came up in between. When
a class-material exchange is relevant, Mentor can use the current uploaded
passage again. The app supplies up to three exchanges to the local model.

Separate regression checks matched eight paraphrased questions to older
topics, excluded unrelated history, and checked retrieval candidates for an
ambiguous reference. A chat-handler check verified that “firsthand accounts”
recovered an earlier rubric exchange and sent the current rubric to the model.

The run also exposed a wrong series/parallel label and broken fraction
formatting. The app now checks a single-current-path example against the
series-circuit rule and renders numeric fractions in plain text. Both final
questions were rechecked using the recorded prior exchanges.

The Python follow-up now explains zero iterations conditionally on the
student's loop using `range(n)`. The paper-folding reply now asks the
learner to count four equal pieces and compare two quarters with one half.
Those replies were rechecked with the preceding exchanges.

## Results

All 76 prompts matched their fixtures and have a recorded reply. Mentor
gave 69 substantive replies and seven fallbacks. A separate replay of the
recorded conversation history found an expected earlier exchange in the
three retrieved candidates for all 12 newly added implicit returns. The
highest-ranked exchange was one of the expected ones in 10 of 12.

- [Cameron](responses/10-03.md) asked about a strong shadow after an astronomy
  detour. Mentor returned to the photography experiment and suggested
  recording the light source, angle, distance, and exposure.
- [Drew](responses/10-04.md) mentioned only a half-cup and 12. Mentor recovered
  the earlier 8-to-12 recipe scaling task and worked through the fraction.
- [Alex](responses/11-01.md) described two bulbs and one route. The rechecked
  response correctly says that one current path through both bulbs is series.
- [Taylor](responses/10-02.md) still got a generic question after asking if
  two firsthand accounts and one textbook chapter met the total. The
  selector retrieved the correct rubric exchange behind two other candidates.
- [Avery](responses/09-01.md) recovered the bridge topic, but the reply did
  not clearly hold span and load placement constant. [Parker](responses/11-02.md)
  recovered the editing topic, but the answer invented a sample caption and
  presented it as the original.

Retrieval and response quality were measured separately. A match in memory
does not guarantee that the reply uses it accurately or mentions every course.
