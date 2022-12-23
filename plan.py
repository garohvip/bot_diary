import datetime
import json
from config import token
from telebot import types
import telebot

agent_ghost = telebot.TeleBot(token)


keyboard_all = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_all.add(types.KeyboardButton("Записи"),
                 types.KeyboardButton("Планы"))


