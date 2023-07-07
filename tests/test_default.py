from woke.testing import *

from pytypes.contracts.sudoku import SudokuValidator
import random

from typing import Tuple

SudokuRow = Tuple[int,int,int,int,int,int,int,int,int]
SudokuBoard = Tuple[SudokuRow,SudokuRow,SudokuRow,SudokuRow,SudokuRow,SudokuRow,SudokuRow,SudokuRow,SudokuRow]

def Validate(board : SudokuBoard) -> bool:
    def _validate(row : SudokuRow) -> bool:
        return False

    return True

def RandomBoard() -> SudokuBoard:
    values = [1,2,3,4,5,6,7,8,9]
    return [random.shuffle(values) for i in range(0,9)]

print(RandomBoard())

@default_chain.connect()
def test_default():
    default_chain.set_default_accounts(default_chain.accounts[0])
    sv = SudokuValidator.deploy()
    ret = sv._validate9([9,2,3,4,5,6,7,8,1])
    assert ret == True

@default_chain.connect()
def test_invalid():
    default_chain.set_default_accounts(default_chain.accounts[0])
    sv = SudokuValidator.deploy()
    board=[
            [1,2,3,4,5,6,7,8,9],
            [2,3,4,5,6,7,8,9,1],
            [3,4,5,6,7,8,9,1,2],
            [4,5,6,7,8,9,1,2,3],
            [5,6,7,8,9,1,2,3,4],
            [6,7,8,9,1,2,3,4,5],
            [7,8,9,1,2,3,4,5,6],
            [8,9,1,2,3,4,5,6,7],
            [9,1,2,3,4,5,6,7,8]
          ]
    
    with must_revert() as e:
        ret = sv.checkSudoku(board)
        

@default_chain.connect()
def test_valid():
    default_chain.set_default_accounts(default_chain.accounts[0])
    sv = SudokuValidator.deploy()
    board=[
            [1,2,3,6,7,8,9,4,5],
            [5,8,4,2,3,9,7,6,1],
            [9,6,7,1,4,5,3,2,8],
            [3,7,2,4,6,1,5,8,9],
            [6,9,1,5,8,3,2,7,4],
            [4,5,8,7,9,2,6,1,3],
            [8,3,6,9,2,4,1,5,7],
            [2,1,9,8,5,7,4,3,6],
            [7,4,5,3,1,6,8,9,2]
          ]
    


   
    assert sv.checkSudoku(board)==True
        