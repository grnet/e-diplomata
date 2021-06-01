import { Holder, Issuer, Document } from '../models';
import bcrypt from "bcryptjs";
import { holderCredentials, verifierCredentials, issuerCredentials } from '@diplomas/core/utils/dummy_credentials';

Document.collection.drop();
Holder.collection.drop();
Issuer.collection.drop();

const InitiateMongoServer = require("../config/db");
InitiateMongoServer();
// import diplomata from '@diplomas/crypto';
// import ledger from '@diplomas/ledger';
const diplomata = {
  generate_keys: (type?: string) => {
    return {
      private: ['a string'],
      public: ['another string', type]
    }
  }
}
const ledger = diplomata

const titles = ['Mechanical Engineer', 'Accountant', 'Logistics', 'Doctor']
const deans = ['Nikos Gryspos', 'Maria Lekousi', 'Avgerinos Lokos']
const types = ['Bachelor','Master', 'Doctorate']
const departments = ['Main', 'Science']
const loadData = async () => {
  const salt = await bcrypt.genSalt(10);

  const holdersData = holderCredentials.map((holder) => {
    return {
      ...holder,
      password: bcrypt.hashSync(holder.password, salt),
      keys: {
        crypto: diplomata.generate_keys(),
        wallet: ledger.generate_keys('holder')
      }

    }
  });

  const holders = await Holder.insertMany(holdersData);

  const verifiersData = verifierCredentials.map((verifier) => {
    return {
      ...verifier,
      password: bcrypt.hashSync(verifier.password, salt),
      keys: {
        crypto: diplomata.generate_keys(),
        wallet: ledger.generate_keys('verifier')
      }
    }
  });

  const verifiers = await Holder.insertMany(verifiersData);

  const issuersData = issuerCredentials.map((issuer) => {
    return {
      ...issuer,
      password: bcrypt.hashSync(issuer.password, salt),
      keys: {
        crypto: diplomata.generate_keys(),
        wallet: ledger.generate_keys('issuer')
      }
    }
  });
  
  const issuers = await Issuer.insertMany(issuersData)
  for (const issuer of issuers) {
    for (const holder of holders) {
      
      const qualification = await issuer.createQualification({
        title: titles[Math.floor(Math.random() * titles.length)],
        type: types[Math.floor(Math.random() * types.length)],
        department: departments[Math.floor(Math.random() * departments.length)],
        grade: Math.floor(Math.random() * 10),
        degreeDate: Date.now(),
        dean: deans[Math.floor(Math.random() * deans.length)],
        certificateNumber: Math.floor(Math.random() * 1000),
        supervisors: 'Kostas Minos'
      }, holder.email)
      console.log(qualification)
    }
  }
  console.log(holders, issuers, verifiers,)
}
loadData()