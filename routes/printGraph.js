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
    let value;
    let filename;

    fs.readFile('./storeValue/' + req.params.id.toString().split('.', 1) + '.txt', 'utf8', (err, data) => {
        if (err) {
            console.error(err);
            return res.status(500).send("Internal Server Error");
        }

        dataToSend = data;

        let firstNewlineIndex = dataToSend.indexOf("\n");
        let secondNewlineIndex = dataToSend.indexOf("\n", firstNewlineIndex + 1);
        filename = dataToSend.substring(0, firstNewlineIndex).split(',')[2];
        let result = dataToSend.substring(firstNewlineIndex + 1, secondNewlineIndex)
        value = result.split(',');

        fs.readFile('./text_file/' + req.params.id.toString().split('.', 1) + '.txt', 'utf8', (err, data) => {
            if (err) {
                // 에러 처리
                console.error(err);
                return res.status(500).send("Internal Server Error");
            }

            text_file = data;

            const python = spawn('python', ['beautiful.py', req.params.id]);

            python.on('close', (code) => {
                res.render('printGraph.ejs', {whoAre:req.params.id.toString().split('.', 1), whoAre2:dataToSend, thisname:text_file, a:value[0], b:value[1].replace(/\r/g, ''), c:filename});
            });
        });
    });
});

router.post("/:id", (req, res) => {
    var filename = req.params.id.toString().split('.', 1) + '.txt';
    const python = spawn('python', ['make_network_dummy.py', filename.toString(), parseFloat(req.body.threshold).toFixed(3), parseFloat(req.body.edge_print_threshold).toFixed(3), req.body.filename, req.body.metric]);
    
    python.stderr.on('data', (data) => {
        console.error(`오류 발생: ${data}`);
    });

    python.on('close', (code) => {
        console.log(`파이썬 프로세스 종료, 종료 코드: ${code}`);
        res.redirect('/');
    });
});

module.exports = router;