require("dotenv").config({ path: ".env" });
var mongoose = require('mongoose')

try {
    mongoose.connect(process.env.ATLAS_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        dbName: "task_rating"
    });
    console.log('Database connected...');
} catch (err) {
    console.error('Can not establish connection ...');
}

const db = mongoose.connection;

module.exports = db 