#%%
import pandas as pd
import numpy as np

campeonatos = pd.read_csv('./datas/campeonatos_gauchos_tratado.csv', sep=',', 
                            dtype=({'Edicao': np.uint8, 'Ano' : np.uint16, 'Artilheiro' : object, 
                            'Primeiro' : 'category' , 'Segundo' : 'category', 'Terceiro' : 'category', 
                            'Quarto' : 'category', 'Cidade_Primeiro' : 'category' , 
                            'Cidade_Segundo' : 'category', 'Cidade_Terceiro' : 'category', 
                            'Cidade_Quarto' : 'category', 'N_de_gols' : 'Int8'}))
times = pd.read_csv('./datas/times_gauchos_tratado.csv', sep=',', 
                    dtype = ({'Apelido': 'category', 'Nome' : 'category', 'Cidade': 'category'}))
cidades = pd.read_csv('./datas/cidades_gauchas_tratado.csv', dtype=({'Cidade' : 'category', 'Microrregioes' : 'category',
                                                                'Mesorregioes' : 'category'}))

#%%

multiverso_campeonatos = campeonatos[['Edicao', 'Ano', 'Primeiro', 'Segundo', 'Terceiro', 'Quarto']]

cols = ['Primeiro', 'Segundo', 'Terceiro', 'Quarto']

multiverso_campeonatos[cols] = multiverso_campeonatos[cols].replace({'Internacional' : 'extinto', 'Grêmio' : 'extinto'})

#%%

for posicoes in cols:
    index = cols.index(posicoes)
    if index < 3:
        name = cols[index + 1] 
        multiverso_campeonatos[posicoes] = multiverso_campeonatos.apply(lambda x: x[name] if x[posicoes] == 'extinto' else x, axis = 1)[posicoes]
#%%

#%timeit
#start = time.time()
for index,rows in multiverso_campeonatos.iterrows():
  #for i in rows: 
  if(multiverso_campeonatos.iloc[index,2] == 'extinto'):
    multiverso_campeonatos.iloc[index,2] = multiverso_campeonatos.iloc[index,3]
    multiverso_campeonatos.iloc[index,3] = multiverso_campeonatos.iloc[index,4]
    multiverso_campeonatos.iloc[index,4] = multiverso_campeonatos.iloc[index,5]
    multiverso_campeonatos.iloc[index,5] = None
    if(multiverso_campeonatos.iloc[index,2] == 'extinto'):
      multiverso_campeonatos.iloc[index,2] = multiverso_campeonatos.iloc[index,3]
      multiverso_campeonatos.iloc[index,3] = multiverso_campeonatos.iloc[index,4]
      multiverso_campeonatos.iloc[index,4] = multiverso_campeonatos.iloc[index,5]
      multiverso_campeonatos.iloc[index,5] = None
  if(multiverso_campeonatos.iloc[index,3] == 'extinto'):
    multiverso_campeonatos.iloc[index,3] = multiverso_campeonatos.iloc[index,4]
    multiverso_campeonatos.iloc[index,4] = multiverso_campeonatos.iloc[index,5]
    multiverso_campeonatos.iloc[index,5] = None
    if(multiverso_campeonatos.iloc[index,3] == 'extinto'):
      multiverso_campeonatos.iloc[index,3] = multiverso_campeonatos.iloc[index,4]
      multiverso_campeonatos.iloc[index,4] = multiverso_campeonatos.iloc[index,5]
      multiverso_campeonatos.iloc[index,5] = None
  if(multiverso_campeonatos.iloc[index,4] == 'extinto'):
    multiverso_campeonatos.iloc[index,4] = multiverso_campeonatos.iloc[index,5]
    multiverso_campeonatos.iloc[index,5] = None
    if(multiverso_campeonatos.iloc[index,4] == 'extinto'):
      multiverso_campeonatos.iloc[index,4] = multiverso_campeonatos.iloc[index,5]
      multiverso_campeonatos.iloc[index,5] = None
  if(multiverso_campeonatos.iloc[index,5] == 'extinto'):
    multiverso_campeonatos.iloc[index,5] = None


multiverso_campeonatos = multiverso_campeonatos.\
    merge(times, how='left', left_on='Primeiro', right_on = "Apelido").drop(columns=['Apelido', 'Nome', 'Fundacao']).rename(columns={"Cidade": "Cidade_Primeiro"}) .\
    merge(times, how='left', left_on='Segundo', right_on = "Apelido").drop(columns=['Apelido', 'Nome', 'Fundacao']).rename(columns={"Cidade": "Cidade_Segundo"}) .\
    merge(times, how='left', left_on='Terceiro', right_on = "Apelido").drop(columns=['Apelido', 'Nome', 'Fundacao']).rename(columns={"Cidade": "Cidade_Terceiro"}) .\
    merge(times, how='left', left_on='Quarto', right_on = "Apelido").drop(columns=['Apelido', 'Nome', 'Fundacao']).rename(columns={"Cidade": "Cidade_Quarto"})


multiverso_campeonatos.drop_duplicates(subset=['Ano'], inplace=True)
# %%
