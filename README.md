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

Baseline: `facebook/bart-large-mnli` zero-shot, prompted with `label_definitions.txt`.
Trained: DistilBERT, seed 42 (`results.json`). Both scored on the same 36 posts in
`test_split.csv` (9 per label).

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.333 | 0.500 | +0.167 |
| Macro F1 | 0.218 | 0.485 | +0.267 |
| F1 — `analysis` | 0.552 | 0.667 | +0.115 |
| F1 — `hot_take` | 0.320 | 0.400 | +0.080 |
| F1 — `joke` | 0.000 | 0.375 | +0.375 |
| F1 — `reaction` | 0.000 | 0.500 | +0.500 |

**What the definitions were worth (same baseline, bare label names, no definitions):**

| Measure | With definitions | Bare names | Difference |
|---|---|---|---|
| Overall accuracy | 0.333 | 0.361 | +0.028 |
| Macro F1 | 0.218 | 0.311 | +0.093 |
| F1 — `analysis` | 0.552 | 0.200 | −0.352 |
| F1 — `hot_take` | 0.320 | 0.424 | +0.104 |
| F1 — `joke` | 0.000 | 0.200 | +0.200 |
| F1 — `reaction` | 0.000 | 0.421 | +0.421 |

The baseline reported in the main table is the **definitions** run
(`baseline_results.json`); the bare-names run is in
`baseline_results_bare_names.json`.

**What I predicted before I looked:**
I predicted that fine-tuning DistilBERT would beat the zero-shot BART-MNLI
baseline most decisively on `joke` and `reaction`, while `analysis` would be a
close contest. Zero-shot NLI models prompted with "makes an argument backed by a
specific checkable fact" can easily latch onto visible numbers and dates, but
they completely lack awareness of Reddit sports slang, sarcastic bits, and
conversational banter without in-domain training examples.

**What the gap actually means:**
Fine-tuning beat the zero-shot baseline on every label, by 0.267 macro F1 on
this split. Almost all of that gain is on `reaction` and `joke`, where the
baseline got zero. With my definitions it sent 20 of 36 posts to `analysis`
and never once predicted `reaction` or `joke`. The definitions actually
*hurt* the baseline overall. Bare label names scored higher on accuracy
(0.361 vs 0.333) and macro F1 (0.311 vs 0.218). The definitions helped only
`analysis`: words like "stat, record, date" pulled anything with a number or
a name toward it. Two caveats keep this from being a clean win for
fine-tuning. First, the comparison covers only seed 42's split. Second, on
seeds 7 and 2024 the trained model scored 0.333 and 0.361 (see run log),
which is no better than the baseline. So the honest finding is that on two
of three splits, fine-tuning added nothing measurable over a zero-shot
model.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

Device: Apple Silicon GPU (MPS), torch 2.14.1. Settings unchanged from unit 5:
`distilbert-base-uncased`, 3 epochs, lr 2e-5, batch 16, max_length 128.
Seed 42 reproduced the unit 5 `results.json` exactly (0.500 / 0.485).

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 every seed | 0.500 | 0.333 | 0.361 | MISSED |
| 2. Per-label F1 floors | analysis ≥ 0.60, reaction ≥ 0.50, hot_take ≥ 0.45, joke ≥ 0.40 | 0.667 / 0.500 / 0.400 / 0.375 | 0.429 / 0.375 / 0.375 / 0.000 | 0.476 / 0.429 / 0.308 / 0.000 | MISSED |
| 3. Label share in `labels.csv` | every label 20%–35% | 25% each | 25% each | 25% each | MET |
| 4. Staff agreement | ≥ 0.80 (24/30) | — | — | — | MET (26/30 = 86.7%) |
| 5. Confident − unsure third accuracy | ≥ +0.15 every seed | +0.417 (0.583 − 0.167) | +0.250 (0.500 − 0.250) | −0.250 (0.250 − 0.500) | MISSED |

Criterion 2 cells read analysis / reaction / hot_take / joke. Criteria 3
and 4 are properties of the data, not of a seed, so they have one value.

**Spread across seeds:**

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.500 | 0.333 | 0.361 | 0.167 |
| Macro F1 | 0.485 | 0.295 | 0.303 | 0.191 |
| F1 — `analysis` | 0.667 | 0.429 | 0.476 | 0.238 |
| F1 — `hot_take` | 0.400 | 0.375 | 0.308 | 0.092 |
| F1 — `reaction` | 0.500 | 0.375 | 0.429 | 0.125 |
| F1 — `joke` | 0.375 | 0.000 | 0.000 | 0.375 |

