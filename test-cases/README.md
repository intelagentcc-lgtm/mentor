# Mentor student test cases

The suite contains 12 fictional students, four per grade, and 64 sessions with
76 student prompts. Each student explores a different interest within the first
session, then starts another interest on a later visit. Two prompts per student
return to earlier work through clues, without naming a prior session.
Each JSON file includes the student's courses and percentages grouped by
grade, hobbies, experience, career interests,
ordered prompts, and expected behavior. Grade 10 cases include grades 9–10,
and grade 11 cases include grades 9–11. The runner saves each student's
full course history before the first session. The `course_references_by_grade`
field lists courses to consider when evaluating a reply. It stays outside
the student prompt. Some cases also
include sample class materials, catalog text, or a saved check-in plan.

The [earlier evaluation](evaluation.md) covers the single-year cases. The
[topic-switch evaluation](topic-switch-evaluation.md) covers the previous run.
The [implicit-recall evaluation](implicit-recall-evaluation.md) covers the
earlier prompts that repeated the coursework. The
[saved-profile evaluation](saved-profile-evaluation.md) covers the current run.

| Grade | Student | Career interests | Case | Conversation |
| --- | --- | --- | --- | --- |
| 9 | Avery | Mechanical engineering | [09-01](09-01.json) | [Transcript](responses/09-01.md) |
| 9 | Jordan | Illustration and journalism | [09-02](09-02.json) | [Transcript](responses/09-02.md) |
| 9 | Morgan | Audio production and music education | [09-03](09-03.json) | [Transcript](responses/09-03.md) |
| 9 | Casey | Landscape design | [09-04](09-04.json) | [Transcript](responses/09-04.md) |
| 10 | Riley | Software engineering | [10-01](10-01.json) | [Transcript](responses/10-01.md) |
| 10 | Taylor | Public policy and journalism | [10-02](10-02.json) | [Transcript](responses/10-02.md) |
| 10 | Cameron | Product design and photography | [10-03](10-03.json) | [Transcript](responses/10-03.md) |
| 10 | Drew | Food science and hospitality | [10-04](10-04.json) | [Transcript](responses/10-04.md) |
| 11 | Alex | Electrical engineering | [11-01](11-01.json) | [Transcript](responses/11-01.md) |
| 11 | Parker | Communication design and editing | [11-02](11-02.json) | [Transcript](responses/11-02.md) |
| 11 | Quinn | Sports analytics and media production | [11-03](11-03.json) | [Transcript](responses/11-03.md) |
| 11 | Skyler | Elementary teaching and library services | [11-04](11-04.json) | [Transcript](responses/11-04.md) |

Start with a fresh browser profile for each case. Enter the course names and
percentages from `courses_and_grades_pct_by_grade` in **Courses** and
**Recent grades**, with a label for each year. Enter hobbies and career interests in
**Interests & goals** and experience in **Experience and skill levels**. Select
**Save my profile** once before session 1. Set the
given mode before each prompt. Apply any supplied material or weekly plan before
the session that uses it. Submit any `follow_ups` in the same tab after the
opening prompt. Reload the page between sessions while keeping the student's
browser storage.

The [responses](responses/) folder holds the expanded conversations. The
recording harness used the app's chat handler and browser storage logic with a
simulated browser interface. Model requests used Qwen 2.5 3B through local
Ollama. The transcripts include fallback replies where the app returned them.
Avery's transcript was rerun after the bridge question was rewritten as a
plain measurement question. It also shows the new context labels underneath
Mentor's replies.
