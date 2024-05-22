def parse_online_players():
    import requests
    from bs4 import BeautifulSoup
    
    page = requests.get("https://excalibur-craft.ru")
    soup = BeautifulSoup(page.content, 'html.parser')
    players_count = soup.find('div', class_='players').find('span').text
    max_players_count = soup.find('div', class_='players').find_all('span')[1].text
    
    return f"В онлайне {players_count} человека"

import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

def parse_online_servers():
    url = "https://excalibur-craft.ru/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    server_blocks = soup.find_all("a", class_="server-link")
    
    server_info = []
    
    for server_block in server_blocks:
        server_name = server_block.find("p").text.strip()
        wipe_date = server_block.find(class_="server-last-wipe").text.strip()
        online_numbers = server_block.find(class_="online-number").find_all("span")
        players_online = online_numbers[0].text.strip()
        max_players = online_numbers[1].text.strip()
        server_version = server_block.find(class_="server-version").text.strip()
        
        server_info.append({
            "Server Name": server_name,
            "Wipe Date": wipe_date,
            "Players Online": players_online,
            "Max Players": max_players,
            "Server Version": server_version
        })
    
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