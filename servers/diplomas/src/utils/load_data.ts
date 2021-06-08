import { Holder, Issuer } from '../models';
import bcrypt from "bcryptjs";
const InitiateMongoServer = require("../config/db");
InitiateMongoServer();
// import diplomata from '@diplomas/crypto';
// import ledger from '@diplomas/ledger';
const diplomata = {
  generate_keys: (type?: string)=>{
    return {
      private: ['a string'],
      public: ['another string', type]
    }
  }
}
const ledger = diplomata

const titles = ['Mechanical Engineer', 'Accountant', 'Logistics', 'Doctor']
const deans = ['Nikos Gryspos', 'Maria Lekousi', 'Avgerinos Lokos']
const loadData = async ()=>{
  const salt = await bcrypt.genSalt(10);
  const holdersData = [
    {
      firstName: 'Mario',
      lastName: 'Menexe',
      fatherName: 'Niko',
      email: 'mario@menexe.com',
      password: await bcrypt.hash('1234567', salt),
      keys: {
        crypto: await diplomata.generate_keys(),
        wallet: await ledger.generate_keys('holder')
      }
    },
    {
      firstName: 'Aggeliki',
      lastName: 'Antoniou',
      fatherName: 'Billy',
      email: 'aggeliki@antoniou.com',
      password: await bcrypt.hash('1234567', salt),
      keys: {
        crypto: await diplomata.generate_keys(),
        wallet: await ledger.generate_keys('holder')
      }
    },
    {
      firstName: 'Nikos',
      lastName: 'Likos',
      fatherName: 'Zonni',
      email: 'nikos@likos.com',
      password: await bcrypt.hash('1234567', salt),
      keys: {
        crypto: await diplomata.generate_keys(),
        wallet: await ledger.generate_keys('holder')
      }
    },
    {
      firstName: 'Antonia',
      lastName: 'Vazelou',
      fatherName: 'Nikos',
      email: 'antonia@vazelou.com',
      password: await bcrypt.hash('1234567', salt),
      keys: {
        crypto: await diplomata.generate_keys(),
        wallet: await ledger.generate_keys('holder')
      }
    },
    {
      firstName: 'Olga',
      lastName: 'Feretou',
      fatherName: 'Dimos',
      email: 'olga@feretou.com',
      password: await bcrypt.hash('1234567', salt),
      keys: {
        crypto: await diplomata.generate_keys(),
        wallet: await ledger.generate_keys('holder')
      }
    },
  ]
  const holders = await Holder.insertMany(holdersData)
  const verifiersData = [
    {
      title: 'My Company',
      email: 'root@mycompany.com',
      password: await bcrypt.hash('1234567', salt),
      keys: {
        crypto: await diplomata.generate_keys(),
        wallet: await ledger.generate_keys('verifier')
      }
    },
    {
      title: 'Happy Company',
      email: 'root@happycompany.com',
      password: await bcrypt.hash('1234567', salt),
      keys: {
        crypto: await diplomata.generate_keys(),
        wallet: await ledger.generate_keys('holder')
      }
    },
    {
      title: 'State Desk',
      email: 'root@statedesk.gr',
      password: await bcrypt.hash('1234567', salt),
      keys: {
        crypto: await diplomata.generate_keys(),
        wallet: await ledger.generate_keys('holder')
      }
    },
  ]
  const verifiers = await Holder.insertMany(verifiersData)
  const issuersData = [
    {
      title: 'University of Athens',
      email: 'root@uoa.gr',
      password: await bcrypt.hash('1234567', salt),
      keys: {
        crypto: await diplomata.generate_keys(),
        wallet: await ledger.generate_keys('issuer')
      }
    },
    {
      title: 'University of Crete',
      email: 'root@uoc.gr',
      password: await bcrypt.hash('1234567', salt),
      keys: {
        crypto: await diplomata.generate_keys(),
        wallet: await ledger.generate_keys('issuer')
      }
    },
  ]
  const issuers = await Issuer.insertMany(issuersData)
  for (const issuer of issuers){
    for(const holder of holders){
      const qualification = await issuer.createQualification({
        title: titles[Math.floor(Math.random() * titles.length)],
        type: 'Bsc',
        department: 'Main',
        grade: Math.floor(Math.random() * 10),
        degreeDate: Date.now(),
        dean: deans[Math.floor(Math.random() * deans.length)],
        certificateNumber: Math.floor(Math.random() * 1000),
        supervisors: 'Kostas Minos'
      }, holder.email)
      console.log(qualification)
    }
  }
  console.log(holders, issuers, verifiers, )
}
loadData()