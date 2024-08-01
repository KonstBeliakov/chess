# Chess
Chess against a bot
### How to install a project
1. Clone the repository
2. Execute `pip install -t requirements.txt`
3. Open `main.py`
---
### Gameplay
You are playing for white against a bot.  
Select a piece and choose one of valid moves (they will be highlighted with green circles)
![Gameplay](/img1.png)
### How bot works
This project is a chess game against a bot written using the mini-max algorithm and alpha-beta puring optimization.  
The bot evaluates positions in which knights and pawns are in the center of the board higher, which allows him to play
relatively well in the opening  
##### Here are tables of the values of different pieces depending on their position on the board:
```python
knight_value = [[2.5, 2.7, 2.8, 2.8, 2.8, 2.8, 2.7, 2.5],
                [2.7, 2.8, 2.9, 2.9, 2.9, 2.9, 2.8, 2.7],
                [2.8, 2.9, 3.0, 3.0, 3.0, 3.0, 2.9, 2.8],
                [2.8, 2.9, 3.0, 3.0, 3.0, 3.0, 2.9, 2.8],
                [2.8, 2.9, 3.0, 3.0, 3.0, 3.0, 2.9, 2.8],
                [2.8, 2.9, 3.0, 3.0, 3.0, 3.0, 2.9, 2.8],
                [2.7, 2.8, 2.9, 2.9, 2.9, 2.9, 2.8, 2.7],
                [2.5, 2.7, 2.8, 2.8, 2.8, 2.8, 2.7, 2.5]]

bishop_value = [[2.7, 2.85, 2.85, 2.85, 2.85, 2.85, 2.85, 2.7],
                [2.85, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.85],
                [2.85, 3.0, 3.05, 3.05, 3.05, 3.05, 3.0, 2.85],
                [2.85, 3.0, 3.05, 3.1, 3.1, 3.05, 3.0, 2.85],
                [2.85, 3.0, 3.05, 3.1, 3.1, 3.05, 3.0, 2.85],
                [2.85, 3.0, 3.05, 3.05, 3.05, 3.05, 3.0, 2.85],
                [2.85, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 2.85],
                [2.7, 2.85, 2.85, 2.85, 2.85, 2.85, 2.85, 2.7]]

pawn_value = [[1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1.05, 1.05, 1, 1, 1],
              [1, 1, 1, 1.35, 1.35, 1, 1, 1],
              [1, 1, 1, 1.35, 1.35, 1, 1, 1],
              [1, 1, 1, 1.05, 1.05, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1]]
```
---
*Thank you for your interest in my project!*