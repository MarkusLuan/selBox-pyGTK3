import gi
from selBox import selBox
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

sel = selBox(["Selecionar produto"])
sel.set_name("sel")

#inicializar o Gtk
gBuilder = Gtk.Builder()
gBuilder.add_from_file("ui.glade")
window = gBuilder.get_object("window1")
grid = gBuilder.get_object("grid1")

# Definir a janela
sel.set_window(window)

#adicionar para a grid
grid.add(sel)
grid.child_set_property(sel, "left_attach", 1)
grid.child_set_property(sel, "top_attach", 0)
grid.child_set_property(sel, "width", 1)
grid.child_set_property(sel, "height", 1)

sel.insert("1", "1" + " - " + "Produto de teste" + "\n" + "descrição 1")
sel.insert("2", "2" + " - " + "Produto de teste" + "\n" + "descrição 2")
sel.insert("3", "3" + " - " + "Produto de teste" + "\n" + "descrição 3")

window.show()
Gtk.main()