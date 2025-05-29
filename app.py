from flask import Flask
from extension import db
import config
from blueprints.character import bp as bp_character
from blueprints.weapon import bp as bp_weapon
from blueprints.equipment import bp as bp_equipment


app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

app.register_blueprint(bp_character)
app.register_blueprint(bp_weapon)
app.register_blueprint(bp_equipment)


if __name__ == '__main__':
    app.run(port=2333, debug=True)
