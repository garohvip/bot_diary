import json
from config import token
from telebot import types
import telebot

agent_ghost = telebot.TeleBot(token)

keyboard_all = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_all.add(types.KeyboardButton("Записи"),
                 types.KeyboardButton("Планы"))


def del_notes(message):
    with open("bd.json", "r") as f:
        data = json.load(f)
    for i in range(len(data)):
        if data[i].get('login') == message.chat.id and data[i]['plan'].get(message.text):
            data[i]['plan'].pop(message.text, None)
            with open("bd.json", "w") as f:
                json.dump(data, f)
            return agent_ghost.send_message(message.chat.id, f"План за {message.text} успешно удален!\n\nВы в меню", reply_markup=keyboard_all)
    else:
        return agent_ghost.send_message(message.chat.id, f"Плана за {message.text} не найдено!\n\nВы в меню", reply_markup=keyboard_all)


def view_plan_for_date(message):
    with open("bd.json", "r") as f:
        data = json.load(f)
    for i in range(len(data)):
        if data[i].get('login') == message.chat.id and data[i]['plan'].get(message.text):
            all_data_of_date = data[i]['plan'].get(message.text)
            c = []
            for j in range(len(all_data_of_date)):
                c.append(f"{j+1}) {all_data_of_date.get(str(j+1))}\n")
            agent_ghost.send_message(message.chat.id, f"План за {message.text}:\n\n{''.join([el for el in c])}")
            return agent_ghost.send_message(message.chat.id, "Вы в меню", reply_markup=keyboard_all)
    else:
        return agent_ghost.send_message(message.chat.id, f"Плана за {message.text} не найдено!\n\nВы в меню", reply_markup=keyboard_all)


def edit_plan_dump(message):
    with open("bd.json", "r") as f:
        data = json.load(f)
    for i in range(len(data)):
        if data[i].get('login') == message.chat.id:
            for j in data[i]['plan']:
                if "r" in j:
                    for k in data[i]['plan'][j]:
                        if "r" in k:
                            data[i]['plan'][j][k] = message.text
                            data[i]['plan'][j][k[1:]] = data[i]['plan'][j].pop(k)
                            data[i]['plan'][j[1:]] = data[i]['plan'].pop(j)
                            with open("bd.json", "w") as f:
                                json.dump(data, f)
                            return agent_ghost.send_message(message.chat.id, "Пункт плана был успешно изменен\n\nВы в меню", reply_markup=keyboard_all)
