const express = require("express")
const app = express()
const http = require("http").Server(app)

let PORT = 50010

app.use("/style", express.static(__dirname + "/style"))
app.use("/js", express.static(__dirname + "/js"))

app.get("/", (req, res) => res.sendFile(__dirname + "/index.html"))
app.get("/epsilon", (req, res) => res.sendFile(__dirname + "/epsilon.html"))
app.get("/heatmap", (req, res) => res.sendFile(__dirname + "/heatmap.html"))
app.get("/heatmapzero", (req, res) => res.sendFile(__dirname + "/heatmapzero.html"))
app.get("/heatmapmut", (req, res) => res.sendFile(__dirname + "/heatmapmutation.html"))

http.listen(PORT, () => console.log(`listening on ${PORT} ...`))
