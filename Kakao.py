#############################################
#   상모고등학교 알림봇 스킬에 사용되는 파일임
############################################
from flask import Flask, jsonify, request
import requests #웹 크롤링에 사용(requests.get등 사용)
from bs4 import BeautifulSoup #웹 크롤링에 사용하는 모듈
from datetime import datetime #yy mm dd 사용

app = Flask(__name__)

yy = datetime.today().year
mm = datetime.today().month
dd = datetime.today().day

source_L = requests.get(f"http://school.gyo6.net/sangmohs/food/{yy}/{mm}/{dd}/dinner").text
soup_L = BeautifulSoup(source_L, "html.parser")
hotKeys_L = soup_L.select('div')[1].text
if hotKeys_L == "\n":
    hotKeys_L = "구성된 식단이 없음!"

source_D = requests.get(f"http://school.gyo6.net/sangmohs/food/{yy}/{mm}/{dd}/dinner").text
soup_D = BeautifulSoup(source_D, "html.parser")
hotKeys_D = soup_D.select('div')[1].text
if hotKeys_D == "\n":
    hotKeys_D = "구성된 식단이 없음!"




@app.route('/keyboard') #Get방식으로 접속하여 서버가 잘 동작하는지 확인
def Keyboard():
    return hotKeys_D

@app.route('/message', methods=['POST']) #POST 방식으로 접속하는 메인 라우터
def Message():
    yy = datetime.today().year ## year / month / day 받아오는 함수들 
    mm = datetime.today().month
    dd = datetime.today().day

    source_L = requests.get(f"http://school.gyo6.net/sangmohs/food/{yy}/{mm}/{dd}/lunch").text
    #requests datetime모듈을 이용해 파싱할 웹 페이지를 .text(문자열)형식으로 저장.
    soup_L = BeautifulSoup(source_L, "html.parser")
    #source에서 html소스로 파싱해야한다고 옵션을 정하고 soup_L에 대입.
    hotKeys_L = soup_L.select('div')[1].text
    #html을 파싱한 soup변수 내부에서 div메타클래스를 가지고 있는 문자열중 [1]번째극 select해서 가져온 뒤 .text형식으로 저장.
    if hotKeys_L == "\n":
        hotKeys_L = "구성된 식단이 없음!"
        #식단이 없을경우 \n으로 표시되기에 식단이 없다는걸 알려주기 위해 hotkey_L을 수정해줌.

    source_D = requests.get(f"http://school.gyo6.net/sangmohs/food/{yy}/{mm}/{dd}/dinner").text
    soup_D = BeautifulSoup(source_D, "html.parser")
    hotKeys_D = soup_D.select('div')[1].text
    if hotKeys_D == "\n":
        hotKeys_D = "구성된 식단이 없음!"

    content = request.get_json()
    content = content['userRequest']
    content = content['utterance']

    dataSend = {
        "version": "2.0",
        "data": {
            "lunch_menu":hotKeys_L,
            "dinner_menu":hotKeys_D,
            "dd" : dd,
            "mm" : mm,
            "yy" : yy
  }
    }
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8889)