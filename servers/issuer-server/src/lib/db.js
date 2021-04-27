const Datastore = require("nedb");

const database = new Datastore("diplomas.db");
database.loadDatabase(function (error) {
  if (error) {
    console.log(
      "FATAL: local database could not be loaded. Caused by: " + error
    );
  } else {
    console.log("INFO: local database loaded successfully.");
  }
});

export default database;
