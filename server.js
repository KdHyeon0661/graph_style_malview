const express = require('express');
const http = require('http');
var fs = require('fs');
const { spawn } = require('child_process');
const path = require("path");
const app = express()
const server = http.createServer(app)
const PORT = 8080

app.set('views', path.join(__dirname, './views'));
app.set('view engine', 'ejs');

app.use(express.static(__dirname + "/lib"));
app.use(express.json())
app.use(express.urlencoded({ extended: false }));

app.get('/', (req, res) => {
    const folder = './graph_folder';
    fs.readdir(folder, function (error, filelist) {
        res.render('mainPage', {gfile:filelist});
    });
});

app.get('/filecontents', (req, res) => {
    res.render('printFileContents');
});

app.post('/filecontents', (req, res) => {
    const a = new Date();

    let year = a.getFullYear();
    let month = a.getMonth() + 1;
    let date = a.getDate();
    let hours = a.getHours();
    let minutes = a.getMinutes();
    let seconds = a.getSeconds();
    let milliseconds = a.getMilliseconds();
    let nowV = year + '_' + month + '_' + date + '_' + hours + '_' + minutes + '_' + seconds + '_' + milliseconds;

    let folder = './text_file/';
    let file = nowV + '.txt';
    fs.open(folder + file, 'w', function (err, fd) {
        if (err) throw err;
        console.log('file open complete');
    });
    fs.writeFile(folder + file, req.body.filecontent, 'utf8', function (error) {
        console.log('write end')
    });
    const python = spawn('python', ['make_network_dummy.py', file]);
    
    python.on('close', (code) => {
        res.redirect('/');
    });
});

app.get('/:id', (req, res) => {
    var dataToSend;
    const python = spawn('python', ['beautiful.py', req.params.id]);
    fs.readFile('./storeValue/' + req.params.id.toString().split('.', 1) + '.txt', 'utf8', (err, data) => {
        dataToSend = data;
    });
    python.on('close', (code) => {
        res.render('printGraph', {whoAre:dataToSend});
    });
});

app.get('/volt_ready', (req, res) => {
    var dataToSend;
    // spawn new child process to call the python script
    const python = spawn('python', ['index.py']);
    // collect data from script
    python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
    });
    // in close event we are sure that stream from child process is closed
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataToSend)
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

server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});