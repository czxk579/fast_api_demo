FROM python:3.12-slim

WORKDIR /app/

# 安装依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . /app/

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 命令由docker-compose.yml控制
# CMD ["python", "main.py"]
