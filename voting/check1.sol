pragma solidity ^0.4.18;

contract Check1{
    
    struct candidate{
        uint age;
        string fname;
        string msg;
        bool doesExist;
    }
    
    struct voter{
         uint uid;
        string fname;
        string msg;
        bool rightToVote;
    }
    
    
    mapping (address => candidate) candidates;
    mapping (address => voter) voters;
    
    address[] public candidateList;
    address[] public voterList;
    
    function setCandidate(address _address, uint _age, string _fname) public{
        
        var candidate = candidates[_address];
        
        candidate.age = _age;
        candidate.fname = _fname;
        candidate.msg = "you are candidate";
        candidate.doesExist = true;
        
        candidateList.push(_address) -1;
    
    }
    
     function setVoter(address _address, uint _uid, string _fname) public{
        
        var voter = voters[_address];
        
        voter.uid = _uid;
        voter.fname = _fname;
        voter.msg = "you are voter";
        voter.rightToVote = true;
        
        voterList.push(_address) -1;
    
    }
    
    function getCandidate() view public returns(address[]){
        
        return candidateList;
    }
    
      function getVoter() view public returns(address[]){
        
        return voterList;
    }
    
    
    function check(address _address) view public returns(uint,string,string,uint){
        
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
    }
   
   //ether transfer garna khojya 
 /*   function vote(address _cAddress) payable returns(uint,uint,uint){
        
        _cAddress.transfer(70000000);
        return(msg.sender.balance,_cAddress.balance,msg.value);
    }*/
    
}