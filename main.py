
import telebot, requests, os, sys
import json, pytz
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from seleniumfolder.parse_info_profile import *
from parsers.online_check import *
from seleniumfolder.parse_news import *
from seleniumfolder.parse_exchange import *
with open('config.json', 'r') as file:
    data_token = json.load(file)
token = data_token['token']


def get_all_usernames_from_files():
    with open('users.json', 'r') as file:
        data = json.load(file)
        usernames = []
        for user_id, user_data in data['users'].items():
            usernames.append(user_data['nickname'])
        return usernames


def get_user_data(user_id):
    data = {}
    with open('users.json', 'r') as file:
        data = json.load(file)
    return data['users'][user_id]


def set_user_data(user_id, data):
    with open('users.json', 'r') as file:
        users_data = json.load(file)
    users_data['users'][user_id] = data
    with open('users.json', 'w') as file:
        json.dump(users_data, file, indent=4)


def register_user(user_id, nickname):
    data = {}
    with open('users.json', 'r') as file:
        data = json.load(file)
    data['users'][user_id] = {'nickname': nickname, 'fun': False, 'rlk': 0}
    with open('users.json', 'w') as file:
        json.dump(data, file, indent=4)


def get_rlk_from_files(user_id):
    data = get_user_data(user_id)
    return data['rlk']


def set_rlk_in_file(user_id, rlk):
    user_data = get_user_data(user_id)
    user_data['rlk'] = rlk
    set_user_data(user_id, user_data)


def set_fun_in_file(user_id, fun_value):
    user_data = get_user_data(user_id)
    user_data['fun'] = fun_value
    set_user_data(user_id, user_data)


bot = telebot.TeleBot(token)


# Команда для бота /click
@bot.message_handler(commands=['click'])
def click_command(message):
    try:
        user_id = str(message.from_user.id)
        user_data = get_user_data(user_id)
        print(f"Пользователь: {user_id}, данные: {user_data}")
        if user_data is None:
            bot.send_message(message.chat.id,
                             "Вы не зарегистрированы.\nРегистрация - /reg")
            return
        if user_data['fun'] == "False":
            bot.send_message(
                message.chat.id,
                "Вы не зарегистрированы на ивенте.\nРегистрация - /fun")
        if user_data['fun'] == "True":
            rlk_money = get_rlk_from_files(user_id)
            if rlk_money is not None:
                rlk_money += 1
                bot.send_message(
                    message.chat.id,
                    f"Ты заработал 1 рлк! Твой баланс теперь {rlk_money}")
                set_rlk_in_file(user_id, rlk_money)
    except Exception as e:
        error_send_message(user_id, "/click", e)


# Команда для бота /top
@bot.message_handler(commands=['top'])
def top_players(message):
    try:
        user_id = str(message.from_user.id)
        usernames = get_all_usernames_from_files()
        player_rlk = []

        for username in usernames:
            user_data = get_user_data(username)
            if user_data['rlk'] == 0:
                continue
            player_rlk.append((username, user_data['rlk']))

        top_10_players = sorted(player_rlk, key=lambda x: x[1],
                                reverse=True)[:10]
        top_players_str = "Топ 10 игроков по РЛК:\n"
        for i, (user_id, rlk) in enumerate(top_10_players):
            top_players_str += f"{i+1}. Никнейм: {user_id}, РЛК: {rlk}\n"

        bot.reply_to(message, top_players_str)
    except Exception as e:
        error_send_message(user_id, "/top", e)


# Команда - /fun
@bot.message_handler(commands=['fun'])
def fun_command(message):
    try:
        user_id = str(message.from_user.id)
        user_data = get_user_data(user_id)
        print(user_data)
        if user_data is None:
            bot.send_message(message.chat.id,
                             "Вы не зарегестриованы.\nРегистрация - /reg")
            return
        if user_data['fun'] == "False":
            bot.send_message(message.chat.id,
                             "Подожди, регистрирую тебя в ивенте")
            time.sleep(1)
            set_fun_in_file(user_id, True)
            bot.send_message(message.chat.id, "Окей...")
            time.sleep(1)
            with open('thanks.png', 'rb') as photo:
                bot.send_photo(message.chat.id,
                               photo,
                               caption="Напиши еще раз команду /fun")
        if user_data['fun'] == "True":
            rlk_money = get_rlk_from_files(user_id)
            bot.send_message(
                message.chat.id,
                f'Привет, ты попал на новый локальный "ивент"\nОшибки насчет его наверное расматриватся не будут,сделан ради потешки\nТвой баланс: {rlk_money} РЛК\n\nКоманда для заработка: /click\nТоп-Игроков /top'
            )

    except Exception as e:
        error_send_message(user_id, "/fun", e)


