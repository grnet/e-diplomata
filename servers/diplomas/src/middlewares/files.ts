import multer from 'multer';


export function storageMiddleware(dir){
  const storage = multer.diskStorage({
    destination: function (req, file, cb) {
      cb(null, `public/uploads/${dir}`)
    },
    filename: function (req, file, cb) {
      cb(null, file.fieldname + "-" + Date.now())
    },
  })
  const upload = multer({ storage: storage })
  return upload
}
