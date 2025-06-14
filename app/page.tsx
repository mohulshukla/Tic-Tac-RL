'use client';

import Link from 'next/link';
import { useState } from 'react';

export default function Home() {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [isXNext, setIsXNext] = useState(true);

  const calculateWinner = (squares: (string | null)[]) => {
    const lines = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
      [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
      [0, 4, 8], [2, 4, 6] // diagonals
    ];

    for (const [a, b, c] of lines) {
      if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
        return squares[a];
      }
    }
    return null;
  };

  const handleClick = (index: number) => {
    if (board[index] || calculateWinner(board)) return;
    
    const newBoard = [...board];
    newBoard[index] = isXNext ? 'X' : 'O';
    setBoard(newBoard);
    setIsXNext(!isXNext);
  };

  const winner = calculateWinner(board);
  const isDraw = !winner && board.every(square => square !== null);
  const status = winner 
    ? `Winner: ${winner}`
    : isDraw 
    ? "It's a draw!"
    : `Next player: ${isXNext ? 'X' : 'O'}`;

  const resetGame = () => {
    setBoard(Array(9).fill(null));
    setIsXNext(true);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 to-blue-100 dark:from-gray-900 dark:to-gray-800 flex flex-col items-center justify-center p-4">
      <h1 className="text-4xl font-bold mb-8 text-gray-800 dark:text-white">Tic Tac Toe</h1>
      
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl p-6 mb-8">
        <div className="text-xl font-semibold mb-4 text-center text-gray-700 dark:text-gray-200">
          {status}
        </div>
        
        <div className="grid grid-cols-3 gap-2">
          {board.map((square, index) => (
            <button
              key={index}
              onClick={() => handleClick(index)}
              className="w-20 h-20 bg-gray-100 dark:bg-gray-700 rounded-lg text-3xl font-bold 
                       hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors
                       flex items-center justify-center text-gray-800 dark:text-white
                       disabled:cursor-not-allowed disabled:opacity-70"
              disabled={winner !== null || square !== null}
            >
              {square}
            </button>
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
