# BioClassify

[![OpenReward Environment](https://img.shields.io/badge/%E2%AD%90%20OpenReward-Environment-f7e6cc)](https://openreward.ai/GeneralReasoning/BioClassify)

## Description

**BioClassify** is an environment for evaluating agents on bioactivity classification tasks. Given a molecule's SMILES string, the agent predicts whether the molecule is active or inactive as an HIV replication inhibitor. The dataset is derived from the [TDC HIV dataset](https://tdcommons.ai/single_pred_tasks/hts/#hiv) (DTP AIDS Antiviral Screen), containing 41,127 molecules screened for ability to inhibit HIV replication.

## Capabilities

- Predicting bioactivity from molecular SMILES notation
- Classifying molecules as active or inactive against HIV replication
- Understanding structure-activity relationships for antiviral compounds

## Compute Requirements

BioClassify does not require a sandbox. It has minimal compute requirements.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (following the TDC dataset license).

## Tasks

There are two splits: train (1,000 tasks) and test (100 tasks). Tasks are sampled from the TDC HIV dataset with stratified sampling targeting ~30% active compounds. Each task presents a molecule's SMILES string and asks the agent to classify it as active (1) or inactive (0) against HIV replication.

| Split | Tasks | Inactive (0) | Active (1) | Active Rate |
|-------|-------|-------------|------------|-------------|
| Train | 1,000 | 705 | 295 | 29.5% |
| Test | 100 | 65 | 35 | 35.0% |

## Reward Structure

This is a sparse, verifiable reward environment with binary scoring. The agent calls `submit_prediction` once with a classification (0 or 1).

- **Correct**: Reward **1.0**.
- **Incorrect**: Reward **0.0**.

We do not use LLM graders for this task.

## Data

Task data is derived from the [TDC HIV dataset](https://tdcommons.ai/single_pred_tasks/hts/#hiv) (DTP AIDS Antiviral Screen, 41,127 molecules). Data files are stored on the OpenReward platform.

## Tools

Agents are given a single tool:

- `submit_prediction`: Submit a bioactivity classification (0 = inactive, 1 = active). Returns whether the prediction is correct. This tool can only be called once per task.

## Time Horizon

BioClassify is a single-turn environment. The agent receives a molecule's SMILES string and submits one classification. Each task requires exactly one tool call.

## Environment Difficulty

[Statistics on environment difficulty here]

## Other Environment Requirements

There are no further environment requirements; BioClassify works out of the box with the OpenReward endpoint without any secrets.

## Safety

Agents in BioClassify are asked to classify molecules for bioactivity against HIV replication. The environment does not present direct safety risks, as agents only provide classification predictions with no access to external systems.

However, this is a dual-use domain. Models trained for bioactivity prediction capabilities could potentially be misused for designing harmful compounds in other contexts.

## Citations

```bibtex
@dataset{GRBioClassify,
  author    = {General Reasoning Inc. Team},
  title     = {BioClassify},
  year      = {2026},
  publisher = {OpenReward},
  url       = {https://openreward.ai/GeneralReasoning/BioClassify}
}
```

```bibtex
@article{AIDS2004screening,
  title={AIDS Antiviral Screen Data},
  author={{National Cancer Institute (NCI)}},
  journal={DTP AIDS Antiviral Screen},
  year={2004},
  note={Available via Therapeutics Data Commons (TDC)}
}
```
