#!/usr/bin/env python3
"""
Readability Analysis Script

Analyzes text for readability metrics including:
- Word, sentence, and paragraph counts
- Average sentence and word lengths
- Dale-Chall readability score
- Identification of difficult words (not in Dale-Chall list)
- Academic Word List (AWL) detection
- Examples of long sentences

Usage:
    python analyze_readability.py "Your text here"
    python analyze_readability.py --file input.txt
    cat input.txt | python analyze_readability.py --stdin
"""

import re
import sys
import argparse
import json
from pathlib import Path
from typing import List, Dict, Tuple, Set
from collections import Counter

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.resolve()

def load_word_list(filename: str) -> Set[str]:
    """Load a word list from a file in the data directory."""
    filepath = SCRIPT_DIR / "data" / filename
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return set(word.strip().lower() for word in f.readlines() if word.strip())
    return set()

# Load word lists
DALE_CHALL_WORDS = load_word_list("dale_chall_words.txt")
AWL_WORDS = load_word_list("awl_words.txt")

def tokenize_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    # Handle common abbreviations
    text = re.sub(r'\b(Mr|Mrs|Ms|Dr|Prof|Jr|Sr|vs|etc|i\.e|e\.g)\.\s', r'\1_DOT_ ', text, flags=re.IGNORECASE)

    # Split on sentence-ending punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Restore abbreviations
    sentences = [s.replace('_DOT_', '.') for s in sentences]

    # Filter out empty sentences
    return [s.strip() for s in sentences if s.strip()]

def tokenize_words(text: str) -> List[str]:
    """Extract words from text."""
    # Remove punctuation and split on whitespace
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return [w for w in words if len(w) > 0]

def get_word_stem(word: str) -> str:
    """Get a simple stem by removing common suffixes."""
    word = word.lower()
    # Dale-Chall allows these suffixes: 's, -s, -r, -d, -es, -ies, -ed, -ied, -ing, -er, -est, -ier, -iest
    suffixes = ['iest', 'ier', 'ing', 'ied', 'ies', 'est', 'ed', 'er', 'es', 's', 'd', 'r']
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) - len(suffix) >= 2:
            stem = word[:-len(suffix)]
            # Check if stem or stem with 'e' is in list
            if stem in DALE_CHALL_WORDS or (stem + 'e') in DALE_CHALL_WORDS:
                return stem
            # For -ied, check -y form
            if suffix == 'ied' and (stem + 'y') in DALE_CHALL_WORDS:
                return stem + 'y'
            # For -ies, check -y form
            if suffix == 'ies' and (stem + 'y') in DALE_CHALL_WORDS:
                return stem + 'y'
    return word

def is_dale_chall_word(word: str) -> bool:
    """Check if a word is in the Dale-Chall easy word list."""
    word = word.lower().strip("'")
    if word in DALE_CHALL_WORDS:
        return True
    # Check with common suffixes removed
    stem = get_word_stem(word)
    return stem in DALE_CHALL_WORDS

def is_awl_word(word: str) -> bool:
    """Check if a word is in the Academic Word List."""
    word = word.lower().strip("'")
    if word in AWL_WORDS:
        return True
    stem = get_word_stem(word)
    return stem in AWL_WORDS

def count_syllables(word: str) -> int:
    """Estimate the number of syllables in a word."""
    word = word.lower()
    if len(word) <= 3:
        return 1

    # Count vowel groups
    vowels = 'aeiouy'
    count = 0
    prev_is_vowel = False

    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel

    # Adjust for silent 'e'
    if word.endswith('e') and count > 1:
        count -= 1

    # Adjust for -le endings
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1

    return max(1, count)

def calculate_dale_chall_score(words: List[str], sentences: List[str]) -> Tuple[float, float]:
    """
    Calculate the Dale-Chall readability score.

    Formula:
    Raw Score = 0.1579 * (difficult_words / total_words * 100) + 0.0496 * (total_words / total_sentences)

    If percentage of difficult words > 5%, add 3.6365 to get adjusted score.

    Returns: (raw_score, adjusted_score)
    """
    if not words or not sentences:
        return 0.0, 0.0

    difficult_words = [w for w in words if not is_dale_chall_word(w)]
    difficult_percentage = (len(difficult_words) / len(words)) * 100
    avg_sentence_length = len(words) / len(sentences)

    raw_score = 0.1579 * difficult_percentage + 0.0496 * avg_sentence_length

    if difficult_percentage > 5:
        adjusted_score = raw_score + 3.6365
    else:
        adjusted_score = raw_score

    return raw_score, adjusted_score

