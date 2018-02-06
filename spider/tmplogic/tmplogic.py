#!/usr/bin/env python
# -*- coding: UTF-8 -*-


if __name__=="__main__":
    pw = 48
    ph = 48
    tw = 24
    th = 24

    # 1. get a line
    # a line define. dir=v/h, direction (ox,oy) is start point.
    a_line = {"ox":50, "oy":52, "len":ph, "dir":"v"}

    # 2. get next tile edge ( /and* to a line)
    dir_x = 1
    dir_y = 0
    a_edge = {}
    if dir_x > 0:
        a_edge = {"ox":(a_line["ox"]/tw+1)*tw, "oy": a_line["oy"], "len":ph, "dir":"v"}

    # 3. get all the tiles a_edge cross
    tiles = []
    oy = a_edge["oy"]
    dy = oy + a_edge["len"] - 1
    oi = oy/th
    di = dy/th
    tile_count = di-oi+1
    

    # 4. check whether all they are enable to pass



