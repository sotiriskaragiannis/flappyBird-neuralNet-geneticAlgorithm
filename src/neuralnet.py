import numpy as np
import scipy.special
import random
from constants import *


# Neural network class
# num_input: number of input nodes
# num_hidden: number of hidden nodes (only one layer)
# num_output: number of output nodes
class NeuralNet:

    def __init__(self, num_input, num_hidden, num_output):
        self.num_input = num_input
        self.num_hidden = num_hidden
        self.num_output = num_output
        self.weights_input_hidden = np.random.uniform(-0.5, 0.5, size=(self.num_hidden, self.num_input))
        self.weights_hidden_output = np.random.uniform(-0.5, 0.5, size=(self.num_output, self.num_hidden))
        self.activation_function = lambda x: scipy.special.expit(x) # Sigmoid function

    def get_outputs(self, inputs_list):
        inputs = np.array(inputs_list, ndmin=2).T # Convert to 2D array
        hidden_inputs = np.dot(self.weights_input_hidden, inputs)
        hidden_outputs = self.activation_function(hidden_inputs)
        final_inputs = np.dot(self.weights_hidden_output, hidden_outputs)
        final_outputs = self.activation_function(final_inputs)
        return final_outputs
    
    def get_max_value(self, inputs_list):
        return np.max(self.get_outputs(inputs_list))
    
    def modify_weights(self):
        NeuralNet.modify_array(self.weights_input_hidden)
        NeuralNet.modify_array(self.weights_hidden_output)

    def create_mixed_weights(self, nn1, nn2):
        self.weights_input_hidden = NeuralNet.get_mix_from_arrays(nn1.weights_input_hidden, nn2.weights_input_hidden)
        self.weights_hidden_output = NeuralNet.get_mix_from_arrays(nn1.weights_hidden_output, nn2.weights_hidden_output)
    
    def modify_array(a):
        for x in np.nditer(a, op_flags=['readwrite']):
            if random.random() < MUTATTION_WEIGHT_MODIFY_CHANCE:
                x[...] = np.random.random_sample() - 0.5

    def get_mix_from_arrays(ar1, ar2):

        total_entries = ar1.size
        num_rows = ar1.shape[0]
        num_cols = ar1.shape[1]

        num_to_take = total_entries - int(total_entries * MUTATION_ARRAY_MIX_PERCENT) # Get number of entries to take
        idx = np.random.choice(np.arange(total_entries), num_to_take, replace=False) # Get random indexes

        res = np.random.rand(num_rows, num_cols) # Create new array

        for row in range(0, num_rows):
            for col in range(0, num_cols):
                index = row * num_cols + col
                if index in idx:
                    res[row][col] = ar1[row][col]
                else:
                    res[row][col] = ar2[row][col]

        return res