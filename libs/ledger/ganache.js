const ganache = require("ganache-cli");
const server = ganache.server({"blockTime": 2});
server.listen(8545, function(err, blockchain) {});