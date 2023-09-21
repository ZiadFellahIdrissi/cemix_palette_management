# drop table if exists Famille;
# drop table if exists Article;
# drop table if exists palette;
# drop table if exists cemix_info;

# CREATE TABLE if not exists Famille (
#                 Id INTEGER PRIMARY KEY,
#                 nom_famille TEXT,
#                 abreviation_famille TEXT
#             );	
	
# CREATE TABLE if not exists Article (
#                 Id INTEGER PRIMARY KEY,
#                 nom_article TEXT,
#                 abreviation_article TEXT,
#                 famille_id INTEGER,
# 				FOREIGN KEY (famille_id) REFERENCES Famille (Id)
#             );	
					
# CREATE TABLE if not exists palette (
#                 Id INTEGER PRIMARY KEY,
#                 date DATETIME,
#                 numero_palette TEXT,
#                 article_id INTEGER,
#                 Commentair TEXT,
#                 nombre_de_sac INTEGER,
#                 poids REAL,
#                 echantillon_4Kg TEXT,
#                 echantillon_10Kg TEXT,
# 				duration_min REAL,
# 				ecart_by_10 REAL,
#                 cemix_main_id INTEGER,
#                 FOREIGN KEY (cemix_main_id) REFERENCES cemix_info(Id),
# 				FOREIGN KEY (article_id) REFERENCES Article(Id)
#             );
			
# CREATE TABLE if not exists cemix_info (
#                 Id INTEGER PRIMARY KEY,
#                 date DATE,
#                 heure TIME,
#                 ligne TEXT,
#                 shift TEXT,
#                 operateur_mix TEXT,
#                 operateur_ensacheuse TEXT,
#                 clarist_m TEXT,
#                 clariste_p TEXT,
#                 aide_magasinier TEXT,
#                 is_terminer INTEGER
#             );			

		
# INSERT INTO Famille (id, nom_famille, abreviation_famille)
# VALUES
#      (1, 'MARTOUBY', 'MAR'),
# 	 (2, 'YAJOURY', 'YAJ');

# INSERT INTO Article (nom_article, abreviation_article, famille_id)
# VALUES
# 	("MARTOUBY MN", "mn", 1),
# 	("MARTOUBY PA", "pa", 1),
# 	("MARTOUBY PX", "px", 1),
# 	("MARTOUBY FN", "fn", 1),
# 	("MARTOUBY P", "p", 1),
# 	("MARTOUBY PX BLANC" , "pxb", 1),
# 	("MARTOUBY FN BLANC" , "fnb", 1),
# 	("MARTOUBY XTRA FINO", "xfn", 1),
# 	("MARTOUBY FN CREME",	"fncRM", 1),
# 	("MARTOUBY FN ROUGE 720", "fnr720", 1),
# 	("MARTOUBY XTRA FINO LB",	"xfnlb", 1),
# 	("MARTOUBY XTRA FINO LG",	"xfnlg", 1),
# 	("MARTOUBY XTRA FINO GRIS 410", "xfngr", 1),
# 	("MARTOUBY PX 590 TEINTE", "px590", 1),
# 	("MARTOUBY PX GRATTE", "pxgra", 1),
# 	("MARTOUBY PX BLANC GRATTE",	"pxbgra", 1),
# 	("MARTOUBY MN LOT", "mnloT", 1),
# 	("Master Batch A", "MSTRA", 1),
# 	("YAJOURY MN", "mn", 2);
	
# -- Insert data into cemix_info table
# INSERT INTO cemix_info (id, date, heure, ligne, shift, operateur_mix, operateur_ensacheuse, clarist_m, clariste_p, aide_magasinier, is_terminer)
# VALUES
#      (1, '2023-09-01', '07:00:00', 'Line A', 'Shift_1', 'Ziad Fellah', 'Karim Mahmoud', 'clarist_m_1', 'clarist_p_1', 'Oussama', 1),
#      (2, '2023-09-01', '15:00:00', 'Line B', 'Shift_2', 'Ziad Fellah', 'Karim Mahmoud', 'clarist_m_1', 'clarist_p_2', 'Reda', 1),
# 	 (3, '2023-09-01', '23:00:00', 'Line C', 'Shift_3', 'Ziad Fellah', 'Karim Mahmoud', 'clarist_m_3', 'clarist_p_1', 'Oussama', 1),
# 	 (4, '2023-09-02', '07:00:00', 'Line A', 'Shift_1', 'Ziad Fellah', 'Karim Mahmoud', 'clarist_m_3', 'clarist_p_3', 'Oussama', 0);

