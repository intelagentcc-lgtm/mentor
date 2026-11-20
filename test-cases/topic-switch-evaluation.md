# Topic-switch evaluation

The expanded suite tests 12 fictional student profiles across 40 sessions
and 52 prompts. Each profile has a same-session topic change and a later
return to an earlier topic. The run used the app's chat handler with local
Qwen 2.5 3B. The harness kept the tab state for follow-ups and started a new
app instance with the student's saved browser storage for each later session.

The retrieval checks also covered a topic older than the three most recent
exchanges, a new topic with unrelated saved history, an implicit follow-up,
persistence beyond 24 exchanges, and the pause and delete controls. A chat
handler check confirmed that removing an old career interest from a prompt
does not change the student's saved profile or course record.

## Results

All 52 prompts matched their fixture and have a recorded reply. Mentor gave
43 substantive replies and nine fallbacks. Substantive replies varied in how
well they used prior work and the course record.

- [Avery](responses/09-01.md) got a Moon-observation project during the switch
  and returned to measuring a cardboard bridge after later sessions. The
  final reply still inferred how Avery had built the bridge.
- [Parker](responses/11-02.md) got a plant-observation project that connected
  all three grade years to the new interest. The later portfolio question
  still received a generic probe.
- [Skyler](responses/11-04.md) got a paper game after a reload and later
  returned to teaching fractions with paper shapes. The game and check-in
  drew on child development and early education but omitted the grade 9
  course connection.
- [Morgan](responses/09-03.md) and [Cameron](responses/10-03.md) received
  generic probes for photography and music production. A few other
  same-session replies answered the new topic but leaned on the prior
  interest more than the current request warranted.

The output count measures completed replies. It does not mean that every
reply met its full expected behavior.
