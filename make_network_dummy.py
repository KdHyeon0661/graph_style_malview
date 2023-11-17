import sys
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform

import warnings
# Set the warning filter for FutureWarning to "ignore"
warnings.filterwarnings("ignore", category=FutureWarning)

if len(sys.argv) != 5:
    print("Insufficient arguments")
    sys.exit()

file_name = sys.argv[1]
e_threshold1 = float(sys.argv[2])
e_threshold2 = float(sys.argv[3])
edge_print_threshold = float(sys.argv[4])

# ============ 1. Read data ============
records = []
with open("./text_file/" + file_name, "r", encoding="utf-8") as f:
    # skip label header
    header = f.readline().strip().split(', ')
    while True:
        line = f.readline()
        if not line:
            break
        raw = line.strip().split(', ')
        # print(raw)
        raw = list(map(int, raw))
        records.append(raw)

data = pd.DataFrame(records, columns=header)  # Skip the first column as it contains numbers

# ============ 2. Print common API for the entire dataset ============
# Define the IQR threshold (you can calculate IQR for each column if needed)
iqr_threshold = 1.5

# Print common API for the entire dataset
common_API = []
# Calculate the IQR for each column in the cluster
for column in (data.columns[1:]):
    if data[column].max() == 0: # if all values are 0, skip
        continue

    iqr = data[column].quantile(0.75) - data[column].quantile(0.25)

    # Identify rows within, below, and above the IQR range for each column
    within_iqr = data[(data[column] >= (data[column].quantile(0.25) - iqr_threshold * iqr)) &
                                  (data[column] <= (data[column].quantile(0.75) + iqr_threshold * iqr))].count()

    # Retrieve the count values (second column) from within_iqr
    within_counts = within_iqr[column]

    total_data_in_cluster = len(data)

    # Calculate the proportion of data for each label within, below, and above the IQR
    proportion_within_iqr = within_counts / total_data_in_cluster

    # Check if any of the ratios exceed 70%
    if column not in common_API and proportion_within_iqr > 0.85:
        common_API.append(column)

# ============ 3. Perform primary clustering ============
# perform primary clustering with jaccard similarity
# np_records = np.array(records)
X = pdist(data, metric='jaccard') # 모든 노드간의 거리가 들어있음 # metric == jaccard // cosine
Z = linkage(X, method='complete', metric='jaccard')
cluster_ids = fcluster(Z, t=e_threshold1, criterion="distance") # 0.25
valX = squareform(X)

cluster_elements = {}

# Assign elements to clusters
for i, element in enumerate(cluster_ids):
    if element not in cluster_elements:
        cluster_elements[element] = []
    cluster_elements[element].append(i)

# Sort cluster numbers in ascending order
sorted_clusters = sorted(cluster_elements.keys())

