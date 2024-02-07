// write a nodejs server that will expose a method call "get" that will return the value of the key passed in the query string
// example: http://localhost:3000/get?key=hello
// if the key is not passed, return "key not passed"
// if the key is passed, return "hello" + key
// if the url has other methods, return "method not supported"
// when server is listening, log "server is listening on port 3000"

const server = require('http').createServer((req, res) => {
    const url = require('url').parse(req.url, true);
    const query = url.query;
    if (url.pathname === '/get') {
        if (query.key) {
            res.end('hello ' + query.key);
        } else {
            res.end('key not passed');
        }
    } else {
        res.end('method not supported');
    }
});

// generate 

