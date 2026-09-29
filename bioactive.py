"""
Bioactive - Bioactivity Classification Environment

Single-turn environment where agents classify molecules as active or inactive
against biological targets. Uses the HIV replication inhibition dataset.

Data source: TDC HIV dataset (41,127 molecules).
Binary reward: 1.0 for correct classification, 0.0 for incorrect.
"""

import json
import os
from pathlib import Path
from typing import List

from pydantic import BaseModel, Field

from openreward.environments import (
    Environment,
    JSONObject,
    Split,
    TextBlock,
    ToolOutput,
    tool,
)

if os.path.exists("/orwd_data"):
    ENV_PATH = Path("/orwd_data")
else:
    ENV_PATH = Path(__file__).parent


def load_all_tasks() -> dict[str, list[dict]]:
    data_dir = ENV_PATH / "data"
    all_tasks = {}
    for split in ["train", "test"]:
        json_file = data_dir / f"{split}.json"
        if json_file.exists():
            with open(json_file, "r", encoding="utf-8") as f:
                all_tasks[split] = json.load(f)
        else:
            print(f"Warning: {json_file} not found")
            all_tasks[split] = []
    return all_tasks


ALL_TASKS = load_all_tasks()

ANSWERS = {
    task["task_id"]: {"value": task["answer"]}
    for split_tasks in ALL_TASKS.values()
    for task in split_tasks
}

print(f"Loaded {len(ANSWERS)} Bioactive tasks")


# Reward for a submission made after the task has already been graded. Negative
# so repeat submissions are actively discouraged, not merely left unscored.
REPEAT_SUBMISSION_PENALTY = -0.1


class BioactiveTaskSpec(BaseModel):
    task_id: str
    smiles: str
    property_name: str
    class_labels: str
    question: str


class SubmitClassificationInput(BaseModel):
    prediction: int = Field(
        ..., description="Your predicted class: 0 (inactive) or 1 (active)"
    )


class Bioactive(Environment):
    """
    Bioactivity classification environment.

    Agents classify molecules as active or inactive against HIV replication.
    Binary reward: 1.0 for correct, 0.0 for incorrect.
    """

    def __init__(self, task_spec: JSONObject, secrets: dict[str, str] = {}) -> None:
        super().__init__(task_spec)
        self.validated = BioactiveTaskSpec.model_validate(task_spec)

        if self.validated.task_id not in ANSWERS:
            raise ValueError(f"Task {self.validated.task_id} not found in ANSWERS")

        self.answer = ANSWERS[self.validated.task_id]

        # Graded submissions this session. Only the first is rewarded. This is a
        # BINARY label, so an uncapped tool scores 1.0 on every task in two calls
        # without predicting anything: submit 0, read that it was wrong, submit
        # the other value.
        self.submitted = 0

    @classmethod
    def list_splits(cls) -> list[Split]:
        return [
            Split(name="train", type="train"),
            Split(name="test", type="test"),
        ]

    @classmethod
    def list_tasks(cls, split: str) -> list[JSONObject]:
        if split not in ALL_TASKS:
            return []
        return [
            {k: v for k, v in task.items() if k != "answer"}
            for task in ALL_TASKS[split]
        ]

    async def get_prompt(self) -> List[TextBlock]:
        return [TextBlock(text=self.validated.question)]

    @tool
    async def submit_prediction(self, params: SubmitClassificationInput) -> ToolOutput:
        """Submit your bioactivity classification for the molecule (0 = inactive, 1 = active)."""
        if self.submitted > 0:
            return ToolOutput(
                blocks=[TextBlock(text="A prediction has already been submitted for this task. "
                                       "This episode is over: it is not re-graded, and repeat "
                                       "submissions are penalised (reward -0.1).")],
                metadata={"task_id": self.validated.task_id, "already_submitted": True,
                          "submission_count": self.submitted},
                reward=REPEAT_SUBMISSION_PENALTY,
                finished=True,
            )

        predicted = params.prediction
        # A value other than 0 or 1 is not a classification, so it is not graded
        # and does not count as the submission.
        if predicted not in (0, 1):
            return ToolOutput(
                blocks=[TextBlock(text=f"Error: Prediction must be 0 (inactive) or 1 (active), got {predicted}. "
                                       "Nothing was graded; resubmit with 0 or 1.")],
                metadata={"task_id": self.validated.task_id, "error": "invalid_prediction",
                          "predicted": predicted},
                reward=0.0,
                finished=False,
            )

        actual = self.answer["value"]
        correct = predicted == actual
        reward = 1.0 if correct else 0.0

        if correct:
            feedback = (
                f"Correct! The molecule is {'active' if actual == 1 else 'inactive'} "
                f"against {self.validated.property_name}.\n"
                f"Reward: {reward:.1f}"
            )
        else:
            feedback = (
                f"Incorrect. You predicted {'active' if predicted == 1 else 'inactive'} "
                f"against {self.validated.property_name}.\n"
                f"Reward: {reward:.1f}"
            )

        self.submitted += 1

        return ToolOutput(
            blocks=[TextBlock(text=feedback)],
            metadata={
                "task_id": self.validated.task_id,
                "smiles": self.validated.smiles,
                "property_name": self.validated.property_name,
                "predicted": predicted,
                "correct": correct,
            },
            reward=reward,
            finished=True,
        )
