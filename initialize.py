import os
import re
from sqlalchemy import create_engine, text
from config import SQLALCHEMY_DATABASE_URI  # 从配置文件中导入数据库连接字符串


def init_database():
    sql_file = 'initialize.sql'

    if not os.path.exists(sql_file):
        print(f"错误：找不到文件 {sql_file}")
        return False

    try:
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # 预处理 SQL 内容
        sql_content = re.sub(r'--.*$', '', sql_content, flags=re.MULTILINE)  # 移除注释
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]

        # 定义数据库引擎
        engine = create_engine(SQLALCHEMY_DATABASE_URI)  # 使用 MySQL 的连接字符串

        with engine.connect() as conn:
            for stmt in statements:
                if 'SET FOREIGN_KEY_CHECKS' in stmt or 'TRUNCATE TABLE' in stmt:
                    conn.execute(text(stmt))  # 单独执行
                else:
                    with conn.begin():  # 自动事务管理
                        conn.execute(text(stmt))

        print("✅ 数据库初始化成功")
        return True

    except Exception as e:
        print(f"❌ 初始化失败: {str(e)}")
        return False


if __name__ == '__main__':
    init_database()
