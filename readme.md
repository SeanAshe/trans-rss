# 说明

订阅、管理番剧，并在下载新番时，通过webhook（例如飞书）推送到手机和电脑，提醒赶快看番。

# 使用docker运行

```yaml
version: '3.9'
services:
  trans-rss:
    image: sssean/trans-rss
    volumes:
      - './config:/app/configs'
    ports:
       - '10018:80'
    restart: unless-stopped
    network_mode: bridge
```