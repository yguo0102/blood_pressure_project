This folder contains the Python scripts used in the blood pressure study written by Yuting Guo.

# File Description

The `data_process` folder contains the python scripts related to data downloading and preprocessing.
| Filename                    | Description                                                                       |
|-----------------------------|-----------------------------------------------------------------------------------|
| data_process/NCDRISC data download.ipynb | Automatically download the datasets from https://ncdrisc.org/data-downloads.html. |
| data_process/NCDRISC data check.ipynb    | Check whether the zip files contains all the country-specific csv files.  	  |
| data_process/Parse AHA papers.ipynb      | Get the plain text splitted by sections from [ahajournals.org](https://www.ahajournals.org/). |
| data_process/Parse Lancet papers.ipynb   | Get the plain text splitted by sections from [https://www.thelancet.com/](https://www.thelancet.com/). |
| data_process/split_data.py               | Split a large csv file into smaller csv files. |
| data_process/parse_ner.py     	   | TBD |

The `LLM` folder contains the Python scripts related to doing prediction/inference by LLM and processing the LLM's answers.
| Filename                    | Description                                                                       |
|-----------------------------|-----------------------------------------------------------------------------------|
| LLM/run_predict.py  			   | Run predcition using the LLM via Azure OpenAI API. |
| LLM/parse_abstract_response.py   	   | Parse the LLM's answers into a table.  	  |

The `deidentification` folder contains Python scripts related to deidentifying the clinical notes.
| Filename                    | Description                                                                       |
|-----------------------------|-----------------------------------------------------------------------------------|
| deidentification/deid_transformers.py  	| TBD |
