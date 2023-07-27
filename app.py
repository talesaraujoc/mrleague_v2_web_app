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
card_faturamento = dbc.Card([
        #dbc.CardImg(src="/assets/money_up.png", top=True, style={'max-width':'58px','max-height':'58px', 'padding-left':'20px', 'padding-top':'20px'}),
        
        dbc.CardBody([
                html.H4("Faturamento", className="card-title"),
            ]),
    ],
    style={"width": "90%", 'height':'100%'})


# Layout    =================
app.layout = html.Div([
    
])



# Callbacks =================


# Servidor  =================
if __name__=='__main__':
    app.run_server(debug=True)