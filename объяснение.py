# Импорт необходимых библиотек
import tkinter as tk  # для графического интерфейса
from tkinter import messagebox  # для всплывающих сообщений
import random  # для случайного выбора слова

# Настройки игры
words = ["питон", "программа", "компьютер", "клавиатура", "монитор", "мышка"]  # список слов для угадывания
max_attempts = 7  # количество допустимых ошибок

# Цветовая схема интерфейса
BG_COLOR = "#f0f8ff"  # цвет фона (AliceBlue)
BUTTON_COLOR = "#e6e6fa"  # цвет кнопок (Lavender)
CORRECT_COLOR = "#2e8b57"  # цвет правильных букв (SeaGreen)
WRONG_COLOR = "#cd5c5c"  # цвет неправильных букв (IndianRed)

# Инициализация глобальных переменных игры
secret_word = ""  # здесь будет храниться загаданное слово
guessed_letters = []  # список уже названных букв
attempts_left = max_attempts  # счетчик оставшихся попыток
wins = 0  # счетчик побед
losses = 0  # счетчик поражений


# ========== ОПРЕДЕЛЕНИЕ ФУНКЦИЙ ==========

def draw_hangman(step):
    """Рисует виселицу с человечком в зависимости от количества ошибок"""
    hangman_canvas.delete("all")  # очищаем холст

    #Canvas — объект библиотеки Tkinter в языке Python, который позволяет создавать двухмерную графику, текст и изображения.
    # Рисуем виселицу по шагам (каждая ошибка добавляет новый элемент)
    if step >= 1: hangman_canvas.create_line(100, 320, 280, 320, width=8)  # основание
    if step >= 2: hangman_canvas.create_line(190, 320, 190, 70, width=6)  # столб
    if step >= 3: hangman_canvas.create_line(190, 70, 280, 70, width=6)  # перекладина
    if step >= 4: hangman_canvas.create_line(280, 70, 280, 100, width=3)  # веревка
    if step >= 5: hangman_canvas.create_oval(265, 100, 295, 130, width=3)  # голова
    if step >= 6: hangman_canvas.create_line(280, 130, 280, 200, width=3)  # тело
    if step >= 7:
        # Последняя ошибка - рисуем конечности
        hangman_canvas.create_line(280, 150, 250, 180, width=3)  # левая рука
        hangman_canvas.create_line(280, 150, 310, 180, width=3)  # правая рука
        hangman_canvas.create_line(280, 200, 250, 250, width=3)  # левая нога
        hangman_canvas.create_line(280, 200, 310, 250, width=3)  # правая нога


def update_display():
    """Обновляет все элементы интерфейса"""
    # Обновляем отображение слова (открываем угаданные буквы)
    word_label.config(text="   ".join([l if l in guessed_letters else "_" for l in secret_word]))
    # Обновляем статистику
    stats_label.config(text=f"Побед: {wins}  Поражений: {losses}")
    # Обновляем счетчик попыток
    attempts_label.config(text=f"Попыток осталось: {attempts_left}")
    # Формируем строку использованных букв
    used_letters = " ".join(sorted(guessed_letters))
    used_letters_label.config(text=f"Использованные буквы: {used_letters}")


def reset_buttons():
    """Сбрасывает все кнопки букв в исходное состояние"""
    for btn in letter_buttons:
        btn.config(state=tk.NORMAL, bg=BUTTON_COLOR)  # делаем активными и возвращаем исходный цвет


