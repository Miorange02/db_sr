# models.py
from extension import db


class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, comment='角色名称')
    path = db.Column(db.String(20), nullable=False, comment='命途类型')
    base_hp = db.Column(db.Integer, nullable=False, default=1000, comment='基础生命值')
    profile = db.Column(db.String(200), comment='角色简介')
    avatar_url = db.Column(db.String(255), nullable=False, default='static/img/default.png', comment='头像URL')


class Weapon(db.Model):
    __tablename__ = 'weapons'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, comment='光锥名称')
    path = db.Column(db.String(20), nullable=False, comment='适用命途')
    bonus_hp = db.Column(db.Integer, nullable=False, default=1000, comment='生命值加成')


class Equipment(db.Model):
    __tablename__ = 'equipments'
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id', ondelete='CASCADE'), primary_key=True,
                             comment='角色唯一ID')
    weapon_id = db.Column(db.Integer, db.ForeignKey('weapons.id', ondelete='SET NULL'), nullable=True,
                          comment='NULL表示未装备')

    character = db.relationship('Character',
                                backref=db.backref('equipment', uselist=False, cascade='all, delete-orphan'))
    weapon = db.relationship('Weapon', backref=db.backref('equipments', cascade='all, delete'))
