import random


class Matrix:

    def __init__(self, rows: int, cols: int):
        self.width = cols
        self.height = rows
        col = []
        for i in range(self.height):
            col.append(0)
        self.tab = []
        for i in range(self.width):
            self.tab.append(col.copy())

    def __mul__(self, other):
        if isinstance(other, (int, float)) or \
                (isinstance(other, Matrix) and self.width == other.width and self.height == other.height):
            result = Matrix(self.height, self.width)
            for x in range(result.width):
                for y in range(result.height):
                    if isinstance(other, (int, float)):
                        result.tab[x][y] = self.tab[x][y] * other
                    else:
                        result.tab[x][y] = self.tab[x][y] * other.tab[x][y]
            return result
        else:
            print('Error during multiplication (element-wise)!')

    def __add__(self, other):
        if isinstance(other, (int, float)) or \
                (isinstance(other, Matrix) and self.width == other.width and self.height == other.height):
            result = Matrix(self.height, self.width)
            for x in range(result.width):
                for y in range(result.height):
                    if isinstance(other, (int, float)):
                        result.tab[x][y] = self.tab[x][y] + other
                    elif isinstance(other, Matrix):
                        result.tab[x][y] = self.tab[x][y] + other.tab[x][y]
            return result
        else:
            print('Error during addition!')

    def __sub__(self, other):
        if isinstance(other, (int, float)) or \
                (isinstance(other, Matrix) and self.width == other.width and self.height == other.height):
            result = Matrix(self.height, self.width)
            for x in range(result.width):
                for y in range(result.height):
                    if isinstance(other, (int, float)):
                        result.tab[x][y] = self.tab[x][y] - other
                    elif isinstance(other, Matrix):
                        result.tab[x][y] = self.tab[x][y] - other.tab[x][y]
            return result
        else:
            print('Error during subtraction!')

    def copy(self):
        result = Matrix(self.height, self.width)
        for x in range(result.width):
            result.tab[x] = self.tab[x].copy()
        return result

    def randomize(self, a=-1, b=1):
        for x in range(self.width):
            for y in range(self.height):
                self.tab[x][y] = random.uniform(float(a), float(b))

    @staticmethod
    def multiply(a, b):
        if isinstance(a, Matrix) and isinstance(b, Matrix):
            if a.width == b.height:
                result = Matrix(a.height, b.width)
                for y in range(result.height):
                    for x in range(result.width):
                        sum = 0
                        for z in range(a.width):
                            sum += a.tab[z][y] * b.tab[x][z]
                        result.tab[x][y] = sum
                return result
            else:
                print('Wrong matrix dimensions!')
        else:
            print('Error during multiplication (matrix-wise)!')

    @staticmethod
    def transpose(matrix):
        result = Matrix(matrix.width, matrix.height)
        for x in range(matrix.width):
            for y in range(matrix.height):
                result.tab[y][x] = matrix.tab[x][y]
        return result

    @staticmethod
    def map(matrix, fun):
        result = Matrix(matrix.height, matrix.width)
        for x in range(result.width):
            for y in range(result.height):
                result.tab[x][y] = fun(matrix.tab[x][y])
        return result

    def __repr__(self):
        string = ""
        temp = Matrix.transpose(self)
        for row in temp.tab:
            string += str(row) + '\n'
        del temp
        return string
