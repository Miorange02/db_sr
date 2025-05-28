from flask import Blueprint, render_template, request, jsonify
from models import Weapon
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('weapon', __name__, url_prefix='/weapons')


@bp.route('/')
def get_weapons():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    weapons = Weapon.query.paginate(page=page, per_page=per_page, error_out=False)
    result = [
        {
            "id": weapon.id,
            "name": weapon.name,
            "path": weapon.path,
            "bonus_hp": weapon.bonus_hp
        }
        for weapon in weapons.items
    ]
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
            request.accept_mimetypes.best == 'application/json':
        return jsonify({"status": "success", "data": result, "total": weapons.total}), 200
    return render_template("weapons.html")


@bp.route('/adds', methods=['GET'])
def add_weapons():
    return render_template("add_weapon.html")


@bp.route('/add', methods=['POST'])
def create_weapon():
    from extension import db  # 延迟导入，避免循环依赖
    try:
        data = request.get_json()
        name = data.get('name')
        path = data.get('path')
        bonus_hp = data.get('bonus_hp', 500)

        if not name or not path:
            return jsonify({"status": "error", "message": "Name, path and are required"}), 400
        new_weapon = Weapon(
            name=name,
            path=path,
            bonus_hp=bonus_hp
        )
        db.session.add(new_weapon)
        db.session.commit()
        return jsonify({"status": "success", "message": "Weapon created successfully", "id": new_weapon.id}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route('/search', methods=['GET'])
def search_weapon():
    try:
        id = request.args.get('id')
        name = request.args.get('name')
        path = request.args.get('path')
        query = Weapon.query
        if id:
            query = query.filter_by(id=id)
        if name:
            query = query.filter(Weapon.name.like(f"%{name}%"))
        if path:
            query = query.filter_by(path=path)
        weapons = query.all()
        result = [
            {
                "id": weapon.id,
                "name": weapon.name,
                "path": weapon.path,
                "bonus_hp": weapon.bonus_hp
            }
            for weapon in weapons
        ]
        return jsonify({"status": "success", "data": result}), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route('/<int:id>', methods=['PUT'])
def update_Weapon(id):
    from extension import db  # 延迟导入，避免循环依赖
    try:
        data = request.get_json()
        weapon = Weapon.query.get(id)
        if not weapon:
            return jsonify({"status": "error", "message": "Weapon not found"}), 404

        weapon.name = data.get('name', weapon.name)
        weapon.path = data.get('path', weapon.path)
        weapon.bonus_hp = data.get('bonus_hp', weapon.bonus_hp)

        db.session.commit()
        return jsonify({"status": "success", "message": "Weapon updated successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route('/<int:id>', methods=['DELETE'])
def delete_weapon(id):
    from extension import db  # 延迟导入，避免循环依赖
    try:
        weapon = Weapon.query.get(id)
        if not weapon:
            return jsonify({"status": "error", "message": "Weapon not found"}), 404
        db.session.delete(weapon)
        db.session.commit()
        return jsonify({"status": "success", "message": "Weapon deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
