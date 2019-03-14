const express = require("express")
const app = express()
const http = require("http").Server(app)
const io = require("socket.io")(http)
const bodyParser = require("body-parser");
const fs = require('fs')
const readline = require('readline');

let PORT = 50001

function emitVectors(path, ev){
 path = __dirname + '/data/' + path

 var rd = readline.createInterface({
    input: fs.createReadStream(path),
    //output: process.stdout,
    console: false
 })

 rd.on('line', function(line) {
  io.emit(ev, line)
 })
}

app.use("/style", express.static(__dirname + "/style"))
app.use("/js", express.static(__dirname + "/js"))
app.use("/gui", express.static(__dirname + "/gui"))

app.use(bodyParser.urlencoded({extended : true}))
app.use(bodyParser.json())

app.get("/", (req, res) => res.sendFile(__dirname + "/index.html"))
app.get("/vector", (req, res) => res.sendFile(__dirname + "/vector.html"))
app.get("/stairs", (req, res) => res.sendFile(__dirname + "/stairs.html"))
app.get("/alignment", (req, res) => res.sendFile(__dirname + "/alignment.html"))
app.get("/dalignment", (req, res) => res.sendFile(__dirname + "/dalignment.html"))
app.get("/heatmap", (req, res) => res.sendFile(__dirname + "/heatmap.html"))

app.post('/message', (req, res) => {
    io.emit('message', req.body)
})

app.post('/init', (req, res) => {
   io.emit('init', req.body)
})

http.listen(PORT, () => console.log(`listening on ${PORT} ...`))

io.on("connection", (socket) => {
    socket.on('stairs', (msg) => {
        emitVectors('stairs.txt','stairs')
    })

    socket.on('align', () => {
	emitVectors("align.txt", 'align')
    })

    socket.on('dalign', () => {
	emitVectors("dalign.txt", 'dalign')
    })


    socket.on('heatmap', () => {
	emitVectors("heatmap.txt", 'heatmap')
    })

})

