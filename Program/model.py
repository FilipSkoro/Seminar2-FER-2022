'''
Faculty of Electrical engineering and Computing

Subject: Seminar 2
Student: Filip Škoro
Mentor: Stjepan Bogdan
Academic Year: 2021./2022.

Python version: Python 3.8.10

'''

import yaml
import numpy as np

def loadYaml(path):

    '''
    This function loads .yaml file from location specified in a function
    argument 'path'. It takes relevant data from a file, which are in this
    case trains names and their stations names and then returns dictionary
    containig these information.
    '''

    with open(path) as file:
        data = yaml.full_load(file)

    trains = []
    for key in data.keys():
        if ("_stops" in key):
            trains.append(key)
        else:
            continue

    trains_stops = []
    for train in trains:
        trains_stops.append([*data.get(train)])

    final_data = {}
    for i in range(len(trains)):
        final_data.__setitem__(trains[i], trains_stops[i])

    return final_data

def printMatrix(matrix):
    '''
    This functions prints matrix 'row by row'. It gets one argument which
    is matrix that needs to be printed. It is used to make matrix printing
    transparent and unambiguous.
    '''

    for i in range(len(matrix)):
        print(matrix[i])

def getTrains(data):

    '''
    This function divides trains from a dictionary and returns
    them in a list. It gets one argument 'data' which is dictionary
    where trains are keys and lists of each trains stations are values.
    '''

    return [*data]

def getSegments(data, trains):

    '''
    This function calculates every segment on a railway network and
    then returns sorted list of those segments. It gets two arguments;
    'data' which is dictionary where trains are keys and lists of each trains
    stations are values and 'trains' which is list of trains.
    '''

    segments = []

    for train in trains:
        route = data.get(train)
        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            if (segment in segments):
                continue
            else:
                segments.append(segment)

    segments.sort()
    return segments

def getTrainsOnSegments(data, trains):

    '''
    This function is used for making strings that represent trains on
    their segments and then returns it as a list. It gets two arguments;
    'data' which is dictionary where trains are keys and lists of each trains
    stations are values and 'trains' which is list of trains.
    '''

    trains_on_segments = []

    for train in trains:
        route = data.get(train)
        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            segment = train + segment
            trains_on_segments.append(segment)

    return trains_on_segments

def getMatrixF(data, trains, segments, trains_on_segments):

    '''
    This function calculates and returns matirx F. It gets four arguments;
    'data' which is dictionary where trains are keys and lists of each trains
    stations are values, 'trains' which is list of trains, 'segments' which is
    list of all segments between stations and 'trains_on_segments' which is
    list of every train on its every segment.
    '''

    num_rows = len(trains)
    num_column_Fv = 0
    num_column_Fu = len(trains)
    num_column_Fr = len(getSegments(data, trains))

    for train in trains:
        num_column_Fv = num_column_Fv + len(data.get(train))
        num_rows = num_rows + len(data.get(train))

    Fv = np.zeros((num_rows, num_column_Fv))
    Fr = np.zeros((num_rows, num_column_Fr))
    Fu = np.zeros((num_rows, num_column_Fu))
    Fy = np.zeros((num_rows, num_column_Fu))

    # matrix Fu
    for train in trains:
        if (trains.index(train) == 0):
            Fu[0][trains.index(train)] = 1
        else:
            cnt = 0
            for i in range(0, trains.index(train)):
                cnt = cnt + len(data.get(trains[i])) + 1

            Fu[cnt][trains.index(train)] = 1

    # matrix Fr
    cnt = 0
    for train in trains:
        route = data.get(train)

        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            Fr[cnt][segments.index(segment)] = 1
            cnt = cnt + 1

        cnt = cnt + 1

    # matrix Fv
    cnt = 1
    for train in trains:
        route = data.get(train)

        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            segment = train + segment
            Fv[cnt][trains_on_segments.index(segment)] = 1
            cnt = cnt + 1

        cnt = cnt + 1

    # matrica F = [Fu Fv Fr Fy]
    F = np.concatenate((Fu, Fv, Fr, Fy), axis=1)

    Fu = Fu.astype(int)
    Fv = Fv.astype(int)
    Fr = Fr.astype(int)
    Fy = Fy.astype(int)
    F = F.astype(int)

    print("\nFu = \n")
    printMatrix(Fu)
    print("\nFv =\n")
    printMatrix(Fv)
    print("\nFr = \n")
    printMatrix(Fr)
    print("\nFy = \n")
    printMatrix(Fy)

    return F

