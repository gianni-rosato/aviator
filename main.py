import sys
import gi

from pathlib import Path

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw, Gio

Adw.init()


BASE_DIR = Path(__file__).resolve().parent
MAIN_WINDOW = str(BASE_DIR.joinpath("window.ui"))


class DialogSelecFolder(Gtk.FileChooserDialog):
    home = Path.home()

    def __init__(self, parent, select_multiple, label):
        super().__init__(transient_for=parent, use_header_bar=True)
        self.select_multiple = select_multiple
        self.label = label
        self.set_action(action=Gtk.FileChooserAction.OPEN)
        self.set_title(title="Select source files" if self.select_multiple else "Select source file")
        self.set_modal(modal=True)
        self.set_select_multiple(select_multiple=self.select_multiple)
        self.connect("response", self.dialog_response)
        self.set_current_folder(Gio.File.new_for_path(path=str(self.home)))

        self.add_buttons(
            "_Cancel", Gtk.ResponseType.CANCEL,
            "_Select", Gtk.ResponseType.OK
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
                print(glocalfile.get_path())
                self.label.set_label(glocalfile.get_path())
        widget.close()


class SourceFile(Gtk.Button):
    __gtype_name__ = "SourceFile"

@Gtk.Template(filename=MAIN_WINDOW)
class MainWindow(Adw.Window):
    __gtype_name__ = "AviatorWindow"

    # Video page
    source_file_label = Gtk.Template.Child()
    resolution_width_entry = Gtk.Template.Child()
    resolution_height_entry = Gtk.Template.Child()
    framerate_entry = Gtk.Template.Child()
    variable_framerate_switch = Gtk.Template.Child()
    crf_scale = Gtk.Template.Child()
    cpu_scale = Gtk.Template.Child()

    # Audio page
    bitrate_entry = Gtk.Template.Child()
    vbr_switch = Gtk.Template.Child()
    music_switch = Gtk.Template.Child()
    stereo_switch = Gtk.Template.Child()

    # Export page
    container_mkv_button = Gtk.Template.Child()
    container_webm_button = Gtk.Template.Child()
    container = "mkv"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Default to MKV
        self.container_webm_button.set_has_frame(False)
        self.container_mkv_button.set_has_frame(True)
        self.container = "mkv"

        self.crf_scale.set_value(0)
        self.crf_scale.set_value(32)
        self.cpu_scale.set_value(0)
        self.crf_scale.set_value(32)

    # Video

    @Gtk.Template.Callback()
    def open_source_file(self, button):
        DialogSelecFolder(parent=self, select_multiple=False, label=self.source_file_label)

    @Gtk.Template.Callback()
    def resolution_same_as_source(self, button):
        print("Setting resolution same as source")

    # Audio

    @Gtk.Template.Callback()
    def framerate_same_as_source(self, button):
        print("Setting framerate same as source")

    @Gtk.Template.Callback()
    def bitrate_same_as_source(self, button):
        print("Setting bitrate same as source")

    # Export

    @Gtk.Template.Callback()
    def container_mkv(self, button):
        self.container_webm_button.set_has_frame(False)
        self.container_mkv_button.set_has_frame(True)
        self.container = "mkv"

    @Gtk.Template.Callback()
    def container_webm(self, button):
        self.container_mkv_button.set_has_frame(False)
        self.container_webm_button.set_has_frame(True)
        self.container = "webm"

    @Gtk.Template.Callback()
    def start_export(self, button):
        print("Starting export")

         # Video page
        print("Source:", self.source_file_label.get_text())
        print(f"Resolution: {self.resolution_width_entry.get_text()}x{self.resolution_height_entry.get_text()}")
        print("FPS:", self.framerate_entry.get_text())
        print("VFR:", self.variable_framerate_switch.get_state())
        print("CRF:", self.crf_scale.get_value())
        print("CPU:", self.cpu_scale.get_value())

        # Audio page
        print("Bitrate:", self.bitrate_entry.get_text())
        print("VBR:", self.vbr_switch.get_state())
        print("Music:", self.music_switch.get_state())
        print("Stereo:", self.stereo_switch.get_state())

        # Export page
        print("Container:", self.container)


class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

app = App(application_id="net.natesales.Aviator")
app.run(sys.argv)
