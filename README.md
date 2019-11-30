# selBox-pyGTK3
#### ComboBox (ou Select) usando biblioteca pyGTK3+ e python 3.4
#### que me permite facilmente:
- Ajustar o tamanho
- Pesquisar elementos, tanto por código, como pelo texto em si
- Selecionar pelo teclado

### Para usar é só:
```python
from selBox import selBox

sel = selBox("[Selecionar produto]")
sel.set_name("sel")

#inicializar o Gtk
gBuilder = Gtk.Builder()
window = gBuilder.get_object("window1")
grid = gBuilder.get_object("grid2")

# Definir a janela
sel.set_window(window)

#adicionar para a grid
grid.add(sel)
grid.child_set_property(sel, "left_attach", 1)
grid.child_set_property(sel, "top_attach", 0)
grid.child_set_property(sel, "width", 1)
grid.child_set_property(sel, "height", 1)
```

### Inserir:
```python
sel.insert(codigo, codigo + " - " + produto + "\n" + descricao)
 ```
