import { storageMiddleware } from "@diplomas/server/middlewares/files";

export default {
  post: [
    storageMiddleware('holder'),

  ]
}