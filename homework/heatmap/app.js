const express = require("express")
const app = express()
const http = require("http").Server(app)
const io = require("socket.io")(http)
const bodyParser = require("body-parser");

let PORT = 50001

app.use("/style", express.static(__dirname + "/style"))
app.use("/js", express.static(__dirname + "/js"))
app.use("/gui", express.static(__dirname + "/gui"))

app.use(bodyParser.urlencoded({extended : true}))
app.use(bodyParser.json())

app.get("/", (req, res) => res.sendFile(__dirname + "/index.html"))
app.get("/vector", (req, res) => res.sendFile(__dirname + "/vector.html"))

app.post('/message', (req, res) => {
    io.emit('message', req.body)
})

app.post('/init', (req, res) => {
   io.emit('init', req.body)
})

http.listen(PORT, () => console.log(`listening on ${PORT} ...`))

io.on("connection", (socket) => {
    /*socket.on('message', (msg) => {
        io.emit("message", msg)
    })*/

})