# INSERT INTO palette (date, numero_palette, article_id, Commentair, nombre_de_sac, poids, echantillon_4Kg, echantillon_10Kg, duration_min, ecart_by_10, cemix_main_id)
# VALUES
#      ('2023-09-01 07:15:20', 'P001',  1, "No Comment", 10, 100.5, 'Sample 4Kg A', 'Sample 10Kg A', 15.33, 15.33-10, 1),
#      ('2023-09-01 07:55:26', 'P002',  3, "No Comment", 8, 75.2, 'Sample 4Kg B', 'Sample 10Kg B', 40.1, 40.1-10, 1),
#      ('2023-09-01 09:45:33', 'P003',  1, "No Comment", 10, 100.5, 'Sample 4Kg A', 'Sample 10Kg A', 110.12, 110.12-10, 1),
#      ('2023-09-01 14:40:45', 'P004',  3, "No Comment", 8, 75.2, 'Sample 4Kg B', 'Sample 10Kg B', 295.2, 295.2-10, 1),
#      ('2023-09-01 15:10:13', 'P005',  5, "No Comment", 10, 100.5, 'Sample 4Kg A', 'Sample 10Kg A', 9, 9-10,  2),
#      ('2023-09-01 19:40:45', 'P006',  8, "No Comment", 8, 75.2, 'Sample 4Kg B', 'Sample 10Kg B', 270.53, 270.53-10, 2),
# 	 ('2023-09-01 23:32:16', 'P007',  19, "No Comment", 8, 75.2, 'Sample 4Kg B', 'Sample 10Kg B', 32.27, 32.27-10, 3),
#      ('2023-09-02 02:17:00', 'P008',  7, "No Comment", 10, 100.5, 'Sample 4Kg A', 'Sample 10Kg A', 164.73, 164.73-10, 3),
#      ('2023-09-02 05:55:30', 'P009',  1, "No Comment", 8, 75.2, 'Sample 4Kg B', 'Sample 10Kg B', 218.5, 218.5-10, 3),
# 	 ('2023-09-02 07:13:10', 'P001',  12, "No Comment", 10, 100.5, 'Sample 4Kg A', 'Sample 10Kg A', 13.17, 13.17-10, 4),
#      ('2023-09-02 09:55:48', 'P002',  8, "No Comment", 8, 75.2, 'Sample 4Kg B', 'Sample 10Kg B', 40.1, 40.1-10, 4),
#      ('2023-09-02 13:33:37', 'P003',  9, "No Comment", 10, 100.5, 'Sample 4Kg A', 'Sample 10Kg A', 110.12, 110.12-10, 4);




# CREATE TABLE if not exists Parameter (
# 		 Id INTEGER PRIMARY KEY,
# 		 username TEXT,
# 		 password TEXT, 
# 		 dpt INTEGER
# );	

# INSERT INTO Parameter (id, username, password, dpt)
# VALUES
#     (1, 'karim_mahmoud', 'Dready@077535', 10);

# import sqlite3
# from datetime import datetime, timedelta, time

# # Connect to the SQLite database
# conn = sqlite3.connect('Cemix_database.db')
# cursor = conn.cursor()

# # Define the start and end times for each cycle (7 AM to 7 AM)
# cycle_start = time(7, 0, 0)
# cycle_end = time(7, 0, 0)

# # Get the distinct dates from the 'palette' table
# cursor.execute("SELECT DISTINCT date FROM palette")
# distinct_dates = cursor.fetchall()

# # Loop through each distinct date
# for date_tuple in distinct_dates:
#     date_str = date_tuple[0]
#     date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()

#     start_time = datetime.combine(date_obj, cycle_start)
#     end_time = start_time + timedelta(days=1)
    
#     # Get the maximum 'numero palette' for the current cycle
#     cursor.execute("SELECT MAX(CAST(substr(numero_palette, 2) AS INTEGER)) FROM palette WHERE date BETWEEN ? AND ?", (start_time, end_time))
#     max_palette_num = cursor.fetchone()[0]
    
#     if max_palette_num is None:
#         max_palette_num = 0
    
#     # Get the last 'numero palette' for the current cycle
#     cursor.execute("SELECT numero_palette FROM palette WHERE date BETWEEN ? AND ? ORDER BY date DESC LIMIT 1", (start_time, end_time))
#     last_palette_num = cursor.fetchone()[0]
    
#     # Calculate the next 'numero palette'
#     next_palette_num = (max_palette_num % 1000) + 1
    
#     # Check if it's time to reset
#     if datetime.now() >= end_time and last_palette_num == f'P{next_palette_num - 1:03d}':
#         next_palette_num = 1
    
#     next_palette_num_str = f'P{next_palette_num:03d}'
    
    
# print(next_palette_num_str)
# # Close the database connection
# conn.close()






import sqlite3
import datetime 