# Команда - /help
@bot.message_handler(commands=['help'])
def help(message):
    result = "Канал бота(новости об обновлениях) - https://t.me/excalburcraftbot_news"
    result += "\nТех.Поддержка - https://t.me/Kirill_Safebot"
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['reg'])
def registration(message):
    user_id = str(message.from_user.id)
    try:
        try:
            data = get_user_data(user_id)
            nickname = message.text.split(' ')[1]
            register_user(user_id, nickname)
            with open('thanks.png', 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="/kabinet\n/fun (НОВИНКА!)")
            print("Новый юзер " + nickname)
        except IndexError:
            bot.send_message(message.chat.id, f"Введите свой никнейм.\nВаш текущий никнейм никнейм: {data['nickname']}\n\nПример:    /reg KirillSafe")
    except Exception as e:
        error_send_message(user_id, "/reg", e)




# Команда - /server
@bot.message_handler(commands=['stats'])
def send_user_list(message):
    user_id = str(message.from_user.id)
    try:
        usernames = get_all_usernames_from_files()
        response = f"Список пользователей ({len(usernames)}):\n\n"
        response += "\n".join(usernames)
        bot.send_message(message.chat.id, response)

    except Exception as e:
        error_send_message(user_id, "/stats", e)


# Команда - /list
@bot.message_handler(commands=['list'])
def list(message):
    bot.send_message(
        message.chat.id,
        "Список всех команд и пояснение к ним:\n/help - Тех.Поддержка\n/list - Список команд\n/start - Начальная команда\n/kabinet - Система личного кабинета с полной информацией о вашем профиле\n/username_search - поиск клана по Никнейму любого человека из него\n/description_search - поиск клана по его описанию\n/clanname_search - поиск клана по его названию\n/news - Последнии новости экскалибура\n/servers - Онлайн и последний вайп серверов\n/profile - поиск профиля человека по его Никнейму(Бета,реализовано в /username_search)\n/exchange - Получить информацию о последних ценах Клановой Биржи"
    )
    bot.send_message(message.chat.id,
                     "/click (НОВИНКА)\n/fun (НОВИНКА)\n/top (НОВИНКА)")


# Команда - /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Бот пользуется открытым Excalibur Craft Clan API и selenium:\nСтатус работы: Альфа\nСписок Бета-Команд: /list /servers'
    )


# Команда - /kabinet
@bot.message_handler(commands=['kabinet'])
def kabinet(message):
    user_id = str(message.from_user.id)
    try:
        nickname = get_user_data(user_id)['nickname']
        if nickname is None:
            bot.send_message(message.chat.id, "Вы не зарегестриованы.\nРегистрация - /reg")
            return

        sent_message = bot.send_message(message.chat.id,f"Поиск может занять до 40+ секунд. Ваш никнейм: {nickname}")

        data = get_clans_data()
        all_leaders = []
        found = False

        for clan, clan_data in data.items():
            if "leaders" in clan_data and clan_data["leaders"] is not None and len(clan_data["leaders"]) > 0:
                all_leaders.extend(clan_data["leaders"])
            # другие проверки зачисления в клан

            if nickname in all_leaders:
                found = True
                bot.send_message(message.chat.id, format_clan_info(clan, clan_data))
                info_name = get_source(nickname)
                with open('outputPROFILE.png', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption=info_name)
                # Удалить сообщение "Поиск может занять до 40+ секунд. Ваш никнейм: {nickname}"
                bot.delete_message(sent_message.chat.id, sent_message.message_id)
                break

        if not found:
            info_name = get_source(nickname)
            if info_name == 1337:
                bot.send_message(message.chat.id, "Вы не зарегестрированы на проекте Excalibur Craft")
                bot.delete_message(sent_message.chat.id, sent_message.message_id)
            else:   
                with open('outputPROFILE.png', 'rb') as photo:
                    info_name += "\nВы не состоите в клане!"
                    bot.send_photo(message.chat.id, photo, caption=info_name)
                # Удалить сообщение "Поиск может занять до 40+ секунд. Ваш никнейм: {nickname}"
                bot.delete_message(sent_message.chat.id, sent_message.message_id)
    except Exception as e:
        error_send_message(user_id, "/kabinet", e)


