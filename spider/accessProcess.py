#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
import urllib
import urllib2

import re
import requests
import time

# import sys
# sys.path.append('ip2region-master/binding/python')
from ip2Region import Ip2Region

def getiploc(ip):
    url = "https://freeapi.ipip.net/%s" % ip
    str = requests.get(url).content
    arr = str.split(",")
    return {"country":arr[0].replace("\"","").replace("[",""),"province":arr[1].replace("\"", ""), "city":arr[2].replace("\"", "")}
    # j = json.loads(str)
    # prov = j["data"]["region"]
    # city = j["data"]["city"]
    # return {"province":prov, "city":city}
    # print(str)
    # req = urllib2.Request(url)
    # res_data = urllib2.urlopen(req)
    # res = res_data.read()
# {"code":0,"data":{"ip":"193.112.3.225","country":"中国","area":"","region":"广东","city":"广州","county":"XX","isp":"电信","country_id":"CN","area_id":"","region_id":"440000","city_id":"440100","county_id":"xx","isp_id":"100017"}}


if __name__=="__main__":



    # print res
    log_dir = "logdata/"
    paths = ["display_detail_access.log", "nodata_access.log", "display_access.log"]
    out_path = "rs_data.txt"
    before_time_format = "%d/%b/%Y:%H:%M:%S"
    after_time_format = "%Y-%m-%d %H:%M:%S"
    header = "uid,page,ip,country,province,city,access_time"
    block_size = 100
    lines = []

    dbFile = "ip2region-master/data/ip2region.db"
    searcher = Ip2Region(dbFile);

    with open(log_dir + out_path, 'w') as of:
        of.write(header+"\n".encode('utf-8'))

    # lines = []
    # ip = "193.112.3.225"
    # data = getiploc(ip)
    # province = data["province"]
    # city = data["city"]
    # line = "%s,%s,%s" % (ip, province, city)
    # lines.append(line)
    # ip = "45.76.49.112"
    # data = getiploc(ip)
    # province = data["province"]
    # city = data["city"]
    # line = "%s,%s,%s" % (ip, province, city)
    # lines.append(line)
    # with open(log_dir + out_path, 'a') as of:
    #     of.write(("\n".join(lines) + "\n"))
    # exit(0)

    line_cnt = 0

    for path in paths:
        with open(log_dir+path, 'r') as f:
            for line in f:
                arr = line.split(" ")
                if len(arr)<10: continue

                ip = arr[0]
                rs = re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}', line);
                if rs is None: continue

                line_time = arr[3]
                url = arr[6]
                status = arr[8]
                if status!="200": continue

                access_time = time.strptime(line_time[1:], before_time_format)
                access_time_str = time.strftime(after_time_format, access_time)
                page = url[url.rfind("/") + 1: url.rfind(".")]
                uid = ""
                if page != "display":
                    uid = url[url.rfind("=") + 1:]
                    uidrs = re.match(r'^\d+$', uid)
                    if uidrs is None: continue

                # pc = getiploc(ip)
                data = searcher.binarySearch(line)
                region = data["region"]
                rarr = region.split("|")
                country = str(rarr[0])
                province = str(rarr[2])
                city = str(rarr[3])
                if province=="0" or city=="0":
                    data = getiploc(ip)
                    country = data["country"]
                    province = data["province"]
                    city = data["city"]
                else:
                    province = province.decode("utf-8")
                    city = city.decode("utf-8")
                    if province.endswith(u"省") or province.endswith(u"市"):
                        province = province[0:-1]
                    if city.endswith(u"省") or city.endswith(u"市"):
                        city = city[0:-1]
                    province = province.encode("utf-8")
                    city = city.encode("utf-8")

                line = "%s,%s,%s,%s,%s,%s,%s" % (uid, page, ip, country, province, city, access_time_str)
                lines.append(line)
                line_cnt += 1

                if len(lines)>=block_size:
                    with open(log_dir+out_path, 'a') as of:
                        of.write(("\n".join(lines)+"\n"))
                        print("write %d !"%line_cnt)
                        lines = []


            if len(lines)>0:
                with open(log_dir + out_path, 'a') as of:
                    of.write(("\n".join(lines) + "\n"))
                    lines = []





    print("all fin!")