Accuracy moved 16.7 points across seeds, past the 10-point line, so a single
split is not a measurement here. Seed 42, the split my unit 5 result and the
baseline comparison used, was the friendliest of the three.

### Confusion matrix

Seed 42 (the notebook's section 7 output):

| true \ predicted | analysis | hot_take | reaction | joke |
|---|---|---|---|---|
| **analysis** | 7 | 1 | 1 | 0 |
| **hot_take** | 4 | 3 | 1 | 1 |
| **reaction** | 0 | 1 | 5 | 3 |
| **joke** | 1 | 1 | 4 | 3 |

Summed over all three seeds (108 test predictions):

| true \ predicted | analysis | hot_take | reaction | joke |
|---|---|---|---|---|
| **analysis** | 15 | 9 | 3 | 0 |
| **hot_take** | 6 | 11 | 9 | 1 |
| **reaction** | 4 | 4 | 14 | 5 |
| **joke** | 4 | 9 | 11 | 3 |

**My biggest off-diagonal number, and what it means:**
On seed 42 the biggest cell is 4 real `hot_take` posts called `analysis`,
with only 1 going the other way. That direction doesn't survive the other
seeds. Summed over all three, `analysis → hot_take` (9) outnumbers
`hot_take → analysis` (6). The robust off-diagonal is **11 real `joke`
posts called `reaction`**, plus 9 more called `hot_take`. Only 3 of 27
jokes were recognised. The model never learned `joke` as a category; it
splits jokes between the two labels they look most like on the surface.



---

## Verdicts and Diagnoses

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy | ≥ 0.60 on every seed | MISSED | No seed reached it: 0.500, 0.333, 0.361 |
| 2 | Per-label F1 floors | analysis 0.60 / reaction 0.50 / hot_take 0.45 / joke 0.40, every seed | MISSED | `hot_take` and `joke` miss on all three seeds; `joke` is 0.000 on two |
| 3 | Label balance | 20%–35% each | MET | 60 / 240 = 25.0% for every label |
| 4 | Staff agreement | ≥ 0.80 | MET | 26 / 30 = 86.7% agreement on `data/staff_posts.csv` |
| 5 | Confidence gap | ≥ +0.15 every seed | MISSED | Seeds 42 and 7 pass (+0.417, +0.250); seed 2024 is reversed (−0.250) |

**Diagnoses**

- **Criterion 1 (Overall accuracy) & Criterion 2 (Floor on `joke`):**
  *Cause: A genuinely hard label pair combined with severe underfitting.*
  How I know: In the 3-epoch run, `joke` collapsed to 0.000 F1 on seeds 7 and
  2024, with only 3 of 27 jokes correctly predicted across splits. The
  confusion matrix shows jokes leaking symmetrically into `reaction` (11) and
  `hot_take` (9). Sarcastic basketball bits like reference gags, memes, and
  puns lack explicit emotional words, but their short lengths and punchy phrasing
  mirror quick reactions. Meanwhile, training loss stalled at 1.328 against
  initial entropy of 1.386 (ln 4), proving 33 optimizer steps were insufficient
  to pull representations away from uniform prior weights.

- **Criterion 2 (Floor on `hot_take`) & `analysis` leakage:**
  *Cause: A boundary I applied inconsistently in my own labels.*
  How I know: Across the three seeds, 9 real `analysis` posts were mispredicted
  as `hot_take`. My agreement check provides direct evidence of why: on post
  `sp_005` (Pile a), I misclassified a controlled personal comparison as
  `hot_take` because I treated personal tracking data with skepticism rather
  than checking if the 2% stat carried the argument. That same inconsistent
  boundary exists in my 240 `labels.csv` rows, where posts citing single-game
  stats or personal observations were split arbitrarily between `analysis` and
  `hot_take`.

- **Criterion 5 (Confidence gap reversed on Seed 2024):**
  *Cause: Optimization stall producing near-uniform output probabilities.*
  How I know: At 3 epochs, the model's winning confidence averaged 0.28 (where
  uniform random guessing is 0.25). When all predictions cluster in a narrow
  0.26–0.30 band, sorting predictions into thirds sorts noise, making seed-to-seed
  rank order unstable. When training epochs were doubled to 6 in Milestone 5,
  loss dropped to 1.19 and Criterion 5 was cleanly MET across all three seeds
  (+0.167, +0.250, +0.250).



---

## Agreement Report

**Agreement rate:** 26 / 30 = 86.7%

**Disagreements**

