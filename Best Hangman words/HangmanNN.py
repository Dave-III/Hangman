from hangman import HangmanSession
from difficulty import WordScoring
import random, math
class HangmanEncoder:
    def __init__(self, max_length=45, pos_enc_dim=16):
        self.alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.max_length = max_length
        self.pos_enc_dim = pos_enc_dim
        self.letter_vector_size = 27 

        self.vector_size = self.letter_vector_size + self.pos_enc_dim
        self.letter_index_dict = {i: ch for i, ch in enumerate(self.alphabet)}
        self.letter_index_dict[26] = "~"

    def one_hot_encode_letter(self, letter):
        vector = [0] * self.letter_vector_size
        if letter in self.alphabet:
            index = self.alphabet.index(letter)
            vector[index] = 1
        elif letter == "~":
            vector[26] = 1
        return vector

    def positional_encoding(self, pos):
        pe = [0] * self.pos_enc_dim
        for i in range(0, self.pos_enc_dim, 2):
            div_term = math.pow(10000, i / self.pos_enc_dim)
            pe[i] = math.sin(pos / div_term)
            if i + 1 < self.pos_enc_dim:
                pe[i + 1] = math.cos(pos / div_term)
        return pe

    def encode_word_state(self, word_state):
        word_state = word_state.lower()
        padded = word_state + "~" * (self.max_length - len(word_state))
        encoded = []
        for pos, letter in enumerate(padded[:self.max_length]):
            letter_vec = self.one_hot_encode_letter(letter)
            pos_vec = self.positional_encoding(pos)
            encoded.extend(letter_vec + pos_vec)
        return encoded
    
    def decoder(self, word_state):
        encoded_matrix = self.encode_word_state(word_state)
        matrix_size = self.vector_size
        nested_list = [encoded_matrix[i:i + matrix_size] for i in range(0, len(encoded_matrix), matrix_size)]

        decrypted_chars = []
        for letter_vector in nested_list:
            try:
                index = letter_vector.index(1)
                decrypted_chars.append(self.letter_index_dict[index])
            except ValueError:
                decrypted_chars.append("_")
        return "".join(decrypted_chars)

    def encode_guessed_letters(self, guessed_letters):
        vector = [0] * 26
        for ch in guessed_letters:
            if ch in self.alphabet:
                vector[self.alphabet.index(ch)] = 1
        return vector
    
    def encode_input(self, word_state, guessed_letters):
        word_features = self.encode_word_state(word_state)
        guess_features = self.encode_guessed_letters(guessed_letters)
        return word_features + guess_features




class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01, weight_decay = 0.0001):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.lr = learning_rate
        self.weight_decay = weight_decay

        # Initialize weights and biases with small random values
        self.W1 = [[random.uniform(-0.1, 0.1) for _ in range(input_size)] for _ in range(hidden_size)]
        self.b1 = [0.0] * hidden_size

        self.W2 = [[random.uniform(-0.1, 0.1) for _ in range(hidden_size)] for _ in range(output_size)]
        self.b2 = [0.0] * output_size

    #Hidden neuron weight calculations
    def relu(self, x):
        return max(0, x)

    def relu_derivative(self, x):
        return 1.0 if x > 0 else 0.0

    #softmax calculation used to update neuron weights
    def softmax(self, x):
        max_x = max(x)
        exps = [math.exp(i - max_x) for i in x]
        sum_exps = sum(exps)
        return [j / sum_exps for j in exps]


    def forward(self, input_vector, training=False, dropout_rate=0.2):
        self.z1 = []
        for i in range(self.hidden_size):
            z = sum(self.W1[i][j] * input_vector[j] for j in range(self.input_size)) + self.b1[i]
            self.z1.append(z)
        self.a1 = [self.relu(z) for z in self.z1]

        if training:
            for i in range(self.hidden_size):
                if random.random() < dropout_rate:
                    self.a1[i] = 0.0

        self.z2 = []
        for i in range(self.output_size):
            z = sum(self.W2[i][j] * self.a1[j] for j in range(self.hidden_size)) + self.b2[i]
            self.z2.append(z)

        self.a2 = self.softmax(self.z2)
        return self.a2

    def backward(self, input_vector, target_vector):
        # Calculate output layer error (cross-entropy loss derivative)
        # target_vector is one-hot encoded
        delta2 = [self.a2[i] - target_vector[i] for i in range(self.output_size)]

        # Gradients for W2 and b2
        dW2 = [[0] * self.hidden_size for _ in range(self.output_size)]
        db2 = [0] * self.output_size

        for i in range(self.output_size):
            for j in range(self.hidden_size):
                dW2[i][j] = delta2[i] * self.a1[j]
            db2[i] = delta2[i]

        # Backpropagate to hidden layer
        delta1 = [0] * self.hidden_size
        for j in range(self.hidden_size):
            error = 0
            for i in range(self.output_size):
                error += delta2[i] * self.W2[i][j]
            delta1[j] = error * self.relu_derivative(self.z1[j])

        # Gradients for W1 and b1
        dW1 = [[0] * self.input_size for _ in range(self.hidden_size)]
        db1 = [0] * self.hidden_size

        for j in range(self.hidden_size):
            for k in range(self.input_size):
                dW1[j][k] = delta1[j] * input_vector[k]
            db1[j] = delta1[j]

        # Update weights and biases with weight decay
        for i in range(self.output_size):
            for j in range(self.hidden_size):
                self.W2[i][j] -= self.lr * (dW2[i][j] + self.weight_decay * self.W2[i][j])  # weight decay term added
            self.b2[i] -= self.lr * db2[i]  # biases usually not decayed

        for j in range(self.hidden_size):
            for k in range(self.input_size):
                self.W1[j][k] -= self.lr * (dW1[j][k] + self.weight_decay * self.W1[j][k])  # weight decay term added
            self.b1[j] -= self.lr * db1[j]

    #runs the NN
    def predict(self, input_vector, guessed_letters, bad_guesses_set):
        # Feedforward to get raw scores
        self.z1 = [sum(self.W1[i][j] * input_vector[j] for j in range(self.input_size)) + self.b1[i]
                for i in range(self.hidden_size)]
        self.a1 = [self.relu(z) for z in self.z1]

        self.z2 = [sum(self.W2[i][j] * self.a1[j] for j in range(self.hidden_size)) + self.b2[i]
                for i in range(self.output_size)]

        for letter in guessed_letters.union(bad_guesses_set):
            idx = encoder.alphabet.index(letter)
            self.z2[idx] = float('-inf')

        self.a2 = self.softmax(self.z2)

        max_index = self.a2.index(max(self.a2))
        max_prob = self.a2[max_index]
        return max_index, max_prob


