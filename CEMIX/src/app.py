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
from generete_barcode import generete_barcode
from cemix_to_excel import cemix_to_excel
import flask


app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

app.title = "CEMIX - Shift Management"
server = app.server
app.config["suppress_callback_exceptions"] = True
app._favicon = "D_cemix.ico"


# Varibales
APP_PATH = str(pathlib.Path(__file__).parent.resolve())
database_name = "Cemix_database_test.db"
file_path_excel_parameter = os.path.join(APP_PATH, 'Parametres\Cemix_input_parametre.xlsx')
shift_start_datetime_when_start = None

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
#########===============                ===============#########
#########============ Functions [Helpers] =============#########
#########===============                ===============#########
#########==============================================#########
#########==============================================#########

def minutes_to_hh_mm(minutes):
    # Calculate the hours and remaining minutes
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    
    # Handle the fractional part of minutes
    fractional_minutes = minutes - int(minutes)
    seconds = int(fractional_minutes * 60)

    # Format the result as HH:MM:SS
    hh_mm_ss = f'{hours:02d}:{remaining_minutes:02d}:{seconds:02d}'
    
    return hh_mm_ss


def fetch_famille_options():
    conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
    cursor = conn.cursor()
    cursor.execute("SELECT Id, nom_famille FROM Famille")
    famille_options = [{'label': row[1], 'value': row[0]} for row in cursor.fetchall()]
    conn.close()
    return famille_options
    



def get_input_options(df,column):
    column_list = list(df[df[column] != "/////////////"][column])
    return [{'label': item, 'value': item} for index, item in enumerate(column_list)]




def get_new_palette_number(cursor):

    cursor.execute("""
                        SELECT numero_palette, date
                        FROM palette
                        WHERE 
                        (
                        strftime('%H:%M:%S', 'now') >= '07:00:00' 
                        AND date BETWEEN 
                                        datetime('now', 'start of day', '-0 day', '07:00:00') AND 
                                        datetime('now', 'start of day','+1 day', '07:00:00')
                        )
                        OR
                        (
                        strftime('%H:%M:%S', 'now') < '07:00:00' 
                        AND date BETWEEN 
                                            datetime('now', 'start of day', '-1 day', '07:00:00') AND
                                            datetime('now', 'start of day', '+0 day', '07:00:00')
                        )
                        ORDER BY date DESC
                        LIMIT 1;
                    """)
    
    last_palette = cursor.fetchone()
    last_numero_palette, last_creation_date = last_palette if last_palette else ('P0000', None)

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Calculate the cycle start and end times (from 7 AM to 7 AM)
    cycle_start = current_datetime.replace(hour=7, minute=0, second=0, microsecond=0)
    if current_datetime.hour < 7:
        cycle_start -= datetime.timedelta(days=1)
    cycle_end = cycle_start + datetime.timedelta(days=1)

    # Determine if we're within the current cycle
    within_current_cycle = cycle_start <= current_datetime < cycle_end

    # Increment 'numero_palette' if within the current cycle
    if within_current_cycle:
        if last_numero_palette == 'P999':
            new_numero_palette = 'P0001'
        else:
            new_numero_palette = f'P{int(last_numero_palette[1:]) + 1:04}'
    else:
        new_numero_palette = 'P0001'

    # Close the database connection
    
    return new_numero_palette







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


def build_tabs():
    return html.Div(
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
                    # dcc.Tab(
                    #     id="Control-chart-tab",
                    #     label="le stock",
                    #     value="tab_itinerary",
                    #     className="custom-tab",
                    #     selected_className="custom-tab--selected",
                    # ),
                ],
            )
        ],
    )



