import requests
from lxml import etree
import pandas as pd
import datetime

sep = "(-------------------------------------------------------------)"
ses = requests.session()

CONheaders = {
    "Host": 'massarservice.men.gov.ma',
    "Content-Length": '156',
    "Cache-Control": 'max-age=0',
    "Sec-Ch-Ua": '" Not A;Brand";v="99", "Chromium";v="96"',
    "Sec-Ch-Ua-Mobile": '?0',
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Upgrade-Insecure-Requests": '1',
    "Origin": 'https://massarservice.men.gov.ma',
    "Content-Type": 'application/x-www-form-urlencoded',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "Sec-Fetch-Site": 'same-origin',
    "Sec-Fetch-Mode": 'navigate',
    "Sec-Fetch-User": '?',
    "Sec-Fetch-Dest": 'document',
    "Referer": 'https://massarservice.men.gov.ma/moutamadris/Account',
    "Accept-Encoding": 'gzip, deflate',
    "Accept-Language": 'en-US,en;q=0.9',
    "Connection": 'close'
}

with open(r'creds.txt', 'r') as file:
    lines = file.readlines()

uid = lines[0].strip().split('=')[1]
Pass = lines[1].strip().split('=')[1]

tokenRequest = ses.get('https://massarservice.men.gov.ma/moutamadris/Account')
domain = 'https://massarservice.men.gov.ma/moutamadris/Account'
parser = etree.HTMLParser()
csrf = etree.fromstring(tokenRequest.text, parser)
csrftoken = csrf.xpath('//form/input[@name="__RequestVerificationToken"]/@value')[0]

Creds = {'UserName': uid, 'Password': Pass, '__RequestVerificationToken': csrftoken}

r1 = ses.post(b'https://massarservice.men.gov.ma/moutamadris/Account', headers=CONheaders, data=Creds)

if 'ChangePassword' in r1.text:
    print('Connected')
else:
    print('Error, maybe Username or password is invalid')
    exit()

sess_choice = input("Choose session (01 for Première semestre, 02 for Deuxième semestre): ")
session_mapping = {
    "01": "1",
    "02": "2",
    "03": "3"
}
today = datetime.date.today()

year = today.year


# Gets the current school year
current_year = year
def get_school_year(current_year, start_month=8, end_month=6):
    if current_year < start_month:
        return current_year - 1, current_year
    else:
        return current_year, current_year + 1


start_year, end_year = get_school_year(current_year)



sess = session_mapping.get(sess_choice)
if not sess:
    print("Invalid session choice")
    exit()

selected_year = input("Select the desired year (leave blank if it the current year): ")

if selected_year == '':
    selected_year = start_year

Creds2 = {"Annee": selected_year, "IdSession": sess}

CONheaders2 = {
    "Sec-Ch-Ua": '" Not A;Brand";v="99", "Chromium";v="96"',
    "Accept": '*/*',
    "Content-Type": 'application/x-www-form-urlencoded; charset=UTF-8',
    "X-Requested-With": 'XMLHttpRequest',
    "Sec-Ch-Ua-Mobile": '?0',
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Origin": 'https://massarservice.men.gov.ma',
    "Sec-Fetch-Site": 'same-origin',
    "Sec-Fetch-Mode": 'cors',
    "Sec-Fetch-Dest": 'empty',
    "Referer": 'https://massarservice.men.gov.ma/moutamadris/TuteurEleves/GetNotesEleve',
    "Accept-Encoding": 'gzip, deflate',
    "Accept-Language": 'en-US,en;q=0.9',
    "Connection": 'close'
}

fr = ses.post(b'https://massarservice.men.gov.ma/moutamadris/General/SetCulture?culture=en', headers=CONheaders2)

r2 = ses.post(
    b'https://massarservice.men.gov.ma/moutamadris/TuteurEleves/GetBulletins',
    headers=CONheaders2,
    data=Creds2,
    cookies=ses.cookies
)


if 'Classe' in r2.text:
    print('Connected')
else:
    print('Error')
    exit()

notes = pd.read_html(r2.text, decimal=',', thousands='.')
tb0 = notes[0]
tb1 = notes[1]

print('Grades')
print(tb0)
print(sep)
print('Global Grades')
print(tb1)
print(sep)

f = etree.fromstring(r2.text, parser)
print(''.join(f.xpath('//*[@id="tab_notes_exam"]/div[2]//text()')))


tb1,tb0.to_csv('grades.csv', index=False)

print('Grades saved to "grades.cvs"')

