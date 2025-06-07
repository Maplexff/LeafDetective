# 使用官方 MySQL 8.0 镜像作为基础镜像
FROM mysql:8.0

# 设置环境变量
ENV MYSQL_ROOT_PASSWORD=leafdetective
ENV MYSQL_DATABASE=leafdetective
ENV MYSQL_USER=leafdetective
ENV MYSQL_PASSWORD=leafdetective

# 复制初始化脚本到容器内（可选）
COPY ./leafdetective.sql /docker-entrypoint-initdb.d/

# 暴露 MySQL 端口
EXPOSE 3306