#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PIL import Image
import os

if __name__ == "__main__":
    img_dir = "rs/heads_1/"
    output_dir = "rs/heads_small/"

    for img in os.listdir(img_dir):
        if str(img).endswith(".jpg"):
            try:
                img_file = Image.open(img_dir+img)
                img_file.thumbnail((64, 64))
                img_file.save(output_dir+img, "JPEG")
                print("fin process image %s" % img)
            except Exception, e:
                print("[FAIL] %s" % img)

    print("all fin!")
