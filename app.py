from dash import dash, html, dcc, Output, Input, dash_table
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template


import plotly as plt
from datetime import date
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_ag_grid as dag


# Servidor
load_figure_template("yeti")

app = dash.Dash(external_stylesheets=[dbc.themes.YETI])
server = app.server

# DataFrame =================

from globals import *

# Pré-layout ================
card_total_partidas = dbc.Card(
    [
        dbc.CardImg(src="/assets/image_1.png", top=True, style={'max-width':'58px','max-height':'58px', 'padding-left':'20px', 'padding-top':'20px'}),
        dbc.CardBody(
            [
                html.H6("Partidas", className="card-title"),
                html.H6(n_partidas_totais)
            ]
        ),
    ],
    
)

card_total_gols = dbc.Card(
    [
        dbc.CardImg(src="/assets/bola_simbolo_card.png", top=True, style={'max-width':'45px','max-height':'45px', 'padding-left':'20px', 'padding-top':'20px'}),
        dbc.CardBody(
            [
                html.H6("Gols", className="card-title"),
                html.H6(n_gols_temporada)
            ]
        ),
    ],
    
)

card_lider_atual = dbc.Card(
    [
        dbc.CardImg(src="/assets/Trofeu_1.png", top=True, style={'max-width':'45px','max-height':'45px', 'padding-left':'20px', 'padding-top':'20px'}),
        dbc.CardBody(
            [
                html.H6("1° geral", className="card-title"),
                html.H6(lider_geral)
                
            ]
        ),
    ],
    
)

card_n_rodadas = dbc.Card(
    [
        dbc.CardImg(src="/assets/n_rodadas.png", top=True, style={'max-width':'45px','max-height':'45px', 'padding-left':'20px', 'padding-top':'20px'}),
        dbc.CardBody(
            [
                html.H6("Rodadas|Liga", className="card-title"),
                html.H6(n_rodadas_liga)
            ]
        ),
    ],
    
)

card_n_copas = dbc.Card(
    [
        dbc.CardImg(src="/assets/n_rodadas.png", top=True, style={'max-width':'45px','max-height':'45px', 'padding-left':'20px', 'padding-top':'20px'}),
        dbc.CardBody(
            [
                html.H6("Copas", className="card-title"),
                html.H6(n_rodadas_copa)
            ]
        ),
    ],
    
)

card_c2 = dbc.Card(
    dbc.CardBody(
        [
            dbc.RadioItems(options=competicoes, value=competicoes[0], id='radio-01-liga-copa', inline=True, style={}),
            
            html.Hr(),
            
            html.H6('Rodada:', style={}),
            dcc.Dropdown(id='dpd-01-rodada'),
            
            html.Hr(),
            
            html.H6('Critério:', style={}),
            dcc.Dropdown(options=lista_criterio, value=lista_criterio[-1], id='dpd-02-criterios') 
        ]
    ),
style={'height':'100%'})

card_position = dbc.Card(
    [
        dbc.CardBody(
            [

                html.H6(id='disparador-posicao')
            ]
        ),
    ],
    
style={'width':'70%'})

card_n_rodadas_individual = dbc.Card(
    [
        dbc.CardBody(
            [

                html.H6(id='disparador-rodadas')
            ]
        ),
    ],
    
style={'width':'70%'})

columnDefs = [
    {'field': 'PLAYER', 'width': 120, 'autosize': True},
    {'field': 'V', 'width': 60},
    {'field': 'E', 'width': 60},
    {'field': 'D', 'width': 60},
    {'field': 'GOL', 'width': 80},
    {'field': 'ASS', 'width': 80},
    {'field': 'STG', 'width': 80},
    {'field': 'AMA', 'width': 80},
    {'field': 'AZUL', 'width': 80},
    {'field': 'VER', 'width': 75},
    {'field': 'FALTA', 'width': 76},
    {'field': 'PTS', 'width': 90},
]


