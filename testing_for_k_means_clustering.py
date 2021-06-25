
import math
from operator import index, ne
import random
import re
from sys import gettrace
from bokeh.core.property.numeric import Size
from bokeh.layouts import column
from bokeh.models.annotations import ColorBar
from bokeh.plotting import graph, output_file,figure,show
from bokeh.models import ColumnDataSource, Label, LabelSet, Range1d, sources
from bokeh.themes import built_in_themes
from bokeh.io import curdoc





def generate_data_set_and_k_point(n,limit,k):
    x_coordenates = [random.randint(0,limit) for x in range(n)] 
    y_coordenates = [random.randint(0,limit) for y in range(n)]

    linked_coordenates = [(x,y) for x,y in zip(x_coordenates,y_coordenates)]

    k_x_random = [random.randint(0,limit) for x in range(k)]
    
    k_y_random = [random.randint(0,limit) for y in range(k)]
  
    linked_coordenates_k = [(x,y) for x,y in zip(k_x_random,k_y_random)]

    return k_x_random,k_y_random, linked_coordenates_k

def extract_data_points_for_graph(data):
    x_axis = []; y_axis = []
    for coordenade in data:
        x_axis.append(coordenade[0])
        y_axis.append(coordenade[1])

    return x_axis,y_axis



def graph(data_set):
    output_file('K_means.html')
    curdoc().theme = 'dark_minimal'
    graph = figure(plot_width=800, plot_height=800)

    data = dict(x = data_set[0],y = data_set[1])
    k_data = dict(x = data_set[3], y = data_set[4])
    source = ColumnDataSource(data)
    source_k = ColumnDataSource(k_data)

    graph.circle(x = 'x', y = 'y', size = 10, color = "Blue", source = source)
    graph.circle(x = 'x', y = 'y', size = 0, color = "Red", source = source_k)

    show(graph)

def graph_2(data_set):
    output_file('K_means.html')
    curdoc().theme = 'dark_minimal'
    graph = figure(plot_width=800, plot_height=800)

    data = dict(x = data_set[0],y = data_set[1])
    k_data = dict(x = data_set[3], y = data_set[4])
    source = ColumnDataSource(data)
    source_k = ColumnDataSource(k_data)

    graph.circle(x = 'x', y = 'y', size = 10, color = "Blue", source = source)
    graph.circle(x = 'x', y = 'y', radius = 0.5, color = "Red",alpha = 0.5, source = source_k)

    show(graph)

def random_color_generator():
    data = []; return_data = []
    with open("./colors.txt","r", encoding="utf-8") as f:
        
        for x in f:
            data.append(str(x))
        
        for clean in data:
            return_data.append(clean[0:-1])
   
    color = return_data[random.randint(0,len(return_data))]
    return color[1::]




