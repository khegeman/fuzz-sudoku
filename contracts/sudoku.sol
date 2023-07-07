// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.15;

interface Sudoku {
    function checkSudoku(uint8[9][9] calldata board) external pure returns (bool);
}

contract SudokuValidator is Sudoku {
    error InvalidBox(uint256, uint256);
    error InvalidColumn(uint256);
    error InvalidRow(uint256);

    error OutOfRange(uint8);

    function _validate9(uint8[9] memory group) internal pure returns (bool) {
        uint8[10] memory counts;

        for (uint256 i = 0; i < 9; ++i) {
            uint8 value = group[i];
            if (value > 9 || value < 1) {
                revert OutOfRange(value);
            }

            counts[value] += 1;
        }
        for (uint256 i = 1; i < 10; ++i) {
            if (counts[i] != 1) {
                return false;
            }
        }
        return true;
    }

    function checkSudoku(uint8[9][9] calldata board) external pure returns (bool) {
        for (uint256 row = 0; row < 9; row++) {
            if (_validate9(board[row]) == false) {
                //return false;
                revert InvalidRow(row);
            }
        }
        uint8[9] memory scratch;
        for (uint256 col = 0; col < 9; col++) {
            for (uint256 row = 0; row < 9; row++) {
                scratch[row] = board[row][col];
            }
            if (_validate9(scratch) == false) {
                revert InvalidColumn(col);
            }
        }

        for (uint256 boxrow = 0; boxrow < 3; boxrow++) {
            for (uint256 boxcol = 0; boxcol < 3; boxcol++) {
                for (uint256 crow = 0; crow < 3; crow++) {
                    for (uint256 ccol = 0; ccol < 3; ccol++) {
                        scratch[crow * 3 + ccol] = board[boxrow * 3 + crow][boxcol * 3 + ccol];
                    }
                }
                if (_validate9(scratch) == false) {
                    revert InvalidBox(boxrow, boxcol);
                    //return false;
                }
            }
        }

        return true;
    }
}
