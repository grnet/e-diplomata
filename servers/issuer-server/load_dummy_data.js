const Datastore = require("nedb");

const valuePool = {
  degree: ["engineer", "architec"],
  typeOfDegree: ["programmer", "architec"],
  school: ["immi", "architectoniki"],
  institution: ["tuc", "assoe"],
  status: ["unawarded"],
  userName: ["giannis", "giorgos", "panagiotis"],
  year: ["2005", "2006", "2007"],
};
const diplomas = new Array(11).fill({}).map((item, index) => {
  return {
    degree:
      valuePool.degree[Math.floor(Math.random() * valuePool.degree.length)],
    typeOfDegree:
      valuePool.typeOfDegree[
        Math.floor(Math.random() * valuePool.typeOfDegree.length)
      ],
    school:
      valuePool.school[Math.floor(Math.random() * valuePool.school.length)],
    institution:
      valuePool.institution[
        Math.floor(Math.random() * valuePool.institution.length)
      ],
    status:
      valuePool.status[Math.floor(Math.random() * valuePool.status.length)],
    userName:
      valuePool.userName[Math.floor(Math.random() * valuePool.userName.length)],
    year: valuePool.year[Math.floor(Math.random() * valuePool.year.length)],
  };
});

const database = new Datastore("diplomas.db");
/* database.persistence.compactDatafile();
database.persistence.setAutocompactionInterval( 500); */
database.loadDatabase(function (error) {
  if (error) {
    console.log(
      "FATAL: local database could not be loaded. Caused by: " + error
    );
  } else {
    console.log("INFO: local database loaded successfully.");
  }
});

database.insert(diplomas, function (error) {
  if (error) {
    console.log("ERROR: saving document caused by: " + error);
  } else {
    console.log("INFO: successfully saved document");
  }
});
