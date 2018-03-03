#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import os
import re
import sys
import traceback
from datetime import datetime
from datetime import timedelta
import time

import requests

import urllib

def save_image(url, filePath):
    with open(filePath, 'wb') as handle:
        response = requests.get(url, stream=True)
        if not response.ok:
            print response
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)


def save_txt(txt, filePath):
    with open(filePath, 'w') as of:
        of.write(txt.encode('utf-8'))


def save_txt_add(txt, filePath):
    with open(filePath, 'a') as of:
        of.write(txt.encode('utf-8'))


def get_data(url):
    try:
        str = requests.get(url, cookies=cookie).content
        json_data = json.loads(str)
        return json_data
    except Exception, e:
        print "error: ", e
        return {}


def save_block(pid, arr, file_path, kname):
    bid = (pid - 1) / PAGE_BLOCK + 1
    save_txt_add("%s_%d:%s\n" % (kname, bid, ",".join(arr)), file_path)
    del arr[:]
    print("%s block %d saved." % (kname, bid))


def is_index_valid(index_info):
    # $.data.cards[字符串00,01].mblog.id  wb_detail_id
    return "data" in index_info and "cards" in index_info["data"] and len(index_info["data"]["cards"])>0


def get_user_info(uid, info_file_path):
    # get his nickname and avatar
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1878650541&containerid=1005051878650541
    # $.data.userInfo.avatar_hd
    # $.data.userInfo.screen_name
    user_info = get_data(
        "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=100505%s" % (uid, uid))
    nick_name = ""
    if "data" in user_info:
        head_url = user_info["data"]["userInfo"]["avatar_hd"]
        nick_name = user_info["data"]["userInfo"]["screen_name"]
        save_image(head_url, "%s%s.jpg" % (head_dir, uid))
        print(u"user %s head pic saved." % (uid))
        txt = "uid:%s\n" % uid
        txt += "nick_name:%s\n" % nick_name
        save_txt(txt, info_file_path)
    else:
        print("[WARN] when get user %s, you get a empty user info..." % uid)


def is_created_at_valid(mblog):
    if "created_at" not in mblog: return False
    created_at = mblog["created_at"].encode("utf-8")
    # before 2017 -> False
    if created_at.startswith("201") and not created_at.startswith("2018-") and not created_at.startswith("2017-"): return False
    # before 2017-10 -> False
    if created_at.startswith("2017-0") or created_at.startswith("2017-9") or created_at.startswith("2017-8") or created_at.startswith("2017-7") or created_at.startswith("2017-6") or created_at.startswith("2017-5") or created_at.startswith("2017-4") or created_at.startswith("2017-3") or created_at.startswith("2017-2") or created_at.startswith("2017-1-"): return False
    return True

def get_index_info(uid, info_file_path):
    # get his recently one month original po's WBID
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1428162532&containerid=107603 1428162532&page=4
    # $.data.cards[字符串00,01].mblog.created_at 时间（可能是字符）
    # $.data.cards[字符串00,01].mblog.id  wb_detail_id
    # $.data.cards[字符串00,01].mblog.retweeted_status 这个数组存在表示是retweet
    pid = 1
    wbids = []
    fault_time = 0
    reach_time_num = 0
    while True:
        # wait some time, i am a person, i need rest
        time.sleep(1)

        load_success = True
        reach_time = False

        # load page content
        index_info = get_data(
            "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%d" % (
            uid, uid, pid))

        # when load fail, wait 5s and retry
        retry_time = 0
        while not is_index_valid(index_info):
            time.sleep(2)
            index_info = get_data(
                "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%d" % (
                uid, uid, pid))
            retry_time += 1
            if retry_time > MAX_RETRY:
                print("[WARN]user %s index page %d is empty!" % (uid, pid))
                load_success = False
                break

        # get info start
        if load_success:
            fault_time = 0
            for card_i in range(0, len(index_info["data"]["cards"])):
                card = index_info["data"]["cards"][card_i]

                # filter
                if "mblog" not in card:
                    continue

                if not is_created_at_valid(card["mblog"]):
                    reach_time_num += 1
                    if reach_time_num >= 3:
                        reach_time = True
                        break
                else:
                    reach_time_num = 0
                    if "retweeted_status" in card["mblog"]: continue

                wbid = str(card["mblog"]["id"])

                if len(wbid.strip())>0:
                    wbids.append(wbid)

            if reach_time:
                break

            pid += 1

            # reach block
            if pid % PAGE_BLOCK == 0:
                if len(wbids)>0:
                    save_block(pid, wbids, info_file_path, "wb")
        else:
            # when continuous fault time more than max fault tolerant time, end loop
            fault_time += 1
            if fault_time > FAULT_TORL:
                break


    # final save block
    if len(wbids) > 0:
        save_block(pid, wbids, info_file_path, "wb")

    print("get %s wb fin. at page %d" % (uid, pid))


