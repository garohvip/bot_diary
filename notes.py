import datetime
import json
from config import token
from telebot import types
import telebot

agent_ghost = telebot.TeleBot(token)

keyboard_all = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_all.add(types.KeyboardButton("Записи"),
                 types.KeyboardButton("Планы"))


def check_notes(message):
    with open("bd.json", "r") as f:
        data = json.load(f)
    date = str(datetime.datetime.now())[:10]
    for i in data:
        if i.get('login') == message.chat.id and i.get('notes').get(f'{date}'):
            return True
    else:
        return False


def add_notes(message):
    with open("bd.json", "r") as f:
        data = json.load(f)
    date = str(datetime.datetime.now())[:10]
    for i in range(len(data)):
        if data[i].get('login') == message.chat.id:
            data[i]['notes'][date] = message.text
            break
    with open("bd.json", "w") as f:
        json.dump(data, f)
    agent_ghost.send_message(message.chat.id, f"Запись успешно добавлена за {date}!\nТекст записи:\n\n{message.text}\n\nВы в меню", reply_markup=keyboard_all)


def del_notes(message):
    with open("bd.json", "r") as f:
        data = json.load(f)
    for i in range(len(data)):
        if data[i].get('login') == message.chat.id and data[i]['notes'].get(message.text):
            data[i]['notes'].pop(message.text, None)
            with open("bd.json", "w") as f:
                json.dump(data, f)
            return agent_ghost.send_message(message.chat.id, f"Запись за {message.text} успешно удалена!\n\nВы в меню", reply_markup=keyboard_all)
    else:
        return agent_ghost.send_message(message.chat.id, f"Записи за {message.text} не найдено!\n\nВы в меню", reply_markup=keyboard_all)


def view_notes_for_date(message):
    with open("bd.json", "r") as f:
        data = json.load(f)
    for i in range(len(data)):
        if data[i].get('login') == message.chat.id and data[i]['notes'].get(message.text):
            all_data_of_date = data[i]['notes'].get(message.text)
            c = int(len(all_data_of_date) / 4096)
            s = 0
            agent_ghost.send_message(message.chat.id, f"Запись за {message.text}:")
            for j in range(c+1):
                agent_ghost.send_message(message.chat.id, all_data_of_date[s:s+4096])
                s += 4096
            return agent_ghost.send_message(message.chat.id, "Вы в меню", reply_markup=keyboard_all)
    else:
        return agent_ghost.send_message(message.chat.id, f"Записи за {message.text} не найдено!\n\nВы в меню", reply_markup=keyboard_all)


def edit_notes_rewrite_dump(message):
    with open("bd.json", "r") as f:
        data = json.load(f)
    for i in range(len(data)):
        if data[i].get('login') == message.chat.id:
            for j in data[i]['notes']:
                if "r" in j:
                    date_edit = j[1:]
                    data[i]["notes"][date_edit] = message.text
                    data[i]["notes"].pop(j, None)
                    with open("bd.json", "w") as f:
                        json.dump(data, f)
                    return agent_ghost.send_message(message.chat.id, f"Запись за {date_edit} успешно изменена\n\nВы в меню", reply_markup=keyboard_all)


def edit_notes_add_dump(message):
    with open("bd.json", "r") as f:
        data = json.load(f)
    for i in range(len(data)):
        if data[i].get('login') == message.chat.id:
            for j in data[i]['notes']:
                if "r" in j:
                    all_data_of_date = data[i]['notes'].get(j)
                    date_edit = j[1:]
                    data[i]["notes"][date_edit] = all_data_of_date + message.text
                    data[i]["notes"].pop(j, None)
                    with open("bd.json", "w") as f:
                        json.dump(data, f)
                    return agent_ghost.send_message(message.chat.id, f"Добавлен текст к записи за {date_edit}\n\nВы в меню", reply_markup=keyboard_all)
