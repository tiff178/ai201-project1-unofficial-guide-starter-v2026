# The Unofficial Guide

Tiffany Truong | Corpus: `city_guides`

# Unit 1

## What This Does

This system uses the `city_guides` corpus to answer questions from fourteen travel guides - nine town guides, plus five guides that cut across all of them (eating, walking, regional transport, seasons, accessibility). You can ask questions to quickly find specific travel recommendations within the guides (e.g. *How do I get to Brightwater?*, *What is there to see in Pellew Sands?*). 

All answers are drawn directly from the documents and name the source files used. If you ask a question that the travel guides do not cover, the system will state that it does not have enough information to answer. 

To begin asking questions: `python app.py ask "..."`

## Chunking Strategy

**Chunk size:** 500
**Overlap:** 100

Each document in the `city_guides` corpora is organized into labeled markdown sections (`## Getting there`, `## Getting around`, `## Eat and drink`, etc.). Instead of chunking by character counts, I decided to split the documents by section headings (`##`). This approach keeps entire travel guide recommendations intact within a single chunk, rather than chunks ending halfway. 

The starter chunk turns `city_guides` into 51 chunks from 14 documents (800-character window), slicing straight through the labeled sections. The starter approach frequently sliced paragraphs mid-sentence and cut section headers halfway through. Since these travel guides cover nine different towns with similar sections (`## Getting there,` `## Getting around`, etc.), a chunk that starts mid-section would not know which specific town it belongs to. To resolve this, I implemented a custom `split_documents` function in `chunker.py` that detects section headers (`##`) and groups related paragraphs together while prepending the parent document title and section label `<Guide Title - Section Heading>` to each chunk. 

I set a target chunk size of 500 characters with a 100-character overlap. The 500-character chunk size aligns with the typical length of a single travel recommendation paragraph, keeping each chunk focused on a specific tip rather than clumping multiple topics together. The 100-character overlap acts as a safety buffer when a section spans across paragraph breaks, ensuring key details like specific restaurant names, transit lines, or seasonal warnings; don't lose their context across chunk boundaries.

Starter Chunk: 51 chunks, 650 characters on average (shortest 24, longest 800) vs
Custom Chunk: **98 chunks, 307 characters on average (shortest 153, longest 554)**

## Sample Chunks

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#4` — produced by: `chunker.py::split_documents`

```
Corry Vale — What to see

The valley itself is the attraction. The footpath network is dense and well marked, and a circuit taking in three of the four villages is about nine miles with 500 metres of ascent. The chapel in the second village is 12th century and always unlocked.
```

**Chunk 3** — source: `guide_givens_mill.md#1 ` — produced by: `chunker.py::split_documents`

```
Givens Mill — Getting there

No station and no bus on Sundays; four buses a day from Brightwater on weekdays, taking 30 minutes. Driving is 20 minutes. The village car park holds about forty cars and is full by 11am on summer Saturdays.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
Kestrelford — What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#7` — produced by: `chunker.py::split_documents`

```
Pellew Sands — Practical notes

Cash is still useful at the market and in smaller places, though cards are
accepted almost everywhere now. Mobile coverage is good in the centre and
patchy on the outskirts. The nearest full hospital is in Brightwater; there is
a minor injuries unit locally with limited hours.
```

## Sample Answer

**Question:** What time should I arrive at if I go to Halden Bay in August?

**Answer:**

```
(best distance 0.243, cutoff 0.66)

If you are going to Halden Bay in August, you should arrive before 10am or plan to use the overflow lot (guide_seasons.md).

Sources retrieved: guide_halden_bay.md, guide_seasons.md
```

**My relevance cutoff:** 0.66

My relevance cutoff is 0.66 because it sits directly in the middle between my in-scope and out-of-scope questions. Four out of my five test questions land between 0.24 and 0.35, with the fifth one more far out (0.524). At 0.66, the cutoff provides a safe, balanced boundary in both directions. Valid questions pass through to retrieval while unrelated queries are safely intercepted by the gate. Setting the cutoff any higher would risk letting out-of-scope questions slip through and cause hallucinations, whereas setting it lower would cause false rejections on valid in-scope questions like "Which places in the region are largely closed in winter?" (0.524).

| Question | In corpus? | Best distance |
|---|---|---|
| What time should I arrive at if I go to Halden Bay in August? | yes | 0.243 |
| What is there to eat and drink at Halden Bay? | yes | 0.313 |
| How do I get to Pellew Sands? | yes | 0.346 |
| How long does it take to drive to Kestrelford? | yes | 0.354 |
| Which places in the region are largely closed in winter? | yes | 0.524 |
| What is the capital of Mongolia? | no | 0.808 |
| What is the recommended dosage of ibuprofen for a headache? | no | 0.835 |
| How do I write a for loop in Rust? | no | 0.859 |
| How do I change the oil in a diesel engine? | no | 0.881 |
| Who won the 1994 World Cup? | no | 0.982 |

## How I Used AI

**1.** I pasted my five draft critera into Claude and asked "*For each of these five acceptance criteria for a retrieval system, tell me exactly how you would test each one using only what the sentence says. Don't suggest improvements - just tell me what you'd do.*" It could describe a test for each of them, so there was no changes needed to be made on my critera. 

**2.** I pasted both sets of distances into Claude and asked "*Here are the best distances for five questions my documents cover, and five they don't. Where would you put the cutoff, and what would I get wrong at that number?*" It suggested a relevance cutoff between 0.6-0.65 with an explanation of why it made that suggestion. I decided to set my relevance cutoff as 0.66 as it would be in between the gap of my in-scope and out-of-scope questions, which is a reasonable choice near the range Claude suggested. 

