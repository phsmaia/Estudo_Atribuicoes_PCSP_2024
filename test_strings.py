import pandas as pd
from data_loader import get_all_datasets
d = get_all_datasets()
print('LONPC Sem Correcao:')
if 'Carreira' in d['lonpc_sem_correcao'].columns: print(d['lonpc_sem_correcao']['Carreira'].tolist())
print('\nReestruturacao:')
if 'Carreira' in d['reestruturacao'].columns: print(d['reestruturacao']['Carreira'].tolist())
print('\nAtual Com Correcao:')
if 'Carreira' in d['atual_com_correcao'].columns: print(d['atual_com_correcao']['Carreira'].tolist())
