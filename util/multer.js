const multer = require('multer');
const path = require('path');

const storage = multer.diskStorage({
  destination(req, file, done) {
    done(null, 'text_file/');
  },

  filename(req, file, done) {
    const ext = path.extname(file.originalname);

    const a = new Date();
    let year = a.getFullYear();
    let month = a.getMonth() + 1;
    let date = a.getDate();
    let hours = a.getHours();
    let minutes = a.getMinutes();
    let seconds = a.getSeconds();
    let milliseconds = a.getMilliseconds();
    let nowV = year + '_' + month + '_' + date + '_' + hours + '_' + minutes + '_' + seconds + '_' + milliseconds;
    
    const fileName = nowV + ext;
    done(null, fileName);
  },
});
const limits = { fileSize: 5 * 1024 * 1024 };

const multerConfig = {
  storage,
  limits,
};

exports.upload = multer(multerConfig);