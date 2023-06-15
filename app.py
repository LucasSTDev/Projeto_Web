from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plootly.graph_objects as go
import pandas as pd

# Importar das páginas para mudar o tema
from dash_bootstrap_templates import ThemeSwitchAIO
import dash

# Instanciar o font awesome para utilizar os icons como fonte externa e o servidor
FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]
app = dash.Dash(__name__, external_stylesheets=FONT_AWESOME)
app.scripts.config.serve_locally = True
server = app.server

# Estilos
"""Todos os cards irão ocupar 100% da coluna"""
tab_card = {'height':'100%'}

"""Configurar os gráficos"""
main_config = {
    "hovermode":"x unified",
    "legend": {"yanchor":"top",
               "y":0.9,
               "xanchor":"left",
               "x":0.1,
               "title":{"text":None},
               "font":{"color":"white"},
               "bgcolor":"rbga(0,0,0,0.5)"},
    "margin":{"l":10,"r":10,"t":10,"b":10}    
    }

"""Desabilitando configuracoes dos botoes do plotly para ficar menos poluido """
config_graph = {"displayModebar":False,"showTips":False}

template_theme1 = "flatly"
template_theme2 = "darklY"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY

# Ler e limpar o data frame
df = pd.read_csv('dataset_asimov.csv')
df_cru = df.copy()

# Meses em numeros para ocupar menos memoria
df.loc[ df['Mês'] == 'Jan', 'Mês'] = 1
df.loc[ df['Mês'] == 'Fev', 'Mês'] = 2
df.loc[ df['Mês'] == 'Mar', 'Mês'] = 3
df.loc[ df['Mês'] == 'Abr', 'Mês'] = 4
df.loc[ df['Mês'] == 'Mai', 'Mês'] = 5
df.loc[ df['Mês'] == 'Jun', 'Mês'] = 6
df.loc[ df['Mês'] == 'Jul', 'Mês'] = 7
df.loc[ df['Mês'] == 'Ago', 'Mês'] = 8
df.loc[ df['Mês'] == 'Set', 'Mês'] = 9
df.loc[ df['Mês'] == 'Out', 'Mês'] = 10
df.loc[ df['Mês'] == 'Nov', 'Mês'] = 11
df.loc[ df['Mês'] == 'Dez', 'Mês'] = 12

# Tratando outros dados
df['Valor Pago'] = df['Valor Pago'].str.lstrip('R$ ')
df.loc[df['Status de Pagamento'] == 'Pago', 'Status de pagamento'] = 1
df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de pagamento'] = 0

# Transformnado o max de dados em int
df ['Chamadas Realizdas'] = df['Chamadas Realizdas'].astype(int)
df['Dia'] = df['Dia'].astype(int)
df['Mês'] = df['Mês'].astype(int)
df['Valor Pago'] = df['Valor Pago'].astype(int)
df['Status de Pagamento'] = df['Status de Pagamento'].astype(int)

# Criando opcaos pros filtros
options_moth = [{'label':'Ano Todo','value':0}]

"""Ordenar a lista de meses por valores"""
for i,j in zip(df_cru['Mês'].unique(), df['Mês'].unique()):
    options_moth.append({'label':i,'value':j})
options_moth = sorted(options_moth, key=lambda x: x['value'])

options_team = [{'label':'Todas Equipes', 'value':0}]
for i in df['equipe'].unique():
    options_team.append({'label':i, 'value':i })
    
    
# Layout
app.layout = dbc.Container(children=[
    # Linha 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Vendas Analizdas")
                        ], sm=8),
                        dbc.Col([
                            html.I(className='fa fa-balance-scale',style={'font-size':'300%'})
                        ], sm=4, align='center')
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme",themes=[url_theme1,url_theme2]),
                            html.Legend("Projeto Guiado")
                        ])
                    ],style={'margin-top':'10px'}),
                    dbc.Row([
                        dbc.Button("Visite o Site", href="https://asimov.academy",target="blank")
                    ], style={'margin-top':'10px'})
                ])
            ],style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend("Top Consultores por Equipe")
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o Mês'),
                            dbc.RadioItems(
                                id="radio-month",
                                options=options_moth,
                                value=0,
                                inline=True,
                                label_checked_class_name="text-sucess",
                                input_checked_class_name="border border-sucess bg-sucess",
                            ),
                            html.Div(id='moth-select',style={'text-align':'center','margin-top':'10px'})
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], class_name='g-2 my-auto',style={'margin-top':'7px'}),
    
    # Linha 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.card([
                        dbc.CardBody([
                            dcc.Graph(id='graph3',class_name='dbc',config=config_graph)
                        ])
                    ],style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph4',className='dbc',config=config_graph)
                        ])
                    ],style=tab_card)
                ])
            ],class_name='g-2 my auto', style={'margin-top':'7px'})  
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph5',className='dbc',config=config_graph)
                        ])
                    ],style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph6',className='dbc',config=config_graph)
                        ])
                    ],style=tab_card)
                ], sm=6)
            ], class_name='g-2'),
            dbc.Row([
                dbc.Col([
                   dbc.Card([
                       dcc.Graph(id='graph7',className='dbc',config=config_graph)
                   ],style=tab_card) 
                ])
            ],class_name='g-2 my-auto', style={'margin-top':'7px'})
        ], sm=12, lg=4),
        dbc.Col([
                dbc.Card([
                    dcc.Graph(id='graph8',className='dbc',config=config_graph)
                   ], style=tab_card) 
                ], sm=12, lg=3)
            ], class_name='g-2 my-auto', style={'margin-top':'7px'}),
    
    # Linha 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Distribuição de Propaganda'),
                    dcc.Graph(id='graph9',className='dbc',config=config_graph)
                ])
            ],style=tab_card)
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph10',className='dbc',config=config_graph)
                ])
            ],style=tab_card)
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph11',className='dbc',config=config_graph)
                ])
            ],style=tab_card)
        ], sm=12, lg=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Escolha sua equipe'),
                    dcc.RadioItems(id='radio-team',
                                   options=options_team,
                                   value=0,
                                   inline=True,
                                   labelClassName="text-warning",
                                   inputCheckedClassName="border border-warning bg-warning",
                                   ),
                    html.Div(id="team-select",style={'text-align':'center','margin-top':'30px'},className='dbc')
                ])
            ],style=tab_card)
        ], sm=12, lg=2)      
    ],class_name='g-2 my-auto',style={'margin-top':'7px'})
    ], fluid=True, style={'height':'100vh'})

# Callbacks

# Grafico 1 e 2
@app.callback(
    Output('graph1','figure'),
    Output('graph2','figure'),
    Output('moth-select','childern'),
    Input('radio-moth','value'),
    Input(ThemeSwitchAIO.ids.switch("theme"),"value")
)

def graph1(month,toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = moth_filter(month)
    
    




# Rodar o server
if __name__ == '__main__':
    app.run_server(debug=True,port=8851)
