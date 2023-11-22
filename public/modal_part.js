const modalOpenButton = document.getElementById('modalOpenButton');
const modalCloseButton = document.getElementById('modalCloseButton');
const modal = document.getElementById('modalContainer');

modalOpenButton.addEventListener('click', () => {
  modal.classList.remove('hidden');
});

modalCloseButton.addEventListener('click', () => {
  modal.classList.add('hidden');
});

const finput = document.getElementById('finput');
const sinput = document.getElementById('sinput');
document.getElementById("clic").addEventListener("click", print);
const first = document.getElementById('first-res');
const second = document.getElementById('second-res');
const third = document.getElementById('third-res');

let text_value = document.getElementById("ham");
let text_val = text_value.innerText.split('\n');
let label_val = text_val[0].split(', ');

let first_res = [];
let second_res = [];

function print(event){
  first.innerHTML = "";
  second.innerHTML = "";
  third.innerHTML = "";
  first_res = [];
  second_res = [];
  let first_value = text_val[Number(finput.value) + 1].split(', ');
  for(let i = 1;i<label_val.length;i++){
    if(first_value[i] != 0){
      first_res.push(label_val[i]);
    }
  }

  let second_value = text_val[Number(sinput.value) + 1].split(', ');
  for(let i = 1;i<label_val.length;i++){
    if(second_value[i] != 0){
      second_res.push(label_val[i]);
    }
  }

  let val = first_res.filter(x => second_res.includes(x));

  for(let i = 0;i < first_res.length;i++){
    let newParagraph = document.createElement('p');
    newParagraph.classList.add('first-value');
    newParagraph.textContent = first_res[i];
    first.appendChild(newParagraph);
  }

  for(let i = 0;i < second_res.length;i++){
    let newParagraph = document.createElement('p');
    newParagraph.classList.add('first-value');
    newParagraph.textContent = second_res[i];
    second.appendChild(newParagraph);
  }

  for(let i = 0;i < val.length;i++){
    let newParagraph = document.createElement('p');
    newParagraph.classList.add('first-value');
    newParagraph.textContent = val[i];
    third.appendChild(newParagraph);
  }
  console.log(first_res.length);
  document.getElementById("corr").innerText = (val.length / first_res.length).toFixed(3);
}
