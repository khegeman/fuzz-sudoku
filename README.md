

# Fuzz Testing Solidity with Woke



The contract implements the following simple interface 

```solidity
interface Sudoku {
    function checkSudoku(uint8[9][9] calldata board) external pure returns (bool);
}
```



Using the [Woke](https://ackeeblockchain.com/woke/docs/latest/) fuzz testing framework, I constructed fuzz tests that cover different rule checks for sudoku.  




## Fuzzing Data Generation

One of the challenges to get full fuzz-based coverage of the solidty function is to generate random sudoku boards with different properties so that we can test all aspects of checkSudoku.  For instance, we need test data where all the rows are valid, but one or more of the columns violate the rules.  We also need to test that we properly check the 3x3 boxes, so we need to generate a board where the rows and columns pass all the rules, but one of the 3x3 boxes is invalid.   Trying to find boxes with these properties with purely random generation is extremely inefficient. It turns out it's much easier to get a board with the desired properties by starting with a valid board and then exchanging values between rows and columns to break the desired rule.  Since we are using woke and it is python based, we have full access to the python ecosystem, we can use a library that generates random sudoku boards.I found this library with a quick google search.  [GitHub - unmade/dokusan: Sudoku generator and solver with step-by-step guidance](https://github.com/unmade/dokusan)  Then I built on top of it to create functions like RandomValidBoard, RandomInvalidRow, RandomInvalidColumn, RandomInvalidBox.  Finally, I the used functions to build the appropriate fuzz tests.



`checkSudoku` is a pure function, so I didn't use flow based testing with state.  I set `flow_count=1` and ran large numbers of sequences to test.

```python
SudokuFuzzTest().run(sequences_count=1000, flows_count=1)  
```



## Running The Tests

```
woke fuzz tests/test_fuzz.py
```



  




