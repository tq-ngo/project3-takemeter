# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

This classifier sorts public comments from `r/nba`, one of Reddit's largest sports communities, into four categories: `analysis`, `hot_take`, `reaction`, and `joke`. The community features a wide spectrum of text, ranging from rigorous statistical breakdowns of player efficiency to low-effort memes, trade hyperbole, and emotional outbursts during close games. TakeMeter filters signal from noise by distinguishing between arguments backed by load-bearing checkable facts, confident unsupported assertions, immediate emotional expressions, and pure punchlines.

---

## Label Taxonomy

### `analysis`

**Definition:** Makes an argument about basketball or the league that is backed by a specific, checkable fact the writer brings (a stat, record, date, comparison, or quote), and that fact supports this specific conclusion. Restating the thread's own headline does not count.

**Example 1:**
> He has 3 block titles in 3 seasons, if he gets one more he'd be tied for the all time lead, with Kareem, Mark Eaton, and Marcus Camby. 3 block titles feels like it already puts you in elite all time conversations

**Example 2:**
> And then consider that Bill Russell is a top 5 all-time player despite being largely a non-factor on offense. He never once finished in the top 5 in pts/36 on his own team and his offensive and defensive advanced stats are as lopsided as Steve Nash's in the opposite direction.

### `hot_take`

**Definition:** Asserts a confident general claim about players, teams, or the league with no checkable support offered, including sarcasm that encodes a real opinion.

**Example 1:**
> He got DPOY because of the market change. That's it. Should have won it years before

**Example 2:**
> Winning in 2017 and not getting the love he thought he’d get broke his brain. He’s been chasing the love he got in OKC ever since

### `reaction`

**Definition:** Reports the writer's own immediate feeling about the clip, game, or news (awe, heartbreak, joy, disgust) rather than making a claim about the world.

**Example 1:**
> Yeah wow. The fact that most of us got a few of them is genuinely nuts. Bravo.

**Example 2:**
> I love rewatching jokic highlights and seeing where he makes his decisions, incredible stuff

### `joke`

**Definition:** Exists only for a punchline (such as a pun, bit, absurd image, or reference gag), with no sincere claim behind it.

**Example 1:**
> They call him AA. It's a 12 step program.

**Example 2:**
> Exactly what James Naismith envisioned basketball would be.

### The hardest boundary

**Which two labels:** `hot_take` vs `joke`

**The decision rule I used every time:**
Strip the "lol", the emoji, and the sarcasm, then ask: *is there a sincere claim left that the writer would defend if challenged?* If yes, it is `hot_take`, however jokey it sounds. If what is left is only an absurd punchline or gag with no sincere claim, it is `joke`.

---

## The Dataset

**Where the posts came from:** Public comment threads on `r/nba` collected across 22 threads via Reddit's public RSS endpoints (top/hot feeds). Plain questions and purely personal anecdotes without basketball claims were excluded during curation.

**How I labelled them:** I labeled 20 posts completely cold first with no tools or AI assistance, marked as `cold` in the `note` column. For the remaining 220 posts, an AI tool was used to pre-label candidates against my written taxonomy, after which I personally read, verified, and corrected every single row before committing, marking them as `pre-labeled, checked`.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `analysis` | 60 | 25.0% |
| `hot_take` | 60 | 25.0% |
| `reaction` | 60 | 25.0% |
| `joke` | 60 | 25.0% |
| **Total** | 240 | 100% |

**Three hard cases**

**1.**
> *The post:* "Winning in 2017 and not getting the love he thought he’d get broke his brain. He’s been chasing the love he got in OKC ever since"
>
> *Could have been:* `analysis` vs `hot_take`
>
> *I chose, because:* I chose `hot_take`. Although the post names a specific year ("2017"), deleting the date leaves the amateur psychological claim completely intact. The date is merely decorative context rather than load-bearing evidence for the conclusion.

**2.**
> *The post:* "Fuck it let’s just move all the NBA teams to the top 30 cities by population worldwide Say hello to the Tokyo Thunder and São Paulo 76ers"
>
> *Could have been:* `hot_take` vs `joke`
>
> *I chose, because:* I chose `joke`. While it mocks expansion discussions, the author is not advocating or defending an actual league relocation to Tokyo and São Paulo; once the hyperbole is stripped away, it is purely an absurd parody punchline.

**3.**
> *The post:* "When he hurt his knee before the half in G1 I was truly heartbroken, my captain continued to play with a bum knee, a broken wrist and a bum ankle (thanks Wemby and Barnes)."
>
> *Could have been:* `reaction` vs `hot_take`
>
> *I chose, because:* I chose `reaction`. Although the parenthetical assigns blame for injuries, the primary communicative purpose of the comment is reporting personal emotional grief ("truly heartbroken") and fan attachment ("my captain").

---

## The Training Run

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, seed 42, max length 128 tokens.

**Anything I changed from the defaults, and why:** None. All training settings were kept at the starter defaults (3 epochs, lr 2e-5, batch 16, max_length 128, seed 42) to establish a standard fine-tuning baseline.

**Split sizes:** 70/15/15 stratified split across 240 rows: train 168 (42 per label), validation 36 (9 per label), test 36 (9 per label). All four labels have 9 examples in the test split, clearing the 8-example threshold that causes erratic metric swings.

---

## How I Used AI

**Moment 1**

- *What I asked for:* Prompted the AI with my initial label definitions and asked it to generate 8 border-case posts specifically designed to probe ambiguity between labels.
- *What came back:* 8 realistic borderline comments (e.g., sarcasm encoding real critique, posts mixing emotion and claims, headline-restating facts).
- *What I changed:* Found that 4 of the 8 posts failed to classify cleanly under my initial draft. I updated the taxonomy with a strict precedence hierarchy (`analysis` -> `hot_take` -> `reaction` -> `joke`), ruled that sarcasm encoding a real opinion is `hot_take`, clarified that restating a thread's headline is not `analysis`, and specified that facts must bear directly on the conclusion.

**Moment 2**

- *What I asked for:* Provided candidate comment batches along with the tightened definitions and asked the model to propose provisional labels to speed up initial sorting.
- *What came back:* Initial batch label proposals, but the model frequently mistook sarcasm for `joke` and misclassified decorative numbers as `analysis`.
- *What I changed:* Read and reviewed every single comment manually, overriding incorrect classifications (especially enforcing the hardest boundary rule between `hot_take` and `joke`) to ensure absolute consistency with the decision rules.

**Pre-labelling disclosure:** 20 posts were labeled completely cold without any AI assistance (`cold`). The remaining 220 posts were pre-labeled with AI and each one was individually read, checked, and manually corrected before inclusion (`pre-labeled, checked`).

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy |  |  |  |
| Macro F1 |  |  |  |
| F1 — `label_one` |  |  |  |
| F1 — `label_two` |  |  |  |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
