#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import os

INFO_DIR = "rs/infos/"
OUTPUT_DIR = "rs/data/"
KUSER_DATA = "kuser.txt"
WB_DATA = "wb.txt"
WB_DETAIL_DATA = "wb_detail.txt"

BATCH = 1

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
            uid = lines[0].split(":")[1].strip()
            nick_name = lines[1].split(":")[1].strip()
            kuser = {"uid":uid, "nick_name":nick_name}
            kusers.append(kuser)

            # get all wbids and detail data
            wbids = []
            comments = {}
            reposts = {}
            likes = {}
            replys = {}
            for line in lines:
                if line.startswith("wb_"):
                    line_wbids = line.strip().split(":")[1].split(",")
                    wbids+=line_wbids
                elif line.startswith("{"):
                    wbdt = json.loads(line.strip())
                    wbid = wbdt["wbid"]
                    comments[wbid] = wbdt["comment"]
                    reposts[wbid] = wbdt["repost"]
                    likes[wbid] = wbdt["like"]
                    replys[wbid] = wbdt["reply"]

            # write all wbids into file
            wbids = list(set(wbids))
            wb_file_content = "\n".join(map(lambda x: "%s,%s,%d" % (x, uid, BATCH), wbids))
            with open(OUTPUT_DIR+WB_DATA, "a") as wb_file:
                wb_file.write(wb_file_content+"\n")
                print("write user %s wb.txt end." % uid)


            # write all wb details into file
            comment_file_content = "\n".join(["%s,comment,%s,%d" % (wbid, uid_format(uid), BATCH) for wbid in comments.keys() for uid in comments[wbid]])
            repost_file_content = "\n".join(["%s,repost,%s,%d" % (wbid, uid_format(uid), BATCH) for wbid in reposts.keys() for uid in reposts[wbid]])
            like_file_content = "\n".join(["%s,like,%s,%d" % (wbid, uid_format(uid), BATCH) for wbid in likes.keys() for uid in likes[wbid]])
            reply_file_content = "\n".join(["%s,reply,%s,%d" % (wbid, uid_format(uid), BATCH) for wbid in replys.keys() for uid in replys[wbid]])
            with open(OUTPUT_DIR+WB_DETAIL_DATA, "a") as wb_detail_file:
                wb_detail_file.write("%s\n%s\n%s\n%s\n" % (comment_file_content, repost_file_content, like_file_content, reply_file_content))
                print("write user %s wb_detail.txt end." % uid)

    kuser_file_content = "\n".join(map(lambda j: "%s,%s,%d" % (j["uid"], j["nick_name"], BATCH), kusers))
    with open(OUTPUT_DIR + KUSER_DATA, "w") as kuser_file:
        kuser_file.write("uid,nick_name,batch\n"+kuser_file_content+"\n")
        print("write user %s kuser.txt end." % uid)

