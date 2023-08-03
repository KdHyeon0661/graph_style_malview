import sys
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

if len(sys.argv) != 4:
    print("Insufficient arguments")
    sys.exit()

file_name = sys.argv[1]
e_threshold = float(sys.argv[3])

# read data
records = []
titles = []
with open('./text_file/' + file_name, "r") as f:
    # skip header
    f.readline()
    while True:
        line = f.readline()
        if not line:
            break
        raw = line.split(", ")
        # remove hash
        titles.append(raw[0])
        record = raw[1:]
        records.append(record)

# perform clustering
np_records = np.array(records)
X = pdist(np_records, metric='jaccard') # 모든 노드간의 거리가 들어있음
Z = linkage(X, method='complete', metric='jaccard')
cluster_ids = fcluster(Z, t=float(sys.argv[2]), criterion="distance")


with open('./text_file/' + file_name, 'r') as a:
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

    group_res.sort()

    with open('./storeValue/' + file_name, 'w') as at:
        for i, j in zip(zip_res, make_matrix):
            at.write(str(' '.join(i[0])) + ',' + str(i[1]) + ',' + ' '.join(list(map(str, j))) + "\n")

    now = 0
    group_pre = [now]
    same_group_edges = []
    for i in range(1, len(group_res)):
        if group_res[now] != group_res[i]:
            now = i
            group_pre.append(now)
            continue
        t1, t2 = now, i
        if t1 > t2:
            t1, t2 = t2, t1
        same_group_edges.append([t1, t2])

    if now != 0:
        group_pre.append(group_pre[0])

    connect_group_edges = []
    for i in range(1, len(group_pre)):
        t1, t2 = i, i - 1
        if t1 > t2:
            t1, t2 = t2, t1
        if make_matrix[t1][t2] >= e_threshold:
            continue
        connect_group_edges.append([t1, t2])

    with open('./graph_folder/' + file_name[:file_name.find('.')] + '.html', 'w') as f:
        f.write("""<html>
    <head>
        <meta charset="utf-8">

        <script
            type="text/javascript"
            src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

        <style type="text/css">
            #mynetwork {
                width: 500px;
                height: 500px;
                background-color: #ffffff;
                border: 1px solid lightgray;
                position: relative;
                float: left;
            }
        </style>
    </head>

    <body>
    <div class="card" style="width: 100%">
        <div id="mynetwork" class="card-body"></div>
    </div>


    <script type="text/javascript">
        var edges;
        var nodes;
        var network;
        var container;
        var options, data;

        // This method is responsible for drawing the graph, returns the drawn network
        function drawGraph() {
            var container = document.getElementById('mynetwork');


            // parsing and collecting nodes and edges from the python
            """)
        f.write("""nodes = new vis.DataSet([\n""")
        for i, j in enumerate(group_res):
            f.write(f'            {{"group": {j}, "id": {i}, "label": {i}, "shape": "dot", "size": 10, "title": "{titles[i]}"}},\n')
        f.write("""        ]);
        """)
        f.write("""    edges = new vis.DataSet([
                """)
        for i, j in same_group_edges:
            f.write(f'            {{"from": {i}, "to": {j}, "label": "{make_matrix[i][j]}", "length": {100 + make_matrix[i][j] * 400}}},\n')
        for i, j in connect_group_edges:
            f.write(f'            {{"from": {group_pre[i]}, "to": {group_pre[j]}, "label": "{make_matrix[i][j]}", "length": {30 + make_matrix[i][j] * 2000}}},\n')
        f.write("""]);
        """)

        f.write("""    data = {nodes: nodes, edges: edges};

                var options = {
                    "layout": {"randomSeed": 8}, 
                    "configure": {"enabled": false}, 
                    "edges": {
                        "color": {"inherit": true},
                        "smooth": {"enabled": true, "type": "dynamic"}
                    },
                    "interaction": {"dragNodes": true, 
                        "hideEdgesOnDrag": false, 
                        "hideNodesOnDrag": false, 
                        "navigationButtons": true}, 
                    "physics": {"enabled": true, 
                        "stabilization": {"enabled": true, 
                        "fit": true, 
                        "iterations": 1000, 
                        "onlyDynamicEdges": false, 
                        "updateInterval": 50}
                      }, 
                    "manipulation": {"editNode": true}
                };
                
                network = new vis.Network(container, data, options);

                return network;
            }

            drawGraph();
        </script>
        </body>
        </html>""")