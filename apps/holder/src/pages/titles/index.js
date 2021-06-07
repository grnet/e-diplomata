import React from "react";
import Documents from "@diplomas/design-system/Documents"
import TitleItem from "holder/components/TitleItem";

export default function Titles() {
  const types = ['Bachelor', 'Master', 'Doctorate']
  const departments = ['Main', 'Science']
  const url = "holder/documents";
  const filterTitles = ["Τίτλοι Σπουδών", "Είδος τίτλου σπουδών", "Ίδρυμα/Σχολή"]
  return (
    <>
      <Documents
        types={types}
        departments={departments}
        url={url}
        filterTitles={filterTitles}
      >
        <TitleItem />
      </Documents>
    </>
  );
}

