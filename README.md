# Bioactive

Single-turn OpenReward environment for classifying molecules as active or inactive against HIV replication from SMILES notation.

## Task

Given a molecule's SMILES string, the agent predicts whether the molecule is active (1) or inactive (0) as an HIV replication inhibitor. One tool call per task.

## Data Source

All data comes from the [TDC HIV dataset](https://tdcommons.ai/single_pred_tasks/hts/#hiv) (DTP AIDS Antiviral Screen), containing 41,127 molecules screened for ability to inhibit HIV replication.

1,100 molecules sampled (1,000 train + 100 test) with stratified sampling targeting ~30% active compounds to make the task non-trivial while reflecting the imbalanced nature of high-throughput screening data.

### Data Statistics

| Split | Tasks | Inactive (0) | Active (1) | Active Rate |
|-------|-------|-------------|------------|-------------|
| Train | 1,000 | 705 | 295 | 29.5% |
| Test | 100 | 65 | 35 | 35.0% |

## Reward Function

Binary reward:

```
reward = 1.0 if predicted == actual else 0.0
```

## Environment API

- **Splits:** `train` (1,000 tasks), `test` (100 tasks)
- **Tool:** `submit_prediction(prediction: int)` -- submit 0 (inactive) or 1 (active)
- **Prompt:** Provides SMILES string and bioactivity endpoint description
- **Finished:** Always `True` after one tool call (single-turn)

## Files

```
bioactive/
├── bioactive.py       # Environment class (Bioactive)
├── server.py          # Server wrapper
├── test_agent.py      # OpenAI Responses API test harness
├── prepare_data.py    # TDC download + JSON generation script
├── requirements.txt   # openreward, pydantic
├── Dockerfile
├── DATA_UPLOAD.md     # Cloud storage upload instructions
└── data/
    ├── train.json     # 1,000 training tasks
    └── test.json      # 100 test tasks
```

## Local Development

```bash
# Generate data (requires PyTDC)
pip install PyTDC pandas
python prepare_data.py

# Run server
pip install -r requirements.txt
python server.py

# Test with agent
export OPENAI_API_KEY=...
python test_agent.py
```

## Docker

```bash
docker build -t bioactive:test .
docker run -p 8080:8080 bioactive:test
```
