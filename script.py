from web3 import Web3
import sys
from solc import compile_source
w3 = Web3(Web3.IPCProvider('/home/manzik/Desktop/final chain/eth/geth.ipc'))
#w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
contract_source_code = '''
pragma solidity ^0.4.19;
pragma experimental ABIEncoderV2;

contract Check1{
    
    struct candidate{
        address addr;
        uint age;
        //string cName;
        string password;   
        string msg;
        bool doesExist;
    }
    
    struct voter{
        address addr;
         uint uid;
        //string vName;
        string password;
        string msg;
        bool rightToVote;
    }
    
    
    mapping (string => candidate) candidates;
    mapping (string => voter) voters;
    
    address[] public candidateList;
    address[] public voterList;
    
    string[] public candidateNames;
    string[] public voterNames;
    
    function setCandidate(address _address, uint _age, string _cName,string _password) public{
        
        var candidate = candidates[_cName];
        
        candidate.addr = _address;
        candidate.age = _age;
        //candidate.cName = _cName;
        candidate.password = _password;
        candidate.msg = "you are candidate";
        candidate.doesExist = true;
        
        candidateList.push(_address) -1;
        candidateNames.push(_cName) -1;
    
    }
    
     function setVoter(address _address, uint _uid, string _vName,string _password) public{
        
        var voter = voters[_vName];
        
        voter.addr = _address;
        voter.uid = _uid;
        //voter.vName = _vName;
        voter.password = _password;
        voter.msg = "you are voter";
        voter.rightToVote = true;
        
        voterList.push(_address) -1;
        voterNames.push(_vName) -1;
    
    }
    
   function getCandidate() view public returns(address[]){
        
        return candidateList;
    }
    
      function getVoter() view public returns(address[]){
        
        return voterList;
    }
    
      
   function getCandidateNames() view public returns(string[]){
        
        return candidateNames;
    }
    
      function getVoterNames() view public returns(string[]){
        
        
        return voterNames;
    }

    
    
    
    function check(string _name) view public returns(uint,address,string,string){
        
       // uint value;
        for (uint i=0;i<voterList.length;i++){
            
             if((voters[_name].addr == voterList[i]) && (voters[_name].rightToVote == true)){
            
             //value = _name.balance;
             return (voters[_name].uid,voters[_name].addr,voters[_name].msg,voters[_name].password);
             break;
        }
        }
        
        for (uint j=0;j<candidateList.length;j++){
        
            if(candidates[_name].addr == candidateList[j]){
            //value = _name.balance;
            return (candidates[_name].age,candidates[_name].addr,candidates[_name].msg,voters[_name].password);
            break;
        }
        }
    }
    
    
    
    
    
    
    /*function check(address _address) view public returns(uint,string,string,uint){
        
        uint value;
        for (uint i=0;i<voterList.length;i++){
            
             if((_address == voterList[i]) && (voters[_address].rightToVote == true)){
            
             value = _address.balance;
             return (voters[_address].uid,voters[_address].fname,voters[_address].msg,value);
             break;
        }
        }
        
        for (uint j=0;j<candidateList.length;j++){
        
            if(_address == candidateList[j]){
            value = _address.balance;
            return (candidates[_address].age,candidates[_address].fname,candidates[_address].msg,value);
            break;
        }
        }
    }*/
   
   //ether transfer garna khojya 
 /*   function vote(address _cAddress) payable returns(uint,uint,uint){
        
        _cAddress.transfer(70000000);
        return(msg.sender.balance,_cAddress.balance,msg.value);
    }*/
    
}
'''

compiled_sol = compile_source(contract_source_code)
contract_interface = compiled_sol['<stdin>:Check1']
w3.personal.unlockAccount(w3.eth.accounts[0],'1234')
w3.eth.defaultAccount=w3.eth.accounts[0]

#instantiate and deploy contract
w3.personal.unlockAccount(w3.eth.accounts[0],'1234',10000)
Check1 = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'], address=w3.eth.accounts[0])

#submit the transaction that deploys the transaction
tx_hash = Check1.constructor().transact()

#wait for transaction to be mined, and get transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print(tx_receipt.contractAddress)

    
