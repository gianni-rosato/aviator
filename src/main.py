# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import sys
import threading
import subprocess
import gi
import json
import os
import time
import shutil
from ffmpeg_progress_yield import FfmpegProgress

from pathlib import Path

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gio

Adw.init()

def humanize(seconds):
    seconds = round(seconds)
    words = ["year", "day", "hour", "minute", "second"]

    if not seconds:
        return "now"
    else:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        y, d = divmod(d, 365)

        time = [y, d, h, m, s]

        duration = []

        for x, i in enumerate(time):
            if i == 1:
                duration.append(f"{i} {words[x]}")
            elif i > 1:
                duration.append(f"{i} {words[x]}s")

        if len(duration) == 1:
            return duration[0]
        elif len(duration) == 2:
            return f"{duration[0]} and {duration[1]}"
        else:
            return ", ".join(duration[:-1]) + " and " + duration[-1]

def notify(text):
    application = Gtk.Application.get_default()
    notification = Gio.Notification.new(title="Aviator")
    notification.set_body(text)
    application.send_notification(None, notification)


def first_open():
    startup_file = os.path.join(Path.home(), ".var/app/net.natesales.Aviator/startup.dat")
    if os.path.exists(startup_file):
        return False
    else:
        with open(startup_file, "w") as f:
            f.write("\n")
        return True

class FileSelectDialog(Gtk.FileChooserDialog):
    home = Path.home()

    def __init__(self, parent, select_multiple, label, selection_type, open_only, callback=None):
        super().__init__(transient_for=parent, use_header_bar=True)
        self.select_multiple = select_multiple
        self.label = label
        self.callback = callback
        self.set_action(action=Gtk.FileChooserAction.OPEN if open_only else Gtk.FileChooserAction.SAVE)

        if selection_type == "source":
            title = _("Select Source Files")
            if not self.select_multiple:
                title = _("Select Source File")

        if selection_type == "output":
            title = _("Select Output Files")
            if not self.select_multiple:
                title = _("Select Output File")

        self.set_modal(modal=True)
        self.set_select_multiple(select_multiple=self.select_multiple)
        self.connect("response", self.dialog_response)
        self.set_current_folder(Gio.File.new_for_path(path=str(self.home)))

        self.add_buttons(
            _("_Cancel"), Gtk.ResponseType.CANCEL,
            _("_Select"), Gtk.ResponseType.OK
        )
        btn_select = self.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        btn_select.get_style_context().add_class(class_name="suggested-action")
        btn_cancel = self.get_widget_for_response(response_id=Gtk.ResponseType.CANCEL)
        btn_cancel.get_style_context().add_class(class_name="destructive-action")

        self.show()

    def dialog_response(self, widget, response):
        if response == Gtk.ResponseType.OK:
            if self.select_multiple:
                gliststore = self.get_files()
                for glocalfile in gliststore:
                    print(glocalfile.get_path())
            else:
                glocalfile = self.get_file()
                # print(glocalfile.get_path())
                self.label.set_label(glocalfile.get_path())
        if self.callback is not None:
            self.callback()
        widget.close()


@Gtk.Template(resource_path="/net/natesales/Aviator/startup.ui")
class OnboardWindow(Adw.Window):
    __gtype_name__ = "OnboardWindow"

    image = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.image.set_from_resource(
            resource_path = "/net/natesales/Aviator/images/net.natesales.Aviator-splash.png"
        )

    @Gtk.Template.Callback()
    def go(self, button):
        app.win = MainWindow(application=app)
        app.win.present()
        self.destroy()



