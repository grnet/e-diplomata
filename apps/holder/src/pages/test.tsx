import React, { Component } from "react";


//import Library
//import zip = require('BlockchainControllerLibrary');
//const BlockchainControllerLibrary = new zip();
//
import {deployContract, publishAward, publishProof} from '@diplomas/ledger';

class Holder extends Component {

  constructor(props) {
   super(props);
   this.state = {
     txForHolder: '',
     // contractAdd is the deployed Contract's address
     contractAdd: '',
     // award and proof functions
     //conAdd is used for calling award and proof functions
     conAdd : '',
     award : '',
     award2: '',
     receiptAward: '',
     //proof
     conAdd2: '',
     GivenSreq: '',
     c: '',
     c2: '',
     Nirenc: '',
     Ev: '',
     receiptProof: '',
     willShowLoader: false,
     reject: false,
   }

   this.handleChange = this.handleChange.bind(this);
   //with backend server
   this.handleDeploymentv2 = this.handleDeploymentv2.bind(this);
   this.deployContractv2 = this.deployContractv2.bind(this);
   this.handleAwardv2 = this.handleAwardv2.bind(this);
   this.Certif_Awardv2 = this.Certif_Awardv2.bind(this);
   this.handleProofv2 = this.handleProofv2.bind(this);
   this.Certif_Proofv2 = this.Certif_Proofv2.bind(this);
  };

  componentDidMount(){
    document.title = "Ypiresia gia ton Holder";
    this.callApi()
      .then(res => console.log("connected"))
      .catch(err => console.log(err));
  }

  callApi = async () => {
    const response = await fetch('/apiTest/hello');
    const body = await response.json();
    if (response.status !== 200) throw Error(body.message);
    return body;
  };

  handleChange(event) {
    event.preventDefault();
    this.setState({ [event.target.name]: event.target.value });
  }

  //Holder provides his owner address
  handleDeploymentv2 = async(event) => {
    event.preventDefault();
    this.setState({willShowLoader: true}, () => {this.deployContractv2();});
  }

  deployContractv2 = async() => {
  /* if we use backend server
    const response = await fetch('/api/blockchain/Deploy', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    });
    const body = await response.json();
    console.log(body);
    if (body == "error"){console.log("error");}
    else{
      this.setState( {
      txForHolder: body.tranHash, contractAdd: body.contractAddress,
      willShowLoader: false, reject: false
    });
    }
  */
  //the following code is for using the Blockchain Typescript Library
    let response = await deployContract();
    console.log(response);
    this.setState( {
      txForHolder: response.tranHash, contractAdd: response.contractAddress,
      willShowLoader: false, reject: false
    });
  }

  //Holder provides his owner address
  handleAwardv2 = async(event) => {
    event.preventDefault();
    console.log(event.target.award.value);
    let hashAward1 = event.target.award.value;
    let hashAward2 = event.target.award2.value;
    let cAdd = event.target.conAdd.value;
    this.setState({willShowLoader: true}, () => {this. Certif_Awardv2(hashAward1,hashAward2,cAdd);});
  }

   Certif_Awardv2 = async(hashAward1,hashAward2,cAdd) => {
    /* if we use backend server
    const response = await fetch('/api/blockchain/Award', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ hashAward1: hashAward1, hashAward2: hashAward2, cAdd: cAdd }),
    });
    const body = await response.json();
    console.log(body);
    if (body == "error"){console.log("error");}
    else{
      this.setState( {receiptAward: body.transactionHash, willShowLoader: false,
      reject: false});
    }
    */
    //the following code is for using the Blockchain Typescript Library
    let response = await publishAward({
      hashOfAwardFirstPart: hashAward1, hashOfAwardSecondPart: hashAward2,
      contractAddressUsedByHolder: cAdd
    });
    console.log(response);
    this.setState( {
      receiptAward: response.transactionHash, willShowLoader: false, reject: false
    });
  }

  //Holder provides his owner address
  handleProofv2 = async(event) => {
    event.preventDefault();
    let cAdd = event.target.conAdd2.value;
    let sReq = event.target.GivenSreq.value;
    let c = event.target.c.value;
    let c2 = event.target.c2.value;
    let nirenc = event.target.Nirenc.value;
    let ev = event.target.Ev.value;
    this.setState({willShowLoader: true}, () => {this. Certif_Proofv2(cAdd,sReq,c,c2,nirenc,ev);});
  }

