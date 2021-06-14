import startServer from '@digigov/cli-server/start';
import {InitiateMongoServer} from '@diplomas/server/config/db'
InitiateMongoServer()
startServer(5000, {
  proxies: {},
  apps:[
    "@digigov/kitchensink"
  ],
})