FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install  -r requirements.txt

# COPY . .
# WORKDIR /MyFastApi
# COPY ./build/python/requirements.txt ./

RUN echo "umask 0022" >> /etc/profile

RUN pip install  -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/; \
sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources ; apt update; \
echo complete;

# COPY requirements.txt ./MyFastApi/requirements.txt

# RUN pip install  --upgrade -r requirements.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6

COPY . .
# apt update;    
# echo complete;
# COPY ./flux-backend ./MyFastApiBackend
RUN chmod -R 777 /app/flux_admin
RUN chmod -R 777 /app/record_img
RUN chmod -R 777 /app
EXPOSE 9099
# CMD ["uvicorn", "fastapimain:app", "--host", "0.0.0.0", "--port", "9099"]
CMD ["python", "app.py", "--env=prod-templates"]






# FROM python:3.10
# WORKDIR /app
# # 拷贝环境配置
# COPY requirements.txt .  
# # 安装环境配置                          
# RUN pip install -r requirements.txt               
# # 安装OpenGL库
# RUN apt-get update && apt-get install -y \       
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     libsm6 \
#     libxrender1 \
#     libxext6
# # 拷贝所有执行文件    
# COPY . .         
# # 文件访问授权                                    
# RUN chmod -R 777 /app          
# # 端口暴露
# EXPOSE 9099                                          
# # 配置并启动
# CMD ["python", "app.py", "--env=prod-templates"] 

