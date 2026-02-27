# Data Upload Requirements for Bioactive

## Overview
This environment requires HIV bioactivity classification data uploaded to OpenReward cloud storage.

## Directory Structure
```
/orwd_data/
└── data/
    ├── train.json (1000 tasks, ~400 KB)
    └── test.json (100 tasks, ~40 KB)
```

## Files Required
- **train.json**: 1000 HIV bioactivity classification tasks from TDC HIV dataset
- **test.json**: 100 HIV bioactivity classification tasks (stratified sampling ~30% active)

## Data Generation
Run locally: `python prepare_data.py` (requires `pip install PyTDC pandas`)

## Upload Instructions
Upload the `data/` directory to your OpenReward namespace at https://openreward.ai.