# Layout    =================
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(html.Img(),lg=2),
                dbc.Col(dbc.Card(card_total_partidas, color="primary", style={"opacity": 0.9}), lg=2),
                dbc.Col(dbc.Card(card_total_gols, color='secondary', style={"opacity": 0.9}), lg=2),
                dbc.Col(dbc.Card(card_lider_atual, color='success', style={"opacity": 0.9}), lg=2),
                dbc.Col(dbc.Card(card_n_rodadas, color='warning', style={"opacity": 0.9}), lg=2),
                dbc.Col(dbc.Card(card_n_copas, color='#64A9DE', style={"opacity": 0.9}), lg=2)
                ], style={'padding-bottom':'20px'}, className='main_row g-2 my-auto'), 
                 
            dbc.Row(dbc.Card(dbc.CardBody([
                dcc.Dropdown(id='dpd-01-rg/c1/r2', 
                            options=[
                                    {'label': 'Ranking Geral', 'value': 'ranking'},
                                    {'label': 'TOP Gols', 'value': 'gol'},
                                    {'label': 'TOP Assistências', 'value': 'assistencia'},
                                    {'label': 'Goleiros', 'value': 'gks'}], value='ranking'),
                dcc.Graph(id='grafico-01-rg/c2/r2', style={'height':'400px'}),
                ])), style={'margin-right':'10px', 'margin-left':'10px'}), 
            dbc.Row(dag.AgGrid(id="ranking-table", rowData=df_table.to_dict("records"), columnDefs=columnDefs, defaultColDef={"resizable": True, "sortable": True}, style={'height':'300px','margin-left':'10px', 'margin-top':'10px', 'padding-right':'20px'})), 
                ], lg=6),
        
        
        dbc.Col([
            dbc.Row(dbc.Card(dbc.CardBody(dbc.Row([dbc.Col(card_c2,lg=2), dbc.Col(dcc.Graph(id='grafico-02-rg-c2-r1-c2'),lg=5), dbc.Col(dcc.Graph(id='grafico-02-rg-c2-r1-c3'), lg=5)]))),className='main_row g-2 my-auto'), 
            dbc.Row(dbc.Card(dbc.CardBody(dbc.Row([
                dbc.Col([dbc.Row([dcc.Dropdown(options=lista_players, value='Lotta',id='identificador-player', style={'width':'95%', 'font-size':'85%'}), html.Div(id='disparador-imagem', style={'width':'90%'})]), 
                         dbc.Row([html.H6('Posição Geral', style={'margin-top':'20px', 'font-size':'85%'}), dbc.Card(card_position)], align='center'),
                         dbc.Row([html.H6('Rodadas', style={'margin-top':'8px', 'font-size':'85%'}), dbc.Card(card_n_rodadas_individual)], align='center')], 
                    lg=2),
                dbc.Col([dbc.Row([dbc.Col([dcc.Graph(id='pizza_01')], lg=4), dbc.Col([dcc.Graph(id='pizza_02')], lg=4), dbc.Col([dcc.Graph(id='pizza_03')], lg=4)]),
                         dbc.Row(dcc.Graph(id='grafico-linha-evolucao', style={'height':'300px'}))], 
                    lg=10)
            ]))), className='main_row g-2 my-auto')
            ] ,lg=6)
    ], className='main_row g-2 my-auto')
])


# Callbacks =================
@app.callback(
    Output('grafico-01-rg/c2/r2', 'figure'),
    [Input('dpd-01-rg/c1/r2', 'value')]
)
def update_grafico_um(criterio):
    if criterio == 'ranking':
        fig_corrida_geral = px.bar(df_corrida_geral, x='PLAYER', y='PTS', title='PONTUAÇÃO GERAL', text_auto='.2s')
        return fig_corrida_geral
    elif criterio == 'gol':
        fig_top_cinco_artilheiros = px.bar(df_top_cinco_artilheiros, x='PLAYER', y='GOL', title='TOP 5 - ARTILHEIRO')
        return fig_top_cinco_artilheiros
    elif criterio == 'assistencia':
        fig_top_cinco_ass = px.bar(df_top_cinco_assistencia, x='PLAYER', y='ASS', title='TOP 5 - ASSISTS')
        return fig_top_cinco_ass
    else:
        fig_gks = px.bar(df_goleiros_gs, x='PLAYER', y=['GS','STG', 'DD'], barmode="group", title='GKs - GS / STG / DDs')
        return fig_gks
    
    
#            #disparador dropdown
@app.callback(
    Output('dpd-01-rodada', 'options'),
    Input('radio-01-liga-copa', 'value')
)
def update_drop_um(selection):
    if selection == 'LIGA':
        return lista_rodadas_liga
    else:
        return lista_rodadas_copa


@app.callback(
    Output('dpd-01-rodada', 'value'),
    Input('dpd-01-rodada', 'options')
)
def set_rodada(available_options):
    return available_options[0]


