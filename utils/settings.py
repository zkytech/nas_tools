import os
# 服务端口
SERVER_PORT = int(os.environ.get("SERVER_PORT", "8080"))
# qbittorrent
QBITTORRENT_HOST = os.environ.get("QBITTORRENT_HOST", "127.0.0.1")
QBITTORRENT_PORT = os.environ.get("QBITTORRENT_PORT", "8888")
QBITTORRENT_USERNAME =os.environ.get("QBITTORRENT_USERNAME", "admin")
QBITTORRENT_PASSWORD=os.environ.get("QBITTORRENT_PASSWORD", "adminadmin")
# 代理
PROXY = os.environ.get("PROXY")
PUBLISH_GROUP = os.environ.get("PUBLISH_GROUP","359")
# 飞书
FEISHU_KEY = os.environ.get("FEISHU_KEY")
# mqtt
MQTT_SERVER = os.environ.get("MQTT_SERVER", "bemfa.com")
MQTT_PORT = int(os.environ.get("MQTT_PORT", "9501"))
MQTT_CLIENT_ID = os.environ.get("MQTT_CLIENT_ID","123456")
MQTT_TOPIC = os.environ.get("MQTT_TOPIC","esp32002")
# 门锁解锁密码
UNLOCK_DOOR_SECRET = os.environ.get("UNLOCK_DOOR_SECRET", "123456")
# 是否启用MQTT服务
ENABLE_MQTT = os.environ.get("ENABLE_MQTT", "false").lower() == "true"