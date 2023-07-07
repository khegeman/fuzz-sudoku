from woke.testing import *
from woke.testing.fuzzing import *
from .sudoku import RandomValidBoard,RandomInvalidRange,RandomInvalidRow,RandomInvalidColumn,RandomInvalidBox
from pytypes.contracts.sudoku import SudokuValidator
import random

random.seed(33)


class SudokuFuzzTest(FuzzTest):
    validator : SudokuValidator
    
    def pre_sequence(self) -> None:
        self.validator = SudokuValidator.deploy()
    @flow()
    def flow_valid_board(self) -> None:

        assert self.validator.checkSudoku(RandomValidBoard())
    @flow()
    def flow_out_of_range(self) -> None:

        with must_revert(SudokuValidator.OutOfRange) as e:
            valid = self.validator.checkSudoku(RandomInvalidRange())


    @flow()
    def flow_invalid_box(self) -> None:
        board = RandomInvalidBox()

        with must_revert(SudokuValidator.InvalidBox) as e:
            valid = self.validator.checkSudoku(board)
#        
    @flow()
    def flow_invalid_row(self) -> None:
        board = RandomInvalidRow()
        with must_revert(SudokuValidator.InvalidRow) as e:
            valid = self.validator.checkSudoku(board)

    @flow()
    def flow_invalid_column(self) -> None:
        board = RandomInvalidColumn()

        with must_revert(SudokuValidator.InvalidColumn) as e:
            valid = self.validator.checkSudoku(board)                    



@default_chain.connect()
def test_sudoku_fuzz():
    default_chain.set_default_accounts(default_chain.accounts[0])
    SudokuFuzzTest().run(sequences_count=1000, flows_count=1)        