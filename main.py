import tkinter as tk
from tkinter import messagebox
import random

# Настройки игры
words = ["шлюха", "манда", "компьютер", "клавиатура", "монитор", "мышка", "программирование", "приложение","питон", "программа", "алгоритм"]
max_attempts = 7

# Цветовая схема
BG_COLOR = "#f0f8ff"  # AliceBlue
BUTTON_COLOR = "#e6e6fa"  # Lavender
BUTTON_ACTIVE_COLOR = "#d8bfd8"  # Thistle
TEXT_COLOR = "#483d8b"  # DarkSlateBlue
HANGMAN_COLOR = "#9370db"  # MediumPurple
CORRECT_COLOR = "#2e8b57"  # SeaGreen
WRONG_COLOR = "#cd5c5c"  # IndianRed

# Глобальные переменные
secret_word = ""
guessed_letters = []
attempts_left = max_attempts
game_over = False
wins = 0
losses = 0

# Создаем главное окно
root = tk.Tk()
root.title("Виселица")
root.geometry("1100x1000")
root.configure(bg=BG_COLOR)

# Стили
button_style = {
    "font": ("Arial", 14),
    "width": 4,
    "height": 2,
    "bg": BUTTON_COLOR,
    "activebackground": BUTTON_ACTIVE_COLOR,
    "fg": TEXT_COLOR,
    "relief": tk.RAISED,
    "borderwidth": 3
}

label_style = {
    "font": ("Arial", 16),
    "bg": BG_COLOR,
    "fg": TEXT_COLOR
}

big_font_style = {
    "font": ("Arial", 42),
    "bg": BG_COLOR,
    "fg": TEXT_COLOR
}

# Основные элементы интерфейса
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(pady=20)

# Холст для виселицы (увеличенный размер)
hangman_canvas = tk.Canvas(main_frame, width=400, height=350, bg=BG_COLOR, highlightthickness=0)
hangman_canvas.grid(row=0, column=0, columnspan=3, pady=(0, 20))

# Область слова
word_frame = tk.Frame(main_frame, bg=BG_COLOR)
word_frame.grid(row=1, column=0, columnspan=3)
word_label = tk.Label(word_frame, text="", **big_font_style)
word_label.pack()

# Статистика и информация
stats_frame = tk.Frame(main_frame, bg=BG_COLOR)
stats_frame.grid(row=2, column=0, columnspan=3, pady=10)

stats_label = tk.Label(stats_frame, text="Побед: 0  Поражений: 0", **label_style)
stats_label.pack(side="left", padx=20)

attempts_label = tk.Label(stats_frame, text=f"Попыток осталось: {max_attempts}", **label_style)
attempts_label.pack(side="left", padx=20)

used_letters_label = tk.Label(main_frame, text="Использованные буквы: ", **label_style)
used_letters_label.grid(row=3, column=0, columnspan=3, pady=10)

# Клавиатура (3 ряда)
keyboard_frame = tk.Frame(main_frame, bg=BG_COLOR)
keyboard_frame.grid(row=4, column=0, columnspan=3, pady=20)

letters_row1 = "абвгдеёжзийкл"
letters_row2 = "мнопрстуфхцчшщ"
letters_row3 = "ъыьэюя"

# Создаем кнопки клавиатуры
for i, row in enumerate([letters_row1, letters_row2, letters_row3]):
    frame = tk.Frame(keyboard_frame, bg=BG_COLOR)
    frame.pack()
    for letter in row:
        btn = tk.Button(
            frame,
            text=letter.upper(),
            **button_style,
            command=lambda l=letter: guess_letter(l)
        )
        btn.pack(side="left", padx=2, pady=2)

# Панель управления
control_frame = tk.Frame(main_frame, bg=BG_COLOR)
control_frame.grid(row=5, column=0, columnspan=3, pady=20)

new_game_btn = tk.Button(
    control_frame,
    text="Новая игра",
    font=("Arial", 14),
    bg="#dda0dd",  # Plum
    activebackground="#ee82ee",  # Violet
    fg="white",
    width=12,
    height=1,
    command=lambda: new_game()
)
new_game_btn.pack(side="left", padx=10)

