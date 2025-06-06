import tkinter as tk
from tkinter import messagebox
import random


words = ["питон", "программа", "компьютер", "клавиатура", "монитор", "мышка"
        "алгоритм", "байт", "бит", "браузер", "веб","вирус", "диск", "драйвер",
         "интернет", "кабель", "код", "курсор", "лан", "линк", "массив", "модем",
         "память", "пароль", "пиксель", "порт", "поиск", "процесс", "работа",
         "сервер", "система", "сканер", "сокет", "софт", "спам", "трафик", "файл",
         "фича", "флешка", "хакер", "цикл", "чарт", "чип", "шрифт", "экран"]
max_attempts = 7

BG_COLOR = "#000000"
BUTTON_COLOR = "#000000"
CORRECT_COLOR = "#8696FF"  # правильных букв
WRONG_COLOR = "#FF3B8B"   # для неправильных
TEXT_COLOR = "#ffffff"
DISABLED_TEXT_COLOR = "#ffffff"  # для отключенных кнопок
DRAWING_COLOR = "#ffffff"

secret_word = ""
guessed_letters = []
attempts_left = max_attempts
wins = 0
losses = 0


def draw_hangman(step):
    hangman_canvas.delete("all")
    if step >= 1: hangman_canvas.create_line(100, 320, 280, 320, width=8, fill=DRAWING_COLOR)
    if step >= 2: hangman_canvas.create_line(190, 320, 190, 70, width=6, fill=DRAWING_COLOR)
    if step >= 3: hangman_canvas.create_line(190, 70, 280, 70, width=6, fill=DRAWING_COLOR)
    if step >= 4: hangman_canvas.create_line(280, 70, 280, 100, width=3, fill=DRAWING_COLOR)
    if step >= 5: hangman_canvas.create_oval(265, 100, 295, 130, width=3, outline=DRAWING_COLOR)
    if step >= 6: hangman_canvas.create_line(280, 130, 280, 200, width=3, fill=DRAWING_COLOR)
    if step >= 7:
        hangman_canvas.create_line(280, 150, 250, 180, width=3, fill=DRAWING_COLOR)
        hangman_canvas.create_line(280, 150, 310, 180, width=3, fill=DRAWING_COLOR)
        hangman_canvas.create_line(280, 200, 250, 250, width=3, fill=DRAWING_COLOR)
        hangman_canvas.create_line(280, 200, 310, 250, width=3, fill=DRAWING_COLOR)


def update_display():
    word_label.config(text="   ".join([l if l in guessed_letters else "_" for l in secret_word]))
    stats_label.config(text=f"Побед: {wins}  Поражений: {losses}")
    attempts_label.config(text=f"Попыток осталось: {attempts_left}")


def reset_buttons():
    for btn in letter_buttons:
        btn.config(state=tk.NORMAL, bg=BUTTON_COLOR, fg=TEXT_COLOR)


def guess_letter(letter):
    global attempts_left, wins, losses

    if letter in guessed_letters:
        return

    guessed_letters.append(letter)
    correct = letter in secret_word

    for btn in letter_buttons:
        if btn['text'].lower() == letter:
            color = CORRECT_COLOR if correct else WRONG_COLOR
            btn.config(bg=color, fg=DISABLED_TEXT_COLOR, state=tk.DISABLED)
            break

    if not correct:
        attempts_left -= 1
        draw_hangman(max_attempts - attempts_left)

    update_display()

    if all(letter in guessed_letters for letter in secret_word):
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

root = tk.Tk()
root.title("Виселица")
root.state('zoomed')
root.configure(bg=BG_COLOR)

# Виджеты
hangman_canvas = tk.Canvas(root, width=400, height=350, bg=BG_COLOR, highlightthickness=0)
hangman_canvas.pack(pady=(12, 12))

word_label = tk.Label(root, font=("Arial", 42), bg=BG_COLOR, fg=TEXT_COLOR)
word_label.pack(pady=0)

stats_label = tk.Label(root, font=("Arial", 18), bg=BG_COLOR, fg=TEXT_COLOR)
stats_label.pack(pady=5)

attempts_label = tk.Label(root, font=("Arial", 18), bg=BG_COLOR, fg=TEXT_COLOR)
attempts_label.pack(pady=(5, 15))

# Кнопки букв (3 ряда)
keyboard_frames = []
for i in range(3):
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(pady=5)
    keyboard_frames.append(frame)

letters_rows = ["абвгдеёжзий", "клмнопрстуфх", "цчшщъыьэюя"]
letter_buttons = []

for i, row in enumerate(letters_rows):
    for letter in row:
        btn = tk.Button(
            keyboard_frames[i],
            text=letter.upper(),
            font=("Arial", 14, "bold"),
            width=4,
            height=2,
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            activebackground="#555555",
            activeforeground=TEXT_COLOR,
            disabledforeground=DISABLED_TEXT_COLOR,
            command=lambda l=letter: guess_letter(l)
        )
        btn.pack(side="left", padx=4, pady=4)
        letter_buttons.append(btn)

# Начало игры
new_game()
root.mainloop()