def is_detail_valid(info):
    # $.data.data[i].user.id
    return "data" in info and "data" in info["data"] and len(info["data"]["data"])>0


def is_detail_no_data(info):
    return "msg" in info and info["msg"]==u"暂无数据"


def get_some_detail_uids(type_name, detail, wbid, uid):
    replys = [] # only used in comment type
    comments = {} # only userd in comment type. data.id -> {uid: data.user.id, reply_to: another data.id}
    pid = 2
    uids = []
    fault_time = 0
    while True:
        time.sleep(1)
        load_success = True
        some_info = get_data(TYPE_URL[type_name] % (wbid, pid))
        if is_detail_no_data(some_info):
            fault_time += 1
            if fault_time > FAULT_TORL: break;
            pid+=1
            continue

        # when load fail, wait 5s and retry
        retry_time = 0
        while not is_detail_valid(some_info):
            time.sleep(1)
            some_info = get_data(TYPE_URL[type_name] % (wbid, pid))
            retry_time += 1
            if retry_time > MAX_RETRY:
                print("[WARN]user %s %s page %d is empty!" % (uid, type_name, pid))
                load_success = False
                break

        if load_success:
            fault_time = 0
            for data in some_info["data"]["data"]:
                other_uid = str(data["user"]["id"])
                # when wb master reply guest, record the guest user
                if type_name=="comment":
                    comments[data["id"]] = {"uid":other_uid}
                    if "reply_id" in data: comments[data["id"]]["reply_to"] = str(data["reply_id"])
                else:
                    uids.append(other_uid)

            pid += 1
        else:
            fault_time += 1
            if fault_time > FAULT_TORL:
                print("reach fault limit.")
                break;

    # finally append
    if type_name=="comment":
        for dataid in comments.keys():
            cm = comments[dataid]
            if "reply_to" in cm and cm["reply_to"] in comments:
                replys.append(comments[cm["reply_to"]]["uid"])
            else:
                uids.append(cm["uid"])

        detail["reply"] = replys

    detail[type_name] = uids


def get_detail_info(uid, info_file_path):
    # 1. load info file via uid.
    # 2. get wb_N, all the wbid.
    # 3. get last line's wbid, know current index.
    # 4. continue to catch wbid from current index.
    cur_i = 0
    wbids = []
    with open(info_file_path) as info_file:
        lines = info_file.readlines()
        for line in lines:
            if line.startswith("wb_"):
                right = line.split(":")[1]
                wbids+=right.split(",")
            elif line.startswith("{"):
                break
        last_line = lines[-1]
        if last_line.startswith("{"):
            wb_detail = json.loads(last_line)
            cur_wbid = wb_detail["wbid"].encode("utf-8")
            cur_i = wbids.index(cur_wbid)
            cur_i+=1

    while cur_i<len(wbids):
        # wbid = "4201908917042237"
        wbid = wbids[cur_i].strip()

        detail = {"wbid": wbid}
        get_some_detail_uids("comment", detail, wbid, uid)
        get_some_detail_uids("repost", detail, wbid, uid)
        get_some_detail_uids("like", detail, wbid, uid)

        save_txt_add(json.dumps(detail)+"\n", info_file_path)

        print("user %s 's wb %s saved." % (uid, wbid))

        cur_i+=1

    print("fin catch all the detail!")


# prepare
MAX_RETRY = 1
PAGE_BLOCK = 5
FAULT_TORL = 1
TYPE_URL = {
    "comment" : "https://m.weibo.cn/api/comments/show?id=%s&page=%d",
    "repost" : "https://m.weibo.cn/api/statuses/repostTimeline?id=%s&page=%d",
    "like" : "https://m.weibo.cn/api/attitudes/show?id=%s&page=%d"
}
# https://m.weibo.cn/api/attitudes/show?id=4194822954639659&page=2
base_dir = "rs/"
head_dir = base_dir + "heads/"
info_dir = base_dir + "infos/"


cookie = ""  # 将your cookie替换成自己的cookie

if __name__ == "__main__":
    # choose one user
    uids = {
        "yaluo" : "1878650541",
        "ala" : "3173872645",
        "zixiong" : "1626912380",
        "buge": "5175655487"
    }
    # uid = uids["ala"]
    uid = sys.argv[1]

    print("start catch user %s ..." % uid)
    info_file_path = "%s%s.txt" % (info_dir, uid)

    get_user_info(uid, info_file_path)
    get_index_info(uid, info_file_path)
    get_detail_info(uid, info_file_path)



