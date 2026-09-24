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

**3. Fixing `scorer.py`**

The version I built in class only checked whether the expected phrase
appeared in the final generated answer, ignoring the `results` parameter
entirely. I asked AI to point out the gap; it explained that checking the
answer instead of the chunks conflates two different failure modes —
retrieval missing the fact, and generation mangling a fact that was actually
retrieved — which is exactly what Milestone 3 asks you to tell apart. I used
the version that checks the retrieved chunks instead.

**4. Diagnosing "no misses"**

Every criterion passed cleanly on the first real run, and rather than accept
that at face value I asked AI to help me think about why. It pointed out that
top-k=5 pulls back nearly a quarter of my 23-chunk corpus on every question,
which could pass criterion 1 by breadth rather than precision. That became my
Milestone 3 diagnosis and my Milestone 4 improvement (cutting top-k to 2). The
result disconfirmed half of it — retrieval held up even at top-k=2 — which I
also wrote down rather than only reporting the part of the hypothesis that
turned out right.

**5. Fact-checking a phrasing difference**

Before flagging a wording difference in one "after" answer ("October and
November of the preceding year" vs. the source's "for the following summer")
as a possible hallucination, I asked AI to check it against the actual source
document rather than assume. It turned out to be an equivalent phrasing from
a different reference point, not an error — but the check is what surfaced
the real gap noted in What's Still Broken: nothing in my criteria would have
caught it if it had been wrong.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

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

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer (4 of 5) | MET | All 3 runs found the expected phrase in the retrieved chunks for all 5 questions (15/15) — clears the target with room to spare. |
| 2 | Every answer names a source (5 of 5) | MET | All 15 answers across the 3 runs named a source, either inline (`(thread_x.txt)`) or with a `Source:` line — 5/5 on every run. |
| 3 | Gate stops out-of-corpus questions (4 of 5) | MET | All 5 out-of-corpus questions were refused by the gate, clearing 4-of-5. |
| 4 | Sampled chunks are a complete thread with no cut-off sentences — revised (4 of 5) | MET | 5/5 sampled chunks are the full thread, start to end — one-thread-per-chunk means there's no character-window split to cut a sentence mid-word. This is a deliberately easier bar than the original wording; see the revision in `criteria.md` for why I swapped a subjective target for a mechanical one rather than a stricter one. |
| 5 | Low-confidence questions rejected at cutoff (4 of 5) | MET — same evidence as #3 | Same 5 out-of-corpus questions, same gate result. `criteria.md` describes criterion 3 ("out of corpus") and criterion 5 ("low-confidence") as two different things, but I don't have evidence that actually separates them — both come from the same gate check on the same questions. I'm calling this MET honestly, but it's one confirmation, not two. See What I'd Do Differently. |

No misses this round. Per the assignment's own warning, that's a sign to check whether the bar was set safe rather than a sign the system is excellent — see Diagnoses below for what I think is actually going on and what I'd tighten.

## Diagnoses

No misses this round, so there's nothing to trace back to a broken stage. What
I want to be honest about instead is *why* nothing missed, because I don't
think it's because retrieval is unusually precise.

**The mechanism: top-k=5 over a 23-chunk corpus is barely a filter.**
`chunker.py::split_documents` produces one chunk per thread, 23 chunks total
for `advice_threads`. Every question in `run_eval.py` retrieves `TOP_K = 5`
chunks via `store.py::search` — almost a quarter of the entire corpus — before
the gate or the model ever narrows anything down. Criterion 1 asks whether the
retrieved chunks include one that contains the answer, but with a net that
wide over a corpus that small, a chunk only loosely related to the question
has a real chance of being swept in alongside the one that actually answers
it. The best distances in the run log (0.30–0.49) are genuinely tight, so
retrieval isn't failing — but the criterion as measured can't tell "retrieval
is precise" apart from "retrieval is wide enough that precision barely
matters at this corpus size." Stage: retrieval. This is the criterion I'd
tighten, and Milestone 4 does it for real — reducing `TOP_K` from 5 to 2 and
re-running the full test, rather than just asserting it would make a
difference.

**A secondary finding, not a pipeline bug:** criteria 3 and 5 turned out to be
the same test wearing two names. Both are answered by putting the same 5
`OUT_OF_SCOPE` questions through `gate.py::check` against the same 0.6
threshold — there's one mechanism (the distance cutoff) behind both, not two
independent confirmations. Nothing in the pipeline needs fixing for this one;
it's a criteria-design gap, and I'm noting it under What I'd Do Differently
rather than pretending it's two green checkmarks.

## The Improvement

**What I changed:** `config.py::TOP_K` from 5 down to 2. Nothing else — same
chunker, same threshold, same prompt, same corpus.

**Why I picked it:** Diagnoses names top-k=5 as the reason nothing missed:
with only 23 chunks in the corpus, retrieving 5 per question pulls back
almost a quarter of everything, which could pass criterion 1 by breadth
rather than precision. Cutting top-k to 2 tests that directly — if precision
was the real story, the answer should still show up; if breadth was
carrying it, at least one question should now miss.

### Run Log — After

Produced by `python run_eval.py --label after`, run on 2026-09-23. Full
transcript: `results/run_2026-09-23_2036_after.md`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Sampled chunks are a complete thread, no cut-off sentences (revised) | 4 of 5 | 5/5 | 5/5 | 5/5 | MET (unaffected by top-k — chunking didn't change) |
| 5. Low-confidence questions rejected at cutoff | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Did it help?** No — and that's a real result, not a non-result. Every
criterion landed exactly where it did before (15/15, 5/5), and every
best-distance value is identical to the "before" run (e.g. 0.4931 for the
bike-parking question in both), because dropping top-k only trims
lower-ranked results — the closest match doesn't move. Only the retrieved
source count shrank, from 5 sources per question down to 2.

That disconfirms half of my diagnosis. Top-k=5 genuinely is generous for a
23-chunk corpus, but that generosity wasn't propping up a weak criterion 1 —
the top-1 match really is that close for all 5 questions, at both top-k=5
and top-k=2. So the honest update is: nothing missed not because retrieval
gets to cheat with a wide net, but most likely because my 5 test questions
are each anchored to one distinctively-worded fact ("three buildings," "48
hours," "October and November") that the embedding model separates cleanly
from the rest of a small corpus. That's a property of the test questions,
not proof the pipeline is robust — see What's Still Broken.

## What's Still Broken

No criterion missed, but three real gaps remain.

**Nothing checks whether the generated answer's paraphrase stays factually
consistent with the source.** Criterion 1 only checks that a keyword phrase
shows up somewhere in the retrieved chunks; criterion 2 only checks that a
source is named. I noticed the gap directly: one "after" run answered the
internship question with "October and November of the preceding year"
instead of the source's "for the following summer." I checked
`thread_internship_timing.txt` before flagging it, and both phrasings
describe the same timing from different reference points — so it wasn't
actually wrong. But nothing in my criteria would have caught it if it had
been. I'd add a sixth criterion for this in a future unit, though making it
objective rather than another vague judgment call would take real thought —
probably an LLM-as-judge, which is the harder version of `scorer.py` the
course itself points at and I didn't build this time.

**Criteria 3 and 5 are the same test wearing two names** (see Diagnoses). I'd
rewrite criterion 5 to check a genuinely different failure mode — e.g.
borderline or adjacent-topic questions instead of clearly out-of-corpus ones
— which would actually stress-test where the 0.6 cutoff sits, rather than
reconfirming criterion 3 a second time.

**My 5 test questions are all the same shape:** one distinctive fact, tied to
one thread. That's the more likely reason nothing missed even after cutting
top-k to 2 — the questions themselves may not be hard enough to expose a
real weakness. I stopped here rather than rewriting `questions.py` mid-unit:
the one-change rule is about the system, and I'd already spent this unit's
one measured change on top-k. Harder, more ambiguous test questions are the
first thing I'd add next, not a second system change squeezed into this one.

## What I'd Do Differently

**Criterion 4:** already revised once this unit for testability, but
"complete thread, no cut-off sentences" is trivially true given a
one-thread-per-chunk strategy — it doesn't fail even in principle. I'd want a
target that says something about chunk *usefulness*, not just *completeness*.

**Criterion 5:** would write it from the start to test a genuinely different
failure mode than criterion 3, instead of reusing the same out-of-corpus
question list under a different name.

**Criterion 1:** would deliberately include one or two harder test questions
— ambiguous phrasing, or an answer that requires combining two threads —
alongside the easy ones, so a 4-of-5 target has some real chance of actually
being tested instead of being cleared by construction.
