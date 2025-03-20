searxng安装命令
```
cd dify
docker run --name searxng-1 -d -p 8081:8080 -v "${PWD}/api/core/tools/provider/builtin/searxng/docker:/etc/searxng" searxng/searxng
```
