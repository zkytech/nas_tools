import os

QBITTORRENT_HOST = os.environ.get("QBITTORRENT_HOST", "127.0.0.1")
QBITTORRENT_PORT = os.environ.get("QBITTORRENT_PORT", "8888")
QBITTORRENT_USERNAME =os.environ.get("QBITTORRENT_USERNAME", "admin")
QBITTORRENT_PASSWORD=os.environ.get("QBITTORRENT_PASSWORD", "adminadmin")
PROXY = os.environ.get("PROXY")
PUBLISH_GROUP = os.environ.get("PUBLISH_GROUP","359")
FEISHU_KEY = os.environ.get("FEISHU_KEY")