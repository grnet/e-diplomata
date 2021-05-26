pragma solidity >=0.4.22 <0.7.0;

contract Award {
    
    event Data(bytes32 s_1,bytes32 s_2,bytes32 s_3);
    
    function publish(bytes32 s_1, bytes32 s_2, bytes32 s_3) public{
        emit Data(s_1, s_2, s_3);
    }
}
