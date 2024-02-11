import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
import db_querry
import readFile
from winPush import WindowPush
from emulation import emulationData
from ml import modelML
from get_current_meteo_situation import meteo_data

conn = sqlite3.connect('UI_scripts/bd.db')
cursor = conn.cursor()

class Monitoringiop(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)

        self.totalData = {}  # Данные всех добавленных метеостанций
        self.data = []  # Данные по текущей метеостанции
        self.listStations = set()
        self.selectedItemListWidget = None
        self.time_start = []
        self.time_end = []

        self.navTab = {
            'Загрузка данных': [self.btnDownloadTab.clicked.connect(self.navigate), 1],
            'Визуализация данных': [self.btnVisualTab.clicked.connect(self.navigate), 2],
            'Анализ данных': [self.btnAnalizeTab.clicked.connect(self.navigate), 3],
            'Прогноз': [self.btnPredictTab.clicked.connect(self.navigate), 4],
            'Мониторинг': [self.btnMonitoringTab.clicked.connect(self.navigate), 5],
            # 'Эмуляция': [self.btnEmulation.clicked.connect(self.navigate), None]
        }

        self.downloadFileData.clicked.connect(self.download)

        self.btnEmulation.clicked.connect(self.emulationData)

        self.homeBtnDowloadTab.clicked.connect(self.homeGo)
        self.homeBtnVisualTab.clicked.connect(self.homeGo)
        self.homeBtnAnalisTab.clicked.connect(self.homeGo)
        self.homeBtnPredict.clicked.connect(self.homeGo)
        self.homeBtnMonitoringtab.clicked.connect(self.homeGo)

        self.pushBtnCheckboxesClear.clicked.connect(self.clearCheckBoxes)
        self.clearBtnGraphView.clicked.connect(self.clear_graph)
        self.visualizationBtn.clicked.connect(self.visualization)

        self.btnUpdateMonitoring.clicked.connect(self.loadTableMonitoringData)



    def download(self):
        # Загрузка данных из файла и запись в таблицу QTableWidgetItem
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        # print(fname)
        try:
            self.data = readFile.readDataFile(fname)
            if self.data[0][0] not in self.totalData.keys():
                syn_station = ''.join([symb for symb in self.data[0][0] if symb.isdigit()])
                self.listStations.add(syn_station)
                # print(self.data)
                self.totalData[syn_station] = self.data

                self.tableWidget.setColumnCount(len(self.data[0]))
                self.tableWidget.setHorizontalHeaderLabels(
                    ['станция', 'год', 'месяц', 'день', 'час', 'направление ветра', 'осадки', 'температура',
                     'влажность']
                )
                self.tableWidget.setRowCount(0)
                for i in range(len(self.data[:int(self.spinBoxCountLineData.text())])):
                    self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

                    for j in range(len(self.data[i])):
                        # print(self.data[i], len(self.data[i]))
                        # Отрисовка содержимого QTableWidgetItem
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))

                self.tableWidget.resizeColumnsToContents()
                self.labelStatusDownloadData.setText(f'Статус: Данные загружены. Всего {len(self.data)} записей.')
                self.pushUp('Данные загружены')
            else:
                print('Повторка!')
                self.labelStatusDownloadData.setText(f'Статус: Эти данные уже были загружены.')
                self.pushUp('Отмена загрузки')
        except Exception as error:
            self.labelStatusDownloadData.setText(f'Статус: Невозможно загрузить данные. {error}')
            self.pushUp('Ошибка загрузки')
            print(error)

        # Заполнение listWidgetStationMeteo
        for item in self.listStations:
            # print(item)
            synaptic_index_station = db_querry.queryStation(str(item))
            # print(synaptic_index_station)
            item = '\t'.join(map(str, synaptic_index_station[0][1:]))
            items = [str(self.listWidgetStationMeteo.item(i).text()) for i in
                     range(self.listWidgetStationMeteo.count())]
            # print(items)
            if item not in items:
                self.listWidgetStationMeteo.addItem(item)

    def loadTableMonitoringData(self):
        # Загрузка метеоданных и запись в таблицу QTableWidgetItem
        try:
            self.labelSourceMeteoData.setText('Источник: open-meteo.com')
            print(self.selectedItemListWidget)
            infoStation = self.selectedItemListWidget[0]
            self.labelCurrentStationMonitoring.setText(f'Текущая метеоситуация: {" ".join(infoStation.split())}')
            station = db_querry.queryStation(infoStation.split()[0])
            lat, long = station[0][3], station[0][4]
            print(f"longitude: {lat}, latitude: {long}")
            paramsPrognose = {
                "latitude": lat,
                "longitude": long,
                "hourly": ["temperature_2m", "relative_humidity_2m", "pressure_msl"],
                "past_days": 92,
                "forecast_days": 1
            }
            paramsCurrent = {
                "latitude": lat,
                "longitude": long,
                "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "precipitation",
                            "rain",
                            "showers", "snowfall", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure",
                            "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
                "wind_speed_unit": "ms",
                "timezone": "Europe/Moscow",
                "forecast_days": 1
            }
            data = meteo_data(lat, long, params=paramsCurrent)
            dataPrognose = meteo_data(lat, long, params=paramsPrognose)
            predict = modelML(dataPrognose)
            print(predict)
            self.textEditPredict.setText(predict)
            # print(dataPrognose)
            # print(data)

            self.tableWidgetMonitoring.setColumnCount(2)
            self.tableWidgetMonitoring.setHorizontalHeaderLabels(
                ['Параметр', 'Значение']
            )
            self.tableWidgetMonitoring.setRowCount(0)
            for i in range(len(data)):
                self.tableWidgetMonitoring.setRowCount(self.tableWidgetMonitoring.rowCount() + 1)
                for j in range(len(data[i])):
                    # Отрисовка содержимого QTableWidgetItem
                    self.tableWidgetMonitoring.setItem(i, j, QTableWidgetItem(str(data[i][j])))

            self.tableWidgetMonitoring.resizeColumnsToContents()
            print(QTableWidget)

            self.pushUp('Данные загружены')
        except Exception as error:
            print(error)
            self.pushUp('Ошибка мониторинга')


    # Визуализация
    def visualization(self):
        self.graphicsView.clear()

        self.selectedItemListWidget = [x.text() for x in self.listWidgetStationMeteo.selectedItems()]
        print(self.listWidgetStationMeteo.selectedItems())

        beginDataViz = self.calendarWidget.selectedDate()
        endDataViz = self.calendarWidget_2.selectedDate()

        tempData = []
        for item in self.data:
            if int(beginDataViz.year()) <= int(item[1]) <= int(endDataViz.year()):
                if int(beginDataViz.month()) <= int(item[2]) <= int(endDataViz.month()):
                    if int(beginDataViz.day()) <= int(item[3]) <= int(endDataViz.day()):
                        tempData.append(item)


        # Выбор параметров в чекбоксах и отрисовка графика
        lengthTempData = range(len(tempData))
        if self.checkBoxHumidity.isChecked():  # Влажность
            coordinates = (lengthTempData, [int(i[-1]) for i in tempData])
            self.graphicsView.plot(coordinates[0], coordinates[1], pen=('g'))
            self.graphicsView_2.plot(coordinates[0], coordinates[1])
            self.pushUp('График визуализирован')

        if self.checkBoxPrecipitation.isChecked():  # Осадки
            coordinates = (lengthTempData, [int(i[-3]) for i in tempData])
            self.graphicsView.plot(coordinates[0], coordinates[1], pen=('b'))
            self.graphicsView_3.plot(coordinates[0], coordinates[1])
            self.pushUp('График визуализирован')

        if self.checkBoxDirectionWind.isChecked():  # Направление ветра
            coordinates = (lengthTempData, [int(i[-4]) for i in tempData])
            self.graphicsView.plot(coordinates[0], coordinates[1], pen=('y'))
            self.graphicsView_4.plot(coordinates[0], coordinates[1])
            self.pushUp('График визуализирован')

        if self.checkBoxTemperature.isChecked():  # Температура
            coordinates = (lengthTempData, [int(i[-2]) for i in tempData])
            self.graphicsView.plot(coordinates[0], coordinates[1], pen=('r'))
            self.graphicsView_6.plot(coordinates[0], coordinates[1])
            self.pushUp('График визуализирован')


    # Очистка чекбоксов
    def clearCheckBoxes(self):
        self.checkBoxHumidity.setChecked(False)
        self.checkBoxPrecipitation.setChecked(False)
        self.checkBoxDirectionWind.setChecked(False)
        self.checkBoxTemperature.setChecked(False)


    def clear_graph(self):
        self.graphicsView.clear()


    # Навигация
    def navigate(self):
        self.tabWidget.setCurrentIndex(self.navTab[self.sender().text()][1])


    def pushUp(self, text):
        # Окно Push-уведомления
        self.pushWindow = WindowPush()
        sizeDysplay = QDesktopWidget().screenGeometry(0)
        self.pushWindow.setGeometry(sizeDysplay.width() - 310,
                                    sizeDysplay.height() - 190,
                                    300, 100)
        self.pushWindow.MessagePush.setText(text)
        self.pushWindow.show()


    def emulationData(self):
        try:
            print(emulationData())
            self.pushUp('Эмуляция завершена')
        except Exception as error:
            print(error)
            self.pushUp('Ошибка эмуляции')


    # На главную
    def homeGo(self):
        self.tabWidget.setCurrentIndex(0)


    def clearTableWidget(self):
        pass

    def loadTable(self):
        pass


    # Местоположение
    # def ip_a(self):
    #     def get_ip():
    #         response = requests.get('https://api64.ipify.org?format=json').json()
    #         return response["ip"]
    #
    #     def get_location():
    #         ip_address = get_ip()
    #         location_data = {
    #             "ip": ip_address}
    #         n = ''.join([j for i, j in location_data.items()])
    #         return n
    #
    #     def main_1():
    #         try:
    #              url = requests.get('https://api64.ipify.org?format=json')
    #              if url:
    #                  ip = get_location()
    #                  n = []
    #                  response = requests.get(f'http://ip-api.com/json/{ip}').json()
    #                  for i, j in response.items():
    #                      if i == 'lat' or i == 'lon':
    #                          n.append(j)
    #                  m = folium.Map(location=[n[0], n[1]], zoom_start=15)
    #                  folium.Marker([n[0], n[1]], poput='Место 1', tooltip=None).add_to(m)
    #                  m.save('weather.html')
    #                  webbrowser.open('weather.html')
    #
    #
    #         except requests.ConnectionError as e:
    #             print(e)
    #
    #
    #     if __name__ == '__main__':
    #         main_1()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Monitoringiop()
    ex.show()
    sys.exit(app.exec_())
