# mic-check

**Check your mic before you say anything.**

Most bad copy isn't badly worded. It's badly timed.

Readers subvocalize. Every sentence gets performed in their head, roughly at the speed of speech. A passage that's uncomfortable to say is uncomfortable to read. Nobody can tell you why. They just leave.

It's also the loudest tell that a machine wrote something. Models settle into a comfortable band, usually fourteen to twenty-two words, and sit there for paragraphs. No individual sentence is wrong. The whole thing is dead anyway.

`mic-check` measures the rhythm of what you wrote, shows you the shape of it, and fixes the timing without touching your voice.

## How it works

Three mechanisms. Only one of them is sentence length.

**Breath.** A person can only say so much before they need air. You type instead of speak. So you build sentences nobody could perform, and the reader's inner voice runs out mid-clause. It's syllables between punctuation, not words per sentence. A forty-word sentence with six commas breathes fine. A twenty-six word sentence with no commas suffocates. Shorter, and worse. Word count tells you the opposite.

**The pocket.** Where a sentence lands versus where the reader expected it. This is why "vary your sentence length" still produces dead writing. Follow it exactly and you get short, long, short, long. The reader clocks that in three paragraphs and stops hearing it. The goal is variation they can't see coming.

**Room after the punch.** You find a great line. You're warmed up now, so you find another one. Then a third. All three go in back to back. The reader is still holding the first when the second lands on top of it. What survives is a vague sense that the paragraph was trying hard. The flat line after a strong one is load-bearing. Almost nobody writes it on purpose.

## It actually measures

There's a Python script in the folder. No dependencies. Takes a file or stdin, runs anywhere.

Out comes a rhythm chart, flags with line numbers, and scores on five axes: breath, variance, landing, room, and open. The overall weights the lowest axis double. On purpose. A draft with one fatal problem shouldn't average out to fine.

Calibration check, on the most famous paragraph in writing advice. Gary Provost's bad example scores **2.0**. His good example scores **4.3**. Same instrument, no thumb on the scale.

Under four sentences it refuses to score at all. It tells you to read the thing out loud instead, because variance on a headline is a confident wrong answer.

## The rule that keeps it honest

**Rhythm never buys a sentence that says nothing.**

Any rewrite that improves the sound and loses a fact, a number, a name, or a caveat gets rejected. The original stands. Fragments added for rhythm have to carry information. "Simple as that." carries nothing, so it dies.

This is the failure mode of every piece of advice about writing with rhythm. The writer learns to make noise and stops making points.

It won't force the frame, either. Error messages. API docs. Legal copy, safety instructions, anything read under pressure. All of that should be flat and even. Point this at documentation and it tells you to leave it alone.

## Install

```bash
git clone https://github.com/MichaelDoesMarketing/mic-check.git ~/.claude/skills/mic-check
```

Or grab the packaged `.skill` from [releases](https://github.com/MichaelDoesMarketing/mic-check/releases).

## Try it with

> "This is grammatically fine and completely forgettable. Fix it."

> "Does this read like AI wrote it?"

> "Make this punchier." (it will tell you if punchier is the wrong fix)

Five modes. **Mic check** is the default pass. **Breath control** measures and diagnoses, no rewriting. **Bar for bar** goes line by line, syllable counts on both, one clause of explanation each. **Run it back** gives you three rhythms. Genuinely different ones, not three polishes.

And **perform it**, which lays your copy over a flow with the bar breaks marked, so you hear what you actually wrote. Copy that hits a wall mid-line can't be read out loud either. That's the diagnosis.

## Real demo: I ran it on my own GitHub profile

The thing at the top of [my profile](https://github.com/MichaelDoesMarketing). Live right now, written carefully, listing every skill I've shipped.

**43 sentences. Overall 4.1 out of 5. Verdict: it plays.**

Then the flags:

```
No air    s25: 30 syllables with no break.
No air    s31: 22 syllables with no break.
No air    s36: 22 syllables with no break.
Drone     s1-s3:   3 sentences within 3 syllables of each other.
Stacked   s31-s33: 3 heavy sentences, no relief between them.
```

Three sentences in there that no human can say in one go, inside a document that scored well. This is the whole argument for reading flags instead of totals. A good average is forty fine sentences carrying three broken ones, and the broken ones are where people stop.

They cluster, too. Nearly every skill on that list gets a bolded name, then one long explanatory sentence. Over and over.

Pull the three worst entries out as their own block and the damage shows up in the score. **2.7 out of 5. Breath at 2.**

> **subtext** reads what came back.
> What a message is actually saying, with every finding tied to a quoted feature and a mandatory innocent reading before anything ships.
>
> **sampled** checks whose it was.
> Whether the idea you're about to publish already belongs to somebody. Sources, dates, and an honest coverage statement every time. It will never tell you something is original.
>
> **headroom** leaves room.
> The beat that sounds best alone is the worst beat to rap on. Finds where your deck or template is standing on the toes of the person who has to use it.

After:

> **subtext** reads what came back.
> What a message is actually saying. Every finding tied to a quote, and an innocent reading required before anything ships.
>
> **sampled** checks whose it was.
> Whether your idea already belongs to somebody else. Sources and dates, every time. It will never call your work original.
>
> **headroom** leaves room.
> The beat that sounds best alone is the worst beat to rap on. It finds where your deck is standing on somebody's toes.

**2.7 to 3.5. Breath from 2 to 5. Zero flags left.** Nothing was cut except words that were already doing nothing.

And it still says *passes, barely*, because variance on a ten-sentence block is mediocre and the tool isn't going to pretend otherwise. A thing that congratulates you after its own fix is useless.

## License

MIT. Michael Daughters.
