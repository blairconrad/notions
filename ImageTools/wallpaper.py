#!/usr/bin/env python

import os
import os.path
import random
import ctypes
import sys
import glob
import datetime
import optparse

try:
    import Image
except:
    try:
        from PIL import Image
    except:
        raise Exception("Can't import PIL or PILLOW. Install one.")

verbose = False

direction_down = (0, 1)
direction_right = (1, 0)


def output(*args):
    global verbose
    if verbose:
        print ' '.join(map(str, args))


class MyFilter:
    def filter(self, i):
        pass


class GrayscaleFilter(MyFilter):
    def filter(self, i):
        return i.convert('L')


class Windows:
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 1
    SPIF_SENDWININICHANGE = 2

    SM_CMONITORS = 80
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1

    @classmethod
    def change_wallpaper(cls, new_wallpaper):
        result = ctypes.windll.user32.SystemParametersInfoA(
            Windows.SPI_SETDESKWALLPAPER, 0, new_wallpaper,
            Windows.SPIF_SENDWININICHANGE | Windows.SPIF_UPDATEINIFILE)
        output('change wallpaper return code:', result)

    @classmethod
    def get_screen_size(cls):
        width = ctypes.windll.user32.GetSystemMetrics(Windows.SM_CXSCREEN)
        height = ctypes.windll.user32.GetSystemMetrics(Windows.SM_CYSCREEN)
        return (width, height)

    @classmethod
    def get_number_of_screens(cls):
        return ctypes.windll.user32.GetSystemMetrics(Windows.SM_CMONITORS)

    @classmethod
    def is_windows_7(cls):
        windows_version = sys.getwindowsversion()
        return windows_version.major == 6 and windows_version.minor == 1


def find_new_size(image_size, candidate_sizes):
    image_aspect = 1.0 * image_size[0] / image_size[1]

    best_candidate = candidate_sizes[0]
    best_aspect = 1.0 * best_candidate[0] / best_candidate[1]
    candidate_aspect = best_aspect
    output(
        'image_aspect:', image_aspect,
        'best_aspect so far:', best_aspect,
        'candidate_aspect:', candidate_aspect)

    for candidate_size in candidate_sizes[1:]:
        candidate_aspect = 1.0 * candidate_size[0] / candidate_size[1]
        output(
            'image_aspect:', image_aspect,
            'best_aspect so far:', best_aspect,
            'candidate_aspect:', candidate_aspect)
        if abs(best_aspect - image_aspect) > abs(candidate_aspect - image_aspect):
            best_aspect = candidate_aspect
            best_candidate = candidate_size

    output('final best_aspect', best_aspect)
    if best_aspect < image_aspect:
        # candidate is skinny, so fit to width
        return ((best_candidate[0], int(best_candidate[0] / image_aspect)), best_candidate)
    else:
        # candidate is fat, so fit to height
        return ((int(image_aspect * best_candidate[1]), best_candidate[1]), best_candidate)


def get_screen_sizes():
    number_of_screens = Windows.get_number_of_screens()
    one_screen_size = Windows.get_screen_size()

    # assume monitors are all same size
    # assume monitors are laid out horizontally
    sizes = [(i * one_screen_size[0], one_screen_size[1])
             for i in range(number_of_screens, 0, -1) if number_of_screens % i == 0]
    output('candidate screen sizes:', sizes)
    return sizes


def are_colors_all_same(im, start_position, increment, num_pixels):
    max_color_diff = 20

    firstpixel = im.getpixel(start_position)
    output('firstpixel = ' + str(firstpixel))
    for y in range(1, num_pixels):
        pix = im.getpixel((
            start_position[0] + y * increment[0],
            start_position[1] + y * increment[1]))

        if isinstance(pix, tuple):
            diff = (
                abs(pix[0] - firstpixel[0]) +
                abs(pix[1] - firstpixel[1]) +
                abs(pix[2] - firstpixel[2]))
        else:
            diff = abs(pix - firstpixel)

        if diff > max_color_diff:
            output('colour diff: ', diff)
            return False
    return True


def fit_image(im, screen_sizes):
    (new_size, screensize) = find_new_size(im.size, screen_sizes)
    output('new_size =', str(new_size))

    resized_image = im.resize(new_size, Image.BICUBIC)

    new_position = ((0, 0))
    background_colour = (0, 0, 0)

    if screensize[0] > new_size[0]:
        # there's a band on the left, and probably right

        left_all_same = are_colors_all_same(im, (0, 0),
                                            direction_down, im.size[1])
        right_all_same = are_colors_all_same(im, (im.size[0] - 1, 0),
                                             direction_down, im.size[1])

        if right_all_same and not left_all_same:
            output('float left')
            background_colour = im.getpixel((im.size[0] - 1, 0))
        else:
            output('float right')
            new_position = ((screensize[0] - resized_image.size[0], 0))
            if left_all_same:
                background_colour = im.getpixel((0, 0))

    elif screensize[1] > new_size[1]:
        # there's a band at the top, and probably bottom

        bottom_all_same = are_colors_all_same(im, (0, im.size[1] - 1),
                                              direction_right, im.size[0])
        top_all_same = are_colors_all_same(im, (0, 0),
                                           direction_right, im.size[0])

        if top_all_same and not bottom_all_same:
            output('float down')
            background_colour = im.getpixel((0, 0))
            new_position = ((0, screensize[1] - resized_image.size[1]))
        else:
            output('float up')
            if bottom_all_same:
                background_colour = im.getpixel((0, im.size[1] - 1))

    new_image = Image.new(im.mode, screensize, background_colour)

    new_image.paste(resized_image,
                    (new_position[0], new_position[1],
                     new_position[0] + new_size[0], new_position[1] + new_size[1]))
    return new_image.convert('RGB')


