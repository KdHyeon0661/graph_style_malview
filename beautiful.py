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
    f.write('var network = drawGraph();')
    f.write("""
    let value = document.getElementById("close");
      let val = value.innerText.split('\\n');
      let tresval = [];
      let group_num = [];
      let API_list = [];
      let node_len = [];
      var i;
      for(i = 0;i<val.length - 1;i++){
        tresval.push(val[i].split(','));
      }
      for(i = 0;i<tresval.length - 1;i++){
        API_list.push(tresval[i][0].split(' '));
        group_num.push(tresval[i][1]);
        node_len.push(tresval[i][2].split(' '));
      }
    """)
    f.write("""
    network.on("click", function (params) {
        var clickedNodes = nodes.get(params.nodes);
        if(clickedNodes.length != 0){
        document.getElementById("eventSpanHeading2").innerText = document.getElementById("eventSpanHeading").innerText;
        document.getElementById("eventTitle2").innerText = document.getElementById("eventTitle").innerText;
        document.getElementById("apiList2").innerText = document.getElementById("apiList").innerText;
        
        document.getElementById("eventSpanHeading").innerText = "Node Id : " + (clickedNodes[0].id).toString();
        document.getElementById("eventTitle").innerText = "Code Id : " + (API_list[clickedNodes[0].id][0]);
        let apil = "";
        for(var i = 1; i<API_list[clickedNodes[0].id].length;i++){
            if(API_list[clickedNodes[0].id][i] >= 1){
                apil += "API" + i + ", ";
            }
        }
        document.getElementById("apiList").innerText = "API List = {" + apil + "}";

        if(!document.getElementById("eventSpanHeading2").innerText === false){
          var nol = document.getElementById("eventSpanHeading").innerText.split(' : ');
          var nol2 = document.getElementById("eventSpanHeading2").innerText.split(' : ');
          var a = [];
          for(var i = 1; i<API_list[clickedNodes[0].id].length;i++){
            if(API_list[Number(nol[1])][i] >= 1 && API_list[Number(nol2[1])][i] >= 1){
                a.push("API" + i);
            }
          }
          document.getElementById("eventSpanHeading3").innerText = "Node-to-node matching API";
          console.log(a)
          if(a.length == 0){
            document.getElementById("apiList3").innerText = "There's no match";
          }else{
          document.getElementById("apiList3").innerText = a;
          }
        }
        }
        
      });</script>
      """)
    '''
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
""")'''