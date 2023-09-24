import os
import io
import pathlib
import dash
from dash import Dash, html, dcc, callback
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd 
import sqlite3
import random
import datetime
import base64
from models.cemix_to_excel import cemix_to_excel
from models.cemix_Synthese_to_excel import cemix_Synthese_to_excel
from functions.functions import minutes_to_hh_mm, fetch_famille_options, get_input_options, get_new_palette_number, get_shifts

G__Ligne_name = "Ligne 4"
G__Ligne_label = "line_4"
G_Shift_Already_started = 0

dash.register_page(__name__, name=G__Ligne_name)
# Varibales
APP_PATH = str(pathlib.Path(__file__).parent.parent.resolve()) 
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


df_inputs = pd.read_excel(file_path_excel_parameter)



def generate_modal():
    conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
    cursor = conn.cursor()
    numero_palette = get_new_palette_number(cursor, G__Ligne_label)
    conn.close()

    return html.Div(
        id="markdown_ligne4",
        className="modal",
        children=(
            html.Div(
                id="markdown-container-ligne4",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=
                        html.Button(
                            id="Time_Feedback-ligne4",
                            children = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),

                    html.Div([
                        html.H2("PALETTE N°", style={'text-align': 'center', "font-family": "Arial, sans-serif", "font-size": "32px", "margin-bottom": "3px"}),
                        html.H1(id="number_of_palette-ligne4", children=str(numero_palette), style={'text-align': 'center', "font-family": "Georgia, serif", "font-size": "48px"}),
                        html.Div([
                            
                            dcc.Dropdown(
                                id = 'product_family_input-ligne4',
                                options=fetch_famille_options(),
                                value = None,
                                placeholder='Famille',
                                style={"width": "100%", "height": "50px", 'text-align':'center', 'margin-right': '15px', 'font-weight': 'bold'}
                            ),
                            
                            dcc.Dropdown(
                                id = 'article_input-ligne4',
                                options=[],
                                value = None,
                                placeholder='Article',
                                style={"width": "100%", "height": "50px", 'text-align': 'center', 'font-weight': 'bold'}
                            ),
                            
                        ], style={'display': 'flex', 'width': '100%', "margin-top": "3px", "margin-bottom": "5px"}),
                        
                        # html.Br(),

                        html.Div([
                            dcc.Input(
                                id = 'nb_sac_input-ligne4',
                                type='number',
                                placeholder='NOMBRE DE SAC',
                                autoComplete='off',
                                value=None,
                                style={"width": "97.5%", "height": "50px", "background-color": "#000000", "color": "#ffffff", 'font-weight': 'bold', 'text-align': 'center', 'margin-right': '15px'}
                            ),
                            dcc.Dropdown(
                                id='Palette_comment-ligne4',
                                options = get_input_options(df_inputs, "Commentaire"),
                                value=None,
                                placeholder='Commentaire',
                                style={"width": "100%", "height": "50px", 'text-align': 'center', 'font-weight': 'bold'}
                            ),

                        ], style={'display': 'flex', 'width': '100%', "margin-bottom": "2px"}),
                        
                        html.Br(),
                        
                        dcc.Input(
                            id = 'Poid_palette_input-ligne4',
                            type='text',
                            placeholder='POIDS PALETTE ...',
                            autoComplete='off',
                            style={'font-size': '24px', 'font-weight': 'bold','width': '100%', 'height': '60px', 'text-align': 'center', "margin-bottom": "10px"}
                        ),
                        html.Div([
                            html.Label('ECHANTILLON 4 KG', style = {"width": "100%", 'font-size': '30px', "margin-right": "50px"}),
                            dcc.RadioItems(
                                id = 'echantillon_4kg_input-ligne4',
                                options=[
                                    {'label': 'Oui', 'value': 'Oui'},
                                    {'label': 'Non', 'value': 'Non'}
                                ],
                                value=None,
                                labelStyle={'display': 'flex', 'font-size': '28px'},
                                style = {"width": "100%"}
                            ),
                            html.Label('ECHANTILLON 10 KG', style = {"width": "100%", 'font-size': '30px', "margin-right": "50px"}),
                            dcc.RadioItems(
                                id = 'echantillon_10kg_input-ligne4',
                                options=[
                                    {'label': 'Oui', 'value': 'Oui'},
                                    {'label': 'Non', 'value': 'Non'}
                                ],
                                value=None,
                                labelStyle={'display': 'flex', 'font-size': '28px'},
                                style = {"width": "100%"}
                            
                            ),
                            
                        ], style={'display': 'flex', 'width': '100%'}),

                        html.Div([
                            html.Button(
                                id='Suivant_button-ligne4',
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
                                id='Terminer-Button-ligne4',
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
        ],
    ),
    
    html.Div(
        id="app-container",

        children = [
            html.H4(
                id="Line_choisen", 
                children="Vous avez choisi la "+ G__Ligne_name + " .", 
                style={
                    'text-align': 'center', 
                    'margin-top': '1%', 
                    'margin-buttom': '0%',
                    "font-family": "Georgia, serif"}
            ),
            dcc.Dropdown(
                id='ligne-input-ligne4',
                options=[
                            {'label': G__Ligne_name , 'value': G__Ligne_label},

                        ],
                value=G__Ligne_label,
                style={'margin': '6px auto','margin-top': '20px', 'width': '80%', 'text-align':'center'}
            ),
            dcc.Dropdown(
                id='shift-input-ligne4',
                options=get_shifts(G__Ligne_label),
                placeholder = "Shift",
                value=None,
                style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'opacity': '1', 'font-weight':'bold'}
            ),
            dcc.Dropdown(
                id='operateur_mix-input-ligne4',
                options=get_input_options(df_inputs, "operateur_mix"),
                value=None,
                placeholder="OPERATEUR MIX",
                style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'color':'white', 'opacity': '1', 'font-weight':'bold'}
            ),
            dcc.Dropdown(
                id='operateur_ensacheus-input-ligne4',
                options=get_input_options(df_inputs, "operateur_ensacheuse"),
                value = None,
                placeholder="OPERATEUR ENSACHEUS",
                style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'color':'white', 'opacity': '1', 'font-weight':'bold'}
            ),
            dcc.Dropdown(
                id='clarsite_m-input-ligne4',
                options=get_input_options(df_inputs, "clariste_m"),
                value = None,
                placeholder="CLARISTE M",
                style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'color':'white', 'opacity': '1', 'font-weight':'bold'}
            ),
            dcc.Dropdown(
                id='clarsite_p-input-ligne4',
                options=get_input_options(df_inputs, "clariste_p"),
                value = None,
                placeholder="CLARISTE P",
                style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'color':'white', 'opacity': '1', 'font-weight':'bold'}
            ),
            dcc.Dropdown(
                id='aide_magasinier-input-ligne4',
                options=get_input_options(df_inputs, "aide_magasinier"),
                value = None,
                placeholder="AIDE MAGASINIER" ,
                style={'margin': '6px auto', 'width': '80%', 'text-align':'center', 'color':'white', 'opacity': '1', 'font-weight':'bold'}
            ),
            html.Button(
                id='start-shift-ligne4',
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
            html.Div(
                id='Feedback-Demare-ligne4',
                children="ziad fellah",
                style={
                    'margin-top':'2%',
                    'display':'none'
                }),
            html.Div(id='hidden-div-ligne4', style={'display': 'none'}),
        ], style={"width": "95%", "margin": "10px auto",  "padding": "2%", 'textAlign': 'center'}
    ),
    generate_modal(),

])