def get_new_palette_number(conn):

     cursor = conn.cursor()

     # Get the last 'numero_palette' value and the creation date of the last palette
     cursor.execute("""
                    SELECT numero_palette, date
                    FROM palette
                    WHERE strftime('%H:%M', date) >= '07:00'
                    AND date >= datetime('now', '-1 day')
                    AND date <= datetime('now')
                    ORDER BY date DESC LIMIT 1;
                    """)
     last_palette = cursor.fetchone()
     print(last_palette)
     last_numero_palette, last_creation_date = last_palette if last_palette else ('P0000', None)

     # Get the current date and time
     current_datetime = datetime.datetime.now()

     # Calculate the cycle start and end times (from 7 AM to 7 AM)
     cycle_start = current_datetime.replace(hour=7, minute=0, second=0, microsecond=0)
     if current_datetime.hour < 7:
          cycle_start -= datetime.timedelta(days=1)
     cycle_end = cycle_start + datetime.timedelta(days=1)

     # Determine if we're within the current cycle
     print("cycle_start:  ", cycle_start,"--- current_datetime:  ", current_datetime,"--- cycle_end:  ",cycle_end, "--- last_numero_palette:   ", last_numero_palette)
     within_current_cycle = cycle_start <= current_datetime < cycle_end

     # Increment 'numero_palette' if within the current cycle
     print(within_current_cycle)
     if within_current_cycle:
          if last_numero_palette == 'P999':
               new_numero_palette = 'P0001'
          else:
               new_numero_palette = f'P{int(last_numero_palette[1:]) + 1:04}'
     else:
          new_numero_palette = 'P0001'

     # Close the database connection
     conn.close()

     return new_numero_palette



conn = sqlite3.connect("Cemix_database_test.db")
print(get_new_palette_number(conn))





("MARTOUBY MN", "mn", 1),
("MARTOUBY PA", "pa", 1),
("MARTOUBY PX", "px", 1),
("MARTOUBY FN", "fn", 1),
("MARTOUBY P", "p", 1),
("MARTOUBY PX BLANC" , "pxb", 1),
("MARTOUBY FN BLANC" , "fnb", 1),
("MARTOUBY XTRA FINO", "xfn", 1),
("MARTOUBY FN CREME",	"fncRM", 1),
("MARTOUBY FN ROUGE 720", "fnr720", 1),
("MARTOUBY XTRA FINO LB",	"xfnlb", 1),
("MARTOUBY XTRA FINO LG",	"xfnlg", 1),
("MARTOUBY XTRA FINO GRIS 410", "xfngr", 1),
("MARTOUBY PX 590 TEINTE", "px590", 1),
("MARTOUBY PX GRATTE", "pxgra", 1),
("MARTOUBY PX BLANC GRATTE",	"pxbgra", 1),
("MARTOUBY MN LOT", "mnloT", 1),
("Master Batch A", "MSTRA", 1),
("YAJOURY MN", "mn", 2);






def generate_modal_Parameter():
    return html.Div(
        id="markdown_Parameter",
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
                            children = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + 'X',
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),

                    html.Div([
                        html.H2("PALETTE N°", style={'text-align': 'center', "font-family": "Arial, sans-serif", "font-size": "32px", "margin-bottom": "3px"}),
                        
                        html.Div([
                            dcc.Input(
                                id = 'nb_sac_input',
                                type='number',
                                placeholder='NOMBRE DE SAC',
                                style={"width": "100%", "height": "50px", "background-color": "#000000", "color": "#ffffff", 'font-weight': 'bold', 'text-align': 'center', 'margin-right': '15px'}
                            ),
                            dcc.Input(
                                id = 'Palette_comment',
                                type='text',
                                placeholder='Commentaire',
                                style={"width": "100%", "height": "50px",'font-weight': 'bold', 'text-align': 'center', "background-color": "#000000", "color": "#ffffff"}
                            ),
                        ], style={'display': 'flex', 'width': '100%', "margin-bottom": "2px"}),
                        
                        html.Br(),
                        
                        dcc.Input(
                            id = 'Poid_palette_input',
                            type='text',
                            placeholder='POIDS PALETTE ...',
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
                        
                        
                    ], style={"width": "86%", "margin": "10px auto", 'textAlign': 'center'})

                ],
            )
        ),
    )

@app.callback(
    Output("markdown_Parameter", "style"),
    [
        Input("start-shift", "n_clicks"),
        Input("closeButton", "n_clicks"),
    ],
    prevent_initial_call= True


)
def update_click_output(suivant_click):
    ctx = dash.callback_context

    if ctx.triggered and suivant_click > 0:

        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "start-shift" :
            
            return {"display": "block"}

    return {"display": "none"}







                    html.Div([
                        html.H2("PALETTE N°", style={'text-align': 'center', "font-family": "Arial, sans-serif", "font-size": "32px", "margin-bottom": "3px"}),
                        html.H1(id="number_of_palette", children=str(numero_palette), style={'text-align': 'center', "font-family": "Georgia, serif", "font-size": "48px"}),
                        
                        
                    ], style={"width": "86%", "margin": "10px auto", 'textAlign': 'center'})