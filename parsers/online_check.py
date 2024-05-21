def parse_online_players():
    import requests
    from bs4 import BeautifulSoup
    
    page = requests.get("https://excalibur-craft.ru")
    soup = BeautifulSoup(page.content, 'html.parser')
    players_count = soup.find('div', class_='players').find('span').text
    max_players_count = soup.find('div', class_='players').find_all('span')[1].text
    
    return f"В онлайне {players_count} человека"

def parse_online_servers():
    import requests
    from bs4 import BeautifulSoup
    
    result = requests.get('https://excalibur-craft.ru/')
    soup = BeautifulSoup(result.text, 'html.parser')
    
    complexes = soup.find_all('div', class_='complex')

    server_info = ""

    for complex in complexes:
        server_name_elem = complex.find('a')
        server_name = server_name_elem.text.strip() if server_name_elem else "Unknown"
        if server_name != "Unknown":
            online_info = complex.find('div', class_='online-number')
            if online_info:
                online_now = online_info.find('span').text
                online_max = online_info.find_all('span')[1].text
                server_info += f"{server_name} {online_now} / {online_max}\n"

    return server_info

def parse_top_players():
    import requests
    from bs4 import BeautifulSoup
    
    url = 'https://excalibur-craft.ru'  # замените на конкретную ссылку на страницу с топами
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        top_players = soup.select(".row .player")[:3]  # выбираем первые три элемента
        result = "Топ-3 игроков:\n"
        
        for idx, player in enumerate(top_players, 1):
            nickname = player.a.get_text(strip=True)
            time = player.find_next_sibling("div").span.get_text(strip=True)
            result += f"{idx}. {nickname} - {time} часов.\n"
        
        return result
    else:
        return 'Не удалось получить данные с веб-сайта'