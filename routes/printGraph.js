var express = require('express');
var fs = require('fs');
const { spawn } = require('child_process');

var router = express.Router();

router.use(express.static('public'));
router.use(express.json())
router.use(express.urlencoded({ extended: false }));

router.get("/:id", (req, res) => {
    let dataToSend;
    let text_file;
    const python = spawn('python', ['beautiful.py', req.params.id]);
    fs.readFile('./storeValue/' + req.params.id.toString().split('.', 1) + '.txt', 'utf8', (err, data) => {
        dataToSend = data;
    });
    fs.readFile('./text_file/' + req.params.id.toString().split('.', 1) + '.txt', 'utf8', (err, data) => {
        text_file = data;
    });
    
    python.on('close', (code) => {
        res.render('printGraph.ejs', {whoAre:req.params.id.toString().split('.', 1), whoAre2:dataToSend, thisname:text_file});
    });
});

router.post("/:id", (req, res) => {
    var filename = req.params.id.toString() + '.txt';

    const python = spawn('python', ['make_network_dummy.py', filename, parseFloat(req.body.t2_threshold).toFixed(2), parseFloat(req.body.e2_threshold).toFixed(2)]);
    python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        res.redirect('/printGraph/' + req.params.id.toString().split('.', 1) + '.html');
    });
});

module.exports = router;