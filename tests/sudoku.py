from typing import Tuple
import random
import copy

from typing_extensions import Annotated

class Length:
    _length: int

    def __init__(self, length: int):
        self._length = length

    @property
    def length(self) -> int:
        return self._length



SudokuRow = Annotated[list[int], Length(9)]
SudokuBoard = Annotated[list[SudokuRow], Length(9)]

def RandomInvalidBoard() -> SudokuBoard:
    def _shuffle(values : SudokuRow) -> SudokuRow:
        v = copy.deepcopy(values)
        random.shuffle(v)
        x : SudokuRow  = v
        return x
    values = [1,2,3,4,5,6,7,8,9]
    board = [_shuffle(values) for i in range(0,9)]
    if Validate(board)[0]==False:
        return board
    return RandomInvalidBoard()

#rb = RandomBoard()
#for row in rb:
#    print("row", row)
#print(type(rb[0]))
from enum import Enum
class Reason(Enum):
    Valid = 0
    Row = 1
    Column = 2
    Box = 3

ValidateReturn = tuple[bool,Reason]
def Validate(board : SudokuBoard) -> ValidateReturn:
    def _validate(row : SudokuRow) -> bool:
        counts = [0 for i in range(0,10)]
        for r in row: 
            if r <= 0:
                return False
            if r > 9:
                return False
            counts[r] = counts[r] + 1
        return all([c==1 for c in counts[1:]])

    for row in board:
        if _validate(row) == False:
            return (False,Reason.Row)
    for col in range(0,9):        
        vals = [row[col] for row in board]
        #print(rb[0][2])
        #print(vals)
        if _validate(vals) == False:
            return (False,Reason.Column)
    for gr in range(0,3):
        for gc in range(0,3):
            vals = [board[gr * 3 + cr][gc*3 + cc] for cr in range(0,3) for cc in range(0,3)]
            if _validate(vals) == False:
                return (False,Reason.Box)

        
    return (True,Reason.Valid)

from dokusan import generators, renderers
from dokusan import solvers, renderers
from dokusan.boards import Sudoku

def RandomInvalidRange() -> SudokuBoard:
    vals = [0,1,2,3,4,5,6,7,8]

    board = RandomValidBoard()            
    row = random.choice(vals)
    col = random.choice(vals)
    board[row][col]=random.choice([0,10,11,245,254])
    return board

def RandomInvalidRow() -> SudokuBoard:
    vals = [0,1,2,3,4,5,6,7,8]

    board = RandomValidBoard()            
    reason = Reason.Valid
    while reason != Reason.Row:
        board = RandomValidBoard()  
        row1 = random.choice(vals)
        row2 = random.choice(vals)
        col = random.choice(vals)
        tmp = board[row1][col]
        board[row1][col] = board[row2][col]
        board[row2][col] = tmp
        valid,reason = Validate(board)
    return board

def RandomInvalidColumn() -> SudokuBoard:
    vals = [0,1,2,3,4,5,6,7,8]

    board = RandomValidBoard()            
    reason = Reason.Valid
    while reason != Reason.Column:
        board = RandomValidBoard()  
        col1 = random.choice(vals)
        col2 = random.choice(vals)
        row = random.choice(vals)
        tmp = board[row][col1]
        board[row][col1] = board[row][col2]
        board[row][col2] = tmp
        valid,reason = Validate(board)
    return board


def RandomInvalidBox() -> SudokuBoard:
    Boxs = [0,1,2]

    def Boxvalue(board, gr,gc,i,j): 
        return board[gr*3 +i][gc*3+j]

    def setvalue(board, gr,gc,i,j, value): 
        board[gr*3 +i][gc*3+j] = value
    
    def find(board, gr,gc, value): 
        for i in range(0,3):
            for j in range(0,3):
                if board[gr*3 +i][gc*3+j] == value:
                    return (True, i,j)
        return (False,0,0)
    
    def display(board):
        for row in board:
            print(row)
    
    board = RandomValidBoard()            
    reason = Reason.Valid
    while reason != Reason.Box:
        board = RandomValidBoard()  
        gcol1 = random.choice(Boxs)
        gcol2 = random.choice([g for g in Boxs if g != gcol1])
        grow1 = random.choice(Boxs)
        grow2 = random.choice([g for g in Boxs if g != grow1])
        

        #we have 2 Boxs from a row
        #now we choose a random location in Box 1
        r = random.choice(Boxs)
        c = random.choice(Boxs)
        value = Boxvalue(board,grow1,gcol1, r,c )

        found, frow,fcol = find(board, grow2,gcol2,value)

        if found:
            if frow != r:
                #swap
                tmp = Boxvalue(board,grow2,gcol2,frow,fcol)
                setvalue(board,grow2,gcol2,frow,fcol,Boxvalue(board,grow1,gcol2,r,fcol))
                setvalue(board,grow1,gcol2,r,fcol,tmp)

                setvalue(board,grow1,gcol1,r,c,Boxvalue(board,grow2,gcol1,frow,c))
                setvalue(board,grow2,gcol1,frow,c,value)

                            

        valid,reason = Validate(board)

    return board

def RandomValidBoard() -> SudokuBoard:
    sudoku = generators.random_sudoku(avg_rank=10)
    solution = solvers.backtrack(sudoku)
    
    return [[c.value for c in row] for row in solution.rows()]


    
