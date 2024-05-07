from flask import Flask,request,make_response,current_app
from flask_mqtt import Mqtt
import requests,re
from lxml import etree
from utils.xml_utils import create_xml,xml_to_str
from utils.mikan import add_feeds_from_mikan_project
from flask_crontab import Crontab
import requests
from utils import settings
from utils.req_utils import make_response
import urllib.parse 
from utils.feishu_utils import sendFeishuMsg

UNLOCK_DOOR_SECRET = settings.UNLOCK_DOOR_SECRET
def fill_zero(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)



headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
app = Flask(__name__)
# 代理地址
app.config['MQTT_BROKER_URL'] = settings.MQTT_SERVER
# 端口
app.config['MQTT_BROKER_PORT'] = settings.MQTT_PORT
app.config['MQTT_CLIENT_ID'] = settings.MQTT_CLIENT_ID
# 设置心跳时间，单位为秒
app.config['MQTT_KEEPALIVE'] = 60
# # 如果服务器支持 TLS，则设置为 True
# app.config['MQTT_TLS_ENABLED'] = False



crontab = Crontab(app)
@crontab.job(minute="0", hour="*")
def my_scheduled_job():
    add_feeds_from_mikan_project()



# 6v电影网  https://www.6vw.cc
@app.route("/6vw")
def hello_world():
    url = request.args.get("url")
    keyword = request.args.get("keyword")
    req = requests.get(url,headers=headers)
    resource_list = []
    body = req.content.decode("gb2312")
    for tr in etree.HTML(body).xpath('//div[@id="text"]/table//tr'):
        resourceUrl = tr.xpath("td[1]/a/@href")[0]
        name = tr.xpath("td[1]/a/text()")[0]
        if name.startswith("http"):
            continue
        if keyword and keyword != "":
            if keyword not in name:
                continue
        resource_list.append({"name":name,"url":resourceUrl})
    title_origin = etree.HTML(body).xpath('//head/title/text()')[0]
    title = re.match(r".*《(.*)》.*",title_origin).group(1)
    xml = create_xml(resource_list,title,request.url)
    
    resp = make_response(xml_to_str(xml))
    resp.headers['Content-Type'] = 'application/xml'
    return resp

@app.route("/rss/add_mikan")
def add_mikan_project():
    print("addmikan")
    add_feeds_from_mikan_project()
    return "done"

@app.route("/sub")
def get_sub():
    url = request.args.get("url")
    url = urllib.parse.unquote(urllib.parse.unquote(url))
    return make_response(requests.get(url, proxies={
        "http":settings.HTTP_PROXY,
        "https":settings.HTTPS_PROXY
    }))

@app.route("/feishu/push")
def feishu_push():
    text = request.args.get("text")
    text = urllib.parse.unquote(text)
    sendFeishuMsg(text)
    return "success"


if settings.ENABLE_MQTT:
    mqtt = Mqtt(app)
    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):

        topic=message.topic[0],
        payload=message.payload.decode()
        # socketio.emit('mqtt_message', data=data)
        print(topic,payload)
        # 开锁
        if topic == settings.MQTT_TOPIC and payload == "on":
            print("on")
            requests.get(f"http://127.0.0.1:{settings.SERVER_PORT}/{UNLOCK_DOOR_SECRET}")
        # 闭锁
        if topic == settings.MQTT_TOPIC and payload == "off":
            print("off")


    @mqtt.on_log()
    def handle_logging(client, userdata, level, buf):
        print(level, buf)
        
    mqtt.subscribe(settings.MQTT_TOPIC)

# 注册锁的ip
@app.route("/register_lock_ip")
def register_lock_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if "ip" in request.args:
        client_ip = request.args.get("ip")
    elif x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request.remote_addr
    current_app.doorlock_helper_ip = client_ip
    return f"Client IP: {client_ip}"

# 执行解锁命令，为尽可能降低风险，这里使用UNLOCK_DOOR_SECRET作为URI
@app.route(f"/{UNLOCK_DOOR_SECRET}")
def unlock_door():
    print(f"正在请求http://{current_app.doorlock_helper_ip}/on")
    requests.get(f"http://{current_app.doorlock_helper_ip}/on")
    return "命令已转发"

if __name__ == "__main__":
    
    app.run(host="0.0.0.0",port=settings.SERVER_PORT,debug=True,use_reloader=False)