import os
import io
import pathlib
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd 
import sqlite3
import random
import datetime
import base64
from models.generete_barcode import generete_barcode
from models.cemix_to_excel import cemix_to_excel
from functions.functions import minutes_to_hh_mm ,fetch_famille_options ,get_input_options ,get_new_palette_number
import flask


app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    use_pages=True
)

app.title = "CEMIX - Shift Management"
server = app.server
app.config["suppress_callback_exceptions"] = True
app._favicon = "D_cemix.ico"


# Varibales
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

print("Main:  ",str(pathlib.Path(__file__).parent.resolve())) 

print("Main:  ",  os.path.join(str(pathlib.Path(__file__).parent.resolve()), 'Parametres\Cemix_input_parametre.xlsx'))

database_name = "Cemix_database_test.db"

file_path_excel_parameter = os.path.join(APP_PATH, 'Parametres\Cemix_input_parametre.xlsx')
shift_start_datetime_when_start = None

print("zia")

conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
cursor = conn.cursor()
cursor.execute("SELECT Id, username, password, dpt FROM Parameter")
result = cursor.fetchone()
conn.close()

username_golabl = result[1]
password_golabl = result[2]
dpt_golabl = result[3]


@app.server.route('/download_excel/')
def download_excel():
    # Serve the Excel file for download
    file_path_excel_parameter = os.path.join(APP_PATH, 'Parametres\Cemix_input_parametre.xlsx')
    if os.path.exists(file_path_excel_parameter):
        return flask.send_file(file_path_excel_parameter, as_attachment=True)
    else:
        return "File not found."

df_inputs = pd.read_excel(file_path_excel_parameter)



#########==============================================#########
#########==============================================#########
#########===========                        ===========#########
#########======== Functions [HTML Components] =========#########
#########===========                        ===========#########
#########==============================================#########
#########==============================================#########

def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("CEMIX"),
                    html.H6("Gestion des équipes et des palettes"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="Parametre_model",
                        children="Paramètre",
                        n_clicks=0
                    ),
                    html.A(
                        html.Img(id="logo", src=app.get_asset_url("cemix.png")),
                        href="",
                    ),
                ],
            ),
        ],
    )