def generate_modal():
    conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
    cursor = conn.cursor()
    numero_palette = get_new_palette_number(cursor)
    conn.close()

    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=
                        html.Button(
                            children = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),

                    html.Div([
                        html.H2("PALETTE N°", style={'text-align': 'center', "font-family": "Arial, sans-serif", "font-size": "32px", "margin-bottom": "3px"}),
                        html.H1(id="number_of_palette", children=str(numero_palette), style={'text-align': 'center', "font-family": "Georgia, serif", "font-size": "48px"}),
                        html.Div([
                            
                            dcc.Dropdown(
                                id = 'product_family_input',
                                options=fetch_famille_options(),
                                value = None,
                                placeholder='Famille',
                                style={"width": "100%", "height": "50px", 'text-align':'center', 'margin-right': '15px', 'font-weight': 'bold'}
                            ),
                            
                            dcc.Dropdown(
                                id = 'article_input',
                                options=[],
                                value = None,
                                placeholder='Article',
                                style={"width": "100%", "height": "50px", 'text-align': 'center', 'font-weight': 'bold'}
                            ),
                            
                        ], style={'display': 'flex', 'width': '100%', "margin-top": "3px", "margin-bottom": "5px"}),
                        
                        # html.Br(),

                        html.Div([
                            dcc.Input(
                                id = 'nb_sac_input',
                                type='number',
                                placeholder='NOMBRE DE SAC',
                                autoComplete='off',
                                style={"width": "97.5%", "height": "50px", "background-color": "#000000", "color": "#ffffff", 'font-weight': 'bold', 'text-align': 'center', 'margin-right': '15px'}
                            ),
                            dcc.Dropdown(
                                id='Palette_comment',
                                options = get_input_options(df_inputs, "Commentaire"),
                                value=None,
                                placeholder='Commentaire',
                                style={"width": "100%", "height": "50px", 'text-align': 'center', 'font-weight': 'bold'}
                            ),

                        ], style={'display': 'flex', 'width': '100%', "margin-bottom": "2px"}),
                        
                        html.Br(),
                        
                        dcc.Input(
                            id = 'Poid_palette_input',
                            type='text',
                            placeholder='POIDS PALETTE ...',
                            autoComplete='off',
                            style={'font-size': '24px', 'font-weight': 'bold','width': '100%', 'height': '60px', 'text-align': 'center', "margin-bottom": "10px"}
                        ),
                        html.Div([
                            html.Label('ECHANTILLON 4 KG', style = {"width": "100%", 'font-size': '30px', "margin-right": "50px"}),
                            dcc.RadioItems(
                                id = 'echantillon_4kg_input',
                                options=[
                                    {'label': 'Oui', 'value': 'oui'},
                                    {'label': 'Non', 'value': 'non'}
                                ],
                                value='oui',
                                labelStyle={'display': 'flex', 'font-size': '28px'},
                                style = {"width": "100%"}
                            ),
                            html.Label('ECHANTILLON 10 KG', style = {"width": "100%", 'font-size': '30px', "margin-right": "50px"}),
                            dcc.RadioItems(
                                id = 'echantillon_10kg_input',
                                options=[
                                    {'label': 'Oui', 'value': 'oui'},
                                    {'label': 'Non', 'value': 'non'}
                                ],
                                value='non',
                                labelStyle={'display': 'flex', 'font-size': '28px'},
                                style = {"width": "100%"}
                            
                            ),
                            
                        ], style={'display': 'flex', 'width': '100%'}),

                        html.Div([
                            html.Button(
                                id='Suivant_button',
                                children="Suivant",
                                n_clicks=0,
                                style={
                                    'padding': '0px',
                                    'background-color': '#4CAF50',
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
                            html.Button(
                                id='Terminer-Button',
                                children="Terminer",
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
                            
                        ], style={'display': 'flex', 'width': '100%', "margin":"1px auto"}),

                        
                    ], style={"width": "86%", "margin": "10px auto", 'textAlign': 'center'})

                ],
            )
        ),
    )


