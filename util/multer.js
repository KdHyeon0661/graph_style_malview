const multer = require('multer');
const path = require('path');

const storage = multer.diskStorage({
  destination(req, file, done) {
    done(null, 'text_file/');
  }
});

const limits = { fileSize: 5 * 1024 * 1024 };

const multerConfig = {
  storage,
  limits,
};

exports.upload = multer(multerConfig);