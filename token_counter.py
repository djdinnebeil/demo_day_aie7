import tiktoken
from pathlib import Path

ROOT_DIR = './amatol2'

def find_txt_files(root_dir: str) -> list[Path]:
    return [p for p in Path(root_dir).rglob('*.txt')]

def count_tokens(text: str, model: str = 'text-embedding-3-small') -> int:
    """Return token count for a given string using the specified model's tokenizer."""
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

import statistics

def report_token_counts(root_dir: str, model: str = 'text-embedding-3-small') -> None:
    paths = find_txt_files(root_dir)
    if not paths:
        print(f'No .txt files found under {root_dir}')
        return

    token_counts = []
    for path in paths:
        text = path.read_text(encoding='utf-8', errors='ignore')
        tokens = count_tokens(text, model)
        token_counts.append((path.name, tokens))

    # Sort by size
    token_counts.sort(key=lambda x: x[1])

    # Print per-file breakdown
    print("\nToken counts per file:")
    for name, tokens in token_counts:
        print(f"  {name:<60} {tokens:>6} tokens")

    values = [t for _, t in token_counts]
    total = sum(values)
    avg = statistics.mean(values)
    median = statistics.median(values)
    stdev = statistics.pstdev(values)

    print("\nSummary statistics:")
    print(f"  Files: {len(values)}")
    print(f"  Total tokens: {total}")
    print(f"  Avg tokens per file: {avg:.1f}")
    print(f"  Median tokens per file: {median}")
    print(f"  Min tokens: {min(values)}")
    print(f"  Max tokens: {max(values)}")
    print(f"  Std dev: {stdev:.1f}")

    # Histogram buckets
    buckets = {
        "<200": 0,
        "200–500": 0,
        "500–1000": 0,
        "1000–2000": 0,
        ">2000": 0
    }
    for v in values:
        if v < 200:
            buckets["<200"] += 1
        elif v < 500:
            buckets["200–500"] += 1
        elif v < 1000:
            buckets["500–1000"] += 1
        elif v < 2000:
            buckets["1000–2000"] += 1
        else:
            buckets[">2000"] += 1

    print("\nHistogram (token count per file):")
    for k, v in buckets.items():
        print(f"  {k:<10}: {v} files")

report_token_counts(ROOT_DIR)