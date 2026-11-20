# Mentor student test cases

The suite contains 12 fictional students, four per grade, and 39 sessions with
one prompt and reply per session. Each JSON file includes the student's courses
and percentages, hobbies, experience,
career interests, ordered prompts, and expected behavior. Some cases also
include sample class materials, catalog text, or a saved check-in plan.

The [rerun evaluation](evaluation.md) compares the original behavior with the
replacement transcripts and identifies remaining quality gaps.

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

Start with a fresh browser profile for each case. Map the course names and
percentages to **Courses** and **Recent grades**, hobbies and career interests to
**Interests & goals**, and experience to **Experience and skill levels**. Set the
given mode before each prompt. Apply any supplied material or weekly plan before
the session that uses it. Keep mentoring memory available between sessions for
the same student.

The [responses](responses/) folder contains the recorded student prompts and
Mentor replies. The recording harness used the app's chat handler and browser
storage logic with a simulated browser interface. Model requests used Qwen 2.5
3B through local Ollama. The transcripts include any fallback replies; use the
expected behavior in each test case when evaluating the results.
