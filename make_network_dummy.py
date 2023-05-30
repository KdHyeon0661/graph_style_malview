from pyvis.network import Network
import networkx as nx

import sys
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

if len(sys.argv) != 2:
    print("Insufficient arguments")
    sys.exit()

file_name = sys.argv[1]

# read data
records = []
with open('./text_file/' + file_name, "r", encoding="utf-8") as f:
    # skip header
    f.readline()
    while True:
        line = f.readline()
        if not line:
            break
        raw = line.split(", ")
        # remove hash
        record = raw[1:]
        records.append(record)

# perform clustering
np_records = np.array(records)
X = pdist(np_records, metric='jaccard') # 모든 노드간의 거리가 들어있음
Z = linkage(X, method='complete', metric='jaccard')
cluster_ids = fcluster(Z, t=0.5, criterion="distance")

# print clustering results
# print(cluster_ids)


with open('./text_file/' + file_name, 'r', encoding="utf-8") as a:
    nx_graph = nx.Graph()
    data = a.readlines()
    res = []
    for i in data:
        res.append(i.strip().split(', '))
    del res[0]
    np_res = np.array(res)
    group_res = cluster_ids.tolist()

    np_zip_res = sorted(zip(np_res, group_res), key=lambda x: x[1])
    np_v_res = []
    for i in np_zip_res:
        np_v_res.append(i[0][1:])
    np_X = pdist(np_v_res, metric='jaccard')
    list_np_X = np_X.tolist()
    make_matrix = []
    k = 0
    for i in range(len(group_res)):
        tmp = []
        for j in range(len(group_res)):
            if i >= j:
                tmp.append(0)
            else:
                tmp.append(list_np_X[k])
                k += 1
        make_matrix.append(tmp)

    zip_res = sorted(zip(res, group_res), key=lambda x: x[1])
    tmp = 0
    for i, j in enumerate(zip_res):
        nx_graph.add_node(i, size=10, title=j[0][0], group=j[1])

    group_res.sort()


    with open('./storeValue/' + file_name, 'w', encoding="utf-8") as at:
        for i, j in zip(zip_res, make_matrix):
            at.write(str(' '.join(i[0])) + ',' + str(i[1]) + ',' + ' '.join(list(map(str, j))) + "\n")

    now = 0
    group_pre = [now]
    for i in range(1, len(group_res)):
        if group_res[now] != group_res[i]:
            now = i
            group_pre.append(now)
            continue
        t1, t2 = now, i
        if t1 > t2:
            t1, t2 = t2, t1
        nx_graph.add_edge(now, i, label=str(make_matrix[t1][t2]))

    if now != 0:
        group_pre.append(group_pre[0])

    for i in range(1, len(group_pre)):
        t1, t2 = i, i - 1
        if t1 > t2:
            t1, t2 = t2, t1
        nx_graph.add_edge(group_pre[i], group_pre[i-1], label=str(make_matrix[t1][t2]))

    nt = Network()
    nt.from_nx(nx_graph)
    nt.set_options("""
var options = {
"layout":{"randomSeed": 8},
  "configure": {
        "enabled": false
    },
    "edges": {
        "color": {
            "inherit": true
        },
        "smooth": {
            "enabled": true,
            "type": "dynamic"
        }
    },
    "interaction": {
        "dragNodes": true,
        "hideEdgesOnDrag": false,
        "hideNodesOnDrag": false,
        "navigationButtons": true
    },
    "physics": {
        "enabled": true,
        "stabilization": {
            "enabled": true,
            "fit": true,
            "iterations": 1000,
            "onlyDynamicEdges": false,
            "updateInterval": 50
        }
    },
            "manipulation": {
                "editNode": true
            }
}
""")
    nt.save_graph('./graph_folder/' + file_name[:file_name.find('.')] + '.html')
