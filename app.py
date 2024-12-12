from flask import Flask, render_template, session, redirect, url_for, request
import random
from copy import deepcopy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш секретный ключ

@app.route('/')
def index():
    # Инициализируем игровое поле, если нужно
    if 'board' not in session or 'player' not in session:
        session['board'] = ['' for _ in range(9)]
        session['player'] = 'X'
        session['winner'] = None
    return render_template('index.html', board=session['board'], player=session['player'], winner=session.get('winner'))

@app.route('/move/<int:cell>')
def move(cell):
    board = session.get('board', ['' for _ in range(9)])
    player = session.get('player', 'X')
    winner = session.get('winner', None)

    if board[cell] == '' and not winner:
        board[cell] = player
        winner = check_winner(board)
        if winner or '' not in board:
            session['winner'] = winner if winner else 'Ничья'
        else:
            # Смена игрока
            player = 'O' if player == 'X' else 'X'
    session['board'] = board
    session['player'] = player
    session['winner'] = winner
    return redirect(url_for('index'))

@app.route('/reset')
def reset():
    session.pop('board', None)
    session.pop('player', None)
    session.pop('winner', None)
    return redirect(url_for('index'))

def check_winner(board):
    # Возможные выигрышные комбинации
    win_conditions = [
        [0, 1, 2],  # Первая строка
        [3, 4, 5],  # Вторая строка
        [6, 7, 8],  # Третья строка
        [0, 3, 6],  # Первый столбец
        [1, 4, 7],  # Второй столбец
        [2, 5, 8],  # Третий столбец
        [0, 4, 8],  # Диагональ из левого верхнего угла
        [2, 4, 6]   # Диагональ из правого верхнего угла
    ]
    for condition in win_conditions:
        a, b, c = condition
        if board[a] == board[b] == board[c] and board[a] != '':
            return board[a]
    return None

if __name__ == '__main__':
    app.run(debug=True)