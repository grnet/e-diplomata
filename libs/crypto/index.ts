import zerorpc from "zerorpc";
import { CryptoInterface, Key } from "@diplomas/protocol";
const ZERORPCURI = process.env.ZERORPCURI || "tcp://127.0.0.1:4242"
const client = new zerorpc.Client();
client.connect(ZERORPCURI);

const DiplomasCrypto = new Proxy(client, {
  get(target, func){
    return function (...args){
      return new Promise((resolve, reject)=>{
        target.invoke(func, ...args, function(error, res){
          if(error){
            reject(error)
          }
          resolve(res)
        })
      })
    }
  }
})

export default class Crypto implements CryptoInterface {
  generateKeys(){
    return DiplomasCrypto.generate_keys()
  }
  computeAward(document: any, issuerKey: Key){
    return DiplomasCrypto.publish_award(document, issuerKey)
  }
  computeRequest(
    s_awd: string, 
    c: string, 
    verifierPub: Key, 
    holderKey: Key
  ) { 
    return DiplomasCrypto.publish_request(
      s_awd, 
      holderKey,
      c, 
      verifierPub,
    )  
  }
  computeProof(
    s_req: string, 
    r: string, 
    c: string,
    s_awd: string,
    verifierPub: Key, 
    issuerKey: Key
  ) { 
    return DiplomasCrypto.publish_proof(
      s_req,
      r, 
      c, 
      issuerKey, 
      verifierPub, 
      s_awd
    )
  }
  computeAck (
    document: string, 
    s_prf: string, 
    proof: any,
    s_req: string,
    issuerPub: Key, 
    verifierKey: Key
  )  { 
    return DiplomasCrypto.publish_ack(
      s_prf, 
      document, 
      proof, 
      issuerPub, 
      verifierKey, 
      s_req
    )  
  }
}