#            #grafico rodada
@app.callback(
    Output('grafico-02-rg-c2-r1-c2', 'figure'),
    Input('radio-01-liga-copa', 'value'),
    Input('dpd-01-rodada', 'value'),
)
def update_grafico_01_c1(competicao, rodada):
        df_target = df_season.loc[df_season['COMPETIÇÃO']==competicao]
        df_target = df_target.loc[df_target['RODADA']==rodada]
        df_target = df_target.groupby('TIME').agg({'V':'sum', 'E':'sum', 'D':'sum'})/6
        df_target = df_target.reset_index()
        
        fig = make_subplots(rows=1, cols=1, subplot_titles=('V/E/D', 'PTS'))
        
        fig.add_trace(go.Bar(x=df_target['TIME'], y=df_target['V'], marker=dict(color='#3ADE3E'), name='Vitórias', showlegend=False), row=1, col=1)
        fig.add_trace(go.Bar(x=df_target['TIME'], y=df_target['E'], marker=dict(color='#EAE5B4'), name='Empates', showlegend=False), row=1, col=1)
        fig.add_trace(go.Bar(x=df_target['TIME'], y=df_target['D'], marker=dict(color='#F52D2A'), name='Derrotas', showlegend=False), row=1, col=1)
        fig.update_layout(yaxis_title=None)
        fig.update_layout(xaxis_title=None)
        fig.update_layout(margin=dict(l=0, r=0, t=20, b=0))
        return fig


#          #grafico criterios rodada
@app.callback(
    Output('grafico-02-rg-c2-r1-c3', 'figure'),
    Input('radio-01-liga-copa', 'value'),
    Input('dpd-01-rodada', 'value'),
    Input('dpd-02-criterios', 'value')
)
def update_grafico_01_c1(competicao, rodada, criterio):
        if criterio == 'GOL' or criterio=='ASS':
            df_target_rodada = df_season.loc[df_season['COMPETIÇÃO']==competicao]
            df_target_rodada = df_target_rodada.loc[df_target_rodada['RODADA']==rodada]
            df_target_rodada = df_target_rodada.groupby('PLAYER').agg({criterio:'sum'})
            df_target_rodada = df_target_rodada.loc[(df_target_rodada[criterio]>0)]
            df_target_rodada = df_target_rodada.reset_index()
            
            fig = px.bar(data_frame=df_target_rodada, x='PLAYER', y=criterio, barmode='group', title=criterio)
            fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
            fig.update_layout(yaxis_title=None)
            fig.update_layout(xaxis_title=None)
            
            return fig
        else:
            df_target_rodada = df_season.loc[df_season['COMPETIÇÃO']==competicao]
            df_target_rodada = df_target_rodada.loc[df_target_rodada['RODADA']==rodada]
            df_target_rodada = df_target_rodada.groupby('PLAYER').agg({criterio:'sum'})
            df_target_rodada = df_target_rodada.reset_index()
            
            fig = px.bar(data_frame=df_target_rodada, x='PLAYER', y=criterio, barmode='group', title=criterio)
            fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
            fig.update_layout(yaxis_title=None)
            fig.update_layout(xaxis_title=None)
            
            return fig
    

#          #disparador imagem
@app.callback(
    Output('disparador-imagem', 'children'),
    Input('identificador-player', 'value')
)
def update_image(nome):
    children = html.Img(src=f"/assets/{nome}.png", style={'height':'150px'})
    return children


#          #disparador posição
@app.callback(
    Output('disparador-posicao', 'children'),
    Input('identificador-player', 'value')
)
def update_posicao(player):
    position = df_table.loc[df_table['PLAYER']==player]['POSITION'].values[0]
    position = str(position)+"°"
    return position


@app.callback(
    Output('disparador-rodadas', 'children'),
    Input('identificador-player', 'value')
)
def update_n_rodadas(player):
    df_contador_liga = df.loc[df['PLAYER']==player]
    df_contador_liga = df_contador_liga.groupby(['PLAYER', 'RODADA']).agg({'PARTIDA':'count'})
    df_contador_liga = df_contador_liga.reset_index()
    
    df_contador_copa = df_copas.loc[df_copas['PLAYER']==player]
    df_contador_copa = df_contador_copa.groupby(['PLAYER', 'RODADA']).agg({'PARTIDA':'count'})
    df_contador_copa = df_contador_copa.reset_index()
    
    target = df_contador_liga['RODADA'].count() + df_contador_copa['RODADA'].count()
    taxa_presenca = target / total_rodadas_season
    taxa_presenca = round(taxa_presenca*100)
    
    
    retorno = str(target) + '  ' + '(' + str(taxa_presenca) + '%' +')'
    
    return retorno


