# Импорт необходимых библиотек
import tkinter as tk  # Для создания графического интерфейса
from tkinter import messagebox  # Для всплывающих сообщений
import random  # Для случайного выбора слов

# Настройки игры
words = [  # Список слов для угадывания (теперь содержит 50+ слов)
    "питон", "программа", "компьютер", "клавиатура", "монитор", "мышка",
    # ... остальные слова ...
]
max_attempts = 7  # Максимальное количество ошибок перед проигрышем

# Цветовая схема интерфейса
BG_COLOR = "#000000"  # Чёрный фон основного окна
BUTTON_COLOR = "#000000"  # Цвет неактивных кнопок (чёрный)
CORRECT_COLOR = "#8696FF"  # Голубой - цвет кнопки при правильной букве
WRONG_COLOR = "#FF3B8B"  # Розовый - цвет кнопки при ошибке
TEXT_COLOR = "#ffffff"  # Белый цвет текста
DISABLED_TEXT_COLOR = "#ffffff"  # Белый цвет текста на отключенных кнопках
DRAWING_COLOR = "#ffffff"  # Белый цвет для рисунка виселицы

# Инициализация игровых переменных
secret_word = ""  # Здесь будет храниться загаданное слово
guessed_letters = []  # Список уже названных букв
attempts_left = max_attempts  # Счётчик оставшихся попыток
wins = 0  # Счётчик побед
losses = 0  # Счётчик поражений


# Функция отрисовки виселицы и человечка
def draw_hangman(step):
    hangman_canvas.delete("all")  # Очищаем холст перед новой отрисовкой

    # Рисуем элементы виселицы в зависимости от количества ошибок:
    if step >= 1:  # Основание
        hangman_canvas.create_line(100, 320, 280, 320, width=8, fill=DRAWING_COLOR)
    if step >= 2:  # Вертикальная стойка
        hangman_canvas.create_line(190, 320, 190, 70, width=6, fill=DRAWING_COLOR)
    if step >= 3:  # Горизонтальная перекладина
        hangman_canvas.create_line(190, 70, 280, 70, width=6, fill=DRAWING_COLOR)
    if step >= 4:  # Верёвка
        hangman_canvas.create_line(280, 70, 280, 100, width=3, fill=DRAWING_COLOR)
    if step >= 5:  # Голова
        hangman_canvas.create_oval(265, 100, 295, 130, width=3, outline=DRAWING_COLOR)
    if step >= 6:  # Туловище
        hangman_canvas.create_line(280, 130, 280, 200, width=3, fill=DRAWING_COLOR)
    if step >= 7:  # Руки и ноги
        hangman_canvas.create_line(280, 150, 250, 180, width=3, fill=DRAWING_COLOR)  # Левая рука
        hangman_canvas.create_line(280, 150, 310, 180, width=3, fill=DRAWING_COLOR)  # Правая рука
        hangman_canvas.create_line(280, 200, 250, 250, width=3, fill=DRAWING_COLOR)  # Левая нога
        hangman_canvas.create_line(280, 200, 310, 250, width=3, fill=DRAWING_COLOR)  # Правая нога


# Функция обновления игрового интерфейса
def update_display():
    # Формируем строку с отображением слова (открытые буквы или подчёркивания)
    display_word = "   ".join([l if l in guessed_letters else "_" for l in secret_word])
    word_label.config(text=display_word)  # Обновляем label с загаданным словом

    # Обновляем счётчики побед и поражений
    stats_label.config(text=f"Побед: {wins}  Поражений: {losses}")

    # Обновляем счётчик оставшихся попыток
    attempts_label.config(text=f"Попыток осталось: {attempts_left}")


# Функция сброса кнопок клавиатуры в начальное состояние
def reset_buttons():
    for btn in letter_buttons:  # Проходим по всем кнопкам с буквами
        btn.config(
            state=tk.NORMAL,  # Делаем кнопку активной
            bg=BUTTON_COLOR,  # Возвращаем исходный цвет фона
            fg=TEXT_COLOR  # Белый цвет текста
        )


