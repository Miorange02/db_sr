-- 删除角色表
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE characters;
SET FOREIGN_KEY_CHECKS = 1;
-- 删除武器表
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE weapons;
SET FOREIGN_KEY_CHECKS = 1;

-- 清空表数据
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE equipments;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO characters (name, path, base_hp, profile, avatar_url) VALUES
('遐蝶', '记忆', 2025, '冥河的女儿遐蝶，寻索「死亡」火种的黄金裔，启程吧。呵护世间魂灵的恸哭，拥抱命运的孤独——生死皆为旅途，当蝴蝶停落枝头，那凋零的又将新生。', 'static/illustration/遐蝶.webp'),
('风堇', '记忆', 1700, '医师雅辛忒丝，守望「天空」火种的黄金裔。丸山彩形态高松灯', 'static/illustration/风堇.webp'),
('刃', '毁灭', 1400, '「星核猎手」的成员，弃身锋刃的剑客。效忠于「命运的奴隶」，拥有可怖的自愈能力。魔芋,爽', 'static/illustration/刃.webp'),
('镜流', '毁灭', 1100, '曾经的罗浮剑首，云骑军不败盛名的缔造者。孩子们我有萌嘤身', 'static/illustration/镜流.webp'),
('流萤', '毁灭', 1600, '星核猎手成员，身着机械装甲「萨姆」战斗。为了找寻「生」的机会而加入星核猎手，找寻违抗命运的方式。宝宝你是一个香香软软的小蛋糕', 'static/illustration/流萤.webp'),
('景元', '智识', 1032, '仙舟联盟帝弓七天将之一，负责节制罗浮云骑军的「神策将军」。要剧情有剧情,要强度有剧情', 'static/illustration/景元.webp'),
('停云', '同谐', 1015, '仙舟「罗浮」天舶司的接渡使。随商团出使过众多世界，缔结贸易与盟谊。歪头杀可还行', 'static/illustration/停云.webp'),
('开拓者•存护', '存护', 1240, '登上星穹列车的开拓者。为了消除星核带来的危机，选择与星穹列车同行。这简直就是我啊', 'static/illustration/开拓者•存护.webp'),
('仙舟三月七', '巡猎', 1040, '换上仙舟服饰的三月七，执剑的武侠少女。向云璃与彦卿拜师学艺，为在仙舟留下更多美好的「回忆」而跃跃欲试。', 'static/illustration/仙舟三月七.webp'),
('黄泉', '虚无', 1200,'自称「巡海游侠」的旅人，本名不详。身佩一柄长刀，独行银河。黄泉大人●▛▙黄泉大人●▛▙黄泉大人●▛▙黄泉大人●▛▙', 'static/illustration/黄泉.webp'),
('卡芙卡', '虚无', 800,'「星核猎手」的成员，听我说dot队玩家才是最有游戏理解的那个', 'static/illustration/卡芙卡.webp'),
('青雀', '智识', 1111,'仙舟「罗浮」太卜司的卜者，兼书库管理员。因工作一再偷闲摸鱼，即将贬无可贬成为「掌门人」。', 'static/illustration/青雀.webp'),
('雪衣', '毁灭', 1000,'仙舟「罗浮」上监察生死的机构「十王司」的判官。这下真的机巧少女不会受伤了。', 'static/illustration/雪衣.webp'),
('云璃', '毁灭', 1200,'仙舟「朱明」的猎剑士，备受「烛渊将军」怀炎宠爱的孙女，性格直率。云璃，你可以吃琼食鸟串。', 'static/illustration/云璃.webp'),
('花火', '同协', 1000,'「假面愚者」的成员之一，难以捉摸，不择手段。', 'static/illustration/花火.webp'),
('加拉赫', '丰饶', 1400,'匹诺康尼猎犬家系的治安官。这特么八岁。', 'static/illustration/加拉赫.webp');

INSERT INTO weapons (name, path, bonus_hp) VALUES
('让告别,更美一些', '记忆', 700),
('银河铁道之夜', '智识', 500),
('到不了的彼岸', '毁灭', 470),
('芳华待灼', '巡猎', 400),
('舞,舞,舞', '同谐', 450),
('游戏尘寰', '同谐', 380),
('雨一直下', '虚无', 550),
('等价交换', '丰饶', 750),
('梦因归于何处', '毁灭', 540),
('宇宙市场趋势', '存护', 420),
('拂晓之前', '智识', 500);

INSERT INTO equipments (character_id, weapon_id) VALUES
(1, 1),
(3, 3),
(5, 9),
(7, NULL),
(8, NULL);
