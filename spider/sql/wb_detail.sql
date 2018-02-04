/*
Navicat PGSQL Data Transfer

Source Server         : localpgsql
Source Server Version : 100100
Source Host           : localhost:5432
Source Database       : kemowb
Source Schema         : public

Target Server Type    : PGSQL
Target Server Version : 100100
File Encoding         : 65001

Date: 2018-02-04 15:52:05
*/


-- ----------------------------
-- Table structure for wb_detail
-- ----------------------------
DROP TABLE IF EXISTS "public"."wb_detail";
CREATE TABLE "public"."wb_detail" (
"wbid" int8 NOT NULL,
"wbtype" varchar COLLATE "default" NOT NULL,
"uid" int8 NOT NULL
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------
