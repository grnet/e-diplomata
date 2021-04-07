const path = require('path')
const os = require('os')
module.exports = {
  "aliases": {
    "@diplomas/blockchain": path.join(__dirname, "../../libs/blockchain/src"),
    react: path.resolve('node_modules/react'),
    "react-dom":  path.resolve('node_modules/react-dom'),
    "@material-ui/core":  path.resolve('node_modules/@material-ui/core'),
  },
}