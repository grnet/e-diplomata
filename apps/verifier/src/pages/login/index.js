import React from "react";
import Login from "@diplomas/design-system/Login";
import { useResource } from "@digigov/ui/api";

export default function Index() {
  const { data } = useResource('verifier/dummy_credentials');
  const url = '/api/verifier/login';
  const type = "Verifier";
  return (
    <>
      <Login
        data={data}
        url={url}
        type={type}
      />
    </>

  );
}