import json
import os
from glob import glob
from typing import Any

import click
import numpy as np
from PIL import Image


def rleToMask(maskRLE: list[int], shape: tuple[int, int], save_dir: str, imgName: str) -> None:
    """Function to convert Run-Length-Encoded Binary Mask Array to PNG

    Args:
        maskRLE (list[int]): RLE Binary Mask Array
        shape (tuple[int, int]): Shape of Input & Output
        save_dir (str): Save Directory
        imgName (str): Image/Mask name
    """
    click.secho(message=f"Converting {imgName} 🚀", fg="blue")

    H, W = shape

    rlePairs = np.array(maskRLE).reshape(-1, 2)

    mask = np.zeros(H * W, dtype=np.uint8)

    currIdx = 0
    for isMask, length in rlePairs:
        mask[currIdx : currIdx + length] = 255 if isMask else 0
        currIdx += length

    reshapedMask = mask.reshape(shape).T

    finalMask = (
        Image.fromarray(reshapedMask)
        .transpose(Image.FLIP_LEFT_RIGHT)
        .rotate(90, Image.Resampling.BILINEAR, expand=True)
        .resize((W, H))
    )

    finalMask.save(f"{save_dir}/{imgName}_mask.png")

    return


@click.command()
@click.option(
    "-M",
    "--mask-dir",
    prompt="Mask Directory",
    type=str,
    required=True,
    help="Directory with Masks as JSON files",
)
@click.option(
    "-S",
    "--save-dir",
    prompt="Save Directory",
    type=str,
    required=True,
    help="Directory to save PNG Masks in",
)
def main(mask_dir: str, save_dir: str) -> None:
    """Utility script to convert Darwin 2.0 JSON Binary Masks from [V7Labs](https://www.v7labs.com/) to PNG. The masks should be Run-Length-Encoded and the JSON document should be following the Darwin 2.0 JSON Format. [Refer here](https://docs.v7labs.com/reference/darwin-json).

    Args:
        mask_dir (str): Mask Directory with Darwin 2.0 JSON files.
        save_dir (str): Saving Directory for PNG Masks.

    Raises:
        OSError: In the event that provided directory does not exist.
    """
    if not os.path.exists(mask_dir):
        raise OSError(f"Provided Directory ({mask_dir}) does not exist")

    masks: list[str] = sorted(glob(os.path.join(mask_dir, "*.json")))

    if not masks:
        raise OSError(f"No RLE JSON masks in the provided directory, {mask_dir}")

    os.makedirs(save_dir, exist_ok=True)

    for mask_path in masks:
        with open(mask_path) as f:
            data: Any = json.load(f)
            imgName: str = os.path.split(mask_path)[1].split(".")[0]

        width: int = data["item"]["slots"][0]["width"]
        height: int = data["item"]["slots"][0]["height"]
        shape: tuple[int, int] = (height, width)

        if not data["annotations"]:
            click.secho(message=f"Saving {imgName} 🚀", fg="blue")
            img = Image.new(mode="L", size=(width, height))
            img.save(f"{save_dir}/{imgName}_mask.png")
            continue

        try:
            maskRLE: list[int] = data["annotations"][0]["raster_layer"]["dense_rle"].copy()
        except KeyError as _:
            maskRLE: list[int] = data["annotations"][1]["raster_layer"]["dense_rle"].copy()

        rleToMask(maskRLE=maskRLE, shape=shape, save_dir=save_dir, imgName=imgName)

    click.secho(message="👍 Done", fg="green")

    return


if __name__ == "__main__":
    main()
