
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

    return x_coordenates,y_coordenates,linked_coordenates,k_x_random,k_y_random, linked_coordenates_k

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
    graph.circle(x = 'x', y = 'y', size = 15, color = "Red", source = source_k)

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


def compare_k(k_points,points):

    

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
            break
        
        if P_iter_cluster == len(k_point_clustered[str(k_iter_cluster)]):

            key_for_point = mean_points[str(k_iter_cluster)][P_in_iter]
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

 

    return new_k_points,radius_for_new_k_points

    

    
x = [1,2,3,4,5,7,8,8,5] ; y = [1,2,2,7,8,5,6,9,2]
k_x = [2,4,10] ; k_y = [4,9,4]


x_y = [(1,1),(2,2),(3,2),(4,7),(5,8),(7,5),(8,6),(8,9),(5,2)]
kx_ky = [(2,4),(4,9),(10,4)]
data = [x,y,x_y,k_x,k_y,kx_ky]




repetead_points = 0 ; last_points = [[]]
new_k_points = []
while repetead_points <= 3:
    new_k_points = compare_k(kx_ky,x_y)
    new_k_x_y = new_k_points[0]
    if new_k_points[0] == last_points[0]:
        repetead_points += 1

    last_points = []
    last_points.append(new_k_points[0])



points_to_graph = extract_data_points_for_graph(new_k_points[0])

new_data = [x,y,x_y,points_to_graph[0],points_to_graph[1],new_k_points]

graph(data)
next = input("Next: ")
if next == "Y" or next == "y":
    graph_2(new_data)































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