# Milestone 2 — Stress test

Eight AI-written posts aimed at the boundaries of the taxonomy in
`milestone2_taxonomy.md`. **They are not data.** None of them go into
`labels.csv`.

> ✋ **Classify all eight yourself before opening the answers.** If you
> disagree with a ruling, the definitions aren't tight enough yet.

1. Jokic averaged a triple double and still didn't win MVP. Voters are clowns lmao
2. I literally screamed when he hit that. Best shooter ever, no debate.
3. Ah yes, the Lakers, famous for their elite perimeter defense
4. Wemby is 7'4 with an 8-foot wingspan. Just put him in the MVP conversation already.
5. Watching this at 3am in Manila and I regret nothing 😭
6. Refs gave the Warriors 14 free throws in the 4th quarter alone. Rigged league lol
7. Imagine paying $400 for courtside seats and getting a Westbrook brick to the face
8. Can't believe they traded him for two second rounders. Front office should be fired.

<details>
<summary>Rulings, and what broke</summary>

| # | Ruling | Boundary | Clean under the v1 rules? |
|---|---|---|---|
| 1 | `analysis` | analysis / hot_take / joke | ✅ The stat is the reason given, so rule 1 applies |
| 2 | `hot_take` | reaction / hot_take | ❌ **No rule for posts with a feeling *and* a claim** |
| 3 | `hot_take` | joke / hot_take | ❌ **The `joke` definition says "sarcasm," but the hardest-boundary rule says a sarcastic claim is `hot_take`. They contradict.** |
| 4 | `hot_take` | analysis / hot_take | ❌ **A real fact is present but doesn't support *this* conclusion (height ≠ MVP play). Rule 2's "delete the number" test was ambiguous here.** |
| 5 | `reaction` | reaction / joke | ✅ |
| 6 | `analysis` | analysis / hot_take | ✅ The fact carries the argument, even with "lol" |
| 7 | `joke` | joke / analysis | ✅ A number, but no argument |
| 8 | `hot_take` | analysis / hot_take / reaction | ❌ **"Two second rounders" is just the thread's headline. Under v1, nearly every r/nba complaint would count as `analysis`.** |

**Four of eight did not classify cleanly**, so the taxonomy was tightened
*before* labeling:

- **A. Added a fixed precedence order for mixed posts** (fixes #2):
  `analysis` → `hot_take` → `reaction` → `joke`. Take the first one that
  applies.
- **B. Sarcasm that encodes a real claim is `hot_take`.** `joke` now means
  "no sincere claim remains" (fixes #3). The `joke` definition no longer
  lists sarcasm by itself.
- **C. Restating the thread's headline is not evidence.** An `analysis`
  fact must be something the writer *brings*: a stat, record, comparison,
  or history (fixes #8).
- **D. The fact must bear on the specific conclusion**, not just be about
  the same player (fixes #4).

</details>
