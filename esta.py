import math
import random
from bokeh.models.annotations import ColorBar
from bokeh.plotting import graph, output_file,figure,show
from bokeh.models import ColumnDataSource, Label, LabelSet, Range1d
from bokeh.themes import built_in_themes
from bokeh.io import curdoc



def sort_for_min_distance(data_set,historial):
    data_set1 = data_set ; distances = [] ; keys = []; new_Data_Set = []
    min_positions_distances = [] ; means = [] ; _keys_to_delete = []; 

    if len(data_set1) == 1:
        return data_set1,historial

    for i in range(0,len(data_set1)):
        for n in range(0,len(data_set1)):
            # key = f"{str(coordenate1)},{str(coordenate2)}" 
            distance = math.sqrt(abs((data_set1[i][0] - data_set1[n][0]))**2 + abs((data_set1[i][1] - data_set1[n][1]))**2)
            if distance != 0:
                distances.append(round(distance,2))
                keys.append((i,n))
                
    minimo = min(distances)
   
  
    for n in range(0,len(distances)):
        if distances[n] == minimo:
            min_positions_distances.append(n)


    for position in min_positions_distances:
        position_data_set = keys[position]
        coor1 = data_set1[position_data_set[0]]
        coor2 = data_set1[position_data_set[1]]

        means_x = (coor1[0] + coor2[0])/2
        means_y = (coor1[1] + coor2[1])/2
        coordenate_means = (means_x,means_y)
        if coordenate_means not in means:
            means.append(coordenate_means)
    
    for deleter in min_positions_distances:
        keys_to_delete = keys[deleter]
        if keys_to_delete[0] not in _keys_to_delete:
            _keys_to_delete.append(keys_to_delete[0])   

        if keys_to_delete[1] not in _keys_to_delete:
            _keys_to_delete.append(keys_to_delete[1])
    
    for deleter_i in range(0,len(data_set1)):
        if deleter_i in keys_to_delete:
           historial.append(data_set1[deleter_i])
        else:
            new_Data_Set.append(data_set1[deleter_i])
     
    for new_coordenade in means:
        new_Data_Set.append(new_coordenade)


    # print(data_set1)
    # print(_keys_to_delete)
    # print(new_Data_Set)


    return sort_for_min_distance(new_Data_Set,historial)



   
    
    
# def writte_into_txt(sort):
#     with open("cor3.txt","w+", encoding="utf-8") as f:
#         for x in zip(sort):
#             f.write(f"{str(x)} \n")



def generate_data_set(n,limit):
    x_coordenates = [random.randint(0,limit) for x in range(n)] 
    y_coordenates = [random.randint(0,limit) for y in range(n)]

    linked_coordenates = [(x,y) for x,y in zip(x_coordenates,y_coordenates)]
    return x_coordenates,y_coordenates,linked_coordenates
data = generate_data_set(16 ,20)[2]
# data = [(5, 4), (8, 4), (0, 8), (1, 4), (9, 6), (8, 7), (9, 2), (6, 10), (10, 2), (6, 9)]   
merge_and_historial = sort_for_min_distance(data,[])
print(merge_and_historial)




def random_color_generator():
    data = []; return_data = []
    with open("./colors.txt","r", encoding="utf-8") as f:
        
        for x in f:
            data.append(str(x))
        
        for clean in data:
            return_data.append(clean[0:-1])
   
    color = return_data[random.randint(0,len(return_data))]
    return color[1::]

def link_progress(historial,random_color_generator,last_circle):

    output_file('Cluster.html')
    curdoc().theme = 'dark_minimal'
    graph = figure()
    
    coordenades = [] 
    axis_x = [] ; axis_y = []  ; complete_set_x = []; complete_set_y = []
    data = dict(x = [], y= [], iteration = []) 
    source = ColumnDataSource(data)

    points_linked = False ; i = 0 ; points_ = False ; e = 1; size = 10
    while points_linked == False:
        try:
            link =  (historial[i], historial[i+1])  
            coordenades.append(link)


            x1 = link[0][0] ; x2 = link[1][0] 
            y1 = link[0][1] ; y2 = link[1][1]
            axis_x.append(x1); axis_x.append(x2)
            axis_y.append(y1);axis_y.append(y2)

            data['x'] = [x1,x2]
            data['y'] = [y1,y2] 
            data['iteration'] = [str(e),str(e)]
            source = ColumnDataSource(data)

            _color = random_color_generator()
            graph.line(x = 'x', y = 'y', color = _color,width = 2, source = source, alpha = 0.5)
            graph.circle(x = 'x', y = 'y', color = _color , size = 15 , source = source)

            labels = LabelSet(x = 'x', y = 'y', text = 'iteration' ,x_offset=5, y_offset=5, source = source,text_color = "White",
            render_mode = 'canvas')
            graph.add_layout(labels)

            axis_x = []; axis_y = [] ; i += 2; e += 1


        except IndexError:
            points_linked = True
            
            # graph.circle(x = 'x', y = 'y', color = _color , size = 20 , source = source)
    
    last_coordenades = last_circle[0]
    data['x'] = [last_coordenades[0]]
    data['y'] = [last_coordenades[1]] 
    data["iteration"] = [f"Final Group ({e})"]
    source = ColumnDataSource(data)
    last_color = random_color_generator()
    graph.circle(x = 'x', y = 'y', color = last_color , size = 60 , source = source, alpha = 0.5)
    last_labels = LabelSet(x = 'x', y = 'y', text = 'iteration' ,x_offset=10, y_offset=10, source = source,text_color = "White",
    render_mode = 'canvas')
    graph.add_layout(last_labels)


    show(graph)
   

 

link_progress(merge_and_historial[1],random_color_generator,merge_and_historial[0])
# print(a)

# writte_into_txt(a)
# [(5, 4), (8, 4), (0, 8), (1, 4), (9, 6), (8, 7), (9, 2), (6, 10), (10, 2), (6, 9)]