@callback(
    Output("markdown_ligne4", "style"),
    Output("Feedback-Demare-ligne4", "children"),
    Output("Feedback-Demare-ligne4", "style"),
    Output("shift-input-ligne4", "options"),
    [
        Input("start-shift-ligne4", "n_clicks"),
        Input("Terminer-Button-ligne4", "n_clicks"),
    ],
    [
        State("ligne-input-ligne4", "value"),
        State("shift-input-ligne4", "value"),
        State("operateur_mix-input-ligne4", "value"),
        State("operateur_ensacheus-input-ligne4", "value"),
        State("clarsite_m-input-ligne4", "value"),
        State("clarsite_p-input-ligne4", "value"),
        State("aide_magasinier-input-ligne4", "value"),
        State("Poid_palette_input-ligne4", "value"),
        State("echantillon_4kg_input-ligne4", "value"),
        State("echantillon_10kg_input-ligne4", "value"),
    ],
    prevent_initial_call= True,
)
def update_click_output(suivant_click, terminer_click, ligne, shift, operateur_mix, operateur_ensacheus, clarsite_m, clarsite_p, aide_magasinier, Poid_palette, echantillon_4kg, echantillon_10kg):
    ctx = dash.callback_context
    global G_Shift_Already_started
    if ctx.triggered and suivant_click > 0:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "start-shift-ligne4" :
            print(shift, operateur_mix, operateur_ensacheus, clarsite_m, clarsite_p,aide_magasinier)
            if shift != None and operateur_mix != None and operateur_ensacheus != None and clarsite_m != None and clarsite_p != None and aide_magasinier != None:
                print(G_Shift_Already_started)
                if G_Shift_Already_started == 0:
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
                    folder_this_day = os.path.join(APP_PATH, "Journal Shifts", "Jour_" + folder_this_day_format.strftime("%d_%m_%Y"), G__Ligne_name)

                    if not os.path.exists(folder_this_day):
                        os.makedirs(folder_this_day)

                    if not os.path.exists(os.path.join(folder_this_day, "Jour")):
                        os.mkdir(os.path.join(folder_this_day, "Jour"))

                    day_before = datetime.datetime.now() - datetime.timedelta(hours=6.5) - datetime.timedelta(hours=24)
                    format_shifts_all_day = "Reporting_journalier_ensachage__" + day_before.strftime("%d_%m_%Y") + ".xlsx"
                    path_shifts_all_day = os.path.join(folder_this_day, "Jour", format_shifts_all_day)

                    try:
                        if not os.path.exists(path_shifts_all_day):
                            data_header_allDay = {
                                'Variable': [
                                    'Date', 'Heure', 'Durée de palette Theorique', 'Objectif PALETTE theorique',
                                    'TOTAL SAC THEORIQUE', 'TOTAL POID', 'Total d\'heure travail',
                                    'durée total d\'arret', 'Total palette', 'total sac'
                                    ],
                                'Value': None
                            }

                            query = f"""
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
                                where DATE(c.date) = DATE('now', '-1 day') and c.ligne = '{G__Ligne_label}' """

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
                                            header_name = "Reporting Journalier D'ensachage",
                                            filename = path_shifts_all_day, 
                                            ishift = False, 
                                            size = 16.5, 
                                            num_rows=2 
                                        )

                            agg_functions = {
                                'Palatte_duration' : 'sum',
                                'Numero de Palette': 'count', 
                                'Nombre de Sac': 'sum',
                                'Ecart': lambda x: x[x > 0].sum(),
                                "Error Commentair": lambda x: '___'.join(x[(x != "") | (x != None)]),
                                'Echantillon 10Kg': lambda x: x[x == "Oui"].count(),
                                'Echantillon 4Kg': lambda x: x[x == "Oui"].count(),
                                'Poids' : "sum",
                            }

                            df_synthes = df_all_day.groupby(["Shift"]).agg(agg_functions).reset_index()

                            df_synthes.rename(columns = {
                                                        "Palatte_duration": "Tottal Heure Travaile", 
                                                        "Numero de Palette": "Nombre De Palette Produite",
                                                        "Ecart" : "Nombre d'heure d'arret", 
                                                        "Nombre de Sac": "Nombre Total SAC", 
                                                        "Poids" : "Tottal Poids", 
                                                        "Echantillon 10Kg": "Tottal Echantillon 10Kg", 
                                                        "Echantillon 4Kg": "Tottal Echantillon 4Kg",
                                                        "Error Commentair": "Cause"
                                                        }, 
                                            inplace = True 
                                        )

                            df_synthes["NBR SAC/PALETTE"] = df_synthes["Nombre Total SAC"] / df_synthes["Nombre De Palette Produite"]
                            df_synthes["Poid Tottal/PALETTE"] = df_synthes["Tottal Poids"] / df_synthes["Nombre De Palette Produite"]
                            df_synthes["OPT"] = round( df_synthes["Tottal Heure Travaile"] / dpt_golabl, 2 )
                            df_synthes["ECART PALETTE"] = df_synthes["OPT"] - df_synthes["Nombre De Palette Produite"]
                            df_synthes["OTS"] = round(df_synthes["OPT"]*64, 2)

                            df_synthes = df_synthes[["Shift", "Tottal Heure Travaile", "Nombre De Palette Produite", "OPT", "ECART PALETTE", 
                                                    "Nombre d'heure d'arret", "Cause", "Nombre Total SAC", "OTS", "Tottal Poids", 
                                                    "NBR SAC/PALETTE", "Poid Tottal/PALETTE", "Tottal Echantillon 10Kg", "Tottal Echantillon 4Kg"]]




                            format_Synthese = "Synthese_de_production__" + day_before.strftime("%d_%m_%Y") + ".xlsx"
                            path_Synthese = os.path.join(folder_this_day, "Jour", format_Synthese)
                            cemix_Synthese_to_excel(df_synthes, path_Synthese)

                    except:
                        print("This could be the first day, let's just skip it !")

                    conn.close()
                    
                    return {"display": "block"}, "", {}, get_shifts(G__Ligne_label)
                else:
                    G_Shift_Already_started = 0
                    return {"display": "block"}, "", {}, get_shifts(G__Ligne_label)
            else:
                colors_list = ["#98260E", "#FF0000", "#770000", "#FF6C6E", "#C9005B"]
                style={
                    "color" : random.choice(colors_list),
                    "font-weight": "Bold",
                    "font-size": "25px"
                }
                Text_Error = "Remplissez les champs pour demare un Shift"
                return dash.no_update, Text_Error, style, get_shifts(G__Ligne_label),

        if prop_id == "Terminer-Button-ligne4" :
            if (Poid_palette == None or Poid_palette == "") and echantillon_4kg == None and echantillon_10kg == None:
                conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
                data_header_shift = {
                    'Variable': ['OPERATEUR MIX', 'OPERATEUR ENSACH', 'CLARIST P', 'CLARIST M', 'AIDE MAGASIGNIER', 'Date', 'Heure', 'Durée de palette Theorique', 'Objectif PALETTE theorique', 'TOTAL SAC THEORIQUE', 'TOTAL POID', 'Total d\'heure travail', "durée total d'arret", 'Total palette', 'total sac'],
                    'Value': None
                }
                query = f"""
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
                    where c.is_terminer = 0 and c.ligne = '{G__Ligne_label}' """
                
                df_shift = pd.read_sql_query(query, conn)

                cursor = conn.cursor()
                cursor.execute("SELECT c.id FROM cemix_info c WHERE c.is_terminer = ? and c.ligne = ?", (0, str(G__Ligne_label)))
                result = cursor.fetchone()  
                cemix_id = result[0]

                cursor.execute("UPDATE cemix_info SET is_terminer = ? WHERE id = ? and ligne = ?", (1, cemix_id, str(G__Ligne_label),))

                if df_shift.shape[0] > 0:
                    folder_this_day_format = datetime.datetime.now().strftime("%d_%m_%Y")
                    folder_this_day = os.path.join(APP_PATH, "Journal Shifts", "Jour_" + folder_this_day_format, G__Ligne_name)

                    if not os.path.exists(folder_this_day):
                        os.makedirs(folder_this_day)
                    
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
                                    num_rows = 3 
                    )     
            else:
                colors_list = ["#98260E", "#FF0000", "#770000", "#FF6C6E", "#C9005B"]
                style__={
                    "color" : random.choice(colors_list),
                    "font-weight": "Bold",
                    "font-size": "25px"
                }
                Text_Error__ = "cliquez sur le bouton suivant puis sur le bouton < Terminé >. !"
                return dash.no_update, Text_Error__, style__, get_shifts(G__Ligne_label)
                
            conn.commit()
            conn.close()

    return {"display": "none"}, '', {}, get_shifts(G__Ligne_label)


