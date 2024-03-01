from cdocs.repl import Repl

class Brepl(Repl):

    def __init__(self):
        print("\n------------------------------")
        print("Brepl. a simple cli for bdocs!")
        print("------------------------------\n")
        super().__init__()
        #self.commands["more stuff"] = {}


    def loop(self):
        print("\n")
        while self._continue:
            self._one_loop()

