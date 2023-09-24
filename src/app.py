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
database_name = "Cemix_database_test.db"
file_path_excel_parameter = os.path.join(APP_PATH, 'Parametres/Cemix_input_parametre.xlsx')
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
