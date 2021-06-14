import React from "react";
import DocumentById from "@diplomas/design-system/DocumentById";

export default function Diploma() {

  const props = {
    title: "Issuer Title",
    content: "Content Text",
    url: "issuer/documents",
    href: "/diplomas",
    showButtons:false,
    presentation: {
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

  }
  return (
    <DocumentById
      props={props}
    />
  );
}
