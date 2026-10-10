# readability-skill

**What it does.** Gives evidence-based feedback on how readable a document, slide deck or web page is, and suggests specific rewrites. It is built on five principles (space, chunks, guides, information structure, language) and covers plain language, accessibility, dyslexia, PowerPoint, and web typography. A small script adds objective metrics: word, sentence and paragraph counts, average lengths, a Dale-Chall score, difficult words, Academic Word List matches and long sentences.

**Who it is for.** Writers, editors, teachers and communicators who want concrete, text-specific advice rather than generic style rules.

**What you need.**

- Claude Code or Codex.
- Python 3 for the optional analysis script (standard library only; no packages to install).
- No accounts, API keys or paid services; the skill is under 1 MB.

**Install.**

```bash
# Claude Code
git clone https://github.com/techczech/readability-skill ~/.claude/skills/readability-skill

# Codex
git clone https://github.com/techczech/readability-skill ~/.codex/skills/readability-skill
```

## Use

Ask the agent to check or improve the readability of some text, a file or a slide deck. The agent applies the guidance in `SKILL.md` and the files in `references/`, quotes your text, shows an improved version and limits itself to five suggestions at a time.

You can also run the script directly:

```bash
python scripts/analyze_readability.py "Your text here"
python scripts/analyze_readability.py --file document.txt
cat document.txt | python scripts/analyze_readability.py --stdin
python scripts/analyze_readability.py --file document.txt --json
```

## Layout

```
SKILL.md                       # the skill definition the agent reads
references/                    # principles, plain language, accessibility, slides, web
scripts/analyze_readability.py # readability metrics
scripts/data/                  # word lists used by the script
```

## Data sources

`scripts/data/` bundles two word lists that the script uses. The files themselves carry no header or citation; the origins below are taken from the project's own provenance notes and are not stated in the files.

- `dale_chall_words.txt` (2,942 entries): the Dale-Chall list of familiar words (Dale and Chall, 1948; revised 1995).
- `awl_words.txt` (571 entries): the Academic Word List (Coxhead, 2000).

They are included for research and educational use. If you are a rights holder and want one removed, please open an issue.

## Credits

The five principles follow "Foundations of Readable and Accessible Documents" (<https://bit.ly/ox-templates>) by Dominik Lukeš. GOV.UK and WCAG figures are attributed where they appear.

## Licence

MIT for the skill text and script; see `LICENSE`. The bundled word lists remain the work of their original authors.
