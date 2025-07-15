# NLP System for Blood Pressure and Biological Sex Analysis

This repository contains the implementation of the NLP system described in the study:  
**"Leveraging Few-Shot Learning and Large Language Models for Analyzing Blood Pressure Variations Across Biological Sex from Scientific Literature."**

## 📂 File Descriptions

### `data_process/` — Data Downloading and Preprocessing
| Filename                         | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `PMC data.ipynb`                 | Decompresses the data downloaded from PMC and extracts manuscript text.    |
| `Prepare dataset.ipynb`         | Performs a 5-fold split and converts the data to BIO format for NER tasks. |

### `LLM/` — Model Inference and Post-processing
| Filename                         | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `run_azure_openai_api.py`       | Runs model inference using the Azure-hosted OpenAI API.                     |
| `post_process.py`               | Parses LLM responses to extract variables and filters out invalid entries.  |
| `Evaluate ner.ipynb`            | Evaluates model performance using standard NER metrics.                     |

## ⚙️ Environment Setup

The code was developed using **Python 3.9** and tested to work with **Python 3.6** and **3.8**.

Before using the Microsoft Azure OpenAI API, set the following environment variable with your API key:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## ▶️ Example Usage
To run inference with the LLM:

```bash
python LLM/run_azure_openai_api.py datasets/train.csv datasets/train_output.csv
```
To post-process the LLM output:
```bash
python LLM/run_azure_openai_api.py datasets/train_output.csv datasets/train_output_processed.xlsx
```
To evaluate the model’s performance, open and run the Jupyter notebook `LLM/Evaluate ner.ipynb`.


## 📖 Citation

If you use this code or dataset in your work, please cite our study:

> Guo, Y., *et al.* (2025). *Leveraging Few-Shot Learning and Large Language Models for Analyzing Blood Pressure Variations Across Biological Sex from Scientific Literature*. Computers in Biology and Medicine, [TBD], pages.[TBD] https://doi.org/10.xxxx/xxxxxx

### BibTeX
```bibtex
@article{guo2025bloodpressurellm,
  title={Leveraging Few-Shot Learning and Large Language Models for Analyzing Blood Pressure Variations Across Biological Sex from Scientific Literature},
  author={Guo, Yuting and others},
  journal={Computers in Biology and Medicine},
  year={2025},
  doi={10.XXXX/XXXXXXX}
}
```

