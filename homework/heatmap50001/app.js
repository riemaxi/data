const express = require("express")
const app = express()
const http = require("http").Server(app)
const io = require("socket.io")(http)
const bodyParser = require("body-parser");

let PORT = 50001

app.use("/assets", express.static(__dirname + "/assets"))
app.use(bodyParser.urlencoded({extended : true}))
app.use(bodyParser.json())
app.get("/", (req, res) => res.sendFile(__dirname + "/index.html"))
app.post('/message', (req, res) => {
    console.log(req.body)

    io.emit('message', req.body)
})

http.listen(PORT, () => console.log(`listening on ${PORT} ...`))

io.on("connection", (socket) => {
    socket.on('message', (msg) => {
        io.emit("message", msg)
    })
})

