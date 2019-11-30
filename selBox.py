import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GObject
import string
from datetime import datetime

from .popupMenu import PopupMenu

class selBox(Gtk.TextView):
    __popupMenu = None
    __gtype_name__ = 'SelBox'
    __dictTeclas = {"num0" : 96, "num1" : 97, "num2" : 98, "num3" : 99, "num4" : 100, "num5" : 101, "num6" : 102, "num7" : 103, "num8" : 104, "num9" : 105, "0" : 48, "1" : 49, "2" : 50, "3" : 51, "4" : 52, "5" : 53, "6" : 54, "7" : 55, "8" : 56, "9" : 57, "a" : 65, "b" : 66, "c" : 67, "d" : 68, "e" : 69, "f" : 70, "g" : 71, "h" : 72, "i" : 73, "j" : 74, "k" : 75, "l" : 76, "m" : 77, "n" : 78, "o" : 79, "p" : 80, "q" : 81, "r" : 82, "s" : 83, "t" : 84, "u" : 85, "v" : 86, "w" : 87, "x" : 88, "y" : 89, "z" : 90, "ç" : 186}

    def __init__(self, options, *args,  **kwds):
        super().__init__(*args, **kwds)

        self.__handleSelect = []
        self.__searchStr = ""
        if options is None:
            self.__options = []
            self.__active = -1
        else:
            self.__options = options
            self.__active = 0

        self.set_size_request(40, 40)
        self.set_editable(False)
        if options is not None:
            self.set_text(self.__options[self.__active])
        self.set_cursor_visible(False)

        self.__handleClick = self.connect("button-press-event", self.showPopup)
        self.__handleKey = self.connect("key-press-event", self.key_press)

        self.__set_style()
        self.show()

    def refresh_search(self):
        self.__searchStr = ""

    def set_window(self, window):
        self.__popupMenu = PopupMenu(self, window)
        self.__popupMenu.connect("state-changed", self.refresh_search)

        self.__handleKey2 = self.__popupMenu.connect("key-press-event", self.key_press)

    def get_options(self):
        return self.__options

    def insert(self, _id, text):
        self.__options.append(text)

        if self.__popupMenu is None:
            return
        
        self.__popupMenu.insert(text)

        if self.__popupMenu.get_active() < 0:
            #self.__active = len(self.__options)-1
            self.activate(None, None, 0)

    def __set_style(self):
        css = bytes("""
                #sel_emp {
                    color: #000000;
                    background-color: #CCCCCC;
                    border-radius: 8px;
                }""",
            "utf8")

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.set_justification(Gtk.Justification.CENTER)

    def set_text(self, text):
        buffer = Gtk.TextBuffer()
        buffer.set_text(text)
        self.set_buffer(buffer)
        self.set_cursor_visible(False)

        self.__text = text

    def showPopup(self, selBox=None, evnt=None):
        if evnt is None or evnt.get_button()[1] == 1:
            GObject.timeout_add(100, self.__popupMenu.show)
            self.set_cursor_visible(False)

    def search(self):
        if self.__searchStr == "":
            return

        a = 0
        resultado = -1
        for o in self.__options:
            o = o.lower()
            tmpO = o.split(" - ") #Separa o código do Texto
            if len(tmpO) != 2:
                a+=1
                continue

            if self.__searchStr.isdigit(): #Pesquisar pelo código
                o = tmpO[0]
            else:                          #Pesquisar pelo nome
                o = tmpO[1]

            if o.startswith(self.__searchStr):
                resultado = a
                break
            if (not self.__searchStr.isdigit()) and (resultado < 0 and self.__searchStr in o):
                resultado = a
            a+=1
        
        if resultado < 0:
            if self.__searchStr == "":
                self.releaseHandleKey()
                return
            
            self.__searchStr = self.__searchStr[:-1]
            return False
        
        self.activate(None, None, resultado, True)

    def releaseHandleKey(self):
        self.handler_unblock(self.__handleKey)
        self.__popupMenu.handler_unblock(self.__handleKey2)

    def key_press(self, widget, evnt):
        self.handler_block(self.__handleKey)
        self.__popupMenu.handler_block(self.__handleKey2)

        self.set_cursor_visible(False)
        code = evnt.get_keycode()[1]

        if code == 8: #Backspace
            if self.__searchStr == "":
                self.releaseHandleKey()
                return
            
            self.__searchStr = self.__searchStr[:-1]
            self.search()
        elif code == 13: #Enter
            if (self.__popupMenu.get_selected() > -1):
                self.activate(None, None, self.__popupMenu.get_selected())

            self.refresh_search()            
            self.__popupMenu.hide()
        elif code == 27: #Esc
            self.refresh_search()
            self.__popupMenu.hide()
        elif code == 32: #Barra de espaço
            if len(self.__searchStr) > 0:
                self.__searchStr += " "
                self.search()
        elif code == 35: #End
            self.refresh_search()
            self.activate(None, None, len(self.__options)-1)
        elif code == 36: #Home
            self.refresh_search()
            self.activate(None, None, 0)
        elif code == 38: #Seta de cima
            self.__popupMenu.prev()
        elif code == 40: #Seta de baixo
            self.__popupMenu.next()

        if code in [8, 13, 32, 38, 40]:
            self.releaseHandleKey()
            return

        for key in self.__dictTeclas:
            if code == self.__dictTeclas[key]:
                self.__searchStr += key.replace("num", "")
                self.search()
                break

        self.releaseHandleKey()

    def activate(self, menuItem, evnt, index, porSearch=False):
        self.__popupMenu.activate(None, None, index)

        if porSearch == False:
            self.refresh_search()

    def get_active(self):
        return self.__popupMenu.get_active()