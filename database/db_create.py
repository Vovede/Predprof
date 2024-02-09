import sqlite3


def create_table_station_bd(synapticIndexStation):
    conn = sqlite3.connect('../UI_scripts/bd.db')
    cursor = conn.cursor()
    # станция, год, месяц, день, час, напр ветра, осадки, темпер-ра, влажность
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {'s' + synapticIndexStation}(
        idrecord INTEGER PRIMARY KEY UNIQUE,
        stname TEXT,
        year INT,
        month INT,
        day INT,
        hour INT,
        dirwind REAL,
        precipit REAL,
        temperature REAL,
        humidity REAL);"""
        )
    conn.commit()


create_table_station_bd(f's{2000}')
