import React, { useEffect, useState, useCallback } from "react";
import Documents from "@diplomas/design-system/Documents"
import DiplomaItem from "issuer/components/diplomaItem";

export default function Diplomas() {
  const types = ['Bachelor', 'Master', 'Doctorate']
  const departments = ['Main', 'Science']
  const url ="issuer/documents";
  return (
    <>
      <Documents
        types={types}
        departments={departments}
        url={url}
      >
        <DiplomaItem />
      </Documents>
    </>
  );
}