def dale_chall_grade_level(score: float) -> str:
    """Convert Dale-Chall score to approximate grade level."""
    if score <= 4.9:
        return "Grade 4 and below (easily understood)"
    elif score <= 5.9:
        return "Grades 5-6"
    elif score <= 6.9:
        return "Grades 7-8"
    elif score <= 7.9:
        return "Grades 9-10"
    elif score <= 8.9:
        return "Grades 11-12"
    elif score <= 9.9:
        return "College level"
    else:
        return "College graduate level"

def analyze_text(text: str) -> Dict:
    """Perform comprehensive readability analysis on text."""
    # Basic tokenization
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    sentences = tokenize_sentences(text)
    words = tokenize_words(text)

    # Calculate metrics
    total_words = len(words)
    total_sentences = len(sentences)
    total_paragraphs = len(paragraphs)

    # Word length analysis
    word_lengths = [len(w) for w in words]
    avg_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

    # Sentence length analysis
    sentence_word_counts = [len(tokenize_words(s)) for s in sentences]
    avg_sentence_length = sum(sentence_word_counts) / len(sentence_word_counts) if sentence_word_counts else 0

    # Find long sentences (over 25 words)
    long_sentences = [(s, len(tokenize_words(s))) for s in sentences if len(tokenize_words(s)) > 25]
    long_sentences.sort(key=lambda x: x[1], reverse=True)

    # Find the longest sentence
    longest_sentence = max(sentences, key=lambda s: len(tokenize_words(s))) if sentences else ""
    longest_sentence_words = len(tokenize_words(longest_sentence))

    # Difficult words analysis
    difficult_words = [w for w in words if not is_dale_chall_word(w)]
    difficult_word_counts = Counter(difficult_words)
    unique_difficult_words = list(difficult_word_counts.keys())
    difficult_percentage = (len(difficult_words) / total_words * 100) if total_words else 0

    # AWL words analysis
    awl_found = [w for w in words if is_awl_word(w)]
    awl_word_counts = Counter(awl_found)
    unique_awl_words = list(awl_word_counts.keys())

    # Dale-Chall score
    raw_score, adjusted_score = calculate_dale_chall_score(words, sentences)
    grade_level = dale_chall_grade_level(adjusted_score)

    # Syllable analysis
    total_syllables = sum(count_syllables(w) for w in words)
    avg_syllables_per_word = total_syllables / total_words if total_words else 0

    return {
        'basic_stats': {
            'total_words': total_words,
            'total_sentences': total_sentences,
            'total_paragraphs': total_paragraphs,
            'total_syllables': total_syllables,
        },
        'averages': {
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_word_length': round(avg_word_length, 1),
            'avg_syllables_per_word': round(avg_syllables_per_word, 2),
            'target_sentence_length': '15-20 words',
        },
        'dale_chall': {
            'raw_score': round(raw_score, 2),
            'adjusted_score': round(adjusted_score, 2),
            'grade_level': grade_level,
            'difficult_word_percentage': round(difficult_percentage, 1),
        },
        'difficult_words': {
            'total_count': len(difficult_words),
            'unique_count': len(unique_difficult_words),
            'top_20': difficult_word_counts.most_common(20),
            'all_unique': sorted(unique_difficult_words)[:100],  # Limit for display
        },
        'awl_words': {
            'total_count': len(awl_found),
            'unique_count': len(unique_awl_words),
            'found': sorted(unique_awl_words),
        },
        'long_sentences': {
            'count': len(long_sentences),
            'examples': [(s[:150] + '...' if len(s) > 150 else s, wc) for s, wc in long_sentences[:5]],
        },
        'longest_sentence': {
            'text': longest_sentence[:300] + ('...' if len(longest_sentence) > 300 else ''),
            'word_count': longest_sentence_words,
        },
    }

