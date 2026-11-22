# Earlier saved-profile evaluation

This evaluation covers the saved-profile and context-label run at commit
`2a37759`. See the [session-depth evaluation](session-depth-evaluation.md) for
the latest cases and transcripts.

This run tests whether Mentor can use a student profile without the student
repeating it. The suite covers 12 fictional students, 64 sessions, and 76
prompts. For each student, the harness initializes the browser's saved profile
once with the student's grade, year-labeled courses and marks, interests, and
experience. Each later session starts a new app instance with the saved browser
data. The runner verifies that the profile is still present and unchanged after
every session. All model calls use Qwen 2.5 3B through local Ollama.

The repeated coursework blocks were removed from the student prompts.
`course_references_by_grade` is evaluation metadata. The student can still
refer to a subject naturally when it belongs to the question itself.

A separate app test verified that an existing profile loads from local
storage, that unsaved edits stay out of chat requests, and that saving edits
affects the next reply. It also verified that pausing chat memory leaves the
profile available, that the optional name stays out of model requests, and
that class-material questions receive the profile alongside the source.

## Full-suite results before context labels

Avery's linked transcript was subsequently refreshed with plain questions and
the context labels. These counts describe the earlier full-suite run.

All 76 student prompts match the fixtures without the repeated coursework
blocks. Mentor gave 66 substantive replies and 10 fallbacks.

- Avery (`09-01`) asked for a project based on classes and grades
  without listing them. Mentor brought in Geometry and Introduction to
  Engineering and suggested a robotic arm. It also attributed programming
  knowledge to a course when the profile reported it separately as experience.
- Jordan (`09-02`) received illustration and journalism ideas tied
  to Digital Art even though the question did not name the course.
- Alex (`11-01`) received the catalog prerequisites with a citation
  and a connection to saved circuit and CAD experience.
- Riley (`10-01`) still received a generic follow-up on the catalog
  question. A saved profile supplies context, and individual answers can still
  miss the requested detail.

## Avery rerun with context labels

All six sessions and seven prompts were rerun on local Ollama. The student
asks for a beginner project and later for a measurement to record. Neither
question restates a course or asks Mentor to look at the profile. The first
reply uses the student's robotics and Arduino experience. The bridge check-in
identifies the earlier bridge-plan exchange and saved weekly plan in its
**Context used** label. The remaining replies show **Context checked** with
the available sources of context.

The bridge measurement reply recommends recording the maximum load. The
final experimental-controls reply still gives weak advice about which
variable to hold constant. The context label shows what the app consulted
and cannot establish that every recommendation is accurate.
