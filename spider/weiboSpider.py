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
from lxml import etree

import urllib


class Weibo:
    cookie = {"Cookie": "ALF=1519909430; SCF=Ag7WAWXq6Zx_fi-6imcy2besbl_eO4pJnIOFELxCLWlV_5Q8_9OuNpb9w4wkaN53s_9s0zr-YZebui3W0dOUW2E.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhvQRSX9UM3aV-rOEsh7Dph5JpX5K-hUgL.FozReo-N1Ke7Soe2dJLoIpYLxKnL12BLBoMLxKBLB.eL122LxKqL1KnL12HkeKn4; SUB=_2A253dA1RDeThGeRG6VcW-S3MzT-IHXVUlpMZrDV6PUJbkdANLXHmkW1NTczUO0H0LINW09hWYCnFL_w_Dqk_ZmOI; SUHB=0V51bfV43P_0rp; SSOLoginState=1517321489"}  # 将your cookie替换成自己的cookie

    # Weibo类初始化
    def __init__(self, user_id, filter=0):
        self.user_id = user_id  # 用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter  # 取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.username = ''  # 用户名，如“Dear-迪丽热巴”
        self.weibo_num = 0  # 用户全部微博数
        self.weibo_num2 = 0  # 爬取到的微博数
        self.following = 0  # 用户关注数
        self.followers = 0  # 用户粉丝数
        self.weibo_content = []  # 微博内容
        self.publish_time = []  # 微博发布时间
        self.up_num = []  # 微博对应的点赞数
        self.retweet_num = []  # 微博对应的转发数
        self.comment_num = []  # 微博对应的评论数

    # 获取用户昵称
    def get_username(self):
        try:
            url = "https://weibo.cn/%d/info" % (self.user_id)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            username = selector.xpath("//title/text()")[0]
            self.username = username[:-3]
            print u"用户名: " + self.username
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 获取用户微博数、关注数、粉丝数
    def get_user_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"

            # 微博数
            str_wb = selector.xpath(
                "//div[@class='tip2']/span[@class='tc']/text()")[0]
            guid = re.findall(pattern, str_wb, re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weibo_num = num_wb
            print u"微博数: " + str(self.weibo_num)

            # 关注数
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print u"关注数: " + str(self.following)

            # 粉丝数
            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print u"粉丝数: " + str(self.followers)

        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 获取用户微博内容及对应的发布时间、点赞数、转发数、评论数
    def get_weibo_info(self):
        try:
            url = "https://weibo.cn/u/%d?filter=%d&page=1" % (
                self.user_id, self.filter)
            html = requests.get(url, cookies=self.cookie).content
            selector = etree.HTML(html)
            if selector.xpath("//input[@name='mp']") == []:
                page_num = 1
            else:
                page_num = (int)(selector.xpath(
                    "//input[@name='mp']")[0].attrib["value"])
            pattern = r"\d+\.?\d*"
            for page in range(1, 3):
            # for page in range(1, page_num + 1):
                url2 = "https://weibo.cn/u/%d?filter=%d&page=%d" % (
                    self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=self.cookie).content
                print(url2)
                print(html2)


                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                if len(info) > 3:
                    for i in range(0, len(info) - 2):
                        # 微博内容
                        str_t = info[i].xpath("div/span[@class='ctt']")
                        weibo_content = str_t[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        self.weibo_content.append(weibo_content)
                        print u"微博内容：" + weibo_content

                        # 微博发布时间
                        str_time = info[i].xpath("div/span[@class='ct']")
                        str_time = str_time[0].xpath("string(.)").encode(
                            sys.stdout.encoding, "ignore").decode(
                            sys.stdout.encoding)
                        publish_time = str_time.split(u'来自')[0]
                        if u"刚刚" in publish_time:
                            publish_time = datetime.now().strftime(
                                '%Y-%m-%d %H:%M')
                        elif u"分钟" in publish_time:
                            minute = publish_time[:publish_time.find(u"分钟")]
                            minute = timedelta(minutes=int(minute))
                            publish_time = (
                                datetime.now() - minute).strftime(
                                "%Y-%m-%d %H:%M")
                        elif u"今天" in publish_time:
                            today = datetime.now().strftime("%Y-%m-%d")
                            time = publish_time[3:]
                            publish_time = today + " " + time
                        elif u"月" in publish_time:
                            year = datetime.now().strftime("%Y")
                            month = publish_time[0:2]
                            day = publish_time[3:5]
                            time = publish_time[7:12]
                            publish_time = (
                                year + "-" + month + "-" + day + " " + time)
                        else:
                            publish_time = publish_time[:16]
                        self.publish_time.append(publish_time)
                        print u"微博发布时间：" + publish_time

                        # 点赞数
                        str_zan = info[i].xpath("div/a/text()")[-4]
                        guid = re.findall(pattern, str_zan, re.M)
                        up_num = int(guid[0])
                        self.up_num.append(up_num)
                        print u"点赞数: " + str(up_num)

                        # 转发数
                        retweet = info[i].xpath("div/a/text()")[-3]
                        guid = re.findall(pattern, retweet, re.M)
                        retweet_num = int(guid[0])
                        self.retweet_num.append(retweet_num)
                        print u"转发数: " + str(retweet_num)

                        # 评论数
                        comment = info[i].xpath("div/a/text()")[-2]
                        guid = re.findall(pattern, comment, re.M)
                        comment_num = int(guid[0])
                        self.comment_num.append(comment_num)
                        print u"评论数: " + str(comment_num)

                        self.weibo_num2 += 1

            if not self.filter:
                print u"共" + str(self.weibo_num2) + u"条微博"
            else:
                print (u"共" + str(self.weibo_num) + u"条微博，其中" +
                       str(self.weibo_num2) + u"条为原创微博"
                       )

            ret_url = "https://weibo.cn/repost/G0NETty0t?uid=1878650541&rl=0&page=2"
            comt_url = "https://weibo.cn/comment/G0NETty0t?&uid=1878650541&&page=2"
            atti_url = "https://weibo.cn/attitude/G0NETty0t?&page=2"

            ret_html = requests.get(ret_url, cookies=self.cookie).content
            print(ret_url)
            print(ret_html)

            comt_html = requests.get(comt_url, cookies=self.cookie).content
            print(comt_url)
            print(comt_html)

            atti_html = requests.get(atti_url, cookies=self.cookie).content
            print(atti_url)
            print(atti_html)


        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 将爬取的信息写入文件
    def write_txt(self):
        try:
            if self.filter:
                result_header = u"\n\n原创微博内容：\n"
            else:
                result_header = u"\n\n微博内容：\n"
            result = (u"用户信息\n用户昵称：" + self.username +
                      u"\n用户id：" + str(self.user_id) +
                      u"\n微博数：" + str(self.weibo_num) +
                      u"\n关注数：" + str(self.following) +
                      u"\n粉丝数：" + str(self.followers) +
                      result_header
                      )
            for i in range(1, self.weibo_num2 + 1):
                text = (str(i) + ":" + self.weibo_content[i - 1] + "\n" +
                        u"发布时间：" + self.publish_time[i - 1] + "\n" +
                        u"点赞数：" + str(self.up_num[i - 1]) +
                        u"	 转发数：" + str(self.retweet_num[i - 1]) +
                        u"	 评论数：" + str(self.comment_num[i - 1]) + "\n\n"
                        )
                result = result + text
            file_dir = os.path.split(os.path.realpath(__file__))[
                0] + os.sep + "weibo"
            if not os.path.isdir(file_dir):
                os.mkdir(file_dir)
            file_path = file_dir + os.sep + "%d" % self.user_id + ".txt"
            f = open(file_path, "wb")
            f.write(result.encode(sys.stdout.encoding))
            f.close()
            print u"微博写入文件完毕，保存路径:" + file_path
        except Exception, e:
            print "Error: ", e
            traceback.print_exc()

    # 运行爬虫
    def start(self):
        try:
            self.get_username()
            self.get_user_info()
            self.get_weibo_info()
            self.write_txt()
            print u"信息抓取完毕"
            print "==========================================================================="
        except Exception, e:
            print "Error: ", e


def main():
    try:
        # 使用实例,输入一个用户id，所有信息都会存储在wb实例中
        user_id = 1878650541  # 可以改成任意合法的用户id（爬虫的微博id除外）
        filter = 1  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
        wb = Weibo(user_id, filter)  # 调用Weibo类，创建微博实例wb
        wb.start()  # 爬取微博信息
        print u"用户名：" + wb.username
        print u"全部微博数：" + str(wb.weibo_num)
        print u"关注数：" + str(wb.following)
        print u"粉丝数：" + str(wb.followers)
        print u"最新一条原创微博为：" + wb.weibo_content[0]
        print u"最新一条原创微博发布时间：" + wb.publish_time[0]
        print u"最新一条原创微博获得的点赞数：" + str(wb.up_num[0])
        print u"最新一条原创微博获得的转发数：" + str(wb.retweet_num[0])
        print u"最新一条原创微博获得的评论数：" + str(wb.comment_num[0])
    except Exception, e:
        print "Error: ", e
        traceback.print_exc()

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
        print("user %s %s head pic saved." % (uid, nick_name))
        txt = "uid:%s\n" % uid
        txt += "nick_name:%s\n" % nick_name
        save_txt(txt, info_file_path)
    else:
        print("[WARN] when get user %s, you get a empty user info..." % uid)


def get_index_info(uid, info_file_path):
    # get his recently one month original po's WBID
    # https://m.weibo.cn/api/container/getIndex?type=uid&value=1428162532&containerid=107603 1428162532&page=4
    # $.data.cards[字符串00,01].mblog.created_at 时间（可能是字符）
    # $.data.cards[字符串00,01].mblog.id  wb_detail_id
    # $.data.cards[字符串00,01].mblog.retweeted_status 这个数组存在表示是retweet
    pid = 1
    wbids = []
    fault_time = 0
    while True:
        # wait some time, i am a person, i need rest
        time.sleep(2)

        load_success = True
        reach_time = False

        # load page content
        index_info = get_data(
            "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%d" % (
            uid, uid, pid))

        # when load fail, wait 5s and retry
        retry_time = 0
        while not is_index_valid(index_info):
            time.sleep(5)
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
                if "mblog" not in card or "retweeted_status" in card["mblog"]:
                    continue

                create_at = card["mblog"]["created_at"]
                wbid = card["mblog"]["id"]

                if create_at.startswith(u"2017-"):
                    reach_time = True
                    break

                wbids.append(wbid)

            if reach_time: break

            pid += 1

            # reach block
            if pid % PAGE_BLOCK == 0:
                save_block(pid, wbids, info_file_path, "wb")
        else:
            # when continuous fault time more than max fault tolerant time, end loop
            fault_time += 1
            if fault_time > FAULT_TORL:
                break
            else:
                time.sleep(10)

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
    pid = 1
    uids = []
    fault_time = 0
    while True:
        time.sleep(2)
        load_success = True
        some_info = get_data(TYPE_URL[type_name] % (wbid, pid))
        if is_detail_no_data(some_info):
            fault_time += 1
            if fault_time > FAULT_TORL: break;
            continue

        # when load fail, wait 5s and retry
        retry_time = 0
        while not is_detail_valid(some_info):
            time.sleep(5)
            some_info = get_data(TYPE_URL[type_name] % (wbid, pid))
            retry_time += 1
            if retry_time > MAX_RETRY:
                print("[WARN]user %s %s page %d is empty!" % (uid, type_name, pid))
                load_success = False
                break

        if load_success:
            fault_time = 0
            for data in some_info["data"]["data"]:
                other_uid = data["user"]["id"]
                uids.append(other_uid)

            pid += 1
        else:
            fault_time += 1
            if fault_time > FAULT_TORL:
                break;
            time.sleep(5)

    # finally append
    detail[type_name] = uids


def get_detail_info(uid, info_file_path):
    with open(info_file_path) as info_file:
        pass

    wbid = "4201908917042237"

    detail = {"wbid": wbid}

    get_some_detail_uids("comment", detail, wbid, uid)
    get_some_detail_uids("repost", detail, wbid, uid)
    get_some_detail_uids("like", detail, wbid, uid)

    save_txt_add(json.dumps(detail), info_file_path)

    print("user %s 's wb %s saved." % (uid, wbid))


# prepare
MAX_RETRY = 3
PAGE_BLOCK = 5
FAULT_TORL = 1
TYPE_URL = {
    "comment" : "https://m.weibo.cn/api/comments/show?id=%s&page=%d",
    "repost" : "https://m.weibo.cn/api/statuses/repostTimeline?id=%s&page=%d",
    "like" : "https://m.weibo.cn/api/attitudes/show?id=%s&page=%d"
}
base_dir = "D:/work/spider/kemowb/"
head_dir = base_dir + "heads/"
info_dir = base_dir + "infos/"
cookie = {"Cookie": "ALF=1519909430; SCF=Ag7WAWXq6Zx_fi-6imcy2besbl_eO4pJnIOFELxCLWlV_5Q8_9OuNpb9w4wkaN53s_9s0zr-YZebui3W0dOUW2E.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhvQRSX9UM3aV-rOEsh7Dph5JpX5K-hUgL.FozReo-N1Ke7Soe2dJLoIpYLxKnL12BLBoMLxKBLB.eL122LxKqL1KnL12HkeKn4; SUB=_2A253dA1RDeThGeRG6VcW-S3MzT-IHXVUlpMZrDV6PUJbkdANLXHmkW1NTczUO0H0LINW09hWYCnFL_w_Dqk_ZmOI; SUHB=0V51bfV43P_0rp; SSOLoginState=1517321489"}  # 将your cookie替换成自己的cookie

if __name__ == "__main__":
    # choose one user
    uid = "1878650541"
    print("start catch user %s ..." % uid)
    info_file_path = "%s%s.txt" % (info_dir, uid)

    # get_user_info(uid, info_file_path)
    # get_index_info(uid, info_file_path)
    get_detail_info(uid, info_file_path)



