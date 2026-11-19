#!/usr/bin/env python3
"""
miccheck.py - measures the rhythm of a passage of prose.

Reports syllable counts per sentence, breath-group lengths, how each sentence
lands, where the passage drones, and where heavy sentences stack with no room
between them. Prints a rhythm chart and a score on five axes.

Usage:
    python3 miccheck.py FILE
    cat draft.md | python3 miccheck.py
    python3 miccheck.py FILE --json
    python3 miccheck.py FILE --quiet      (scores and flags, no chart)

No dependencies. Python 3.8+.

The syllable counter is a heuristic, not a pronunciation dictionary. It is
accurate enough for comparing sentences inside one passage, which is all these
measures need. Do not quote its per-word counts as fact.
"""

import json
import re
import statistics
import sys

# ---------------------------------------------------------------- text intake

CODE_FENCE = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`]*`")
MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
MD_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
HTML_TAG = re.compile(r"<[^>]+>")
MD_MARKS = re.compile(r"[*_~#>|]+")
URL = re.compile(r"https?://\S+")
LIST_BULLET = re.compile(r"^\s*(?:[-+*]|\d+[.)])\s+", re.M)
BLOCKQUOTE = re.compile(r"^\s*>.*$", re.M)
TABLE_ROW = re.compile(r"^\s*\|.*$", re.M)
WHITESPACE = re.compile(r"[ \t]+")


def clean(text, keep_quotes=False):
    """Strip markdown furniture so the measures see prose, not syntax.

    Blockquotes come out by default. Quoted material is someone else's
    rhythm, and a document that quotes bad writing as an example should not
    be scored on it. Pass keep_quotes=True when the blockquotes are pull
    quotes the author wrote.
    """
    text = CODE_FENCE.sub(" ", text)
    if not keep_quotes:
        text = BLOCKQUOTE.sub(" ", text)
    text = TABLE_ROW.sub(" ", text)
    text = MD_IMAGE.sub(" ", text)
    text = MD_LINK.sub(r"\1", text)
    text = INLINE_CODE.sub(" ", text)
    text = HTML_TAG.sub(" ", text)
    text = URL.sub(" ", text)
    text = LIST_BULLET.sub("", text)
    text = MD_MARKS.sub("", text)
    text = WHITESPACE.sub(" ", text)
    return text


# Abbreviations that end in a period but do not end a sentence.
ABBREV = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st", "vs", "etc", "e.g",
    "i.e", "inc", "ltd", "co", "approx", "fig", "no", "vol", "p", "pp",
    "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "sept", "oct",
    "nov", "dec", "u.s", "u.k", "a.m", "p.m",
}

SENT_SPLIT = re.compile(r"(?<=[.!?…])[\"')\]]*\s+")


def split_sentences(text):
    """Split into sentences. Line breaks end a sentence even without a period,
    because a standalone line in copy is read as its own beat."""
    out = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = SENT_SPLIT.split(line)
        buf = ""
        for part in parts:
            part = part.strip()
            if not part:
                continue
            candidate = (buf + " " + part).strip() if buf else part
            last = candidate.rstrip("\"')]").split()[-1].lower() if candidate.split() else ""
            if last.rstrip(".") in ABBREV and candidate.endswith("."):
                buf = candidate
                continue
            out.append(candidate)
            buf = ""
        if buf:
            out.append(buf)
    return [s for s in out if re.search(r"[A-Za-z]", s)]


WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")


def words(sentence):
    return WORD.findall(sentence)


# ----------------------------------------------------------------- syllables

VOWELS = "aeiouy"

