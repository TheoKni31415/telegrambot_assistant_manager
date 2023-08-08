import json
import telebot
import traceback
from datetime import datetime
from time import sleep
from telebot import types

bot = telebot.TeleBot('6011317370:AAFElMJAy4PsDtzJLZwAhN-uhXqRRQO266M')
file_path = "mydata.json"
name = ""
id = ""
post = ""

def check_dir(mydir, id, name):
    if str(id) in mydir["celler"]:
        return mydir
    else:
        mydir["celler"][str(id)] = {}
        mydir["celler"][str(id)]["name"] = name
        mydir["celler"][str(id)]["tasks"] = []
        return mydir

def check_tasks(dir, task):
    try:
        for i in dir["celler"]:
            if task in dir["celler"][i]["tasks"]:
                return True
        return False
    except:
        return False

def man_or_cell():
    keyboard = types.InlineKeyboardMarkup()
    key_man = types.InlineKeyboardButton(text='Менеджер', callback_data='manager')
    key_sel = types.InlineKeyboardButton(text='Продавец', callback_data='celler')
    keyboard.add(key_man)
    keyboard.add(key_sel)
    return keyboard

def manager(cellrs, id):
    keyboard = types.InlineKeyboardMarkup()
    for id in cellrs["celler"]:
        len_task = len(cellrs["celler"][id]["tasks"])
        count = 0
        for task in cellrs["celler"][id]["tasks"]:
            if task.startswith("✅"):
                count += 1
        task_value = f"{count}/{len_task}"
        keyboard.add(types.InlineKeyboardButton(text=f'{cellrs["celler"][id]["name"]} {task_value}', callback_data=str(id)))
    keyboard.add(types.InlineKeyboardButton(text="Уволиться", callback_data=f"del_{id}_self"))
    keyboard.add(types.InlineKeyboardButton(text="Обновить", callback_data="m_update"))
    return keyboard

def man_tasks(m_tasks, id):
    count = 0
    keyboard = types.InlineKeyboardMarkup()
    for i in m_tasks["celler"][id]["tasks"]:
        keyboard.add(types.InlineKeyboardButton(text=i, callback_data=f"m_{i}_{id}_{count}"))
        count += 1
    add_t = types.InlineKeyboardButton(text="Назначить", callback_data=f"add_task_{id}")
    dele = types.InlineKeyboardButton(text="Уволить", callback_data=f"delete_{id}")
    keyboard.add(add_t, dele)
    backtos = types.InlineKeyboardButton(text="Назад", callback_data=f"backto_{id}")
    keyboard.add(backtos)
    return keyboard

def in_task(id):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Назад", callback_data=f"back_task_{id}"))
    return keyboard


def man_yes_no(id, pos):
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data=f"m_{id}_{pos}_yes")
    no = types.InlineKeyboardButton(text="Нет", callback_data=f"m_{id}_{pos}_no")
    keyboard.add(yes, no)
    return keyboard

def del_yes_no(id):
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data=f"d_{id}_yes")
    no = types.InlineKeyboardButton(text="Нет", callback_data=f"d_{id}_no")
    keyboard.add(yes, no)
    return keyboard

def del_self_y_n(id):
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data=f"self_{id}_yes")
    no = types.InlineKeyboardButton(text="Нет", callback_data=f"self_{id}_no")
    keyboard.add(yes, no)
    return keyboard

def cell_tasks(c_tasks, id):
    count = 0
    keyboard = types.InlineKeyboardMarkup()
    for i in c_tasks["celler"][id]["tasks"]:
        keyboard.add(types.InlineKeyboardButton(text=i, callback_data=f"c_{i}_{id}_{count}"))
        count += 1
    keyboard.add(types.InlineKeyboardButton(text="Обновить", callback_data=f"c_update_{id}"))
    return keyboard

def cell_yes_no(id):
    keyboard = types.InlineKeyboardMarkup()
    yes = types.InlineKeyboardButton(text="Да", callback_data=f"c_{id}_yes")
    no = types.InlineKeyboardButton(text="Нет", callback_data=f"c_{id}_no")
    keyboard.add(yes, no)
    return keyboard

def save_dictionary(dictionary):
    with open(file_path, 'w', encoding="utf-8") as file:
        json.dump(dictionary, file, ensure_ascii=False)


