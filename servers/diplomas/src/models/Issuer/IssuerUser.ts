import mongoose from "mongoose";
import KeysSchema from '@diplomas/core/models/Keys';
import Document from '@diplomas/core/models/Issuer/Document';
import ContractSchema from "../Contract";
import IssuedDocument from "./IssuedDocument";

const IssuerUserSchema = new mongoose.Schema({
  email: {
    type: String,
    required: true
  },
  title: String,
  password: {
    type: String,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now()
  },
  publicKey: String,
  contract: ContractSchema,
  keys: KeysSchema
});

IssuerUserSchema.methods.createQualification = async function(data, holderPub){
  const qualification = await Document.create({
    ...data,
    holderPub,
    issuer: this._id
  })
  return qualification
}
IssuerUserSchema.methods.awardQualification = async function(data, holderPub){
  const qualification = await IssuedDocument.create({
    ...data,
    holderPub,
    issuer: this._id
  })
  const {signature, c, r}= await Dipl
  return qualification
}
// export model user with IssuerSchema
const IssuerUser =  mongoose.model("IssuerUser", IssuerUserSchema);

export default IssuerUser