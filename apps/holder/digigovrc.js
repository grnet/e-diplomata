const path = require("path");
const os = require("os");
const SERVERURI = process.env.SERVERURI || "http://localhost:5000/api/"
module.exports = {
  proxy: {
    "/api": {
      target: SERVERURI,
      pathRewrite: {
        "^/api": "/",
      },
      changeOrigin: true,
    },
  },
};
