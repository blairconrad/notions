#!/usr/bin/env python

import sys
import Image
import ImageDraw
import ImageFont
import hippo


def center(object, canvas):
    return ((canvas[0]-object[0])/2, (canvas[1]-object[1])/2)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = hippo.OptionParser()
    parser.add_option('--output', action='store',
                      help='File name to write output to. If unspecified, image will be shown.')
    parser.add_option('--background-colour', action='store', metavar='COLOUR', default='rgb(58, 110, 165)')
    parser.add_option('--width', action='store', type='int', default=800)
    parser.add_option('--height', action='store', type='int', default=600)
    parser.add_option('--title-font-size', action='store', type='int', default=48)
    parser.add_option('--title-font', action='store', default='georgia')
    parser.add_option('--title-colour', action='store', default='white')
    parser.add_option('--subtitle-font-size', action='store', type='int', default=16)
    parser.add_option('--subtitle', action='store', type='string', default=None)
    parser.add_option('--subtitle-font', action='store', default='georgia')
    parser.add_option('--subtitle-colour', action='store', default='white')
    (options, args) = parser.parse_args(args)

    image_size = (options.width, options.height)
    shadow_offset = 3
    shadow_colour = 'black'

    title = ' '.join(args)
    title_font = ImageFont.truetype(options.title_font + '.ttf', options.title_font_size)

    i = Image.new('RGB', image_size, color=options.background_colour)

    d = ImageDraw.Draw(i)
    title_text_size = d.textsize(title, font=title_font)

    if options.subtitle:
        subtitle_font = ImageFont.truetype(options.subtitle_font + '.ttf', options.subtitle_font_size)
        subtitle_text_size = d.textsize(options.subtitle, font=subtitle_font)

        subtitle_left_offset = (i.size[0]-subtitle_text_size[0])/2
        title_box_top_offset = (i.size[1] - title_text_size[1] - subtitle_text_size[1] - subtitle_text_size[1]/2)/2

        subtitle_pos = (subtitle_left_offset, title_box_top_offset + title_text_size[1] + subtitle_text_size[1]/2)

        d.text((subtitle_pos[0]+shadow_offset, subtitle_pos[1]+shadow_offset),
               options.subtitle, font=subtitle_font, fill=shadow_colour)
        d.text(subtitle_pos, options.subtitle, font=subtitle_font, fill=options.title_colour)

        pos = ((i.size[0] - title_text_size[0])/2, title_box_top_offset)
    else:
        pos = center(title_text_size, i.size)
    d.text((pos[0]+shadow_offset, pos[1]+shadow_offset), title, font=title_font, fill=shadow_colour)
    d.text(pos, title, font=title_font, fill=options.title_colour)

    if options.output:
        i.save(options.output)
    else:
        i.show()
    return 0


if __name__ == '__main__':
    sys.exit(main())
