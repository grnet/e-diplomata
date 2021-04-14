export const datasets = {
  degree: [
    { label: "Μηχανικος", value: "engineer" },
    { label: "Αρχιτεκτονας", value: "architec" },
  ],
  typeOfDegree: [
    { label: "Προγραμματιστης", value: "programmer" },
    { label: "Αρχιτεκτονας", value: "architec" },
  ],
  school: [
    { label: "ΗΜΜΥ", value: "immi" },
    { label: "Αρχιτεκτονικής", value: "architectoniki" },
  ],
  institution: [
    { label: "TUC", value: "tuc" },
    { label: "ΑΣΣΟΕ", value: "assoe" },
  ],
};

export default async function handler(req, res) {
  return res.status(200).json(datasets);
}
