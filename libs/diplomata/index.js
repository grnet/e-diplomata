const zerorpc = require("zerorpc");
var spawn = require('child_process').spawn;
var child = spawn('python',['server.py'],{
  cwd: process.cwd(),
  stdio: "inherit"
});

const client = new zerorpc.Client();
client.connect("tcp://127.0.0.1:4242");

const DiplomasCrypto = new Proxy(client, {
  get(target, func){
    return function (...args){
      return new Promise((resolve, reject)=>{
        target.invoke(func, ...args, function(error, res){
          if(error){
            reject(error)
          }
          resolve(res)
        })
      })
    }
  }
})


// issuer_key
async function run(){
  const keys = await DiplomasCrypto.generate_keys()
  // const step_one = await DiplomasCrypto.step_one()
  console.log(keys)
}
run()