def build_input_settings():
    return html.Div([
            html.Div([
                dcc.Dropdown(
                    id='ligne-input',
                    options=[
                             {'label': 'Ligne', 'value': 'line'},
                             {'label': 'Ligne 1', 'value': 'line_1'},
                             {'label': 'Ligne 2', 'value': 'line_2'},
                             {'label': 'Ligne 3', 'value': 'line_3'},
                             {'label': 'Ligne 3', 'value': 'line_4'},
                            ],
                    value='line',
                    style={'margin': '6px auto','margin-top': '20px', 'width': '80%', 'text-align':'center'}
                ),
                dcc.Dropdown(
                    id='shift-input',
                    options=[
                             {'label': 'Shift', 'value': 'Shift'},
                             {'label': "shift-1", 'value': "shift-1"},
                             {'label': "shift-2", 'value': "shift-2"},
                             {'label': "shift-3", 'value': "shift-3"},
                             {'label': "shift-4", 'value': "shift-4"},
                             {'label': "shift-5", 'value': "shift-5"},
                             {'label': "shift-6", 'value': "shift-6"}
                            ],
                    value='Shift',
                    style={'margin': '6px auto', 'width': '80%', 'text-align':'center'}
                ),
                dcc.Dropdown(
                    id='operateur_mix-input',
                    options=get_input_options(df_inputs, "operateur_mix"),
                    value=None,
                    placeholder="OPERATEUR MIX",
                    style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'color':'white', 'opacity': '1', 'font-weight':'bold'}
                ),
                dcc.Dropdown(
                    id='operateur_ensacheus-input',
                    options=get_input_options(df_inputs, "operateur_ensacheuse"),
                    value = None,
                    placeholder="OPERATEUR ENSACHEUS",
                    style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'color':'white', 'opacity': '1', 'font-weight':'bold'}
                ),
                dcc.Dropdown(
                    id='clarsite_m-input',
                    options=get_input_options(df_inputs, "clariste_m"),
                    value = None,
                    placeholder="CLARISTE M",
                    style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'color':'white', 'opacity': '1', 'font-weight':'bold'}
                ),
                dcc.Dropdown(
                    id='clarsite_p-input',
                    options=get_input_options(df_inputs, "clariste_p"),
                    value = None,
                    placeholder="CLARISTE P",
                    style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'color':'white', 'opacity': '1', 'font-weight':'bold'}
                ),
                dcc.Dropdown(
                    id='aide_magasinier-input',
                    options=get_input_options(df_inputs, "aide_magasinier"),
                    value = None,
                    placeholder="AIDE MAGASINIER" ,
                    style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'color':'white', 'opacity': '1', 'font-weight':'bold'}
                ),
                html.Button(
                        id='start-shift',
                        children=[
                            html.Span(className='plus', children='Demare')
                        ],
                        n_clicks=0,
                        style={
                            'padding': '0px',
                            'background-color': '#4CAF50',
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
            ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center'}),
    ])



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
    Output("app-content", "children"),
    [Input("app-tabs", "value")]
)
def render_tab_content(tab_switch):

    if tab_switch == "tab_itinerary":
        return 
    return (
        html.Div(
            # id="status-container",
            children=[
                build_input_settings(),
            ],
        ),
        
    )


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


@app.callback(
    Output("upload-data", "disabled"),
    Output("add-article-button", "disabled"),
    Output("add-famille-button", "disabled"),
    Output("dpt_edit", "disabled"),
    Output("download-button", "style"),

    Input("Password_input", "value")
)
def verify_password(password):
    style={
        # "display": "inline-block",
        "padding": "10px 20px",
        "background-color": "#007BFF",
        "color": "#fff",
        "text-decoration": "none",
        "border": "none",
        "border-radius": "5px",
        "cursor": "pointer",
        "font-weight": "bold",
        'display': 'flex',
        'width': '50%',
        'margin-right': '10%',
    }
    if password == password_golabl:
        return  False, False, False, False, style
    else:
        return  True, True, True, True, dash.no_update
    

@app.callback(
    Output('article_input', 'options'),
    Input('product_family_input', 'value')
)
def update_article_options(selected_famille):
    if selected_famille is None:
        return []
    
    conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
    cursor = conn.cursor()
    # Query the database for Article options based on the selected Famille
    cursor.execute("SELECT Id, nom_article FROM Article WHERE famille_id = ?", (selected_famille,))
    article_options = [{'label': row[1], 'value': row[0]} for row in cursor.fetchall()]
    
    return article_options