restart_btn = tk.Button(
    control_frame,
    text="Начать сначала",
    font=("Arial", 14),
    bg="#9370db",  # MediumPurple
    activebackground="#8a2be2",  # BlueViolet
    fg="white",
    width=13,
    height=1,
    command=lambda: restart_game()
)
restart_btn.pack(side="left", padx=10)


def draw_hangman(step):
    """Рисует виселицу с улучшенной графикой"""
    hangman_canvas.delete("all")

    # Координаты и размеры для крупной виселицы
    base_x, base_y = 100, 320
    pole_height = 250
    beam_length = 180
    rope_length = 40
    head_radius = 25
    body_length = 100
    limb_length = 40

    # Основание (толще и с тенью)
    hangman_canvas.create_line(
        base_x - 50, base_y,
        base_x + 50, base_y,
        width=8, fill=HANGMAN_COLOR
    )

    # Столб
    hangman_canvas.create_line(
        base_x, base_y,
        base_x, base_y - pole_height,
        width=6, fill=HANGMAN_COLOR
    )

    # Перекладина
    hangman_canvas.create_line(
        base_x, base_y - pole_height,
                base_x + beam_length, base_y - pole_height,
        width=6, fill=HANGMAN_COLOR
    )

    # Веревка
    if step >= 1:
        hangman_canvas.create_line(
            base_x + beam_length, base_y - pole_height,
            base_x + beam_length, base_y - pole_height + rope_length,
            width=3, fill="gray"
        )

    # Голова
    if step >= 2:
        hangman_canvas.create_oval(
            base_x + beam_length - head_radius, base_y - pole_height + rope_length,
            base_x + beam_length + head_radius, base_y - pole_height + rope_length + head_radius * 2,
            width=3, outline="black", fill="#ffdead"  # NavajoWhite
        )

    # Тело
    if step >= 3:
        hangman_canvas.create_line(
            base_x + beam_length, base_y - pole_height + rope_length + head_radius * 2,
            base_x + beam_length, base_y - pole_height + rope_length + head_radius * 2 + body_length,
            width=3, fill="black"
        )

    # Руки
    if step >= 4:
        # Левая рука
        hangman_canvas.create_line(
            base_x + beam_length, base_y - pole_height + rope_length + head_radius * 2 + 30,
            base_x + beam_length - limb_length, base_y - pole_height + rope_length + head_radius * 2 + 60,
            width=3, fill="black"
        )
        # Правая рука
        hangman_canvas.create_line(
            base_x + beam_length, base_y - pole_height + rope_length + head_radius * 2 + 30,
            base_x + beam_length + limb_length, base_y - pole_height + rope_length + head_radius * 2 + 60,
            width=3, fill="black"
        )

    # Ноги
    if step >= 5:
        # Левая нога
        hangman_canvas.create_line(
            base_x + beam_length, base_y - pole_height + rope_length + head_radius * 2 + body_length,
            base_x + beam_length - limb_length, base_y - pole_height + rope_length + head_radius * 2 + body_length + 30,
            width=3, fill="black"
        )
        # Правая нога
        hangman_canvas.create_line(
            base_x + beam_length, base_y - pole_height + rope_length + head_radius * 2 + body_length,
            base_x + beam_length + limb_length, base_y - pole_height + rope_length + head_radius * 2 + body_length + 30,
            width=3, fill="black"
        )

    # Лицо (при проигрыше)
    if step >= 6:
        # Глаза
        hangman_canvas.create_oval(
            base_x + beam_length - 15, base_y - pole_height + rope_length + head_radius - 5,
            base_x + beam_length - 5, base_y - pole_height + rope_length + head_radius + 5,
            fill="red", outline="red"
        )
        hangman_canvas.create_oval(
            base_x + beam_length + 5, base_y - pole_height + rope_length + head_radius - 5,
            base_x + beam_length + 15, base_y - pole_height + rope_length + head_radius + 5,
            fill="red", outline="red"
        )
        # Рот
        hangman_canvas.create_line(
            base_x + beam_length - 10, base_y - pole_height + rope_length + head_radius + 15,
            base_x + beam_length + 10, base_y - pole_height + rope_length + head_radius + 15,
            width=2, fill="red"
        )


