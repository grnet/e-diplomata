
const mongoose = require("mongoose");

// Replace this with your MONGOURI.
const MONGOURI = "mongodb://localhost:27017";

const InitiateMongoServer = async (uri) => {
  try {
    return await mongoose.connect(uri || MONGOURI, {
      useNewUrlParser: true,
      useUnifiedTopology: true
    });
  } catch (e) {
    console.log(e);
    throw e;
  }
};

module.exports = InitiateMongoServer;