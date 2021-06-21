from bokeh.models import ColumnDataSource, Label, LabelSet, Range1d
from bokeh.plotting import figure, output_file, show

output_file("label.html")
data = dict(height=[66, 71, 72, 68, 58, 62],
                                    weight=[165, 189, 220, 141, 260, 174],
                                    names=['Mark', 'Amir', 'Matt', 'Greg',
                                           'Owen', 'Juan'])
source = ColumnDataSource(data)

p = figure()
p.circle([165, 189, 220, 141, 260, 174], [66, 71, 72, 68, 58, 62], size=8, source=source)


labels = LabelSet(x='weight', y='height', text='names',
              x_offset=5, y_offset=5, source=source, render_mode='canvas')



p.add_layout(labels)

  last_coordenades = last_circle[0]
            data['x'] = [last_coordenades[0]]
            data['y'] = [last_coordenades[1]] 
            data["iteration"] = [f"Final Group ({e})"]
            source = ColumnDataSource(data)
            graph.circle(x = 'x', y = 'y', color = _color , size = 20 , source = source)
    
show(p)