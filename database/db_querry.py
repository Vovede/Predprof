import sqlite3

conn = sqlite3.connect('../UI_scripts/bd.db')
cursor = conn.cursor()


def queryStation(sinaptic_index):
    cursor.execute(
        """SELECT * FROM synaptic_index_stations
            WHERE sinaptic_index=?;""",
        (sinaptic_index,)
    )
    res = cursor.fetchall()
    print(res)
    return res


def coordinatesStation(sinaptic_index):
    cursor.execute(
        """SELECT latitude, longitude FROM synaptic_index_stations
            WHERE sinaptic_index=?;""",
        (sinaptic_index,)
    )
    res = cursor.fetchone()
    print(res)
    return res

# print(queryStation(str(20049)))