# Words the vowel-group rule gets wrong often enough to be worth hardcoding.
SYLL_OVERRIDE = {
    "the": 1, "a": 1, "i": 1, "you": 1, "your": 1, "our": 1, "hour": 1,
    "are": 1, "were": 1, "we're": 1, "they're": 1, "you're": 1, "there": 1,
    "here": 1, "where": 1, "one": 1, "once": 1, "some": 1, "come": 1,
    "every": 3, "everyone": 3, "everything": 4, "people": 2, "business": 2,
    "really": 3, "being": 2, "doing": 2, "going": 2, "idea": 3, "area": 3,
    "create": 2, "creates": 2, "created": 3, "creating": 3, "creative": 3,
    "science": 2, "quiet": 2, "poem": 2, "fire": 1, "hire": 1, "wire": 1,
    "more": 1, "store": 1, "whole": 1, "while": 1, "life": 1, "like": 1,
    "make": 1, "take": 1, "give": 1, "have": 1, "live": 1, "love": 1,
    "move": 1, "serve": 1, "nice": 1, "twice": 1, "voice": 1, "choice": 1,
}

SILENT_E = re.compile(r"[^aeiou]e$")


def syllables(word):
    w = word.lower().strip("'’-")
    if not w:
        return 0
    if w in SYLL_OVERRIDE:
        return SYLL_OVERRIDE[w]

    # Count vowel groups.
    count = 0
    prev_vowel = False
    for ch in w:
        is_vowel = ch in VOWELS
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel

    # Silent final e: "make" is one group short of what the rule gives.
    if SILENT_E.search(w) and count > 1:
        count -= 1
    # "-le" after a consonant is its own syllable: "table", "little".
    if w.endswith("le") and len(w) > 2 and w[-3] not in VOWELS:
        count += 1
    # "-ed" is usually silent unless it follows t or d: "walked" vs "wanted".
    if w.endswith("ed") and len(w) > 3 and w[-3] not in "td" and w[-3] not in VOWELS:
        count -= 1
    # "-es" after a sibilant is its own syllable: "faces", "watches".
    if w.endswith("es") and len(w) > 3 and (w[-3] in "sxzcg" or w[-4:-2] in ("sh", "ch")):
        count += 1

    return max(1, count)


def syll_count(sentence):
    return sum(syllables(w) for w in words(sentence))


# -------------------------------------------------------------- breath groups

# Punctuation a reader takes air on, inside a sentence.
BREATH_BREAK = re.compile(r"[,;:—–()]| - ")


def breath_groups(sentence):
    """Syllables between the places a reader can take a breath."""
    chunks = [c for c in BREATH_BREAK.split(sentence) if c and c.strip()]
    if not chunks:
        chunks = [sentence]
    return [syll_count(c) for c in chunks if syll_count(c) > 0]


# ------------------------------------------------------------------- landings

FUNCTION_WORDS = {
    "the", "a", "an", "of", "to", "in", "on", "at", "by", "for", "with",
    "and", "but", "or", "nor", "so", "yet", "as", "if", "than", "that",
    "is", "was", "are", "were", "be", "been", "am", "it", "its", "this",
    "these", "those", "there", "here", "them", "they", "he", "she", "we",
    "you", "i", "me", "him", "her", "us", "our", "my", "your", "their",
    "his", "hers", "ours", "theirs", "about", "into", "from", "too", "also",
    "just", "very", "really", "some", "any", "all", "more", "most", "well",
}

WEAK_SUFFIX = (
    "ing", "tion", "sion", "ity", "ive", "ous", "ment", "ness", "able",
    "ible", "ally", "ingly", "ier", "iest", "ism", "ure", "ence", "ance",
    "ency", "ancy", "eous", "ious", "ual", "ular", "ative", "itive",
)


def landing(sentence):
    """How the sentence lands. 'hard' stops. 'soft' trails off."""
    ws = words(sentence)
    if not ws:
        return "soft"
    last = ws[-1].lower()
    if last in FUNCTION_WORDS:
        return "soft"
    if syllables(last) == 1:
        return "hard"
    if last.endswith(WEAK_SUFFIX):
        return "soft"
    if last.endswith("ly") or last.endswith("y"):
        return "soft"
    return "mid"


# -------------------------------------------------------------------- measure