def update_word_display():
    """Обновляет отображение слова с крупными черточками"""
    displayed = []
    for letter in secret_word:
        if letter in guessed_letters:
            displayed.append(letter)
        else:
            displayed.append("_")
    word_label.config(text="   ".join(displayed))


def update_stats():
    """Обновляет статистику"""
    stats_label.config(text=f"Побед: {wins}  Поражений: {losses}")


def update_used_letters():
    """Обновляет список использованных букв"""
    used_letters = sorted(guessed_letters)
    # Подсвечиваем неправильные буквы
    used_text = "Использованные буквы: "
    for letter in used_letters:
        if letter not in secret_word:
            used_text += f"[{letter}] "
        else:
            used_text += f"{letter} "
    used_letters_label.config(text=used_text.strip())


def update_attempts():
    """Обновляет счетчик попыток"""
    attempts_label.config(text=f"Попыток осталось: {attempts_left}")


def disable_all_buttons():
    """Отключает все кнопки букв"""
    for frame in keyboard_frame.winfo_children():
        for btn in frame.winfo_children():
            btn.config(state=tk.DISABLED)


def enable_all_buttons():
    """Включает все кнопки букв"""
    for frame in keyboard_frame.winfo_children():
        for btn in frame.winfo_children():
            btn.config(state=tk.NORMAL)
            if btn['text'].lower() in guessed_letters:
                btn.config(bg="#d3d3d3")  # LightGray для использованных
            else:
                btn.config(bg=BUTTON_COLOR)


def check_win():
    """Проверяет, угадано ли слово"""
    for letter in secret_word:
        if letter not in guessed_letters:
            return False
    return True


def guess_letter(letter):
    """Обрабатывает угадывание буквы"""
    global attempts_left, game_over, wins, losses

    if game_over:
        return

    if letter in guessed_letters:
        messagebox.showinfo("Уже было", "Вы уже пробовали эту букву!")
        return

    guessed_letters.append(letter)
    update_used_letters()

    # Находим кнопку этой буквы и меняем ее цвет
    for frame in keyboard_frame.winfo_children():
        for btn in frame.winfo_children():
            if btn['text'].lower() == letter:
                if letter in secret_word:
                    btn.config(bg=CORRECT_COLOR, fg="white")
                else:
                    btn.config(bg=WRONG_COLOR, fg="white")
                btn.config(state=tk.DISABLED)
                break

    if letter not in secret_word:
        attempts_left -= 1
        update_attempts()
        draw_hangman(max_attempts - attempts_left + 1)

        if attempts_left == 0:
            game_over = True
            losses += 1
            update_stats()
            disable_all_buttons()
            # Показываем все буквы при проигрыше
            word_label.config(text="   ".join(list(secret_word)))
            messagebox.showinfo("Проигрыш", f"Игра окончена! Слово было: {secret_word}")
    else:
        update_word_display()
        if check_win():
            game_over = True
            wins += 1
            update_stats()
            disable_all_buttons()
            messagebox.showinfo("Победа!", "Поздравляю, вы угадали слово!")


def new_game():
    """Начинает новую игру с новым словом"""
    global secret_word, guessed_letters, attempts_left, game_over

    secret_word = random.choice(words)
    guessed_letters = []
    attempts_left = max_attempts
    game_over = False

    update_word_display()
    update_used_letters()
    update_attempts()
    draw_hangman(0)
    enable_all_buttons()


def restart_game():
    """Начинает текущее слово сначала"""
    global guessed_letters, attempts_left, game_over

    if not secret_word:
        return

    guessed_letters = []
    attempts_left = max_attempts
    game_over = False

    update_word_display()
    update_used_letters()
    update_attempts()
    draw_hangman(0)
    enable_all_buttons()


# Начальная инициализация
new_game()
root.mainloop()