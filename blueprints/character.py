import os

from flask import Blueprint, request, jsonify, render_template, current_app
from models import Character
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('character', __name__, url_prefix='/characters')


@bp.route('/')
def get_characters():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    characters = Character.query.paginate(page=page, per_page=per_page, error_out=False)
    result = [
        {
            "id": character.id,
            "name": character.name,
            "path": character.path,
            "base_hp": character.base_hp,
            "profile": character.profile
        }
        for character in characters.items
    ]
    # 判断请求头
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or \
            request.accept_mimetypes.best == 'application/json':
        return jsonify({"status": "success", "data": result, "total": characters.total}), 200
    # 非AJAX请求则渲染网页
    return render_template("characters.html")


@bp.route('/adds', methods=['GET'])
def add_characters():
    return render_template("add_character.html")


@bp.route('/add', methods=['POST'])
def create_character():
    from extension import db  # 延迟导入，避免循环依赖
    try:
        data = request.get_json()
        name = data.get('name')
        path = data.get('path')
        base_hp = data.get('base_hp', 1000)
        profile = data.get('profile', '')
        avatar_url = data.get('avatar_url', 'static/img/default.png')

        if not name or not path:
            return jsonify({"status": "error", "message": "Name and path are required"}), 400

        # 检查是否存在与 name 同名的图片
        avatar_url = f"static/illustration/{name}.webp"
        if not os.path.exists(f"static/illustration/{name}.webp"):
            avatar_url = "static/img/default.png"# 默认头像路径
        print(f"static/illustration/{name}.webp")
        print(name)
        new_character = Character(
            name=name,
            path=path,
            base_hp=base_hp,
            profile=profile,
            avatar_url=avatar_url
        )
        db.session.add(new_character)
        db.session.commit()

        return jsonify({"status": "success", "message": "Character created successfully", "id": new_character.id}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route('/search', methods=['GET'])
def search_character():
    try:
        id = request.args.get('id')
        name = request.args.get('name')
        path = request.args.get('path')

        query = Character.query
        if id:
            query = query.filter_by(id=id)
        if name:
            query = query.filter(Character.name.like(f"%{name}%"))
        if path:
            query = query.filter_by(path=path)

        characters = query.all()
        result = [
            {
                "id": character.id,
                "name": character.name,
                "path": character.path,
                "base_hp": character.base_hp,
                "profile": character.profile
            }
            for character in characters
        ]
        return jsonify({"status": "success", "data": result}), 200
    except SQLAlchemyError as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route('/<int:id>', methods=['PUT'])
def update_character(id):
    from extension import db  # 延迟导入，避免循环依赖
    try:
        data = request.get_json()
        character = Character.query.get(id)
        if not character:
            return jsonify({"status": "error", "message": "Character not found"}), 404

        character.name = data.get('name', character.name)
        character.path = data.get('path', character.path)
        character.base_hp = data.get('base_hp', character.base_hp)
        character.profile = data.get('profile', character.profile)
        character.avatar_url = data.get('avatar_url', character.avatar_url)

        db.session.commit()
        return jsonify({"status": "success", "message": "Character updated successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@bp.route('/<int:id>', methods=['DELETE'])
def delete_character(id):
    from extension import db  # 延迟导入，避免循环依赖
    try:
        character = Character.query.get(id)
        if not character:
            return jsonify({"status": "error", "message": "Character not found"}), 404

        db.session.delete(character)
        db.session.commit()
        return jsonify({"status": "success", "message": "Character deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
