import requests
from bs4 import BeautifulSoup
import re
import smtplib
from email.mime.text import MIMEText
import settings

EML = settings.EML
PWD = settings.PWD


def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr 
    msg['To'] = to_addr
    return msg

def send_mail(from_addr, to_addr, body_msg):
    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(EML, PWD)
    smtpobj.sendmail(from_addr, to_addr, create_message(from_addr, to_addr, subject, body).as_string())
    smtpobj.close()


url = "https://auctions.yahoo.co.jp/search/search?auccat=2084061400&tab_ex=commerce&ei=utf-8&aq=1&oq=%E3%83%98%E3%83%A9%E3%82%AF%E3%83%AC%E3%82%B9&exflg=1&p=%E3%83%98%E3%83%A9%E3%82%AF%E3%83%AC%E3%82%B9&x=0&y=0&fixed=0&sc_i=auc_sug_cat"
ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
headers = {'User-Agent': ua}

#出品と商品リンクの取得
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.content,'html.parser')
text = soup.find('h1',class_='Info__keyword').text


#メールの内容
from_addr = 'auction'
to_addr = EML
subject = '新しくヘラクレスが出品されました'
body = url


old_nums = []
new_num = re.search(r"\d+",text).group()

#\dは半角数字。group()でマッチオブジェクトのmatchの値をnewNumに代入。
#出品数(num)が前回アクセス時よりも増えたらメールを送る
if len(old_nums) == 0:
    create_message(from_addr, to_addr, subject,body)
    send_mail(from_addr, to_addr, body)
    old_nums.append(new_num)
elif old_nums[-1] < new_num:
    create_message(from_addr, to_addr, subject,body)
    send_mail(from_addr, to_addr, body)
    old_nums.append(new_num)
    old_nums.pop(0)
else:
    old_nums.append(new_num)
    old_nums.pop(0)


    



# 参考
# 分かりやすいpythonの正規表現の例 https://qiita.com/luohao0404/items/7135b2b96f9b0b196bf3
#【requestsモジュール】pythonの文字化けを対策するhttps://tomowarkar.com/python-mozibake/”
#smtplib.SMTPAuthenticationError が出るのでGMAILでIMAPを有効化