**1.**
> *The post:* "Carbon plates aren't the whole story. My times dropped 2% in the shoes and another 2% the following year in the same pair, when the only thing that changed was going from 35 to 50 miles a week."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* Staff is right. I was overly skeptical because the post
> opens like an assertive gear take and relies on an N=1 training log.
> However, Rule 1 asks: *does the fact carry the argument?* The author isolates
> shoe impact (2%) against increased mileage volume (2% in the same shoes) to
> prove that mileage mattered as much as the shoes. The two percentages are
> load-bearing to the conclusion, not decorative. I applied Rule 1 too loosely
> by dismissing personal training data.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**2.**
> *The post:* "Three of us ran the same session on the same day, different shoes, within 10 seconds of each other over 5 miles. I'm not saying shoes do nothing, but whatever they do was smaller than the noise between three people."
>
> *Staff said / I said:* `analysis` / `hot_take`
>
> *My call, and why:* I think my call is defensible. Staff called this
> `analysis` because the sample ("three of us", "within 10 seconds over 5 miles")
> is a checkable observation that the writer's conclusion rests upon. However,
> three different human runners possess differing baseline fitness and
> mechanics; comparing their times in different shoes does not constitute a
> controlled test, and concluding that shoe differences are "smaller than noise"
> is a sweeping inductive leap that the anecdotal data cannot logically support.
> Under Rule 1, the observation fails to bear the conclusion, making it an
> unsupported hot take.
>
> *Which pile:* (c) the rule is ambiguous here and my reading is defensible

