import hangman
import wordSolver
import utils

GAME_VALID = ["1", "game", "hangman game", "hangman", "g"]
SOLVER_VALID = ["2", "solver", "hangman solver", "solve", "s"]
EXIT_VALID = ["3", "exit", "e"]

def main():
    while True:
        userIn = utils.askUntilValid("[1] Hangman Game\n[2] Hangman Solver\n[3] Exit\n>>> ", GAME_VALID + SOLVER_VALID + EXIT_VALID)

        # if game selected
        if userIn.lower() in GAME_VALID:
            q = hangman.HangmanSession()
            exitcode = q.main()

            # depending on game output, continues or exits the program
            match exitcode:
                case 0:
                    break
                case 1:
                    continue

        # if solver selected
        elif userIn.lower() in SOLVER_VALID:
            while True:
                try:
                    wordLength = int(input("What is the word length?\n>>> "))
                except ValueError:
                    continue
                break
            solver = wordSolver.HangmanSolver(wordLength)
            solver.start()
        else:
            pass

if __name__ == "__main__":
    main()