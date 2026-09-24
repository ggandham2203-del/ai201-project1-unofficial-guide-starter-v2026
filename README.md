# The Unofficial Guide

Name: Gayathri Gandham
Corpus: advice_threads

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

This project builds a question-answering system over a corpus of 23 student advice
threads. The threads cover topics such as commuting, changing majors, group
projects, internships, office hours, and other student experiences. The system
loads the documents, divides them into chunks, retrieves the most relevant
chunks for a question, and generates an answer using only the retrieved
information. It also uses a relevance cutoff so that questions outside the
corpus can be rejected instead of receiving an unsupported answer.

## Chunking Strategy

**Chunk size:** One complete thread/document per chunk
**Overlap:** None

I chose to keep each advice thread as one chunk because the documents are short
and each thread already groups related replies around one question. The five
sample chunks showed that the complete thread can be read as a coherent unit,
without sentences or replies being cut in the middle. I chose no overlap because
repeating the same thread across chunks would duplicate information and increase
the number of chunks unnecessarily.

The starter chunker produced 26 chunks from the 23 documents using fixed-size
character windows. My replacement produces 23 chunks, one for each advice
thread, using `chunker.py::split_documents`.


## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `thread_bike_commute.txt#0` — produced by: `chunker.py::split_documents`

```text
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.

--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.

--- reply 3 (22 votes) ---
Both true. I keep a cheap bike for September to November and walk the rest of the year. Total cost was about $120 for the bike and I don't care what happens to it.

--- reply 4 (5 votes) ---
If you do get one, the campus does free registration and it's the only reason I got mine back after it was taken.
```

**Chunk 2** — source: `thread_first_gen.txt#0` — produced by: `chunker.py::split_documents`

```text
THREAD: Anything specific for first-generation students?

--- reply 1 (33 votes) ---
The advising office has a specific programme and it is genuinely good, but it is opt-in and badly publicised. Ask for it by name.

--- reply 2 (41 votes) ---
The thing I'd say: the unwritten rules are the hard part, not the coursework. Ask about the unwritten rules explicitly. People are happy to explain them and nobody volunteers them.

--- reply 3 (16 votes) ---
Emergency fund for textbooks and travel exists and is not means-tested beyond a short form.
```

**Chunk 3** — source: `thread_laptop_specs.txt#0` — produced by: `chunker.py::split_documents`

```text
THREAD: How much laptop do I actually need for CS courses?

--- reply 1 (31 votes) ---
Less than the recommended spec page says. 16GB of RAM is the one number worth paying for; everything else you'll never notice.

--- reply 2 (18 votes) ---
Adding: the lab machines exist and are better than anything you'll buy. For the heavy assignments people just use those.

--- reply 3 (12 votes) ---
I did two years on an 8GB machine and it was fine until the last project, at which point it very much wasn't. 16 is the answer.
```

**Chunk 4** — source: `thread_office_hours_etiquette.txt#0` — produced by: `chunker.py::split_documents`

```text
THREAD: Is it weird to go to office hours with no specific question?

--- reply 1 (44 votes) ---
No, and this is the single most common thing first years get wrong. 'I'm following the lectures but I don't feel like I understand the shape of it' is a completely normal thing to say.

--- reply 2 (29 votes) ---
They're usually empty. You are doing the instructor a favour by turning up.

--- reply 3 (18 votes) ---
If it helps, treat it as a standing appointment. Go every week for a month and it stops feeling like a thing.
```

**Chunk 5** — source: `thread_professor_email.txt#0` — produced by: `chunker.py::split_documents`

```text
THREAD: Do professors actually answer email?

--- reply 1 (21 votes) ---
Varies enormously. General rule I've found: if the syllabus states a response window, it's honoured. If it doesn't, assume 48 hours and don't panic before then.

--- reply 2 (33 votes) ---
Office hours are dramatically more effective than email for anything that takes more than two sentences to answer. They're also usually empty.

--- reply 3 (15 votes) ---
Empty office hours is the biggest unused resource here and I say that having wasted a year not going.
```

## Sample Answer

**Question:**

When do large employers typically recruit for summer internships?

**Answer:**

Large employers close applications for summer internships in October and
November for the following summer.

Source: `thread_internship_timing.txt`

**My relevance cutoff:** 0.6

I tested five questions covered by the corpus and five questions outside the
corpus. The five in-corpus questions had best distances from 0.302 to 0.493,
while the five out-of-corpus questions had best distances from 0.787 to 0.930.
The gap between the two groups supported keeping the cutoff at 0.6.

