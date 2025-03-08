## 1. searxng配置

配置文件：`dify/api/core/tools/provider/builtin/searxng/docker/settings.yml`

运行命令：

```
cd dify
docker run --name searxng-1 -d -p 8081:8080 -v "${PWD}/api/core/tools/provider/builtin/searxng/docker:/etc/searxng" --restart always searxng/searxng
```



## 2. sandbox额外配置依赖

- 进入sandbox容器

  ```
  docker exec -it docker-sandbox-1 /bin/bash
  ```

- 配置pip镜像源

  ```
  pip config set global.extra-index-url https://mirrors.aliyun.com/pypi/simple
  pip config set global.extra-index-url https://pypi.tuna.tsinghua.edu.cn/simple
  pip config set global.extra-index-url https://pypi.mirrors.ustc.edu.cn/simple/
  pip install --upgrade pip
  ```

- 在 `docker/volumes/sandbox/dependencies/python-requirements.txt` 中添加所需依赖，如：

  ```
  bs4>=0.0.2
  ```

- 修改`docker/docker-compose.yaml`文件：

  ```
    volumes:
      - ./volumes/sandbox/dependencies:/dependencies
      - ./volumes/sandbox/conf:/conf	# 新增
  ```

- 在sandbox容器内部下载所需要的包

  ```
  pip install ...
  ```

- 重启容器

  ```
  docker compose restart sandbox
  ```

- 如果显示`Run failed: error: operation not permitted`

  查看：

  https://www.bilibili.com/video/BV1EtBTYHE1y/

  https://github.com/brightwang/dify-sandbox-use-check-permissions

  注意在容器内 `/dependencies/code` 目录下，运行 `bash test.sh` 命令之前，先运行 `sed -i 's/\r$//' test.sh`，来删除所有 `\r` 字符