def analyze(text, keep_quotes=False):
    quoted = len(BLOCKQUOTE.findall(text)) if not keep_quotes else 0
    sentences = split_sentences(clean(text, keep_quotes=keep_quotes))
    if not sentences:
        return None

    rows = []
    for s in sentences:
        ws = words(s)
        groups = breath_groups(s)
        rows.append({
            "text": s,
            "words": len(ws),
            "syllables": syll_count(s),
            "longest_breath": max(groups) if groups else 0,
            "breath_groups": groups,
            "landing": landing(s),
        })

    sylls = [r["syllables"] for r in rows]
    median = statistics.median(sylls)
    stdev = statistics.pstdev(sylls) if len(sylls) > 1 else 0.0

    # Drone runs: three or more consecutive sentences within 3 syllables.
    drone_runs = []
    run_start = 0
    for i in range(1, len(sylls) + 1):
        same = i < len(sylls) and abs(sylls[i] - sylls[run_start]) <= 3
        if not same:
            if i - run_start >= 3:
                drone_runs.append((run_start, i - 1, i - run_start))
            run_start = i

    # Stacking: consecutive heavy sentences with no relief between them.
    # "Heavy" has to mean meaningfully above the median, not merely above it.
    # Half of all sentences are above the median by definition, so that
    # threshold fires on chance alone once a document gets long.
    heavy_floor = median * 1.25
    heavy = [i for i, v in enumerate(sylls) if v > heavy_floor]
    stack_runs = []
    run = []
    for i, v in enumerate(sylls):
        if v > heavy_floor:
            run.append(i)
        else:
            if len(run) >= 2:
                stack_runs.append((run[0], run[-1], len(run)))
            run = []
    if len(run) >= 2:
        stack_runs.append((run[0], run[-1], len(run)))

    # Share of the passage sitting inside a flat run. Rates, not counts:
    # a long document collects runs by length alone, and scoring the raw
    # count punishes size instead of rhythm.
    drone_share = sum(n for _, _, n in drone_runs) / len(rows)
    # Two above-median sentences in a row is ordinary prose. Three is a wall.
    big_stacks = [(s, e, n) for s, e, n in stack_runs if n >= 3]
    stack_share = sum(n for _, _, n in big_stacks) / len(rows)

    hard = sum(1 for r in rows if r["landing"] == "hard")
    mid = sum(1 for r in rows if r["landing"] == "mid")
    soft = sum(1 for r in rows if r["landing"] == "soft")
    # A mid landing is a content word that neither stops nor trails. Half credit.
    stop_pct = (hard + 0.5 * mid) / len(rows) * 100
    hard_pct = hard / len(rows) * 100
    soft_pct = soft / len(rows) * 100

    longest_breath = max(r["longest_breath"] for r in rows)
    over_20 = [i for i, r in enumerate(rows) if r["longest_breath"] > 20]
    over_12 = [i for i, r in enumerate(rows) if r["longest_breath"] > 12]
    airless_pct = len(over_20) / len(rows) * 100

    return {
        "sentences": rows,
        "count": len(rows),
        "syllables": sylls,
        "median": median,
        "stdev": round(stdev, 2),
        "shortest": min(sylls),
        "longest": max(sylls),
        "spread": max(sylls) - min(sylls),
        "drone_runs": drone_runs,
        "stack_runs": stack_runs,
        "drone_share": round(drone_share, 3),
        "stack_share": round(stack_share, 3),
        "hard_pct": round(hard_pct, 1),
        "soft_pct": round(soft_pct, 1),
        "stop_pct": round(stop_pct, 1),
        "longest_breath": longest_breath,
        "airless_pct": round(airless_pct, 1),
        "breath_over_20": over_20,
        "breath_over_12": over_12,
        "heavy_count": len(heavy),
        "opener": sylls[0],
        "quoted_lines_skipped": quoted,
    }


# ---------------------------------------------------------------------- score


def band(value, cuts, scores):
    for cut, score in zip(cuts, scores):
        if value <= cut:
            return score
    return scores[-1]