# Основная игровая логика - обработка нажатия буквы
def guess_letter(letter):
    global attempts_left, wins, losses  # Используем глобальные переменные

    # Если буква уже называлась, ничего не делаем
    if letter in guessed_letters:
        return

    guessed_letters.append(letter)  # Добавляем букву в список использованных
    correct = letter in secret_word  # Проверяем, есть ли буква в слове

    # Находим соответствующую кнопку и меняем её стиль
    for btn in letter_buttons:
        if btn['text'].lower() == letter:
            color = CORRECT_COLOR if correct else WRONG_COLOR  # Выбираем цвет
            btn.config(
                bg=color,  # Меняем цвет фона
                fg=DISABLED_TEXT_COLOR,  # Белый текст
                state=tk.DISABLED  # Делаем кнопку неактивной
            )
            break

    # Если буква неверная
    if not correct:
        attempts_left -= 1  # Уменьшаем количество попыток
        draw_hangman(max_attempts - attempts_left)  # Рисуем следующую часть виселицы

    update_display()  # Обновляем интерфейс

    # Проверяем условия победы
    if all(letter in guessed_letters for letter in secret_word):
        wins += 1  # Увеличиваем счётчик побед
        messagebox.showinfo("Победа!", "Вы угадали слово!")
        new_game()  # Начинаем новую игру

    # Проверяем условия поражения
    elif attempts_left == 0:
        losses += 1  # Увеличиваем счётчик поражений
        word_label.config(text="   ".join(secret_word))  # Показываем загаданное слово
        messagebox.showinfo("Проигрыш", f"Слово было: {secret_word}")
        new_game()  # Начинаем новую игру


# Функция начала новой игры
def new_game():
    global secret_word, guessed_letters, attempts_left

    secret_word = random.choice(words)  # Выбираем случайное слово
    guessed_letters = []  # Очищаем список угаданных букв
    attempts_left = max_attempts  # Сбрасываем счётчик попыток

    reset_buttons()  # Сбрасываем кнопки клавиатуры
    update_display()  # Обновляем интерфейс
    draw_hangman(0)  # Очищаем виселицу


# Создание главного окна
root = tk.Tk()
root.title("Виселица")  # Заголовок окна
root.state('zoomed')  # Открываем окно на весь экран
root.configure(bg=BG_COLOR)  # Устанавливаем чёрный фон

# Создаем холст для рисования виселицы
hangman_canvas = tk.Canvas(
    root,
    width=400,
    height=350,
    bg=BG_COLOR,  # Чёрный фон
    highlightthickness=0  # Убираем рамку
)
hangman_canvas.pack(pady=(30, 20))  # Размещаем с отступами сверху и снизу

# Label для отображения загаданного слова
word_label = tk.Label(
    root,
    font=("Arial", 42),  # Большой шрифт
    bg=BG_COLOR,  # Чёрный фон
    fg=TEXT_COLOR  # Белый текст
)
word_label.pack(pady=20)  # Размещаем с отступом

# Label для отображения статистики
stats_label = tk.Label(
    root,
    font=("Arial", 18),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
stats_label.pack(pady=10)

# Label для отображения оставшихся попыток
attempts_label = tk.Label(
    root,
    font=("Arial", 18),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
attempts_label.pack(pady=(10, 30))  # Больший отступ снизу

# Создаем клавиатуру (3 ряда кнопок)
keyboard_frames = []  # Список для хранения рядов кнопок
for i in range(3):  # Создаем 3 ряда
    frame = tk.Frame(root, bg=BG_COLOR)  # Фрейм для ряда кнопок
    frame.pack(pady=8)  # Размещаем с отступом
    keyboard_frames.append(frame)  # Добавляем в список

# Распределение русских букв по рядам
letters_rows = ["абвгдеёжзий", "клмнопрстуфх", "цчшщъыьэюя"]
letter_buttons = []  # Список для хранения всех кнопок

# Создаем кнопки для каждой буквы
for i, row in enumerate(letters_rows):  # Для каждого ряда букв
    for letter in row:  # Для каждой буквы в ряду
        btn = tk.Button(
            keyboard_frames[i],  # Помещаем в соответствующий фрейм
            text=letter.upper(),  # Заглавные буквы
            font=("Arial", 14, "bold"),  # Жирный шрифт
            width=4,  # Ширина кнопки
            height=2,  # Высота кнопки
            bg=BUTTON_COLOR,  # Чёрный фон
            fg=TEXT_COLOR,  # Белый текст
            activebackground="#555555",  # Цвет при нажатии
            activeforeground=TEXT_COLOR,  # Цвет текста при нажатии
            disabledforeground=DISABLED_TEXT_COLOR,  # Цвет текста неактивной кнопки
            command=lambda l=letter: guess_letter(l)  # Обработчик нажатия
        )
        btn.pack(side="left", padx=4, pady=4)  # Размещаем кнопку с отступами
        letter_buttons.append(btn)  # Добавляем кнопку в список

# Начало игры
new_game()  # Инициализируем первую игру
root.mainloop()  # Запускаем главный цикл приложения