import csv
import random

def emulationData():
    # станция, год, месяц, день, час, напр ветра, осадки, темпер-ра, влажность
    data = []
    day_begin = 1
    for i in range(31):
        template = {
                "station": 20046,
                "year": 2024,
                "month": 1,
                "day": day_begin + i,
                "hours": 0,
                "dirwild": random.randint(0, 10),
                "precipitation": random.randint(0, 10),
                "temparature": -10 + random.randint(0, 10),
                "humidity": random.randint(80, 100)
             }
        # print(template)
        data.append(template)
    with open("employee_data.csv", mode="w", newline="", encoding="utf-8") as csv_file:
        fieldnames = ["station", "year", "month", "day", "hours", "dirwild", "precipitation", "temparature", "humidity"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # writer.writeheader()
        for row in data:
            writer.writerow(row)
    return data
