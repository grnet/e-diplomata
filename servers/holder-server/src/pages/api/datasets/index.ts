export const datasets = {
  typeOfDegree: [
    { label: "Προγραμματιστής", value: "programmer" },
    { label: "Αρχιτέκτονας", value: "architec" },
  ],
  school: [
    { label: "ΗΜΜΥ", value: "immi" },
    { label: "Αρχιτεκτονική", value: "architectoniki" },
  ],
  institution: [
    { label: "TUC", value: "tuc" },
    { label: "ΑΣΣΟΕ", value: "assoe" },
  ],
};

export default async function handler(req, res) {
  return res.status(200).json(datasets);
}
