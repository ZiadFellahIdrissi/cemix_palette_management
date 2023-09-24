import dash
from dash import dcc, html

dash.register_page(__name__, path='/')

layout = html.Div([

    html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab_clustering",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="",
                        value="tab_clustering",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ]
    ),

    html.Div(
        id="app-container",
        children=[
            html.H4(
                id="Line_choise",
                children="Sélectionnez la ligne sur laquelle vous souhaitez travailler.",
                style={
                    'text-align': 'center',
                    'margin-top': '1%',
                    'margin-buttom': '0%',
                    "font-family": "Georgia, serif"
                }
            ),

            html.Div([
                dcc.Link(
                    html.Button(
                        id='forward_to_Line_1',
                        children="Ligne 1",
                        n_clicks=0,
                        style={
                            'padding': '0px',
                            'background-color': '#e42521',
                            'border': 'none',
                            'color': 'white',
                            'font-size': '16px',
                            'cursor': 'pointer',
                            'border-radius': '25px',
                            'box-shadow': '0 2px 2px 0 rgba(0, 0, 0, 0.8)',
                            'vertical-align': "center",
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'width': '200px',
                            'height': '40px',
                            'margin': '8px auto',
                            'margin-top': '20px'
                        }
                    ),
                    href='/ligne-1',
                    style={'margin': '8px auto', 'text-decoration': 'none'},  # Specify the URL you want to navigate to when the button is clicked
                ),

                dcc.Link(
                    html.Button(
                        id='forward_to_Line_2',
                        children="Ligne 2",
                        n_clicks=0,
                        style={
                            'padding': '0px',
                            'background-color': '#e42521',
                            'border': 'none',
                            'color': 'white',
                            'font-size': '16px',
                            'cursor': 'pointer',
                            'border-radius': '25px',
                            'box-shadow': '0 2px 2px 0 rgba(0, 0, 0, 0.8)',
                            'vertical-align': "center",
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'width': '200px',
                            'height': '40px',
                            'margin': '8px auto',
                            'margin-top': '20px'
                        }
                    ),
                    href='/ligne-2',
                    style={'margin': '8px auto', 'text-decoration': 'none'}, # Specify the URL you want to navigate to when the button is clicked
                ),

            ], style={'display': 'flex', 'width': '100%', "margin-top": "3px", "margin-bottom": "5px"}),

            html.Br(),

            html.Div([

                dcc.Link(
                    html.Button(
                        id='forward_to_Line_3',
                        children="Ligne 3",
                        n_clicks=0,
                        style={
                            'padding': '0px',
                            'background-color': '#e42521',
                            'border': 'none',
                            'color': 'white',
                            'font-size': '16px',
                            'cursor': 'pointer',
                            'border-radius': '25px',
                            'box-shadow': '0 2px 2px 0 rgba(0, 0, 0, 0.8)',
                            'vertical-align': "center",
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'width': '200px',
                            'height': '40px',
                            'margin': '8px auto',
                            'margin-top': '20px'
                        }
                    ),
                    href='/ligne-3',
                    style={'margin': '8px auto', 'text-decoration': 'none'},  # Specify the URL you want to navigate to when the button is clicked
                ),

                dcc.Link(
                    html.Button(
                        id='forward_to_Line_4',
                        children="Ligne 4",
                        n_clicks=0,
                        style={
                            'padding': '0px',
                            'background-color': '#e42521',
                            'border': 'none',
                            'color': 'white',
                            'font-size': '16px',
                            'cursor': 'pointer',
                            'border-radius': '25px',
                            'box-shadow': '0 2px 2px 0 rgba(0, 0, 0, 0.8)',
                            'vertical-align': "center",
                            'display': 'flex',
                            'align-items': 'center',
                            'justify-content': 'center',
                            'width': '200px',
                            'height': '40px',
                            'margin': '8px auto',
                            'margin-top': '20px'
                        }
                    ),
                    href='/ligne-4',
                    style={'margin': '8px auto', 'text-decoration': 'none'},
                )
            ], style={'display': 'flex', 'width': '100%', "margin-top": "3px", "margin-bottom": "5px"}),

        ], style={"width": "95%", "margin": "10px auto", "padding": "2%", 'textAlign': 'center'}
    )

])