@callback(
    [
        Output("number_of_palette-ligne4", "children"),
        Output("product_family_input-ligne4", "value"),
        Output("article_input-ligne4", "value"),
        Output("nb_sac_input-ligne4", "value"),
        Output("Palette_comment-ligne4", "value"),
        Output("Poid_palette_input-ligne4", "value"),
        Output("echantillon_4kg_input-ligne4", "value"),
        Output("echantillon_10kg_input-ligne4", "value"),
        Output("Time_Feedback-ligne4", "children"),
        Output("Time_Feedback-ligne4", "style"),
    ],
    [Input("Suivant_button-ligne4", "n_clicks")],
    [
        State("product_family_input-ligne4", "value"),
        State("article_input-ligne4", "value"),
        State("nb_sac_input-ligne4", "value"),
        State("Palette_comment-ligne4", "value"),
        State("Poid_palette_input-ligne4", "value"),
        State("echantillon_4kg_input-ligne4", "value"),
        State("echantillon_10kg_input-ligne4", "value"),
    ],
)
def Suivant(Suivant_button, product_family, article, nb_sac, Palette_comment, Poid_palette, echantillon_4kg, echantillon_10kg):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
    cursor = conn.cursor()
    numero_palette = get_new_palette_number(cursor, G__Ligne_label)
    if Suivant_button > 0:
        if product_family != None and article != None and nb_sac != None and Poid_palette != None and echantillon_4kg != None and echantillon_10kg != None:
            cursor.execute("SELECT c.id, c.date, c.heure, c.shift, c.ligne FROM cemix_info c WHERE c.is_terminer = ? and c.ligne = ?", (0, str(G__Ligne_label)))
            result = cursor.fetchone()
            cemix_id = result[0]
            cemix_date = result[1]
            cemix_heure = result[2]
            cemix_shift = result[3]
            cemix_ligne = result[4]
            
            numero_palette = get_new_palette_number(cursor, G__Ligne_label)
            
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
            # generete_barcode(Num_Palette_complet.replace("_", "").replace("-",""), APP_PATH)

            numero_palette = get_new_palette_number(cursor, G__Ligne_label)
            conn.commit()   
            conn.close()

            return numero_palette, dash.no_update, dash.no_update, dash.no_update, "", None, None, None, current_date, {}
        
        else:
            colors_list = ["#98260E", "#FF0000", "#770000", "#FF6C6E"]
            style={
            "color" : random.choice(colors_list),
            "font-weight": "Bold",
            "font-size": "25px"
        }
        Text_Error = "Remplissez les champs pour Passe vers la palette suivante"

        return numero_palette, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, Text_Error, style
    
    else:
        return numero_palette,  dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, current_date, {}


@callback(
    Output("start-shift-ligne4", "n_clicks"),
    Output("shift-input-ligne4", "value"),
    Output("operateur_mix-input-ligne4", "value"),
    Output("operateur_ensacheus-input-ligne4", "value"),
    Output("clarsite_m-input-ligne4", "value"),
    Output("clarsite_p-input-ligne4", "value"),
    Output("aide_magasinier-input-ligne4", "value"),
    Input("hidden-div-ligne4", "children"),
)
def check_demare_already_clicked(click):
    global G_Shift_Already_started
    conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
    cursor = conn.cursor()
    cursor.execute(f"select * from cemix_info where is_terminer = ? and ligne = '{G__Ligne_label}'", (0,))
    result = cursor.fetchone()
    if result:
        print("Resultat__: ",result)
        G_Shift_Already_started = 1
        return 1, result[4], result[5], result[6], result[7], result[8], result[9] 
    else:
        print("Nothing")
        G_Shift_Already_started = 0
        print("G_Shift_Already_started= ", G_Shift_Already_started)
        return 0, None, None, None, None, None, None



@callback(
    Output('article_input-ligne4', 'options'),
    Input('product_family_input-ligne4', 'value')
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