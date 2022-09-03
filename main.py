import sys
import gi

from pathlib import Path

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw


BASE_DIR = Path(__file__).resolve().parent
MAIN_WINDOW = str(BASE_DIR.joinpath('window.ui'))


@Gtk.Template(filename=MAIN_WINDOW)
class AdwPreferencesWindow(Adw.Window):
    __gtype_name__ = 'AviatorWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # @Gtk.Template.Callback()
    # def on_open(self, button):
    #     print("Picking file");

    # @Gtk.Template.Callback()
    # def on_switch_button_clicked(self, switch, GParamBoolean):
    #     if switch.get_active():
    #         print('Botão marcado')
    #     else:
    #         print('Botão desmarcado')


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Things will go here

class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        # self.win = MainWindow(application=app)
        self.win = AdwPreferencesWindow(application=app)
        self.win.present()

app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
