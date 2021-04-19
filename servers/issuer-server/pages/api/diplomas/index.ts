/* export const diplomas = [
  {
    id: 1,
    degree: "Μηχανικος",
    typeOfDegree: "Πολιτικός Μηχανικός",
    school: "ΜΠΔ",
    institution: "TUC",
    status: "έγκριση",
    userName: "Νίκος Γκάλης",
    year: "2000",
  },
  {
    id: 2,
    degree: "Μηχανικος",
    typeOfDegree: "Πληροφορική",
    school: "ΜΗΠΕΡ",
    institution: "TUC",
    status: "σε εκκρεμότητα",
    userName: "Παναγίωτης Φασούλας",
    year: "2004",
  },
  {
    id: 3,
    degree: "Μηχανικος",
    typeOfDegree: "Πληροφορική",
    school: "ΗΜΜΥ",
    institution: "ΑΣΟΕΕ",
    status: "έγκριση",
    userName: "Παναγιώτης Γιαννάηκης",
    year: "2003",
  },
  {
    id: 4,
    degree: "Μηχανικος",
    typeOfDegree: "Πολιτικός Μηχανικός",
    school: "ΗΜΜΥ",
    institution: "ΑΣΟΕΕ",
    status: "σε εκκρεμότητα",
    userName: "Λευτέρης Μπακατσιάς",
    year: "2002",
  },
]; */

export const valuePool = {
  degree: ["enginner", "architec"],
  typeOfDegree: ["programmer", "architec"],
  school: ["immi", "architectoniki"],
  institution: ["tuc", "assoe"],
  status: ["approved", "pending"],
  userName: ["giannis", "giorgos", "panagiotis"],
  year: ["2005", "2006", "2007"],
};
export const diplomas = new Array(100).fill({}).map((item, index) => {
  return {
    id: `${index}`,
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

/* export default async function handler(req, res) {
  let response = null;
  if (req.method === "POST") {
    // Process a POST request
    response = res.status(200).json({ ok: true });
  } else {
    const limit = parseInt(req.query.limit) || 10;
    const offset = parseInt(req.query.offset) || 0;
    const requestedDiplomas = diplomas
      .filter((item) => {
        return Object.values(item).join(" ").includes(req.query.search);
      })
      .slice(offset, offset + limit);
    response = res.send({
      data: requestedDiplomas,
      meta: {
        total: diplomas.length / limit,
        count: diplomas.length,
      },
    });
  }
  return response;
} */

export default async function handler(req, res) {
  let response = null;
  if (req.method === "POST") {
    // Process a POST request
    response = res.status(200).json({ ok: true });
  } else {
    const limit = parseInt(req.query.limit) || 10;
    const offset = parseInt(req.query.offset) || 0;
    const requestedDiplomas = diplomas
      .filter((item) => {
        const queryKeys = Object.keys(req.query);
        console.log("req query is ", req.query);
        console.log("queryKeys is ", queryKeys);
        return !queryKeys.some((key) => {
          if (["limit", "offset"].includes(key)) {
            return false;
          }
          if (key === "search") {
            if (req.query[key]) {
              return !Object.values(item).join(" ").includes(req.query.search);
            } else {
              return false;
            }
          } else {
            if (req.query[key]) {
              return item[key] !== req.query[key];
            } else {
              return false;
            }
          }
        });
      })
      .slice(offset, offset + limit);
    response = res.send({
      data: requestedDiplomas,
      meta: {
        total: diplomas.length / limit,
        count: diplomas.length,
      },
    });
  }
  return response;
}