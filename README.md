
##### 前端

```bash

# 安装依赖
npm install 或 yarn --registry=https://registry.npmmirror.com

# 建议不要直接使用 cnpm 安装依赖，会有各种诡异的 bug。可以通过如下操作解决 npm 下载速度慢的问题
npm install --registry=https://registry.npmmirror.com

# 启动服务
npm run dev 或 yarn dev
```

##### 后端

```bash

# 安装依赖环境, 建议使用aconda， python版本推荐3.11
pip3 install -r requirements.txt

# 配置环境
在.env.dev（开发环境）文件中配置开发环境的数据库和redis，


# 运行sql文件
1.使用命令或数据库连接工具运行sql文件夹下的leafdetective，或使用SQL的Docker

# 运行后端
python3 app.py --env=dev

```

##### 访问

```bash
# 默认账号密码
账号：admin
密码：admin123

# 浏览器访问
地址：http://localhost:80
```

#### Docker打包

##### 前端

```bash
# 构建测试环境
npm run build:stage 或 yarn build:stage

# 构建生产环境
npm run build:prod 或 yarn build:prod

docker build -t fastvue:latest 。
```

##### 后端

```bash
# 配置环境
在.env.prod文件中配置生产环境的数据库和redis

docker build -t fastapiback:latest .

```

##### SQL

```bash

docker build -t fastsql:latest .

```

##### 运行docker-compose

```bash

docker compose up -d

```

##### 可使用docker镜像

```bash
# FastAPI backend
https://hub.docker.com/repository/docker/maplexx/fastapiback/general
# FastVue
https://hub.docker.com/repository/docker/maplexx/fastvue/general
# FastSQL
https://hub.docker.com/repository/docker/maplexx/fastsql/general


```