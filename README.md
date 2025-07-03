# Wordle Helper (Python Edition - Frequency Scoring)

A command-line Python tool to help you solve Wordle puzzles by filtering and ranking five-letter word guesses based on your clues.  
You provide the green (correct spot), yellow (wrong spot), and gray (eliminated) letter clues interactively.  
The script filters a word list and scores the remaining words by letter frequency to suggest the most strategic guesses.

---

## Features

- **Green (🟩) support:** Enter letters in their known correct positions (`..e.r` for unknowns).
- **Yellow (🟨) support:** Specify letters known to be in the word but in the wrong position (format: `..k..`).
- **Gray (⬜) support:** Enter all eliminated letters (e.g., `shnt`).
- **Smart Ranking:** Suggests the best guesses using letter frequency among possible words, to help maximize your information gain per guess.
- **Interactive:** Keeps filtering and suggesting until you find the word or quit.

---

## Requirements

- Python 3 (recommended 3.6+)

---

## Setup

1. **Clone this repo** or download the script file.

2. **Prepare a Word List**

   - The script expects a file named `list_wordles.txt` in the same directory, containing one five-letter word per line.
