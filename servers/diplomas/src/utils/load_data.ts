import { HolderUser as Holder, IssuerUser as Issuer, Document, VerifierUser as Verifier } from '@diplomas/server/models';
import bcrypt from "bcryptjs";
import { holderCredentials, verifierCredentials, issuerCredentials } from '@diplomas/server/utils/dummy_credentials';
import Crypto from '@diplomas/crypto';
import Ledger from '@diplomas/ledger';
import { Profile } from '@diplomas/server/models';

import {InitiateMongoServer} from '@diplomas/server/config/db'
const titles = ['Mechanical Engineer', 'Accountant', 'Logistics', 'Doctor']
const deans = ['Nikos Gryspos', 'Maria Lekousi', 'Avgerinos Lokos']
const loadData = async () => {
  await InitiateMongoServer();
  console.log('dropping collections')
  try{
    await Holder.collection.drop()
    await Issuer.collection.drop()
    await Verifier.collection.drop()
    await Document.collection.drop()
    await Profile.collection.drop()
  }
  catch(e){

  }
  const salt = await bcrypt.genSalt(10);
  const crypto = new Crypto()
  
  console.log('create holders')
  const holdersData = await Promise.all(holderCredentials.map(async (holder) => {
    console.log(holder.email)
    const keys = await crypto.generateKeys()
    return {
      ...holder,
      password: bcrypt.hashSync(holder.password, salt),
      publicKey: keys.public.join('-'),
      keys: {
        crypto: keys,
        wallet: await Ledger.generateWallet({networkType: 'ganache', party: 'Holder'})
      }
    }
  }));
  const holderProfiles = holdersData.map((holder) => {
    console.log(holder.email)
    return {
      title: `${holder.firstName} ${holder.lastName}`,
      publicKey: holder.keys.crypto.public.join('-'),
      walletAddress: holder.keys.wallet.public,
      service: 'http://localhost:5000',
      type: 'Holder',
    }
  });
  const holders = await Holder.insertMany(holdersData) as any;
  console.log(holders)
  console.log('create verifiers')

  const verifiersData = await Promise.all(verifierCredentials.map(async (verifier) => {
    console.log(verifier.email)
    const keys = await crypto.generateKeys()
    return {
      ...verifier,
      password: bcrypt.hashSync(verifier.password, salt),
      publicKey: keys.public.join('-'),
      keys: {
        crypto: keys,
        wallet: await Ledger.generateWallet({networkType: 'ganache', party: 'Verifier'})
      }
    }
  }));
  const verifierProfiles = verifiersData.map((verifier) => {
    console.log(verifier.email)
    return {
      title: verifier.title,
      publicKey: verifier.keys.crypto.public.join('-'),
      walletAddress: verifier.keys.wallet.public,
      service: 'http://localhost:5000',
      type: 'Verifier',
    }
  });
  await Verifier.insertMany(verifiersData);
  console.log('create issuers')

  const issuersData = await Promise.all(issuerCredentials.map(async (issuer) => {
    console.log(issuer.email)
    const keys = await crypto.generateKeys()

    return {
      ...issuer,
      password: bcrypt.hashSync(issuer.password, salt),
      publicKey: keys.public.join('-'),
      keys: {
        crypto: keys,
        wallet: await Ledger.generateWallet({networkType: 'ganache', party: 'Issuer'})
      }
    }
  }));
  const issuerProfiles = issuersData.map((issuer) => {
    console.log(issuer.email)
    return {
      title: issuer.title,
      publicKey: issuer.keys.crypto.public.join('-'),
      walletAddress: issuer.keys.wallet.public,
      service: 'http://localhost:5000',
      type: 'Issuer',
    }
  });
  const issuers = await Issuer.insertMany(issuersData) as any
  await Profile.insertMany([...holderProfiles, ...verifierProfiles, ...issuerProfiles])
  for (const issuer of issuers) {
    for (const holder of holders) {
      await issuer.createQualification({
        title: titles[Math.floor(Math.random() * titles.length)],
        type: 'Bsc',
        department: 'Main',
        grade: Math.floor(Math.random() * 10),
        degreeDate: Date.now(),
        dean: deans[Math.floor(Math.random() * deans.length)],
        certificateNumber: Math.floor(Math.random() * 1000),
        supervisors: 'Kostas Minos'
      }, holder.publicKey)
      // console.log(qualification)
    }
  }
  console.log('Loaded!')
  process.exit()
}
loadData()