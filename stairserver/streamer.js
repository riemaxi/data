const express = require("express")
const app = express()
const http = require("http").Server(app)
const io = require("socket.io")(http)
const bodyParser = require("body-parser");

let PORT = 5000

app.use("/style", express.static(__dirname + "/style"))
app.use(bodyParser.urlencoded({extended : true}))
app.get("/", (req, res) => res.sendFile(__dirname + "/index.html"))
app.post('/message', (req, res) => {
    console.log(req.body.data)
    io.emit('message', req.body)
})

http.listen(PORT, () => console.log(`listening on ${PORT}`))

io.on("connection", (socket) => {

    console.log('new connection')

    socket.on('message', (msg) => {
        io.emit("message", msg)
    })
})