def load_dictionary():
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"manager": {}, "celler": {}, "ignore": []}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        global id
        global mydir
        global manager_id
        mydir = load_dictionary()
        check_id = str(message.chat.id)
        if check_id in mydir["ignore"]:
            text_ignore = "Ты не можешь пользоваться этим ботам по решению менеджера. Если это сделано по ошибки, обратись к нему."
            bot.send_message(message.chat.id, text_ignore)

        elif check_id in mydir["manager"]:
            manager_id = int(check_id)
            text_start_m = f"Привет, {mydir['manager'][str(message.chat.id)]}, вот твои сотрудники."
            bot.send_message(message.chat.id, text=text_start_m, reply_markup=manager(mydir, manager_id))
        elif check_id in mydir["celler"]:
            text_start_c = f"Привет, {mydir['celler'][str(message.chat.id)]['name']}, вот твои задачи."
            bot.send_message(message.chat.id, text=text_start_c, reply_markup=cell_tasks(mydir, str(message.chat.id)))
        else:
            bot.send_message(message.chat.id, "Привет, я твой бот-помощник. Для начала напиши 'Привет'.")
            id = message.from_user.id
    except:
        dt_now = str(datetime.now())
        var = dt_now + traceback.format_exc()
        bot.send_message(466449753, var)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def acquaintance(message):
    global mydir
    try:
        mydir = load_dictionary()
        check_id = str(message.chat.id)
        if check_id in mydir["ignore"]:
            text_ignore = "Ты не можешь пользоваться этим ботом по решению менеджера. Если это сделано по ошибки, обратись к нему."
            bot.send_message(message.chat.id, text_ignore)
            message.text = "ignore"

        elif message.text.lower() == "привет":
            bot.send_message(message.chat.id, "Как тебя зовут?")
            bot.register_next_step_handler(message, get_name)

        elif message.text == "/help":
            bot.send_message(message.chat.id, "Для начала напиши 'Привет'")
        elif message.text.lower().startswith("t"):
            try:
                if str(message.chat.id) in mydir["manager"]:
                    if len(message.text) - 1 <= 22:
                        name_cel = mydir["celler"][id_task_celler]["name"]
                        mydir["celler"][id_task_celler]["tasks"].append(f"❌{message.text[1:]}")
                        bot.send_message(message.chat.id, text=name_cel, reply_markup=man_tasks(mydir, id_task_celler))
                        bot.send_message(int(id_task_celler), text="Тебе назначена задача", reply_markup=cell_tasks(mydir, id_task_celler))
                    else:
                        wrong_len = f"Длина задания не должна превышать 22 символа с учетом пробелов. Длина твоего задания - {len(message.text) - 1}."
                        bot.send_message(message.chat.id, text=wrong_len)
                else:
                    text_c = "Для использования этой команды нужно быть менеджером. Пока это не ты) Вот твои задачи."
                    bot.send_message(message.chat.id, text=text_c, reply_markup=cell_tasks(mydir, str(message.chat.id)))
            except:
                var = traceback.format_exc()
                bot.send_message(466449753, var)
                text_e = "Для этой команды нужно выбрать сотрудника для составления задачи. Или что то пошло не так. Давай начнем сначала)"
                bot.send_message(message.chat.id, text_e)

        elif message.text == "ignore":
            pass

        else:
            bot.send_message(message.chat.id, "Не понимаю тебя, напиши /help")
        save_dictionary(mydir)
    except:
        dt_now = str(datetime.now())
        var = dt_now + traceback.format_exc()
        bot.send_message(466449753, var)

