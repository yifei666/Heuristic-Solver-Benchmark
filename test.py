#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 15:13:44 2021

@author: yifeiwang
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 14:28:47 2021

@author: yifeiwang
"""
from solver import solvermethod
from randomgraph import nxgraphgenerator
import numpy as np
import matplotlib.pyplot as plt
import json

def filesave(file):
    with open('graphdata2.json', 'w') as json_file:
        json.dump(file, json_file,indent=4)
        
    
def draw_errorbar(nodes, avglist, std, name):
    labels = []
    x_axis = []
    for num in range(nodes[0],nodes[1]):
        labels.append(str(num))
        x_axis.append(num)

    x_pos = np.arange(len(labels))
    fig, ax = plt.subplots()
    ax.bar(x_pos, avglist,
           yerr=std,
           align='center',
           alpha=0.5,
           ecolor='black',
           capsize=10)

    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_title('Heuristic Std Error')
    ax.yaxis.grid(True)
    ax.set_xlabel("Number of Nodes")
    ax.set_ylabel('Path Weights')
    

    plt.tight_layout()
    # plt.savefig('Heuristic Std Error.png', dpi = 300)
    plt.show()

def draw_comparisionbarplot(nodes, solvertimelist, heurtimelist):
    labels = []
    x_axis = []
    for num in range(nodes[0],nodes[1]):
        labels.append(str(num))
        x_axis.append(num)


    plt.plot(x_axis, solvertimelist, label = "solver")
    plt.plot(x_axis, heurtimelist, label = "heur")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Milliseconds")
    plt.title("Computation Time: Solver Vs Heuristic")
    plt.legend()
    # plt.savefig("Computatoin Time", dpi = 300)
    plt.show()

def draw_weightcomparison(nodes, heuravglist, solveravglist):
        
    Y = heuravglist
    Z = solveravglist
      
    X = list(range(nodes[0],nodes[1]))
    
    X_axis = np.arange(len(X))
      
    plt.bar(X_axis - 0.2, Y, 0.4, label = 'Heuristic Solution')
    plt.bar(X_axis + 0.2, Z, 0.4, label = 'Solver Solution')
      
    plt.xticks(X_axis, X)
    plt.xlabel("Nodes")
    plt.ylabel("NWeights")
    plt.title("Heuristic VS Solver (Sorted by latency)")
    plt.legend()
    # plt.savefig('Weights comparision.png', dpi = 300)
    plt.show()
    

def draw_errorplotweightplot(nodes,heuravglist, solveravglist, heurstd, solstd):
        
    Y = heuravglist
    Z = solveravglist
    Yerr = heurstd
    Zerr = solstd
    
    x_axis = np.linspace(nodes[0],nodes[1]-1, nodes[1]-nodes[0])
    
    fig, ax = plt.subplots()
    
    
    ax.errorbar(x_axis, Y,
                yerr=Yerr,
                fmt='-o',label="Heuristic")
    ax.errorbar(x_axis, Z,
                yerr=Zerr,
                fmt='-o',label = "Solver")
    
    ax.set_xlabel('Nodes')
    ax.set_ylabel('Weight')
    ax.set_title('Weight plot with error bars')
    plt.legend()
    # plt.savefig("errorbar.png", dpi=300)
    
    plt.show()
    
def graphgenerator(): 
    with open('graphdata2.json') as f:
          file = json.load(f)
    solvertimelist = file["solvertimelist"]   
    heurtimelist = file["heurtimelist"]
    solveravglist = file["solveravglist"]
    heuravglist = file["heuravglist"]
    heurstd = file["heurstd"]
    solstd = file["solstd"]
    nodes = file["nodes"]

    draw_errorbar(nodes, heuravglist, heurstd, 'Heuristic Std Error')
    
    draw_errorbar(nodes, solveravglist, solstd, 'Heuristic Std Error')
    
    draw_comparisionbarplot(nodes, solvertimelist, heurtimelist)

    draw_weightcomparison(nodes, heuravglist, solveravglist)
    
    draw_errorplotweightplot(nodes,heuravglist, solveravglist, heurstd, solstd)
    
    
    
    
def test(latency, nodes, n, samplenumber, coefficient, bwlimit):
    data=[]
    perlist=[]
    for node in range(nodes[0],nodes[1]+1):
        i = 0
        while i < samplenumber:
            heurresult = nxgraphgenerator(node, n, coefficient*node, bwlimit)
            heur = heurresult[0]
            heurtime = heurresult[1]
            if heur != "Null":
                solverresult = solvermethod()
                solver = solverresult[0]
                solvertime = solverresult[1]
                if abs(heur- solver)> 10:
                    errper = abs(heur - solver)/solver
                    perlist.append(errper)
                    data.append([solver,heur,solvertime,heurtime,node,i])
                    i+=1
    print("data:"+str(data))
    solvertimelist = []
    heurtimelist = []
    solveravglist = []
    heuravglist = []
    heurstd = []
    solstd = []
    length = int(nodes[1]-nodes[0])
    for n in range(length):
        solvertime = []
        heurtime = []
        solversol = []
        heursol= []
        c = 0
        while c < samplenumber:
            solversol.append(data[n * samplenumber+c][0])
            heursol.append(data[n * samplenumber+c][1])
            solvertime.append(data[n * samplenumber+c][2])
            heurtime.append(data[n * samplenumber+c][3])
            c=c+1
        solvertimelist.append(np.mean(solvertime))
        heurtimelist.append(np.mean(heurtime))
        solveravglist.append(np.mean(solversol))
        heuravglist.append(np.mean(heursol))
        solstd.append(np.std(solversol))
        heurstd.append(np.std(heursol))

    
            
            
        
        
    print(solvertimelist)
    print(heurtimelist)
    print(solveravglist)
    print(heuravglist)
    print(heurstd)
    print(solstd)
    
    file = {}
    file['solvertimelist'] = solvertimelist
    file['heurtimelist'] = heurtimelist
    file['solveravglist'] = solveravglist
    file['heuravglist'] = heuravglist
    file['heurstd'] = heurstd
    file['solstd'] = solstd
    file["nodes"] = nodes
    
    filesave(file)
    graphgenerator()



test(nodes=[15,18],n=0.1,samplenumber=5, coefficient=7,latency = 1000, bwlimit = 20)

