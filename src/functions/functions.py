import sqlite3
import datetime
import os
import pathlib
import pandas as pd

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
database_name = "../Cemix_database_test.db"

# here is the list of the function exists in this script
# ==== minutes_to_hh_mm
# fetch_famille_options
# get_input_options
# get_new_palette_number

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




def get_new_palette_number(cursor, ligne):

    cursor.execute(f"""
                        SELECT p.numero_palette, p.date
                        FROM palette p
                        join cemix_info c on c.id = p.cemix_main_id
                        WHERE 
                        ((
                        strftime('%H:%M:%S', 'now') >= '07:00:00' 
                        AND p.date BETWEEN 
                                        datetime('now', 'start of day', '-0 day', '07:00:00') AND 
                                        datetime('now', 'start of day','+1 day', '07:00:00')
                        )
                        OR
                        (
                        strftime('%H:%M:%S', 'now') < '07:00:00' 
                        AND p.date BETWEEN 
                                            datetime('now', 'start of day', '-1 day', '07:00:00') AND
                                            datetime('now', 'start of day', '+0 day', '07:00:00')
                        ))
                        and 
                        c.ligne = '{ligne}'
                        ORDER BY p.date DESC
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




def get_shifts(ligne):
    conn = sqlite3.connect(os.path.join(APP_PATH, database_name))
    query = f"""
                SELECT p.numero_palette, p.date, c.shift
                FROM palette p
                join cemix_info c on c.id = p.cemix_main_id
                WHERE 
                ((
                strftime('%H:%M:%S', 'now') >= '07:00:00' 
                AND p.date BETWEEN 
                                datetime('now', 'start of day', '-0 day', '07:00:00') AND 
                                datetime('now', 'start of day','+1 day', '07:00:00')
                )
                OR
                (
                strftime('%H:%M:%S', 'now') < '07:00:00' 
                AND p.date BETWEEN 
                                    datetime('now', 'start of day', '-1 day', '07:00:00') AND
                                    datetime('now', 'start of day', '+0 day', '07:00:00')
                ))
                and 
                c.ligne = '{ligne}' """
    
    df = pd.read_sql_query(query, conn)

    list_shifts = ["shift-1", "shift-2", "shift-3", "shift-4", "shift-5", "shift-6"]
    list_shifts_used = list(set(df["shift"])) 

    shift_allowed = [item for item in list_shifts if item not in list_shifts_used]
    conn.close()

    shift_allowed_html = [{'label': shift.replace("s", "S").replace("-", " "), 'value': shift} for shift in shift_allowed]
    return shift_allowed_html
    