def format_results_table(results: Dict) -> str:
    """Format results as a readable table."""
    lines = []

    lines.append("=" * 70)
    lines.append("READABILITY ANALYSIS REPORT")
    lines.append("=" * 70)

    # Basic Stats
    lines.append("\n## BASIC STATISTICS")
    lines.append("-" * 40)
    stats = results['basic_stats']
    lines.append(f"  Words:        {stats['total_words']:,}")
    lines.append(f"  Sentences:    {stats['total_sentences']:,}")
    lines.append(f"  Paragraphs:   {stats['total_paragraphs']:,}")
    lines.append(f"  Syllables:    {stats['total_syllables']:,}")

    # Averages
    lines.append("\n## AVERAGES")
    lines.append("-" * 40)
    avgs = results['averages']
    status = "✓" if 15 <= avgs['avg_sentence_length'] <= 20 else "⚠"
    lines.append(f"  Avg sentence length:     {avgs['avg_sentence_length']} words {status}")
    lines.append(f"  (Target:                 {avgs['target_sentence_length']})")
    lines.append(f"  Avg word length:         {avgs['avg_word_length']} characters")
    lines.append(f"  Avg syllables per word:  {avgs['avg_syllables_per_word']}")

    # Dale-Chall
    lines.append("\n## DALE-CHALL READABILITY")
    lines.append("-" * 40)
    dc = results['dale_chall']
    lines.append(f"  Adjusted Score:          {dc['adjusted_score']}")
    lines.append(f"  Grade Level:             {dc['grade_level']}")
    lines.append(f"  Difficult Word %:        {dc['difficult_word_percentage']}%")

    # Difficult Words
    lines.append("\n## DIFFICULT WORDS (not in Dale-Chall list)")
    lines.append("-" * 40)
    dw = results['difficult_words']
    lines.append(f"  Total occurrences:       {dw['total_count']}")
    lines.append(f"  Unique words:            {dw['unique_count']}")
    if dw['top_20']:
        lines.append("\n  Most frequent difficult words:")
        for word, count in dw['top_20'][:10]:
            lines.append(f"    - {word}: {count}")

    # AWL Words
    lines.append("\n## ACADEMIC WORD LIST (AWL) WORDS")
    lines.append("-" * 40)
    awl = results['awl_words']
    lines.append(f"  Total occurrences:       {awl['total_count']}")
    lines.append(f"  Unique AWL words:        {awl['unique_count']}")
    if awl['found']:
        lines.append(f"\n  AWL words found: {', '.join(awl['found'][:20])}")
        if len(awl['found']) > 20:
            lines.append(f"    ... and {len(awl['found']) - 20} more")

    # Long Sentences
    lines.append("\n## LONG SENTENCES (>25 words)")
    lines.append("-" * 40)
    ls = results['long_sentences']
    lines.append(f"  Count: {ls['count']}")
    if ls['examples']:
        lines.append("\n  Examples:")
        for i, (sent, wc) in enumerate(ls['examples'][:3], 1):
            lines.append(f"\n  {i}. ({wc} words)")
            lines.append(f"     \"{sent}\"")

    # Longest Sentence
    lines.append("\n## LONGEST SENTENCE")
    lines.append("-" * 40)
    longest = results['longest_sentence']
    lines.append(f"  Word count: {longest['word_count']}")
    lines.append(f"  \"{longest['text']}\"")

    lines.append("\n" + "=" * 70)

    return "\n".join(lines)

def format_results_json(results: Dict) -> str:
    """Format results as JSON."""
    return json.dumps(results, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description='Analyze text readability')
    parser.add_argument('text', nargs='?', help='Text to analyze')
    parser.add_argument('--file', '-f', help='Read text from file')
    parser.add_argument('--stdin', action='store_true', help='Read text from stdin')
    parser.add_argument('--json', action='store_true', help='Output as JSON')

    args = parser.parse_args()

    # Get text from appropriate source
    if args.stdin:
        text = sys.stdin.read()
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        sys.exit(1)

    if not text.strip():
        print("Error: No text provided or empty text")
        sys.exit(1)

    # Analyze
    results = analyze_text(text)

    # Output
    if args.json:
        print(format_results_json(results))
    else:
        print(format_results_table(results))

if __name__ == '__main__':
    main()
