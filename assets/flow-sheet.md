# Flow sheet

Worksheet for a single passage. Fill it top to bottom. Stop at the first section you cannot answer, because that is the work.

---

## The passage

**What it is:** (post, page section, email, case study, script, other)

**Who reads it and in what state:** (scrolling, deciding, under pressure, at leisure)

**What it has to do:** (one sentence, no hedging)

---

## Measured

Run `python3 scripts/miccheck.py <file>` and paste the header line.

```
_ sentences | median _ syl | shortest _ | longest _ | stdev _
```

| Axis | Score | What the number is reacting to |
|---|---|---|
| Breath | /5 | |
| Variance | /5 | |
| Landing | /5 | |
| Room | /5 | |
| Open | /5 | |
| **Overall** | **/5** | |

**Flags, verbatim from the script:**

---

## The one problem

One sentence. Name the dominant failure and the line numbers it lives on.

> 

**Why the other flags are symptoms of it:**

---

## By hand

Things the script cannot see. Answer all four.

**Read it out loud. Where did you stumble?**

**What are the three best lines, and what comes immediately after each?**

| Strong line | What follows it | Competing? |
|---|---|---|
| | | |
| | | |
| | | |

**Is the rhythm predictable by paragraph three?**

**Does anything in it surprise you on the second read?**

---

## The fix

In order. Skip any step that does not apply, and say why.

- [ ] **Break the long ones.** Groups over 20 syllables: _____
- [ ] **Cut one sentence in each drone run to under half the median.** Runs: _____
- [ ] **Change the landings.** Sentences to re-end: _____
- [ ] **Open room after the best line.** What gets demoted: _____
- [ ] **Pocket.** Where the passage arrives early or late on purpose: _____

---

## After

Re-run the script.

```
_ sentences | median _ syl | shortest _ | longest _ | stdev _
Overall: _/5
```

**Is it actually better, or did the numbers move?**

If the scores improved and the passage did not, roll it back and write down what the metric missed. That note is worth more than the rewrite.

---

## Left alone

Anything that scored badly and stays that way, with the reason.

| What | Score | Why it stays |
|---|---|---|
| | | |

---

## Meaning check

The last gate. Answer honestly or the whole exercise is decoration.

- [ ] No fact, number, name, or qualification was lost in the rewrite
- [ ] Every fragment added for rhythm carries information
- [ ] Nothing was shortened past the point of being true
- [ ] The voice still sounds like the person who wrote it
