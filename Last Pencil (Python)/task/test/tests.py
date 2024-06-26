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

    @dynamic_test()
    def CheckNumericNumber(self):
        main = TestedProgram()
        main.start()
        for inp in ["a", "_", "test", "|", "|||||", " ", "-", "two", "10g", "k5", "-0.2", "0.3"]:
            output = main.execute(inp).lower()
            if ("number of pencils" not in output) or ("numeric" not in output):
                return CheckResult.wrong("When the user provides the number of pencils as a non-numeric sequence, the "
                                         "game should inform user that their input is incorrect and prompt the user "
                                         "for input again with the \"The number of pencils should be numeric\" string.")
        return CheckResult.correct()

    @dynamic_test()
    def CheckNotZeroNumber(self):
        main = TestedProgram()
        main.start()
        for i in range(1, 6):
            output = main.execute("0").lower()
            if ("number of pencils" not in output) or ("positive" not in output):
                return CheckResult.wrong("When the user provides \"0\" as a number of pencils, the game should "
                                         "inform the user that their input is incorrect and prompt the user for input "
                                         "again with the \"The number of pencils should be positive\" string.")
        return CheckResult.correct()

    @dynamic_test()
    def CheckBothIncorrect(self):
        main = TestedProgram()
        main.start()
        for inp in ['0', 'a', '0', '+']:
            check_str = 'positive' if inp == '0' else 'numeric'
            output = main.execute(inp).lower()
            if ("number of pencils" not in output) or (check_str not in output):
                return CheckResult.wrong(f"When the user provides \"{inp}\" as a number of pencils, the game should "
                                         f"inform the user that their input is incorrect and prompt the user for input "
                                         f"again with the \"The number of pencils should be {check_str}\" string.")
        output2 = main.execute("1").replace(" ", "")
        if not re.match(r".*\([a-zA-Z_0-9]+,[a-zA-Z_0-9]+\)", output2):
            return CheckResult.wrong("When the user inputs the number of pencils correctly, the game should ask "
                                     "who will be the first player ending with the \"(\"Name\", \"Name2\")\" string.")
        return CheckResult.correct()

    test_data = [
        [5, True, [2, 1], 2, 2],
        [20, True, [3, 2, 3, 1, 2, 3, 3, 2], 1, 2],
        [30, True, [3, 2, 3, 1, 2, 3, 3, 3, 2, 3, 3], 2, 1],
        [5, False, [2, 1], 2, 1],
        [20, False, [3, 2, 3, 1, 2, 3, 3, 2], 1, 1],
        [30, False, [3, 2, 3, 1, 2, 3, 3, 3, 2, 3, 3], 2, 2],
    ]

    @dynamic_test(data=test_data)
    def CheckGame(self, number, first_starts, moves, last, winner):
        main = TestedProgram()
        main.start()

        output = main.execute(str(number))
        output = output.replace(" ", "")

        if "who" not in output.lower() or 'first' not in output.lower():
            return CheckResult.wrong("The game should ask the user to input the player that goes first.")

        left_name = output[output.rfind('(') + 1:output.rfind(',')]
        right_name = output[output.rfind(',') + 1:output.rfind(')')]

        prev_player, next_player = (left_name, right_name) if first_starts else (right_name, left_name)

        output2 = main.execute(left_name + right_name).lower()
        if any(token not in output2 for token in ["choose between", left_name.lower(), right_name.lower()]):
            return CheckResult.wrong(f"When the user provides a name that is not '{left_name}' or '{right_name}', "
                                     f"the game should inform the user that their input is incorrect "
                                     f"and prompt the user for input again "
                                     f"with the \"Choose between '{left_name}' and '{right_name}'\" string.")

        output3 = main.execute(prev_player).lower()
        lines = [s for s in re.split(r'[\r\n]+', output3.strip()) if s != '']

        if len(lines) != 2:
            return CheckResult.wrong("When the player provides the initial game conditions, "
                                     "your program should print 2 non-empty lines:\n"
                                     "one with with vertical bar symbols representing the number of pencils, "
                                     "the other with the \"*NameX* turn\" string.\n"
                                     f"{len(lines)} lines were found in the output.")

        pencils = [s.strip() for s in lines if '|' in s]
        if len(pencils) != 1:
            return CheckResult.wrong("When the player provides the game initial conditions, "
                                     "your program should print only one line with several vertical bar "
                                     "symbols ('|') representing pencils.")
        if len(list(set(pencils[0]))) != 1:
            return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|' symbol.")

        if len(pencils[0]) != int(number):
            return CheckResult.wrong("The line with pencils should contain as many '|' symbols as the player provided.")

        if not any((prev_player.lower() in s) and ("turn" in s) for s in lines):
            return CheckResult.wrong(f"When the player provides the initial game conditions "
                                     f"there should be a line in output that contains the \"{prev_player}\'s turn\" "
                                     f"string if {prev_player} is the first player.")

        on_table = number

        for j in ["4", "a", "0", "-1", "_", "|", "|||||"]:
            output = main.execute(j).lower()
            if any(token not in output for token in ['possible values', '1', '2', '3']):
                return CheckResult.wrong(f"If the player enters values different from "
                                         f"'1', '2', or '3', the game should inform the user that "
                                         f"their input is incorrect and prompt the user for input again "
                                         f"with the \"Possible values: '1', '2', '3'\" string.")
            if prev_player.lower() not in output and next_player.lower() in output:
                return CheckResult.wrong(f"When {prev_player} provides values different from "
                                         f"'1', '2', or '3', you need to prompt {prev_player} for input again.\n"
                                         f"However, the {next_player}'s name was found in your output.")

        for i in moves:
            on_table -= i
            output = main.execute(str(i)).lower()
            lines = [s for s in re.split(r'[\r\n]+', output.strip()) if s != '']

            if len(lines) != 2:
                return CheckResult.wrong("When one of the players enters the number of pencils they want to remove, "
                                         "the program should print 2 non-empty lines.")

            pencils = [s.strip() for s in lines if '|' in s]
            if len(pencils) != 1:
                return CheckResult.wrong("When one of the players enters the number of pencils they want to remove, "
                                         "your program should print only one line with vertical bar symbols ('|') "
                                         "representing pencils.")
            if len(list(set(pencils[0]))) != 1:
                return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|'.")

            if len(pencils[0]) != on_table:
                return CheckResult.wrong("When one of the players enters the number of pencils they want to remove, "
                                         "the line with pencils should contain as many '|' symbols as there are "
                                         "pencils left.")
            if not any((next_player.lower() in s) and ("turn" in s) for s in lines):
                return CheckResult.wrong(f"When {prev_player} enters the number of pencils they want to remove "
                                         f"there should be a line in output that contains \"{next_player} turn\".")
            prev_player, next_player = next_player, prev_player

        output = main.execute(str(last + 1)).lower()
        if any(token not in output for token in ["too many", "pencils"]):
            return CheckResult.wrong("If the player enters the number of pencils that is greater than the current "
                                     "number of pencils on the table, the game should inform the user that "
                                     "their input is incorrect and prompt the user for input again "
                                     "with the \"too many pencils\" string.")

        output = main.execute(str(last)).lower()
        lines = [s for s in re.split(r'[\r\n]+', output.strip()) if s != '']

        winner_name = left_name if winner == 1 else right_name

        if len(lines) != 1 or (winner_name.lower() not in lines[0]) or (
                'win' not in lines[0] and 'won' not in lines[0]):
            if len(lines) >= 1:
                if winner_name.lower() not in lines[0] and ('win' in lines[0] or 'won' in lines[0]):
                    return CheckResult.wrong("Make sure you determined the winner of the game correctly.\n"
                                             "The player who takes the last pencil loses the game.")
            return CheckResult.wrong("When the last pencil is taken, the program should print one line that informs "
                                     "who is the winner in this game with \"*Name*\" and \"win\"/\"won\" strings.")

        if not main.is_finished():
            return CheckResult.wrong("Your program should not request anything when there are no pencils left.")
        return CheckResult.correct()


if __name__ == '__main__':
    LastPencilTest().run_tests()