def get_name(message):
    global name
    global mydir
    try:
        mydir = load_dictionary()
        name = message.text
        keyboard = man_or_cell()
        question = "В какой должности работаешь?"
        bot.send_message(message.chat.id, text=question, reply_markup=keyboard)
        save_dictionary(mydir)
    except:
        dt_now = str(datetime.now())
        var = dt_now + traceback.format_exc()
        bot.send_message(466449753, var)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global post
    global mydir
    global task_t
    global task_pos
    global id_task_celler
    try:
        mydir = load_dictionary()
        post = call.data
        id = str(call.message.chat.id)
        check_id = str(call.message.chat.id)
        if check_id in mydir["ignore"]:
            text_ignore = "Ты не можешь пользоваться этим ботам по решению менеджера. Если это сделано по ошибки, обратись к нему."
            bot.send_message(call.message.chat.id, text_ignore)
            post = "ignore"

        elif post == "manager":
            if not mydir["manager"]:
                manager_id = str(call.message.chat.id)
                mydir[post][id] = name
                save_dictionary(mydir)
                mystr = f"Итак, тебя зовут {name} и твоя должость Менеджер. Запомню)\nДобро пожаловать в нашу команду 'Ковры и Свет'."
                bot.send_message(call.message.chat.id, mystr)
                mydir = load_dictionary()
                bot.send_message(call.message.chat.id, text="Твои сотрудники", reply_markup=manager(mydir, manager_id))
            else:
                str_f = "Позиция менеджера уже занята. Подумай получше."
                bot.send_message(call.message.chat.id, text=str_f, reply_markup=man_or_cell())

        elif post in mydir["celler"]:
            id_celler = post
            name_id = mydir["celler"][id_celler]["name"]
            bot.send_message(call.message.chat.id, text=name_id, reply_markup=man_tasks(mydir, id_celler))

        elif len(post.split("_")) == 4 and post.split("_")[0] == "m" and check_tasks(mydir, post.split("_")[1]):
            task_pos = int(post.split("_")[3])
            id_pos = task_pos
            task_id = post.split("_")[2]
            bot.send_message(call.message.chat.id, text="Сотрудник выполнил задачу?", reply_markup=man_yes_no(task_id, id_pos))

        elif len(post.split("_")) == 4 and post.split("_")[0] == "m" and post.split("_")[3] == "no":
            id_celler = post.split("_")[1]
            id_pos = int(post.split("_")[2])
            word = mydir["celler"][id_celler]["tasks"][id_pos]
            word = word.replace("✅","❌", 2)
            mydir["celler"][id_celler]["tasks"][id_pos] = word
            name_id = mydir["celler"][id_celler]["name"]
            bot.send_message(call.message.chat.id, text=name_id, reply_markup=man_tasks(mydir, id_celler))
            bot.send_message(int(id_celler), text="Менеджер отклонил выполнение задачи", reply_markup=cell_tasks(mydir, id_celler))

        elif len(post.split("_")) == 4 and post.split("_")[0] == "m" and post.split("_")[3] == "yes":
            id_celler = post.split("_")[1]
            name_id = mydir["celler"][id_celler]["name"]
            del mydir["celler"][id_celler]["tasks"][task_pos]
            bot.send_message(call.message.chat.id, text=name_id, reply_markup=man_tasks(mydir, id_celler))

        elif len(post.split("_")) == 2 and post.split("_")[0] == "m" and post.split("_")[1] == "update":
            manager_id = str(call.message.chat.id)
            bot.send_message(call.message.chat.id, text="Твои сотрудники", reply_markup=manager(mydir, manager_id))

        elif len(post.split("_")) == 2 and post.split("_")[0] == "backto":
            manager_id = str(call.message.chat.id)
            bot.send_message(call.message.chat.id, text="Твои сотрудники", reply_markup=manager(mydir, manager_id))

        elif len(post.split("_")) == 2 and post.split("_")[0] == "delete":
            mytext = "Сотрудник решил развиваться в другой компании?"
            id_celler = post.split("_")[1]
            bot.send_message(call.message.chat.id, text=mytext, reply_markup=del_yes_no(id_celler))

        elif len(post.split("_")) == 3 and post.split("_")[0] == "d" and post.split("_")[2] == "no":
            id_celler = post.split("_")[1]
            name_id = mydir["celler"][id_celler]["name"]
            bot.send_message(call.message.chat.id, text=name_id, reply_markup=man_tasks(mydir, id_celler))

        elif len(post.split("_")) == 3 and post.split("_")[0] == "d" and post.split("_")[2] == "yes":
            manager_id = str(call.message.chat.id)
            id_celler = post.split("_")[1]
            del mydir["celler"][id_celler]
            mydir["ignore"].append(id_celler)
            str_del = "Менеджер ограничил тебя в использовании этим ботом. Если это сделано по ошибке, обратись к своему менеджеру."
            bot.send_message(int(id_celler), text=str_del)
            bot.send_message(call.message.chat.id, text="Твои сотрудники", reply_markup=manager(mydir, manager_id))

        elif len(post.split("_")) == 3 and post.split("_")[0] == "del" and post.split("_")[2] == "self":
            id_del_self = post.split("_")[1]
            bot.send_message(call.message.chat.id, text="Точно?", reply_markup=del_self_y_n(id_del_self))

        elif len(post.split("_")) == 3 and post.split("_")[0] == "self" and post.split("_")[2] == "no":
            id_del_self = post.split("_")[1]
            bot.send_message(call.message.chat.id, text="Твои сотрудники", reply_markup=manager(mydir, id_del_self))

        elif len(post.split("_")) == 3 and post.split("_")[0] == "self" and post.split("_")[2] == "yes":
            id_self = post.split("_")[1]
            self_str = "Теперь ты не можешь пользоваться этим ботом. Если твое действие было совершено по ошибке, обратись к создателю этого бота."
            del mydir["manager"][id_self]
            mydir["ignore"].append(id_self)
            bot.send_message(call.message.chat.id, text=self_str)

        elif len(post.split("_")) == 3 and post.split("_")[0] == "add" and post.split("_")[1] == "task":
            id_task_celler = post.split("_")[2]
            bot.send_message(call.message.chat.id, text="Введи 't' и сразу описание задачи",
                             reply_markup=in_task(id_task_celler))

        elif len(post.split("_")) == 3 and post.split("_")[0] == "back" and post.split("_")[1] == "task":
            id_celler = post.split("_")[2]
            name_id = mydir["celler"][id_celler]["name"]
            bot.send_message(call.message.chat.id, text=name_id, reply_markup=man_tasks(mydir, id_celler))


        elif post == "celler":
            id = str(call.message.chat.id)
            mydir = check_dir(mydir, id, name)
            save_dictionary(mydir)
            mydir = load_dictionary()
            mystr = f"Итак, тебя зовут {name} и твоя должность Продавец. Запомню)\nДобро пожаловать в нашу команду 'Ковры и Свет'."
            bot.send_message(call.message.chat.id, mystr)
            bot.send_message(call.message.chat.id, text="Твои задачи", reply_markup=cell_tasks(mydir, id))

        elif len(post.split("_")) == 3 and post.split("_")[0] == "c" and post.split("_")[1] == "update":
            id_c_update = str(call.message.chat.id)
            bot.send_message(call.message.chat.id, text="Твои задачи", reply_markup=cell_tasks(mydir, id_c_update))

        elif len(post.split("_")) == 4 and post.split("_")[0] == "c" and check_tasks(mydir, post.split("_")[1]):
            task_pos = int(post.split("_")[3])
            id_c = str(call.message.chat.id)
            bot.send_message(call.message.chat.id, text="Задача выполнена?", reply_markup=cell_yes_no(id_c))

        elif len(post.split("_")) == 3 and post.split("_")[0] == "c" and post.split("_")[2] == "no":
            id_c_no = str(call.message.chat.id)
            bot.send_message(call.message.chat.id, text="Твои задачи", reply_markup=cell_tasks(mydir, id_c_no))

        elif len(post.split("_")) == 3 and post.split("_")[0] == "c" and post.split("_")[2] == "yes":
            id_c_yes = str(call.message.chat.id)
            id_now = id_c_yes
            c_now_name = mydir["celler"][id_c_yes]["name"]
            word = mydir["celler"][id_c_yes]["tasks"][task_pos]
            word = word.replace("❌", "✅")
            mydir["celler"][id_c_yes]["tasks"][task_pos] = word

            bot.send_message(call.message.chat.id, text="Твои задачи", reply_markup=cell_tasks(mydir, id_c_yes))
            for k, v in mydir['manager'].items():
                bot.send_message(k, text=f"{c_now_name} пометил свое задание как выполненное.", reply_markup=man_tasks(mydir, id_now))

        elif post == "ignore":
            pass

        save_dictionary(mydir)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except:
        dt_now = str(datetime.now())
        var = dt_now + traceback.format_exc()
        bot.send_message(466449753, var)


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as _ex:
        print(_ex)
        sleep(15)

#telegrambot_assistant_manager