import argparse
import ctypes
import datetime
import os
import win32com
import win32com.client

try:
    import Image
    import ImageDraw
    import ImageFont
except:
    try:
        from PIL import Image
        from PIL import ImageDraw
        from PIL import ImageFont
    except:
        raise Exception("Can't import PIL or PILLOW. Install one.")


def main(args):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "mode",
        metavar="mode",
        default="list",
        choices=["list", "splash"],
        type=str,
        nargs="?",
        help="How to show the meetings.",
    )
    parser.add_argument(
        "which",
        metavar="which",
        default="upcoming",
        choices=["upcoming", "next", "now"],
        type=str,
        nargs="?",
        help="Which meetings to show.",
    )
    # parser.add_argument(
    #     "--id-suffix",
    #     "-s",
    #     default="",
    #     help="A short string appended to each ID field, such as PatientID, "
    #     "AccessionNumber, and so on, to make it easier to identify anonymized "
    #     "studies. Longer suffixes reduce the number of available random "
    #     "characters in the ID and increase the chance of collisions with other "
    #     "IDs. May be combined with --id-prefix.",
    # )
    # parser.add_argument(
    #     "--output-directory",
    #     "-o",
    #     action="store",
    #     type=str,
    #     help="Instead of anonymizing files in-place, write anonymized files to "
    #     "OUTPUT_DIRECTORY, which will be created if necessary",
    # )
    # parser.add_argument(
    #     "--quiet",
    #     "-q",
    #     action="store_true",
    #     help="Reduce the verbosity of output. Suppresses summary of anonymized studies.",
    # )
    # parser.add_argument(
    #     "--log-level",
    #     action="store",
    #     metavar="LEVEL",
    #     default="WARNING",
    #     help="Set the log level. May be one of DEBUG, INFO, WARNING, ERROR, or CRITICAL.",
    # )
    # parser.add_argument(
    #     "--seed",  # currently only intended to make testing easier
    #     help="The seed to use when generating random attribute values. Primarily "
    #     "intended to make testing easier. Best anonymization practice is to omit "
    #     "this value and let dicognito generate its own random seed.",
    # )
    # parser.add_argument("--version", action="version", version=dicognito.__version__)

    args = parser.parse_args(args)
    print(args)

    now = datetime.datetime.now() + datetime.timedelta(hours=-6)

    appointments = find_appointments(args.mode, now)
    if args.mode == "list":
        for appointment in appointments:
            print(appointment.Start, appointment.Subject, appointment.Location)
    else:
        appointment = next(appointments)
        screen_size = Windows.get_screen_size()
        splash_size = calculate_splash_size(screen_size)
        image = create_image(appointments, splash_size)
        change_logon_background(image)


class Windows:
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 1
    SPIF_SENDWININICHANGE = 2

    SM_CMONITORS = 80
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1

    @classmethod
    def change_wallpaper(cls, new_wallpaper):
        result = ctypes.windll.user32.SystemParametersInfoW(
            Windows.SPI_SETDESKWALLPAPER, 0, new_wallpaper, Windows.SPIF_SENDWININICHANGE | Windows.SPIF_UPDATEINIFILE
        )
        print("change wallpaper return code:", result)

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

    class disable_file_system_redirection:
        _disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
        _revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

        @classmethod
        def __enter__(self):
            self.old_value = ctypes.c_long()
            self.success = self._disable(ctypes.byref(self.old_value))

        @classmethod
        def __exit__(self, type, value, traceback):
            if self.success:
                self._revert(self.old_value)


def find_appointments(mode, now):
    earliest_meeting_start = now + datetime.timedelta(minutes=-10)
    latest_meeting_start = datetime.datetime(year=now.year, month=now.month, day=now.day) + datetime.timedelta(days=1)

    OUTLOOK_FOLDER_CALENDAR = 9

    filter_early = datetime.datetime.strftime(earliest_meeting_start, "%Y-%m-%d %H:%M")
    filter_late = datetime.datetime.strftime(latest_meeting_start, "%Y-%m-%d %H:%M")

    filter = f"[MessageClass]='IPM.Appointment' AND [Start] >= '{filter_early}' AND [Start] <= '{filter_late}'"

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    appointments = outlook.GetDefaultFolder(OUTLOOK_FOLDER_CALENDAR).Items
    appointments.IncludeRecurrences = True

    for appointment in resolve_recurring_appointments(appointments.Restrict(filter), now):
        if earliest_meeting_start <= appointment.Start.replace(tzinfo=None) <= latest_meeting_start:
            yield appointment


