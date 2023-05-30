const input = document.querySelector('#file_uploads');
const preview = document.querySelector('.preview'); 
const vex = document.querySelector('.vex'); 

input.addEventListener('change', showTextFile);

function showTextFile() {
  const selectedFiles = input.files;

  for(const file of selectedFiles) {
    if(validFileType(file)) {
      let reader = new FileReader();
      reader.onload = function () {
        vex.textContent = reader.result;
      };
      reader.readAsText(file, "UTF-8");
    } else {
    }
  }
}

const fileTypes = [
  'text/plain',
];

function validFileType(file) {
  return fileTypes.includes(file.type);
}

function returnFileSize(number) {
  if(number < 1024) {
    return number + 'bytes';
  } else if(number > 1024 && number < 1048576) {
    return (number/1024).toFixed(1) + 'KB';
  } else if(number > 1048576) {
    return (number/1048576).toFixed(1) + 'MB';
  }
}