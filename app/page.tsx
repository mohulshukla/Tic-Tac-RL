'use client';

import { useState, useEffect } from 'react';

interface SingleGrid {
  grid: (string | null)[][];
  winner: string | null;
}

export default function Home() {
  const [bigGrid, setBigGrid] = useState<SingleGrid[][]>(
    Array(3).fill(null).map(() => 
      Array(3).fill(null).map(() => ({
        grid: Array(3).fill(null).map(() => Array(3).fill(null)),
        winner: null
      }))
    )
  );
  const [currentPlayer, setCurrentPlayer] = useState<'X' | 'O'>('X');
  const [nextGridIndex, setNextGridIndex] = useState<number | null>(4); // Start in middle grid
  const [gameWinner, setGameWinner] = useState<string | null>(null);

  const checkSmallGridWinner = (grid: (string | null)[][]) => {
    const lines = [
      // Rows
      [[0, 0], [0, 1], [0, 2]],
      [[1, 0], [1, 1], [1, 2]],
      [[2, 0], [2, 1], [2, 2]],
      // Columns
      [[0, 0], [1, 0], [2, 0]],
      [[0, 1], [1, 1], [2, 1]],
      [[0, 2], [1, 2], [2, 2]],
      // Diagonals
      [[0, 0], [1, 1], [2, 2]],
      [[0, 2], [1, 1], [2, 0]]
    ];

    for (const line of lines) {
      const [a, b, c] = line;
      if (
        grid[a[0]][a[1]] &&
        grid[a[0]][a[1]] === grid[b[0]][b[1]] &&
        grid[a[0]][a[1]] === grid[c[0]][c[1]]
      ) {
        return grid[a[0]][a[1]];
      }
    }

    // Check for draw
    if (grid.every(row => row.every(cell => cell !== null))) {
      return 'D';
    }

    return null;
  };

  const checkBigGridWinner = () => {
    const bigGridState = bigGrid.map(row => 
      row.map(cell => cell.winner)
    );

    const lines = [
      // Rows
      [[0, 0], [0, 1], [0, 2]],
      [[1, 0], [1, 1], [1, 2]],
      [[2, 0], [2, 1], [2, 2]],
      // Columns
      [[0, 0], [1, 0], [2, 0]],
      [[0, 1], [1, 1], [2, 1]],
      [[0, 2], [1, 2], [2, 2]],
      // Diagonals
      [[0, 0], [1, 1], [2, 2]],
      [[0, 2], [1, 1], [2, 0]]
    ];

    for (const line of lines) {
      const [a, b, c] = line;
      if (
        bigGridState[a[0]][a[1]] &&
        bigGridState[a[0]][a[1]] === bigGridState[b[0]][b[1]] &&
        bigGridState[a[0]][a[1]] === bigGridState[c[0]][c[1]]
      ) {
        return bigGridState[a[0]][a[1]];
      }
    }

    // Check for draw
    if (bigGridState.every(row => row.every(cell => cell !== null))) {
      return 'D';
    }

    return null;
  };

  const handleCellClick = (bigRow: number, bigCol: number, smallRow: number, smallCol: number) => {
    // If there's a game winner or the cell is already filled, do nothing
    if (gameWinner || bigGrid[bigRow][bigCol].grid[smallRow][smallCol] !== null) {
      return;
    }

    // If nextGridIndex is set, only allow moves in that grid
    if (nextGridIndex !== null) {
      const targetRow = Math.floor(nextGridIndex / 3);
      const targetCol = nextGridIndex % 3;
      
      // If the target grid is already won/drawn, allow move in any available grid
      if (bigGrid[targetRow][targetCol].winner) {
        // Allow move in any grid that isn't won/drawn
        if (bigGrid[bigRow][bigCol].winner) {
          return;
        }
      } else if (targetRow !== bigRow || targetCol !== bigCol) {
        return;
      }
    }

    // Make the move
    const newBigGrid = [...bigGrid];
    newBigGrid[bigRow][bigCol].grid[smallRow][smallCol] = currentPlayer;
    setBigGrid(newBigGrid);

    // Check if the small grid has a winner
    const smallGridWinner = checkSmallGridWinner(newBigGrid[bigRow][bigCol].grid);
    if (smallGridWinner) {
      newBigGrid[bigRow][bigCol].winner = smallGridWinner;
      setBigGrid(newBigGrid);
    }

    // Check if the big grid has a winner
    const bigGridWinner = checkBigGridWinner();
    if (bigGridWinner) {
      setGameWinner(bigGridWinner);
      return;
    }

    // Set next grid index based on the position played
    const nextIndex = smallRow * 3 + smallCol;
    
    // Check if the next grid is already won/drawn
    const nextRow = Math.floor(nextIndex / 3);
    const nextCol = nextIndex % 3;
    if (newBigGrid[nextRow][nextCol].winner) {
      // If next grid is won/drawn, set nextGridIndex to null to allow any grid
      setNextGridIndex(null);
    } else {
      setNextGridIndex(nextIndex);
    }

    // Switch players
    setCurrentPlayer(currentPlayer === 'X' ? 'O' : 'X');
  };

  const resetGame = () => {
    setBigGrid(
      Array(3).fill(null).map(() => 
        Array(3).fill(null).map(() => ({
          grid: Array(3).fill(null).map(() => Array(3).fill(null)),
          winner: null
        }))
      )
    );
    setCurrentPlayer('X');
    setNextGridIndex(4);
    setGameWinner(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 to-blue-100 dark:from-gray-900 dark:to-gray-800 flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-8 text-gray-800 dark:text-white">Ultimate Tic Tac Toe</h1>
      
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl p-6 mb-8">
        <div className="text-xl font-semibold mb-4 text-center text-gray-700 dark:text-gray-200">
          {gameWinner 
            ? `Winner: ${gameWinner === 'D' ? 'Draw!' : gameWinner}`
            : nextGridIndex === null
              ? `Next player: ${currentPlayer} (Pick any available grid)`
              : `Next player: ${currentPlayer}`}
        </div>
        
        <div className="grid grid-cols-3 gap-4">
          {bigGrid.map((bigRow, bigRowIndex) => (
            bigRow.map((bigCell, bigColIndex) => (
              <div 
                key={`${bigRowIndex}-${bigColIndex}`}
                className={`grid grid-cols-3 gap-1 p-2 rounded-lg ${
                  nextGridIndex === bigRowIndex * 3 + bigColIndex 
                    ? 'bg-green-100 dark:bg-green-900' 
                    : 'bg-gray-100 dark:bg-gray-700'
                }`}
              >
                {bigCell.winner ? (
                  <div className="col-span-3 row-span-3 flex items-center justify-center text-4xl font-bold">
                    {bigCell.winner}
                  </div>
                ) : (
                  bigCell.grid.map((smallRow, smallRowIndex) => (
                    smallRow.map((cell, smallColIndex) => (
                      <button
                        key={`${smallRowIndex}-${smallColIndex}`}
                        onClick={() => handleCellClick(bigRowIndex, bigColIndex, smallRowIndex, smallColIndex)}
                        className="w-12 h-12 bg-white dark:bg-gray-600 rounded text-xl font-bold 
                                 hover:bg-gray-200 dark:hover:bg-gray-500 transition-colors
                                 flex items-center justify-center text-gray-800 dark:text-white
                                 disabled:cursor-not-allowed disabled:opacity-70"
                        disabled={gameWinner !== null || cell !== null}
                      >
                        {cell}
                      </button>
                    ))
                  ))
                )}
              </div>
            ))
          ))}
        </div>
      </div>

      <button
        onClick={resetGame}
        className="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg
                 font-semibold transition-colors shadow-lg hover:shadow-xl"
      >
        Reset Game
      </button>
    </div>
  );
}

