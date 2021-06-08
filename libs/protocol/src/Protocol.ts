import { CryptoInterface, Key } from "./Crypto";
import {  LedgerInterface } from "./Ledger";
import { MessagingInterface } from "./Messaging";
import { StorageEntry, StorageInterface } from "./Storage";


export interface UserInterface {
  pubKey: string
  keys: {
    crypto: {
      private: string[]
    }
  }
}

export interface ProtocolInterfaceConstructor {
  storage: StorageInterface;
  ledger: LedgerInterface;
  messaging: MessagingInterface;
  crypto: CryptoInterface;
  user: UserInterface
}

export interface ProtocolInterface  {
  award: (documentId: string, holderPub: string, issuerKey: Key) => Promise<StorageEntry>;
  request: (awardDocumentId: string, verifierPub: Key) => Promise<StorageEntry>;
  proof: (requestId: string, verifierPub: Key) => Promise<StorageEntry>;
  acknowledge: (proofRequestId: string, document: any) => Promise<StorageEntry>;
}

export class Protocol implements ProtocolInterface {
  storage: StorageInterface;
  ledger: LedgerInterface;
  messaging: MessagingInterface;
  crypto: CryptoInterface;
  user: UserInterface;

  constructor(props: ProtocolInterfaceConstructor){
    this.storage = props.storage
    this.ledger = props.ledger
    this.messaging = props.messaging
    this.crypto = props.crypto
    this.user = props.user
  }

  async award(documentID, holderPub, issuerKey) {
    const document = await this.storage.getBy('Document', {id: documentID})
    const holder = await this.messaging.getEntity(holderPub)
    const { s_awd, c, r } = await this.crypto.computeAward(document, issuerKey)
    const issuedDocument = await this.storage.create('IssuedDocument',{
      document: document.id,
      holderPub: holderPub,
      issuer: this.user,
      c,
      r,
      signature: s_awd,
      status: 'pending'
    }) as any
    const {hash: pendingHash} =  await this.ledger.publish(s_awd)
    const {hash, status, error} = await this.ledger.getTransaction(pendingHash)
    issuedDocument.status = status;
    issuedDocument.error = error;
    this.storage.update('IssuedDocument', issuedDocument.id, issuedDocument)
    if(status === 'confirmed'){
      await this.messaging.sendMessage(holderPub, 'award', {...document, award: hash})
    }
    return issuedDocument
  }

  async request(awardedDocumentID, verifierPub) {
    const awardedDocument = await this.storage.getBy('AwardedDocument', {id: awardedDocumentID}) as any
    const {s_awd, c} = awardedDocument 
    const issuer = await this.messaging.getEntity(awardedDocument.issuerPub)
    const verifier = await this.messaging.getEntity(verifierPub) 
    const request = await this.storage.create('Request', {awardedDocumentID, verifier}) as any
    const {s_req} = await this.crypto.computeRequest(s_awd, c, verifier.publicKey.split('|'), this.user.keys.crypto.private)
    const {hash: pendingHash} = await this.ledger.publish(s_req)
    const {hash, status, error} = await this.ledger.getTransaction(pendingHash)
    request.status = status;
    request.error = error;
    this.storage.update('Request', request.id, request)
    if(status === 'confirmed'){
      await this.messaging.sendMessage(issuer.publicKey, 'request', {hash, s_awd})
    }
    return request
  }

  async proof(requestId, verifierPub) {
    const request = await this.storage.getBy('Request', {id: requestId}) as any
    const {s_awd} = request
    const verifier = await this.messaging.getEntity(verifierPub)
    const {c, r} = await this.storage.getBy('IssuedDocument', {s_awd}) as any
    const {data: s_req} = await this.ledger.getTransaction(request.hash)
    const {s_prf, proof} = await this.crypto.computeProof(
      s_req, 
      r, 
      c,
      s_awd, 
      verifier.publicKey.split('|'), 
      this.user.keys.crypto.private
    )
    const {hash: pendingHash} = await this.ledger.publish(s_prf)
    const {hash, status, error} = await this.ledger.getTransaction(pendingHash)
    if(status === 'confirmed'){
      await this.messaging.sendMessage(verifierPub, 'proof', {proof, hash})
    }
    request.status = 'confirmed';
    request.signatureTransaction = hash
    request.error = error
    await this.storage.update('Request', request.id, request)
    return request
  }

  acknowledge(proofRequestId, document) {
    return {} as any
  }
}





export class Authority extends Protocol {

  createProfile(){

  }
  retrieveProfile(){}
  disableProfile(){

  }
}