**3.**
> *The post:* "Nobody actually enjoys the long run. They enjoy having done it, which is a completely different thing, and the sport would be more honest if it said so."
>
> *Staff said / I said:* `hot_take` / `reaction`
>
> *My call, and why:* Staff is right. The comment felt like an emotional
> personal confession about the grueling fatigue of long runs, leading me to
> label it `reaction`. But Rule 2 is explicit: *is it about a claim or about
> the writer?* "`reaction` reports what just happened to the writer and how it
> felt. `hot_take` asserts something general about the world." The writer makes
> a sweeping assertion about everyone in the sport ("Nobody actually enjoys the
> long run"), not a report of their own run that morning. I let the reflective
> tone override the rule's subject test.
>
> *Which pile:* (a) the rule covered it and I applied it loosely

**4.**
> *The post:* "Just realised the shoes I set every PB in this year are the ones I bought by accident in the wrong size."
>
> *Staff said / I said:* `reaction` / `hot_take`
>
> *My call, and why:* This is a gap in the taxonomy. The comment is framed as
> an immediate personal discovery ("Just realised..."), which fits `reaction`
> under Rule 2. But in the context of a running forum, the communicative
> purpose is an ironic, satirical commentary on gear obsession and shoe sizing
> dogma. The staff taxonomy provides no class for wry humor or satire (which my
> 4-class taxonomy splits into `joke`), leaving a gap between reporting personal
> surprise (`reaction`) and making an implicit critique of the sport
> (`hot_take`). Staff favored the first-person framing; I favored the satirical
> communicative payload.
>
> *Which pile:* (b) the rule genuinely doesn't say

**What the pattern in my disagreements tells me:**
The two Pile (a) disagreements reveal a consistent pattern in how I apply
decision rules:
1. On `analysis` vs `hot_take` (`sp_005`), I tend to dismiss personal data and
   self-experiments as "anecdotal hot takes" rather than checking whether the
   numbers do load-bearing argumentative work.
2. On `hot_take` vs `reaction` (`sp_019`), I let emotional or reflective
   phrasing pull sweeping general claims into `reaction`.

This pattern directly mirrors my model's confusion matrix: 9 real `analysis`
posts were predicted as `hot_take`, and 9 `joke`/`hot_take` posts were predicted
as `reaction`. My own threshold for what counts as an argument was applied
inconsistently in the 240 training examples, teaching the model blurry decision
boundaries.



---

## The Improvement

**What I changed:**
Increased training epochs from 3 to 6 (`EPOCHS = 6`). Everything else—base
model (`distilbert-base-uncased`), learning rate (2e-5), batch size (16),
max sequence length (128), and the stratified split logic—was kept strictly
identical.

**Which diagnosis pointed at it:**
The diagnosis that the model underfitted after only 33 optimizer steps (3
epochs on 168 training examples at batch size 16). At 3 epochs, training loss
stalled at 1.328 against a random-guessing baseline of 1.386 (ln 4), winning
confidences hovered around 0.28, and subtle minority cues like `joke`
completely collapsed to 0.000 F1 on two of three seeds. Doubling the training
budget to 6 epochs gave AdamW 66 optimization steps to move weights away from
initialization.

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | ≥ 0.60 every seed | 0.528 | 0.444 | 0.472 | MISSED |
| 2. Per-label F1 floors | analysis ≥ 0.60, reaction ≥ 0.50, hot_take ≥ 0.45, joke ≥ 0.40 | 0.609 / 0.526 / 0.462 / 0.471 | 0.533 / 0.500 / 0.364 / 0.421 | 0.609 / 0.333 / 0.476 / 0.375 | MISSED |
| 3. Label share in `labels.csv` | every label 20%–35% | 25% each | 25% each | 25% each | MET |
| 4. Staff agreement | ≥ 0.80 (24/30) | — | — | — | MET (26/30 = 86.7%) |
| 5. Confident − unsure third accuracy | ≥ +0.15 every seed | +0.167 (0.667 − 0.500) | +0.250 (0.667 − 0.417) | +0.250 (0.583 − 0.333) | **MET** |

**Spread across seeds (After):**

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.528 | 0.444 | 0.472 | 0.083 |
| Macro F1 | 0.517 | 0.455 | 0.448 | 0.068 |
| F1 — `analysis` | 0.609 | 0.533 | 0.609 | 0.075 |
| F1 — `hot_take` | 0.462 | 0.364 | 0.476 | 0.113 |
| F1 — `reaction` | 0.526 | 0.500 | 0.333 | 0.193 |
| F1 — `joke` | 0.471 | 0.421 | 0.375 | 0.096 |

**Did it help, and how do I know:**
Yes, it helped clearly, and the numbers show three specific improvements:
1. **Spread was cut in half:** Overall accuracy spread dropped from 0.167
   (unstable, > 10 points) down to 0.083 (within the 0.05–0.10 stable range).
   Macro F1 spread dropped from 0.191 down to 0.068.
2. **`joke` was rescued from zero:** In the before run, `joke` had 0.000 F1
   on seeds 7 and 2024, with only 3 of 27 test jokes correctly predicted
   overall. At 6 epochs, `joke` scored 0.471, 0.421, and 0.375 across the
   seeds, recalling 11 of 27 test jokes across splits.
3. **Criterion 5 turned from MISSED to MET:** In the before run, Seed 2024's
   confidence was inverted (−0.250). At 6 epochs, training loss reached
   1.19–1.25 and confidence predictions calibrated properly across all three
   seeds (+0.167, +0.250, +0.250), satisfying Criterion 5.

However, it did not push accuracy over the 0.60 target (peaking at 0.528 on
seed 42), confirming that additional optimization steps cannot replace
missing training examples or resolve genuine semantic ambiguity.

---

## What's Still Broken

- **Criterion 1 (Overall accuracy ≥ 0.60):** Missed on all three seeds
  (0.528, 0.444, 0.472). The model still gets roughly 1 in 2 posts wrong on
  held-out splits. What I would do next is double the dataset size from 240
  to 500 rows, because 42 training examples per class is too few for
  DistilBERT to generalize beyond prominent lexical markers.
- **Criterion 2 (Per-label F1 floors):** Missed on seeds 7 (`hot_take`
  0.364) and 2024 (`reaction` 0.333, `joke` 0.375). With only 9 test posts
  per label, a single misclassification swings F1 by ~0.10.
- **Why I stopped here:** Pushing epochs beyond 6 caused validation loss to
  bottom out and begin fluctuating (~1.20–1.25), indicating that further
  training would overfit to idiosyncrasies of the 168 training posts rather
  than improve test generalization.

**The gap between what I meant my labels to capture and what the model
learned:**
I meant my labels to distinguish between arguments backed by load-bearing facts,
unsupported opinions, and pure punchlines, but the model primarily learned
surface syntax—mistaking emotional expressions in jokes for `reaction` and
treating any number or player name as evidence for `analysis`. Because
DistilBERT lacks domain-specific NBA background knowledge, it cannot discern
whether a sarcastic comment carries a sincere underlying critique or is merely
an absurd bit.



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

       [x] Baseline vs. Trained table, with your prediction written beforehand
       [x] Run Log — Before, five criteria across three seeds
       [x] Confusion matrix TYPED AS A MARKDOWN TABLE
       [x] A verdict on every criterion
       [x] A diagnosis for every miss, using the agreement report as evidence
       [x] Agreement Report with every disagreement adjudicated
       [x] One improvement, with Run Log — After
       [x] What's Still Broken
       [x] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [x] At least four new commits
       [x] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
