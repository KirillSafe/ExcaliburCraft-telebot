import telebot, requests
from replit import db
TOKEN = db["token"] #Используете этот код на другом хостинге (ну не на repl.it) то придется переделать регистрацию и токен
#ну а если вы на repl.it то добавте свой токен в датабазу, гайды ищите в интернете друзья
bot = telebot.TeleBot(TOKEN)
db.keys() #выгружаем всех юзеров
@bot.message_handler(commands=['reg'])
def registration(message):
  nickname = message.text.split(' ', 1)
  user_id = message.from_user.id
  if str(user_id) not in db.keys():
    if len(nickname) > 1: #написал ли 
      nickname_yes = nickname[1]
      db[user_id] = nickname_yes
      bot.reply_to(message, "Вы успешно зарегестрировались\n\n/kabinet")
    else:
      bot.reply_to(message, "Укажите никнейм с учетом регистра после /reg {text}\n\nДля удаления профиля введите команду заного")
  else:
    bot.reply_to(message, "Ваш профиль удален, повторите попытку регистрации")
    del db[str(user_id)]
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Бот пользуется открытым Excalibur Craft Clan API\nКлуб на форуме: Скоро\nСтатус работы: Бета\nКоманды вводить с учетом регистра(Бот кусается)')
@bot.message_handler(commands=['kabinet'])
def kabinet_system(message):  
    user_id = str(message.from_user.id)
    if user_id not in db.keys():
        bot.send_message(message.chat.id, "Вы на данный момент не зарегистрированы в нашей системе, для регистрации введите команду /reg")
    else:
      bot.send_message(message.chat.id, "Поиск может занять до 40+ секунд. Ваш никнейм: " + db[user_id])
      data = get_clans_data()
      all_leaders = []
      found = False #if "leaders" in clan_data and clan_data["leaders"] is not None and len(clan_data["leaders"]) > 0:
      for clan, clan_data in data.items():
        if "leaders" in clan_data and clan_data["leaders"] is not None and len(clan_data["leaders"]) > 0:
            all_leaders.extend(clan_data["leaders"])  # Add leaders to the list
        if "trusted" in clan_data and clan_data["trusted"] is not None and len(clan_data["trusted"]) > 0:
            all_leaders.extend(clan_data["trusted"])
        if "officers" in clan_data and clan_data["officers"] is not None and len(clan_data["officers"]) > 0:
            all_leaders.extend(clan_data["officers"])
        if "members" in clan_data and clan_data["members"] is not None and len(clan_data["members"]) > 0:
            all_leaders.extend(clan_data["members"])
        if "newbies" in clan_data and clan_data["newbies"] is not None and len(clan_data["newbies"]) > 0:
             all_leaders.extend(clan_data["newbies"])
            #получаем всех дядя негро 
        if db[user_id] in all_leaders: #ал лидерс это алл мемберс мне лень менять
          #найден ли дядя негр
            found = True
            bot.send_message(message.chat.id, format_clan_info(clan, clan_data))
            break
      if not found:
        bot.send_message(message.chat.id, "Вы не состоите в клане либо неправильно зарегестрировались, попробуйте заново зарегестрироватся либо войдите в любой клан")
#######################################
@bot.message_handler(commands=['username_search'])
def cmd_username(message):
  #bot.send_message(message.chat.id, 'Введите имя участника клана клана:')
  mesg = bot.send_message(message.chat.id,'Введите имя человека с учетом регистра')
  bot.register_next_step_handler(mesg, search_clan_by_user)
def search_clan_by_user(message):
    bot.send_message(message.chat.id, "Поиск может занять некоротое время")
    nickname = message.text  
    print(nickname)
    data = get_clans_data()
    all_leaders = []
    found = False
    for clan, clan_data in data.items():
      if "leaders" in clan_data and clan_data["leaders"] is not None and len(clan_data["leaders"]) > 0:
          all_leaders.extend(clan_data["leaders"])  # Add leaders to the list
      if "trusted" in clan_data and clan_data["trusted"] is not None and len(clan_data["trusted"]) > 0:
          all_leaders.extend(clan_data["trusted"])
      if "officers" in clan_data and clan_data["officers"] is not None and len(clan_data["officers"]) > 0:
          all_leaders.extend(clan_data["officers"])
      if "members" in clan_data and clan_data["members"] is not None and len(clan_data["members"]) > 0:
          all_leaders.extend(clan_data["members"])
      if "newbies" in clan_data and clan_data["newbies"] is not None and len(clan_data["newbies"]) > 0:
           all_leaders.extend(clan_data["newbies"])
          #получаем всех дядя негро 
      if nickname in all_leaders: #ал лидерс это алл мемберс мне лень менять
        #найден ли дядя негр
          found = True
          bot.send_message(message.chat.id, format_clan_info(clan, clan_data))
          break
    if not found:
        bot.send_message(message.chat.id, 'Увы, я не смог найти ваш клан\nПовторите попытку с учетом регистра\n\n/username_search')
###################################
@bot.message_handler(commands=['clanname_search'])
def search_by_name(message):
    bot.send_message(message.chat.id, 'Введите название клана с учетом регистра:')
    bot.register_next_step_handler(message, search_clan_by_name)
def search_clan_by_name(message):
    name = message.text
    data = get_clans_data()
    found = False
    for clan, clan_data in data.items():
        if name.lower() == clan.lower():
            found = True
            bot.send_message(message.chat.id, format_clan_info(clan, clan_data))
    if not found:
        bot.send_message(message.chat.id, 'Увы, я не смог найти ваш клан.\n\n/clanname_search')
############################
@bot.message_handler(commands=['description_search'])
def search_by_description(message):
    bot.send_message(message.chat.id, 'Введите описание с учетом регистра:')
    bot.register_next_step_handler(message, search_clan_by_description)
def search_clan_by_description(message):
    description = message.text
    data = get_clans_data()
    found = False
    for clan, clan_data in data.items():
        if description.lower() == clan_data['motto'].lower():
            found = True
            bot.send_message(message.chat.id, format_clan_info(clan, clan_data))
    if not found:
        bot.send_message(message.chat.id, 'Увы, я не смог найти ваш клан\nПовторите попытку с учетом регистра\n\n/description_search')
##################
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
            f"Трейдеры: {trusted}\n"
            f"Офицеры: {officers}\n"
            f"Лидеры: {leaders}")

print(f"Бот стартед")

print(db.keys()) #для галочки

bot.polling()

