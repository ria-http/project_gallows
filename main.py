import tkinter as tk
from tkinter import messagebox
import random

# Настройки игры
words = ["питон", "программа", "компьютер", "клавиатура", "монитор", "мышка"]
max_attempts = 7

# Цвета
BG_COLOR = "#f0f8ff"
BUTTON_COLOR = "#e6e6fa"
CORRECT_COLOR = "#2e8b57"
WRONG_COLOR = "#cd5c5c"

# Инициализация игры
secret_word = ""
guessed_letters = []
attempts_left = max_attempts
wins = 0
losses = 0


# Функции
def draw_hangman(step):
    hangman_canvas.delete("all")
    if step >= 1: hangman_canvas.create_line(100, 320, 280, 320, width=8)
    if step >= 2: hangman_canvas.create_line(190, 320, 190, 70, width=6)
    if step >= 3: hangman_canvas.create_line(190, 70, 280, 70, width=6)
    if step >= 4: hangman_canvas.create_line(280, 70, 280, 100, width=3)
    if step >= 5: hangman_canvas.create_oval(265, 100, 295, 130, width=3)
    if step >= 6: hangman_canvas.create_line(280, 130, 280, 200, width=3)
    if step >= 7:
        hangman_canvas.create_line(280, 150, 250, 180, width=3)
        hangman_canvas.create_line(280, 150, 310, 180, width=3)
        hangman_canvas.create_line(280, 200, 250, 250, width=3)
        hangman_canvas.create_line(280, 200, 310, 250, width=3)


def update_display():
    word_label.config(text="   ".join([l if l in guessed_letters else "_" for l in secret_word]))
    stats_label.config(text=f"Побед: {wins}  Поражений: {losses}")
    attempts_label.config(text=f"Попыток осталось: {attempts_left}")
    used_letters = " ".join(sorted(guessed_letters))
    used_letters_label.config(text=f"Использованные буквы: {used_letters}")


def reset_buttons():
    for btn in letter_buttons:
        btn.config(state=tk.NORMAL, bg=BUTTON_COLOR)


def guess_letter(letter):
    global attempts_left, wins, losses

    if letter in guessed_letters: return

    guessed_letters.append(letter)
    correct = letter in secret_word

    for btn in letter_buttons:
        if btn['text'].lower() == letter:
            btn.config(bg=CORRECT_COLOR if correct else WRONG_COLOR, state=tk.DISABLED)
            break

    if not correct:
        attempts_left -= 1
        draw_hangman(max_attempts - attempts_left + 1)

    update_display()

    if set(secret_word) <= set(guessed_letters):
        wins += 1
        messagebox.showinfo("Победа!", "Вы угадали слово!")
        new_game()
    elif attempts_left == 0:
        losses += 1
        word_label.config(text="   ".join(secret_word))
        messagebox.showinfo("Проигрыш", f"Слово было: {secret_word}")
        new_game()

def new_game():
    global secret_word, guessed_letters, attempts_left
    secret_word = random.choice(words)
    guessed_letters = []
    attempts_left = max_attempts
    reset_buttons()
    update_display()
    draw_hangman(0)


def restart_game():
    global guessed_letters, attempts_left
    if not secret_word: return
    guessed_letters = []
    attempts_left = max_attempts
    reset_buttons()
    update_display()
    draw_hangman(0)


# Создание окна
root = tk.Tk()
root.title("Виселица")
root.state('zoomed')
root.configure(bg=BG_COLOR)

# Виджеты
hangman_canvas = tk.Canvas(root, width=400, height=350, bg=BG_COLOR)
hangman_canvas.pack(pady=10)

word_label = tk.Label(root, font=("Arial", 42), bg=BG_COLOR)
word_label.pack(pady=10)

stats_label = tk.Label(root, font=("Arial", 16), bg=BG_COLOR)
stats_label.pack()

attempts_label = tk.Label(root, font=("Arial", 16), bg=BG_COLOR)
attempts_label.pack()

used_letters_label = tk.Label(root, font=("Arial", 16), bg=BG_COLOR)
used_letters_label.pack(pady=5)

# Кнопки букв (3 ряда)
keyboard_frames = []
for i in range(3):
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack()
    keyboard_frames.append(frame)

letters_rows = ["абвгдеёжзийкл", "мнопрстуфхцчшщ", "ъыьэюя"]
letter_buttons = []

for i, row in enumerate(letters_rows):
    for letter in row:
        btn = tk.Button(
            keyboard_frames[i],
            text=letter.upper(),
            font=("Arial", 14),
            width=4,
            height=2,
            bg=BUTTON_COLOR,
            command=lambda l=letter: guess_letter(l)
        )
        btn.pack(side="left", padx=2, pady=2)
        letter_buttons.append(btn)

# Начало игры
new_game()
root.mainloop()