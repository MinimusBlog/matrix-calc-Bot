import telebot
from telebot import types
from dotenv import load_dotenv
import os
import numpy as np
from commands import parse_matrix, matrix_addition, matrix_subtraction, matrix_multiplication, matrix_transposition, matrix_power, matrix_scalar_multiplication, matrix_determinant

load_dotenv()
bot_token = os.getenv('TELEBOT_TOKEN')  # Токен бота

bot = telebot.TeleBot(bot_token) # Инициализация бота

operation_mode = None

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton('Матрицы')
    ]
    markup.add(*buttons)
    bot.reply_to(message, "Привет! Выбери категорию.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Матрицы')
def matrices(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        types.KeyboardButton('Сложение'),
        types.KeyboardButton('Вычитание'),
        types.KeyboardButton('Умножение'),
        types.KeyboardButton('Возведение в степень'),
        types.KeyboardButton('Умножение на число'),
        types.KeyboardButton('Транспонирование'),
        types.KeyboardButton('Определитель'),
        types.KeyboardButton('Помощь'),
        types.KeyboardButton('Назад')
    ]
    markup.add(*buttons)
    bot.send_message(message.chat.id, "Выбери операцию с матрицами:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Назад')
def back(message):
    welcome(message)

command_handlers = { #Словарь для хранения команд и их обработчиков
    'matrix_addition': ('matrix_addition', 'Отправьте две матрицы для сложения, разделённые пустой строкой.'),
    'matrix_subtraction': ('matrix_subtraction', 'Отправьте две матрицы для вычитания, разделённые пустой строкой.'),
    'matrix_multiplication': ('matrix_multiplication', 'Отправьте две матрицы для умножения, разделённые пустой строкой.'),
    'matrix_transposition': ('matrix_transposition', 'Отправьте матрицу для транспонирования.'),
    'matrix_power': ('matrix_power', 'Отправьте матрицу и степень, разделённые пустой строкой.'),
    'matrix_scalar': ('matrix_scalar', 'Отправьте матрицу и число, разделённые пустой строкой.'),
    'matrix_determinant': ('matrix_determinant', 'Отправьте матрицу.'),
    'help': ('help', """
    Привет! Это инструкции по использованию бота:

    1. Сложение:
    - Нажмите кнопку "Сложение".
    - Отправьте две матрицы A и B, разделённые пустой строкой.
    - Бот вернёт результат сложения матриц.

    2. Вычитание:
    - Нажмите кнопку "Вычитание".
    - Отправьте две матрицы A и B, разделённые пустой строкой.
    - Бот вернёт результат вычитания матриц.

    3. Умножение:
    - Нажмите кнопку "Умножение".
    - Отправьте две матрицы A и B, разделённые пустой строкой.
    - Бот вернёт результат умножения матриц.

    4. Транспонирование:
    - Нажмите кнопку "Транспонирование".
    - Отправьте матрицу для транспонирования.
    - Бот вернёт транспонированную матрицу.

    5. Возведение в степень:
    - Нажмите кнопку "Возведение в степень".
    - Отправьте матрицу и степень, разделённые пустой строкой.
    - Бот вернёт результат возведения матрицы в степень.

    6. Умножение на число:
    - Нажмите кнопку "Умножение на число".
    - Отправьте матрицу и число, разделённые пустой строкой.
    - Бот вернёт результат умноженной матрицы на число.

    7. Нахождение определителя:
    - Нажмите кнопку "Определитель".
    - Отправьте матрицу для нахождения.
    - Бот вернёт результат определителя.

    7. Нахождение минора:
    - Нажмите кнопку "Минор".
    - Отправьте матрицу для нахождения.
    - Бот вернёт результат минора.

    Пример ввода матриц:
    ```
    1 2 3
    4 5 6

    7 8 9
    10 11 12
    ```

    Если у вас возникли вопросы или проблемы, пожалуйста, свяжитесь с администратором.
    """)
}

@bot.message_handler(func=lambda message: message.text in command_handlers)
def handle_command(message):
    global operation_mode
    command = message.text
    operation_mode, response_message = command_handlers[command]
    bot.send_message(message.chat.id, response_message)

@bot.message_handler(content_types=['voice']) #Обработчик для голосовых сообщений
def handle_voice_message(message):
    bot.send_message(message.chat.id, "Извините, я не могу обрабатывать голосовые сообщения. Пожалуйста, воспользуйтесь текстовыми сообщениями или кнопкой 'Помощь'.")
@bot.message_handler(content_types=['sticker']) #Обработчик для стикеров
def handle_sticker_message(message):
    bot.send_message(message.chat.id, "Извините, я не могу обрабатывать стикеры. Пожалуйста, воспользуйтесь текстовыми сообщениями или кнопкой 'Помощь'.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global operation_mode
    try:
        text = message.text.strip()

        if operation_mode == 'matrix_transposition':
            matrix = parse_matrix(text)
            result = matrix_transposition(matrix)
            bot.reply_to(message, f"Транспонированная матрица:\n{np.array(result)}")

        elif operation_mode == 'matrix_determinant':
            matrix = parse_matrix(text)
            result = matrix_determinant(matrix)
            bot.reply_to(message, f"Определитель матрицы:\n{np.array(result)}")

        elif operation_mode == 'matrix_power':
            parts = text.split('\n\n')
            if len(parts) == 2:
                matrix = parse_matrix(parts[0])
                power = int(parts[1].strip())
                result = matrix_power(matrix, power)
                bot.reply_to(message, f"Результат возведения в степень:\n{np.array(result)}")
            else:
                bot.reply_to(message, "Пожалуйста, отправьте матрицу и степень, разделённые пустой строкой.")

        elif '\n\n' in text:
            matrices = text.split('\n\n')  # Разделяем текст на две части по пустой строке
            if len(matrices) == 2:
                matrix1 = parse_matrix(matrices[0])  # Преобразуем первую в матрицу
                matrix2 = parse_matrix(matrices[1])  # Преобразуем вторую в матрицу

                if operation_mode == 'matrix_addition':
                    result = matrix_addition(matrix1, matrix2)  # Сложение матриц
                    bot.reply_to(message, f"Результат сложения:\n{np.array(result)}")

                elif operation_mode == 'matrix_subtraction':
                    result = matrix_subtraction(matrix1, matrix2)  # Вычитание матриц
                    bot.reply_to(message, f"Результат вычитания:\n{np.array(result)}")

                elif operation_mode == 'matrix_multiplication':
                    result = matrix_multiplication(matrix1, matrix2)  # Умножение матриц
                    bot.reply_to(message, f"Результат умножения:\n{np.array(result)}")

                elif operation_mode == 'matrix_scalar':
                    scalar = float(matrices[1].strip())  # Извлекаем скаляр
                    result = matrix_scalar_multiplication(matrix1, scalar)  # Скалярное умножение
                    bot.reply_to(message, f"Результат умножения на число:\n{np.array(result)}")

                else:
                    bot.reply_to(message, "Пожалуйста, выберите операцию: Сложение, Вычитание, Умножение, Транспонирование или Возведение в степень.")
            else:
                bot.reply_to(message, "Пожалуйста, отправьте две матрицы, разделённые пустой строкой.")
        else:
            bot.reply_to(message, "Пожалуйста, отправьте две матрицы, разделённые пустой строкой.")

    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

if __name__ == "__main__":
    bot.polling()