const express = require("express");
const router = express.Router();
const ratingController = require("../controllers/ratingController");

router.get("/api/v1/rating", ratingController.getAllRating);

module.exports = router;