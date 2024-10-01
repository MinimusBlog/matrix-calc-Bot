import numpy as np

def parse_matrix(text):
    try:
        matrix = np.array([list(map(int, line.split())) for line in text.strip().split('\n')])
        return matrix
    except ValueError as e:
        raise ValueError("Введены некорректные данные") from e

def matrix_addition(matrix1, matrix2): #Сложение двух матриц
    if matrix1.shape != matrix2.shape:
        raise ValueError("Матрицы имеют разные размеры")
    return np.add(matrix1, matrix2).tolist()

def matrix_subtraction(matrix1, matrix2): #Вычитание двух матриц
    if matrix1.shape != matrix2.shape:
        raise ValueError("Матрицы имеют разные размеры")
    return np.subtract(matrix1, matrix2).tolist()

def matrix_multiplication(matrix1, matrix2): #Умножение двух матриц
    if matrix1.shape[1] != matrix2.shape[0]:
        raise ValueError("Матрицы не могут быть перемножены. Количество столбцов первой матрицы должно быть равно количеству строк второй матрицы.")
    return np.dot(matrix1, matrix2).tolist()

def matrix_transposition(matrix): #Транспонирование матрицы
    return np.transpose(matrix).tolist()

def matrix_power(matrix, power): #Возведение в степень
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Матрица должна быть квадратной для возведения в степень")
    return np.linalg.matrix_power(matrix, power).tolist()

def matrix_scalar_multiplication(matrix, scalar):
    return np.multiply(matrix, scalar).tolist()

def matrix_determinant(matrix):
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Матрица должна быть квадратной для нахождения её определителя")
    return np.linalg.det(matrix)