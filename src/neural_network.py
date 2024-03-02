import tensorflow as tf
from tensorflow import keras
import numpy as np

class NeuralNetwork:

    def __init__(self, num_features):
        self.num_features = num_features
        self.model = self._create_model()

    def _create_model(self):
        # Define the model architecture (same as previous example)
        model = keras.Sequential([
            keras.layers.Dense(128, activation="relu", input_shape=(self.num_features,)),
            keras.layers.Dense(64, activation="relu"),
            keras.layers.Dense(1)
        ])
        # Compile the model
        model.compile(optimizer="adam", loss="mse")
        return model
    
    def read_file(self, filename):
        """
        Read a file with binary lists and fitness values.

        Args:
            filename: The filename of the file to read.

        Returns:
            A list of tuples containing (binary_list, fitness_value).
        """

        data = []
        fitness_values = []
        with open(filename, "r") as f:
            for line in f:
                # Split the line into binary list and fitness value
                line = line.strip()
                line = line.replace("[", "")
                line = line.replace("]", "")

                
                line = line.split(",")
                binary_list = line[:-1]
                binary_list = [int(x) for x in binary_list]
                
                fitness_value = float(line[-1])
                data.append(binary_list)
                fitness_values.append(fitness_value)
        
        return data, fitness_values

    def train_nn(self, training_data_path: str, epochs=100):
        """
        Train the neural network on the provided training data file

        Args:
            training_data_path: The path to the file containing training data.
            epochs: The number of epochs to train for (default: 1000).
        """

        individuals, fitness = self.read_file(training_data_path)
        X_train = np.array(individuals)
        Y_train = np.array(fitness)
        X_train = X_train.reshape(-1, self.num_features)
        
        # Compile the model
        self.model.fit(X_train, Y_train, epochs=epochs, verbose=1)
        
    
    def save_nn(self, filename):
        """
        Save the trained neural network model to a file.

        Args:
            filename: The filename to save the model to.
        """

        self.model.save(filename)

    def load_nn(self, filename):
        """
        Load a pre-trained neural network model from a file.

        Args:
            filename: The filename of the saved model.
        """

        self.model = keras.models.load_model(filename)
        # Update num_features in case it was different in the saved model
        self.num_features = self.model.layers[0].input_shape[1]

    def evaluate_fitness(self, binary_list):
        """
        Evaluate the fitness of a binary list using the trained model.

        Args:
            binary_list: A list representing the binary features.

        Returns:
            The predicted fitness value (between 0 and 1).
        """

        data = tf.cast(binary_list, dtype=tf.float32)
        data = tf.expand_dims(data, axis=0)
        fitness = self.model.predict(data)[0][0]
        return fitness
    
    def evaluate_list_of_lists(self, list_of_binary_lists):
        """
        Evaluate the fitness of each binary list in a list of lists.

        Args:
            list_of_binary_lists: A list containing sublists representing binary features.

        Returns:
            A list of fitness values corresponding to each binary list.
        """

        if len(list_of_binary_lists) == 1:
            return [self.evaluate_fitness(list_of_binary_lists[0])]
        

        
        fitness = self.model.predict(list_of_binary_lists, batch_size=32, verbose=1)
        
        fitness = fitness.tolist()
        fitness = [x[0] for x in fitness]
        

        return fitness
        
        fitness_values = []
        for binary_list in list_of_binary_lists:
            fitness = self.evaluate_fitness(binary_list)
            fitness_values.append(fitness)
        return fitness_values


# Example usage

if __name__ == "__main__":
    network = NeuralNetwork(num_features=77)  # Replace X with actual number of features

    #network.train_nn("generated-files/train_data.txt")
    #network.save_nn("my_model.h5")
    chromossome = [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1]
    fitness = network.evaluate_fitness(chromossome)
