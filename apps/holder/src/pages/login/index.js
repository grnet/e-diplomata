import React from "react";
import Login from "@diplomas/design-system/Login";
import { useResource } from "@digigov/ui/api";

export default function Index() {
  const { data } = useResource('holder/dummy_credentials');
  const url = '/api/holder/login';
  const type = "Holder";
  return (
    <>
      <Login
        data={data}
        url={url}
        type ={type}
      />
    </>

  );
}
