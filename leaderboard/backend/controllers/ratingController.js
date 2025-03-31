const db = require('../db/database')

const ratingCollection = db.collection("informal")

async function getAllRating (req, res) { 
    try {
      const ratings = await ratingCollection.find({}).toArray();
      res.status(200).send(ratings);
    } catch (error) {
      res.status(500).send(error);
    }
}

module.exports = {
    getAllRating
}