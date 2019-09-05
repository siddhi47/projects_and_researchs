from django.shortcuts import render, redirect,HttpResponse
from web3 import HTTPProvider,Web3
print('ehello')

import commission.views as comm

from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
import random

#w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
w3 = Web3(Web3.IPCProvider('/home/manzik/Desktop/final chain/eth/geth.ipc'))
print(comm.address)
check = w3.eth.contract(address=comm.address, abi=comm.contract_interface['abi'])


def index(request):
    print(comm.address)

    return render(request, 'home/home.html')

def register(request):
    return render(request,'home/register.html')

def submit(request):

    name = request.POST.get("name")
    password = request.POST.get("pass")
    cpassword = request.POST.get("cpass")

    if (password == cpassword):
        pin = random.randint(1000,9999)
        acc = w3.personal.newAccount(pin)
        send_mail(
            'Your Accound details',
            'Pin: '+ pin+ 'id: ' + acc,
            'siddhi.47.skb@gmail.com',
            ['siddhi_47@outlook.com'],
            fail_silently=False
        )
        return render(request, 'home/register.html', {"message": 'successful',"pin":pin,"acc":acc})
    else:
        return render(request, 'home/register.html', {"message": 'unsuccessful'})

def loginView(request):
    name = request.POST.get("name")
    password = request.POST.get("pass")

    print(check.functions.check(name).call())

    voterChainList = check.functions.check(name).call()
    if voterChainList[3] == password:
        voterAcc = voterChainList[1]
        voterBalance = w3.eth.getBalance(w3.toChecksumAddress(voterAcc))
        if (voterBalance<w3.toWei(1,'ether')):
            return HttpResponse('You may have already voted or the voting may not have started yet!')
        else:
            canAcc = []
            canName = []
            candidateChainList = check.functions.getCandidate().call()
            length = len(candidateChainList)
            for can in candidateChainList:
                print(can)
                canAcc.append(can)
            for i in range(0,length):
                canName.append(check.functions.candidateNames(i).call())
            detail = zip(canAcc,canName)
            return render(request, 'home/vote.html', {"msg": 'success', "detail": detail, "user": name})
    return render(request, 'home/home.html', {"msg": 'unsuccessful'})
    ''' 
    voterList = Vote.objects.filter(type='Voter')
    for voter in voterList:
        if (voter.name == name):
            if (voter.password == password):
                voterAcc = voter.account
                voterBalance = w3.eth.getBalance(w3.toChecksumAddress(voterAcc))
                if (voterBalance < w3.toWei(1,"ether")):
                    return HttpResponse('You do not have sufficient voting points!')
                canList = []
                account = []
                candidate = Vote.objects.filter(type="Candidate")


                for can in candidate:
                    canList.append(can.name)
                    account.append(can.account)

                print(canList)
                detail = zip(account, canList)

                return render(request,'home/vote.html',{"msg":'success',"detail":detail,"user":name})
    return render(request, 'home/home.html',{"msg":'un'})
    '''
def vote(request):
    acc = request.POST.get('acc')
    user = request.POST.get('user')
    pin = str(request.POST.get('pin'))
    print(acc)
    print(pin)
    account = check.functions.check(user).call()[1]#kamchalau
    print('voter : ' + w3.toChecksumAddress(account))
    print ('candidate :' + acc)
    try:
        w3.personal.unlockAccount(account,pin)
        if (w3.eth.getBalance(account) < w3.toWei(1,"ether")):
            return HttpResponse('You have insufficient votes!')
        w3.eth.sendTransaction({'from': w3.toChecksumAddress(account), 'to': acc, 'value': w3.toWei(1, "ether")})

        return render(request, 'home/home.html',{"status":'success'})
    except:
        print('error')
        return HttpResponse('Pin did not match!')