def guess_letter(letter):
    """Обрабатывает выбор буквы игроком"""
    global attempts_left, wins, losses  # используем глобальные переменные

    # Если буква уже называлась - ничего не делаем
    if letter in guessed_letters: return

    # Добавляем букву в список использованных
    guessed_letters.append(letter)
    correct = letter in secret_word  # проверяем, есть ли буква в слове

    # Находим кнопку этой буквы и меняем ее вид
    for btn in letter_buttons:
        if btn['text'].lower() == letter:
            # Меняем цвет в зависимости от правильности
            btn.config(bg=CORRECT_COLOR if correct else WRONG_COLOR, state=tk.DISABLED)
            break

    # Если буквы нет в слове
    if not correct:
        attempts_left -= 1  # уменьшаем количество попыток
        draw_hangman(max_attempts - attempts_left + 1)  # рисуем следующую часть виселицы

    update_display()  # обновляем интерфейс

    # Проверяем условия окончания игры
    if set(secret_word) <= set(guessed_letters):  # если все буквы угаданы
        wins += 1  # увеличиваем счетчик побед
        messagebox.showinfo("Победа!", "Вы угадали слово!")  # показываем сообщение
        new_game()  # запуск новой игры
    elif attempts_left == 0:  # если попытки закончились
        losses += 1  # увеличиваем счетчик поражений
        word_label.config(text="   ".join(secret_word))  # показываем загаданное слово
        messagebox.showinfo("Проигрыш", f"Слово было: {secret_word}")  # сообщение о проигрыше
        new_game()  # запуск новой игры

def new_game():
    """Начинает новую игру с новым случайным словом"""
    global secret_word, guessed_letters, attempts_left
    secret_word = random.choice(words)  # выбираем случайное слово
    guessed_letters = []  # очищаем список угаданных букв
    attempts_left = max_attempts  # сбрасываем счетчик попыток
    reset_buttons()  # сбрасываем кнопки
    update_display()  # обновляем интерфейс
    draw_hangman(0)  # рисуем пустую виселицу


def restart_game():
    """Начинает текущее слово заново"""
    global guessed_letters, attempts_left
    if not secret_word: return  # если слова нет - выходим
    guessed_letters = []  # очищаем список угаданных букв
    attempts_left = max_attempts  # сбрасываем счетчик попыток
    reset_buttons()  # сбрасываем кнопки
    update_display()  # обновляем интерфейс
    draw_hangman(0)  # рисуем пустую виселицу


# ========== СОЗДАНИЕ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА ==========

# Создаем главное окно
root = tk.Tk()
root.title("Виселица")  # заголовок окна
root.state('zoomed')  # размеры окна
root.configure(bg=BG_COLOR)  # цвет фона

# Создаем холст для рисования виселицы
hangman_canvas = tk.Canvas(root, width=400, height=350, bg=BG_COLOR)
hangman_canvas.pack(pady=10)  # размещаем с отступом сверху

# Создаем метку для отображения слова
word_label = tk.Label(root, font=("Arial", 42), bg=BG_COLOR)
word_label.pack(pady=10)

# Создаем метку для статистики
stats_label = tk.Label(root, font=("Arial", 16), bg=BG_COLOR)
stats_label.pack()

# Создаем метку для отображения оставшихся попыток
attempts_label = tk.Label(root, font=("Arial", 16), bg=BG_COLOR)
attempts_label.pack()

# Создаем метку для отображения использованных букв
used_letters_label = tk.Label(root, font=("Arial", 16), bg=BG_COLOR)
used_letters_label.pack(pady=5)

# Создаем фреймы для кнопок букв (3 ряда)
keyboard_frames = []  # список для хранения фреймов
for i in range(3):
    frame = tk.Frame(root, bg=BG_COLOR)  # создаем фрейм
    frame.pack()  # размещаем фрейм
    keyboard_frames.append(frame)  # добавляем в список

# Распределяем буквы по рядам
letters_rows = ["абвгдеёжзийкл", "мнопрстуфхцчшщ", "ъыьэюя"]
letter_buttons = []  # список для хранения кнопок

# Создаем кнопки для каждой буквы
for i, row in enumerate(letters_rows):  # для каждого ряда букв
    for letter in row:  # для каждой буквы в ряду
        # Создаем кнопку
        btn = tk.Button(
            keyboard_frames[i],  # помещаем в соответствующий фрейм
            text=letter.upper(),  # текст кнопки (заглавная буква)
            font=("Arial", 14),  # шрифт
            width=4, height=2,  # размеры
            bg=BUTTON_COLOR,  # цвет фона
            command=lambda l=letter: guess_letter(l)  # действие при нажатии
        )
        btn.pack(side="left", padx=2, pady=2)  # размещаем кнопку
        letter_buttons.append(btn)  # добавляем в список кнопок

# ========== ЗАПУСК ИГРЫ ==========
new_game()  # начинаем новую игру
root.mainloop()  # запускаем главный цикл обработки событий