def generate_modal_Parameter():
    return html.Div(
        id="markdown_Parameter",
        className="modal",
        children=(
            html.Div(
                id="markdown-Parameter-container",
                className="markdown-Parameter-container",
                children=[
                    html.Div(
                        className="close-Parameter-container",
                        children=
                        html.Button(
                            children =  'Fermer ' + 'X',
                            id="markdown_Parameter_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),

                    html.Br(),
                    
                    html.Div([
                        html.Div(
                            children = [
                                html.H2(
                                    "Paramètre et Configuration des Inputs",
                                    style={'text-align': 'center', "font-family": "Arial, sans-serif", "font-size": "32px", "display": "inline-block"} 
                                ),
                                dcc.Input(
                                    id='Password_input',
                                    type='password',
                                    value = None,
                                    placeholder = "Password",
                                    autoComplete='off',
                                    style={'display': 'inline-block', 'width': '40%', 'margin-left':'2%', 'font-weight':'bold', 'text-align': 'center'}
                                ),
                            ],
                            style={'display': 'inline-block', "margin-bottom": "40px", "width":"100%"}
                        ),
                        
                        html.Br(),

                        html.Div([

                            html.Label(
                                'Durée de Palette Theorique:',
                                style={'display': 'flex', 'width': '35%', 'font-weight':'bold' }
                            ),
                            dcc.Input(
                                id='DPT-input',
                                type='number',
                                value = dpt_golabl,
                                autoComplete='off',
                                style={'display': 'flex', 'width': '65%', 'margin-left':'2%', 'font-weight':'bold' }
                            ),
                            html.Button('Modifier le DPT',
                                    id='dpt_edit',
                                    n_clicks=0,
                                    style={ 'display': 'flex',
                                            'width': '20%',
                                            'margin-left':'2%',
                                            'background-color': '#4CAF50',
                                            'border': 'none',
                                            'color': 'white',
                                            'font-size': '12px',
                                            'cursor': 'pointer',
                                            'border-radius': '5px',
                                            'box-shadow': '0 0.5px 0.5px 0 rgba(0, 0, 0, 0.9)',
                                            'vertical-align': "center",
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                    },
                                    disabled=True,

                            ),

                        ], style={'display': 'flex', 'margin-bottom': '40px'}),

                        html.Div([

                            dcc.Input(
                                id='famille-input',
                                type='text',
                                value='',
                                placeholder = 'Familler', 
                                autoComplete='off',
                                style={'display': 'flex', 'width': '65%', 'font-weight':'bold' }
                            ),
                            dcc.Input(
                                id='abbv-famille-input',
                                type='text',
                                value='',
                                placeholder = 'Familler Abreviation ', 
                                autoComplete='off',
                                style={'display': 'flex', 'width': '65%', 'margin-left':'2%', 'font-weight':'bold' }
                            ),
                            html.Button('Ajouter Familler',
                                    id='add-famille-button',
                                    n_clicks=0,
                                    style={ 'display': 'flex',
                                            'width': '20%',
                                            'margin-left':'2%',
                                            'background-color': '#4CAF50',
                                            'border': 'none',
                                            'color': 'white',
                                            'font-size': '12px',
                                            'cursor': 'pointer',
                                            'border-radius': '5px',
                                            'box-shadow': '0 0.5px 0.5px 0 rgba(0, 0, 0, 0.9)',
                                            'vertical-align': "center",
                                            'align-items': 'center',
                                            'justify-content': 'center',
                                    },
                                    disabled=True,
                            ),

                        ], style={'display': 'flex', 'margin-bottom': '20px'}),
                        
                        # Section to insert Articles for a Famille
                        html.Div([
                            
                            dcc.Dropdown(
                                id='famille-dropdown',
                                options=fetch_famille_options(),
                                value=None,
                                placeholder = 'Familler',
                                style={ 'width': '100%', 'font-weight':'bold', 'background-color':'white' }
                            ),

                            dcc.Input(
                                id='article-input',
                                type='text',
                                value='',
                                placeholder = 'Article', 
                                autoComplete='off',
                                style={'width': '50%', 'margin-left':'2%', 'display': 'flex', 'font-weight':'bold'}
                            ),

                            dcc.Input(
                                id='article-abv-input',
                                type='text',
                                value='',
                                placeholder = 'Article Abreviation', 
                                autoComplete='off',
                                style={'width': '50%', 'margin-left':'2%',  'display': 'flex', 'font-weight':'bold'}
                            ),

                            html.Button('Ajouter Article', 
                                id='add-article-button', 
                                n_clicks=0, 
                                style={ 'display': 'flex',
                                        'width': '20%',
                                        'margin-left':'2%',
                                        'background-color': '#4CAF50',
                                        'border': 'none',
                                        'color': 'white',
                                        'font-size': '12px',
                                        'cursor': 'pointer',
                                        'border-radius': '5px',
                                        'box-shadow': '0 0.5px 0.5px 0 rgba(0, 0, 0, 0.9)',
                                        'vertical-align': "center",
                                        'align-items': 'center',
                                        'justify-content': 'center',
                                },
                                disabled=True,
                            ),
                        ], style={'display': 'flex', 'margin-bottom': '40px', 'width':'100%'}),

                        html.Div([
                            html.A(
                                "Telecharger le fichier de parametre",
                                href="/download_excel/",
                                id="download-button",
                                style={
                                    # "display": "inline-block",
                                    "padding": "10px 20px",
                                    "background-color": "#007BFF",
                                    "color": "#fff",
                                    "text-decoration": "none",
                                    "border": "none",
                                    "border-radius": "5px",
                                    "font-weight": "bold",
                                    'display': 'flex',
                                    'width': '50%',
                                    'margin-right': '10%',
                                    "pointer-events": "none",
                                    "cursor": "not-allowed"
                                },
                                # disabled=True,
                            ),
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Fichier Parametres')
                                ]),
                                style={
                                    'width': '100%',
                                    'height': '50px',
                                    'lineHeight': '50px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'textAlign': 'center',
                                    'padding-left': '10%',
                                    'padding-right': '10%',
                                    'display': 'flex'
                                },
                                multiple=False,
                                disabled=True,
                            ),
                            
                        ], style={'display': 'flex', 'margin-bottom': '1%', 'width':'100%'}),

                    
                        html.Div(
                                id='Feedback-output',
                                children="",
                                style={
                                        'display':'none'
                                }),
                            
                    ], style={"width": "86%", "margin": "10px auto"}) 
                ],
            )
        ),
    )




#########==============================================#########
#########==============================================#########
#########==============                  ==============#########
#########=========== Functions [Callbacks] ============#########
#########==============                  ==============#########
#########==============================================#########
#########==============================================#########


@app.callback(
    Output("markdown_Parameter", "style"),
    [
        Input("Parametre_model", "n_clicks"),
        Input("markdown_Parameter_close", "n_clicks"),
    ],
    prevent_initial_call= True,
)
def Model_Parameter(suivant_click, close):
    ctx = dash.callback_context
    if ctx.triggered and suivant_click > 0:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "Parametre_model" :
            
            return {"display": "block"}

    return {"display": "none"}



  

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        html.Div([
            dash.page_container,
        ], style={'width': '85%', 'alignItems': 'center', 'justifyContent': 'center',}),
        
        generate_modal_Parameter(),
        html.Div(id='output')
    ]
)


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8060)
