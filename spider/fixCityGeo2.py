#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup

log_file = "logdata/nogeo.log"
url = "http://www.ximizi.com/JingWeiDu_Results.php"
url2 = "https://jingwei.supfree.net/"

def ximizi(city):
    params = {"jingweidu_key": city, "jwd": "经纬度查询"}
    r = requests.post(url, params)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, "lxml")
    div = soup.find_all(class_="crm_text_1")
    jmsg = ""
    wmsg = ""
    if len(div) > 0:
        msg = div[0].p.find_all("font")
        if (len(msg) >= 2):
            jmsg = msg[0].text
            wmsg = msg[1].text

    if len(jmsg) == 0:
        print("no data for %s" % city)
        return ""
    else:
        jmsg = jmsg.encode("utf-8").replace("经度：", "")
        wmsg = wmsg.encode("utf-8").replace("纬度：", "")
        rs = "'%s': [%s,%s]," % (city, jmsg, wmsg)
        return rs


def supfree():
    city_dict = {}
    r = requests.get(url2)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, "lxml")
    ulinks = soup.find_all("p", class_="ulink")
    if len(ulinks)>0:
        for ulink in ulinks:
            citys = ulink.find_all("a")
            if len(citys)>0:
                for city in citys:
                    city_link = city['href']
                    city_name = city.text
                    #print("%s %s" % (city_name, city_link))
                    city_dict[city_name] = city_link
            else:
                print("no citys!")
    else:
        print("no ulinks!")

    return city_dict

def supfreeSecond(name, second):
    page_url = url2+second
    r = requests.get(page_url)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text, "lxml")
    ul = soup.find_all("ul", class_="oul")
    if len(ul)>0:
        city_link = ul[0].li.a['href']

        real_page_url = url2+city_link
        r2 = requests.get(real_page_url)
        r2.encoding = 'gb2312'
        soup2 = BeautifulSoup(r2.text, "lxml")
        jw = soup2.select("span.bred.botitle18")
        if len(jw)>=2:
            jmsg = jw[0].text.strip()
            wmsg = jw[1].text.strip()
            rs = "'%s': [%s,%s]," % (name, jmsg, wmsg)
            return rs

    print("get error for %s"%name)


if __name__=="__main__":
    city_dict = supfree()
    lines = []
    with open(log_file, 'r') as lf:
        for line in lf:
            if line.startswith("no geo for"):
                city = line[11:].strip("\r").strip("\n").decode("utf-8")
                print(city)
                rs = ""
                real_city = city
                if not city_dict.has_key(city):
                    if city_dict.has_key(city+u"市"):
                        real_city = city+u"市"
                    else:
                        rs = ximizi(city)
                        if len(rs)==0:
                            print("no city data %s" % city)
                        else:
                            lines.append(rs)
                        continue

                second = city_dict[real_city]
                rs = supfreeSecond(city, second)
                lines.append(rs)

        print("\n".join(lines))

    # print(supfreeSecond('','kongzi.asp?id=3133'))
