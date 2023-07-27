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
load_figure_template("united")

app = dash.Dash(external_stylesheets=[dbc.themes.UNITED])
server = app.server

# DataFrame =================

from globals import *

# Pré-layout ================
card_total_partidas = dbc.Card(
    [
        dbc.CardImg(src="/assets/image_1.png", top=True, style={'max-width':'58px','max-height':'58px', 'padding-left':'20px', 'padding-top':'20px'}),
        dbc.CardBody(
            [
                html.H5("Partidas", className="card-title"),
                html.H2(n_partidas_totais)
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_total_gols = dbc.Card(
    [
        dbc.CardImg(src="/assets/bola_simbolo_card.png", top=True, style={'max-width':'45px','max-height':'45px', 'padding-left':'20px', 'padding-top':'20px'}),
        dbc.CardBody(
            [
                html.H5("Gols", className="card-title"),
                html.H2(n_gols_temporada)
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_lider_atual = dbc.Card(
    [
        dbc.CardImg(src="/assets/Trofeu_1.png", top=True, style={'max-width':'45px','max-height':'45px', 'padding-left':'20px', 'padding-top':'20px'}),
        dbc.CardBody(
            [
                html.H5("1° geral", className="card-title"),
                html.H2(lider_geral)
                
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_n_rodadas = dbc.Card(
    [
        dbc.CardImg(src="/assets/n_rodadas.png", top=True, style={'max-width':'45px','max-height':'45px', 'padding-left':'20px', 'padding-top':'20px'}),
        dbc.CardBody(
            [
                html.H5("N° de rodadas|Liga", className="card-title"),
                html.H2(n_rodadas_liga)
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_n_copas = dbc.Card(
    [
        dbc.CardImg(src="/assets/n_rodadas.png", top=True, style={'max-width':'45px','max-height':'45px', 'padding-left':'20px', 'padding-top':'20px'}),
        dbc.CardBody(
            [
                html.H5("N° de rodadas|Copa", className="card-title"),
                html.H2(n_rodadas_copa)
            ]
        ),
    ],
    style={"width": "18rem"},
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
            dcc.Dropdown(options=lista_criterio, value=lista_criterio[0], id='dpd-02-criterios') 
        ]
    ),
style={'height':'100%'})

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
    {'field': 'VER', 'width': 80},
    {'field': 'FALTA', 'width': 90},
    {'field': 'PTS', 'width': 90},
]


# Layout    =================
app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.Card(card_total_partidas, color="primary", style={"opacity": 0.9}), lg=2),
                dbc.Col(dbc.Card(card_total_gols, color='secondary', style={"opacity": 0.9}), lg=2),
                dbc.Col(dbc.Card(card_lider_atual, color='success', style={"opacity": 0.9}), lg=2),
                dbc.Col(dbc.Card(card_n_rodadas, color='warning', style={"opacity": 0.9}), lg=2),
                dbc.Col(dbc.Card(card_n_copas, color='#64A9DE', style={"opacity": 0.9}), lg=2),
                ], style={'padding-bottom':'20px'}), 
                 
            dbc.Row(dbc.Card(dbc.CardBody([
                dcc.Dropdown(id='dpd-01-rg/c1/r2', 
                            options=[
                                    {'label': 'Ranking Geral', 'value': 'ranking'},
                                    {'label': 'TOP Gols', 'value': 'gol'},
                                    {'label': 'TOP Assistências', 'value': 'assistencia'},
                                    {'label': 'Goleiros', 'value': 'gks'}], value='ranking'),
                dcc.Graph(id='grafico-01-rg/c2/r2', style={'height':'400px'}),
                ]))), 
            dbc.Row(dag.AgGrid(id="ranking-table", rowData=df_table.to_dict("records"), columnDefs=columnDefs, defaultColDef={"resizable": True, "sortable": True}, style={'height':'300px'})), 
                ], lg=6),
        
        dbc.Col([dbc.Card(dbc.CardBody(
                [
                dbc.Row(html.H6('Análise por Rodada'),style={}),
                dbc.Row([dbc.Col(card_c2,lg=2), dbc.Col([dcc.Graph(id='grafico-02-rg-c2-r1-c2')],lg=5), dbc.Col([dcc.Graph(id='grafico-02-rg-c2-r1-c3')], lg=5)]), 
                ])),
                dbc.Row()], lg=6)
    ])
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


#          #grafico gol/ass rodada
@app.callback(
    Output('grafico-02-rg-c2-r1-c3', 'figure'),
    Input('radio-01-liga-copa', 'value'),
    Input('dpd-01-rodada', 'value'),
)
def update_grafico_01_c1(competicao, rodada):
        df_target_rodada = df_season.loc[df_season['COMPETIÇÃO']==competicao]
        df_target_rodada = df_target_rodada.loc[df_target_rodada['RODADA']==rodada]
        df_target_rodada = df_target_rodada.groupby('PLAYER').agg({'GOL':'sum', 'ASS':'sum', 'STG':'sum'})
        df_target_rodada = df_target_rodada.loc[(df_target_rodada['GOL']>0) | (df_target_rodada['ASS']>0)]
        df_target_rodada = df_target_rodada.reset_index()
        
        fig = px.bar(data_frame=df_target_rodada, x='PLAYER', y=['GOL', 'ASS'], barmode='group', title='GOL/ASS')
        fig.update_layout(margin=dict(l=0, r=0, t=30, b=0))
        fig.update_layout(yaxis_title=None)
        fig.update_layout(xaxis_title=None)
        
        return fig
    
# Servidor  =================
if __name__=='__main__':
    app.run_server(debug=True)