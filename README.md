This repository contains the implementation of the NLP system in the study "Leveraging Few-Shot Learning and Large Language Models for Analyzing Blood Pressure Variations Across Biological Sex from Scientific Literature".

# File Description

The `data_process` folder contains the python scripts related to data downloading and preprocessing.
| Filename                    | Description                                                                       |
|-----------------------------|-----------------------------------------------------------------------------------|
| data_process/PMC data.ipynb | Decompress the data downloaded from PMC and extract the manuscript text |
| data_process/Prepare dataset.ipynb    | Perform 5-fold split and convert the data to the BIO format  	  |

The `LLM` folder contains the Python scripts related to model inference and post-processing of the LLM answers.
| Filename                    | Description                                                                       |
|-----------------------------|-----------------------------------------------------------------------------------|
| LLM/run_azure_openai_api.py | Run model inference using the LLM API supported by Microsoft Azure OpenAI. |
| LLM/post_process.py   	  | Parse the LLM's answers to extract the varibales and filter out the invalid values.  	  |
| LLM/Evaluate ner.ipynb      | Evaluate the model performance using NER metrics. |