import os
import csv

EXT = {
    '.dat': None,
    '.csv': ';'
}

def readDataFile(fname):
    file_extension = os.path.splitext(fname)[-1]
    splitter = EXT[file_extension]
    print(file_extension)
    data = None
    try:
        match file_extension:
            case '.dat':
                f = open(fname, 'r')
                data = []
                for s in f.readlines():
                    temp = s.split(splitter)
                                # станция, год, месяц, день, час, напр ветра, осадки, темпер-ра, влажность
                    data.append([temp[0], temp[5], temp[6], temp[7], temp[10],
                                 float(temp[39]), float(temp[47]), float(temp[-31]), float(temp[-15])])
                    # print([temp[0], temp[5], temp[6], temp[7], temp[10], float(temp[39]), float(temp[47]), float(temp[-31]), float(temp[-15])])
            case '.csv':
                data = []
                with open(fname, mode='r') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter=splitter)
                    for row in csvreader:
                        print(row[0])
                        line = row[0].split(',')
                        line = line[:4] + list(map(int, line[4:]))
                        # line = [line[0], line[5], line[6], line[7], line[10],
                        #         float(line[39]), float(line[47]), float(line[-31]), float(line[-15])]
                        data.append(line)
                        # print(line)
    except Exception as error:
        print(error)
        # return None
    # print(data)
    return data