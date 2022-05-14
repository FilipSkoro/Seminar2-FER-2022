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

def loadTrainsAndSegments(path):
    '''
    This function loads .yaml file from location specified in a function
    argument 'path'. The .yaml file that is placed on a specified location
    contains railway network information. The function takes relevant data 
    from a file, which are in this case trains names and their stations names
    and then returns dictionary containig these information.
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

def loadYaml(path):
    '''
    This function loads .yaml file from location specified in a function
    argument 'path'. The .yaml file that is placed on a specified location
    contains input and output matrices of a particular railway network.
    The function loads these matrices in a dictionary and then returns it.
    '''

    with open(path) as file:
        matrices = yaml.full_load(file)

    return matrices

def printMatrix(matrix):
    '''
    This functions prints matrix 'row by row'. It gets one argument which
    is matrix that needs to be printed. It is used to make matrix printing
    transparent and unambiguous.
    '''

    for i in range(len(matrix)):
        print(matrix[i])

def getSegmentsNumber(data):
    '''
    This function is used for calculating number of segments between
    the stations in a particular railway network. It gets one argument 'data'
    which is a dictionary where trains are keys and lists of each trains 
    stations are values. The function returns the number of segments.
    '''

    segments = []

    for train in data.keys():
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
    return len(segments)

def getMatrixF(matrices, data):
    '''
    This function is used for extracting matrix F and matrices Fu, Fv, Fr and Fy
    from the input matrix I. It recieves two arguments; 'matrices' which is a
    dictionary in which keys are strings 'I' and 'O' and values are input and
    output matrices. The second argument is 'data' which is dictionary where
    trains are keys and lists of each trains stations are values. The function
    returns matrix F.
    '''

    num_trains = len(data.keys())
    num_segments = getSegmentsNumber(data)

    for key in matrices.keys():
        if (key == "I"):
            F = matrices.get(key)
        else:
            continue

    # matrix Fu
    Fu = []
    for i in range(num_trains):
        Fu.append(F[i])

    # matrix Fy
    Fy = []
    for i in range(1, num_trains + 1):
        Fy.append(F[len(F)-i])
    Fy.reverse()

    # matrix Fr
    Fr = []
    for i in range(num_trains + 1, num_trains + num_segments + 1):
        Fr.append(F[len(F)-i])
    Fr.reverse()

    # matrix Fv
    Fv = []
    for i in range(len(Fu), len(F) - len(Fr) - len(Fy)):
        Fv.append(F[i])

    Fu = np.transpose(Fu)
    Fv = np.transpose(Fv)
    Fr = np.transpose(Fr)
    Fy = np.transpose(Fy)
    F = np.transpose(F)

    print("\nFu =\n")
    printMatrix(Fu)
    print("\nFv =\n")
    printMatrix(Fv)
    print("\nFr =\n")
    printMatrix(Fr)
    print("\nFy =\n")
    printMatrix(Fy)

    return F

def getMatrixS(matrices, data):
    '''
    This function is used for extracting matrix S and matrices Su, Sv, Sr and Sy
    from the output matrix O. It recieves two arguments; 'matrices' which is a
    dictionary in which keys are strings 'I' and 'O' and values are input and
    output matrices. The second argument is 'data' which is dictionary where
    trains are keys and lists of each trains stations are values. The function
    returns matrix S.
    '''

    num_trains = len(data.keys())
    num_segments = getSegmentsNumber(data)

    # matrix S
    for key in matrices.keys():
        if (key == "O"):
            S = np.transpose(matrices.get(key))
        else:
            continue

    # matrix Su
    Su = []
    for i in range(num_trains):
        Su.append(S[i])

    # matrix Sy
    Sy = []
    for i in range(1, num_trains + 1):
        Sy.append(S[len(S)-i])
    Sy.reverse()

    # matrix Sr
    Sr = []
    for i in range(num_trains + 1, num_trains + num_segments + 1):
        Sr.append(S[len(S)-i])
    Sr.reverse()

    # matrix Sv
    Sv = []
    for i in range(len(Su), len(S) - len(Sr) - len(Sy)):
        Sv.append(S[i])

    print("\nSu =\n")
    printMatrix(Su)
    print("\nSv =\n")
    printMatrix(Sv)
    print("\nSr =\n")
    printMatrix(Sr)
    print("\nSy =\n")
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
    This is a main function which is used for starting the program and calling all
    relevant functions. It is also function where user has to define path for needed
    .yaml files. Function 'loadYaml' is used for loading .yaml file containg input and
    output matrices I and O while 'loadTrainsAndSegments' function is used for loading
    railway network information.
    '''

    matrices = {}
    matrices = loadYaml(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data_matrices_IO.yaml')
    #matrices = loadYaml(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data2_matrices_IO.yaml')
    #matrices = loadYaml(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data3_matrices_IO.yaml')
    #matrices = loadYaml(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data4_matrices_IO.yaml')
    #matrices = loadYaml(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data5_matrices_IO.yaml')
    data = {}
    data = loadTrainsAndSegments(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data.yaml')
    #data = loadTrainsAndSegments(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data2.yaml')
    #data = loadTrainsAndSegments(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data3.yaml')
    #data = loadTrainsAndSegments(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data4.yaml')
    #data = loadTrainsAndSegments(r'C:\Users\Filip\Desktop\Seminar 2\Zadatak\Program\route_data5.yaml')

    print("\n========================================================\n")
    print("Determination of matrices F and S from matrices I and O")
    print("\n========================================================\n")

    F = getMatrixF(matrices, data)
    print("\nF = [Fu Fv Fr Fy] = \n")
    print(F)

    S = getMatrixS(matrices, data)
    print("\nS = [Su; Sv; Sr; Sy] =\n")
    print(S)

    W = getMatrixW(F, S)
    print("\nW =\n")
    printMatrix(W)