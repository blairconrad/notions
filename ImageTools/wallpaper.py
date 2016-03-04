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


def findNewSize(imageSize, screenSizes):
    image_aspect = 1.0 * imageSize[0] / imageSize[1]

    bestScreen = screenSizes[0]
    bestAspect = 1.0 * bestScreen[0] / bestScreen[1]

    for screensize in screenSizes[1:]:
        screen_aspect = 1.0 * screensize[0] / screensize[1]
        output('image_aspect:', image_aspect,
               'bestAspect:', bestAspect,
               'screen_aspect:', screen_aspect)
        if abs(bestAspect - image_aspect) > abs(screen_aspect - image_aspect):
            bestAspect = screen_aspect
            bestScreen = screensize

    if bestAspect < image_aspect:
        # screen is skinny, so fit to width
        return ((bestScreen[0], int(bestScreen[0] / image_aspect)), bestScreen)
    else:
        # screen is fat, so fit to height
        return ((int(image_aspect * bestScreen[1]), bestScreen[1]), bestScreen)
        

def getScreenSizes():
    SM_CMONITORS = 80
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1
    number_of_monitors = ctypes.windll.user32.GetSystemMetrics(SM_CMONITORS)
    width = ctypes.windll.user32.GetSystemMetrics(SM_CXSCREEN)
    height = ctypes.windll.user32.GetSystemMetrics(SM_CYSCREEN)
    sizes = []

    # assume monitors are all same size
    # assume monitors are laid out horizontally
    sizes = []
    for i in range(number_of_monitors, 0, -1):
        if number_of_monitors % i == 0:
            sizes.append((i * width, height))
    output('candidate screen sizes:', sizes)
    return sizes


def areColorsAllSame(im, startPosition, increment, numPixels):
    max_color_diff = 20

    firstpixel = im.getpixel(startPosition)
    for y in range(1, numPixels):
        pix = im.getpixel((startPosition[0] + y * increment[0],
                          startPosition[1] + y * increment[1]))
        diff = (abs(pix[0] - firstpixel[0]) +
                abs(pix[1] - firstpixel[1]) +
                abs(pix[2] - firstpixel[2]))
        if diff > max_color_diff:
            output('colour diff: ', diff)
            return False
    return True


def fitImage(im, screenSizes):
    (new_size, screensize) = findNewSize(im.size, screenSizes)
    output('new_size =', str(new_size))
    
    resized_image = im.resize(new_size, Image.BICUBIC)

    new_position = ((0, 0))
    background_colour = (0, 0, 0)

    if screensize[0] > new_size[0]:
        # there's a band on the left, and probably right

        left_all_same = areColorsAllSame(im, (0, 0),
                                         direction_down, im.size[1])
        right_all_same = areColorsAllSame(im, (im.size[0] - 1, 0),
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

        bottom_all_same = areColorsAllSame(im, (0, im.size[1] - 1),
                                           direction_right, im.size[0])
        top_all_same = areColorsAllSame(im, (0, 0),
                                        direction_right, im.size[0])

        if top_all_same and not bottom_all_same:
            output('float down')
            background_colour = im.getpixel((0, 0))
            new_position = ((0, screensize[1] - resized_image.size[1]))
        else:
            output('float up')
            if bottom_all_same:
                background_colour = im.getpixel((0, im.size[1] - 1))

    new_image = Image.new('RGB', screensize, background_colour)

    new_image.paste(resized_image, (new_position[0], new_position[1],
                                    new_position[0] + new_size[0],
                                    new_position[1] + new_size[1]))
    return new_image


def getFile(dir):
    files = os.listdir(dir)

    month_number = '%02d' % (datetime.date.today().month)

    if 'month' + month_number in files:
        output('found month', month_number)
        if random.random() < 0.25:
            output('using files from month', month_number)
            return getFile(os.path.join(dir, 'month' + month_number))

    if 'current.bmp' in files:
        files.remove('current.bmp')
        
    if 'current.txt' in files:
        files.remove('current.txt')
        
    if 'Thumbs.db' in files:
        files.remove('Thumbs.db')

    output('files length:', len(files))

    # chop out the month dirs, by assuming everything else will have a .
    files = [f for f in files if '.' in f]
    output('files length:', len(files))
    output('choosing from', files)
    return os.path.join(dir, random.choice(files))


logonScreenDimensions = [
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


def changeLogonBackground(image, screenSize):
    # change the logon UI background if on Windows 7. From learning at
    # http://www.withinwindows.com/2009/03/15/windows-7-to-officially-support-logon-ui-background-customization/
    windowsVersion = sys.getwindowsversion()
    if windowsVersion.major != 6 or \
       windowsVersion.minor != 1:  # Windows 7
        return

    desiredRatio = float(screenSize[0]) / screenSize[1]
    output('Changing logon background. desiredRatio=', desiredRatio)

    for possibleScreenSize in logonScreenDimensions:
        possibleRatio = float(possibleScreenSize[0]) / possibleScreenSize[1]

        if possibleRatio == desiredRatio:
            image = fitImage(image, [possibleScreenSize])
            logonBackgroundDir = \
                r'%(windir)s\system32\oobe\info\backgrounds' % os.environ

            if not os.path.exists(logonBackgroundDir):
                os.makedirs(logonBackgroundDir)
            
            logonBackgroundPath = os.path.join(logonBackgroundDir,
                                               'background%dx%d.jpg'
                                               % possibleScreenSize)
            output('path for logon screen background =', logonBackgroundPath)
            quality = 80
            while quality >= 50:
                output('saving logon picture at quality', quality)
                image.save(logonBackgroundPath, 'JPEG', quality=quality)
                fileSize = os.path.getsize(logonBackgroundPath)
                output('file size is', fileSize)
                if fileSize < 256 * 1024:
                    break
                quality -= 5
            return
        

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

    (options, args) = parser.parse_args(args)

    global verbose
    verbose = options.verbose
    
    if len(args) > 0:
        locationArg = args[0]
        if os.path.isdir(locationArg):
            theFile = getFile(locationArg)
        elif os.path.isfile(locationArg):
            theFile = locationArg
        else:
            file_choices = glob.glob(locationArg)
            output('available files', file_choices)
            theFile = random.choice(file_choices)
    else:
        theFile = getFile(source_dir)

    output('chose', theFile)

    i = Image.open(theFile)

    screenSizes = getScreenSizes()
    scaledImage = fitImage(i, screenSizes)

    filter_it = random.random()
    while filter_it < filter_chance:
        filter = random.choice(filters)
        scaledImage = filter.filter(scaledImage)
        
        filter_it = random.random()

    scaledImage.save(destination)

    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 1
    SPIF_SENDWININICHANGE = 2

    result = ctypes.windll.user32.SystemParametersInfoA(
        SPI_SETDESKWALLPAPER, 0, destination,
        SPIF_SENDWININICHANGE | SPIF_UPDATEINIFILE)
    output('change wallpaper return code:', result)

    file(audit, 'w').write(theFile)

    changeLogonBackground(i, screenSizes[-1])
    
if __name__ == '__main__':
    sys.exit(main())
