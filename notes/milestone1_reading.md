# Milestone 1 — Community and reading notes

## The community

**r/nba** — public, no login needed to read, very high volume, with a wide
range of quality, from stat-heavy breakdowns to one-line jokes.

- ✅ Public only: collected through Reddit's public RSS feeds, no account.
- ✅ Not built around one show or release. It covers the whole league, so
  there are no spoilers to worry about.
- ✅ Enough volume: `scripts/collect_nba.py` pulled **1,459 candidate
  comments** (8–250 words each) from 22 threads in one timeboxed run, which
  is far more than the 200 needed. The pool is `data/nba_candidates.csv`.

Collection unit: **one top-level or reply comment = one post.** r/nba
submissions are mostly links and highlight clips with no body text. The
comments are where people actually argue.

## Reading log

> ⚠️ **Do this yourself.** The brief says "Actually read them." Pull 30–40
> rows from `data/nba_candidates.csv` and read them before you accept or
> change anything below.
>
> ```bash
> .venv/bin/python -c "import pandas as pd; [print(f'[{i}]', t, '\n') for i,t in enumerate(pd.read_csv('data/nba_candidates.csv').sample(40, random_state=7).text, 1)]"
> ```

## Candidate distinctions seen in the text

Each one is something you can point at in the post, not a judgment of quality.

1. **Some posts cite a checkable fact; most don't.** For example: *"He never
   once finished in the top 5 in pts/36 on his own team"* (Bill Russell),
   *"The trips are paid for through a sponsorship deal"*, and a paraphrased
   Kobe quote. Facts are rare, maybe 1 in 8 posts.
2. **Confident general claims with nothing behind them.** *"It probably is
   the greatest moment in Knicks history."* *"He got DPOY because of the
   market change. That's it."* *"Ban the advertising too. Should be treated
   like cigarettes."* These are very common.
3. **Jokes and bits that make no claim at all.** *"They call him AA. It's a
   12 step program."* *"I thought it was Guile based on the hair lmao."*
   *"Exactly what James Naismith envisioned basketball would be."* These
   are roughly 1 in 5 posts, which is common enough that ignoring them would
   force them into the wrong bucket.
4. **Immediate feeling about the clip or news.** *"Yeah wow… Bravo."* *"I
   love rewatching jokic highlights… incredible stuff."* *"we love hali and
   the Pacers in this building."*

Also seen, but not quality distinctions: plain questions (*"Can anyone
explain what the story here is?"*) and personal anecdotes (*"Met his dad. He
was a super nice guy"*). These need a rule, either a label or an exclusion,
before labeling starts.
