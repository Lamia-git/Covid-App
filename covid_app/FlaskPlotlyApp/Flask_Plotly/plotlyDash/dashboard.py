import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
from .utils import expDataDepartment, expDataRegion, GetInfoPopulation
from dash.dependencies import Input, Output
import plotly.graph_objs as go
# Data
df_depart, allDataDepartment,dfDepDate = expDataDepartment()
default = allDataDepartment[(allDataDepartment['departement'] == 'Loire-Atlantique')]
depart = df_depart['departement'].unique()
region, allDataRegion = expDataRegion()
df_depart_pop,df_region_pop = GetInfoPopulation()


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/style.css', '/static/bulma/bulma/css/bulma.min.css'
        ]
    )
    # Graphs
    # Bar to show result covid by department
    dataByDepart = px.bar(default, x="date", y="deces",
                          labels={'deces': 'Nombre de décès'},
                          color="deces",
                          barmode="group",
                          hover_name="departement",
                          hover_data=["hospitalises", "reanimation", "gueris"],
                          height=400,
                         )

    # Graphe Confinement
    figure_confinement = go.Figure()
    figure_confinement.add_trace(go.Scatter(x=allDataRegion.date,
                                            y=allDataRegion.nouvellesHospitalisations,
                                            mode='lines',
                                            name='Nouvelles Hospitalisations',))

    figure_confinement.add_trace(go.Scatter(x=allDataRegion.date,
                                            y=allDataRegion.nouvellesReanimations,
                                            mode='lines',
                                            name='Nouvelles Reanimations', ))

    figure_confinement.add_vrect(
                  x0='2020-03-17', x1='2020-05-11')

    figure_confinement.add_vrect(
        x0='2020-10-30', x1='2020-12-15')
    figure_confinement.add_vrect(
        x0='2021-4-3', x1='2021-5-3')

    #Departement plus touchés
    figure_depart_touche = px.bar(df_depart_pop, x='departement',
                                  y="deces_population",
                                  labels={'deces_population':'Nombre de décès sur la population'},
                                  color='deces_population',
                                  height=400,
                                  width =1050)

    figure_depart_touche.update_layout(barmode='group', xaxis_tickangle=-45)

    #comparaison gurison et hospitalisation


    figure_comp_bis =  go.Figure()
    figure_comp_bis.add_trace(go.Scatter(x=dfDepDate.date,
                                         y=dfDepDate.nouvellesHospitalisations,
                                        mode='markers',
                                         name='Nouvelles Hospitalisations',))

    figure_comp_bis.add_trace(go.Scatter(x=dfDepDate.date, y=dfDepDate.nouveau_deces,
                                            mode='markers',
                                            name='nouveau décès', ))

    #Region plus touchés
    figure_region_touche = px.pie(df_region_pop, values='deces', names='region')
    figure_region_touche.update_traces(textfont_size=20)



    # Create Dash Layout

    dash_app.layout = html.Div(
        html.Div(
            className="column is-12 ",
            children=[
                html.Div(
                    className="columns",
                    children=[
                        html.Div(
                            className="column is-6",
                            children=[
                                html.H1("STATISTIQUES CORONAVIRUS PAR DEPARETEMENT",
                                        style={'textAlign': 'center',
                                               'color': 'black',
                                               'margin-bottom': '15px',
                                               'font-size': 'xx-large'}),

                                dcc.Dropdown(
                                    id='filterDepartement',
                                    placeholder='Loire-Atlantique',
                                    options=[{'label': i, 'value': i} for i in depart],
                                    value='Loire-Atlantique'
                                ),
                                dcc.Graph(
                                    id='covid-dep',
                                    figure=dataByDepart
                                )
                            ]
                        ),
                        html.Div(
                            className="column is-6",
                            children=[

                                html.H1("STATISTIQUES CORONAVIRUS (EN/HORS CONFINEMENT)",
                                        style={'textAlign': 'center',
                                               'color': 'black',
                                               'margin-bottom': '15px',
                                               'font-size': 'xx-large'}),
                                dcc.Graph(
                                    id='Confinement',
                                    figure=figure_confinement
                                ),
                            ]
                        ),



                    ]),
                html.Div(
                    className="columns",
                    children=[html.Div(
                            className="column is-6",
                            children=[

                                html.H1("LES DÉPARTEMENT LES PLUS TOUCHÉS",
                                        style={'textAlign': 'center',
                                               'color': 'black',
                                               'margin-bottom': '15px',
                                               'font-size': 'xx-large'}),
                                dcc.Graph(
                                    id='depart_touches',
                                    figure=figure_depart_touche
                                ),

                            ], ),

                        html.Div(

                            className="column is-6",
                            children=
                            [

                                html.H1("LES RÉGIONS LES PLUS TOUCHÉES",
                                        style={'textAlign': 'center',
                                               'color': 'black',
                                               'margin-bottom': '15px',
                                               'font-size': 'xx-large'}),
                                dcc.Graph(
                                    id='region_touches',
                                    figure=figure_region_touche
                                ),

                            ], ),]),
                html.Div(
                    className="columns",
                    children=[html.Div(
                            className="column is-offset-2 is-8",
                            children=[

                                html.H1("MESURE DES TAUX DE LÉTALITÉ HOSPITALIÈRE ('TERRITOIRE DE BELFORT')",
                                        style={'textAlign': 'center',
                                               'color': 'black',
                                               'margin-bottom': '15px',
                                               'font-size': 'xx-large'}),
                                dcc.Graph(
                                    id='comparasion',
                                    figure=figure_comp_bis
                                ),

                            ]),]),
            ])
    )

    @dash_app.callback(
        # What does the callback change? Right now we want to change the figure of the graph.
        # You can assign only one callback for each property of each component.
        Output(component_id='covid-dep', component_property='figure'),

        # Any components that modify the outcome of the callback
        # (sect_id picker should go here as well)
        [Input(component_id='filterDepartement', component_property='value')])
    def update_graph(departement):
        default = allDataDepartment[(allDataDepartment['departement'] == departement)]
        dataByDepart = px.bar(default, x="date", y="deces",
                              labels={'deces': 'Nombre de décès'},color="deces", barmode="group",
                              hover_name="departement",
                              hover_data=["hospitalises", "reanimation", "gueris"], height=400,)
        return dataByDepart

    return dash_app.server
