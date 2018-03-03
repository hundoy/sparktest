#!/usr/bin/env python
# -*- coding: UTF-8 -*-

#The list of lists
import time

list_of_lists = [range(4), range(7)]

#flatten the lists
flattened_list = [y for x in list_of_lists for y in x]

print(flattened_list)

arr_str = ""

before_time_format = "%d/%b/%Y:%H:%M:%S"
after_time_format = "%Y-%m-%d %H:%M:%S"

line_time = "[16/Feb/2018:14:46:37"
url = "/pages/display_detail.html?uid=1273750617"

access_time = time.strptime(line_time[1:], before_time_format)
access_time_str = time.strftime(after_time_format, access_time)
page = url[url.rfind("/") + 1: url.rfind(".")]
uid = ""
if page != "display":
    uid = url[url.rfind("=")+1:]

print(access_time_str)
print(page)
print(uid)

str = u"辽宁省"
str2 = u"本溪市"
if (str.endswith(u"省")):
    print(str[0:-1])