def compare_k(k_points,points,ready_to_graph):

    idk = 0; idp = 0; k_sets = {} ;distances_full = []
    clustering_finished = False; k_limit = len(k_points); p_limit = len(points)
    cluster_iter_k = 0; cluster_iter_p = 0; k_groups = {}

    for k_point in k_points:
        Kx = k_point[0]; Ky = k_point[1]; idp = 0
        k_sets[str(idk)] = []
    
        for point in points:
            Px = point[0]; Py = point[1]
            distance = round(math.sqrt((Kx - Px)**2 + (Ky - Py)**2),2)
            # distances.append(((idk,idp),distance)) ;idp += 1
            k_sets[str(idk)].append(distance)
            distances_full.append(distance)
            idp +=1 
        idk +=1
    
    
    cache = dict(cache = []);  k_point_clustered = {}; comparing = []; _cache_save = []
    for key_generator in range(0,len(k_points)):
        k_point_clustered[str(key_generator)] = []

    
    

    while clustering_finished == False:
        comparing = cache['cache'] ; _cache_save = cache['cache']

        if cluster_iter_p == p_limit:
            clustering_finished = True 
            cache['cache'] = [];  cluster_iter_k = 0; cluster_iter_p = 0

        if len(cache['cache']) == k_limit:

            min_value = comparing[comparing.index(min(comparing))]
            key_min_val = comparing.index(min(comparing))
            key_max_val = comparing.index(max(comparing))
            # k_point_clustered[str(comparing.index(min(comparing)))].append((cluster_iter_p,comparing[comparing.index(min(comparing))]))
            k_point_clustered[str(comparing.index(min(comparing)))].append(cluster_iter_p)

            comparing[key_min_val] = comparing[key_max_val] + 1

            if comparing[comparing.index(min(comparing))] != min_value:
                cache['cache'] = []; cluster_iter_p +=1 ; cluster_iter_k = 0; 
                comparing = []
            
          
            
        else:
            cache['cache'].append(k_sets[str(cluster_iter_k)][cluster_iter_p])
            cluster_iter_k +=1 ; 
    
        
    
    mean_points = {}; radius_for_new_k_points = []
    for k_point_key_generor in range(len(k_point_clustered)):
        mean_points[str(k_point_key_generor)] = []


    sum_for_mean_x = 0; sum_for_mean_y = 0
    getted_means_values = False ; k_iter_cluster = 0; P_iter_cluster = 0; P_in_iter = 0

    while getted_means_values == False:
        if k_iter_cluster == len(mean_points):
            getted_means_values = True
            break
        
        if P_iter_cluster == len(k_point_clustered[str(k_iter_cluster)]):
            try:   
                key_for_point = mean_points[str(k_iter_cluster)][P_in_iter]
            except IndexError:
                sum_for_mean_x = 0; sum_for_mean_y = 0
                getted_means_values = False ; k_iter_cluster = 0; P_iter_cluster = 0; P_in_iter = 0
                mean_points = {}; radius_for_new_k_points = []
                for k_point_key_generor in range(len(k_point_clustered)):
                    mean_points[str(k_point_key_generor)] = []

            coordenade_x = points[key_for_point][0]
            coordenade_y = points[key_for_point][1]
            
            sum_for_mean_x += coordenade_x
            sum_for_mean_y += coordenade_y
            
            if P_in_iter+1 == len(k_point_clustered[str(k_iter_cluster)]):
                mean_for_x = round(sum_for_mean_x / len(k_point_clustered[str(k_iter_cluster)]),2)
                mean_for_y = round(sum_for_mean_y / len(k_point_clustered[str(k_iter_cluster)]),2)
                mean_points[str(k_iter_cluster)] = (mean_for_x,mean_for_y)

                k_iter_cluster += 1; P_iter_cluster = 0; P_in_iter = 0
                sum_for_mean_x = 0; sum_for_mean_y = 0

            else:
                P_in_iter += 1 
                    
        else: 
            val = k_point_clustered[str(k_iter_cluster)][P_iter_cluster]
            mean_points[str(k_iter_cluster)].append(val)
            P_iter_cluster += 1             

       
    new_k_points = list(mean_points.values())

    graphed_all_points = False ; iter_for_k_point = 0; iter_for_points_in_k = 0

#------------------------------------------------------------------------------------------
    output_file('K_means.html')
    curdoc().theme = 'dark_minimal'
    canvas = figure(plot_width=800, plot_height=800)
#------------------------------------------------------------------------------------------   
    while graphed_all_points == False:

        if iter_for_k_point == len(k_point_clustered):

            if ready_to_graph == True: 
               show(canvas); graphed_all_points = True
               break

            else: 
                graphed_all_points = True; break

        if iter_for_points_in_k  == len(k_point_clustered[str(iter_for_k_point)]):
            iter_for_k_point += 1; iter_for_points_in_k = 0

        else:
            key_for_coordendes_point = k_point_clustered[str(iter_for_k_point)][iter_for_points_in_k]
            x_k_point = mean_points[str(iter_for_k_point)][0]
            y_k_point = mean_points[str(iter_for_k_point)][1]

            actual_point_x = points[key_for_coordendes_point][0] 
            actual_point_y = points[key_for_coordendes_point][1] 

            
            x_vals = [x_k_point,actual_point_x]
            y_vals = [y_k_point,actual_point_y]

            canvas.circle([actual_point_x],[actual_point_y], size = 10, color = "Green")
            canvas.circle([x_k_point],[y_k_point], radius = 0.2, color = "Red",alpha = 0.5)
            canvas.line(x_vals,y_vals, color = "white", dash = "dashed")

            iter_for_points_in_k += 1


    return new_k_points,radius_for_new_k_points


data_k = generate_data_set_and_k_point(10,40,5)
# x = [1,2,3,4,5,7,8,8,5,8,11,4,2] ; y = [1,2,2,7,8,5,6,9,9,5,2,8,6]
x = [0, 35, 3, 20, 7, 2, 9, 36, 28, 11, 6, 17, 22, 6, 39, 20, 18, 7, 18, 19]
y = [5, 6, 24, 0, 8, 20, 25, 25, 14, 21, 2, 10, 5, 29, 15, 31, 20, 33, 8, 25]

k_x = data_k[0] ; k_y = data_k[1]


