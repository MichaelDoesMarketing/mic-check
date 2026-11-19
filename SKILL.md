---
name: mic-check
description: Fix writing that is technically correct and still flat, robotic, exhausting, or forgettable - measures sentence rhythm, breath length, and how lines land, then rewrites for sound. Use when copy reads like AI wrote it, when a draft drones, when every sentence is the same size, when something is grammatically fine but nobody finishes it, when a post or page or email needs more personality, or when the user says make this punchier, tighten this, or something feels off and they cannot say what.
---

# Mic Check

Prose has a rhythm whether the writer intended one or not. Readers subvocalize, which means every sentence gets performed in their head at roughly the pace of speech, and a passage that is uncomfortable to say is uncomfortable to read. Most bad copy is not badly worded. It is badly timed.

This is also the clearest tell of machine-written text. Models settle into a comfortable band, usually somewhere between fourteen and twenty-two words, and stay there for paragraphs at a time. Nothing is wrong with any individual sentence. The reader leaves anyway.

Three things fix it, and only one of them is sentence length.

Use the mechanics. Never announce them. Nothing in the output talks about beats, bars, flows, or rappers unless the user asks where the method comes from.

## The three mechanisms

**1. Breath.** A person can only say so much before they need air. Writers type instead of speak, so they build sentences nobody could perform, and the reader's inner voice runs out and bails mid-clause. Measured as syllables between punctuation breaks, not words per sentence. A forty-word sentence cut into four clauses breathes fine. A twenty-five word sentence with no comma does not. `references/breath.md`

**2. The pocket.** Where the sentence lands relative to where the reader expects it to. On-time is boring even when the lengths vary, which is why "vary your sentence length" advice produces writing that is still dead. Personality lives in the beat you arrive a little early or a little late on. `references/pocket.md`

**3. Room after the punch.** A good line needs silence after it. Writers stack their three best sentences in a row and lose all three, because the reader is still processing the first when the second arrives. The throwaway line after a strong one is doing load-bearing work. `references/throwaway.md`

Sound texture sits underneath all three: which consonants land on the stressed syllables, where the vowels repeat, how the last word of a sentence feels in the mouth. `references/sound.md`

## Step 1: Measure before you judge

Run the script. It is in `scripts/miccheck.py`, needs nothing installed, and takes a file or stdin.

```
python3 scripts/miccheck.py draft.md
cat draft.md | python3 scripts/miccheck.py
python3 scripts/miccheck.py draft.md --json      # for further processing
python3 scripts/miccheck.py draft.md --quiet     # scores and flags, no chart
```

It returns a rhythm chart, five scores, and specific flags with sentence numbers. Read the chart before reading the scores. A passage that drones looks like a brick wall and you can see it in a second.

If the script cannot be run in this environment, do the same five judgments by hand and say that the numbers are estimated. Do not pretend to have measured.

Run it on the whole piece first, then on any section that scored badly, because averages hide local disasters.

## Step 2: Read the flags, not the total

The score exists to locate the problem, not to grade the writing. A 4.2 with a dead opening paragraph is worse than a 3.4 that holds attention.

The five axes:

- **Breath** - how much of the passage a reader cannot say in one go
- **Variance** - whether the length actually changes, docked for every run of similar sentences
- **Landing** - how often a sentence stops instead of trailing off
- **Room** - sentences above the median stacked with no relief between them
- **Open** - whether the first line earns the second

The overall score weights the lowest axis double, on purpose. A passage is only as good as the thing most wrong with it, and averaging is how a draft with one fatal problem reads as fine.

## Step 3: Name the one problem

Not five problems. One.

Almost every flat passage has a single dominant failure and four symptoms of it. A draft that drones usually also lands soft, because the writer is in explanation mode and explanation mode produces both. Fix the dominant one and the rest move on their own.

Say what it is in a sentence, in plain terms, pointing at specific line numbers. "Sentences nine through fourteen are all the same size" is useful. "The rhythm could be more varied" is not.

## Step 4: Fix the shape, not the words

Order of operations. Doing these out of order wastes the work.

