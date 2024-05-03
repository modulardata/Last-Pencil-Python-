from hstest import *
import re


class LastPencilTest(StageTest):

    @dynamic_test()
    def CheckOutput(self):
        main = TestedProgram()
        output = main.start().lower()
        lines = output.strip().split('\n')
        if len(lines) != 1 or "how many pencils" not in output:
            return CheckResult.wrong("When the game starts, it should output only one line asking the user about the "
                                     "number of pencils they would like to use with the \"How many pencils\" string")

        output2 = main.execute("1").replace(" ", "")
        if len(output2.split()) != 1:
            return CheckResult.wrong("When the user replies with the number of pencils, the game should print 1 "
                                     "non-empty line asking who will be the first player.\n"
                                     f"{len(output2.split())} lines were found in the output.")
        if not re.match(r".*\([a-zA-Z_0-9]+,[a-zA-Z_0-9]+\)", output2):
            return CheckResult.wrong("When the user replies with the number of pencils, the game should ask who will "
                                     "be the first player ending with the \"(\"Name1\", \"Name2\")\" string.")
        return CheckResult.correct()

    @dynamic_test(data=[[i, j] for i in [5, 20, 300] for j in [True, False]])
    def CheckGame(self, number, first_starts):
        main = TestedProgram()
        main.start()
        output2 = main.execute(str(number)).replace(" ", "")

        left_name = output2[output2.rfind('(') + 1:output2.rfind(',')]
        right_name = output2[output2.rfind(',') + 1:output2.rfind(')')]
        name = left_name if first_starts else right_name

        output3 = main.execute(name).lower()
        lines = [s for s in re.split(r'[\r\n]+', output3.strip()) if s != '']

        if len(lines) != 2:
            return CheckResult.wrong("When the player provides the initial game conditions"
                                     ", your program should print 2 non-empty lines:\n"
                                     "one with with vertical bar symbols representing the number of pencils, "
                                     "the other with the \"*NameX* is going first\" string.\n"
                                     f"{len(lines)} lines were found in the output.")

        pencils = [s for s in lines if '|' in s]
        if len(pencils) != 1:
            return CheckResult.wrong("When the player provides the initial game conditions, "
                                     "your program should print only one line with several vertical bar "
                                     "symbols ('|') representing pencils.")
        if len(list(set(pencils[0]))) != 1:
            return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|' symbol.")
        if len(pencils[0]) != number:
            return CheckResult.wrong("The line with pencils should contain as many '|' symbols as the player provided.")
        if not any((name.lower() in s) and ("first" in s) for s in lines):
            return CheckResult.wrong(f"There should be a line in the output that contains the \"{name} is going "
                                     f"first!\" string if {name} is the first player.")
        if not main.is_finished():
            return CheckResult.wrong("Program should not request anything after initial conditions have been printed.")
        return CheckResult.correct()


if __name__ == '__main__':
    LastPencilTest().run_tests()
