# 使用 Python 3.12 作为基础镜像
FROM python:3.12
# 设置工作目录
RUN mkdir /app
WORKDIR /app
# 复制项目文件到工作目录
COPY . /app
# 设置清华 pip 镜像
ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
ENV PIP_TRUSTED_HOST=pypi.tuna.tsinghua.edu.cn
# 安装项目依赖
RUN pip install -r requirements.txt
# 设置环境变量
ENV PYTHONUNBUFFERED=1
EXPOSE 8000
# 启动 Django 服务器
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]