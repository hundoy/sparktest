#!/usr/bin/env python
# -*- coding: UTF-8 -*-


def tilemap_get_at_pixel(mapid, param, param1):
    return 1


if __name__=="__main__":
    mapid=""
    pw = 48
    ph = 48
    tw = 24
    th = 24

    dir_x = 1
    dir_y = 1

    # 1. get a line
    # a line define. dir=v/h, direction (ox,oy) is start point.
    line_ox = 50
    line_oy = 52
    line_len = ph

    line_ox_h = 3
    line_oy_h = 99
    line_len_h = pw

    # 2. get next tile edge ( /and* to a line)
    edge_ox = 0
    edge_oy = 0
    if dir_x > 0:
        edge_ox = (line_ox/tw+1)*tw
        edge_oy = line_oy
    elif dir_x < 0:
        edge_ox = line_ox/tw*tw - 1
        edge_oy = line_oy

    # 3. get all the tiles a_edge cross
    tiles = []
    edge_dy = edge_oy + line_len - 1
    tile_count = edge_dy/th-edge_oy/th+1
    for i in range(0, tile_count):
        tile = tilemap_get_at_pixel(mapid, edge_ox, edge_oy + i*th)
        tiles.append(tile)

    # 4. get valid move distance to the edge
    valid_move_x = 0
    if dir_x>0:
        valid_move_x = edge_ox - line_ox - 1
    elif dir_x<0:
        valid_move_x = line_ox - edge_ox - 1

    # 4. check whether all they are enable to pass
    can_pass = True
    for tile in tiles:
        if tile>0:
            can_pass = False
            break