@Gtk.Template(resource_path='/net/natesales/Aviator/window.ui')
class MainWindow(Adw.Window):
    __gtype_name__ = 'AviatorWindow'

    # Video page
    source_file_label = Gtk.Template.Child()
    resolution_width_entry = Gtk.Template.Child()
    resolution_height_entry = Gtk.Template.Child()
    deinterlace_toggle = Gtk.Template.Child()
    crop_toggle = Gtk.Template.Child()
    warning_image_speed = Gtk.Template.Child()
    gop_toggle = Gtk.Template.Child()
    # scaling_method = Gtk.Template.Child()
    psy_toggle = Gtk.Template.Child()
    crf_scale = Gtk.Template.Child()
    speed_scale = Gtk.Template.Child()
    grain_scale = Gtk.Template.Child()
    denoise_toggle = Gtk.Template.Child()

    # Audio page
    bitrate_entry = Gtk.Template.Child()
    downmix_switch = Gtk.Template.Child()
    audio_copy_switch = Gtk.Template.Child()
    info_copy_audio = Gtk.Template.Child()
    loudnorm_toggle = Gtk.Template.Child()
    volume_scale = Gtk.Template.Child()

    # Export page
    output_file_label = Gtk.Template.Child()
    warning_image_webm = Gtk.Template.Child()
    container_mkv_button = Gtk.Template.Child()
    container_webm_button = Gtk.Template.Child()
    container = "mkv"
    encode_button = Gtk.Template.Child()
    encoding_spinner = Gtk.Template.Child()
    stop_button = Gtk.Template.Child()
    progress_bar = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Default to MKV
        self.container_webm_button.set_has_frame(False)
        self.container_mkv_button.set_has_frame(True)
        self.container = "mkv"

        # Reset value to remove extra decimal
        self.speed_scale.set_value(0)
        self.speed_scale.set_value(6)
        self.crf_scale.set_value(0)
        self.crf_scale.set_value(32)
        self.grain_scale.set_value(0)
        self.grain_scale.set_value(6)
        self.grain_scale.set_value(0)
        self.volume_scale.set_value(0)
        self.volume_scale.set_value(6)
        self.volume_scale.set_value(0)

        # resolution and audio bitrate
        self.metadata: (float, float, float) = ()
        self.bitrate_entry.set_text(str(80))

        # Absolute source path file
        self.source_file_absolute = ""
        self.output_file_absolute = ""

        # Set progress bar to 0
        self.progress_bar.set_fraction(0)
        self.progress_bar.set_text(_("0%"))
        self.process = None
        self.encode_start = None

    def load_metadata(self):
        self.metadata = metadata(self.source_file_absolute)

    @Gtk.Template.Callback()
    def empty_or_not_empty(self, switch, gboolean):
        if self.audio_copy_switch.get_state():
            self.container_webm_button.set_sensitive(True)
            self.bitrate_entry.set_sensitive(True)
            self.audio_copy_switch.set_sensitive(True)
            self.loudnorm_toggle.set_sensitive(True)
            self.volume_scale.set_sensitive(True)
            self.downmix_switch.set_sensitive(True)
        else:
            self.container_mkv_button.set_has_frame(True)
            self.container_mkv("clicked")
            self.container_webm_button.set_sensitive(False)
            self.bitrate_entry.set_sensitive(False)
            self.loudnorm_toggle.set_sensitive(False)
            self.volume_scale.set_sensitive(False)
            self.downmix_switch.set_sensitive(False)

    def handle_file_select(self):
        # Trim file path
        if "/" in self.source_file_label.get_text():
            self.source_file_absolute = self.source_file_label.get_text()
            self.source_file_label.set_text(os.path.basename(self.source_file_absolute))

    # Video

    @Gtk.Template.Callback()
    def open_source_file(self, button):
        FileSelectDialog(
            parent=self,
            select_multiple=False,
            label=self.source_file_label,
            selection_type="source",
            open_only=True,
            callback=self.handle_file_select
        )

    @Gtk.Template.Callback()
    def speed_changed(self, button):
        if self.speed_scale.get_value() < 3:
            self.warning_image_speed.set_visible(True)
        elif self.speed_scale.get_value() > 2:
            self.warning_image_speed.set_visible(False)
        else:
            self.warning_image_speed.set_visible(True)

    # Export

    @Gtk.Template.Callback()
    def open_output_file(self, button):
        FileSelectDialog(
            parent=self,
            select_multiple=False,
            label=self.output_file_label,
            selection_type="output",
            open_only=False,
        )

    @Gtk.Template.Callback()
    def container_mkv(self, button):
        self.container_webm_button.set_has_frame(False)
        self.warning_image_webm.set_visible(False)
        self.container_mkv_button.set_has_frame(True)
        self.container = "mkv"

    @Gtk.Template.Callback()
    def container_webm(self, button):
        self.container_mkv_button.set_has_frame(False)
        self.warning_image_webm.set_visible(True)
        self.container_webm_button.set_has_frame(True)
        self.container = "webm"

    def report_encode_finish(self,encode_start):
        encode_end = time.time() - encode_start
        notify(_("Encode finished in {0}! ✈️").format(humanize(encode_end)))
        self.progress_bar.set_fraction(0)
        self.progress_bar.set_text(_("Encode Finished ~ 0%"))
        self.stop_button.set_visible(False)

        self.encode_button.set_visible(True)
        self.encoding_spinner.set_visible(False)

    @Gtk.Template.Callback()
    def start_export(self, button):
        self.encode_button.set_visible(False)
        self.encoding_spinner.set_visible(True)
        self.stop_button.set_visible(True)

        output = self.output_file_label.get_text()
        if self.container == "mkv" and not output.endswith(".mkv"):
            output += ".mkv"
        elif self.container == "webm" and not output.endswith(".webm"):
            output += ".webm"

        def run_in_thread():

            width = height = None

            try:
                width = int(self.resolution_width_entry.get_text())
            except ValueError:
                pass

            try:
                height = int(self.resolution_height_entry.get_text())
            except ValueError:
                pass

            if self.crop_toggle.get_active():
                if width is not None and height is None:
                    height = "ih"
                elif width is None and height is not None:
                    width = "iw"
            else:
                if width is not None and height is None:
                    height = -2
                elif width is None and height is not None:
                    width = -2

            method = "bicubic:param0=0:param1=1/2"

            # if self.scaling_method.get_selected_item() == "Lanczos":
            #     method = "lanczos"
            # elif self.scaling_method.get_selected_item() == "Mitchell":
            #     method = "bicubic:param0=1/3:param1=1/3"
            # elif self.scaling_method.get_selected_item() == "BicubicDidee":
            #     method = "bicubic:param0=-1/2:param1=1/4"
            # else:
            #     method = "bicubic:param0=0:param1=1/2"

            if self.deinterlace_toggle.get_active():
                vfilters_prefix = "-vf"
                vfilters = "fieldmatch,nnedi=weights=/app/bin/nnedi3_weights.bin,format=yuv420p10le,decimate"
            else:
                vfilters_prefix = "-y"
                vfilters = "-y"

            if width is not None and height is not None:
                if vfilters_prefix == "-vf":
                    vfilters += ","
                    vfilters += "crop" + f"={width}:{height}" if self.crop_toggle.get_active() else "scale" + f"={width}:{height}:flags={method}"
                else:
                    vfilters_prefix = "-vf"
                    vfilters = "crop" + f"={width}:{height}" if self.crop_toggle.get_active() else "scale" + f"={width}:{height}:flags={method}"

            if self.psy_toggle.get_active():
                tune = 3
                sharpness = 1
            else:
                tune = 2
                sharpness = 0

            if self.denoise_toggle.get_active():
                denoise_val = 1
            else:
                denoise_val = 0

            if self.gop_toggle.get_active():
                gop_val = 1
            else:
                gop_val = 2

            if self.audio_copy_switch.get_state():
                afilters = "-y"
            else:
                if self.volume_scale.get_value() == 0:
                    if self.loudnorm_toggle.get_active():
                        afilters = "loudnorm,aformat=channel_layouts=7.1|6.1|5.1|stereo"
                    else:
                        afilters = "aformat=channel_layouts=7.1|6.1|5.1|stereo"
                else:
                    if self.loudnorm_toggle.get_active():
                        afilters = f"loudnorm,volume={int(self.volume_scale.get_value())}dB,aformat=channel_layouts=7.1|6.1|5.1|stereo"
                    else:
                        afilters = f"volume={int(self.volume_scale.get_value())}dB,aformat=channel_layouts=7.1|6.1|5.1|stereo"

            if self.audio_copy_switch.get_state():
                afilters_prefix = "-y"
            else:
                afilters_prefix = "-af"

            cmd = [
                "ffmpeg",
                "-nostdin",
                "-hide_banner",
                "-loglevel", "info",
                "-y",
                "-i", self.source_file_absolute,
                vfilters_prefix,
                vfilters,
                "-map", "0:v",
                "-c:v", "libsvtav1",
                "-crf", str(int(self.crf_scale.get_value())),
                "-preset", str(int(self.speed_scale.get_value())),
                "-pix_fmt", "yuv420p10le",
                "-svtav1-params", f"film-grain={int(self.grain_scale.get_value())}:" + f"tune={tune}:" + f"sharpness={sharpness}:" + "input-depth=10:enable-qm=1:qm-min=0:keyint=300:aq-mode=2:sharpness=1:" + f"irefresh-type={gop_val}:" + f"film-grain-denoise={denoise_val}",
                "-map", "0:a?",
                "-c:a", "copy" if self.audio_copy_switch.get_state() else "libopus",
                "-mapping_family", "1",
                "-b:a", self.bitrate_entry.get_text() + "K",
                afilters_prefix,
                afilters,
                "-ac", "2" if self.downmix_switch.get_state() else "0",
                "-map", "0:s?" if self.container == "mkv" else "-0:s",
                "-c:s", "copy",
                "-metadata", "comment=\"Encoded with Aviator\"",
                output,
            ]

            print(cmd)
            self.encode_start = time.time()
            self.process = FfmpegProgress(cmd)
            for progress in self.process.run_command_with_progress():
                print(f"{progress}/100")
                self.progress_bar.set_fraction(progress/100)
                self.progress_bar.set_text(_("Encoding ~ {0:0.1f}%").format(float(progress)))
            self.report_encode_finish(self.encode_start)

        thread = threading.Thread(target=run_in_thread)
        thread.start()

    @Gtk.Template.Callback()
    def stop_encode(self, button):
        print("Killing encoding job...")
        if self.process is not None:
            self.process.quit()
            print("Killed encoding job")
            self.report_encode_finish(self.encode_start)


