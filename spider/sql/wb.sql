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

Date: 2018-02-04 15:51:56
*/


-- ----------------------------
-- Table structure for wb
-- ----------------------------
DROP TABLE IF EXISTS "public"."wb";
CREATE TABLE "public"."wb" (
"wbid" int8 NOT NULL,
"uid" int8 NOT NULL
)
WITH (OIDS=FALSE)

;

-- ----------------------------
-- Alter Sequences Owned By 
-- ----------------------------

-- ----------------------------
-- Primary Key structure for table wb
-- ----------------------------
ALTER TABLE "public"."wb" ADD PRIMARY KEY ("wbid");
