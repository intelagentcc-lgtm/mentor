# Mentor regression evaluation

Each transcript records one prompt and one visible reply per session. The run
used the app's chat handler and real Qwen 2.5 3B inference on local Ollama.
Within each case, subsequent sessions could use the same student's saved
memory. The six-exchange limit, reload, pause and delete behavior were also
checked with simulated model replies.

## What the original run revealed

- Mentor read an editable summary on later turns. It did not keep the actual
  questions and replies, and generic failure notes could push useful details out
  of the summary. Both Avery's bridge check-in and Jordan's Earth Science
  follow-up returned generic requests for an assignment.
- The input filter redirected ordinary academic questions, including a Python
  loop quiz and a school catalog lookup. Some model output failures surfaced as
  instructions to restart Ollama.
- The review approved an incorrect rhythm count. The circuit plan also credited
  Alex with a calculation the app had only proposed as practice.
- The original rubric lookups did not return the requested requirements with
  citations, even though each requirement was in the supplied material.

## Changes tested in the rerun

Mentor now keeps recent screened exchanges as well as its summary. A new
rubric lookup leaves unrelated chat out of the drafting context. A draft that
fails checks can be regenerated once. When a predefined public topic is
relevant, Mentor can fetch a Wikipedia excerpt for that retry. It sends only the
public topic label. Class and catalog requirements rely on supplied sources.
When the retry cannot produce a reviewed answer, Mentor asks a question for the
selected mode. The final local review checks safety and accuracy. The simple
4/4 example and the serving-ratio hint also use deterministic calculations or
rules before that review.

## Results

| Visible outcome | Original | Rerun |
| --- | ---: | ---: |
| Substantive reply | 18 | 34 |
| Verification fallback or probing question | 12 | 5 |
| Generic scope redirect | 6 | 0 |
| Request error | 3 | 0 |
| Total sessions | 39 | 39 |

A substantive reply can still miss an expectation. This count measures what
the student saw, and the following review records specific quality issues.

| Case | What improved | What still needs work |
| --- | --- | --- |
| [09-01](responses/09-01.md) | The bridge check-in acknowledges the build and recommends recording two load trials. The next reply stays on the bridge topic. | The first reply assumes mechanical engineering experience. The proposed experiment exceeds the two short blocks, and the geometry reply gives several ideas instead of one controlled variable. |
| [09-02](responses/09-02.md) | Mentor gives an opening hint and a useful Earth Science study-guide idea based on drawing and writing. | The first reply suggests two illustration activities and gives little distinct journalism practice. |
| [09-03](responses/09-03.md) | The check-in addresses the rhythm difficulty. The worked example identifies six note onsets across four beats. | The plan could assign a concrete goal to each of the three 15-minute sessions. |
| [09-04](responses/09-04.md) | The garden activity fits the sketchbook and the area hint preserves the calculation for the student. The cited rubric answer correctly says at least four different plants. | The landscape activity could start with one smaller sketch. |
| [10-01](responses/10-01.md) | The course and prerequisite are correct and cited. The Python quiz provides one unanswered question. | Planning and check-in fall back to questions, despite the two hours and the reported loop progress. Both sessions were more useful in the original run. |
| [10-02](responses/10-02.md) | The reply cites the exact requirement of three sources with at least one primary source. It also gives a usable comparison hint. | The career comparison falls back to a question instead of suggesting a podcast or debate project. |
| [10-03](responses/10-03.md) | The example correctly scales the photo to 8 by 12. The plan carries forward the photography context and suggests two lighting setups. | The experiment could explicitly hold camera settings, product position, and framing constant. |
| [10-04](responses/10-04.md) | The hint sets up target servings over original servings. The check-in focuses on fractional recipe quantities. | The initial food-science question falls back to a probe. The practice example needs to restate the original serving count to be solvable on its own. |
| [11-01](responses/11-01.md) | The current calculation is 3 A. The plan avoids crediting unreported work, and the check-in refers to the completed diagrams. | The first reply still fails to name the catalog course and its alternative prerequisites. |
| [11-02](responses/11-02.md) | The cited rubric reply correctly requires a fair counterargument and an evidence-based response. The portfolio reply suggests privacy-preserving samples. | The first project emphasizes layout and typography more than comparing design with editing. |
| [11-03](responses/11-03.md) | A small project now combines data and video editing. The quiz gives one unanswered mean question. | The last reply lists three actions even though the student requested two. |
| [11-04](responses/11-04.md) | The project compares library and teaching work. The plan sticks to math, and the check-in builds on the student's use of paper shapes. | The check-in could explicitly show quarters by folding each half again. |

The Wikipedia endpoint returned results for a public topic in a separate
live check. Tests with simulated replies verified that only the predefined
label leaves the browser and that an unavailable lookup falls back to a
probing question. The 39 saved conversations contain class and catalog
citations. None displays a Wikipedia citation.
