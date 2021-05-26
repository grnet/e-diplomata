export const Bytecode = "0x6080604052348015600f57600080fd5b5060ee8061001e6000396000f3fe6080604052348015600f57600080fd5b506004361060285760003560e01c8063155c4a4e14602d575b600080fd5b606a60048036036060811015604157600080fd5b81019080803590602001909291908035906020019092919080359060200190929190505050606c565b005b7f7522d075874d0eadcea7f89764cd5f0afb00ad2822383adc7fc6b8e62ae279af83838360405180848152602001838152602001828152602001935050505060405180910390a150505056fea2646970667358221220f291a16fe2266ab8a8cef00793cb0a5bbca45bc4c69b2073619514619bec135764736f6c634300060c0033";
/*CERTIFICATE_ADDRESS is the address of the smart contract that corresponds to an Issuer
  The Issuer has previously deployed a contract and he sets in the variable the address
  returned from the transaction
*/
export const CERTIFICATE_ADDRESS = '0x5D632C607655357A0F87e2905060b0bD2055d8A3';
export const CERTIFICATE_ABI = [
    {
        "anonymous": false,
        "inputs": [
            {
                "indexed": false,
                "internalType": "bytes32",
                "name": "s_1",
                "type": "bytes32"
            },
            {
                "indexed": false,
                "internalType": "bytes32",
                "name": "s_2",
                "type": "bytes32"
            },
            {
                "indexed": false,
                "internalType": "bytes32",
                "name": "s_3",
                "type": "bytes32"
            }
        ],
        "name": "Data",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "s_1",
                "type": "bytes32"
            },
            {
                "internalType": "bytes32",
                "name": "s_2",
                "type": "bytes32"
            },
            {
                "internalType": "bytes32",
                "name": "s_3",
                "type": "bytes32"
            }
        ],
        "name": "publish",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
];