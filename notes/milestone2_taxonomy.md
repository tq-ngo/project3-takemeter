# Milestone 2 — TakeMeter label taxonomy (r/nba)

One post = one r/nba comment. Four labels. Each post gets exactly one label.

**Out of scope, not collected into `labels.csv`:** plain questions and
personal anecdotes that make no claim and no joke (*"Can anyone explain what
the story here is?"*, *"Met his dad. He was a super nice guy"*). These are
skipped while picking the 200 posts, and the README discloses that.

---

## `analysis`

**Definition:** makes an argument about basketball or the league that is
backed by a specific, checkable fact the writer brings (a stat, record,
date, comparison, or quote), and that fact supports this specific
conclusion. Restating the thread's own headline does not count.

**Example 1** (#1329)
> He has 3 block titles in 3 seasons, if he gets one more he'd be tied for the
> all time lead, with Kareem, Mark Eaton, and Marcus Camby. 3 block titles
> feels like it already puts you in elite all time conversations

**Example 2** (#1336, opening)
> And then consider that Bill Russell is a top 5 all-time player despite being
> largely a non-factor on offense. He never once finished in the top 5 in
> pts/36 on his own team and his offensive and defensive advanced stats are as
> lopsided as Steve Nash's in the opposite direction. …

## `hot_take`

**Definition:** asserts a confident, general claim about players, teams, or
the league with no checkable support, or with a fact that is only
decoration on a conclusion the writer already reached.

**Example 1** (#776)
> He got DPOY because of the market change. That's it. Should have won it
> years before

**Example 2** (#487)
> Winning in 2017 and not getting the love he thought he'd get broke his
> brain. He's been chasing the love he got in OKC ever since

## `reaction`

**Definition:** reports the writer's own immediate feeling about the clip,
game, or news in the thread (awe, joy, hurt, disgust) instead of making a
claim about the world.

**Example 1** (#701)
> Yeah wow. The fact that most of us got a few of them is genuinely nuts.
> Bravo.

**Example 2** (#1295)
> I love rewatching jokic highlights and seeing where he makes his decisions,
> incredible stuff

## `joke`

**Definition:** the post exists only for a punchline (a bit, pun, absurd
image, or reference gag), and once the joke is stripped out, no sincere
claim is left. Sarcasm that encodes a real opinion is `hot_take`.

**Example 1** (#270)
> They call him AA. It's a 12 step program.

**Example 2** (#37)
> Exactly what James Naismith envisioned basketball would be.

---

## The hardest boundary: `hot_take` vs `joke`

r/nba wraps real opinions in jokey tone constantly, and "lol" appears in
both labels. In the reading sample, **"lol"/"lmao" showed up in hot takes,
analysis, and jokes alike**, so tone markers cannot decide this.

**Decision rule, used every time:**
> Strip the "lol", the emoji, and the sarcasm, then ask: *is there a sincere
> claim left that the writer would defend if challenged?* If yes, it is
> `hot_take`, however jokey it sounds. If what's left is only a punchline,
> it is `joke`.

- *"NBA players already act like living in Toronto is a 3rd world shit hole
  lol. Mexico City is an amazing city but I doubt a lot of these players
  care"* → `hot_take`. The writer really believes players won't want Mexico
  City.
- *"They call him AA. It's a 12 step program."* → `joke`. There is no claim
  left once the pun is removed.

## Secondary rules

**Precedence for mixed posts** (added after the stress test). Walk this
list and take the first label that applies:

1. Has a load-bearing checkable fact → `analysis`
2. Has a sincere general claim → `hot_take`
3. Main content is the writer's feeling → `reaction`
4. Only a punchline left → `joke`

The detailed rules:

1. **Any load-bearing checkable fact → `analysis`**, even if the tone is
   jokey or heated. *"Mexico City's elevation is over 2000 feet higher than
   Denver's. They would have a crazy home court advantage lol"* →
   `analysis`, because the elevation fact *is* the argument.
2. **Fact as decoration → not `analysis`.** If deleting the number leaves
   the conclusion exactly as strong, the number wasn't doing work. *"Winning
   in 2017 … broke his brain"* → `hot_take`. The fact must bear on *this*
   conclusion: *"He's 7'4, put him in the MVP conversation"* → `hot_take`,
   because height is not evidence of MVP-level play.
3. **The headline is not evidence.** Repeating what the thread is about
   (*"Can't believe they traded him for two second rounders"* in the trade
   thread) does not make a post `analysis`. The writer has to bring the
   fact.
4. **`reaction` vs `hot_take`: about the writer, or about the world?**
   *"Definitely fucking hurts"* is about the writer → `reaction`. *"That's
   the best block of the decade"* is about the world → `hot_take`. If a
   post has both, the claim wins (precedence step 2).
5. **`reaction` vs `joke`:** if the main content is a feeling, it is
   `reaction` even with a wisecrack attached. If the main content is the
   wisecrack, it is `joke`.

_Rules were tightened after the stress test. See
`milestone2_stress_test.md`._