def resolve_recurring_appointments(appointments, now):
    for appointment in appointments:
        if not appointment.IsRecurring:
            yield appointment

        try:
            filter = appointment.Start.replace(year=now.year, month=now.month, day=now.day)
            appointment = appointment.GetRecurrencePattern().GetOccurrence(filter)
            yield appointment
        except:
            pass


def calculate_splash_size(screen_size):

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

    desired_ratio = float(screen_size[0]) / screen_size[1]
    print("Changing logon background. desired_ratio=", desired_ratio)

    for possible_screen_size in logon_screen_dimensions:
        possible_ratio = float(possible_screen_size[0]) / possible_screen_size[1]

        if possible_ratio == desired_ratio:
            return possible_screen_size

    raise ("Can't figure out the best splash size for screen", screen_size)


def create_image(appointments, size):
    i = Image.new("RGB", size, color="black")

    appointment = next(appointments)

    font = ImageFont.truetype("georgia.ttf", 40)

    message = datetime.datetime.strftime(appointment.Start, "%H:%M") + " " + appointment.Location

    d = ImageDraw.Draw(i)
    title_text_size = d.textsize(message, font=font)

    # if options.subtitle:
    #     subtitle_font = ImageFont.truetype(options.subtitle_font + ".ttf", options.subtitle_font_size)
    #     subtitle_text_size = d.textsize(options.subtitle, font=subtitle_font)

    #     subtitle_left_offset = (i.size[0] - subtitle_text_size[0]) / 2
    #     title_box_top_offset = (i.size[1] - title_text_size[1] - subtitle_text_size[1] - subtitle_text_size[1] / 2) / 2

    #     subtitle_pos = (subtitle_left_offset, title_box_top_offset + title_text_size[1] + subtitle_text_size[1] / 2)

    #     d.text(
    #         (subtitle_pos[0] + shadow_offset, subtitle_pos[1] + shadow_offset),
    #         options.subtitle,
    #         font=subtitle_font,
    #         fill=shadow_colour,
    #     )
    #     d.text(subtitle_pos, options.subtitle, font=subtitle_font, fill=options.title_colour)

    #     pos = ((i.size[0] - title_text_size[0]) / 2, title_box_top_offset)
    # else:

    pos = (i.size[0] - title_text_size[0], 0)  # center(title_text_size, i.size)
    print(pos)
    # d.text((pos[0] + shadow_offset, pos[1] + shadow_offset), title, font=title_font, fill=shadow_colour)
    d.text(pos, message, font=font, fill="white")

    return i


def center(object, canvas):
    return ((canvas[0] - object[0]) / 2, (canvas[1] - object[1]) / 2)


def change_logon_background(image):
    # change the logon UI background if on Windows 7. From learning at
    # http://www.withinwindows.com/2009/03/15/windows-7-to-officially-support-logon-ui-background-customization/
    if not Windows.is_windows_7():
        print("not windows 7")
        return

    logon_background_dir = r"%(windir)s\system32\oobe\info\backgrounds" % os.environ

    if not os.path.exists(logon_background_dir):
        os.makedirs(logon_background_dir)

    logon_background_path = os.path.join(logon_background_dir, "background%dx%d.jpg" % image.size)
    print("path for logon screen background =", logon_background_path)
    quality = 80
    with Windows.disable_file_system_redirection():
        while quality >= 50:
            print(f"saving logon picture {logon_background_path} at quality {quality}")
            image.save(logon_background_path, "JPEG", quality=quality)
            file_size = os.path.getsize(logon_background_path)
            print("file size is", file_size)
            if file_size < 256 * 1000:
                # Windows.change_wallpaper(logon_background_path)
                break
            quality -= 5


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
