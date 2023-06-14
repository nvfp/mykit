import numpy as _np
import random as _random
from typing import (
    Callable as _Callable,
    List as _List,
    Optional as _Optional,
    Tuple as _Tuple
)

from mykit.kit.math import relu as _ReLU


class DenseNN:
    """Also known as fully connected neural networks"""

    def __init__(
        self,
        sizes: _List[int],
        hidden_act_fn: _Callable[[_np.ndarray, bool], _np.ndarray] = _ReLU,
        output_act_fn: _Callable[[_np.ndarray, bool], _np.ndarray] = _ReLU,
        load_weights_and_biases: _Optional[_Tuple[_List[_np.ndarray], _List[_np.ndarray]]] = None,
    ) -> None:
        """
        The network uses normalized Xavier weight initialization and cross-entropy loss function.

        ---

        `load_weights_and_biases`: Pre-loaded weights and biases decoded by `decode` method. `None` for a new network.
        """

        self.sizes = sizes
        self.hidden_act_fn = hidden_act_fn
        self.output_act_fn = output_act_fn

        if load_weights_and_biases is None:
            self.weights = [
                -_np.sqrt(6/(x+y)) + _np.random.rand(y, x)*2*_np.sqrt(6/(x+y))  # normalized Xavier
                for x, y in zip(self.sizes[:-1], self.sizes[1:])
            ]
            self.biases = [
                _np.random.randn(y, 1)
                for y in self.sizes[1:]
            ]
        else:
            self.weights, self.biases = load_weights_and_biases

        self.n_layer = len(sizes)
        self.n_input = sizes[0]
        self.hidden_layers = sizes[1:-1]
        self.n_hidden_layer = len(self.hidden_layers)
        self.n_output = sizes[-1]

        ## values of these list are from the last feedforwarding
        self.z_values = []
        self.a_values = []
        self.decision = None  # the index of the output neuron with highest value

    def feedforward(self, a: _np.ndarray) -> int:
        """
        feedforward for given input `a`.

        ---

        ## Params
        `a`: Input array with shape `(n, 1)`.
            Example: `np.array([[i1], [i2], [i3], ...])`
        
        ## Returns
        The index of the maximum value in the output array.
        """

        ## reset
        self.z_values = []
        self.a_values = [a]

        ## if `self.n_layer` is 4 -> the variable `idx` below will be: 0, 1, 2
        for idx, (w, b) in enumerate(zip(self.weights, self.biases)):

            z = _np.dot(w, a) + b

            if idx == (self.n_layer - 2):  # output layer
                a = self.output_act_fn(z)
            else:
                a = self.hidden_act_fn(z)

            ## used for backpropagation
            self.z_values.append(z)
            self.a_values.append(a)

        self.decision = a.argmax()  # the index of the maximum value in `a`
        return self.decision

    def _backprop(self, inputs: _np.ndarray, outputs: _np.ndarray):
        """
        backpropagation algorithm.

        ---

        ## Params
        `inputs`: Input array with shape `(n, 1)`.
            Example: `np.array([[i1], [i2], [i3], ...])`
        `outputs`: Desired output array with shape `(m, 1)`.
            Example: `np.array([[o1], [o2], [o3], ...])`

        ## Returns
        `Tuple[dgw, dgb]`: Gradients of weights and biases as lists.
        """

        self.feedforward(inputs)

        ## gradient delta
        dgw = [_np.zeros(w.shape) for w in self.weights]
        dgb = [_np.zeros(b.shape) for b in self.biases]

        ## output layer
        delta = self.a_values[-1] - outputs  # using cross-entropy loss function
        dgw[-1] = _np.dot(delta, self.a_values[-2].transpose())
        dgb[-1] = delta

        ## hidden layers
        for l in range(2, self.n_layer):
            delta = _np.dot(self.weights[-l + 1].transpose(), delta)*self.hidden_act_fn(self.z_values[-l], derivative=True)
            dgw[-l] = _np.dot(delta, self.a_values[-l - 1].transpose())
            dgb[-l] = delta

        return (dgw, dgb)

    def _tuning(self, samples: _List[_Tuple[_np.ndarray, _np.ndarray]], k1: float, k2: float) -> None:
        """
        Update weights and biases.

        ---
        
        ## Params
            - `samples`: A list of input-output pairs used for updating the model
            - For optimization purposes, these values are precalculated:
                - `k1`: `learning_rate*(regularization/n_training_data)`
                - `k2`: `learning_rate/len(samples)`
        """

        ## Initialize gradients
        gw = [_np.zeros(w.shape) for w in self.weights]
        gb = [_np.zeros(b.shape) for b in self.biases]

        ## Compute gradients
        for inputs, outputs in samples:
            dgw, dgb = self._backprop(inputs, outputs)

            gw = [_gw + _dgw for _gw, _dgw in zip(gw, dgw)]
            gb = [_gb + _dgb for _gb, _dgb in zip(gb, dgb)]

        ## Update weights and biases
        self.weights = [
            (1 - k1)*w - k2*_gw
            for w, _gw in zip(self.weights, gw)
        ]
        self.biases = [
            b - k2*_gb
            for b, _gb in zip(self.biases, gb)
        ]

    def train(
        self,
        training_data: _List[_Tuple[_np.ndarray, _np.ndarray]],
        sample_size: int,
        n_epoch: int,
        learning_rate: float = 0.005,
        regularization: float = 0.001
    ) -> None:
        """
        Trains the model using gradient descent with regularization.

        ---

        ## Params
            - `training_data`: A list of tuples containing input-output pairs
            - `sample_size`: The number of samples to use for each iteration of gradient descent
                - `sample_size = 1` for stochastic gradient descent
                - `1 < sample_size < n_training_data` for mini-batch gradient descent
                - `sample_size = n_training_data` for batch gradient descent
            - `n_epoch`: The number of times to iterate over the entire training dataset
            - `learning_rate`: The learning rate used for gradient descent
            - `regularization`: The regularization factor to prevent overfitting
        """

        n_training_data = len(training_data)

        k1 = learning_rate*(regularization/n_training_data)

        for _ in range(n_epoch):

            _random.shuffle(training_data)
            list_of_samples = [
                training_data[i : i + sample_size]
                for i in range(0, n_training_data, sample_size)
            ]

            for samples in list_of_samples:
                self._tuning(samples, k1, learning_rate/len(samples))


    def encode(self) -> dict:
        """Encode the weights and biases as a JSON-serializable dictionary."""
        encoded_data = {
            'weights': [w.tolist() for w in self.weights],
            'biases': [b.tolist() for b in self.biases]
        }
        return encoded_data

    @staticmethod
    def decode(encoded_data: dict) -> _Tuple[_List[_np.ndarray], _List[_np.ndarray]]:
        """Decode the weights and biases from what is encoded by the `encode` method."""
        weights = [_np.array(w) for w in encoded_data['weights']]
        biases = [_np.array(b) for b in encoded_data['biases']]
        return weights, biases