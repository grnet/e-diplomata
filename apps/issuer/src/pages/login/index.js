import React from "react";
import Login from "@diplomas/design-system/Login";
import { useResource } from "@digigov/ui/api";

export default function Index() {
  const { data } = useResource('issuer/dummy_credentials');
  const url = '/api/issuer/login';
  const type = "Issuer";
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
