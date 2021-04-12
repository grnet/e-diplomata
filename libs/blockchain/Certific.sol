pragma solidity >=0.4.22 <0.7.0;

contract Certific {

    address private owner;

    event FirstProof(bytes32 cert, bytes32 cert2);
    event Request(bytes32 cert, bytes32 verifierAddr, bytes32 verifierAddr2, bytes32 verifierAddr3, bytes32 verifierAddr4);
    event Proof(bytes32 sreq, bytes32 c1, bytes32 c2, bytes32 ni, bytes32 Ev);
    event Ack(bytes32 sprf, bytes32 eI);
    event Fail(bytes32 sprf);
    event OwnerSet(address indexed oldOwner, address indexed newOwner);

    modifier isOwner() {
        require(msg.sender == owner, "Caller is not owner");
        _;
    }

    constructor() public {
        owner = msg.sender;
        emit OwnerSet(address(0), owner);
    }

    function changeOwner(address newOwner) public isOwner {
        emit OwnerSet(owner, newOwner);
        owner = newOwner;
    }

    function getOwner() external view returns (address) {
        return owner;
    }

    function award(bytes32 cert, bytes32 cert2) public isOwner{
        emit FirstProof(cert ,cert2);
    }

    function request(bytes32 sawd,  bytes32 verifierAddr,  bytes32 verifierAddr2, bytes32 verifierAddr3, bytes32 verifierAddr4) public {
        emit Request(sawd, verifierAddr, verifierAddr2, verifierAddr3, verifierAddr4);
    }

    function proof(bytes32 sreq, bytes32 c1, bytes32 c2, bytes32 ni, bytes32 Ev) public isOwner{
        emit Proof(sreq, c1, c2, ni, Ev);
    }

    function ack(bytes32 sprf, bytes32 eI) public {
        emit Ack(sprf, eI);
    }

    function fail(bytes32 sprf) public {
        emit Fail(sprf);
    }

}
