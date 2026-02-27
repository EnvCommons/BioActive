"""
Download and prepare HIV bioactivity dataset from TDC.

Creates 1000 train + 100 test tasks from HIV dataset (41,127 molecules).
Ensures balanced class representation in the selected subset.
Run once locally: python prepare_data.py
"""

import json
from pathlib import Path

import pandas as pd
from tdc.single_pred import HTS

PROPERTY_NAME = "HIV Replication Inhibition"
CLASS_LABELS = "0 = inactive, 1 = active"
TRAIN_SIZE = 1000
TEST_SIZE = 100
TOTAL = TRAIN_SIZE + TEST_SIZE


def make_question(smiles: str) -> str:
    return (
        f"You are a drug discovery expert specializing in bioactivity prediction.\n\n"
        f"Given the molecule with SMILES notation: {smiles}\n\n"
        f"Predict whether this molecule is active (1) or inactive (0) against "
        f"HIV replication. Active compounds inhibit HIV replication in vitro.\n\n"
        f"Classes: {CLASS_LABELS}\n\n"
        f"Submit your prediction as 0 or 1 using the submit_prediction tool."
    )


def main():
    print("Downloading HIV dataset...")
    data = HTS(name="HIV")
    df = data.get_data()
    df = df.dropna(subset=["Drug", "Y"])
    df = df.drop_duplicates(subset=["Drug"])
    df["Y"] = df["Y"].astype(int)
    df = df[df["Y"].isin([0, 1])]

    print(f"Total molecules: {len(df)}")
    print(f"Class distribution: {df['Y'].value_counts().to_dict()}")

    # Stratified sampling to ensure both classes are represented
    active = df[df["Y"] == 1].sample(frac=1, random_state=42)
    inactive = df[df["Y"] == 0].sample(frac=1, random_state=42)

    # Target ~30% active to make it non-trivial but not too imbalanced
    n_active = min(len(active), int(TOTAL * 0.3))
    n_inactive = TOTAL - n_active

    selected = pd.concat([
        active.head(n_active),
        inactive.head(n_inactive),
    ]).sample(frac=1, random_state=42).reset_index(drop=True)

    print(f"Selected {len(selected)} molecules: {selected['Y'].value_counts().to_dict()}")

    tasks = []
    for idx, row in selected.iterrows():
        split = "test" if idx < TEST_SIZE else "train"
        task = {
            "task_id": f"bio_{split}_{idx}",
            "smiles": row["Drug"],
            "property_name": PROPERTY_NAME,
            "class_labels": CLASS_LABELS,
            "answer": int(row["Y"]),
            "question": make_question(row["Drug"]),
        }
        tasks.append(task)

    test_tasks = [t for t in tasks if "test" in t["task_id"]]
    train_tasks = [t for t in tasks if "train" in t["task_id"]]

    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    with open(data_dir / "test.json", "w") as f:
        json.dump(test_tasks, f, indent=2)
    with open(data_dir / "train.json", "w") as f:
        json.dump(train_tasks, f, indent=2)

    print(f"\nSaved {len(train_tasks)} train tasks and {len(test_tasks)} test tasks")


if __name__ == "__main__":
    main()