# x_y = [(1,1),(2,2),(3,2),(4,7),(5,8),(7,5),(8,6),(8,9),(5,9),(8,5),(11,2),(4,8),(2,6)]
x_y = [(0, 5), (35, 6), (3, 24), (20, 0), (7, 8), (2, 20), (9, 25), (36, 25), (28, 14), (11, 21), (6, 2), (17, 10), (22, 5), (6, 29), (39, 15), (20, 31), (18, 20), (7, 33), (18, 8), (19, 25)]

    # kx_ky = [(2,4),(4,9),(10,4)]
kx_ky = data_k[2]

data = [x,y,x_y,k_x,k_y,kx_ky]



graph(data)
        
data_k = generate_data_set_and_k_point(10,40,5)
# x = [1,2,3,4,5,7,8,8,5,8,11,4,2] ; y = [1,2,2,7,8,5,6,9,9,5,2,8,6]
x = [0, 35, 3, 20, 7, 2, 9, 36, 28, 11, 6, 17, 22, 6, 39, 20, 18, 7, 18, 19]
y = [5, 6, 24, 0, 8, 20, 25, 25, 14, 21, 2, 10, 5, 29, 15, 31, 20, 33, 8, 25]

k_x = data_k[0] ; k_y = data_k[1]


# x_y = [(1,1),(2,2),(3,2),(4,7),(5,8),(7,5),(8,6),(8,9),(5,9),(8,5),(11,2),(4,8),(2,6)]
x_y = [(0, 5), (35, 6), (3, 24), (20, 0), (7, 8), (2, 20), (9, 25), (36, 25), (28, 14), (11, 21), (6, 2), (17, 10), (22, 5), (6, 29), (39, 15), (20, 31), (18, 20), (7, 33), (18, 8), (19, 25)]

# kx_ky = [(2,4),(4,9),(10,4)]
kx_ky = data_k[2]

data = [x,y,x_y,k_x,k_y,kx_ky]

repetead_points = 0 ; last_points = [[]]
new_k_points = []; certain = 5
while repetead_points <= certain:

    if repetead_points == certain:
        new_k_points = compare_k(kx_ky,x_y,True)
    else: 
        new_k_points = compare_k(kx_ky,x_y,False)
        kx_ky = new_k_points[0]

    if new_k_points[0] == last_points[0]:
        repetead_points += 1

    last_points = []
    last_points.append(new_k_points[0])


points_to_graph = extract_data_points_for_graph(new_k_points[0])

new_data = [x,y,x_y,points_to_graph[0],points_to_graph[1],new_k_points]

# graph(data)
# next = input("Next: ")
# if next == "Y" or next == "y":
#     graph_2(new_data)































# new_x = [1, 1, 1, 1.5, 2, 2, 2, 2.5, 3, 3, 3.5, 3.5, 4, 4, 6, 6.5, 6.5, 7.5, 7.5, 8, 8, 8.5, 9]
# new_y = [1, 2, 3, 7.5, 2, 4, 6.5, 3, 2, 8, 1, 10, 3, 6.5, 6, 1.5, 8, 2, 3, 6.5, 9, 2.5, 1]


# new_x_y = [(1,1),(1,2),(1,3),
#       (1.5,7.5),
#       (2,2),(2,4),(2,6.5),
#       (2.5,3),
#       (3,2),(3,8),
#       (3.5,1),(3.5,10),
#       (4,3),(4,6.5),
#       (6,6),
#       (6.5,1.5),(6.5,8),
#       (7.5,2),(7.5,3),
#       (8,6.5),(8,9),
#       (8.5,2.5),
#       (9,1)]


# new_k_x_y = [(2,1),(5,9),(10,3)]

# new_k_x = [2, 5, 10]
# new_k_y = [1, 9, 3]




# aa_data = [new_x,new_y,new_x_y,new_k_x,new_k_y,new_k_x_y]



# repetead_points = 0 ; last_points = [[]]
# while repetead_points <= 3:
#     new_k_points = compare_k(new_k_x_y,new_x_y)
#     new_k_x_y = new_k_points[0]
#     if new_k_points[0] == last_points[0]:
#         repetead_points += 1

#     last_points = []
#     last_points.append(new_k_points[0])




# points_to_graph = extract_data_points_for_graph(new_k_points[0])

# new_data = [new_x,new_y,new_x_y,points_to_graph[0],points_to_graph[1],new_k_points]

# graph(aa_data)
# next = input("Next: ")
# if next == "Y" or next == "y":
#     graph_2(new_data)




# # graph(aa_data)