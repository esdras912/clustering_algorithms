
import math
import random
from bokeh.core.property.numeric import Size
from bokeh.layouts import column
from bokeh.models.annotations import ColorBar
from bokeh.plotting import graph, output_file,figure,show
from bokeh.models import ColumnDataSource, Label, LabelSet, Range1d, sources
from bokeh.themes import built_in_themes
from bokeh.io import curdoc
from jinja2.filters import F, K
from jinja2.nodes import With


def generate_data_set_and_k_point(n,limit,k):
    x_coordenates = [random.randint(0,limit) for x in range(n)] 
    y_coordenates = [random.randint(0,limit) for y in range(n)]

    linked_coordenates = [(x,y) for x,y in zip(x_coordenates,y_coordenates)]

    k_x_random = [random.randint(0,limit) for x in range(k)]
    
    k_y_random = [random.randint(0,limit) for y in range(k)]
  
    linked_coordenates_k = [(x,y) for x,y in zip(k_x_random,k_y_random)]

    return x_coordenates,y_coordenates,linked_coordenates,k_x_random,k_y_random, linked_coordenates_k


def graph(data_set):
    output_file('K_means.html')
    curdoc().theme = 'dark_minimal'
    graph = figure()

    data = dict(x = data_set[0],y = data_set[1])
    k_data = dict(x = data_set[3], y = data_set[4])
    source = ColumnDataSource(data)
    source_k = ColumnDataSource(k_data)

    graph.circle(x = 'x', y = 'y', size = 10, color = "Blue", source = source)
    graph.circle(x = 'x', y = 'y', size = 15, color = "Red", source = source_k)

    show(graph)

data = generate_data_set_and_k_point(5,5,2)


def compare_k(k_points,points):
    distances = []; idk = 0; idp = 0; k_sets = {} ;distances_full = []
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
            k_point_clustered[str(comparing.index(min(comparing)))].append((cluster_iter_p,comparing[comparing.index(min(comparing))]))
            comparing[key_min_val] = comparing[key_max_val] + 1

            if comparing[comparing.index(min(comparing))] != min_value:
                cache['cache'] = []; cluster_iter_p +=1 ; cluster_iter_k = 0; 
                comparing = []
            
          
            
        else:
            cache['cache'].append(k_sets[str(cluster_iter_k)][cluster_iter_p])
            cluster_iter_k +=1 ; 
    
        
    
    print(k_point_clustered)
    print(k_sets)



    

    

        
        

           



x = [2,2,1,3,2]
y = [4,0,4,2,2]

k_x = [3,2,]
k_y = [3,5]

x_y = [(2,4),(2,0),(1,4),(3,2),(2,2)]
kx_ky = [(3,3),(2,5),(1,3)]
data = [x,y,x_y,k_x,k_y,kx_ky]
# graph(data)

compare_k(kx_ky,x_y)
print(x_y)