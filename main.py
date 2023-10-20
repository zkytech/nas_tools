from flask import Flask,request,make_response
import requests,re
from lxml import etree
from utils.xml_utils import create_xml,xml_to_str
from utils.mikan import add_feeds_from_mikan_project
from flask_crontab import Crontab
import requests


def fill_zero(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)




headers = {
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
app = Flask(__name__)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)