from flask import Flask
from extension import db
import config
from blueprints.character import bp as bp_character
from blueprints.weapon import bp as bp_weapon
from blueprints.equipment import bp as bp_equipment
from flask_caching import Cache


app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

# 初始化缓存
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/some_data')
@cache.cached(timeout=60)
def some_data():
    # 模拟数据处理
    return {'data': 'these are some caching data'}

app.register_blueprint(bp_character)
app.register_blueprint(bp_weapon)
app.register_blueprint(bp_equipment)


if __name__ == '__main__':
    app.run(port=2333, debug=True)
