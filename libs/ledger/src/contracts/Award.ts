//with external and no event emit
export const Bytecode =
  '0x6080604052348015600f57600080fd5b5060a78061001e6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c8063155c4a4e14602d575b600080fd5b606a60048036036060811015604157600080fd5b81019080803590602001909291908035906020019092919080359060200190929190505050606c565b005b50505056fea2646970667358221220086435e2fbe08bdf88ec0c77c3c4ac46096e41ccce374938baef7b1054ce682d64736f6c634300060c0033';
/*CERTIFICATE_ADDRESS is the address of the smart contract that corresponds to an Issuer
  The Issuer has previously deployed a contract and he sets in the variable the address
  returned from the transaction
*/
//thash = 0x2c3c43b8f67a14f9cbfb33dc0a433bdbea5a008b48d36b320833d4c0a14fecf5
export const ADDRESS = '0xc466220c018f76747a272d2416e93de8bbd37d6e';
export const ABI = [
  {
    inputs: [
      {
        internalType: 'bytes32',
        name: 's_1',
        type: 'bytes32',
      },
      {
        internalType: 'bytes32',
        name: 's_2',
        type: 'bytes32',
      },
      {
        internalType: 'bytes32',
        name: 's_3',
        type: 'bytes32',
      },
    ],
    name: 'publish',
    outputs: [],
    stateMutability: 'nonpayable',
    type: 'function',
  },
];
