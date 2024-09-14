import numpy as np

def parse_matrix(text):
    lines = text.split('\n')
    return np.array([list(map(int, line.split())) for line in lines])

def matrix_addition(matrix1, matrix2): #Сложение двух матриц
    
    return np.add(matrix1, matrix2).tolist()
