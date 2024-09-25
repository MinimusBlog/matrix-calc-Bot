import telebot
from telebot import types
from dotenv import load_dotenv
import os
import numpy as np
from commands import parse_matrix, matrix_addition, matrix_subtraction, matrix_multiplication, matrix_transposition

load_dotenv()
bot_token = os.getenv('TELEBOT_TOKEN')  #Токен бота

bot = telebot.TeleBot(bot_token) #Инициализация бота

operation_mode = None

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Сложение'))
    markup.add(types.KeyboardButton('Вычитание'))
    markup.add(types.KeyboardButton('Умножение'))
    markup.add(types.KeyboardButton('Транспонирование'))
    markup.add(types.KeyboardButton('Помощь'))
    bot.reply_to(message, "Привет! Выбери операцию.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Сложение')
def add(message):
    global operation_mode
    operation_mode = 'matrix_addition'
    bot.send_message(message.chat.id, 'Отправьте две матрицы для сложения, разделённые пустой строкой.')

@bot.message_handler(func=lambda message: message.text == 'Вычитание')
def subtract(message):
    global operation_mode
    operation_mode = 'matrix_subtraction'
    bot.send_message(message.chat.id, 'Отправьте две матрицы для вычитания, разделённые пустой строкой.')

@bot.message_handler(func=lambda message: message.text == 'Умножение')
def multiply(message):
    global operation_mode
    operation_mode = 'matrix_multiplication'
    bot.send_message(message.chat.id, 'Отправьте две матрицы для умножения, разделённые пустой строкой.')

@bot.message_handler(func=lambda message: message.text == 'Транспонирование')
def transpose(message):
    global operation_mode
    operation_mode = 'matrix_transposition'
    bot.send_message(message.chat.id, 'Отправьте матрицу для транспонирования.')

@bot.message_handler(func=lambda message: message.text == 'Помощь')
def help_message(message):
    instructions = """
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

    Пример ввода матриц:
    ```
    1 2 3
    4 5 6

    7 8 9
    10 11 12
    ```
    """
    bot.send_message(message.chat.id, instructions)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global operation_mode
    try:
        text = message.text.strip()

        if operation_mode == 'matrix_transposition': #Транспонированая матрица
            matrix = parse_matrix(text)
            result = matrix_transposition(matrix)
            bot.reply_to(message, f"Транспонированная матрица:\n{np.array(result)}")

        elif '\n\n' in text:
            matrices = text.split('\n\n')  #Разделяем текст на две части по пустой строке
            if len(matrices) == 2:
                matrix1 = parse_matrix(matrices[0])  #Преобразуем первую в матрицу
                matrix2 = parse_matrix(matrices[1])  #Преобразуем вторую в матрицу

                if operation_mode == 'matrix_addition':
                    result = matrix_addition(matrix1, matrix2) #Сложение матриц
                    bot.reply_to(message, f"Результат сложения:\n{np.array(result)}")

                elif operation_mode == 'matrix_subtraction':
                    result = matrix_subtraction(matrix1, matrix2) #Вычитание матриц
                    bot.reply_to(message, f"Результат вычитания:\n{np.array(result)}")

                elif operation_mode == 'matrix_multiplication':
                    result = matrix_multiplication(matrix1, matrix2) #Умножение матриц
                    bot.reply_to(message, f"Результат умножения:\n{np.array(result)}")

                else:
                    bot.reply_to(message, "Пожалуйста, выберите операцию: Сложение, Вычитание, Умножение или Транспонирование.")
            else:
                bot.reply_to(message, "Пожалуйста, отправьте две матрицы, разделённые пустой строкой.")
        else:
            bot.reply_to(message, "Пожалуйста, отправьте две матрицы, разделённые пустой строкой.")

    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")

@bot.message_handler(content_types=['voice']) #Обработчик для голосовых сообщений
def handle_voice_message(message):
    bot.send_message(message.chat.id, "Извините, я не могу обрабатывать голосовые сообщения. Пожалуйста, воспользуйтесь текстовыми сообщениями или кнопкой 'Помощь'.")

@bot.message_handler(content_types=['sticker']) #Обработчик для стикеров
def handle_sticker_message(message):
    bot.send_message(message.chat.id, "Извините, я не могу обрабатывать стикеры. Пожалуйста, воспользуйтесь текстовыми сообщениями или кнопкой 'Помощь'.")

if __name__ == "__main__":
    bot.polling()