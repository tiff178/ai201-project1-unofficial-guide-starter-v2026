# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that contains the answer.

**Why this target:** Four of my five test questions have their answer located within a single, labeled section of a guide document, making them straightforward to retrieve. The fifth test question, "Which places in the region are largely closed in winter?," spans multiple guide documents with several potential answers, making it harder to capture. 

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:** Every document in the city_guides corpus represents either a specific town guide or topic guide (accessibility, eating, transportation, seasons, walking). As source document filenames are attached directly to each retrieved chunk passed into the model, this target is achievable, though it could fail if the model fails to parse metadata. 

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate stops it and the system returns "I don't have enough information about that" — in at least 4 of 5 tries.

**Why this target:** Each document covers specific locations and travel details (e.g. getting there, getting around, what to see, etc.), so completely unrelated topics produce distinctly higher distance scores. This target ensures the distance cutoff catches out-of-scope questions while allowing flexibility for edge cases that happen to use similar keywords. 

---

## 4. Retrieved chunks are detailed enough to provide context 

For at least 3 of my 5 test questions, the retrieved chunks are at least 250 characters long. 

**Why this target:** The city_guides corpus includes descriptive details on sights, dining, transportation, etc. Retrieved chunks under 250 characters are either fragmented headings or isolated text snippets that lack enough surrounding detail to answer a question. Setting a 250 character minimum ensures that each chunk yields complete, informative context while leaving room for naturally shorter summary chunks. 

---

## 5. Answers remain concise 

For at least 4 of my 5 test questions, the answer the system produces is four sentences or fewer. 

**Why this target:** Users searching city guides need fast, direct answers rather than verbose summaries. Retrieved chunks already contain focused details from the documents, therefore keeping responses to four sentences or fewer ensures answers remain concise while leaving room for questions that list several locations. 

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->