| Question | In corpus? | Best distance |
|---|---|---:|
| Where is covered bike parking available, and when does it tend to fill up? | Yes | 0.493 |
| What should a student consider when changing majors in their second year? | Yes | 0.324 |
| What should students do when a group-project member stops contributing? | Yes | 0.359 |
| When do large employers typically recruit for summer internships? | Yes | 0.302 |
| How long should a student generally wait for a professor's email response if the syllabus doesn't specify a response window? | Yes | 0.312 |
| What is the capital of Mongolia? | No | 0.890 |
| How do I change the oil in a diesel engine? | No | 0.930 |
| Who won the 1994 World Cup? | No | 0.787 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.828 |
| How do I write a for loop in Rust? | No | 0.871 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1. Acceptance criteria**

I used AI to pressure-test the acceptance criteria I drafted for the project.
The initial criteria included ideas such as checking whether answers contained
the expected information and whether unsupported questions were rejected. AI
pointed out where some of these ideas were too vague to test and helped me
make the targets observable, such as using 4 of 5 questions and specifying
what should happen for low-confidence retrieval. I kept the actual criteria
and targets based on my project decisions.

**2. Chunking strategy**

I used AI to review the starter chunks and think through whether the fixed-size
chunking strategy fit my advice-thread corpus. The starter produced complete
short threads in many cases, and the corpus naturally organizes information as
a thread question followed by related replies. Based on that observation, I
chose to keep each complete thread as one chunk with no overlap rather than
splitting or duplicating the thread across multiple chunks.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

Produced by `python run_eval.py --label before`, run on 2026-09-23. Full
transcript (every question, every run): `results/run_2026-09-23_2016_before.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks contain valid, understandable information | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 5. Low-confidence questions rejected at the retrieval cutoff | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

Criteria 1 and 2 come from `scorer.py::judge` scoring the three real runs per
question (caching off). Criteria 3 and 5 share the same evidence — the same
five `OUT_OF_SCOPE` questions through `gate.py::check` — because both are
really testing the same gate mechanism, just described two different ways;
that's a single deterministic pass, so the same number goes in all three run
columns. Criterion 4 comes from `app.py::cmd_chunks -n 5`, also a single
deterministic sample, not three runs.

### Real output

**Criteria 1 & 2 — retrieval and sourcing**, from `store.py::search` and
`generate.py::answer_from_chunks`, via `run_eval.py::run_once`:

```
Question: When do large employers typically recruit for summer internships?
Best distance: 0.3019 (passed the gate)
Sources retrieved: thread_clubs.txt, thread_first_gen.txt, thread_first_year_regret.txt, thread_internship_timing.txt, thread_professor_email.txt

Large employers close applications for summer internships in October and November for the following summer (thread_internship_timing.txt).
```

```
Question: What should students do when a group-project member stops contributing?
Best distance: 0.3593 (passed the gate)
Sources retrieved: thread_first_year_regret.txt, thread_group_project.txt, thread_late_work.txt, thread_office_hours_etiquette.txt, thread_roommate_conflict.txt

Based on the provided documents, students should document things early so they have something written down if they need to go to the instructor (thread_group_project.txt). Additionally, students should raise the issue to instructors before the deadline rather than after, as instructors will most likely adjust individual grades beforehand (thread_group_project.txt). Finally, students should split the work into pieces that can be handed off so that one person's absence does not sink the entire project (thread_group_project.txt).
```

**Criteria 3 & 5 — the relevance gate on out-of-corpus questions**, from
`gate.py::check`, via `run_eval.py::check_out_of_scope`, cutoff 0.6:

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.890 | refused |
| How do I change the oil in a diesel engine? | 0.930 | refused |
| Who won the 1994 World Cup? | 0.787 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.828 | refused |
| How do I write a for loop in Rust? | 0.871 | refused |

**Criterion 4 — sampled chunks**, from `chunker.py::split_documents`, via
`app.py::cmd_chunks -n 5` (same 5-chunk sample as the Unit 1 Sample Chunks
section above — the chunker hasn't changed):

```
Chunk 1  |  source: thread_bike_commute.txt#0  |  produced by: chunker.py::split_documents
THREAD: Is a bike worth it for a 20 minute walk commute?

--- reply 1 (14 votes) ---
Yeah. Cuts an 18 minute walk to about 6. The thing nobody mentions is storage — covered bike parking exists at three buildings and is full by 9am at all three.
--- reply 2 (9 votes) ---
Counterpoint, I sold mine. Between November and March the paths are either icy or salted and salt destroys a drivetrain in one season.
```

```
Chunk 5  |  source: thread_professor_email.txt#0  |  produced by: chunker.py::split_documents
THREAD: Do professors actually answer email?

--- reply 1 (21 votes) ---
Varies enormously. General rule I've found: if the syllabus states a response window, it's honoured. If it doesn't, assume 48 hours and don't panic before then.
```

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
