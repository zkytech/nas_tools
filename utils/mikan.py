from flask import Flask,request,make_response
import requests,re
from lxml import etree
from utils.xml_utils import create_xml,xml_to_str
# from utils.mikan import add_feeds_from_mikan_project
import hashlib
from datetime import datetime
from flask_crontab import Crontab
import requests
import feedparser
import urllib.parse
import qbittorrentapi
from utils import settings
import json



def add_feeds_from_mikan_project():

    # instantiate a Client using the appropriate WebUI configuration
    conn_info = dict(
        host=settings.QBITTORRENT_HOST,
        port=settings.QBITTORRENT_PORT,
        username=settings.QBITTORRENT_USERNAME,
        password=settings.QBITTORRENT_PASSWORD
    )
    print("login mikan :" + json.dumps(conn_info))
    qbt_client = qbittorrentapi.Client(**conn_info)
    # the Client will automatically acquire/maintain a logged-in state
    # in line with any request. therefore, this is not strictly necessary;
    # however, you may want to test the provided login credentials.
    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)

    publish_group = settings.PUBLISH_GROUP
    resp = requests.get("https://mikanani.me/Home/PublishGroup/{}".format(publish_group),proxies={
        "http": settings.PROXY,
        "https": settings.PROXY
    })
    print(resp)
    for timeline in etree.HTML(resp.text).xpath('//div[contains(@class,"js-sort-item pubgroup-timeline-item")]'):
        print(timeline)
        # 番剧上映年月，例如：2023.10
        pub_month_year = timeline.xpath('div[contains(@class,"pubgroup-date")]/text()')[0]
        pub_month = pub_month_year.split(".")[1]
        pub_year = pub_month_year.split(".")[0]
        month_year_str = "{}年{}月".format(pub_year,pub_month)
        if not "动漫" in qbt_client.rss_items():
            qbt_client.rss_add_folder("动漫")
        if not month_year_str in qbt_client.rss_items()["动漫"]:
            qbt_client.rss_add_folder("动漫\{}".format(month_year_str))
        for bangumi_li in timeline.xpath('div/div/div/ul[contains(@class,"list-inline pubgroup-ul")]/li'):
            bangumi_id = bangumi_li.attrib["data-bangumiid"]
            subgroup_id = bangumi_li.attrib["data-subtitlegroupid"]
            bangumi_name = bangumi_li.xpath('div/div/a/text()')[0]
            print("正在处理:【{}】".format(bangumi_name))
            try:
                rss_url = "https://mikanani.me/RSS/Bangumi?bangumiId={}&subgroupid={}".format(bangumi_id, subgroup_id)

                if  bangumi_name in qbt_client.rss_items()["动漫"][month_year_str].keys():
                    print("【{}】已存在，跳过".format(bangumi_name))
                    continue
                qbt_client.rss_add_feed(url =rss_url,item_path = "动漫\{}\{}".format(month_year_str, bangumi_name))
                qbt_client.rss_set_rule(rule_name = "动漫-{}-{}".format(month_year_str, bangumi_name),rule_def={
                            "enabled": True,
                            "mustContain": "",
                            "mustNotContain": "",
                            "useRegex": False,
                            "episodeFilter": "",
                            "smartFilter": False,
                            "previouslyMatchedEpisodes": [
                            ],
                            "affectedFeeds": [
                                rss_url
                            ],
                            "ignoreDays": 0,
                            "savePath": "/downloads/media/动漫/{}/{}".format(month_year_str,bangumi_name)
                        }
                )
            except Exception as e:
                print(e)
