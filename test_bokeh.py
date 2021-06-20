

from bokeh.plotting import figure, output_file, show

output_file("line.html")

p = figure()

p.circle((2),(3), size=20, color= "red" , alpha=1)
p.circle((7),(9), size=80, color= "#FF0", alpha=1)
p.line((2,7),(3,9), width = 2, color="navy", alpha=0.5)


# show the results
show(p)
