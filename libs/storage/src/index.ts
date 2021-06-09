import {StorageInterface} from '@diplomas/protocol'


export class MongooseStorage implements StorageInterface {
  mongoose: any;
  constructor(mongoose){
    this.mongoose = mongoose
  }
  async getBy(type, query){
    const result = await this.mongoose.model(type).findOne(query).exec()
    return result.toJSON()
  }
  async create(type, data){
    const result = await this.mongoose.model(type).create(data)
    return result.toJSON()
  }
  async update(type, id, data){
    const result = await this.mongoose.model(type).updateOne({_id:id},data).exec()
    return result
  }
}


export default MongooseStorage