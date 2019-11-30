import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject
import string
from datetime import datetime

class PopupMenu(Gtk.Window):
    __gtype_name__ = 'SelBox_popupMenu'
    __timesleep = None
    __active = -1

    def __init__(self, selBox, selBoxWin, *args, **kwds):
        super().__init__(Gtk.WindowType.POPUP)

        self.__selected = -1
        self.__visible = False

        self.__selBox = selBox
        self.__selBoxWin = selBoxWin

        self.__scrollView = Gtk.ScrolledWindow()
        self.__scrollView.set_vexpand(True)
        self.__scrollView.set_hexpand(False)
        self.__scrollView.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.add(self.__scrollView)

        self.__box = Gtk.Box()
        self.__box.set_orientation(Gtk.Orientation.VERTICAL)

        self.__store = Gtk.ListStore(str)

        a = 0
        for o in self.__selBox.get_options():
            self.__insert(o, a)
            a+=1

        self.__scrollView.add(self.__box)

        self.__selBox.connect("size-allocate", self.__resize)
        self.__selBoxWin.connect("state-changed", self.__hide)
        
        self.__set_style()
        self.activate(None, None, 0)

    def __set_style(self):
        css = bytes("""
                GtkBox #selected {
                    color: #000000;
                    background-color: #CCCCCC;
                }

                GtkBox #active {
                    color: #FFFFFF;
                    background-color: #0000FF;
                }""",
            "utf8")

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def __resize(self, *args):
        size = self.__selBoxWin.get_size()
        self.set_size_request(size.width - 150, 200)
        self.size_request()
        self.set_resizable(False)

        pos = self.__selBoxWin.get_position()
        self.move(pos.root_x + 85, pos.root_y + size.height - 30)
    
    def __hide(self, *args):
        super().hide()

    def __insert(self, text, index):
        tmpEntry = Gtk.TextView()
        tmpBuffer = Gtk.TextBuffer()
        tmpBuffer.set_text(text)
        tmpEntry.set_buffer(tmpBuffer)

        tmpEntry.connect("button-press-event", self.onclick_item, index)
        tmpEntry.connect("motion-notify-event", self.select, index)
        self.__box.add(tmpEntry)

        tmpEntry.set_justification(Gtk.Justification.FILL)
        pass

    def insert(self, text):
        a = len(self.__box.get_children()) -1

        self.__insert(text, a)

    def show(self):
        if self.__visible:
            self.hide()
            self.__visible = False
            return
        
        self.__visible = True
        super().show_all()

        self.__resize()
        self.go_to(self.__active)

    def waitfordeselect(self, index):
        if index < 0:
            return
        if self.__selected < 0:
            return

        agora = datetime.now()

        time = agora - self.__timesleep

        if time.seconds >= 2:
            self.select(None, None, index)

    def select(self, bt, evnt, index):
        if index > -1:
            self.__timesleep = datetime.now()
        if self.__selected == index:
            return

        if self.__selected > -1:
            childs = self.__box.get_children()

            if self.__selected == self.__active:
                childs[self.__selected].set_name("active")
            else:
                childs[self.__selected].set_name("")
        
        self.__selected = index

        if index > -1:
            bt.set_name("selected")
            GObject.timeout_add(3000, self.waitfordeselect, -1)

    def go_to(self, index):
        a = index
        a = int((a+1) /2) * 2 + 3

        childs = self.__box.get_children()
        if a >= len(childs) -1:
            a = index

        childs[0].grab_focus()
        childs[a].grab_focus()
        childs[self.__active].set_name("active")

    def activate(self, bt, evnt, index):
        childs = self.__box.get_children()

        if self.__active > -1:
            childs[self.__active].set_name("")

        self.__active = index

        self.__selBox.set_text(self.__selBox.get_options()[self.__active])
        childs[self.__active].set_name("active")

        if self.__selected > -1:
            if self.__selected == self.__active:
                childs[self.__selected].set_name("")
            self.__selected = -1

        self.go_to(self.__active)

    def onclick_item(self, *args):
        index = args[len(args) -1]
        self.__selBox.activate(None, None, index)
        self.hide()

    def get_active(self):
        return self.__active

    def get_selected(self):
        return self.__selected

    def next(self):
        childs = self.__box.get_children()

        if self.__active < len(childs) -1:
            self.__selBox.activate(None, None, self.__active +1)
        else:
            self.__selBox.activate(None, None, 0)

    def prev(self):
        childs = self.__box.get_children()

        if self.__active > 0:
            self.__selBox.activate(None, None, self.__active -1)
        else:
            self.__selBox.activate(None, None, len(childs) -1)
            
        childs[self.__active].set_name("active")