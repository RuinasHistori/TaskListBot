import telebot
from telebot import types
import os

FILE_NAME = "tasks.txt"

def load_tasks():
    """Загружает задачи из файла."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            return [line.strip().split('|') for line in file.readlines()]
    return []

def save_tasks(tasks):
    """Сохраняет задачи в файл."""
    with open(FILE_NAME, "w") as file:
        for task in tasks:
            file.write('|'.join(task) + "\n")

# Замените 'YOUR_BOT_TOKEN' на ваш токен бота
TOKEN = 'ТОКЕН'
bot = telebot.TeleBot(TOKEN)

# Список разрешенных идентификаторов пользователей
ALLOWED_USERS = { id человека , id человека }  # Замените идентификаторы на нужные вам

def is_authorized(user_id):
    """Проверяет, принадлежит ли пользователь к списку разрешенных."""
    return user_id in ALLOWED_USERS

def create_main_keyboard():
    """Создает основную клавиатуру."""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [types.KeyboardButton(text) for text in ['/add', '/list', '/delete']]
    keyboard.add(*buttons)
    return keyboard

def notify_admins(task, username, exclude_user_id):
    """Уведомляет администраторов о новой задаче, исключая пользователя, который добавил задачу."""
    for user_id in ALLOWED_USERS:
        if user_id != exclude_user_id:
            bot.send_message(user_id, f"Новая задача добавлена пользователем @{username}: {task}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if is_authorized(message.from_user.id):
        bot.send_message(
            message.chat.id,
            "Привет! Я бот для управления задачами. Используйте команды /add, /list и /delete для управления задачами.",
            reply_markup=create_main_keyboard()
        )
    else:
        bot.reply_to(message, "Извините, у вас нет доступа к этому боту.")

@bot.message_handler(commands=['add'])
def add_task(message):
    if is_authorized(message.from_user.id):
        msg = bot.send_message(message.chat.id, "Введите задачу:")
        bot.register_next_step_handler(msg, save_new_task)
    else:
        bot.reply_to(message, "Извините, у вас нет доступа к этому боту.")

def save_new_task(message):
    if is_authorized(message.from_user.id):
        task = message.text.strip()
        if task:
            tasks = load_tasks()
            tasks.append([task, message.from_user.username])
            save_tasks(tasks)
            notify_admins(task, message.from_user.username, message.from_user.id)
            bot.reply_to(message, "Задача добавлена!", reply_markup=create_main_keyboard())
        else:
            bot.reply_to(message, "Пожалуйста, укажите задачу.", reply_markup=create_main_keyboard())

@bot.message_handler(commands=['list'])
def list_tasks(message):
    if is_authorized(message.from_user.id):
        tasks = load_tasks()
        if not tasks:
            bot.reply_to(message, "Ваш список задач пуст.", reply_markup=create_main_keyboard())
        else:
            task_list = "\n".join([f"{i+1}. {task[0]} (добавлено @{task[1]})" for i, task in enumerate(tasks)])
            bot.reply_to(message, f"Ваши задачи:\n{task_list}", reply_markup=create_main_keyboard())
    else:
        bot.reply_to(message, "Извините, у вас нет доступа к этому боту.")

@bot.message_handler(commands=['delete'])
def delete_task(message):
    if is_authorized(message.from_user.id):
        tasks = load_tasks()
        if not tasks:
            bot.reply_to(message, "Ваш список задач пуст.", reply_markup=create_main_keyboard())
        else:
            task_list = "\n".join([f"{i+1}. {task[0]} (добавлено @{task[1]})" for i, task in enumerate(tasks)])
            msg = bot.send_message(message.chat.id, f"Ваши задачи:\n{task_list}\nВведите номер задачи для удаления:")
            bot.register_next_step_handler(msg, confirm_delete_task)
    else:
        bot.reply_to(message, "Извините, у вас нет доступа к этому боту.")

def confirm_delete_task(message):
    if is_authorized(message.from_user.id):
        try:
            task_num = int(message.text.strip())
            tasks = load_tasks()
            if 1 <= task_num <= len(tasks):
                removed_task = tasks.pop(task_num - 1)
                save_tasks(tasks)
                bot.reply_to(message, f"Задача '{removed_task[0]}' удалена!", reply_markup=create_main_keyboard())
            else:
                bot.reply_to(message, "Неверный номер задачи.", reply_markup=create_main_keyboard())
        except ValueError:
            bot.reply_to(message, "Введите корректный номер задачи.", reply_markup=create_main_keyboard())
    else:
        bot.reply_to(message, "Извините, у вас нет доступа к этому боту.")

bot.polling()