def train_network(session, letter_net, position_net, encoder, epochs=1000):
    total = 0
    average = 0

    for epoch in range(epochs):
        session.difficulty = random.randint(1, 3)
        session.wordGen = WordScoring(session.wordlist)
        session._HangmanSession__reset()
        true_word = session.wordToGuess
        guessed_so_far = set()
        bad_guesses_set = set()

        print(f"\nEpoch {epoch + 1} start. Word to guess: {true_word}")

        unguessed_letters = set(true_word) - guessed_so_far

        while "_" in session.wordState and session.badLetters < 10:
            input_vector = encoder.encode_input(session.wordState, ''.join(sorted(guessed_so_far)))
            predicted_index, confidence = letter_net.predict(input_vector, guessed_so_far, bad_guesses_set)
            predicted_letter = encoder.alphabet[predicted_index]

            epsilon = 0.1
            target_vector = [epsilon / 26] * 26  # baseline smoothing

            for letter in unguessed_letters:
                target_vector[encoder.alphabet.index(letter)] += (1.0 - epsilon) / len(unguessed_letters)


            # Train the network on all remaining letters (helps build stronger associations)
            letter_net.forward(input_vector)
            letter_net.backward(input_vector, target_vector)

            was_correct = predicted_letter in unguessed_letters
            if predicted_letter in unguessed_letters:
                # Correct prediction — update state
                guessed_so_far.add(predicted_letter)
                unguessed_letters.remove(predicted_letter)

                session.wordState = ''.join([
                    predicted_letter if true_word[i] == predicted_letter else session.wordState[i]
                    for i in range(len(true_word))
                ])
            else:
                # Wrong prediction, punished for getting letter wrong
                session.badLetters += 1
                bad_guesses_set.add(predicted_letter)

            total += 1


            #prints stats for human interpretation
            print(f"Predicted: '{predicted_letter}', letter was correct?: {was_correct}, Confidence: {confidence:.2%}, Bad guesses: {session.badLetters}")
        average +=  session.badLetters
    print(f"\ntotal guesses: {total}, average wrong: {average/epoch}")


if __name__ == "__main__":


    max_length = 45
    pos_enc_dim = 16
    encoder = HangmanEncoder(max_length=max_length, pos_enc_dim = pos_enc_dim)

    # Neural networks for letter and position prediction
    letter_net = SimpleNeuralNetwork(
        input_size = encoder.vector_size * encoder.max_length + 26,
        hidden_size=512,
        output_size=26
    )

    position_net = SimpleNeuralNetwork(
        input_size=encoder.vector_size * encoder.max_length + 26,
        hidden_size=512,
        output_size=max_length  # position index (0 to max_length-1)
    )

    session = HangmanSession()

    train_network(session, letter_net, position_net, encoder, epochs=100)
