const first = document.getElementById('first-res');
const second = document.getElementById('second-res');
const third = document.getElementById('third-res');

let text_value = document.getElementById("ham");
let text_val = text_value.innerText.split('\n');
let label_val = text_val[0].split(', ');

let first_res = [];
let second_res = [];

network.on("click", function(event){
  let clickedNodes = nodes.get(event.nodes);
  let check = "선택된 노드 : " + (clickedNodes[0].id).toString();

  if(check != document.getElementById("firstNode").innerText){
    second.innerHTML = "";
    document.getElementById("secondNode").innerText = document.getElementById("firstNode").innerText;
    second_res = first_res;
    for(let i = 0;i < second_res.length;i++){
      let newParagraph = document.createElement('p');
      newParagraph.classList.add('first-value');
      newParagraph.textContent = second_res[i];
      second.appendChild(newParagraph);
    }
  }

  first.innerHTML = "";
  third.innerHTML = "";
  first_res = [];

  document.getElementById("firstNode").innerText = check;

  let first_value = text_val[clickedNodes[0].id].split(', ');
  for(let i = 1;i<label_val.length;i++){
    if(first_value[i] != 0){
      first_res.push(label_val[i]);
    }
  }

  let val = first_res.filter(x => second_res.includes(x));

  for(let i = 0;i < first_res.length;i++){
    let newParagraph = document.createElement('p');
    newParagraph.classList.add('first-value');
    newParagraph.textContent = first_res[i];
    first.appendChild(newParagraph);
  }

  for(let i = 0;i < val.length;i++){
    let newParagraph = document.createElement('p');
    newParagraph.classList.add('first-value');
    newParagraph.textContent = val[i];
    third.appendChild(newParagraph);
  }
  document.getElementById("corr").innerText = "선택한 두 노드의 API 일치도 : " + (val.length / first_res.length).toFixed(3);
});