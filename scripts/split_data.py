import json
import random
from pathlib import Path

def split_clean_sentences(input_file, output_dir, seed=42):
    random.seed(seed)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    with open(input_file, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]

    random.shuffle(records)
    total = len(records)
    train_end = int(0.80 * total)
    val_end = int(0.90 * total)

    splits = {
        "train_clean.jsonl": records[:train_end],
        "val_clean.jsonl": records[train_end:val_end],
        "test_clean.jsonl": records[val_end:]
    }

    for fname, data in splits.items():
        with open(out_path / fname, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    split_clean_sentences(
        "/content/drive/MyDrive/thesis-data/processed/clean_sentences.jsonl",
        "/content/drive/MyDrive/thesis-data/processed/splits"
    )