def getMatrixS(data, trains, segments, trains_on_segments):

    '''
    This function calculates and returns matirx S. It gets four arguments;
    'data' which is dictionary where trains are keys and lists of each trains
    stations are values, 'trains' which is list of trains, 'segments' which is
    list of all segments between stations and 'trains_on_segments' which is
    list of every train on its every segment.
    '''

    num_columns = len(trains)
    num_rows_Sv = 0
    num_rows_Sy = len(trains)
    num_rows_Sr = len(getSegments(data, trains))

    for train in trains:
        num_rows_Sv = num_rows_Sv + len(data.get(train))
        num_columns = num_columns + len(data.get(train))

    Sv = np.zeros((num_rows_Sv, num_columns))
    Sr = np.zeros((num_rows_Sr, num_columns))
    Su = np.zeros((num_rows_Sy, num_columns))
    Sy = np.zeros((num_rows_Sy, num_columns))

    # matrix Sy
    for train in trains:
        if (trains.index(train) == 0):
            Sy[0][len(data.get(train))] = 1
        else:
            cnt = 0
            for i in range(0, trains.index(train)):
                cnt = cnt + len(data.get(trains[i])) + 1

            Sy[trains.index(train)][cnt + len(data.get(train))] = 1

    # matrix Sr
    cnt = 1
    for train in trains:
        route = data.get(train)

        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            Sr[segments.index(segment)][cnt] = 1
            cnt = cnt + 1

        cnt = cnt + 1

    # matrix Sv
    cnt = 0
    for train in trains:
        route = data.get(train)

        for i in range(0, len(route)):
            if (i != (len(route) - 1)):
                if (route[i] > route[i+1]):
                    segment = route[i+1] + route[i]
                else:
                    segment = route[i] + route[i+1]
            else:
                if (route[i] > route[0]):
                    segment = route[0] + route[i]
                else:
                    segment = route[i] + route[0]

            segment = train + segment
            Sv[trains_on_segments.index(segment)][cnt] = 1
            cnt = cnt + 1

        cnt = cnt + 1

    # matrica S = [Su; Sv; Sr; Sy]
    S = np.concatenate((Su, Sv, Sr, Sy), axis=0)

    Su = Su.astype(int)
    Sv = Sv.astype(int)
    Sr = Sr.astype(int)
    Sy = Sy.astype(int)
    S = S.astype(int)

    print("\nSu = \n")
    printMatrix(Su)
    print("\nSv =\n")
    printMatrix(Sv)
    print("\nSr = \n")
    printMatrix(Sr)
    print("\nSy = \n")
    printMatrix(Sy)

    return S

def getMatrixW(F, S):

    '''
    This function calculates matrix W. It gets matrices F and S as
    arguments and then calculates matrix W by formula W = transpose(S) - F
    and returns it as a result.
    '''

    W = np.transpose(S) - F

    return W

if __name__ == "__main__":

    '''
    This is a main function which is used for starting the program
    and calling all relevant functions. It is also function where user
    has to define path for needed .yaml file.
    '''

    data = {}
    data = loadYaml(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data.yaml')
    #data = loadYaml(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data2.yaml')
    #data = loadYaml(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data3.yaml')
    #data = loadYaml(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data4.yaml')
    #data = loadYaml(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data5.yaml')
    trains = getTrains(data)

    print("\n===========================================================\n")
    print("Determination of matrices F and S from railway network data")
    print("\n===========================================================\n")

    F = getMatrixF(data, trains, getSegments(data, trains), getTrainsOnSegments(data, trains))
    S = getMatrixS(data, trains, getSegments(data, trains), getTrainsOnSegments(data, trains))
    W = getMatrixW(F, S)

    print("\nF = [Fu Fv Fr Fy] = \n")
    printMatrix(F)

    print("\nS = [Su; Sv; Sr; Sy] = \n")
    printMatrix(S)

    print("\nW =\n")
    printMatrix(W)