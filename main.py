import telebot, requests, os, sys
import json, pytz
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from seleniumfolder.parse_info_profile import *
from parsers.online_check import *
from seleniumfolder.parse_news import *
from seleniumfolder.parse_exchange import *
with open(R'D:\VScode\excalibur bot\data.json', 'r') as file:
    db = json.load(file)



bot = telebot.TeleBot("6429953074:AAHU4Hm05RiptHXq3qq2gZce4XXzt2AJhtE")
@bot.message_handler(commands=['help'])
def help(message):
    result = "Канал бота(новости об обновлениях) - https://t.me/excalburcraftbot_news"
    result += "\nТех.Поддержка - https://t.me/Kirill_Safebot" 
    bot.send_message(message.chat.id, result)
@bot.message_handler(commands=['reg'])
def registration(message):
    try:
        nickname = message.text.split(' ', 1)
        user_id = str(message.from_user.id)  # Convert user ID to a string
        if user_id not in db.keys():
            if len(nickname) > 1:
                nickname_yes = nickname[1]
                db[user_id] = nickname_yes
                with open('data.json', 'w') as file:
                    json.dump(db, file)
                bot.reply_to(message, "Вы успешно зарегистрировались\n\n/kabinet")
                print("Новый юзер" + db[user_id])
            else:
                bot.reply_to(message, "Укажите никнейм с учетом регистра после /reg {text}\n\nДля удаления профиля введите команду заного")
        else:
            bot.reply_to(message, "Ваш профиль удален, повторите попытку регистрации")
            del db[user_id]
            with open('data.json', 'w') as file:
                json.dump(db, file)
    except Exception as e:
        error_send_message(user_id, "/reg", e)

@bot.message_handler(commands=['stats'])
def send_user_list(message):
    try:
        user_id = str(message.from_user.id)
        user_list = "\n".join(db.values())
        user_count = len(db)
        response = f"Список пользователей ({user_count}):\n\n{user_list}"
        bot.send_message(message.chat.id, response)
    except Exception as e:
        error_send_message(user_id, "/stats", e)


@bot.message_handler(commands=['list'])
def list(message):
    bot.send_message(message.chat.id, "Список всех команд и пояснение к ним:\n/help - Тех.Поддержка\n/list - Список команд\n/start - Начальная команда\n/kabinet - Система личного кабинета с полной информацией о вашем профиле\n/username_search - поиск клана по Никнейму любого человека из него\n/description_search - поиск клана по его описанию\n/clanname_search - поиск клана по его названию\n/news - Последнии новости экскалибура\n/servers - бета команда\n/profile - поиск профиля человека по его Никнейму(Бета,реализовано в /username_search)\n/exchange - Получить информацию о последних ценах Клановой Биржи")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот пользуется открытым Excalibur Craft Clan API и selenium:\nСтатус работы: Альфа\nСписок Бета-Команд: /list /servers')

@bot.message_handler(commands=['kabinet'])
def kabinet(message):
    try:  
        user_id = str(message.from_user.id)
        if user_id not in db.keys():
            bot.send_message(message.chat.id, "Вы на данный момент не зарегистрированы в нашей системе, для регистрации введите команду /reg")
        else:
            bot.send_message(message.chat.id, "Поиск может занять до 40+ секунд. Ваш никнейм: " + db[user_id])

            data = get_clans_data()
            all_leaders = []
            found = False
            for clan, clan_data in data.items():
                if "leaders" in clan_data and clan_data["leaders"] is not None and len(clan_data["leaders"]) > 0:
                    all_leaders.extend(clan_data["leaders"]) 
                if "trusted" in clan_data and clan_data["trusted"] is not None and len(clan_data["trusted"]) > 0:
                    all_leaders.extend(clan_data["trusted"])
                if "officers" in clan_data and clan_data["officers"] is not None and len(clan_data["officers"]) > 0:
                    all_leaders.extend(clan_data["officers"])
                if "members" in clan_data and clan_data["members"] is not None and len(clan_data["members"]) > 0:
                    all_leaders.extend(clan_data["members"])
                if "newbies" in clan_data and clan_data["newbies"] is not None and len(clan_data["newbies"]) > 0:
                    all_leaders.extend(clan_data["newbies"])

                if db[user_id] in all_leaders:
                    found = True
                    bot.send_message(message.chat.id, format_clan_info(clan, clan_data))
                    info_name = get_source(db[user_id])
                    with open('outputPROFILE.png', 'rb') as photo:
                        bot.send_photo(message.chat.id, photo, caption=info_name)
                    os.remove("outputPROFILE.png")
                    break
        
            if not found:
                bot.send_message(message.chat.id, "Вы не состоите в клане либо неправильно зарегестрировались, попробуйте заново зарегестрироватся либо войдите в любой клан")
                info_name = get_source(db[user_id])
                if info_name != "Пользователь не найден":
                    with open('outputPROFILE.png', 'rb') as photo:
                        bot.send_photo(message.chat.id, photo, caption=info_name)
                    os.remove("outputPROFILE.png")
                else:
                    return
    except Exception as e:
        error_send_message(user_id, "/kabinet", e)

