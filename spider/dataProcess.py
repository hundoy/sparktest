#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import os

INFO_DIR = "rs/infos/"
OUTPUT_DIR = "rs/data/"
KUSER_DATA = "kuser.txt"
WB_DATA = "wb.txt"
WB_DETAIL_DATA = "wb_detail.txt"

BATCH = 3

def uid_format(uid):
    if isinstance(uid, long) or isinstance(uid, int):
        return str(uid)
    else:
        return uid.encode("utf-8")

if __name__ == "__main__":
    with open(OUTPUT_DIR + WB_DATA, "w") as wb_file:
        wb_file.write("wbid,uid,batch\n")
    with open(OUTPUT_DIR + WB_DETAIL_DATA, "w") as wb_detail_file:
        wb_detail_file.write("wbid,wbtype,uid,batch\n")

    kusers = []

    for info in os.listdir(INFO_DIR):
        with open(INFO_DIR+info, "r") as info_file:
            lines = info_file.readlines()

            # get uid
            # uid = lines[0].split(":")[1].strip()
            # nick_name = lines[1].split(":")[1].strip()
            uid = 0
            nick_name = ""
            # get all wbids and detail data
            wbids = []
            comments = {}
            reposts = {}
            likes = {}
            replys = {}
            for line in lines:
                if line.startswith("uid:"):
                    uid = line.split(":")[1].strip()
                elif line.startswith("nick_name:"):
                    nick_name = line.split(":")[1].strip()
                elif line.startswith("wb_"):
                    wbids_str = line.strip().split(":")[1].strip()
                    if len(wbids_str)>0:
                        line_wbids = wbids_str.split(",")
                        if len(line_wbids)>0:
                            wbids+=line_wbids
                elif line.startswith("{"):
                    wbdt = json.loads(line.strip())
                    wbid = wbdt["wbid"]
                    if len(wbdt["comment"])>0 : comments[wbid] = wbdt["comment"]
                    if len(wbdt["repost"]) > 0: reposts[wbid] = wbdt["repost"]
                    if len(wbdt["like"]) > 0: likes[wbid] = wbdt["like"]
                    if len(wbdt["reply"]) > 0: replys[wbid] = wbdt["reply"]

            if uid==0 or len(nick_name.strip())==0:
                print("[WARN]%s file error, uid or nick_name miss!" % info)
                continue
            else:
                kuser = {"uid": uid, "nick_name": nick_name}
                kusers.append(kuser)

            # write all wbids into file
            wbids = list(set(wbids))
            if len(wbids)>0:
                wb_file_content = "\n".join(map(lambda x: "%s,%s,%d" % (x, uid, BATCH), wbids))
                with open(OUTPUT_DIR+WB_DATA, "a") as wb_file:
                    wb_file.write(wb_file_content+"\n")
                    print("write user %s wb.txt end." % uid)


            # write all wb details into file
            comment_file_content = "\n".join(["%s,comment,%s,%d" % (wbid, uid_format(uid), BATCH) for wbid in comments.keys() for uid in comments[wbid]])
            repost_file_content = "\n".join(["%s,repost,%s,%d" % (wbid, uid_format(uid), BATCH) for wbid in reposts.keys() for uid in reposts[wbid]])
            like_file_content = "\n".join(["%s,like,%s,%d" % (wbid, uid_format(uid), BATCH) for wbid in likes.keys() for uid in likes[wbid]])
            reply_file_content = "\n".join(["%s,reply,%s,%d" % (wbid, uid_format(uid), BATCH) for wbid in replys.keys() for uid in replys[wbid]])
            file_content = ""
            if len(comments)>0: file_content+=comment_file_content+"\n"
            if len(reposts)>0: file_content+=repost_file_content+"\n"
            if len(likes)>0: file_content+=like_file_content+"\n"
            if len(replys)>0: file_content+=reply_file_content+"\n"

            if len(file_content)>0:
                with open(OUTPUT_DIR+WB_DETAIL_DATA, "a") as wb_detail_file:
                    wb_detail_file.write(file_content)
                    print("write user %s wb_detail.txt end." % uid)

    kuser_file_content = "\n".join(map(lambda j: "%s,%s,%d" % (j["uid"], j["nick_name"], BATCH), kusers))
    with open(OUTPUT_DIR + KUSER_DATA, "w") as kuser_file:
        kuser_file.write("uid,nick_name,batch\n"+kuser_file_content+"\n")
        print("write user %s kuser.txt end." % uid)

