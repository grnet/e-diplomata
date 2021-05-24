const Datastore = require("nedb");

const valuePool = {
  degree: ["engineer", "architec"],
  typeOfDegree: ["programmer", "architec"],
  school: ["immi", "architectoniki"],
  institution: ["tuc", "assoe"],
  firstName: ["Giannis", "Giorgos", "Panagiotis"],
  lastName: ["fasoulas", "bakatsias", "papanagiotou"],
  fatherName: ["Nikos", "Kwstas", "Ilias"],
  numberOfDegree: ["7", "8", "9"],
  rector: ["tuc", "assoe"],
  year: ["2005", "2006", "2007"],
  status: ["unawarded", "success", "failed"],
};
const diplomas = new Array(25).fill({}).map((item, index) => {
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
    firstName:
      valuePool.firstName[Math.floor(Math.random() * valuePool.firstName.length)],
    lastName:
      valuePool.lastName[Math.floor(Math.random() * valuePool.lastName.length)],
    fatherName:
      valuePool.fatherName[Math.floor(Math.random() * valuePool.fatherName.length)],
    numberOfDegree: valuePool.numberOfDegree[Math.floor(Math.random() * valuePool.numberOfDegree.length)],
    rector: valuePool.rector[Math.floor(Math.random() * valuePool.rector.length)],
    year: valuePool.year[Math.floor(Math.random() * valuePool.year.length)],
  };
});

const database = new Datastore("titles.db");
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