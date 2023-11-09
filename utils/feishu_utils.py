
from utils import settings
import json,requests

# SDK 使用说明: https://github.com/larksuite/oapi-sdk-python#readme
# 复制该 Demo 后, 需要将 "APP_ID", "APP_SECRET" 替换为自己应用的 APP_ID, APP_SECRET.
def sendFeishuMsg(content):
    # 创建client
    requests.post("https://open.feishu.cn/open-apis/bot/v2/hook/{}".format(settings.FEISHU_KEY),
        json = {
            "msg_type": "text", "content": { "text": content }
        }
    )