---

# Unit 2

## Run Log — Before

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 2. Every answer names a source | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 3. Gate stops out-of-corpus questions | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Retrieved chunks are detailed enough to provide context | 3 of 5 | 4/5 | 4/5 | 4/5 | MET |
| 5. Answers remain concise | 4 of 5 | 5/5 | 5/5 | 5/5 | MET |

**Criterion 1**: Scored by `scorer.py::retrieval_hit`; checks whether the `expects` phrase appears in any retrieved chunks

Four out of five test questions passed all three runs, meeting the set acceptance critera. 

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| What is there to eat and drink at Halden Bay? | pass | pass | pass |
| How do I get to Pellew Sands? | fail | fail | fail |
| How long does it take to drive to Kestrelford? | pass | pass | pass |
| What time should I arrive at if I go to Halden Bay in August? | pass | pass | pass |
| Which places in the region are largely closed in winter? | pass | pass | pass |

**Criterion 2**: Produced by `generate.py::answer_from_chunks`

Each test question for all three runs provides a source file of where it found the answer. 

**Question**: What is there to eat and drink at Halden Bay?

```
Based on the documents, Halden Bay offers genuinely fresh seafood because the two harbour restaurants buy directly from boats that land in the early morning (*guide_halden_bay.md* and *guide_eating.md*). Additionally, prices on the harbour front are roughly double those on Fell Street, one level up, for comparable food (*guide_halden_bay.md* and *guide_eating.md*). 

Sources: `guide_halden_bay.md` and `guide_eating.md`
```

**Criterion 3**: Produced by `run_eval.py::check_out_of_scope`

| Out-of-scope question | Best distance | Gate |
|---|---|---|
| What is the capital of Mongolia? | 0.808 | refused |
| How do I change the oil in a diesel engine? | 0.881 | refused |
| Who won the 1994 World Cup? | 0.982 | refused |
| What is the recommended dosage of ibuprofen for a headache? | 0.835 | refused |
| How do I write a for loop in Rust? | 0.859 | refused |

**Criterion 4**: Scored by `scorer.py::chunk_detailed`; checks whether the retrieved chunks are at least 250 characters long

Four out of five test questions passed all three runs. One of the question fails all three runs, suggesting that the retrieved chunk is most likely less than 250 characters. 

| Question | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| What is there to eat and drink at Halden Bay? | pass | pass | pass |
| How do I get to Pellew Sands? | fail | fail | fail |
| How long does it take to drive to Kestrelford? | pass | pass | pass |
| What time should I arrive at if I go to Halden Bay in August? | pass | pass | pass |
| Which places in the region are largely closed in winter? | pass | pass | pass |

**Criterion 5**: Manually count the number of sentences retrieved; four sentences or fewer to pass the criteria. All five answers have four sentences or fewer. 

**Question**: Which places in the region are largely closed in winter?

```
Halden Bay largely closes in winter. This information comes from the documents `guide_seasons.md` and `guide_halden_bay.md`.
```

## Verdicts

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 | Retrieved chunk contains the answer | MET | 4 of 5 across all three runs, meeting the target exactly; One of the test questions ("How do I get to Pellew Sands?") failed on all three runs consistently due to a retrieval miss, but the other 4 questions passed every time. 
| 2 | Every answer names a source | MET | 5 of 5; All five test questions for each three runs name at least one source file. Even for the question that failed to contain the answer has provided a source file name. |
| 3 | Gate stops out-of-corpus questions | MET | Exceeded the 4 of 5 target with 5 of 5 refused. The distances for out-of-scope questions ranged from 0.808 to 0.982 against a 0.66 cutoff. |
| 4 | Retrieved chunks are detailed enough to provide context | MET | Exceeded the 3 of 5 target with 4 of 5 on all three runs. For 4 of 5 test questions, the top retrieved chunk exceeded 250 characters across all three runs. One of the test questions ("How do I get to Pellew Sands?") failed because no relevant chunk was retrieved. |
| 5 | Answers remain concise | MET | Exceeded the target of 4 of 5 with 5 of 5 on all three runs. All five questions provided a concise answer with four sentences or fewer for each of the three runs. |

## Diagnoses

**In-Scope Question Failed**: How do I get to Pellew Sands?
**Stage**: Chunking/Retrieval 

For all three runs on this question, it stated it does not have enough information to answer how to get to Pellew Sands. However, it successfully identified the correct source documents (`guide_accessibility.md` and `guide_pellew_sands.md`). This likely happened because the semantic search retrieved descriptive chunks instead of the specific travel section (## Getting there) or direction details were split across chunk boundaries. The grounding instruction prevents the model from hallucinations, so missing the factual text in the retrieved chunk forced the system to correctly respond that it did not have enough information to answer. 

All 5 criterion met their target threshold. Some targets were set too conservatively, like targeting 4 of 5 for Criterion 1 allowed the system to pass despite consistently failing to answer one of the questions on every run ("How do I get to Pellew Sands?"). Applying stricter acceptance criteria forces the evaluation to surface specific failure modes, such as context retrieval misses, that would otherwise be masked by lower targets. 

- Criterion 1 should be changed to *Every retrieved chunk contains the answer.*
- Criterion 4 should be changed to *For at least 4 of my 5 test questions, the retrieved chunks are at least 250 characters long.* 

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