class AviatorApplication(Adw.Application):
    """The main application singleton class."""
    def __init__(self, version):
        super().__init__(application_id='net.natesales.Aviator',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.version = version
        self.connect("activate", self.on_activate)

        about_action = Gio.SimpleAction(name="about")
        about_action.connect("activate", self.about_dialog)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction(name="quit")
        quit_action.connect("activate", self.quit)
        self.add_action(quit_action)

    def on_activate(self, app):
        # if first_open():
        #     startup_window = OnboardWindow(application=self)
        #     startup_window.present()
        # else:
            self.win = MainWindow(application=app)
            self.win.present()

    def about_dialog(self, *args):
        about = Adw.AboutWindow(transient_for=self.win,
                                application_name="Aviator",
                                application_icon="net.natesales.Aviator",
                                developer_name="Nate Sales & Gianni Rosato",
                                version=self.version,
                                copyright="Copyright © 2024 Nate Sales &amp; Gianni Rosato",
                                license_type=Gtk.License.GPL_3_0,
                                website="https://github.com/gianni-rosato/aviator",
                                issue_url="https://github.com/gianni-rosato/aviator/issues")
        # TRANSLATORS: eg. 'Translator Name <your.email@domain.com>' or 'Translator Name https://website.example'
        about.set_translator_credits(_("translator-credits"))
        about.add_link(_("Donate"), 'https://github.com/sponsors/gianni-rosato')
        about.set_developers(
            [
                "Nate Sales https://natesales.net",
                "Gianni Rosato https://giannirosato.com",
                "Trix<>"
            ]
        )
        about.set_designers(["Gianni Rosato https://giannirosato.com"])
        about.add_acknowledgement_section(
            _("Special thanks to the encoding community!"),
            [
                "AV1 For Dummies https://discord.gg/bbQD5MjDr3",
                "SVT-AV1-PSY Fork https://github.com/gianni-rosato/svt-av1-psy",
                "Codec Wiki https://wiki.x266.mov/"
            ]
        )
        about.add_legal_section(
            title='FFmpeg',
            copyright='Copyright © 2024 FFmpeg',
            license_type=Gtk.License.GPL_3_0,
        )
        about.add_legal_section(
            title='SVT-AV1',
            copyright='Copyright © 2024 Alliance for Open Media',
            license_type=Gtk.License.BSD,
        )
        about.present()

    def quit(self, action=None, user_data=None):
        exit()

def main(version):
    """The application's entry point."""
    app = AviatorApplication(version)
    return app.run(sys.argv)
