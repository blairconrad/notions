#!/usr/bin/env python

import sys
import colorsys
import Image
import ImageDraw
import ImageFont

def makeColours(numHues, numVals):
    results = []
    for h in range(numHues):
        values = []
        for v in range(numVals):
                this_val = float(v + 1) / (numVals)
                this_hue = 1.0 * h / numHues
                this_sat = 0.25
                (r, g, b) = colorsys.hsv_to_rgb(this_hue, this_sat, this_val)
                #print this_val, this_hue, this_sat, r, g, b, author, versions[index]
                values.append((min(255, int(256 * r)), min(255, int(256 * g)), min(255, int(256 * b))))
        results.append(values)
    return results

def main(args=None):
    if args == None:
        args = sys.argv[1:]

    defaultColour = '#FFFFF0'

    blockSize= 60
    numHues = 3
    numVals = 20

    colours = makeColours(numHues, numVals)
    print colours

    font = ImageFont.truetype('verdana.ttf', 10);

    im = Image.new('RGB', (2 * len(colours) * blockSize, len(colours[0]) * blockSize), defaultColour)

    for i in range(len(colours)):
        for j in range(len(colours[i])):
            block = Image.new('RGB', (blockSize, blockSize), colours[i][j])
            im.paste(block, (i * blockSize, j*blockSize, (i+1) * blockSize, (j+1) * blockSize))

    draw = ImageDraw.Draw(im)
    for i in range(len(colours)):
        for j in range(len(colours[i])):
            draw.text((i * blockSize, j*blockSize), ' #%02X%02X%02X' % colours[i][j], fill=defaultColour, font=font)

    for i in range(len(colours)):
        for j in range(len(colours[i])):
            block = Image.new('RGB', (blockSize, blockSize), defaultColour)
            im.paste(block, (blockSize * len(colours) + i * blockSize, j*blockSize, blockSize * len(colours) + (i+1) * blockSize, (j+1) * blockSize))

    draw = ImageDraw.Draw(im)
    for i in range(len(colours)):
        for j in range(len(colours[i])):
            draw.text((blockSize * len(colours) + i * blockSize,  j*blockSize), ' #%02X%02X%02X' % colours[i][j], fill=colours[i][j], font=font)

    im.show()
    
                  
    
    makeColours(3,3)
    return 0


if __name__ == '__main__':
    sys.exit(main())

