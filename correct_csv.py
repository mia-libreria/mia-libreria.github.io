import pandas as pd


df = pd.read_csv('library_old.csv')

df.drop(columns=['Unnamed: 0.3','Unnamed: 0.2', 'Unnamed: 0.1' ,'Unnamed: 0'], inplace=True)

df['AUTORE2'] = df['AUTORE'] + ' ' + df['Unnamed: 2']

df.drop(columns=['AUTORE', 'Unnamed: 2'], inplace=True)
df.rename({'AUTORE2': 'AUTORE'}, inplace=True)

df.to_csv('library2.csv')