1. **Break the long ones.** Any breath group over twenty syllables gets split or punctuated. This is mechanical and it is usually a third of the problem.
2. **Cut one sentence in every drone run to under half the median.** Not shortened. Cut to a fragment if that is what it takes. The gap is the point.
3. **Change the landings.** A passage where nothing stops needs hard endings. End on a one-syllable content word. "It did not work" beats "it was unsuccessful" for reasons that have nothing to do with word choice.
4. **Open room after the best line.** Find the strongest sentence in the passage. Look at what comes immediately after it. If that is also a strong sentence, one of them is being wasted.
5. **Then go after the pocket**, which is the part that cannot be measured and is the difference between competent and memorable.

Re-run the script after. If the scores moved and the writing is not better, you optimized the metric instead of the passage. Say so and roll it back.

## Modes

**Mic check** - the default. Measure, name the one problem, fix the shape, show the before and after. Run this when someone hands over a draft.

**Breath control** - measurement only, no rewrite. The script, the chart, and a plain reading of what the numbers say. Use when the user wants a diagnosis, is deciding whether a piece needs work at all, or is comparing drafts.

**Bar for bar** - line by line. Their sentence, the rewrite, the syllable counts for both, and one clause saying what changed. No commentary beyond that. This is the mode that teaches, so the explanation has to be short enough to read forty times.

**Run it back** - the same passage in three genuinely different rhythms, each with a name and a job. Not three polishes of one approach. If the three could be swapped without changing which one suits the format, they are the same version and the mode has failed. `references/genres.md` has the shapes that suit each format.

**Perform it** - lay the copy over a flow and mark the bar breaks, so the user hears what they actually wrote. Four beats to a bar, four bars to a block, stresses marked. Copy that cannot be laid over a flow without hitting a wall mid-line is copy nobody can read out loud either, and that is the diagnosis. This mode is allowed to be funny and is not allowed to be mean.

## The rule that protects this skill

**Rhythm never buys a sentence that says nothing.**

A line that sounds great and carries no information gets cut, no matter how good it sounds. This is the failure mode of every piece of advice about writing with rhythm: the writer learns to make noise and stops making points.

Applied, that means:

- Any rewrite that improves the sound and loses a fact, a number, a name, or a qualification is rejected and the original stands
- A fragment added for rhythm must carry meaning. "Simple as that." carries nothing. Cut it
- If the fix for a drone run is to delete a sentence, delete it. Do not replace it with a shorter sentence that says less
- When a passage scores badly because it is dense with real information, say that. Technical writing, legal copy, documentation, and anything a reader will act on are allowed to be flat. Report the score and recommend no change

If a passage has nothing to say, rhythm will not save it and this skill is the wrong tool. Say so.

## Output format

Deliver in this shape unless the user asks for something else.

```
WHAT IT SOUNDS LIKE
The chart, or a plain description of the shape if the script could not run.

THE SCORE
Five axes and the overall. One line, no interpretation yet.

THE ONE PROBLEM
A sentence naming the dominant failure, with line numbers.

THE FIX
The rewritten passage. Whole, not fragments, so it can be read as a thing.

WHAT CHANGED
Three or four lines maximum. What moved and why. Not a lecture.

WHAT STAYED
Anything that scored badly and was left alone on purpose, and the reason.
```

Worksheets are in `assets/flow-sheet.md` and `assets/rewrite-card.md`.

## Rules of engagement

**Preserve the voice.** This skill fixes timing. It does not make everyone sound the same, and it especially does not make everyone sound punchy. A writer whose natural register is long and winding gets better long winding sentences, not short ones.

**Format decides the target.** A landing page and a case study have different correct rhythms. Applying social-post timing to a technical explainer makes it worse. Check `references/genres.md` before rewriting anything.

**Not every flat passage is broken.** Error messages, legal text, API docs, safety instructions, and anything read under pressure should be boring and even. Flag the score and recommend no change.

**Do not add personality that is not theirs.** If the user's writing has no jokes in it, the rewrite does not get jokes. Rhythm is not a license to insert a voice.

**Meaning outranks sound, every time.** See the rule above. It is the only one in this skill with no exceptions.

**Measure or say you did not.** Never report a syllable count or a score that came from a guess. The script is in the folder for a reason, and an invented number is worse than no number.

**Short is not the goal.** Hemingway scores well on every axis here and so does a lot of writing with nothing in it. The target is variation with purpose, not compression.
