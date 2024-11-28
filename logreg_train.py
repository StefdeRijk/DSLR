import argparse
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score


class LogisticRegression2:
    def __init__(self, learning_rate=0.001, epochs=1000):
        self.lr = learning_rate
        self.epochs = epochs
        self.weights = None
        self.bias = None
        self.losses = []

    @staticmethod
    def _sigmoid(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def compute_loss(y_true, y_pred):
        # binary cross entropy
        y1 = y_true * np.log(y_pred + 1e-9)
        y2 = (1 - y_true) * np.log(1 - y_pred + 1e-9)
        return -np.mean(y1 + y2)

    def feed_forward(self, X):
        z = np.dot(X, self.weights) + self.bias
        y_pred = self._sigmoid(z)
        return y_pred

    def fit(self, X, y_true):
        n_samples, n_features = X.shape

        self.weights = np.zeros(n_features)
        self.bias = 0

        # gradient descent
        for i in range(self.epochs):
            y_pred = self.feed_forward(X)
            self.losses.append(self.compute_loss(y_true, y_pred))
            # compute gradients
            difference = y_pred - y_true  # derivative of sigmoid and bce X.T*(A-y)
            gradient_weight = np.array((1 / n_samples) * np.dot(X.transpose(), difference), dtype=float)
            gradient_bias = (1 / n_samples) * np.sum(difference)

            self.weights -= self.lr * gradient_weight
            self.bias -= self.lr * gradient_bias

    def predict(self, X):
        threshold = .5
        y_hat = np.dot(X, self.weights) + self.bias
        y_predicted = self._sigmoid(y_hat)
        y_predicted_cls = [1 if i > threshold else 0 for i in y_predicted]

        return np.array(y_predicted_cls)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Settings for logistic regression')
    parser.add_argument('--data-file', type=str, required=True,
                        help='Path to the csv file that contains the data')
    args = parser.parse_args()

    data = pd.read_csv(args.data_file)
    data.dropna(inplace=True)
    y = data['Hogwarts House'].copy(deep=True)
    data = data.select_dtypes(['number'])
    data.drop(columns=['Index'], inplace=True)
    X = data
    for i, house in enumerate(y):
        if house == 'Hufflepuff':
            y.iloc[i] = 1
        else:
            y.iloc[i] = 0

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    regressor = LogisticRegression2(learning_rate=0.001, epochs=1000)
    regressor.fit(X_train, y_train)
    predictions = regressor.predict(X_test)
    print(predictions)
    print(y_test.to_numpy())
    accuracy3 = accuracy_score(y_test.to_numpy(), predictions)
    print(accuracy3)
