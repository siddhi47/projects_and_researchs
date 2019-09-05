from django.shortcuts import render
from django.http import HttpResponse
from .models import Vote
from web3 import Web3
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from solc import compile_source
print('eee')
#w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(Web3.IPCProvider('/home/manzik/Desktop/final chain/eth/geth.ipc'))
print('sss')

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
print('comp')

contract_interface = compiled_sol['<stdin>:Check1']
w3.personal.unlockAccount(w3.eth.accounts[0],'1234',10000)
w3.eth.defaultAccount=w3.eth.accounts[0]

#instantiate and deploy contract
w3.personal.unlockAccount(w3.eth.accounts[0],'1234',10000)
Check1 = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'], address=w3.eth.accounts[0])

#submit the transaction that deploys the transaction
tx_hash = Check1.constructor().transact()

#wait for transaction to be mined, and get transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

#create contract instance with newly deployed address
#run the script file and put that address
address = '0xf5DBd4e3f3F01AaAB5665EBcf1348F32564BBDf2'
#address = '0x0Dc0273710bC6D48a605bb845c2e1b362Bc76be6'
check = w3.eth.contract(address=address ,abi=contract_interface['abi'],)



def commission(request):
    return render(request, "commission/commission.html", {'address':tx_receipt.contractAddress})

def register(request):
    print('fine 1')

    name = request.POST.get('name')
    password = request.POST.get('pass')
    confirm = request.POST.get('cpass')
    drop = request.POST.get('drop')
    email = request.POST.get('email')
    print('fine2')
    if(password==confirm):
        print('password is fine')
        pin = str(randint(1000, 9999))

        print('before pin')
        account = w3.personal.newAccount(pin)
        print('after pin')
        print(pin)
        if drop == 'Voter':
            print('entered voter')
            print("contract address:" + tx_receipt.contractAddress)
            print('Voter')
            hashed = check.functions.setVoter(w3.toChecksumAddress(account),10,name,password).transact()
            w3.eth.waitForTransactionReceipt(hashed)
            print('registered')
        elif drop == 'Candidate':
            print("contract address:" + tx_receipt.contractAddress)
            print('Candidate')
            hashed = check.functions.setCandidate(w3.toChecksumAddress(account), 10, name,password).transact()
            w3.eth.waitForTransactionReceipt(hashed)
        subject = 'Pin Number'
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]
        message = "Your Pin:" + str(pin)
        send_mail(subject=subject,from_email=from_email, recipient_list=to_email, message=message, fail_silently=True)
        return render(request,"commission/commission.html",{'message':drop +' was registered successfully.', "pin": pin, "account":'account : '+account})
    else:
        return render(request,"commission/commission.html",{"message": drop +"registration unsuccessful"})

def distribute(request):
    return render(request,"commission/distribute.html")

def dist(request):
    length = len(check.functions.getVoter().call())
    for i in range(0,length):
        w3.personal.unlockAccount(w3.eth.accounts[0], '1234',10000)
        w3.eth.sendTransaction({'from':w3.eth.accounts[0], 'to':check.functions.getVoter().call()[i], 'value': w3.toWei(1.5, "ether")})
    return render(request,"commission/distribute.html",{"message":'success'})


def showTx(request):
    d = {}
    toVoter = 0
    toCom = 0
    dList = []
    for i in range(1, w3.eth.blockNumber):
        blockCount = w3.eth.getBlockTransactionCount(i)
        if w3.eth.getTransactionFromBlock(i, 0) != None:
            if w3.eth.getTransactionFromBlock(i,0).value != 0:
                for j in range(0,blockCount):
                    if w3.eth.getTransactionFromBlock(i, j).value/1000000000000000000 >1.2:
                        toVoter=toVoter+1
                        dList.append(
                            {'Value': w3.eth.getTransactionFromBlock(i, j).value/1000000000000000000, 'To': w3.eth.getTransactionFromBlock(i, j).to, 'type':'Voter'})
                    else:
                        toCom = toCom+1
                        dList.append(
                            {'Value': w3.eth.getTransactionFromBlock(i, j).value / 1000000000000000000,
                             'To': w3.eth.getTransactionFromBlock(i, j).to, 'type': 'Candidate'})
    return render(request,"commission/transaction.html",{"list":dList,'toVoter':toVoter,'toCom':toCom})
