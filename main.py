import telebot, requests, os, sys
import json, pytz
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from seleniumfolder.parse_info_profile import *
from parsers.online_check import *
from seleniumfolder.parse_news import *
from seleniumfolder.parse_exchange import *
with open('config.json', 'r') as file:
    data = json.load(file)
token = data['token']
def get_nickname_from_file(file_name):
    try:
        with open(file_name,"r") as file:
            for line in file:
                if line.startswith("nickname:"):
                    nickname = line.strip().split(":")[1]
                    return nickname
        return None  # Если nickname не найден
    except FileNotFoundError:
        print("Файл не найден")
        return None
def get_fun_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            for line in file:
                if line.startswith("fun:"):
                    fun = line.strip().split(":")[1]
                    return fun
    except FileNotFoundError:
        return None

def get_rlk_from_files(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith("rlk:"):
                return line.strip().split(":")[1]
    return None
def get_all_usernames_from_files(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith("nickname:"):
                return line.strip().split(":")[1]
    return None

def set_fun_in_file(file_name, fun_value):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    with open(file_name, 'w') as file:
        for line in lines:
            if line.startswith("fun:"):
                line = f"fun:{fun_value}\n"
            file.write(line)

def set_rlk_in_file(file_name, rlk):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    with open(file_name, 'w') as file:
        for line in lines:
            if line.startswith("rlk:"):
                line = f"rlk:{rlk}\n"
            file.write(line)

bot = telebot.TeleBot(token)



@bot.message_handler(commands=['click'])
def click_command(message):
    try:
        user_id = str(message.from_user.id)
        file_name = user_id + ".txt"
        user_data = get_fun_from_file(file_name)
        if user_data is None:
            bot.send_message(message.chat.id, "Вы не зарегистрированы.\nРегистрация - /reg")
            return
        if user_data == "False":
            bot.send_message(message.chat.id, "Вы не зарегистрированы на ивенте.\nРегистрация - /fun")
        if user_data == "True":
            rlk_money = get_rlk_from_files(file_name)
            if rlk_money is not None:
                rlk_money = int(rlk_money)
                rlk_money += 1
                bot.send_message(message.chat.id, f"Ты заработал 1 рлк! Твой баланс теперь {rlk_money}")
                set_rlk_in_file(file_name, rlk_money)
    except Exception as e:
        error_send_message(user_id, "/click", e)
        
def get_rlk_from_files(file_name):
    with open(file_name, 'r') as file:
        for line in file:
            if line.startswith("rlk:"):
                return int(line.strip().split(":")[1])
    return 0

# Команда для бота /top
@bot.message_handler(commands=['top'])
def top_players(message):
    try:
        user_id = str(message.from_user.id)
        file_list = os.listdir()
        player_rlk = []

        for file_name in file_list:
            if file_name.endswith('.txt'):
                user_id = file_name.split('.')[0]
                rlk = get_rlk_from_files(file_name)
                nickname = get_nickname_from_file(file_name)
                print(nickname)
                if rlk == 0:
                    continue
                player_rlk.append((nickname, rlk))

        top_10_players = sorted(player_rlk, key=lambda x: x[1], reverse=True)[:10]
        top_players_str = "Топ 10 игроков по РЛК:\n"
        for i, (user_id, rlk) in enumerate(top_10_players):
            top_players_str += f"{i+1}. Никнейм: {user_id}, РЛК: {rlk}\n"

        bot.reply_to(message, top_players_str)
    except Exception as e:
        error_send_message(user_id, "/top", e)
@bot.message_handler(commands=['fun'])
def fun_command(message):
    try:
        user_id = str(message.from_user.id)
        file_name = user_id + ".txt"
        print(file_name)
        user_data = get_fun_from_file(file_name)
        print(user_data)
        if user_data is None:
            bot.send_message(message.chat.id, "Вы не зарегистрированы.\nРегистрация - /reg")
            return
        if user_data == "False":
            bot.send_message(message.chat.id, "Подожди, регистрирую тебя в ивенте")
            time.sleep(1)
            set_fun_in_file(file_name, True)
            bot.send_message(message.chat.id, "Окей...")
            time.sleep(1)
            with open('thanks.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Напиши еще раз команду /fun")
        if user_data == "True":
            rlk_money = get_rlk_from_files(file_name)
            bot.send_message(message.chat.id, f'Привет, ты попал на новый локальный "ивент"\nОшибки насчет его наверное расматриватся не будут,сделан ради потешки\nТвой баланс: {rlk_money} РЛК\n\nКоманда для заработка: /click\nТоп-Игроков /top')
        
    except Exception as e:
        error_send_message(user_id, "/fun", e)
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
        file_name = user_id + ".txt"
        try:
            with open(file_name, 'r') as file:
                data = file.read()
                if data:  # Если файл не пустой, значит пользователь уже зарегистрирован
                    bot.reply_to(message, "Ваш профиль успешно не удален")
                    return
        except FileNotFoundError:
            pass  # Продолжаем регистрацию, если файл не найден

        if len(nickname) > 1:
            nickname_yes = nickname[1]
            with open(file_name, 'w') as file:
                file.write("nickname:" + nickname_yes + "\nfun:False" + "\nrlk:0")
            with open('thanks.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="/kabinet\n/fun (НОВИНКА!)")
            print("Новый юзер " + nickname_yes)
        else:
            bot.reply_to(message, "Укажите никнейм с учетом регистра после /reg {text}\n\nДля удаления профиля введите команду заного")
    except Exception as e:
        error_send_message(user_id, "/reg", e)




@bot.message_handler(commands=['stats'])
def send_user_list(message):
    try:
        user_id = str(message.from_user.id)
        file_names = [file for file in os.listdir() if file.endswith(".txt")]
        usernames = []
        for file_name in file_names:
            username = get_all_usernames_from_files(file_name)
            if username:
                usernames.append(username)

        response = f"Список пользователей ({len(usernames)}):\n\n"
        response += "\n".join(usernames)
        bot.send_message(message.chat.id, response)

    except Exception as e:
        error_send_message(user_id, "/stats", e)

@bot.message_handler(commands=['list'])
def list(message):
    bot.send_message(message.chat.id, "Список всех команд и пояснение к ним:\n/help - Тех.Поддержка\n/list - Список команд\n/start - Начальная команда\n/kabinet - Система личного кабинета с полной информацией о вашем профиле\n/username_search - поиск клана по Никнейму любого человека из него\n/description_search - поиск клана по его описанию\n/clanname_search - поиск клана по его названию\n/news - Последнии новости экскалибура\n/servers - Онлайн и последний вайп серверов\n/profile - поиск профиля человека по его Никнейму(Бета,реализовано в /username_search)\n/exchange - Получить информацию о последних ценах Клановой Биржи")
    bot.send_message(message.chat.id, "/click (НОВИНКА)\n/fun (НОВИНКА)\n/top (НОВИНКА)")
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот пользуется открытым Excalibur Craft Clan API и selenium:\nСтатус работы: Альфа\nСписок Бета-Команд: /list /servers')

@bot.message_handler(commands=['kabinet'])
def kabinet(message):
    try:
        user_id = str(message.from_user.id)
        file_name = user_id + ".txt"
        print(file_name)
        nickname = get_nickname_from_file(file_name)
        if nickname == None:
            bot.send_message(message.chat.id, "Вы не зарегестриованы.\nРегистрация - /reg")
            return
        
        bot.send_message(message.chat.id, "Поиск может занять до 40+ секунд. Ваш никнейм: ")
        
        
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
            bot.send_message(message.chat.id, "Вы не состоите в клане либо неправильно зарегистрировались, попробуйте заново зарегистрироватся либо войдите в любой клан")
            info_name = get_source(nickname)
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
            if info_name == 1337:
                print(123)
                return
            else:
                print(312)
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
        bot.send_message(message.chat.id, beta_parse(), parse_mode='Markdown')
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
    
    servers_info = parse_online_servers()
    for server in servers_info:
        txt.append(f"`{server['Server Name']}` {server['Server Version']}  Вайп: `{server['Wipe Date']}`\n")
        txt.append(f"Игроки онлайн: {server['Players Online']}/{server['Max Players']}\n")
        txt.append("\n")
        

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
            bot.send_photo(message.chat.id, photo, caption="Последнии новости экскалибура\nТак-же внутри бота началось фан-ивент. Для регистрации - /fun")
        os.remove("output.png")
    except Exception as e:
        error_send_message(user_id, "/news", e)

@bot.message_handler(commands=['exchange'])
def exchange(message):
    user_id = str(message.from_user.id)
    try:
        exchange = get_exchange()
        if exchange == "Клановая система находится на технических работах, повторите позже":
            bot.send_message(message.chat.id, exchange)
        else:
            with open('exchangeoutput.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=exchange)
    except Exception as e:
        error_send_message(user_id, "/exchange", e)
def main():
    while True:
        try:
            print("     Bot succes started!")
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