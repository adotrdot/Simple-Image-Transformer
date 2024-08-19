import argparse
import cv2 as cv
import sys


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Simple Image Transformer")

    # Add the necessary arguments
    parser.add_argument(
        "-i",
        "--input",
        help="path to an image file that you want to transform",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="path which the program will save the resulting image in",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--flip",
        choices=["H", "V", "A"],
        help="flip image horizontally, vertically, or all sides",
        required=False,
    )
    parser.add_argument(
        "-r",
        "--rotate",
        metavar="ANGLE",
        type=int,
        help="rotate image with the image's center as center point",
        required=False,
    )
    parser.add_argument(
        "-s",
        "--scale",
        nargs=2,
        metavar=("HORIZONTAL_SCALE", "VERTICAL_SCALE"),
        type=int,
        help="scale image horizontally and/or vertically",
        required=False,
    )

    # Run transformer
    args = parser.parse_args()
    simple_transformer(
        input=args.input,
        output=args.output,
        flip_orientation=args.flip,
        rotate_angle=args.rotate,
        scale_xy=args.scale,
    )


def simple_transformer(
    input: str, output: str, flip_orientation: str, rotate_angle: int, scale_xy: tuple
):
    # Open image
    img = cv.imread(input)
    if img is None:
        sys.exit("Could not open input image")

    # Flip image
    if flip_orientation:
        img = flip(img, flip_orientation)

    # Rotate image
    if rotate_angle:
        img = rotate(img, rotate_angle)

    # Scale image
    if scale_xy:
        img = scale(img, *scale_xy)

    # Save image
    cv.imwrite(output, img)


def flip(img, orientation):
    match orientation:
        case "H":
            # Flip horizontally
            return cv.flip(img, 1)
        case "V":
            # Flip vertically
            return cv.flip(img, 0)
        case "A":
            # Flip all
            return cv.flip(img, -1)
        case _:
            return img


def rotate(img, angle):
    # Get center point
    height, width, _ = img.shape
    point = (height / 2, width / 2)

    # Rotate image
    rotation_matrix = cv.getRotationMatrix2D(point, angle, 1)

    return cv.warpAffine(img, rotation_matrix, (width, height))


def scale(img, scale_x, scale_y):
    # Scale image horizontally and/or vertically
    return cv.resize(img, None, fx=scale_x, fy=scale_y)


if __name__ == "__main__":
    main()
