import React from "react";
import Documents from "@diplomas/design-system/Documents";
import DiplomaItem from "issuer/components/diplomaItem";

export default function Diplomas() {
  const types = ['Bachelor', 'Master', 'Doctorate'];
  const departments = ['Main', 'Science'];
  const dataFilters = [{ title: "Είδος τίτλου σπουδών", filterData: types, filterTypeData: "type" }, { title: "Ίδρυμα/Σχολή", filterData: departments, filterTypeData: "department" }];
  const url ="issuer/documents";
  const title = "Τίτλοι Σπουδών";
  return (
    <>
      <Documents
        dataFilters={dataFilters}
        url={url}
        title={title}
      >
        <DiplomaItem />
      </Documents>
    </>
  );
}
