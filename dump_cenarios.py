import pandas as pd
from data_loader import get_all_datasets

d = get_all_datasets()
output = []
for name, df in d.items():
    output.append(f"=== {name} ===")
    if 'Carreira' in df.columns:
        c_list = df['Carreira'].dropna().tolist()
    else:
        c_list = df.index.dropna().tolist()
    for c in sorted(c_list):
        output.append(str(c))
    output.append("\n")

with open('dump.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(output))
