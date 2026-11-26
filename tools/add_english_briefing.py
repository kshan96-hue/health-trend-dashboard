#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inserts/replaces the englishBriefing block in a daily report JSON.

Usage: add_briefing <date>   (from the repository root)
The block is written with the file's existing 1-space indent style so the
rest of the report stays byte-identical.
"""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

BRIEFINGS = {
    "2026-11-26": {
        "title": "Korea Health Supplement Market Briefing — Thursday, November 26, 2026",
        "duration": "14문장 · 약 2분 (1.0x 기준)",
        "sentences": [
            "Good morning. This is your Korea health supplement market briefing for Thursday, November 26.",
            "Four things matter today: one new advertising rule, nine product launches, a quiet shift in search, and a surprise on Coupang.",
            "First, regulation. Starting tomorrow, Korean ads for food and supplements may not use AI-generated virtual doctors, pharmacists, or professors to recommend a product.",
            "Even a label saying the person is virtual will not help, and the penalty goes up to five years in prison or a fine of fifty million won.",
            "Second, new products. We confirmed nine launches between November 24 and 26, and they fall into three clear directions.",
            "One is the senior market through Daiso, where Ankuk Pharmaceutical introduced a single-tablet ginkgo product and a phosphatidylserine powder stick.",
            "Another is convenience in one dose: Newon's gum health tablet combines fifteen ingredients in a single tablet, launched on home shopping today.",
            "The third is dual format, a liquid shot plus tablets in the same bottle, which already holds the top three spots in convenience store sales.",
            "On the food side, Maeil's protein bars cut the size to forty grams and sugar below two grams, so a protein bar now reads as a meal, not a snack.",
            "Third, search. Omega-3, magnesium lactate, and magnesium held the top three, while melatonin moved up two places to eighth.",
            "NMN dropped out of the top twenty and a bone-health ingredient came in, so anti-aging interest looks to be moving from NMN toward CoQ10 and bone health.",
            "On YouTube this week, two themes won: value picks from Costco and Daiso, and anti-aging claims built around CoQ10 and NMN.",
            "Daiso supplement shorts passed two million views each, so price-led comparison content is reaching a far wider audience than ingredient science.",
            "Finally, commerce. A creatine powder ranked eighth on Coupang by units sold at about twenty-one thousand won, which tells us strength supplements are moving from gym users to everyday consumers.",
        ],
    }
}


def main():
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-11-26"
    data = BRIEFINGS[date]
    path = os.path.join(ROOT, "data", "daily", date + ".json")
    with open(path, encoding="utf-8") as f:
        raw = f.read()

    block = json.dumps({"englishBriefing": data}, ensure_ascii=False, indent=1)
    # 1-space top-level indent: strip the outer braces, keep inner lines prefixed by one space
    inner = block.split("\n", 1)[1].rsplit("\n", 1)[0]
    new_block = inner + ",\n"

    if '"englishBriefing"' in raw:
        # replace an existing block: from the key line up to the line before the next top-level key
        start = raw.index(' "englishBriefing"')
        m = re.compile(r"\n ([a-zA-Z\"]+)", re.M).search(raw, raw.index("\n", raw.index('"englishBriefing"')))
        # find the next top-level key after the block
        idx = raw.index('"englishBriefing"')
        nxt = re.compile(r"\n \"[a-zA-Z]+\": ").search(raw, idx)
        if nxt:
            end = nxt.start() + 1
            # keep a trailing comma if the following key exists (it always does unless last)
            raw = raw[:start + 1] + new_block + raw[end:]
        else:
            raw = raw[:start + 1] + new_block.rstrip(",\n") + "\n" + raw[end:]
    else:
        # insert before "views" so the date/header block stays on top
        pos = raw.index('\n "views":')
        raw = raw[:pos + 1] + new_block + raw[pos + 1:]

    json.loads(raw)  # validate before writing
    with open(path, "w", encoding="utf-8") as f:
        f.write(raw)
    print("updated", path, "sentences:", len(data["sentences"]),
          "words:", sum(len(s.split()) for s in data["sentences"]))


if __name__ == "__main__":
    main()
