from django.shortcuts import render
from web3 import Web3
import commission.views as comm
from django.http import HttpResponse


#w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(Web3.IPCProvider('/home/manzik/Desktop/final chain/eth/geth.ipc'))
check = w3.eth.contract(address=comm.address, abi=comm.contract_interface['abi'])

is_publish = False

def setPublish():
    is_publish = True

def getPublish():
    return is_publish

def viewResults(request):
    candidateChainList = check.functions.getCandidate().call()
    length = len(candidateChainList)
    canList = []
    balance = []
    for i in range(0, length):
        canList.append(check.functions.candidateNames(i).call())
    for can in candidateChainList:
        balance.append(int(w3.eth.getBalance(w3.toChecksumAddress(can))/1000000000000000000))
    '''
    for can in candidateChainList:
        canList.append(can)
        balance.append(int(w3.eth.getBalance(w3.toChecksumAddress(can.account))/1000000000000000000))
    '''
    detail = zip(canList,balance)
    print(balance)
    return render(request,'public/results.html',{"detail":detail})