   Certif_Proofv2 = async(cAdd,sReq,c,c2,nirenc,ev) => {
    /* if we use backend server
    const response = await fetch('/api/blockchain/Proof', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ cAdd: cAdd, sReq: sReq, c: c, c2: c2, nirenc: nirenc, ev: ev }),
    });
    const body = await response.json();
    console.log(body);
    if (body == "error"){console.log("error");}
    else{
      this.setState( {receiptProof: body.transactionHash, willShowLoader: false, reject: false});
    }
    */
    //the following code is for using the Blockchain Typescript Library
    let response = await publishProof({
       contractAddressUsedByHolder: cAdd, sReq: sReq, c: c, c2: c2, nirenc: nirenc, ev: ev
    });
    console.log(response);
    this.setState( {
      receiptProof: response.transactionHash, willShowLoader: false, reject: false
    });
  }

  render() {
   let displayTxForHolder = ((this.state.txForHolder == "") ? (<p></p>) : (<p> Holder your transaction receipt is {this.state.txForHolder}</p>));
   let displayContractAdd = ((this.state.contractAdd == "") ? (<p></p>) : (<p> and your contract is at address {this.state.contractAdd}</p>));
   let displayTxAward = ((this.state.receiptAward == "") ? (<p></p>) : (<p> Your transaction receipt is {this.state.receiptAward}</p>));
   let displayTxProof = ((this.state.receiptProof == "") ? (<p></p>) : (<p> Your transaction receipt is {this.state.receiptProof}.<br />Save this value and later display it with the coresponding verifier's public key in your website, so that the Verifier can see it</p>));
   //let text = ((this.state.receiptProof == "") ? (<p></p>) : (<p> Save this value and later display it with the coresponding verifier's public key in your website, so that the Verifier can see it</p>));
   //in return we should also add a tab where Holder can see the Request published for him
   //data will be retrieved from the database. When a Holder publishes a request for proof from the website,
   //website will save the data. Another way is for the website actively listen to all events emited from an Holder's contract.
   //If we have many Holder we should listen from all contracts. So if a Holder publishes a request without using the website
   //using for example Remix, then in order our website to save the request, it should actively listen when the function request of a specific
   //smart contract is emited so that it can be saved and later it could be displayed to the Holder through the website.
   //we should consider that only requests that are emitted from a valid holder are saved.
   return (
     <div className="MakeRequest">
          Deploy a contract for your School.<br />
          <br />
          <button onClick={this.handleDeploymentv2}>
          Deploy a contract
          </button>
          {displayTxForHolder}
          {displayContractAdd}
          <br />
          <form onSubmit={this.handleAwardv2}>
          <label>
            Publish an award <br />Insert the Ethereum address of the contract that you use as an Holder and the hash value of the award you want to publish.<br />
            <input type="text" placeholder="Input contract's address" value={this.state.conAdd} name="conAdd" onChange={this.handleChange} />
            <input type="text" placeholder="Input first value of the award" value={this.state.award} name="award" onChange={this.handleChange} />
            <input type="text" placeholder="Input second value of the award" value={this.state.award2} name="award2" onChange={this.handleChange} />
          </label>
          <button>Send</button>
          </form>
          {displayTxAward}
          <form onSubmit={this.handleProofv2}>
          <label>
            Publish a proof <br />Insert the Ethereum address of the contract that you use as an Holder and all other necessary values.<br />
            <input type="text" placeholder="Input contract's address" value={this.state.conAdd2} name="conAdd2" onChange={this.handleChange} />
            <input type="text" placeholder="Input sreq" value={this.state.GivenSreq} name="GivenSreq" onChange={this.handleChange} />
            <input type="text" placeholder="Input c'" value={this.state.c} name="c" onChange={this.handleChange} />
            <input type="text" placeholder="Input second value of c'" value={this.state.c2} name="c2" onChange={this.handleChange} />
            <input type="text" placeholder="Input NIRENC(c,c')" value={this.state.Nirenc} name="Nirenc" onChange={this.handleChange} />
            <input type="text" placeholder="Input Ev" value={this.state.Ev} name="Ev" onChange={this.handleChange} />
          </label>
          <button>Send</button>
          </form>
          {displayTxProof}
          {(this.state.willShowLoader)?<p> Your transaction is pending</p> : null}
          {(this.state.reject)?<p> You rejected the transaction</p> : null}
    </div>
   );
  }
}

export default Holder;
