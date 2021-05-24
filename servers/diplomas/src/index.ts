import express from "express" // CommonJS import style!
const InitiateMongoServer = require("./config/db");
InitiateMongoServer();

// import some useful middleware
// const bodyParser = require("body-parser") // middleware to help parse incoming HTTP POST data
// import multer from "multer" // middleware to handle HTTP POST requests with file uploads
// import axios from "axios" // middleware for making requests to APIs

import morgan from "morgan" // middleware for nice logging of incoming HTTP requests

import dotenv from "dotenv"
import glob from 'glob'

dotenv.config({ }) // load environmental variables from a hidden file named .env

const app = express() // instantiate an Express object
// use the morgan middleware to log all incoming http requests
app.use(morgan("dev")) // morgan has a few logging default styles - dev is a nice concise color-coded style

// use the bodyparser middleware to parse any data included in a request
app.use(express.json()) // decode JSON-formatted incoming POST data
app.use(express.urlencoded({ extended: true })) // decode url-encoded incoming POST data

// enable file uploads saved to disk in a directory named 'public/uploads'
// const storage = multer.diskStorage({
//   destination: function (req, file, cb) {
//     cb(null, "public/uploads")
//   },
//   filename: function (req, file, cb) {
//     cb(null, file.fieldname + "-" + Date.now())
//   },
// })
// const upload = multer({ storage: storage })
type Method = 'get' | 'post' | 'put' | 'delete' | 'patch'
const routes = glob.sync('api/**/*.ts',{cwd: './src'})
routes.forEach((route)=>{
  const routePath = `/${route
    .replace(/\[(.*?)\]/g, ':$1')
    .replace(/\.ts$/, '')
    .replace(/index$/, '')}`
  const routeConfig = require(`./${route}`).default
  if(routeConfig){
    const methods = Object.keys(routeConfig) as Method[]
    methods.forEach((method: Method)=>{
      console.log(routePath)
      app[method](routePath, ...routeConfig[method])
    })

  }

})
const port = 5000

// call a function to start listening to the port
const listener = app.listen(port, function () {
  console.log(`Server running on port: ${port}`)
})

export default listener