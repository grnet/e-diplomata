import React from "react";
import DocumentById from "@diplomas/design-system/DocumentById";

export default function Title() {

  const props = {
    title: "Issuer Title",
    content: "Content Text",
    url: "titles",
    href: "/titles",
    showButtons: false,
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

