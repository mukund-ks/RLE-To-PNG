import json
import os
from glob import glob

import numpy as np
from PIL import Image

MASK_DIR = "Data"


def rleToMask(maskRLE, shape, saveDir, imgName):
    H, W = shape

    RLEpairs = np.array(maskRLE).reshape(-1, 2)

    mask = np.zeros(H * W, dtype=np.uint8)

    currIdx = 0
    for isMask, length in RLEpairs:
        if isMask == 1:
            mask[currIdx : currIdx + length] = 255
        else:
            mask[currIdx : currIdx + length] = 0

        currIdx += length

    mask_reshaped = mask.reshape(shape).T

    final_mask = (
        Image.fromarray(mask_reshaped)
        .transpose(Image.FLIP_LEFT_RIGHT)
        .rotate(90, Image.Resampling.BILINEAR, expand=True)
        .resize((W, H))
    )

    final_mask.save(f"{saveDir}/{imgName}_mask.png")


def main():
    masks = sorted(glob(os.path.join(MASK_DIR, "*.json")))

    saveDir = "Mask"

    os.makedirs(saveDir, exist_ok=True)

    for mask_path in masks:
        with open(mask_path) as f:
            data = json.load(f)
            imgName = os.path.split(mask_path)[1].split(".")[0]

        width = data["item"]["slots"][0]["width"]
        height = data["item"]["slots"][0]["height"]
        shape = (height, width)
        maskRLE = data["annotations"][0]["raster_layer"]["dense_rle"].copy()

        rleToMask(maskRLE=maskRLE, shape=shape, saveDir=saveDir, imgName=imgName)


if __name__ == "__main__":
    main()
