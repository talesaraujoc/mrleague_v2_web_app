import pandas as pd

df = pd.read_excel('data/testedatasetv2b.xlsx')
df_copas = pd.read_excel('data/copas_mr.xlsx')
df_season = pd.concat([df, df_copas])

df.fillna(0, inplace=True)
df_copas.fillna(0, inplace=True)
df_season.fillna(0, inplace=True)

df_corrida_geral = df_season.groupby('PLAYER').agg({'PTS':'sum', 'GOL':'sum', 'ASS':'sum'})
df_corrida_geral = df_corrida_geral.sort_values(by='PTS', ascending=False)
df_corrida_geral = df_corrida_geral.reset_index()
lider_geral = df_corrida_geral.iloc[0]['PLAYER']

#table
df_table = df_season.groupby('PLAYER').agg({'V':'sum', 'E':'sum', 'D':'sum', 'GOL':'sum', 'ASS':'sum', 'STG':'sum','AMA':'sum', 'AZUL':'sum', 'VER':'sum','FALTA':'sum', 'PTS':'sum'})
df_table = df_table.sort_values(by='PTS', ascending=False)
df_table = df_table.reset_index()
df_table['POSITION'] = df_table.index.values + 1

#algumas variáveis
lista_partidas = df['PARTIDA'].to_list()
lista_partidas_copas = df_copas['PARTIDA'].to_list()
n_partidas_totais = lista_partidas[-1] + lista_partidas_copas[-1]
n_rodadas_liga = df['RODADA'].unique()[-1]
n_rodadas_copa = df_copas['RODADA'].unique()[-1]

df_top_cinco_artilheiros = df_corrida_geral.sort_values(by='GOL', ascending=False)  
df_top_cinco_artilheiros = df_top_cinco_artilheiros.reset_index()
df_top_cinco_artilheiros = df_top_cinco_artilheiros.drop('index', axis=1)
df_top_cinco_artilheiros = df_top_cinco_artilheiros.iloc[0:5]

df_top_cinco_assistencia = df_corrida_geral.sort_values(by='ASS', ascending=False)  
df_top_cinco_assistencia = df_top_cinco_assistencia.reset_index()
df_top_cinco_assistencia = df_top_cinco_assistencia.drop('index', axis=1)
df_top_cinco_assistencia = df_top_cinco_assistencia.iloc[0:5]

n_gols_temporada = df_season['GOL'].sum()

df_gk = df_season.loc[df_season['POSIÇÃO']=='GK']
df_gk = df_gk.loc[df_gk['PLAYER']!='GK sub']
df_gk = df_gk.loc[df_gk['PLAYER']!='Carlos GK']
df_gk = df_gk.loc[df_gk['PLAYER']!='Victor GK']
df_goleiros_gs = df_gk.groupby('PLAYER').agg({'STG':'mean','GS':'mean','DD':'mean'})
df_goleiros_gs = df_goleiros_gs.sort_values(by='GS', ascending=True)
df_goleiros_gs = df_goleiros_gs.reset_index()

df_liga = pd.read_excel('data/testedatasetv2b.xlsx')
df_copa = pd.read_excel('data/copas_mr.xlsx')
df_season = pd.concat([df_liga, df_copa])

df_liga.fillna(0, inplace=True)
df_copa.fillna(0, inplace=True)  

competicoes = df_season['COMPETIÇÃO'].unique()
lista_rodadas_liga = df_liga['RODADA'].unique()
lista_rodadas_copa = df_copa['RODADA'].unique()

rodadas_liga = lista_rodadas_liga.tolist()
rodadas_copa = lista_rodadas_copa.tolist()
len_liga = len(rodadas_liga)
len_rodada = len(rodadas_copa)
total_rodadas_season = len_liga + len_rodada

lista_criterio = ['GOL','ASS','STG', 'GC', 'AMA', 'AZUL', 'VER', 'PP', 'FALTA', 'PTS']

# lista players

lista_players = df_season['PLAYER'].unique()