# Команда - /username_search
@bot.message_handler(commands=['username_search'])
def search_clan_by_user(message):
    try:
        user_id = str(message.from_user.id)
        user_message = message.text
        nickname = user_message.replace("/username_search  ", "")
        print(f"Сделан поиск клана по никнейму: {nickname}")
        data = get_clans_data()
        all_leaders = []
        found = False

        for clan, clan_data in data.items():
            if "leaders" in clan_data and clan_data[
                    "leaders"] is not None and len(clan_data["leaders"]) > 0:
                all_leaders.extend(clan_data["leaders"])
            if "trusted" in clan_data and clan_data[
                    "trusted"] is not None and len(clan_data["trusted"]) > 0:
                all_leaders.extend(clan_data["trusted"])
            if "officers" in clan_data and clan_data[
                    "officers"] is not None and len(clan_data["officers"]) > 0:
                all_leaders.extend(clan_data["officers"])
            if "members" in clan_data and clan_data[
                    "members"] is not None and len(clan_data["members"]) > 0:
                all_leaders.extend(clan_data["members"])
            if "newbies" in clan_data and clan_data[
                    "newbies"] is not None and len(clan_data["newbies"]) > 0:
                all_leaders.extend(clan_data["newbies"])

            if nickname in all_leaders:
                found = True
                bot.send_message(message.chat.id,
                                 format_clan_info(clan, clan_data))
                info_name = get_source(nickname)
                with open('outputPROFILE.png', 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption=info_name)
                os.remove("outputPROFILE.png")
                break

        if not found:
            bot.send_message(
                message.chat.id,
                'Увы, я не смог найти ваш клан\nПовторите попытку с учетом регистра\n\n/username_search'
            )
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


# Команда - /clanname_search
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
                bot.send_message(message.chat.id,
                                 format_clan_info(clan, clan_data))

        if not found:
            bot.send_message(
                message.chat.id,
                'Увы, я не смог найти ваш клан.\n\n/clanname_search')
    except Exception as e:
        error_send_message(user_id, "/search_clan_by_name", e)


# Команда - /description_search
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
                bot.send_message(message.chat.id,
                                 format_clan_info(clan, clan_data))

        if not found:
            bot.send_message(
                message.chat.id,
                'Увы, я не смог найти ваш клан\nПовторите попытку с учетом регистра\n\n/description_search'
            )
    except Exception as e:
        error_send_message(user_id, "/description_search", e)


def get_clans_data():
    response = requests.get(
        'https://excalibur-craft.ru/engine/ajax/clans/api.php')
    data = response.json()
    return data


def format_clan_info(clan, clan_data):
    members = ", ".join(
        clan_data['members']) if clan_data['members'] is not None else "Нету"
    officers = ", ".join(
        clan_data['officers']) if clan_data['officers'] is not None else "Нету"
    trusted = ", ".join(
        clan_data['trusted']) if clan_data['trusted'] is not None else "Нету"
    leaders = ", ".join(
        clan_data['leaders']) if clan_data['leaders'] is not None else "Нету"
    newbies = ", ".join(
        clan_data['newbies']) if clan_data['newbies'] is not None else "Нету"

    return (
        f"Клан: {clan}\n"
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
        f"Ссылка: https://excalibur-craft.ru/index.php?do=clans&go=profile&id={clan_data['id']}"
    )


# Команда - /servers
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
        txt.append(
            f"`{server['Server Name']}` {server['Server Version']}  Вайп: `{server['Wipe Date']}`\n"
        )
        txt.append(
            f"Игроки онлайн: {server['Players Online']}/{server['Max Players']}\n"
        )
        txt.append("\n")

    result = ''.join(map(str, txt))
    return result


# Команда - /profile
@bot.message_handler(commands=["profile"])
def search_profile(message):
    try:
        user_id = str(message.from_user.id)
        user_message = message.text
        name = user_message.replace("/profile ", "")
        if name == "/profile":
            bot.send_message(
                message.chat.id,
                "Введите имя пользователя либо зарегестрируйтесь\n/reg /profile"
            )
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


# Команда - /news
@bot.message_handler(commands=['news'])
def news(message):
    user_id = str(message.from_user.id)
    try:
        crop_screenshot()
        with open('output.png', 'rb') as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption=
                "Последнии новости экскалибура\nТак-же внутри бота началось фан-ивент. Для регистрации - /fun"
            )
        os.remove("output.png")
    except Exception as e:
        error_send_message(user_id, "/news", e)


# Команда - /exchange
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


def error_send_message(user_id, command, e):
    time = get_time_for_debuging()
    message = "Отправьте данный лог в тех.поддержку:\n"
    message += f"```python\n{e}\n```\n"
    message += f"Использовано `{command}` пользователем `{user_id}` в `{time}`"
    bot.send_message(user_id, message, parse_mode='Markdown')


if __name__ == '__main__':
    main()