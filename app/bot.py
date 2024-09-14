import telebot
from dotenv import load_dotenv
import os
import numpy as np
from commands import matrix_addition, parse_matrix 

load_dotenv()
bot_token = os.getenv('TELEBOT_TOKEN')  # Токен бота

bot = telebot.TeleBot(bot_token) # Инициализация бота

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Привет! Отправь две матрицы, разделённые пустой строкой, для сложения.")

@bot.message_handler(commands=['add'])
def handle_add(message):
    bot.reply_to(message, "Отправьте две матрицы для сложения, разделённые пустой строкой.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        text = message.text.strip()
        
        if text.count('\n\n') > 0:
            matrices = text.split('\n\n')  # Разделяем текст на две части по пустой строке
            matrix1 = parse_matrix(matrices[0])  # Преобразуем первую в матрицу
            matrix2 = parse_matrix(matrices[1])  # Преобразуем вторую в матрицу

            result = matrix_addition(matrix1, matrix2) # Сложение матриц
            bot.reply_to(message, f"Результат сложения:\n{np.array(result)}")

        else:
            bot.reply_to(message, "Пожалуйста, отправьте две матрицы, разделённые пустой строкой.")

    except Exception as e:
        bot.reply_to(message, f"Ошибка: {str(e)}")


if __name__ == "__main__":
    bot.polling()