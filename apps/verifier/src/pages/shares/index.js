import React from "react";
import Documents from "@diplomas/design-system/Documents"
import SharedTitleItem from "verifier/components/SharedTitleItem";

export default function SharedTitle() {
  const types = ['Bachelor', 'Master', 'Doctorate']
  const departments = ['Main', 'Science']
  const url = "verifier/documents";
  const filterTitles = ["Τίτλοι Σπουδών", "Είδος τίτλου σπουδών", "Ίδρυμα/Σχολή"]
  return (
    <>
      <Documents
        types={types}
        departments={departments}
        url={url}
        filterTitles={filterTitles}
      >
        <SharedTitleItem />
      </Documents>
    </>
  );
}