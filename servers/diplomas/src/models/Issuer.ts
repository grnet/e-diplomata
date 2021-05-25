import mongoose from "mongoose";
import KeysSchema from "./Keys";
import Document from './Document';
import Holder from './Holder';
const IssuerSchema = new mongoose.Schema({
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
  keys: KeysSchema
});

IssuerSchema.methods.createQualification = async function(data, holderEmail){
  const holder = await Holder.findOne({email: holderEmail})
  const qualification = await Document.create({
    ...data,
    holder: holder._id,
    issuer: this._id
  })
  return qualification
}
// export model user with IssuerSchema
const Issuer =  mongoose.model("Issuer", IssuerSchema);

export default Issuer