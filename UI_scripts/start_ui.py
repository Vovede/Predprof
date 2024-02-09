import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from database import readFile, db_querry

conn = sqlite3.connect('bd.db')
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
            'Экспорт': [self.btnExportTab.clicked.connect(self.navigate), 6]
        }

        self.downloadFileData.clicked.connect(self.download)

        self.homeBtnDowloadTab.clicked.connect(self.homeGo)
        self.homeBtnVisualTab.clicked.connect(self.homeGo)
        self.homeBtnAnalisTab.clicked.connect(self.homeGo)
        self.homeBtnPredictTab.clicked.connect(self.homeGo)
        self.homeBtnMonitoringtab.clicked.connect(self.homeGo)

        self.pushBtnCheckboxesClear.clicked.connect(self.clear_button)
        self.clearBtnGraphView.clicked.connect(self.clear_graph)
        self.visualizationBtn.clicked.connect(self.visualization)



    #
    def download(self):
        # Загрузка данных из файла и запись в таблицу QTableWidgetItem
        fname = QFileDialog.getOpenFileName(self, 'Выбрать файл', '')[0]
        print(fname)
        try:
            self.data = readFile.readDataFile(fname)
            if self.data[0][0] not in self.totalData.keys():
                syn_station = ''.join([symb for symb in self.data[0][0] if symb.isdigit()])
                self.listStations.add(syn_station)
                print(self.data)
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
                        self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))

                self.tableWidget.resizeColumnsToContents()
                self.labelStatusDownloadData.setText(f'Статус: Данные загружены. Всего {len(self.data)} записей.')
                # self.pushUp('Данные загружены')
            else:
                print('Повторка!')
                self.labelStatusDownloadData.setText(f'Статус: Эти данные уже были загружены.')
                # self.pushUp('Отмена загрузки')
        except Exception as error:
            self.labelStatusDownloadData.setText(f'Статус: Невозможно загрузить данные. {error}')
            # self.pushUp('Ошибка загрузки')
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


    # Визуализация
    def visualization(self):
        self.graphicsView.clear()

        self.selectedItemListWidget = [x.text() for x in self.listWidgetStationMeteo.selectedItems()]

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


        if self.checkBoxPrecipitation.isChecked():  # Осадки
            coordinates = (lengthTempData, [int(i[-3]) for i in tempData])
            self.graphicsView.plot(coordinates[0], coordinates[1], pen=('b'))
            self.graphicsView_3.plot(coordinates[0], coordinates[1])

        if self.checkBoxDirectionWind.isChecked():  # Направление ветра
            coordinates = (lengthTempData, [int(i[-4]) for i in tempData])
            self.graphicsView.plot(coordinates[0], coordinates[1], pen=('y'))
            self.graphicsView_4.plot(coordinates[0], coordinates[1])

        if self.checkBoxTemperature.isChecked():  # Температура
            coordinates = (lengthTempData, [int(i[-2]) for i in tempData])
            self.graphicsView.plot(coordinates[0], coordinates[1], pen=('r'))
            self.graphicsView_6.plot(coordinates[0], coordinates[1])


    # Очистка чекбоксов
    def clear_button(self):
        self.checkBoxHumidity.setChecked(False)
        self.checkBoxPrecipitation.setChecked(False)
        self.checkBoxDirectionWind.setChecked(False)
        self.checkBoxTemperature.setChecked(False)


    def clear_graph(self):
        self.graphicsView.clear()


    # Навигация
    def navigate(self):
        self.tabWidget.setCurrentIndex(self.navTab[self.sender().text()][1])


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
