# =====================================
# DSML Chatbot 2017
# Author(Minchul,Taekyung)
# Maintain(Minchul, wow@suwon.ac.kr)
#======================================
from flask import Flask, request, jsonify
import requests,json
from answer import *
import html.parser
from auth import *

main_msg={"type":"text"}
app = Flask(__name__)
# ----- INTERFACE ------
def getAnswer(question):
    url = 'https://westus.api.cognitive.microsoft.com/qnamaker/v2.0/knowledgebases/'+api+'/generateAnswer'
    headers = {'Content-Type':'application/json; charset=utf-8',
                'Ocp-Apim-Subscription-Key':key}
    data = json.dumps({"question": question})
    r = requests.post(url, headers=headers, data=data)
    rjson = json.loads(r.text)
    answer = rjson.get('answers')[0]['answer']
    answer = html.parser.HTMLParser().unescape(answer)
    return answer
# ----- MAIN PAGE -----
@app.route('/')
def hello_world():
    return 'Hello World!'
# ----- SINEAGE ------
@app.route('/keyboard')
def Keyboard():
    return jsonify(main_msg)
# ----- MSG PASSED BY AZURE -----
@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']
    user_msg=getAnswer(content)
    print(user_msg)
    if user_msg=="No good match found in the KB":
        user_msg="뭐라 대답해야 할 지 모르겠어요. ㅜ.ㅜ"
    dataSend = {"message":{"text":user_msg}}
    return jsonify(dataSend)
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
