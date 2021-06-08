import { storageMiddleware } from "@diplomas/core/middlewares/files";

export default {
  post: [
    storageMiddleware('holder'),

  ]
}