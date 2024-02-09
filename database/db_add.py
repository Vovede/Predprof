import sqlite3

conn = sqlite3.connect('database/bd1.db')
cursor = conn.cursor()


def add_record(temp):
    cursor.execute(
        f"""
                    INSERT INTO {'s' + temp[0]} (
                                 stname,
                                 year,
                                 month,
                                 day,
                                 hour,
                                 dirwind,
                                 precipit,
                                 temperature,
                                 humidity
                             )
                             VALUES (
                                  {temp[0]},
                                  {temp[1]},
                                  {temp[2]},
                                  {temp[3]},
                                  {temp[4]},
                                  {str(temp[5])},
                                  {str(temp[6])},
                                  {str(temp[7])},
                                  {str(temp[8])}
                             );
        """
    )
    conn.commit()


def add_synaptic_index(temp):
    cursor.execute(
        """
                    INSERT INTO synaptic_index_stations (
                                 sinaptic_index,
                                 name_station,
                                 latitude,
                                 longitude,
                                 height_sea_level,
                                 country
                             )
                             VALUES (
                                 ?, ?, ?, ?, ?, ?
                             );
        """, (
            temp[0],
            temp[1],
            float(temp[2]),
            float(temp[3]),
            int(temp[4]),
            temp[5]
        )
    )
    conn.commit()