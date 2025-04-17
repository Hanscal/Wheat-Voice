-- 创建数据库
CREATE DATABASE IF NOT EXISTS wheatvoice CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE wheatvoice;

-- 设置字符集和禁用外键约束
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- 创建 user 表
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `phone` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `verification_code` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `sign_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `receive_date` datetime DEFAULT NULL,
  `password` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `account` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`,`phone`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- 创建 ay_member 表
-- ----------------------------
DROP TABLE IF EXISTS `ay_member`;
CREATE TABLE `ay_member` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ucode` varchar(20) NOT NULL,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `usermobile` varchar(11) NOT NULL DEFAULT '',
  `useremail` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '',
  `nickname` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `password` varchar(32) NOT NULL,
  `headpic` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `status` varchar(1) NOT NULL,
  `gid` varchar(20) NOT NULL,
  `wxid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `qqid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `wbid` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `score` int NOT NULL DEFAULT '0',
  `register_time` varchar(30) NOT NULL,
  `login_count` int NOT NULL DEFAULT '0',
  `last_login_ip` varchar(30) NOT NULL,
  `last_login_time` varchar(30) NOT NULL,
  `sex` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '',
  `birthday` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '',
  `qq` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT '',
  `activation` varchar(1) NOT NULL DEFAULT '1',
  `APPKey` varchar(100) DEFAULT NULL,
  `sign_name` varchar(255) DEFAULT NULL,
  `verification_code` varchar(255) DEFAULT NULL,
  `receive_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ay_member_ucode` (`ucode`),
  UNIQUE KEY `ay_member_username` (`username`),
  KEY `ay_member_gid` (`gid`),
  KEY `ay_member_qqid` (`qqid`),
  KEY `ay_member_useremail` (`useremail`),
  KEY `ay_member_usermobile` (`usermobile`),
  KEY `ay_member_wbid` (`wbid`),
  KEY `ay_member_wxid` (`wxid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 恢复外键检查
SET FOREIGN_KEY_CHECKS = 1;
