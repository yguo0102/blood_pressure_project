import sys
import pandas as pd
import os

infile = sys.argv[1]

with open(infile) as f:
    sections = f.readlines()
    proc_sections = [x.strip() for x in sections if len(x.strip()) > 0]
    pd.DataFrame({'text':proc_sections}).to_csv('sample1_sections.csv')

