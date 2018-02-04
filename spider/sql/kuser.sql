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

Date: 2018-02-04 15:51:17
*/


-- ----------------------------
-- Table structure for kuser
-- ----------------------------
DROP TABLE IF EXISTS "public"."kuser";
CREATE TABLE "public"."kuser" (
"uid" int8 NOT NULL,
"nick_name" varchar COLLATE "default"
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table kuser
-- ----------------------------
ALTER TABLE "public"."kuser" ADD PRIMARY KEY ("uid");
