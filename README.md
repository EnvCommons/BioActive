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

[MIT](https://opensource.org/licenses/MIT). The underlying TDC HIV dataset is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

## Tasks

There are 1,000 tasks in the `train` split and 100 in `test`. Tasks are sampled from the TDC HIV dataset with stratified sampling targeting ~30% active compounds. Each task presents a molecule's SMILES string and asks the agent to classify it as active (1) or inactive (0) against HIV replication.

| Split | Tasks | Inactive (0) | Active (1) | Active Rate |
|-------|-------|-------------|------------|-------------|
| Train | 1,000 | 705 | 295 | 29.5% |
| Test | 100 | 65 | 35 | 35.0% |

## Reward Structure

This is a sparse, verifiable reward environment with binary scoring. The agent calls `submit_prediction` with a classification (0 or 1). The first graded prediction ends the episode; a value other than 0 or 1 is not graded, and a submission after grading gets -0.1.

- **Correct**: Reward **1.0**.
- **Incorrect**: Reward **0.0**.

We do not use LLM graders for this task.

## Data

Task data is derived from the [TDC HIV dataset](https://tdcommons.ai/single_pred_tasks/hts/#hiv) (DTP AIDS Antiviral Screen, 41,127 molecules). Data files are stored on the OpenReward platform.

## Tools

Agents are given a single tool:

- `submit_prediction`: Submit a bioactivity classification (0 = inactive, 1 = active). Returns whether the prediction is correct. The first graded prediction ends the episode; a value other than 0 or 1 is not graded and can be resubmitted.

## Time Horizon

BioClassify is a single-turn environment. The agent receives a molecule's SMILES string and submits one classification. Each task requires one graded tool call.

## Other Environment Requirements

There are no further environment requirements; BioClassify works out of the box with the OpenReward endpoint without any secrets.

## Safety

Agents in BioClassify are asked to classify molecules for bioactivity against HIV replication. The environment does not present direct safety risks, as agents only provide classification predictions with no access to external systems.

However, this is a dual-use domain. Models trained for bioactivity prediction capabilities could potentially be misused for designing harmful compounds in other contexts.

## Citations

```bibtex
@inproceedings{huang2021tdc,
  title     = {Therapeutics Data Commons: Machine Learning Datasets and Tasks for Drug Discovery and Development},
  author    = {Huang, Kexin and Fu, Tianfan and Gao, Wenhao and Zhao, Yue and Roohani, Yusuf and Leskovec, Jure and Coley, Connor W. and Xiao, Cao and Sun, Jimeng and Zitnik, Marinka},
  booktitle = {Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks},
  year      = {2021},
  eprint    = {2102.09548},
  archivePrefix = {arXiv}
}

@article{wu2018moleculenet,
  title   = {MoleculeNet: a benchmark for molecular machine learning},
  author  = {Wu, Zhenqin and Ramsundar, Bharath and Feinberg, Evan N. and Gomes, Joseph and Geniesse, Caleb and Pappu, Aneesh S. and Leswing, Karl and Pande, Vijay},
  journal = {Chemical Science},
  volume  = {9},
  number  = {2},
  pages   = {513--530},
  year    = {2018}
}

@misc{AIDS2004screening,
  title  = {AIDS Antiviral Screen Data},
  author = {{National Cancer Institute (NCI)}},
  note   = {DTP AIDS Antiviral Screen. Available via Therapeutics Data Commons (TDC)},
  url    = {https://wiki.nci.nih.gov/display/NCIDTPdata/AIDS+Antiviral+Screen+Data}
}
```
