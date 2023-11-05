const express = require('express');
var fs = require('fs');
const { spawn } = require('child_process');
const path = require("path");
const app = express()
const session = require('express-session');
const bodyParser = require('body-parser');
const { upload } = require('./util/multer.js');
const multer = require('multer');
const printGraphRouter = require('./routes/printGraph');


const PORT = 8080

app.set('views', path.join(__dirname, './views'));
app.engine('html', require('ejs').renderFile);  
app.set('view engine', 'html');

app.use('/printGraph', printGraphRouter);
app.use(express.static(__dirname + "/lib"));
app.use(express.static('text_file'));
app.use(express.static('public'));
app.use(express.json())
app.use(bodyParser.urlencoded({ extended: true }));
app.use(session({
    secret: 'your-secret-key',
    resave: true,
    saveUninitialized: true
}));


app.get('/', (req, res) => {
    const folder = './graph_folder';
    fs.readdir(folder, function (error, filelist) {
        res.render('mainPage.ejs', {gfile:filelist});
    });
});


app.get('/filecontents', (req, res) => {
    res.render('printFileContents.ejs');
});

app.post('/filecontents', upload.single('file_uploads'), (req, res) => {
    const { filename, destination } = req.file;

    const python = spawn('python', ['make_network_dummy.py', filename.toString(), parseFloat(req.body.threshold).toFixed(2), parseFloat(req.body.e_threshold).toFixed(2)]);
    
    python.stderr.on('data', (data) => {
        // 오류 출력
        console.error(`오류 발생: ${data}`);
    });

    python.on('close', (code) => {
        console.log(`파이썬 프로세스 종료, 종료 코드: ${code}`);
        res.redirect('/');
    });
});

app.post('/upload_graph', (req, res) => {
    var file = req.params.id + '.txt';
    const python = spawn('python', ['make_network_dummy.py', file, parseFloat(req.body.threshold).toFixed(2), parseFloat(req.body.e_threshold).toFixed(2)]);
    
    python.on('close', (code) => {
        res.redirect('/');
    });
});

app.get('/make_file', (req, res) => {
    res.render('makeFile.ejs');
});

const upload2 = multer({ dest: 'filestore/' });
app.post('/make_file', upload2.array('file', 100), (req, res) => {
    console.log("파일업로드했습니다")
    console.log(req.files);
    const python = spawn('python', ['cpptotxt.py']);
    python.on('close', (code) => {
        res.render('downloadPage.ejs');
    });
});

app.use(function(req, res, next) {
    res.status(404);
    res.send(
		'<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">' +
		'<html><head><title>404 페이지 오류</title></head>' + 
		'<body><h1>찾을 수 없습니다</h1>' + 
		'<p>요청하신 URL ' + req.url + ' 을 이 서버에서 찾을 수 없습니다..</p><hr>' +
		'</body></html>'
	);
});

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});