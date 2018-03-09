#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

log_file = "logdata/nogeo.log"
url = "http://www.ximizi.com/JingWeiDu_Results.php"

if __name__=="__main__":
    lines = []
    with open(log_file, 'r') as lf:
        for line in lf:
            if line.startswith("no geo for"):
                city = line[11:].strip("\r").strip("\n")
                print(city)
                params = {"jingweidu_key": city, "jwd": "经纬度查询"}
                r = requests.post(url, params)
                r.encoding = 'utf-8'
                soup = BeautifulSoup(r.text, "lxml")
                div = soup.find_all(class_="crm_text_1")
                jmsg = ""
                wmsg = ""
                if len(div)>0:
                    msg = div[0].p.find_all("font")
                    if (len(msg)>=2):
                        jmsg = msg[0].text
                        wmsg = msg[1].text

                if len(jmsg)==0:
                    print("no data for %s" % city)
                else:
                    jmsg = jmsg.encode("utf-8").replace("经度：","")
                    wmsg = wmsg.encode("utf-8").replace("纬度：","")
                    rs = "'%s': [%s,%s]," % (city, jmsg, wmsg)
                    lines.append(rs)

        print("\n".join(lines))
