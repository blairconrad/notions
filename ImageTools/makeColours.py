#!/usr/bin/env python

import sys
import colorsys
import Image
import Image_draw
import Image_font


def make_colours(num_hues, num_vals):
    results = []
    for h in range(num_hues):
        values = []
        for v in range(num_vals):
                this_val = float(v + 1) / (num_vals)
                this_hue = 1.0 * h / num_hues
                this_sat = 0.25
                (r, g, b) = colorsys.hsv_to_rgb(this_hue, this_sat, this_val)
                values.append((min(255, int(256 * r)), min(255, int(256 * g)), min(255, int(256 * b))))
        results.append(values)
    return results


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    default_colour = '#FFFFF0'

    block_size = 60
    num_hues = 3
    num_vals = 20

    colours = make_colours(num_hues, num_vals)
    print colours

    font = Image_font.truetype('verdana.ttf', 10)

    im = Image.new('RGB', (2 * len(colours) * block_size, len(colours[0]) * block_size), default_colour)

    for i in range(len(colours)):
        for j in range(len(colours[i])):
            block = Image.new('RGB', (block_size, block_size), colours[i][j])
            im.paste(block, (i * block_size, j*block_size, (i+1) * block_size, (j+1) * block_size))

    draw = Image_draw.Draw(im)
    for i in range(len(colours)):
        for j in range(len(colours[i])):
            draw.text((i * block_size, j*block_size), ' #%02X%02X%02X' % colours[i][j], fill=default_colour, font=font)

    for i in range(len(colours)):
        for j in range(len(colours[i])):
            block = Image.new('RGB', (block_size, block_size), default_colour)
            im.paste(
                block,
                (block_size * len(colours) + i * block_size,
                 j*block_size,
                 block_size * len(colours) + (i+1) * block_size,
                 (j+1) * block_size))

    draw = Image_draw.Draw(im)
    for i in range(len(colours)):
        for j in range(len(colours[i])):
            draw.text(
                (block_size * len(colours) + i * block_size,  j*block_size),
                ' #%02X%02X%02X' % colours[i][j], fill=colours[i][j], font=font)

    im.show()

    make_colours(3, 3)
    return 0


if __name__ == '__main__':
    sys.exit(main())