@bot.message_handler(commands=['username_search'])
def search_clan_by_user(message):
    try:
        user_id = str(message.from_user.id)
        user_message = message.text
        nickname = user_message.replace("/username_search  ", "")
        print(nickname)
        print(f"Сделан поиск клана по никнейму: {nickname}")
        data = get_clans_data()
        all_leaders = []
        found = False

        for clan, clan_data in data.items():
            if "leaders" in clan_data and clan_data["leaders"] is not None and len(clan_data["leaders"]) > 0:
                all_leaders.extend(clan_data["leaders"])
            if "trusted" in clan_data and clan_data["trusted"] is not None and len(clan_data["trusted"]) > 0:
                all_leaders.extend(clan_data["trusted"])
            if "officers" in clan_data and clan_data["officers"] is not None and len(clan_data["officers"]) > 0:
                all_leaders.extend(clan_data["officers"])
            if "members" in clan_data and clan_data["members"] is not None and len(clan_data["members"]) > 0:
                all_leaders.extend(clan_data["members"])
            if "newbies" in clan_data and clan_data["newbies"] is not None and len(clan_data["newbies"]) > 0:
                all_leaders.extend(clan_data["newbies"])

            if nickname in all_leaders:
                found = True
                bot.send_message(message.chat.id, format_clan_info(clan, clan_data))
                info_name = get_source(nickname)
                with open('outputPROFILE.png', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption=info_name)
                os.remove("outputPROFILE.png")
                break

        if not found:
            bot.send_message(message.chat.id, 'Увы, я не смог найти ваш клан\nПовторите попытку с учетом регистра\n\n/username_search')
            info_name = get_source(nickname)
            if info_name != "Пользователь не найден":
                os.remove("outputPROFILE.png")    
            else:
                with open('outputPROFILE.png', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption=info_name)
                return
    except Exception as e:
        error_send_message(user_id, "/search_clan_by_name", e)
        
        


@bot.message_handler(commands=['clanname_search'])
def search_clan_by_name(message):
    try:
        user_id = str(message.from_user.id)
        user_message = message.text
        name = user_message.replace("/username_search ", "")
        print(f"Сделан поиск клана по описанию: {name}")
        data = get_clans_data()
        found = False

        for clan, clan_data in data.items():
            if name.lower() == clan.lower():
                found = True
                bot.send_message(message.chat.id, format_clan_info(clan, clan_data))

        if not found:
            bot.send_message(message.chat.id, 'Увы, я не смог найти ваш клан.\n\n/clanname_search')
    except Exception as e:
        error_send_message(user_id, "/search_clan_by_name", e)
@bot.message_handler(commands=['description_search'])
def search_clan_by_description(message):
    try:
        user_id = str(message.from_user.id)
        user_message = message.text
        description = user_message.replace("/username_search ", "")
        print(f"Сделан поиск клана по описанию: {description}")
        data = get_clans_data()
        found = False

        for clan, clan_data in data.items():
            if description.lower() == clan_data['motto'].lower():
                found = True
                bot.send_message(message.chat.id, format_clan_info(clan, clan_data))

        if not found:
            bot.send_message(message.chat.id, 'Увы, я не смог найти ваш клан\nПовторите попытку с учетом регистра\n\n/description_search')
    except Exception as e:
        error_send_message(user_id, "/description_search", e)
