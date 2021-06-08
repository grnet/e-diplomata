import startServer from '@digigov/cli-server/start';
import initiateMongo from '@digigov/cli-server/initiateMongo'

initiateMongo()
startServer(5000, {
  proxies: {},
  apps:[
    "@digigov/kitchensink"
  ],
})