from web3 import Web3
import sys
from solc import compile_source
w3 = Web3(Web3.IPCProvider('/home/siddhi/testnet/eth/geth.ipc'))


d = {}
dList = []
for i in range(1,w3.eth.blockNumber):
	if w3.eth.getTransactionByBlock(i,0) != None:
		print('====================================================')
		print('Transaction in block', i)
		'''print('Value : ',w3.eth.getTransactionByBlock(i,0).value)
		print('TO :',w3.eth.getTransactionByBlock(i,0).to)
		'''
		#d['To'] = w3.eth.getTransactionByBlock(i,0).to
		#d['Value'] = w3.eth.getTransactionByBlock(i,0).value
		dList.append({'Value':w3.eth.getTransactionByBlock(i,0).value,'To':w3.eth.getTransactionByBlock(i,0).to})
for i in range(0,len(dList)):
	print(dList[i])

#		print('FROM : ',w3.eth.getTransactionByBlock(i,0))

