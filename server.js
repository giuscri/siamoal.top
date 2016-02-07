var fs = require('fs')
var express = require('express')
var app = express();

base_url = 'http://audio.radio24.ilsole24ore.com/radio24_audio'

app.get('/', function (req, res) {
    var _res = res;
    _res.set({'Access-Control-Allow-Origin': '*'});
    fs.readFile('episodes.timestamp', 'utf-8', function (err, res) {
        if (err) { return err; }
        var lns = res.trim().split('\n')
        var inx = Math.floor(Math.random() * lns.length);
        var url = base_url;
        url = [url, lns[inx].split('-')[0]].join('/');
        url = [url, lns[inx].split('-').join('').slice(2)].join('/');
        url = [url, 'lazanzara.mp3'].join('-');
        return _res.send({
            timestamp: lns[inx],
            src: url,
        });
    });
});

app.listen(3000);
console.log('[DEBUG] Listening on port 80 ...');
