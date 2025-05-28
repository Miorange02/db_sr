from flask import Blueprint, render_template, jsonify, request
from models import Character, Equipment, Weapon

bp = Blueprint('equipment', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route('/initialize', methods=['GET'])
def initialize():
    pass


@bp.route('/equipments', methods=['GET'])
def get_characters():
    from app import db  # 延迟导入
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 9, type=int)
    characters_query = Character.query
    total = characters_query.count()
    characters = characters_query.paginate(page=page, per_page=per_page, error_out=False).items

    data = []
    for character in characters:
        equipment = Equipment.query.filter_by(character_id=character.id).first()
        weapon = equipment.weapon if equipment and equipment.weapon else None
        total_hp = character.base_hp + (weapon.bonus_hp if weapon else 0)
        data.append({
            'id': character.id,
            'name': character.name,
            'weapon': weapon.name if weapon else '无',
            'total_hp': total_hp,
            'profile': character.profile,
            'avatar_url': character.avatar_url
        })

    return jsonify({
        "data": data,
        "total": total,
        "page": page,
        "per_page": per_page
    })


@bp.route('/equipments/<int:character_id>', methods=['POST'])
def update_equipment(character_id):
    from app import db  # 延迟导入
    data = request.get_json()
    weapon_id = data.get('weapon_id')

    # 验证角色是否存在
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"message": "角色不存在"}), 404

    # 处理卸下装备的情况
    if weapon_id is None:
        equipment = Equipment.query.filter_by(character_id=character_id).first()
        if equipment:
            equipment.weapon_id = None
            db.session.commit()
        return jsonify({"message": "已成功卸下光锥"}), 200

    # 验证光锥是否存在
    weapon = Weapon.query.get(weapon_id)
    if not weapon:
        return jsonify({"message": "光锥不存在"}), 400

    # 创建或更新装备记录
    equipment = Equipment.query.filter_by(character_id=character_id).first()
    if not equipment:
        equipment = Equipment(character_id=character_id, weapon_id=weapon_id)
        db.session.add(equipment)
    else:
        equipment.weapon_id = weapon_id

    try:
        db.session.commit()
        return jsonify({"message": "光锥更新成功"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "数据库更新失败", "error": str(e)}), 500