def score(a):
    # Breath. How much of the passage a reader cannot say in one go.
    # One long sentence among short ones is a feature. Many is suffocation.
    breath = band(a["airless_pct"], [0, 15, 30, 50], [5, 4, 3, 2, 1])
    if a["longest_breath"] > 35:
        breath = min(breath, 2)

    # Variance. Spread measured against the passage's own scale, so a piece
    # of short sentences is not judged by the same yardstick as a piece of
    # long ones. Raw stdev is not comparable across passages; this is.
    cv = a["stdev"] / a["median"] if a["median"] else 0
    variance = band(cv, [0.35, 0.50, 0.70, 1.00], [1, 2, 3, 4, 5])
    if a["drone_share"] > 0.40:
        variance -= 1
    variance = max(1, variance)

    # Landing. How often a sentence stops instead of trailing off.
    sp = a["stop_pct"]
    if sp < 15:
        land = 1
    elif sp < 25:
        land = 2
    elif sp < 35:
        land = 3
    elif sp <= 75:
        land = 5
    elif sp <= 90:
        land = 4
    else:
        land = 3

    # Room. How much of the passage sits in a run of three or more
    # above-median sentences with no relief.
    room = band(a["stack_share"], [0.0, 0.10, 0.20, 0.35], [5, 4, 3, 2, 1])

    # Open. The first sentence sets the beat. A long one loses the room.
    med = a["median"] or 1
    ratio = a["opener"] / med
    opening = band(ratio, [0.6, 1.0, 1.5, 2.5], [5, 4, 3, 2, 1])
    if a["count"] > 1 and a["syllables"][0] > med and a["syllables"][1] > med:
        opening = max(1, opening - 1)

    axes = {
        "breath": breath,
        "variance": variance,
        "landing": land,
        "room": room,
        "open": opening,
    }
    # The weakest axis carries double weight. A passage is only as good as the
    # thing most wrong with it, and averaging hides exactly that.
    mean = sum(axes.values()) / len(axes)
    total = round((mean + 2 * min(axes.values())) / 3, 1)
    kill = min(axes.values()) == 1
    return axes, total, kill


# --------------------------------------------------------------------- report

BLOCKS = "█"


def chart(a, width=52):
    # Cap the scale so one outlier does not flatten every other bar.
    peak = min(max(a["syllables"]), max(8, a["median"] * 3)) or 1
    lines = []
    for i, r in enumerate(a["sentences"]):
        n = r["syllables"]
        length = max(1, round(n / peak * width))
        over = length > width
        bar = BLOCKS * min(length, width) + (">" if over else "")
        mark = {"hard": ".", "soft": "~", "mid": "-"}[r["landing"]]
        flag = " <!" if r["longest_breath"] > 20 else ""
        lines.append(f"{i+1:>3} {bar}{mark} {n}{flag}")
    return "\n".join(lines)


MIN_SENTENCES = 4


def short_report(a):
    """Under four sentences there is no rhythm to measure, only sound.
    Scoring variance on a headline produces a confident wrong answer."""
    out = []
    out.append("MIC CHECK")
    out.append("=" * 62)
    plural = "sentence" if a["count"] == 1 else "sentences"
    out.append(f"{a['count']} {plural}. Too short to score.")
    out.append("")
    out.append("Rhythm is a relationship between sentences, and there are not")
    out.append("enough here to have one. Variance, room, and open would all be")
    out.append("noise. What can still be said:")
    out.append("")
    for i, r in enumerate(a["sentences"]):
        tag = {"hard": "lands hard", "soft": "trails off", "mid": "lands mid"}[r["landing"]]
        air = "  NO AIR" if r["longest_breath"] > 20 else ""
        out.append(f"  s{i+1}  {r['syllables']} syl, longest run {r['longest_breath']}, {tag}{air}")
    out.append("")
    out.append("Run the mouth test instead. Say it out loud at the speed you")
    out.append("would actually say it, and mark every stumble. See")
    out.append("references/sound.md.")
    out.append("")
    return "\n".join(out)


