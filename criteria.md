# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy is at least 0.60 on the held-out test split, on every seed

Overall accuracy ≥ **0.60** on `test_split.csv` for each of seeds 42, 7 and
2024. Not the average: all three.

**Why this target:** With four labels balanced near 25% each, both a random
guesser and an always-guess-the-biggest-label guesser score about 0.25 to
0.30. So 0.60 is more than double chance. It is the point where using
TakeMeter to sort an r/nba thread gets 3 in 5 posts right, which is the
lowest bar I'd call useful. I did not pick 0.75. The test split is only
about 36 posts, so one seed's accuracy moves by about 0.03 per post. On top
of that, `hot_take` vs `joke` depends on detecting sarcasm, which a small
DistilBERT trained on about 170 posts will often miss.

---

## 2. Every label clears its own F1 floor, on every seed

Per-label F1 on the test split, on all three seeds:
`analysis` ≥ **0.60**, `reaction` ≥ **0.50**, `hot_take` ≥ **0.45**,
`joke` ≥ **0.40**.

**Why this target:** The floors are deliberately unequal, and each one
reflects how much surface signal that label has in r/nba text. `analysis`
posts carry visible cues (numbers, player names, records like *"3 block
titles in 3 seasons"*), so it gets the highest floor. `joke` gets the
lowest. Puns like *"They call him AA. It's a 12 step program"* need world
knowledge the model doesn't have, and every label will have only about 9
test posts, so one miss moves F1 by roughly 0.1. Even 0.40 is well above
the roughly 0.25 a guesser gets, so no label is allowed to be dead weight.

---

## 3. No label is more than 35% or less than 20% of `labels.csv`

In the final `labels.csv` (target 240 rows), every label's share is between
**20%** and **35%**, so between 48 and 84 posts.

**Why this target:** The brief's cap is 70%, but with four labels that
would leave the other three sharing 30%. A model trained that way learns to
guess the big label. The real pressure here is the floor. In my
45-post reading sample, only about 1 in 8 r/nba comments was `analysis`.
Collected at random, 240 rows would give about 30 analysis posts and only
about 4 in the test split, too few to measure. A 20% floor (48 posts, about
7 in test) forces me to oversample analysis on purpose from the 1,459-post
pool.

---

## 4. I agree with the staff labels on at least 80% of the 30 staff posts

`agreement.py` reports an agreement rate of at least **0.80** (24 of 30)
between my labels and staff's on `data/staff_posts.csv`, using staff's
taxonomy.

**Why this target:** Three of my four labels share names with the staff
taxonomy. Its key rule ("a fact is `analysis` only if it is load-bearing,
otherwise it is a `hot_take` with a statistic in it") is the same rule
as my decision rule 2. So if I'm applying my own rules consistently, I
should apply theirs well too. 80% allows six disagreements. That's room
for the cases where my headline-isn't-evidence rule or my habit of
splitting out `joke` pulls me away from staff, but not room for sloppy
labeling. Below 0.80, the model's errors in criteria 1–2 could be my
labels, not the model.

---

## 5. Confident predictions beat unsure ones by at least 0.15, on every seed

In `results.json`, `accuracy_most_confident_third` minus
`accuracy_least_confident_third` is at least **0.15** on each of the three
seeds.

**Why this target:** TakeMeter is only useful for triage if a high
confidence score means "trust this." Then low-confidence posts, which I
expect to be the sarcastic `hot_take`/`joke` ones, can go to a human. With
about 36 test posts, each third has about 12 posts, so 0.15 means at least
2 more correct answers in the confident third than in the unsure third.
That's the smallest gap I'd trust as more than noise at this size. A gap
near zero would mean the confidence score is decoration, which matters
because the README would then have to say not to use it.
---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
