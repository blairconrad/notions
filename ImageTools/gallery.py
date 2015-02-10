#!/usr/bin/env python

import sys, os, getopt, glob
try:
    from PIL import Image
except ImportError:
    print >>sys.stderr, ("Unable to import PIL.Image; "
                         "is the Python Imaging Library installed?")
    sys.exit(0)

__version__ = '1.01'
__doc__ = """%s [option] file1 file2
Options:
  --help 	    Display this usage message
  --html            Output HTML to stdout
  --resize x y      Resize specified images to x,y
  --size            Display the image sizes
  --thumbnail x y   Make thumbnails of specified images, ignoring existing
                    thumbnails that happen to be listed among the files.

If a filename is of the form *_thumb.*, it's assumed to be a thumbnail.

""" % sys.argv[0]

def is_thumbnail (filename):
    "Returns true if the filename is for a thumbnail"
    root, ext = os.path.splitext(filename)
    return root.endswith('_thumb')

def thumbnail_name (filename):
    """Return the thumbnail form of a filename,
    converting foo.jpg to foo_thumb.jpg.
    """
    assert not is_thumbnail(filename)
    root, ext = os.path.splitext(filename)
    return root + '_thumb' + ext
    
def output_html (args):
    for filename in args:
        if is_thumbnail(filename): continue
        thumbnail = thumbnail_name(filename)

        if not os.path.exists(thumbnail):
            print >>sys.stderr, ("%s: thumbnail %s doesn't exist" %
                                 (sys.argv[0], thumbnail) )
            
        im = Image.open(thumbnail)
        width, height = im.size
        
        print ('<a href="%s"><img src="%s" width="%i" height="%i"></a><br>'
               % (filename, thumbnail, width, height) )

def make_thumbnails (args):
    x, y = int(args[0]), int(args[1])
    args = args[2:] ; args.sort()
    
    for filename in args:
        if is_thumbnail(filename): continue
        thumbnail = thumbnail_name(filename)

        print >>sys.stderr, filename
        im = Image.open(filename)
        im.thumbnail((x,y))
        im.save(thumbnail)
        
def resize_images (args):
    x, y = int(args[0]), int(args[1])
    args = args[2:] ; args.sort()
    for filename in args:
        im = Image.open(filename)
        w,h = im.size
        im2 = im.resize((x,y))
        print >>sys.stderr, ('%s: was %i,%i; resizing to %i,%i'
                             % (filename, w,h, x,y) )
        im2.save(filename)

def glob_args(the_args):
    result = []
    for thing in the_args:
        result.extend(glob.glob(thing))
    return result
    

def main ():
    opts, args = getopt.getopt(sys.argv[1:],
                               'h',
                               ['help',
                                'html',
                                'resize',
                                'size',
                                'thumbnail'])

    # Remove the unused option arguments
    opts = [opt for opt,arg in opts]

    # Print usage message if requested
    if '-h' in opts or '--help' in opts:
        print >>sys.stderr, __doc__
        sys.exit(0)

    # Ensure that exactly one option is supplied
    if len(opts) == 0:
        print >> sys.stderr, ("%s: must specify one of --size, --help"
                              "\n            --html, --resize, --thumbnail" %
                              sys.argv[0] )
        sys.exit(0)
    elif len(opts) > 1:
        print >> sys.stderr, ("%s: cannot specify multiple options" %
                              sys.argv[0] )
        sys.exit(0)

    # Perform each of the possible actions
    opt = opts[0]
    if opt == '--html':
        output_html(glob_args(args))
    elif opt == '--resize':
        resize_images(args[0:2] + glob_args(args[2:]))
    elif opt == '--size':
        for filename in glob_args(args):
            image = Image.open(filename)
            x, y = image.size
            print filename, ':', x,y
    elif opt == '--thumbnail':
        args = args[0:2] + glob_args(args[2:])
        make_thumbnails(args)
    
    else:
        print >>sys.stderr, ("%s: unknown option" % sys.argv[0])
        
if __name__ == '__main__':
    main()
    
