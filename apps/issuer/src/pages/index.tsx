import React from 'react';
import StartPage from "@diplomas/design-system/StartPage";


export default function Index() {
  return (
    <>
      <StartPage
        title = "Ediplomas issuer service"
        text = "You can issue diploma in the blockchain"
        href ="/login?next=/diplomas"
      />
    </>
  );
}
