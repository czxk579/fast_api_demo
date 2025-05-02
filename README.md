# FastAPI Demo 项目

这是一个使用 FastAPI 框架开发的示例项目，展示如何构建一个功能完整的后端 API 服务。

## 功能特点

- 用户认证与授权
- RESTful API 设计
- 数据库集成 (PostgreSQL via SQLAlchemy ORM)
- 缓存支持 (Redis)
- 任务队列 (Celery)
- 接口文档自动生成 (Swagger UI, ReDoc)
- 单元测试与集成测试
- 异步支持
- 中间件集成
- 日志系统

## 项目结构

```
├── app/                  # 应用代码
│   ├── api/              # API 路由
│   ├── core/             # 核心配置
│   ├── db/               # 数据库模型和会话
│   ├── models/           # SQLAlchemy 模型
│   ├── schemas/          # Pydantic 模型
│   ├── services/         # 业务逻辑
│   └── utils/            # 工具函数
├── migrations/           # 数据库迁移文件
├── tests/                # 测试代码
├── .env                  # 环境变量
├── .env.example          # 环境变量示例
├── alembic.ini           # Alembic 配置
├── main.py               # 应用入口
└── requirements.txt      # 项目依赖
```

## 快速开始

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 配置环境变量:
```bash
cp .env.example .env
# 编辑 .env 文件设置你的环境变量
```

3. 运行开发服务器:
```bash
python main.py
```

4. 访问API文档:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 数据库迁移

```bash
# 初始化迁移
alembic init migrations

# 创建迁移
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head
```

## 单元测试
```
- 运行所有：pytest
  - 运行指定模块：
    pytest -vs ./tests/test_main.py
    pytest -vs ./tests/test_users.py
    pytest -vs ./tests/test_api_auth.py -v
    pytest -vs ./tests/test_users.py -v -p no:warnings
  - 运行指定目录：pytest -vs ./tests
  - 通过nodeID运行指定的测试函数：
    pytest -vs ./tests/test_main.py::test_register_user
    pytest -vs ./tests/test_main.py::TestLogin::test_04_func
```

## 部署

项目可以通过 Docker 或直接部署到服务器:

### Docker 部署
```bash
docker-compose up -d
```

### 直接部署
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
``` 

### 访问 API 文档：
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

### 项目生成描述
帮我推荐一款 python 后端框架，我想通过该框架来开发自己的后端接口服务。
该框架应具备以下特点：
1. 简单易上手：框架的学习曲线应该低，初学者可以快速上手，并快速熟悉框架的使用方法。
2. 高性能：框架应具有高性能，能够支撑大并发、高吞吐量的业务场景。
3. 支持异步：框架应支持异步编程，能够有效提升框架的并发能力。
4. 支持接口文档生成：框架应提供接口文档生成工具，能够自动生成接口文档，并提供在线浏览接口文档的能力。
5. 集成常用中间件：框架应集成常用中间件，如 mysql、redis、mongo、rabbitmq、kafka、celery、sentry、opentracing等，能够提升开发效率。
6. 集成 ORM：框架应集成 ORM，能够方便地操作数据库，并提供数据库连接池管理能力。
7. 集成消息队列：框架应集成消息队列，能够方便地进行消息的发布、订阅、消费，并提供消息队列管理能力。
8. 集成日志系统：框架应集成日志系统，能够方便地进行日志的记录、查询，并提供日志管理能力。
9. 集成代码自动部署：框架应提供代码自动部署能力，能够自动部署代码到服务器，并提供代码部署管理能力。
10. 集成单元测试：框架应提供单元测试能力，能够自动化测试代码，并提供单元测试管理能力。
11. 该框架生态完善，社区活跃，文档齐全，易于扩展。
12. 使用该框架帮我生成一个 demo 项目，并提供项目部署到服务器的能力，我可以快速上手该框架，并快速开发自己的后端接口服务。
