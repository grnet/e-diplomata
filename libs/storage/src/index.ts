import {StorageInterface} from '@diplomas/protocol'

type Status =  'pending' | 'confirmed' |'fail'; 

interface IssuerDocument {
  file: any;
  holder: string;
  issuer: string;
  s_awd: string;
  t_awd: string;
  c: any;
  r: string;
  status: Status;
}

interface HolderDocument {
  file: any;
  holder: string;
  issuer: string;
  s_awd: string;
  t_awd: string;
  c: any;
}

interface HolderRequest {
  s_awd: string;
  s_req: string;
  t_req: string;
  status: Status;
  verifier: string;
  holder: string;
  issuer: string;
}

interface ProofRequest {
  s_awd: string;
  t_req: string;
  s_prf: string;
  t_prf: string;
  proof: any;
  status: Status;
  verifier: string;
  holder: string;
  issuer: string;
}

interface Acknowledgment {
  t_prf: string;
  proof: any;
  issuer: string;
  t_ack: string;
  s_ack: string;
  status: Status;
  result: Status;

}

export class MongooseStorage implements StorageInterface {
  mongoose: any;
  constructor(mongoose){
    this.mongoose = mongoose
  }
  getBy(type, query){
    return this.mongoose.model(type).findOne(query)
  }
  create(type, data){
    return this.mongoose.model(type).create(data)
  }
  update(type, id, data){
    return this.mongoose.model(type).update({id},data)
  }
}