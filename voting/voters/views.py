from django.shortcuts import render
import json
import web3
import commission.views as comm

from web3 import Web3, HTTPProvider, TestRPCProvider, IPCProvider
from solc import compile_source
from web3.contract import ConciseContract

print(comm.tx_receipt.contractAddress)

def voterHome(request):
    balance = []
    i=0
    #w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    w3 = Web3(Web3.IPCProvider('/home/siddhi/testnet/eth/geth.ipc'))
    for bal in w3.eth.accounts:
        balance.append(w3.eth.getBalance(bal))
        i=i+1
    print(balance)
    account= w3.eth.accounts
    detail=zip(account,balance)
    print(account)
    return render(request,'voters/votingPage.html', {"detail":detail })


def getBalance(request):
    w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
    req = request.POST.get('balance')
    bal = w3.eth.getBalance(req)
    print(bal)
    return render(request,'voters/votingPage.html' ,{"req":bal})

def transfer(request):
    w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
    sender = request.POST.get('from')
    receiver = request.POST.get('to')
   # w3.personal.unlockAccount(receiver,'')
    print('receiver:' + receiver )
    w3.eth.sendTransaction({'from' : sender, 'to':receiver,'value':w3.toWei(.05,"ether")})
    return render(request,'voters/votingPage.html')
def getBlock(request):
    w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
    blocks = w3.eth.getBlock(0).hash.hex()
    return render(request,'voters/votingPage.html', {"blocks":blocks})

def vote(request):
    account = request.POST.get('acc')
    w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
    w3.eth.sendTransaction({'from' : w3.eth.accounts[0], 'to':account,'value':w3.toWei(.05,"ether")})

    return render(request, 'voters/votingPage.html',{'account':account})

