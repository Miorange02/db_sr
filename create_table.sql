CREATE DATABASE IF NOT EXISTS StarRail_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE StarRail_db;

-- 创建角色表
CREATE TABLE characters (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '角色名称',
    path VARCHAR(20) NOT NULL COMMENT '命途类型',
    base_hp INT NOT NULL DEFAULT 1000 COMMENT '基础生命值',
    profile VARCHAR(200) COMMENT '角色简介',
    avatar_url VARCHAR(255) COMMENT '头像URL'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建武器表
CREATE TABLE weapons (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL COMMENT '武器名称',
    path VARCHAR(20) NOT NULL COMMENT '适用命途',
    bonus_hp INT NOT NULL DEFAULT 1000 COMMENT '生命值加成'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建角色与武器关联表
CREATE TABLE equipments (
    character_id INT PRIMARY KEY COMMENT '角色唯一ID',
    weapon_id INT DEFAULT NULL COMMENT 'NULL表示未装备',
    FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE,
    FOREIGN KEY (weapon_id) REFERENCES weapons(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

