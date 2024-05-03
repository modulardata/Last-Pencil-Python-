import re

from hstest import *


class LastPencilTest(StageTest):
    @dynamic_test
    def test(self):
        main = TestedProgram()
        lines = [s for s in re.split(r'[\r\n]+', main.start().lower().strip()) if s != '']
        if len(lines) != 2:
            return CheckResult.wrong(f"Your program should print 2 non-empty lines.")
        pencils = [s for s in lines if '|' in s]
        if len(pencils) != 1:
            return CheckResult.wrong("The output should include only one line with several vertical bar "
                                     "symbols ('|') representing pencils.")
        if len(list(set(pencils[0]))) != 1:
            return CheckResult.wrong("The line with pencils should not contain any symbols other than the '|' symbol.")
        if not any("your turn" in s for s in lines):
            return CheckResult.wrong("The output should include one line with the \"Your turn\" string")
        return CheckResult.correct()


if __name__ == '__main__':
    LastPencilTest().run_tests()
