require("dotenv").config({ path: ".env" });

const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
const ratingRouter = require('./routes/ratingRouter');

const app = express();
const PORT = process.env.PORT;
const HOST = process.env.HOST;

app.use(bodyParser.json());
app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static("dist"));

//Routes
app.use(ratingRouter);

app.listen(PORT, () => {
  console.log(`Listen to ${HOST}:${PORT}`);
});
