const Datastore = require("nedb");

const database = new Datastore({ filename: "diplomas.db", autoload: true });

const db = () => {
  return database;
}

database.persistence.compactDatafile();

export default db;
