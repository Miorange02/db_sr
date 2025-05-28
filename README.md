# 项目名称

崩铁数据库系统

## 项目简介

本项目是一个基于Python `Flask` 框架，前端使用CDN引入`vue`,`axios`,`bootstrap`的数据库管理系统，主要功能包括：
- 数据库的创建与初始化

- 数据表的增删改查操作

- 数据的可视化管理

  角色只有一个装备记录，光锥可以有多个装备记录

## 项目结构

```
project/
├── app.py
├── config.py
├── create_table.sql
├── DP更新立绘.py
├── extension.py
├── initialize.py
├── initialize.sql
├── models.py
├── README.md
├── requirements.txt
├── blueprints/
│   ├── __init__.py
│   ├── character.py
│   ├── equipment.py
│   ├── weapon.py
├── static/
│   ├── css/
│   ├── js/
│   ├── illustration/
│   ├── img/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── character.html
│   ├── weapons.html
│   ├── add_character.html
│   ├── add_weapon.html
└── __pycache__/
```

## 环境依赖

- Python 3.10+
- Flask
- Flask-SQLAlchemy
- DrissonPage

## 安装与运行

1. 克隆项目到本地：
   ```bash
   git clone <项目地址>
   cd <项目目录>
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 连接数据库：
   修改 `config.py` 中的数据库连接信息。
   
4. 初始化数据库：
  ```bash
    # mysql创建数据库
   source create_table.sql
    # 初始化数据库内容 (可以用python initialize.py)
   source initialize.sql
  ```

5. 运行项目：
   ```bash
   python app.py
   ```

6. 打开浏览器访问：
   ```
   http://127.0.0.1:2333
   ```

## 功能说明

### 数据库设计

1. **概念结构设计**
   - 使用 E-R 图描述实体及其关系。
2. **逻辑结构设计**
   - 使用 SQL 脚本定义表结构。

### 应用系统实现

1. **数据库连接**
   - 使用 `Flask-SQLAlchemy` 进行数据库连接。
2. **数据库以及表的创建**
   - 提供 SQL 脚本 `create_table.sql`。
4. **数据查询、插入、更新、删除**
   - blueprints提供对应的 API 和templates提供前端页面。

## 文件说明

- `app.py`：主程序入口，注册蓝图并运行服务。
- `config.py`：配置文件，包含数据库连接信息等。
- `initialize.py`：初始化数据库内容脚本。
- `models.py`：ORM模型与表的映射。
- `blueprints/`：存放各功能模块的蓝图。
- `DP更新立绘`：需要时执行从米游社wiki爬取更新立绘
- `static/`：存放静态资源（CSS、JS、图片等）。
- `/static/illustration`：存放主视图的立绘
- `templates/`：存放 HTML 模板文件。

