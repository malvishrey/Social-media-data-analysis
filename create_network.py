import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def draw_graph(ne, color_labels):
    G = nx.DiGraph()
    for x in ne.keys():
        for y in ne[x]:
            G.add_edges_from([(y,x)])
    # G.order()  
    d = dict(G.degree)
    #d
    if(color_labels is not None):
        c_list = []
        for x in G.nodes:
            c_list.append(color_labels[x])
            
    else:
        c_list = 'blue'
        
            
    pos = nx.spring_layout(G,scale=70, k=5/np.sqrt(G.order()))
    plt.figure(figsize=(8, 7))

    nx.draw(G, pos, with_labels=False, node_size=[d[k]*10 for k in d], node_color=c_list, font_color='black')
    if(color_labels is not None):
        plt.savefig('graph_elon_classified.png')
    else:
        plt.savefig('graph_elon.png')
    
def main():
    try:
        with open("node_labels_elon.json", "r") as out1:
            cl = json.load(out1)
    except:
        cl = None
    with open("json_edge_data_list_elon.json", "r") as out:
        ne = json.load(out)
    draw_graph(ne,cl)
    
if __name__ == '__main__':
    main()