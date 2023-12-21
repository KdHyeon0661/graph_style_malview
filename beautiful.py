import sys
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print("Insufficient arguments")
    sys.exit()

file_name = sys.argv[1]

page = open('./graph_folder/' + file_name, 'rt', encoding='utf-8').read()
soup = BeautifulSoup(page, 'html.parser')

with open('./views/script.ejs', 'w', encoding='utf-8') as f:
    f.write(str(soup.find_all('script')[-1])[:-30])
    f.write('drawGraph();')
    f.write("""
      let value = document.getElementById("close");
      let val = value.innerText.split('\\n');
      let size = Number(val[0].split(',')[0]);
      let edgeValue = Number(val[0].split(',')[1]) - size;
      let modeVal = (val[0].split(',')[3]).toString();
      let api_val = [];
      let c2clen = [];
      let clusterIds = [];
      for(let i = 2;i <2 + size;i++){
        clusterIds.push(val[i].split(','));
      }
      for(let i = 2 + size;i <2 + size * 2;i++){
        api_val.push(val[i].split(','));
      }

      for(let i = 2 + size * 2;i <2 + size * 3;i++){
        c2clen.push(val[i].split(','));
      }


    """)
    f.write("""
    network.on("click", function (params) {
        let clickedNodes = nodes.get(params.nodes);
        document.getElementById("clusterId").innerText = (clickedNodes[0].group).toString();
        document.getElementById("nodeId").innerText = (clickedNodes[0].id).toString();

        const parentElement = document.getElementById('cluster-api-list');
        while (parentElement.firstChild) {
          parentElement.removeChild(parentElement.firstChild);
        }

        for(let i = 0;i < api_val[clickedNodes[0].group].length;i++){
          let newParagraph = document.createElement('p');
          newParagraph.classList.add('first-value');
          newParagraph.textContent = api_val[clickedNodes[0].group][i];
          parentElement.appendChild(newParagraph);
        }

        const parentElement2 = document.getElementById('c2c-length-list');
        while (parentElement2.firstChild) {
          parentElement2.removeChild(parentElement2.firstChild);
        }
        for(let i = 0;i < c2clen[clickedNodes[0].group].length;i++){
          let newParagraph = document.createElement('p');
          newParagraph.classList.add('second-value');
          newParagraph.textContent = "클러스터 " + i.toString() + "과의 API 거리 : " + c2clen[clickedNodes[0].group][i].toString();
          parentElement2.appendChild(newParagraph);
        }
        
      });
      
      """)

    
    f.write("""
    var clusterIndex = 0;
      var clusters = [];
      var lastClusterZoomLevel = 0;
      var clusterFactor = 0.9;
      
    network.once("initRedraw", function () {
        if (lastClusterZoomLevel === 0) {
          lastClusterZoomLevel = network.getScale();
        }
      });

      // we use the zoom event for our clustering
      network.on("zoom", function (params) {
        if (params.direction == "-") {
          if (params.scale < lastClusterZoomLevel * clusterFactor) {
            makeClusters(params.scale);
            lastClusterZoomLevel = params.scale;
          }
        } else {
          openClusters(params.scale);
        }
      });

      // if we click on a node, we want to open it up!
      network.on("selectNode", function (params) {
        if (params.nodes.length == 1) {
          if (network.isCluster(params.nodes[0]) == true) {
            network.openCluster(params.nodes[0]);
          }
        }
      });

      // make the clusters
      function makeClusters(scale) {
        var clusterOptionsByData = {
          processProperties: function (clusterOptions, childNodes) {
            clusterIndex = clusterIndex + 1;
            var childrenCount = 0;
            for (var i = 0; i < childNodes.length; i++) {
              childrenCount += childNodes[i].childrenCount || 1;
            }
            clusterOptions.childrenCount = childrenCount;
            clusterOptions.label = "# " + childrenCount + "";
            clusterOptions.font = { size: childrenCount * 5 + 30 };
            clusterOptions.id = "cluster:" + clusterIndex;
            clusters.push({ id: "cluster:" + clusterIndex, scale: scale });
            return clusterOptions;
          },
          clusterNodeProperties: {
            borderWidth: 3,
            shape: "database",
            font: { size: 30 },
          },
        };
        network.clusterOutliers(clusterOptionsByData);
        if (document.getElementById("stabilizeCheckbox").checked === true) {
          // since we use the scale as a unique identifier, we do NOT want to fit after the stabilization
          network.setOptions({ physics: { stabilization: { fit: false } } });
          network.stabilize();
        }
      }

      // open them back up!
      function openClusters(scale) {
        var newClusters = [];
        var declustered = false;
        for (var i = 0; i < clusters.length; i++) {
          if (clusters[i].scale < scale) {
            network.openCluster(clusters[i].id);
            lastClusterZoomLevel = scale;
            declustered = true;
          } else {
            newClusters.push(clusters[i]);
          }
        }
        clusters = newClusters;
        if (
          declustered === true &&
          document.getElementById("stabilizeCheckbox").checked === true
        ) {
          // since we use the scale as a unique identifier, we do NOT want to fit after the stabilization
          network.setOptions({ physics: { stabilization: { fit: false } } });
          network.stabilize();
        }
      }
</script>
""")