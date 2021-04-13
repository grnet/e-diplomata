export const Bytecode = "0x608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16600073ffffffffffffffffffffffffffffffffffffffff167f342827c97908e5e2f71151c08502a66d44b6f758e3ac2f1de95f02eb95f0a73560405160405180910390a36107a0806100dc6000396000f3fe608060405234801561001057600080fd5b506004361061007d5760003560e01c8063893d20e81161005b578063893d20e814610148578063a6f9dae114610192578063b0bff6c6146101d6578063bfca96eb1461020e5761007d565b80633649bf9f146100825780636b0937bc146100ba578063839c242614610110575b600080fd5b6100b86004803603604081101561009857600080fd5b810190808035906020019092919080359060200190929190505050610284565b005b61010e600480360360a08110156100d057600080fd5b8101908080359060200190929190803590602001909291908035906020019092919080359060200190929190803590602001909291905050506102c7565b005b6101466004803603604081101561012657600080fd5b8101908080359060200190929190803590602001909291905050506103e7565b005b6101506104ec565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6101d4600480360360208110156101a857600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610515565b005b61020c600480360360408110156101ec57600080fd5b810190808035906020019092919080359060200190929190505050610695565b005b610282600480360360c081101561022457600080fd5b810190808035906020019092919080359060200190929190803590602001909291908035906020019092919080359060200190929190803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506106d8565b005b7fcfbada41fc04f7d9aa285457e0e0d511f304cb4a4156ad2ac7956c5d32cee7a88282604051808381526020018281526020019250505060405180910390a15050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614610389576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260138152602001807f43616c6c6572206973206e6f74206f776e65720000000000000000000000000081525060200191505060405180910390fd5b7f9a7de6d9c5a24d073da5532a4b214edfe049bf20695e45fdbd0d94dec910f9348585858585604051808681526020018581526020018481526020018381526020018281526020019550505050505060405180910390a15050505050565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146104a9576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260138152602001807f43616c6c6572206973206e6f74206f776e65720000000000000000000000000081525060200191505060405180910390fd5b7f0920506e34ee71cded5e4d99ca8314c57764aa978799fcd23ac67165a70090ce8282604051808381526020018281526020019250505060405180910390a15050565b60008060009054906101000a900473ffffffffffffffffffffffffffffffffffffffff16905090565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16146105d7576040517f08c379a00000000000000000000000000000000000000000000000000000000081526004018080602001828103825260138152602001807f43616c6c6572206973206e6f74206f776e65720000000000000000000000000081525060200191505060405180910390fd5b8073ffffffffffffffffffffffffffffffffffffffff166000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff167f342827c97908e5e2f71151c08502a66d44b6f758e3ac2f1de95f02eb95f0a73560405160405180910390a3806000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555050565b7f143737e2dafc80aa0d1dde85207e69a29cdb5f201b6dd3f3cd4df03d2888f6a58282604051808381526020018281526020019250505060405180910390a15050565b7f01e797981fa104c108363b566fa41b05939b2c5170970407147896b70981d601868686868686604051808781526020018681526020018581526020018481526020018381526020018273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001965050505050505060405180910390a150505050505056fea265627a7a72315820a162b2608da79513956cef6242ebbcec06c2826ca6a63ec581744ae70a23012164736f6c63430005100032";
/*CERTIFICATE_ADDRESS is the address of the smart contract that corresponds to an Issuer
  The Issuer has previously deployed a contract and he sets in the variable the address
  returned from the transaction
*/
export const CERTIFICATE_ADDRESS = '0xC2d331e7952530CEFdc275cf41D818abf0f73007';

// Ropsten 0x454B18da1B4DA36D0BD8824953caB84992048887
//exports cCERTIFICATE_ADDRESS = '0x454B18da1B4DA36D0BD8824953caB84992048887';

export const CERTIFICATE_ABI = [
  {
    "inputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "sprf",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "eI",
        "type": "bytes32"
      }
    ],
    "name": "Ack",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "sprf",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "eI",
        "type": "bytes32"
      }
    ],
    "name": "Fail",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "cert",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "cert2",
        "type": "bytes32"
      }
    ],
    "name": "FirstProof",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": true,
        "internalType": "address",
        "name": "oldOwner",
        "type": "address"
      },
      {
        "indexed": true,
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "OwnerSet",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "sreq",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "c1",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "c2",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "ni",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "Ev",
        "type": "bytes32"
      }
    ],
    "name": "Proof",
    "type": "event"
  },
  {
    "anonymous": false,
    "inputs": [
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "cert",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "verifierAddr",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "verifierAddr2",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "verifierAddr3",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "bytes32",
        "name": "verifierAddr4",
        "type": "bytes32"
      },
      {
        "indexed": false,
        "internalType": "address",
        "name": "verifier",
        "type": "address"
      }
    ],
    "name": "Request",
    "type": "event"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "address",
        "name": "newOwner",
        "type": "address"
      }
    ],
    "name": "changeOwner",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [],
    "name": "getOwner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "cert",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "cert2",
        "type": "bytes32"
      }
    ],
    "name": "award",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "sawd",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "verifierAddr",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "verifierAddr2",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "verifierAddr3",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "verifierAddr4",
        "type": "bytes32"
      },
      {
        "internalType": "address",
        "name": "verifier",
        "type": "address"
      }
    ],
    "name": "request",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "sreq",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "c1",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "c2",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "ni",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "Ev",
        "type": "bytes32"
      }
    ],
    "name": "proof",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "sprf",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "eI",
        "type": "bytes32"
      }
    ],
    "name": "ack",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "internalType": "bytes32",
        "name": "sprf",
        "type": "bytes32"
      },
      {
        "internalType": "bytes32",
        "name": "eI",
        "type": "bytes32"
      }
    ],
    "name": "fail",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
];
