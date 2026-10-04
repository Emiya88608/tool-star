import json
import re
from pathlib import Path

import pandas as pd


root = Path(__file__).resolve().parent
sft_candidates = [
    root / "LLaMA-Factory-main" / "data" / "toolstar-sft.json",
    root / "LLaMA-Factory-main" / "data" / "final_sft_edition9.json",
    root / "data-toolstar" / "sft" / "final_sft_edition9.json",
]
sft_path = next((path for path in sft_candidates if path.exists()), sft_candidates[0])
rl_path = root / "data-toolstar" / "rl" / "grpo_mix_train.parquet"

if sft_path.exists():
    sft = json.loads(sft_path.read_text(encoding="utf-8"))
    print("SFT type:", type(sft).__name__)
    print("SFT rows:", len(sft))
    if isinstance(sft, list):
        print("SFT columns:", list(sft[0]))
        print("SFT first row:", json.dumps(sft[0], ensure_ascii=False)[:1500])
        tags = {}
        for row in sft[:5000]:
            for tag in re.findall(r"<([a-zA-Z_][\w-]*)>", row.get("output", "")):
                tags[tag] = tags.get(tag, 0) + 1
        print("SFT output tags:", sorted(tags.items(), key=lambda item: item[1], reverse=True))
        python_rows = [
            row
            for row in sft
            if "<python>" in row.get("output", "") and "</python>" in row.get("output", "")
        ]
        print("SFT python rows:", len(python_rows))
        python_no_search_rows = [
            row for row in python_rows if "<search>" not in row.get("output", "")
        ]
        print("SFT python-only rows:", len(python_no_search_rows))
        if python_rows:
            print(
                "SFT python example:",
                json.dumps(python_rows[0], ensure_ascii=False)[:2500],
            )

rl = pd.read_parquet(rl_path)
print("RL shape:", rl.shape)
print("RL columns:", list(rl.columns))
print("RL first row:", rl.iloc[0].to_dict())
print("RL data_source counts:")
print(rl["data_source"].value_counts().to_string())
print("RL ability counts:")
print(rl["ability"].value_counts().to_string())
