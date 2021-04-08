const path = require("path");
const os = require("os");
module.exports = {
  proxy: {
    "/api": {
      target: "http://localhost:4000/api/",
      pathRewrite: {
        "^/api": "/",
      },
      changeOrigin: true,
    },
  },
};
