from matrix import *
from math import tanh, cosh


class NeuralNetwork:

    def __init__(self, n_inputs: int, n_hidden: list[int], n_outputs: int, learning_rate: float = 0.1):

        # wspolczynnik korekcji bledow
        self.learning_rate = learning_rate

        # macierz wezlow wejsciowych
        self.input_nodes = Matrix(n_inputs, 1)

        # macierz wezlow warstw ukrytych
        self.hidden_nodes = []
        for n in n_hidden:
            self.hidden_nodes.append(Matrix(n, 1))

        # macierz wezlow wyjsciowych
        self.output_nodes = Matrix(n_outputs, 1)

        # macierz wag polaczen - ukryte
        self.weights_ih = Matrix(n_hidden[0], n_inputs)
        self.weights_ih.randomize()

        # macierz wag polaczen - ukryte
        self.weights_h = []
        for i in range(len(n_hidden) - 1):
            self.weights_h.append(Matrix(n_hidden[i + 1], n_hidden[i]))
            self.weights_h[i].randomize()

        # macierz wag polaczen - wyjscie
        self.weights_ho = Matrix(n_outputs, n_hidden[len(n_hidden) - 1])
        self.weights_ho.randomize()

    def feed_forward(self, input: list[float]) -> list[float]:

        if self.input_nodes.height == len(input):

            # przypisanie danych wejsciowych do wezlow
            for i in range(len(input)):
                self.input_nodes.tab[0][i] = input[i]
        else:
            return []

        # obliczanie wartosci wezlow ukrytych
        self.hidden_nodes[0] = Matrix.multiply(self.weights_ih, self.input_nodes)
        self.hidden_nodes[0] = Matrix.map(self.hidden_nodes[0], hyperbolic_tangent)
        for i in range(1, len(self.hidden_nodes)):
            self.hidden_nodes[i] = Matrix.multiply(self.weights_h[i - 1], self.hidden_nodes[i - 1])
            self.hidden_nodes[i] = Matrix.map(self.hidden_nodes[i], hyperbolic_tangent)

        # obliczanie wartosci wezlow wyjsciowych
        self.output_nodes = Matrix.multiply(self.weights_ho, self.hidden_nodes[len(self.hidden_nodes) - 1])
        self.output_nodes = Matrix.map(self.output_nodes, hyperbolic_tangent)

        # przypisanie wartosci wezlow wyjsciowych do listy
        guess = self.output_nodes.tab[0]
        return guess

    def train(self, input: list[float], answer: list[float]):  # ciuuuch ciuuch!!!

        last_guess = self.feed_forward(input)
        if self.output_nodes.height == len(last_guess):
            self.output_nodes.tab[0] = last_guess.copy()
        answers = Matrix(self.output_nodes.height, 1)
        if answers.height == len(answer):
            answers.tab[0] = answer.copy()

        # ponizej algorytm propagacji wstecznej
        errors_o = answers - self.output_nodes

        errors_h = [Matrix.multiply(Matrix.transpose(self.weights_ho), errors_o)]
        for i in range(len(self.weights_h) - 1, -1, -1):
            temp_errors = errors_h[0].copy()
            errors_h.insert(0, Matrix.multiply(Matrix.transpose(self.weights_h[i]), temp_errors))

        gradient_o = Matrix.map(self.output_nodes, grad) * errors_o * self.learning_rate
        delta_ho = Matrix.multiply(gradient_o, Matrix.transpose(self.hidden_nodes[len(self.hidden_nodes) - 1]))
        self.weights_ho += delta_ho

        gradient_h = []
        delta_h = []
        for i in range(len(self.hidden_nodes) - 1, -1, -1):
            gradient_h.insert(0, Matrix.map(self.hidden_nodes[i], grad) * errors_h[i] * self.learning_rate)
            if i > 0:
                delta_h.insert(0, Matrix.multiply(gradient_h[0], Matrix.transpose(self.hidden_nodes[i - 1])))
                self.weights_h[i - 1] += delta_h[0]
            else:
                delta_ih = Matrix.multiply(gradient_h[0], Matrix.transpose(self.input_nodes))
                self.weights_ih += delta_ih

    def save(self, file_path):
        with open(file_path, 'w') as file:
            file.write(str(self.weights_ih.width) + '\n' + str(self.weights_ih.height) + '\n')
            for col in self.weights_ih.tab:
                for val in col:
                    file.write(str(val) + '\n')
            file.write(str(len(self.weights_h)) + '\n')
            for hidden in self.weights_h:
                file.write(str(hidden.width) + '\n' + str(hidden.height) + '\n')
                for col in hidden.tab:
                    for val in col:
                        file.write(str(val) + '\n')
            file.write(str(self.weights_ho.width) + '\n' + str(self.weights_ho.height) + '\n')
            for col in self.weights_ho.tab:
                for val in col:
                    file.write(str(val) + '\n')

    def load(self, file_path):
        with open(file_path, 'r') as file:
            width_ih = int(file.readline())
            height_ih = int(file.readline())
            self.hidden_nodes = [Matrix(height_ih, 1)]
            self.input_nodes = Matrix(width_ih, 1)
            self.weights_ih = Matrix(height_ih, width_ih)
            for col in self.weights_ih.tab:
                for i in range(len(col)):
                    col[i] = float(file.readline())
            hidden_layers_count = int(file.readline())
            self.weights_h = []
            for i in range(hidden_layers_count):
                width_h = int(file.readline())
                height_h = int(file.readline())
                self.hidden_nodes.append(Matrix(height_h, 0))
                hidden_layer = Matrix(height_h, width_h)
                for col in hidden_layer.tab:
                    for j in range(len(col)):
                        col[j] = float(file.readline())
                self.weights_h.append(hidden_layer)
            width_ho = int(file.readline())
            height_ho = int(file.readline())
            self.output_nodes = Matrix(height_ho, 1)
            self.weights_ho = Matrix(height_ho, width_ho)
            for col in self.weights_ho.tab:
                for i in range(len(col)):
                    col[i] = float(file.readline())


def hyperbolic_tangent(x: float):
    return tanh(x)


def grad(x: float):
    return 1/(cosh(x) ** 2)
