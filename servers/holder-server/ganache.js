const ganache = require("ganache-cli");
const server = ganache.server({"blocktime": 20});
server.listen(8545, function(err, blockchain) {});