import json
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
    
def plot_graphs(pro,neu,anti,cat):
    plt.figure(figsize=(20, 5))
    plt.subplot(1,3,1)
    plt.hist(pro,  color='green')
    plt.xlabel(cat)
    plt.ylabel('No of nodes')
    plt.title(cat+' - (Pro-Elon Musk)')
    
    plt.subplot(1,3,2)
    plt.hist(neu,  color='blue')
    plt.xlabel(cat)
    plt.ylabel('No of nodes')
    plt.title(cat+' - (Neutral-Elon Musk)')
    
    plt.subplot(1,3,3)
    plt.hist(anti,  color='red')
    plt.xlabel(cat)
    plt.ylabel('No of nodes')
    plt.title(cat+' - (Anti-Elon Musk)')
    plt.savefig(cat+'.png')
    
    
    
def main():
    with open("json_edge_data_list_elon.json", "r") as out:
        ne = json.load(out)
    with open("node_labels_elon.json", "r") as out1:
        cl = json.load(out1)   
        
        
    G = nx.DiGraph()
    for x in ne.keys():
        for y in ne[x]:
            G.add_edges_from([(y,x)])
    # G.order()  
    d = dict(G.degree)

    pro=[]
    neu=[]
    anti=[]
    for n, d in G.degree():
        if cl[n]=="green":
            pro.append(d)
        elif cl[n]=="red":
            anti.append(d)
        else:
            neu.append(d)
    plot_graphs(pro,neu,anti,'Degree Dist.')       


    pro=[]
    neu=[]
    anti=[]
    betweenness_centrality = nx.betweenness_centrality(G)
    for key in betweenness_centrality.keys():
        if cl[key]=="green":
            pro.append(betweenness_centrality[key])
        elif cl[key]=="red":
            anti.append(betweenness_centrality[key])
        else:
            neu.append(betweenness_centrality[key])
    plot_graphs(pro,neu,anti,'Betweeness Cent.')


    pro=[]
    neu=[]
    anti=[]
    closeness_centrality = nx.closeness_centrality(G)
    for key in closeness_centrality.keys():
        if cl[key]=="green":
            pro.append(closeness_centrality[key])
        elif cl[key]=="red":
            anti.append(closeness_centrality[key])
        else:
            neu.append(closeness_centrality[key])
    plot_graphs(pro,neu,anti,'Closeness Cent.')

    
if __name__ == '__main__':
    main()