#         #grafico pizza individual gol
@app.callback(
    Output('pizza_01', 'figure'),
    Input('identificador-player', 'value')
)
def update_pizza_individual(player):
    gols_player_selected = df_season[df_season['PLAYER']==player]
    gols_player_selected = gols_player_selected['GOL'].sum()
    
    gols_rest = df_season[df_season['PLAYER']!=player]
    gols_rest = gols_rest.groupby('PLAYER').agg({'GOL':'sum'}).mean()
    gols_rest = round(gols_rest[0])

    data = {'PLAYER': [player, 'Média Gols Competição'], 'GOLS': [gols_player_selected, gols_rest]}
    dff = pd.DataFrame(data)
    
    fig = go.Figure(data=[go.Pie(labels=dff['PLAYER'], values=dff['GOLS'], hole=.7, pull=[0.04, 0], textinfo='value', showlegend=False)])
    
    fig.update_layout(title_text="Gols", width=175,height=175, margin=dict(l=0,r=0,b=0,t=40), annotations=[dict(text=gols_player_selected, font_size=26, showarrow=False)])

    return fig


#      #grafico pizza vitorias
@app.callback(
    Output('pizza_02', 'figure'),
    Input('identificador-player', 'value')
)
def update_pizza_individual(player):
    vitorias_selected_player = df_season[df_season['PLAYER']==player]
    vitorias_selected_player = vitorias_selected_player['V'].sum()
    
    vitorias_rest = df_season[df_season['PLAYER']!=player]
    vitorias_rest = vitorias_rest.groupby('PLAYER').agg({'V':'sum'}).mean()
    vitorias_rest = round(vitorias_rest[0])

    data = {'PLAYER': [player, 'Média Vitórias Competição'], 'V': [vitorias_selected_player, vitorias_rest]}
    dff = pd.DataFrame(data)
    
    fig = go.Figure(data=[go.Pie(labels=dff['PLAYER'], values=dff['V'], hole=.7, pull=[0.04, 0], textinfo='value', showlegend=False)])
    
    
    fig.update_layout(title_text="Vitórias", width=175,height=175, margin=dict(l=0,r=0,b=0,t=40), annotations=[dict(text=vitorias_selected_player, font_size=26, showarrow=False)])

    return fig

#     #grafico pizza derrotas
@app.callback(
    Output('pizza_03', 'figure'),
    Input('identificador-player', 'value')
)
def update_pizza_individual(player):
    derrotas_player_selected = df_season[df_season['PLAYER']==player]
    derrotas_player_selected = derrotas_player_selected['D'].sum()
    
    derrotas_rest = df_season[df_season['PLAYER']!=player]
    derrotas_rest = derrotas_rest.groupby('PLAYER').agg({'D':'sum'}).mean()
    derrotas_rest = round(derrotas_rest[0])

    data = {'PLAYER': [player, 'Média Derrotas Competição'], 'D': [derrotas_player_selected, derrotas_rest]}
    dff = pd.DataFrame(data)
    
    fig = go.Figure(data=[go.Pie(labels=dff['PLAYER'], values=dff['D'], hole=.7, pull=[0.04, 0], textinfo='value', showlegend=False)])
    
    
    fig.update_layout(title_text="Derrotas", width=175,height=175, margin=dict(l=0,r=0,b=0,t=40), annotations=[dict(text=derrotas_player_selected, font_size=26, showarrow=False)])

    return fig

#      #grafico linha pontuacao individual
@app.callback(
    Output('grafico-linha-evolucao', 'figure'),
    Input('identificador-player', 'value')
)
def update_grafico_perfomance(player):
    df_player_select = df_season.loc[df_season['PLAYER']==player]
    df_player_select = df_player_select.groupby('RODADA').agg({'PTS':'sum'})
    df_player_select = df_player_select.reset_index()
    
    fig = px.line(df_player_select, x='RODADA', y='PTS')
    fig.update_layout(yaxis_title=None)
    
    return fig


# Servidor  =================
if __name__=='__main__':
    app.run_server(debug=True)