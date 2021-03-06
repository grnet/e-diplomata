import { MessagingInterface } from "@diplomas/protocol"
import fetch from 'node-fetch';

const AUTH_API = process.env.AUTH_API || 'http://localhost:5000/'


export class Messaging implements MessagingInterface {
  async sendMessage (pubKey, transaction, data) {
    const entity = await this.getEntity(pubKey)
    const response = await fetch(`${entity.service}/api/${entity.type.toLowerCase()}/${transaction}/`, {
      method: 'POST',
      body: JSON.stringify(data),
      headers: { 'Content-Type': 'application/json' },
    })
    return await response.json()
  }

  async getEntity(pubKey){
    const response = await fetch(AUTH_API+'api/auth/profile?publicKey='+pubKey)
    return await response.json()
  }
}
export default Messaging