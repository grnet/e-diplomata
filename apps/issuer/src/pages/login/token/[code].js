import React from 'react';
import { TokenLogin } from '@digigov/auth';
import { useRouter } from 'next/router';

export default function MyTokenLogin() {
  const router = useRouter();
  const { code } = router.query;
  return <TokenLogin code={code} />;
}
