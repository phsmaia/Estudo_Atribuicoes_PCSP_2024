import pandas as pd
from data_loader import get_all_datasets
import os

d = get_all_datasets()
all_careers = set()
for name, df in d.items():
    if 'Carreira' in df.columns:
        all_careers.update(df['Carreira'].dropna().tolist())
    else:
        all_careers.update(df.index.dropna().tolist())

with open('all_careers.txt', 'w', encoding='utf-8') as f:
    for c in sorted(all_careers):
        f.write(str(c) + '\n')
