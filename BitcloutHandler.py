import webbrowser
import datetime as dt
import requests
from bs4 import BeautifulSoup
import csv

if __name__ == '__main__':

    users = []
    columns = ["UserName", "Reward", "Price", "Locked", "Created", "DateTime"]

    while True:

        print(dt.datetime.now().replace(microsecond=0))

        response = requests.get('https://api.cloutgate.com/users?sort=created&order=-1&verified=&reserved=&created=1')
        data = response.json()
        # file = 'D:\\Bitclout.csv'

        for user in data:
            unique = True
            userName = user.get('username')

            if userName in users:
                continue
            else:
                users.append(userName)
                reward = user.get('reward')
                price = user.get('price')
                locked = user.get('locked')
                created = user.get('created')
                dateTime = dt.datetime.now().replace(second=0, microsecond=0)
                userData = {"UserName": userName, "Reward": reward, "Price": price, "Locked": locked,
                            "Created": created, "DateTime": dateTime}
                try:
                    query = userName + '+instagram'
                    url = 'http://www.google.com/search?q='
                    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 '
                    #                          '(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
                    page = requests.get(url + query)
                    soup = BeautifulSoup(page.text)
                    next_page = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")
                    if next_page is not None:
                        try:
                            next_pageText = next_page.div.text
                            indexFollowers = next_pageText.find("Followers")
                            followers = next_pageText[0:indexFollowers - 1]
                            lastChar = followers[-1]
                            loginNameIndex = next_pageText.find("@")
                            loginName = next_pageText[loginNameIndex + 1:next_pageText.find(")")]

                            if loginName.lower() == userName.lower():
                                if lastChar == "m" or lastChar == "k" or int(followers) > 4000:
                                    with open(file, 'a') as csvFile:
                                        writer = csv.DictWriter(csvFile, fieldnames=columns)
                                        writer.writerow(userData)
                                    webbrowser.open_new('https://www.instagram.com/' + userName)
                                    webbrowser.open_new('https://bitclout.com/u/' + userName + '?tab=creator-coin')
                        except Exception:
                            # with open(file, 'a') as csvFile:
                            #     writer = csv.DictWriter(csvFile, fieldnames=columns)
                            #     writer.writerow(userData)
                            webbrowser.open_new('https://www.instagram.com/' + userName)
                            webbrowser.open_new('https://bitclout.com/u/' + userName + '?tab=creator-coin')
                except Exception:
                    webbrowser.open_new('https://www.instagram.com/' + userName)
                    webbrowser.open_new('https://bitclout.com/u/' + userName + '?tab=creator-coin')
