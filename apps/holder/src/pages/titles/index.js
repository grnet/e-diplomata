import React from "react";
import Documents from "@diplomas/design-system/Documents";
import TitleItem from "holder/components/TitleItem";

export default function Titles() {
  const types = ['Bachelor', 'Master', 'Doctorate'];
  const departments = ['Main', 'Science'];
  const dataFilters = [{ title: "Είδος τίτλου σπουδών", filterData: types, filterTypeData: "type" }, { title: "Ίδρυμα/Σχολή", filterData: departments, filterTypeData: "department" }];
  const url = "holder/documents";
  const title = "Τίτλοι Σπουδών";
  const presentation = {
    url: (row) => `/titles/${row._id}`,
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