@app.callback(
    Output('output-div', 'children'),
    Input('upload-data', 'contents'),
    Input('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        raise PreventUpdate

    try:
        # Parse the content of the uploaded file
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_excel(io.BytesIO(decoded))

        # Define the folder path for saving the file
        folder_path = os.path.join(APP_PATH, 'Parametres')

        filename = "Cemix_input_parametre.xlsx"
        # Define the full path for the saved file
        file_path = os.path.join(folder_path, filename)

        # Save the uploaded file to the folder
        df.to_excel(file_path, index=False)

        return html.Div([
            html.H6('File successfully uploaded and saved to "Parametres" '),
            html.P(filename)
        ])

    except Exception as e:
        return html.Div([
            html.H6('An error occurred while processing the file ...'),
            html.Pre(str(e))
        ])




@app.callback(
    Output('famille-dropdown', 'options'),
    Output('famille-input', 'value'),
    Output('abbv-famille-input', 'value'),
    Output('famille-dropdown', 'value'),
    Output('article-input', 'value'),
    Output('article-abv-input', 'value'),
    Output('Feedback-output', 'children'),
    Output('Feedback-output', 'style'),
    Output("DPT-input", "value"),
    Input('dpt_edit', 'n_clicks'),
    Input('add-famille-button', 'n_clicks'),
    Input('add-article-button', 'n_clicks'),
    State('famille-input', 'value'),
    State('abbv-famille-input', 'value'),
    State('famille-dropdown', 'value'),
    State('article-input', 'value'),
    State('article-abv-input', 'value'),
    State("DPT-input", "value"),
    prevent_initial_call=True
)
def add_famille_or_article(n_clicks_famille, n_clicks_article, n_clicks_dpt, famille_name, famille_abv, selected_famille, article_name, article_abv, dpt_in):
    style = {
        'margin-top': '5%',
        'border': '1px solid white',
        'border-radius': '10px',
        'padding': '10px',
        'align-items': "center",
        'text-align': "center",
        'display': 'block'
    }
    famille_options = fetch_famille_options()
    
    ctx = dash.callback_context
    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == 'add-famille-button':
            if famille_name and famille_abv:
                conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Famille (nom_famille, abreviation_famille) VALUES (?, ?)",
                            (famille_name, famille_abv))
                conn.commit()
                conn.close()
                style["background-color"] = '#4CAF50'
                msg_reuss = 'La Famille ' + famille_name + ' est Bien Ajoutée '
                famille_options = fetch_famille_options()
                return famille_options, '', '', '', '', '', msg_reuss, style, dash.no_update
            else:
                style["background-color"] = 'red'
                msg_error = 'Remplissez les champs pour ajouter une Famille!'
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, msg_error, style, dash.no_update
        
        elif prop_id == 'add-article-button':
            if selected_famille and article_name:
                conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
                cursor = conn.cursor()
                cursor.execute("INSERT INTO Article (nom_article, abreviation_article, famille_id) VALUES (?, ?, ?)",
                            (article_name, article_abv, selected_famille))
                conn.commit()
                conn.close()
                style["background-color"] = '#4CAF50'
                msg_reuss = "L'article " + article_name + " est Bien Ajouté "
                return dash.no_update, '', '', '', '', '', msg_reuss, style, dash.no_update
            else:
                style["background-color"] = 'red'
                msg_error = 'Remplissez les champs pour ajouter un Article!'
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, msg_error, style, dash.no_update
    
        elif prop_id == 'dpt_edit':
            if dpt_in:
                global dpt_golabl
                conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
                cursor = conn.cursor()
                cursor.execute("update Parameter set dpt = ? where id = ?;",
                              (dpt_in, 1,))
                conn.commit()
                conn.close()
                style["background-color"] = '#4CAF50'
                dpt_golabl = dpt_in
                msg_reuss = "DPT est Bien Modifié [dpt = "+str(dpt_in)+" ]"
                return dash.no_update, '', '', '', '', '', msg_reuss, style, dpt_in
            else:
                style["background-color"] = 'red'
                msg_error = 'Remplissez le champ pour modifier le DPT !'
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, msg_error, style, dpt_in
        
    return famille_options, '', '', '', '', '', '', style, dpt_in



@app.callback(
    Output("markdown", "style"),
    [
        Input("start-shift", "n_clicks"),
        Input("Terminer-Button", "n_clicks"),
    ],
    [
        State("ligne-input", "value"),
        State("shift-input", "value"),
        State("operateur_mix-input", "value"),
        State("operateur_ensacheus-input", "value"),
        State("clarsite_m-input", "value"),
        State("clarsite_p-input", "value"),
        State("aide_magasinier-input", "value"),
    ],
    prevent_initial_call= True
)
def update_click_output(suivant_click, terminer_click, ligne, shift, operateur_mix, operateur_ensacheus, clarsite_m, clarsite_p, aide_magasinier):
    ctx = dash.callback_context

    if ctx.triggered and suivant_click > 0:

        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "start-shift" :
            global shift_start_datetime_when_start
            conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
            query = """
                        INSERT INTO cemix_info (date, heure, ligne, shift, operateur_mix, operateur_ensacheuse, clarist_m, clariste_p, aide_magasinier, is_terminer)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
            
            shift_start_datetime_when_start = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            current_date = datetime.datetime.now() - datetime.timedelta(hours=6.5)
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            conn.execute(query, (current_date.strftime("%Y-%m-%d"), current_time, ligne, shift, operateur_mix, operateur_ensacheus, clarsite_m ,clarsite_p ,aide_magasinier, 0))
            conn.commit()

            folder_this_day_format = datetime.datetime.now() - datetime.timedelta(1)
            folder_this_day = os.path.join(APP_PATH, "Journal Shifts", "Jour_" + folder_this_day_format.strftime("%d_%m_%Y"))

            if not os.path.exists(folder_this_day):
                os.mkdir(folder_this_day)

            if not os.path.exists(os.path.join(folder_this_day, "All Day")):
                os.mkdir(os.path.join(folder_this_day, "All Day"))

            day_before = datetime.datetime.now() - datetime.timedelta(hours=6.5) - datetime.timedelta(hours=24)
            format_shifts_all_day = "Shifts__" + day_before.strftime("%d_%m_%Y") + ".xlsx"
            path_shifts_all_day = os.path.join(folder_this_day, "All Day", format_shifts_all_day)

            if not os.path.exists(path_shifts_all_day):
                data_header_allDay = {
                    'Variable': [
                        'Date', 'Heure', 'Durée de palette Theorique', 'Objectif PALETTE theorique',
                        'TOTAL SAC THEORIQUE', 'TOTAL POID', 'Total d\'heure travail',
                        'durée total d\'arret', 'Total palette', 'total sac'
                        ],
                    'Value': None
                }

                query = """
                    SELECT c.date as 'Date de Shift', c.heure as 'Heure de Shift',
                    c.ligne as 'Ligne', c.shift as 'Shift', c.operateur_mix as 'Operateur Mix', 
                    c.operateur_ensacheuse  as 'Operateur Ensacheuse',
                    c.clarist_m  as 'Clarist M', c.clariste_p as 'Clariste P',
                    c.aide_magasinier as 'Aide Magasinier',
                    p.date as 'Date de Palette', p.numero_palette as 'Numero de Palette' ,
                    a.nom_article as 'Article', p.nombre_de_sac as 'Nombre de Sac',
                    p.Commentair as 'Error Commentair', p.poids as 'Poids',
                    p.echantillon_10Kg as 'Echantillon 10Kg',
                    p.echantillon_4Kg as 'Echantillon 4Kg',
                    p.duration_min as 'Palatte_duration',
                    p.ecart_by_10 as 'Ecart'
                    FROM cemix_info c
                    join palette p on p.cemix_main_id = c.id
                    join article a on a.id = p.article_id
                    where DATE(c.date) = DATE('now', '-9 day');
                """
                df_all_day = pd.read_sql_query(query, conn)


                Date_cemix = df_all_day["Date de Shift"].iloc[0]
                heure_cemix = df_all_day["Heure de Shift"].iloc[0]
                tottal_heure_travaile = df_all_day["Palatte_duration"].sum()

                otp = round(( (tottal_heure_travaile) / dpt_golabl ),2)
                ots = round((otp*64),2)

                tottal_poids = df_all_day["Poids"].sum()
                tottal_darret = df_all_day[df_all_day["Ecart"] >= 0]["Ecart"].sum()
                tottal_palette = df_all_day.shape[0]
                tottal_sac = df_all_day["Nombre de Sac"].sum()
                

                final_values_header = []
                final_values_header.extend([
                                            Date_cemix, heure_cemix, str(dpt_golabl), str(otp),
                                            str(ots), str(tottal_poids), 
                                            minutes_to_hh_mm(tottal_heure_travaile), str(tottal_darret), str(tottal_palette),
                                            str(tottal_sac)
                                            ])
            
                data_header_allDay["Value"] =  final_values_header

                df_all_day_UD = df_all_day[[
                        "Date de Palette", "Numero de Palette", "Nombre de Sac", "Article",
                        "Operateur Mix", "Operateur Ensacheuse", "Clarist M", "Clariste P", "Aide Magasinier",
                        "Error Commentair", "Palatte_duration", "Ecart"
                        ]]

                header_all_day = df_all_day_UD.columns.tolist()
                df_all_day_UD.loc[-1] = header_all_day
                df_all_day_UD.index = df_all_day_UD.index + 1
                df_all_day_UD = df_all_day_UD.sort_index()

                cemix_to_excel(
                                df_header = data_header_allDay,
                                df_ = df_all_day_UD, 
                                header_name = "reporting journalier d'ensachage",
                                filename = path_shifts_all_day, 
                                ishift = False, 
                                size = 16.5, 
                                num_rows=2 
                            )

            conn.close()
                
            
            return {"display": "block"}
        
        if prop_id == "Terminer-Button" :
            conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
            data_header_shift = {
                'Variable': ['OPERATEUR MIX', 'OPERATEUR ENSACH', 'CLARIST P', 'CLARIST M', 'AIDE MAGASIGNIER', 'Date', 'Heure', 'Durée de palette Theorique', 'Objectif PALETTE theorique', 'TOTAL SAC THEORIQUE', 'TOTAL POID', 'Total d\'heure travail', "durée total d'arret", 'Total palette', 'total sac'],
                'Value': None
            }
            query = """
                SELECT c.date as 'Date de Shift', c.heure as 'Heure de Shift',
                c.ligne as 'Ligne', c.shift as 'Shift', c.operateur_mix as 'Operateur Mix', 
                c.operateur_ensacheuse  as 'Operateur Ensacheuse',
                c.clarist_m  as 'Clarist M', c.clariste_p as 'Clariste P',
                c.aide_magasinier as 'Aide Magasinier',
                p.date as 'Date de Palette', p.numero_palette as 'Numero de Palette' ,
                a.nom_article as 'Article', p.nombre_de_sac as 'Nombre de Sac',
                p.Commentair as 'Error Commentair', p.poids as 'Poids',
                p.echantillon_10Kg as 'Echantillon 10Kg',
                p.echantillon_4Kg as 'Echantillon 4Kg',
                p.duration_min as 'Palatte_duration',
                p.ecart_by_10 as 'Ecart'
                FROM cemix_info c
                join palette p on p.cemix_main_id = c.id
                join article a on a.id = p.article_id
                where c.is_terminer = 0;
            """
            df_shift = pd.read_sql_query(query, conn)

            cursor = conn.cursor()
            cursor.execute("SELECT c.id FROM cemix_info c WHERE c.is_terminer = ?", (0,))
            result = cursor.fetchone()
            cemix_id = result[0]

            cursor.execute("UPDATE cemix_info SET is_terminer = ? WHERE id = ?", (1, cemix_id,))

            folder_this_day_format = datetime.datetime.now().strftime("%d_%m_%Y")
            folder_this_day = os.path.join(APP_PATH, "Journal Shifts", "Jour_"+folder_this_day_format)

            if not os.path.exists(folder_this_day):
                os.mkdir(folder_this_day)
            
            if not os.path.exists(os.path.join(folder_this_day, "Shifts")):
                os.mkdir(os.path.join(folder_this_day, "Shifts"))

            shift_format = shift + "__" + datetime.datetime.now().strftime("%d_%M_%Y__%H_%M_%S") + ".xlsx"
            file_output_shift = os.path.join(folder_this_day, "Shifts", shift_format)


            cemix_info_list = list(df_shift[["Operateur Mix","Operateur Ensacheuse", "Clariste P", "Clarist M", "Aide Magasinier"]].iloc[0])
            shift_start_date = df_shift["Date de Shift"].iloc[0]
            shift_start_time = df_shift["Heure de Shift"].iloc[0]

            shift_start_datetime = df_shift["Date de Palette"].iloc[0]
            shift_start_datetime = datetime.datetime.strptime(shift_start_datetime , '%Y-%m-%d %H:%M:%S')

            current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_date = datetime.datetime.strptime(current_date , '%Y-%m-%d %H:%M:%S')

            tottal_dure_travaile = current_date - shift_start_datetime
            otp = round(( (tottal_dure_travaile.total_seconds() / 60) / dpt_golabl ),2)
            ots = round((otp*64),2)
            tottal_poids = df_shift["Poids"].sum()
            tottal_darret = df_shift[df_shift["Ecart"] >= 0]["Ecart"].sum()
            tottal_palette = df_shift.shape[0]
            tottal_sac = df_shift["Nombre de Sac"].sum()


            final_values_header = []
            final_values_header.extend(cemix_info_list)
            final_values_header.extend([
                                        shift_start_date, shift_start_time, str(dpt_golabl), str(otp),
                                        str(ots), str(tottal_poids), 
                                        str(tottal_dure_travaile), str(tottal_darret), str(tottal_palette),
                                        str(tottal_sac)
                                        ])
            
            data_header_shift["Value"] =  final_values_header

            df_shift_UD = df_shift[[
                                    "Date de Palette", "Numero de Palette", "Nombre de Sac",
                                    "Article", "Error Commentair", "Echantillon 10Kg", 
                                    "Echantillon 4Kg", "Palatte_duration", "Ecart"
                                    ]]

            header_shift = df_shift_UD.columns.tolist()
            df_shift_UD.loc[-1] = header_shift
            df_shift_UD.index = df_shift_UD.index + 1
            df_shift_UD = df_shift_UD.sort_index()


            cemix_to_excel(
                            df_header = data_header_shift,
                            df_ = df_shift_UD,
                            header_name = "SHIFT reporting d'ensachage",
                            filename = file_output_shift,
                            ishift = True,
                            size = 18.5, 
                            num_rows = 3 )
        
            conn.commit()
            conn.close()

    return {"display": "none"}



@app.callback(
    [
        Output("number_of_palette", "children"),
        Output("markdown_close", "children"),
        Output("product_family_input", "value"),
        Output("article_input", "value"),
        Output("nb_sac_input", "value"),
        Output("Palette_comment", "value"),
        Output("Poid_palette_input", "value"),
        Output("echantillon_4kg_input", "value"),
        Output("echantillon_10kg_input", "value"),
    ],
    [Input("Suivant_button", "n_clicks")],
    [
        State("product_family_input", "value"),
        State("article_input", "value"),
        State("nb_sac_input", "value"),
        State("Palette_comment", "value"),
        State("Poid_palette_input", "value"),
        State("echantillon_4kg_input", "value"),
        State("echantillon_10kg_input", "value"),
    ],
    
    prevent_initial_call= True
)
def Suivant(Suivant_button, product_family, article, nb_sac, Palette_comment, Poid_palette, echantillon_4kg, echantillon_10kg):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if Suivant_button > 0:
        conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
        cursor = conn.cursor()
        cursor.execute("SELECT c.id, c.date, c.heure, c.shift, c.ligne FROM cemix_info c WHERE c.is_terminer = ?", (0,))
        result = cursor.fetchone()
        cemix_id = result[0]
        cemix_date = result[1]
        cemix_heure = result[2]
        cemix_shift = result[3]
        cemix_ligne = result[4]
        
        numero_palette = get_new_palette_number(cursor)
        
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_date_UD = datetime.datetime.strptime(current_date , '%Y-%m-%d %H:%M:%S')
        duration = None


        cursor.execute("select p.id, p.date from palette p join cemix_info c on p.cemix_main_id = c.id where c.id = ? order by p.Id desc limit ?;  ", (cemix_id,1))
        result = cursor.fetchone()
        if not result: 
            shift_start_date = shift_start_datetime_when_start
            shift_start_date = datetime.datetime.strptime(shift_start_date , '%Y-%m-%d %H:%M:%S')
            duration  = current_date_UD - shift_start_date
            duration = duration.total_seconds() / 60

        else: 
            palette_prec_date = datetime.datetime.strptime(result[1] , '%Y-%m-%d %H:%M:%S')
            duration  = current_date_UD - palette_prec_date
            duration = duration.total_seconds() / 60


        cursor.execute("select id from Article where id = ?;", (article,))
        result = cursor.fetchone()
        article_id = result[0]

        query = """
                INSERT INTO palette (date, numero_palette, article_id, nombre_de_sac, Commentair, poids, echantillon_4Kg, echantillon_10Kg, duration_min, ecart_by_10, cemix_main_id)
                VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
        
        try:
            cursor.execute(query, (current_date, str(numero_palette), int(article_id), int(nb_sac), str(Palette_comment), float(Poid_palette), echantillon_4kg, echantillon_10kg, round(duration,2), round((duration - int(dpt_golabl)),2),  cemix_id,))
        except:
            print("error")

        Num_Palette_complet = cemix_date.replace("-", ".") + cemix_shift.replace("shift", "S") + cemix_ligne.replace("line", "l") +  numero_palette
        generete_barcode(Num_Palette_complet.replace("_", "").replace("-",""), APP_PATH)

        numero_palette = get_new_palette_number(cursor)
        conn.commit()   
        conn.close()

        return numero_palette, current_date, dash.no_update, dash.no_update, dash.no_update, "", "", "oui", "oui"
    else:
        return dash.no_update, current_date, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


  

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        generate_modal(),
        generate_modal_Parameter(),
        html.Div(id='output')
    ],
)


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8060)
