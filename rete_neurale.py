from collections import deque
from keras import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import random

class agente():
    def __init__(self, param):
        self.impostazioni(param)
        self.crea_modello()

    def impostazioni(self, param):
        self.n_output = 4
        self.n_input = 12
        self.gamma = param["gamma"]
        self.batch_size = param["batch_size"]
        self.eps = param["eps"]
        self.eps_min = param["eps_min"]
        self.eps_decay = param["eps_decay"]
        self.learning_rate = param["learning_rate"]
        self.layer1 = param["layer1"]
        self.layer2 = param["layer2"]
        self.layer3 = param["layer3"]
        self.memory = deque(maxlen=2500)

    def crea_modello(self):
        self.model = Sequential(
            [
                ## Input
                Dense(units=self.layer1, input_shape=(self.n_input,), activation="relu"),
                Dense(units=self.layer2, activation="relu"),
                Dense(units=self.layer3, activation="relu"),
                ## Output
                Dense(units=self.n_output, activation="softmax")
            ]
        )
        self.model.compile(loss="mse", optimizer=Adam(learning_rate=self.learning_rate))

    def remember(self, state, action, reward, next_state, done):
        ## Aggiungiamo nella nostra memoria
        self.memory.append((state, action, reward, next_state, done))

    def act(self, stati):
        ## La percentuale di casualità per portare una variazione
        if np.random.rand() <= self.eps:
            return random.randrange(self.n_output)
        ## Predict
        act_values = self.model.predict(np.reshape(stati, (1, self.n_input)))
        return np.argmax(act_values[0])
    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states = np.array([i[0] for i in minibatch])
        actions = np.array([i[1] for i in minibatch])
        rewards = np.array([i[2] for i in minibatch])
        next_states = np.array([i[3] for i in minibatch])
        dones = np.array([i[4] for i in minibatch])

        states = np.squeeze(states)
        next_states = np.squeeze(next_states)

        targets = rewards + self.gamma*(np.amax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
        targets_full = self.model.predict_on_batch(states)

        ind = np.array([i for i in range(self.batch_size)])
        targets_full[[ind], [actions]] = targets

        self.model.fit(states, targets_full, epochs=1, verbose=0)
        if self.eps > self.eps_min:
            self.eps *= self.eps_decay
