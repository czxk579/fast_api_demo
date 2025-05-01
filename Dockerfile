FROM python:3.9-slim

WORKDIR /app/

# 安装依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . /app/

# 运行服务器
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 