def get_clans_data():
    response = requests.get('https://excalibur-craft.ru/engine/ajax/clans/api.php')
    data = response.json()
    return data

def format_clan_info(clan, clan_data):
    members = ", ".join(clan_data['members']) if clan_data['members'] is not None else "Нету"
    officers = ", ".join(clan_data['officers']) if clan_data['officers'] is not None else "Нету"
    trusted = ", ".join(clan_data['trusted']) if clan_data['trusted'] is not None else "Нету"
    leaders = ", ".join(clan_data['leaders']) if clan_data['leaders'] is not None else "Нету"
    newbies = ", ".join(clan_data['newbies']) if clan_data['newbies'] is not None else "Нету"

    return (f"Клан: {clan}\n"
            f"Айди: {clan_data['id']}\n"
            f"Опыт: {clan_data['xp']}\n"
            f"Опыт за неделю: {clan_data['week_xp']}\n"
            f"Голоса: {clan_data['votes']}\n"
            f"Описание: {clan_data['motto']}\n"
            f"Новенькие: {newbies}\n"
            f"Участники: {members}\n"
            f"Доверенные: {trusted}\n"
            f"Офицеры: {officers}\n"
            f"Лидеры: {leaders}\n"
            f"Ссылка: https://excalibur-craft.ru/index.php?do=clans&go=profile&id={clan_data['id']}")

@bot.message_handler(commands=['servers'])
def online(message):
    try:
        user_id = str(message.from_user.id)
        bot.send_message(message.chat.id, beta_parse())
    except Exception as e:
        error_send_message(user_id, "/servers", e)
def beta_parse():
    txt = []
    txt.append(parse_online_players())
    txt.append("\n")
    txt.append("\n")
    txt.append(str(parse_top_players()))
    txt.append("\n")
    txt.append("Онлайн серверов:")
    txt.append("\n")
    txt.append(parse_online_servers())
    result = ''.join(map(str, txt))
    return result


#parse_info_profile.py импортируем команды


@bot.message_handler(commands=["profile"])
def search_profile(message):
    try:
        user_id = str(message.from_user.id)
        user_message = message.text
        name = user_message.replace("/profile ", "")
        if name == "/profile":
            bot.send_message(message.chat.id, "Введите имя пользователя либо зарегестрируйтесь\n/reg /profile")
            return
        found = False
        bot.send_message(message.chat.id, "Поиск может занять некоторое время")
        info_name = get_source(name)
        bot.send_message(message.chat.id, info_name)
        if info_name != "Пользователь не найден":
            with open('outputPROFILE.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo)
        else:
            return
    except Exception as e:
        error_send_message(user_id, "/profile", e)
@bot.message_handler(commands=['news'])
def news(message):
    user_id = str(message.from_user.id)
    try:
        crop_screenshot()
        with open('output.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption="Последнии новости экскалибура")
        os.remove("output.png")
    except Exception as e:
        error_send_message(user_id, "/news", e)

@bot.message_handler(commands=['exchange'])
def exchange(message):
    user_id = str(message.from_user.id)
    try:
        exchange = get_exchange()
        with open('exchangeoutput.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=exchange)
    except Exception as e:
        error_send_message(user_id, "/exchange", e)
def main():
    while True:
        try:
            print("     Bot succes started!")
            print(db.keys())
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(15)  # Ждем 15 секунд перед повторным запуском
def get_time_for_debuging():
    ekb_tz = pytz.timezone('Asia/Yekaterinburg')
    msk_tz = pytz.timezone('Europe/Moscow')
    utc_now = datetime.now(pytz.UTC)
    ekb_time = utc_now.astimezone(ekb_tz)
    msk_time = utc_now.astimezone(msk_tz)
    ekb_formatted = ekb_time.strftime('%H:%M')
    msk_formatted = msk_time.strftime('%H:%M')
    return f"{ekb_formatted} ЕКБ {msk_formatted} МСК"
def error_send_message(user_id, command, e ):
    time = get_time_for_debuging()
    message = "Отправьте данный лог в тех.поддержку:\n"
    message += f"```python\n{e}\n```\n"
    message += f"Использовано `{command}` пользователем `{user_id}` в `{time}`"
    bot.send_message(user_id, message, parse_mode='Markdown')
if __name__ == '__main__':
    main()