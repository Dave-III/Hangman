import hangman
import wordSolver
import utils

GAME_VALID = ["1", "game", "hangman game", "hangman", "g"]
SOLVER_VALID = ["2", "solver", "hangman solver", "solve", "s"]
EXIT_VALID = ["3", "exit", "e"]

def main():
    while True:
        userIn = utils.askUntilValid("[1] Hangman Game\n[2] Hangman Solver\n[3] Exit\n>>> ", GAME_VALID + SOLVER_VALID + EXIT_VALID)
        if userIn.lower() in GAME_VALID:
            q = hangman.HangmanSession()
            exitcode = q.main()
            match exitcode:
                # when user exits out of program via 'exit' and 'back' respectively
                case 0:
                    break
                case 1:
                    continue
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