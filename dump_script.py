import pandas as pd
df = pd.read_csv(r'c:\Users\maiap\OneDrive\Desktop\Desenvolvimento\Estudo_Atribuicoes_PCSP_2024\05 - Atrib Rest Rem Pericia.CSV', encoding='iso-8859-1', sep=';')
with open(r'c:\Users\maiap\OneDrive\Desktop\Desenvolvimento\Estudo_Atribuicoes_PCSP_2024\cargos.txt', 'w') as f:
    f.write(str(df['Carreira'].tolist() if 'Carreira' in df.columns else df.iloc[:,0].tolist()))