node_vals = []
node_api_vals = []
cluster_X_vals = []
# ============ 4. Perform secondary clustering ============
n = 0
# perform secondary clustering with cosine similarity
for cluster, elements in cluster_elements.items():
    # print progress (print percentage of current cluster number / total cluster number)
    n += 1
    # print(f"Progress: {n}/{len(cluster_elements)}")

    cluster_data = data.iloc[elements]
    # if elements in a cluster is less than 2, skip
    # if len(cluster_records) < 2:
    #     continue
    cluster_X = pdist(cluster_data, metric='cosine')
    cluster_Z = linkage(cluster_X, method='complete', metric='cosine')
    cluster_ids = fcluster(cluster_Z, t=e_threshold2, criterion="distance") # 0.4
    cluster_X_vals.append(cluster_X);

    # Create a dictionary to store the elements for each cluster
    sub_cluster_elements = {}

    # Assign elements to clusters
    for i, element in enumerate(cluster_ids):
        if element not in sub_cluster_elements:
            sub_cluster_elements[element] = []
        sub_cluster_elements[element].append(cluster_elements[cluster][i])

    # Sort cluster numbers in ascending order
    sub_sorted_clusters = sorted(sub_cluster_elements.keys())

    # Print the elements for each cluster in sorted order
    for sub_cluster in sub_sorted_clusters:
        elements = sub_cluster_elements[sub_cluster]
        node_vals.append(elements)
        # print(f"Cluster {cluster}.{sub_cluster}: {elements}")

    # ============ 5. Print API candidates for each cluster ============
    # Print API candidates for each cluster
    for sub_cluster, elements in sub_cluster_elements.items():

        cluster_data = data.iloc[elements]
        # print(cluster_data.columns[1:])
        # Initialize a list to store labels for each column within the cluster
        labels = []

        # Calculate the IQR for each column in the cluster
        for column in (cluster_data.columns[1:]):
            if cluster_data[column].max() == 0:  # if all values are 0, skip
                continue

            # Convert the column to numeric and handle non-numeric values with 'coerce' option
            # cluster_data[column] = pd.to_numeric(cluster_data[column], errors='coerce')

            iqr = data[column].quantile(0.75) - data[column].quantile(0.25)

            # Identify rows within, below, and above the IQR range for each column
            within_iqr = cluster_data[(cluster_data >= (data.quantile(0.25) - iqr_threshold * iqr)) &
                                      (cluster_data <= (data.quantile(0.75) + iqr_threshold * iqr))].count()
            below_iqr = cluster_data[cluster_data < (data.quantile(0.25) - iqr_threshold * iqr)].count()
            above_iqr = cluster_data[cluster_data > (data.quantile(0.75) + iqr_threshold * iqr)].count()

            # Retrieve the count values (second column) from within_iqr
            within_counts = within_iqr[1:].values
            below_counts = below_iqr[1:].values
            above_counts = above_iqr[1:].values

            total_data_in_cluster = len(cluster_data)

            # Calculate the proportion of data for each label within, below, and above the IQR
            proportion_within_iqr = within_counts / total_data_in_cluster
            proportion_below_iqr = below_counts / total_data_in_cluster
            proportion_above_iqr = above_counts / total_data_in_cluster

            # print(f"Within IQR for {column}: {proportion_within_iqr}")
            # Iterate through the labels (assuming labels are column names)
            for label, ratio_within, ratio_below, ratio_above in zip(cluster_data.columns[1:], proportion_within_iqr,
                                                                     proportion_below_iqr, proportion_above_iqr):
                # Check if any of the ratios exceed 70%
                if label not in labels and (ratio_below > 0.7 or ratio_above > 0.7):
                    labels.append(label)
        
        node_api_vals.append(labels)

        # Print the results for this cluster
        '''if labels:
            print(f"Cluster {cluster}.{sub_cluster}: Candidate API List: {', '.join(labels)}")
            print(f"Cluster {cluster}.{sub_cluster}: Candidate API Count: {len(labels)}")'''

# --------------------------------------------

res = []
for i in range(len(node_api_vals)):
    a = []
    for j in range(len(node_api_vals)):
        b = 0
        for k in node_api_vals[j]:
            if k in node_api_vals[i]:
                b += 1
        if(len(node_api_vals[i]) != 0):
            a.append(round(b / len(node_api_vals[i]), 3))
    res.append(a)

with open('./storeValue/' + file_name, 'w') as f:
    f.write(str(len(node_api_vals)))
    for i in node_vals:
        v = ','.join(map(str,i))
        f.write('\n' + v);
    for i in node_api_vals:
        v = ','.join(map(str,i))
        f.write('\n' + v);
    for i in res:
        v = ','.join(map(str, i))
        f.write('\n' + v);
    

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
        for i in range(len(node_vals)):
            for j in range(len(node_vals[i])):
                f.write(f'            {{"group": {i + 1}, "id": {node_vals[i][j]}, "label": {node_vals[i][j]}, "shape": "dot", "size": 10, "title": "{node_vals[i][j]}"}},\n')
        f.write("""        ]);
        """)
        f.write("""    edges = new vis.DataSet([\n
                """)

        for i in range(len(node_vals)):
            if(len(node_vals[i]) > 1):
                for j in range(1, len(node_vals[i])):
                    f.write(
                        f'            {{"from": {node_vals[i][0]}, "to": {node_vals[i][j]}, "label": "{round(valX[node_vals[i][0]][node_vals[i][j]], 3)}"}},\n')

        for i in range(len(node_vals)):
            for j in range(i + 1, len(node_vals)):
                if(round(valX[node_vals[i][0]][node_vals[j][0]], 3) < edge_print_threshold):
                    f.write(
                    f'            {{"from": {node_vals[i][0]}, "to": {node_vals[j][0]}, "label": "{round(valX[node_vals[i][0]][node_vals[j][0]], 3)}", "length": {100 + valX[node_vals[i][0]][node_vals[j][0]] * 1000}}},\n')

        f.write("""]);
        """)

        f.write("""    data = {nodes: nodes, edges: edges};

                var options = {
                    "layout": {"randomSeed": 1}, 
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