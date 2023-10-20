# rss_service

## 功能

- 蜜柑计划RSS自动添加：自动添加蜜柑计划指定发布组的所有内容rss订阅到QBittorrent中，并自动更新
- 6V电影网页面转RSS：将6v电影网  https://www.6vw.cc 的指定页面转换成rss订阅

## 配置项

DOCKER 环境变量说明：
- `QBITTORRENT_HOST`: QBittorrent 服务地址, 例如: `192.168.1.1`
- `QBITTORRENT_PORT`: QBittorrent 服务端口, 例如: `8888`
- `QBITTORRENT_USERNAME`: QBittorrent 用户名, 例如: `admin`
- `QBITTORRENT_PASSWORD`: QBittorrent 密码, 例如: `adminadmin`
- `HTTPS_PROXY`: HTTPS代理地址，例如:`http://192.168.1.3:7890`
- `HTTP_PROXY`: HTTP代理地址，例如:`http://192.168.1.3:7890`
- `PUBLISH_GROUP`: 蜜柑发布组ID，点击发布组名称，从URL中获取，例如:`https://mikanani.me/Home/PublishGroup/359`，url路径最后一段就是发布组ID

## API
- `/rss/add_mikan`: 手动触发蜜柑计划rss订阅添加任务
- `/6vw`: 将6v电影网  https://www.6vw.cc 的指定页面转换成rss订阅，支持以下url query参数
    - `url`: 需要转换成rss订阅的页面地址
    - `keyword`: 用于匹配资源的关键词