def get_file(dir):
    files = os.listdir(dir)

    month_number = '%02d' % (datetime.date.today().month)

    if 'month' + month_number in files:
        output('found month', month_number)
        if random.random() < 0.25:
            output('using files from month', month_number)
            return get_file(os.path.join(dir, 'month' + month_number))

    if 'current.bmp' in files:
        files.remove('current.bmp')

    if 'current.txt' in files:
        files.remove('current.txt')

    if 'Thumbs.db' in files:
        files.remove('Thumbs.db')

    files = [f for f in files if not f.endswith('.json')]

    output('files length:', len(files))

    # chop out the month dirs, by assuming everything else will have a .
    files = [f for f in files if '.' in f]
    output('files length:', len(files))
    output('choosing from', files)
    return os.path.join(dir, random.choice(files))


logon_screen_dimensions = [
    (1360, 768),
    (1280, 768),
    (1920, 1200),
    (1440, 900),
    (1600, 1200),
    (1280, 960),
    (1024, 768),
    (1280, 1024),
    (1024, 1280),
    (960, 1280),
    (900, 1440),
    (768, 1280),
]


def change_logon_background(image, screen_size):
    # change the logon UI background if on Windows 7. From learning at
    # http://www.withinwindows.com/2009/03/15/windows-7-to-officially-support-logon-ui-background-customization/
    if not Windows.is_windows_7():
        return

    desired_ratio = float(screen_size[0]) / screen_size[1]
    output('Changing logon background. desired_ratio=', desired_ratio)

    for possible_screen_size in logon_screen_dimensions:
        possible_ratio = float(possible_screen_size[0]) / possible_screen_size[1]

        if possible_ratio == desired_ratio:
            image = fit_image(image, [possible_screen_size])
            logon_background_dir = \
                r'%(windir)s\system32\oobe\info\backgrounds' % os.environ

            if not os.path.exists(logon_background_dir):
                os.makedirs(logon_background_dir)

            logon_background_path = os.path.join(logon_background_dir,
                                                 'background%dx%d.jpg'
                                                 % possible_screen_size)
            output('path for logon screen background =', logon_background_path)
            quality = 80
            while quality >= 50:
                output('saving logon picture at quality', quality)
                image.save(logon_background_path, 'JPEG', quality=quality)
                file_size = os.path.getsize(logon_background_path)
                output('file size is', file_size)
                if file_size < 256 * 1000:
                    break
                quality -= 5
            return


def choose_wallpaper_file(source_dir, args):
    if len(args) > 0:
        location_arg = args[0]
        if os.path.isdir(location_arg):
            the_file = get_file(location_arg)
        elif os.path.isfile(location_arg):
            the_file = location_arg
        else:
            file_choices = glob.glob(location_arg)
            output('available files', file_choices)
            the_file = random.choice(file_choices)
    else:
        the_file = get_file(source_dir)

    output('chose', the_file)
    return the_file


def main(args=None):
    filter_chance = 0.10
    filters = [GrayscaleFilter()]

    try:
        source_dir = r'%(HOME)s\..\Documents\Dropbox\Pictures\wallpapers' % os.environ
    except:
        source_dir = os.getcwd()
        output('No HOME environment variable defined. Will use ',
               source_dir, ' for generated files.')

    if not os.path.exists(source_dir):
        os.makedirs(source_dir)

    destination = os.path.join(source_dir, 'current.bmp')
    audit = os.path.join(source_dir, 'current.txt')

    if args is None:
        args = sys.argv[1:]

    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose',
                      action='store_true', dest='verbose', default=False)
    parser.add_option('--region',
                      action='store', dest='region', default=None)
    parser.add_option('--create-config',
                      action='store_true', dest='create_config', default=None)

    (options, args) = parser.parse_args(args)

    global verbose
    verbose = options.verbose

    the_file = choose_wallpaper_file(source_dir, args)

    i = Image.open(the_file)
    output('image size is', i.size)

    original_region = region = [0, 0] + list(i.size)

    config_file = the_file + '.json'
    if options.create_config:
        if os.path.exists(config_file):
            print 'File', config_file, 'already exists'
        else:
            sample_config = {
                'regions': [original_region]
                }
            import json
            json.dump(sample_config, file(config_file, 'wb'), sort_keys=True, indent=4)
            print 'Created config file', config_file
        return

    if options.region:
        region = [int(part, 10) for part in options.region.split(',')]
    else:
        if os.path.isfile(config_file):
            import json
            config = json.load(file(config_file))
            region = config["regions"][0]

    if region != original_region:
        output('cropping to', region)
        i = i.crop(region)

    screen_sizes = get_screen_sizes()
    scaled_image = fit_image(i, screen_sizes)

    filter_it = random.random()
    while filter_it < filter_chance:
        filter = random.choice(filters)
        scaled_image = filter.filter(scaled_image)

        filter_it = random.random()

    scaled_image.save(destination)

    Windows.change_wallpaper(destination)

    file(audit, 'w').write(the_file)

    change_logon_background(i, screen_sizes[-1])

if __name__ == '__main__':
    sys.exit(main())