def report(a, quiet=False):
    if a["count"] < MIN_SENTENCES:
        return short_report(a)

    axes, total, kill = score(a)
    out = []
    out.append("MIC CHECK")
    out.append("=" * 62)
    out.append(
        f"{a['count']} sentences | median {a['median']:.0f} syl | "
        f"shortest {a['shortest']} | longest {a['longest']} | stdev {a['stdev']}"
    )
    if a["quoted_lines_skipped"]:
        out.append(
            f"{a['quoted_lines_skipped']} blockquoted lines skipped. "
            f"Use --include-quotes to score them."
        )
    out.append("")

    if not quiet:
        out.append("RHYTHM")
        out.append("-" * 62)
        out.append(chart(a))
        out.append("")
        out.append("  . lands hard   ~ trails off   - lands mid   <! no air")
        out.append("")

    out.append("SCORE")
    out.append("-" * 62)
    labels = {
        "breath": "Breath   can a person say it in one go",
        "variance": "Variance does the length change",
        "landing": "Landing  do sentences stop or trail",
        "room":  "Room     is there space after the heavy lines",
        "open":  "Open     does the first line earn the second",
    }
    for key, label in labels.items():
        v = axes[key]
        out.append(f"  {label:<48} {v}/5 {'#' * v}")
    out.append(f"  {'OVERALL':<48} {total}/5")
    out.append("")

    out.append("FLAGS")
    out.append("-" * 62)
    flags = []
    for i in a["breath_over_20"]:
        s = a["sentences"][i]
        flags.append(
            f"  No air    s{i+1}: {s['longest_breath']} syllables with no break. "
            f"\"{s['text'][:60]}...\""
        )
    for start, end, length in a["drone_runs"]:
        flags.append(
            f"  Drone     s{start+1}-s{end+1}: {length} sentences in a row within "
            f"3 syllables of each other."
        )
    for start, end, length in a["stack_runs"]:
        if length < 3:
            continue
        flags.append(
            f"  Stacked   s{start+1}-s{end+1}: {length} sentences above the median "
            f"in a row, with no relief between them."
        )
    if a["stop_pct"] < 25:
        flags.append(
            f"  Trailing  {a['soft_pct']}% of sentences end on a weak syllable or a "
            f"function word. The passage never stops, it fades."
        )
    if a["stop_pct"] > 90:
        flags.append(
            f"  Relentless almost every sentence lands hard. Every line is a punch, "
            f"so none of them are."
        )
    if a["opener"] > a["median"] * 1.5:
        flags.append(
            f"  Slow open s1 is {a['opener']} syllables against a median of "
            f"{a['median']:.0f}. The first line is the one that has to work hardest."
        )
    if not flags:
        flags.append("  None. The rhythm holds.")
    out.extend(flags)
    out.append("")

    if kill:
        out.append("VERDICT: REWRITE")
        out.append("  This scores 1 on a structural axis. Editing it line by line")
        out.append("  will not fix the shape. Write the passage again.")
    elif total < 3:
        out.append("VERDICT: FIX THE SHAPE")
        out.append("  The problems are in the arrangement, not the wording.")
    elif total < 4:
        out.append("VERDICT: PASSES, BARELY")
        out.append("  Readable. Not memorable. Fix the lowest axis first.")
    else:
        out.append("VERDICT: IT PLAYS")
    out.append("")
    return "\n".join(out)


def main():
    args = [a for a in sys.argv[1:]]
    as_json = "--json" in args
    quiet = "--quiet" in args
    keep_quotes = "--include-quotes" in args
    paths = [a for a in args if not a.startswith("--")]

    if paths:
        try:
            with open(paths[0], "r", encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            sys.stderr.write(f"miccheck: cannot read {paths[0]}: {exc}\n")
            return 1
    else:
        text = sys.stdin.read()

    a = analyze(text, keep_quotes=keep_quotes)
    if a is None:
        sys.stderr.write("miccheck: no sentences found.\n")
        return 1

    if as_json:
        payload = dict(a)
        payload["sentences"] = [
            {k: v for k, v in r.items() if k != "text"} for r in a["sentences"]
        ]
        if a["count"] < MIN_SENTENCES:
            payload["scored"] = False
            payload["reason"] = "too short to score: fewer than 4 sentences"
        else:
            axes, total, kill = score(a)
            payload["scored"] = True
            payload["axes"] = axes
            payload["overall"] = total
            payload["kill"] = kill
        print(json.dumps(payload, indent=2))
    else:
        print(report(a, quiet=quiet))
    return 0


if __name__ == "__main__":
    sys.exit(main())
