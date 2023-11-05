from random import random
from math import tanh


def random_val():
    return 2 * random() - 1


class Neuron:
    def __init__(self, num_wheights):
        self.wheights = [random_val() for _ in range(num_wheights)]
        self.bias = random_val()
        self.result = 0
        self.input_values = []

    @staticmethod
    def activation(value):
        return tanh(value)

    @staticmethod
    def deriv_activation(value):
        return 1 - tanh(value) * tanh(value)

    def calculate_result(self, input_values):
        result = self.bias
        self.input_values = input_values
        for w, v in zip(self.wheights, input_values):
            result += w * v
        self.result = result
        return self.activation(result)

    def learn(self, error, new_error):
        adjust_factor = error * self.deriv_activation(self.result)
        for i in range(len(self.wheights)):
            new_error[i] += adjust_factor * self.wheights[i]
            self.wheights[i] -= adjust_factor * self.input_values[i] * LEARNING_RATE
        self.bias -= adjust_factor * LEARNING_RATE


class Layer:
    def __init__(self, num_neurons, prev_layer_size):
        self.neurons = [Neuron(prev_layer_size) for _ in range(num_neurons)]

    def calculate_result(self, input_values):
        return [neuron.calculate_result(input_values) for neuron in self.neurons]

    def learn(self, layer_error):
        new_error = [0 for _ in range(len(self.neurons[0].wheights))]
        for neuron, error in zip(self.neurons, layer_error):
            neuron.learn(error, new_error)
        return new_error


class Network:
    def __init__(self, num_layers, neurons_per_layer, input_layer_size, output_layer_size):
        self.layers = [Layer(neurons_per_layer, input_layer_size)]
        for _ in range(1, num_layers):
            self.layers.append(Layer(neurons_per_layer, neurons_per_layer))
        self.layers.append(Layer(output_layer_size, neurons_per_layer))

    def add_layer():
        self.layers.insert(-1, Layer(neurons_per_layer, neurons_per_layer))

    def calculate_result(self, input_values):
        current = input_values
        for layer in self.layers:
            current = layer.calculate_result(current)
        return current

    def learn(self, input_values, expected_output):
        output = self.calculate_result(input_values)
        # mse = 0
        deriv = []
        n = len(output)
        for o, e in zip(output, expected_output):
            deriv.append(2 * (o - e) / n)
        layer_error = deriv
        for layer in reversed(self.layers):
            layer_error = layer.learn(layer_error)

    def run(self, input_list, expected_output_list, epocs):
        for _ in range(epocs):
            for i, e in zip(input_list, expected_output_list):
                self.learn(i, e)


LEARNING_RATE = 0.01


def main():
    input_list = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ]
    expected_output_list = [
        [0], [1], [1], [0]
    ]
    rede = Network(1, 2, 2, 1)
    print("Antes de aprender:")
    for i in input_list:
        print(rede.calculate_result(i))
    print()
    print("Aprendendo...")
    rede.run(input_list, expected_output_list, 10000)
    print()
    print("Resultado final:")
    for i in input_list:
        print(rede.calculate_result(i))


if __name__ == '__main__':
    main()