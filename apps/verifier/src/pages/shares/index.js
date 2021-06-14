import React from "react";
import Documents from "@diplomas/design-system/Documents";
import SharedTitleItem from "verifier/components/SharedTitleItem";

export default function SharedTitle() {
  const types = ['Bachelor', 'Master', 'Doctorate'];
  const departments = ['Main', 'Science'];
  const dataFilters = [{ title: "Είδος τίτλου σπουδών", filterData: types, filterTypeData: "type" }, { title: "Ίδρυμα/Σχολή", filterData: departments, filterTypeData: "department" }];
  const url = "verifier/documents/shares";
  const title = "Τίτλοι Σπουδών";
  const presentation = {
    url: (row) => `/diplomas/${row._id}`,
    fields: [
      {
        label: 'Τιτλος σπουδων',
        key: 'title'
      },
      {
        label: 'Είδος τίτλου Σπουδών',
        key: 'type'
      },
      {
        label: 'Τμήμα/Σχολή',
        key: 'department'
      }
    ]
  }

  return (
    <>
      <Documents
        dataFilters={dataFilters}
        url={url}
        title={title}
        presentation={presentation}
      >
       </Documents>
    </>
  );
}