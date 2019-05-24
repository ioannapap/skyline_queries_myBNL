import csv
import sys
from operator import itemgetter

allStats='2017_ALL.csv'
assistStats='2017_AST.csv'
pointStats='2017_PTS.csv'
stealStats='2017_STL.csv'
blockStats='2017_BLK.csv'
reboundStats='2017_TRB.csv'


def getINput():

	chosenCategories=[]
	args=[]
	checked=0

	print('------------------------------NBA STATS 2017------------------------------')
	print('------------------------------TOK K PLAYERS ------------------------------\n')
	print('Choose which of the following statCategories you are interested in: ')
	print('1. Rebounds 	  2. Assists 	 3. Steals  	4. Blocks 	  5. Points')

	while checked==0 or len(args)!=2:
		args=input('\nGive the numbers with comma in [ ] and then, the number of the Top-k players you are looking for:\n').split(' ')
		checked=checkArgs(args, chosenCategories)

	k=int(args[1])
	return [chosenCategories, k]



def checkArgs(args, cat):

	#checking chosenCategories

	if args[0][0]!='[' or args[0][len(args[0])-1]!=']':
		print('\nInsert the chosen categories in [ ]\n')
		return 0

	for i in args[0]:

		if i.isdigit(): 
				
			if int(i)>=1 and int(i)<=5:
				cat.insert(len(cat), int(i))
			else:
				print('\nInsert number from 1-5.\n')
				return 0 

		elif i=='[' or i==']' or i==',':
			pass
		elif i=='-':
			print('\nInsert number from 1-5.\n')
			return 0 

		else:
			print('\nInsert number from 1-5.\n')
			return 0 

	#checking k
	try:
		k=int(args[1])

	except ValueError:
		print('\nInsert integer for k.\n')
		return 0

	except IndexError:
		print('Insert integer for k.\n')
		return 0

	if k<0 or k>595:
		print( '\nAll players are 595.\n')
		return 0

	return 1



def topKEvaluation(cat, k):

	hashMap={} #ids and names only
	hashMap1={}
	hashMap2={}
	hashMap3={}
	hashMap4={}
	hashMap5={}
	upperBoundsDict={}
	W=[]
	u=5.0
	t=0 #the k-st highest score in list Wk
	canYield=0
	numOfAccesses=0 #num of lines read from files
	firstRow=1	

	with open(allStats, 'r', encoding='UTF-8') as df:
		
		row=df.readline() #to skip labels

		for row in df:						
			data=row.split(',') 
			data[-1] = data[-1].strip() #remove 
			name=data[1]
			team=data[2]
			trb=int(data[3])
			ast=int(data[4])
			stl=int(data[5])
			blk=int(data[6])
			pts=int(data[7])
			hashMap.update({int(data[0]): [name, team, trb, ast, stl, blk, pts]})

	optionFiles={0: allStats, 1: reboundStats, 2: assistStats, 3: stealStats, 4: blockStats, 5: pointStats}
	numOfChoices=len(cat)

	if numOfChoices<5:
		leftovers=5-numOfChoices
		for i in range(leftovers):
			cat.append(0)

	
	with open(optionFiles[cat[0]], 'r', encoding='UTF-8') as df1, open(optionFiles[cat[1]], 'r', encoding='UTF-8') as df2, open(optionFiles[cat[2]], 'r',encoding='UTF-8') as df3, open(optionFiles[cat[3]], 'r', encoding='UTF-8') as df4, open(optionFiles[cat[4]], 'r', encoding='UTF-8') as df5:
		
		if numOfChoices==1: #cat[0] 
	
			for row in df1:
				data1=row.split(',')
				topKPlayer=hashMap.get(int(data1[0]))
				yield [str(topKPlayer[0]), int(topKPlayer[cat[0]+1]), numOfAccesses]
				numOfAccesses+=1

		elif numOfChoices==2: #cat[0] cat[1]	

			for row in zip(df1,df2):
				data1,data2=fixData(row, numOfChoices)
	
				if firstRow==1:
					maxv1=data1[1]
					maxv2=data2[1]
					firstRow=0
				print('data1', data1[0])
				print('data2', data2[0])
				performance1=normalization(int(data1[1]), maxv1) 
				performance2=normalization(int(data2[1]), maxv2) 
				hashMap1.update({int(data1[0]): performance1})
				hashMap2.update({int(data2[0]): performance2})	
				T=performance1+performance2
				currentIds=[data1[0], data2[0]]
				currentPerformances=[performance1, performance2]
				hashMapsList=[hashMap1, hashMap2]
				R=lara(currentIds, currentPerformances, hashMapsList, t, T, W, upperBoundsDict, numOfChoices, numOfAccesses, k)
				W=R[0]
				t=R[1]
				T=R[2]
				upperBoundsDict=R[3]
				numOfAccesses=R[4]
				canYield=R[5]
				if canYield==1:
					print('W ready to Yield:', W)
					for ks in W:
						topKPlayer=hashMap.get(ks[0])
						yield [str(topKPlayer[0]), int(topKPlayer[cat[0]+1]), int(topKPlayer[cat[1]+1]), numOfAccesses]
					

		elif numOfChoices==3: #cat[0] cat[1] cat[2]

			for row in zip(df1,df2,df3):
				data1,data2, data3=fixData(row, numOfChoices)

				if firstRow==1:
					maxv1=data1[1]
					maxv2=data2[1]
					maxv3=data3[1]
					firstRow=0

				performance1=normalization(int(data1[1]), maxv1)
				performance2=normalization(int(data2[1]), maxv2) 
				performance3=normalization(int(data3[1]), maxv3)
				hashMap1.update({int(data1[0]): performance1})
				hashMap2.update({int(data2[0]): performance2})
				hashMap3.update({int(data3[0]): performance3})
				currentIds=[data1[0], data2[0], data3[0]]
				T=performance1+performance2+performance3
				currentPerformances=[performance1,performance2, performance3]
				hashMapsList=[hashMap1, hashMap2, hashMap3]
				R=lara(currentIds, currentPerformances, hashMapsList, t, T, W, upperBoundsDict, numOfChoices, numOfAccesses, k)
				W=R[0]
				t=R[1]
				T=R[2]
				upperBoundsDict=R[3]
				numOfAccesses=R[4]
				canYield=R[5]
				if canYield==1:
					for ks in W:
						topKPlayer=hashMap.get(ks[0])
						yield [str(topKPlayer[0]), int(topKPlayer[cat[0]+1]), int(topKPlayer[cat[1]+1]), int(topKPlayer[cat[2]+1]), numOfAccesses]

		elif numOfChoices==4: #cat[0] cat[1] cat[2] cat[3]

			for row in zip(df1,df2,df3,df4):
				data1,data2, data3, data4=fixData(row, numOfChoices)

				if firstRow==1:
					maxv1=data1[1]
					maxv2=data2[1]
					maxv3=data3[1]
					maxv4=data4[1]
					firstRow=0

				performance1=normalization(int(data1[1]), maxv1)
				performance2=normalization(int(data2[1]), maxv2) 
				performance3=normalization(int(data3[1]), maxv3)	
				performance4=normalization(int(data4[1]), maxv4)
				hashMap1.update({int(data1[0]): performance1})
				hashMap2.update({int(data2[0]): performance2})
				hashMap3.update({int(data3[0]): performance3})				
				hashMap4.update({int(data4[0]): performance4})
				T=performance1+performance2+performance3+performance4
				currentIds=[data1[0], data2[0], data3[0], data4[0]]
				currentPerformances=[performance1,performance2, performance3, performance4]
				hashMapsList=[hashMap1, hashMap2, hashMap3, hashMap4]
				R=lara(currentIds, currentPerformances, hashMapsList, t, T, W, upperBoundsDict, numOfChoices, numOfAccesses, k)
				W=R[0]
				t=R[1]
				T=R[2]
				upperBoundsDict=R[3]
				numOfAccesses=R[4]
				canYield=R[5]
				if canYield==1:
					for ks in W:
						topKPlayer=hashMap.get(ks[0])
						yield [str(topKPlayer[0]), int(topKPlayer[cat[0]+1]), int(topKPlayer[cat[1]+1]), int(topKPlayer[cat[2]+1]), int(topKPlayer[cat[3]+1]), numOfAccesses]

		elif numOfChoices==5: #cat[0] cat[1] cat[2] cat[3] cat[4]

			for row in zip(df1,df2,df3,df4,df5):
				data1,data2, data3, data4, data5=fixData(row, numOfChoices)

				if firstRow==1:
					maxv1=data1[1]
					maxv2=data2[1]
					maxv3=data3[1]
					maxv4=data4[1]
					maxv5=data5[1]
					firstRow=0

				performance1=normalization(int(data1[1]), maxv1)
				performance2=normalization(int(data2[1]), maxv2) 
				performance3=normalization(int(data3[1]), maxv3)	
				performance4=normalization(int(data4[1]), maxv4)
				performance5=normalization(int(data5[1]), maxv5)
				hashMap1.update({int(data1[0]): performance1})
				hashMap2.update({int(data2[0]): performance2})
				hashMap3.update({int(data3[0]): performance3})				
				hashMap4.update({int(data4[0]): performance4})
				hashMap5.update({int(data5[0]): performance5})
				T=performance1+performance2+performance3+performance4+performance5
				currentIds=[data1[0], data2[0], data3[0], data4[0], data5[0]]
				currentPerformances=[performance1,performance2, performance3, performance4, performance5]
				hashMapsList=[hashMap1, hashMap2, hashMap3, hashMap4, hashMap5]
				R=lara(currentIds, currentPerformances, hashMapsList, t, T, W, upperBoundsDict, numOfChoices, numOfAccesses, k)
				W=R[0]
				t=R[1]
				T=R[2]
				upperBoundsDict=R[3]
				numOfAccesses=R[4]
				canYield=R[5]
				if canYield==1:
					for ks in W:
						topKPlayer=hashMap.get(ks[0])
						yield [str(topKPlayer[0]), int(topKPlayer[cat[0]+1]), int(topKPlayer[cat[1]+1]), int(topKPlayer[cat[2]+1]), int(topKPlayer[cat[3]+1]), int(topKPlayer[cat[4]+1]), numOfAccesses]


def normalization(rowValue, maxv):
	return rowValue/maxv



def fixData(row, numOfChoices):

	if numOfChoices==2:

		data1=list(row[:1])
		data1[-1] = data1[-1].strip() 
		data1=data1[0].split(',')
		data1=[int(l) for l in data1]

		data2=list(row[1:2])
		data2[-1] = data2[-1].strip() 
		data2=data2[0].split(',')
		data2=[int(l) for l in data2]

		return [data1, data2]

	elif numOfChoices==3:

		data1=list(row[:1])
		data1[-1] = data1[-1].strip() 
		data1=data1[0].split(',')
		data1=[int(l) for l in data1]

		data2=list(row[1:2])
		data2[-1] = data2[-1].strip() 
		data2=data2[0].split(',')
		data2=[int(l) for l in data2]

		data3=list(row[2:3])
		data3[-1] = data3[-1].strip() 
		data3=data3[0].split(',')
		data3=[int(l) for l in data3]

		return [data1, data2, data3]


	elif numOfChoices==4:

		data1=list(row[:1])
		data1[-1] = data1[-1].strip() 
		data1=data1[0].split(',')
		data1=[int(l) for l in data1]

		data2=list(row[1:2])
		data2[-1] = data2[-1].strip() 
		data2=data2[0].split(',')
		data2=[int(l) for l in data2]

		data3=list(row[2:3])
		data3[-1] = data3[-1].strip() 
		data3=data3[0].split(',')
		data3=[int(l) for l in data3]

		data4=list(row[3:4])
		data4[-1] = data4[-1].strip() 
		data4=data4[0].split(',')
		data4=[int(l) for l in data4]


		return [data1, data2, data3, data4]


	elif numOfChoices==5:

		data1=list(row[:1])
		data1[-1] = data1[-1].strip() 
		data1=data1[0].split(',')
		data1=[int(l) for l in data1]

		data2=list(row[1:2])
		data2[-1] = data2[-1].strip() 
		data2=data2[0].split(',')
		data2=[int(l) for l in data2]

		data3=list(row[2:3])
		data3[-1] = data3[-1].strip() 
		data3=data3[0].split(',')
		data3=[int(l) for l in data3]

		data4=list(row[3:4])
		data4[-1] = data4[-1].strip() 
		data4=data4[0].split(',')
		data4=[int(l) for l in data4]
	
		data5=list(row[4:5])
		data5[-1] = data5[-1].strip() 
		data5=data5[0].split(',')
		data5=[int(l) for l in data5]

		return [data1, data2, data3, data4, data5]

def calcBounds(hashMapsList, currentPerformances, numOfChoices):

	if numOfChoices==2:

		for i in hashMapsList[0]:

			if i not in hashMapsList[1]:

				f1Lb=hashMapsList[0].get(i)
				f1Ub=hashMapsList[0].get(i)+currentPerformances[1]

			else:

				f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)
				f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)

		for i in hashMapsList[1]:

			if i not in hashMapsList[0]:

				f2Lb=hashMapsList[1].get(i)
				f2Ub=hashMapsList[1].get(i)+currentPerformances[0]

			else:

				f2Lb=hashMapsList[1].get(i)+hashMapsList[0].get(i)
				f2Ub=hashMapsList[1].get(i)+hashMapsList[0].get(i)


		return [f1Lb, f1Ub, f2Lb, f2Ub]
	'''
	elif numOfChoices==3:

	elif numOfChoices==4:

	elif numOfChoices==5:
	'''

def insertInW(lb, curID, upperBoundsDict, W, t, k):

	if len(W)<k:

		W.insert(len(W), [curID, lb])
		Wk=sorted(W, reverse=True, key=itemgetter(1))
		W=Wk
		t=W[-1][1]

	elif len(W)==k:

		if lb>t:

			found=0
			pos=0
			for ks in W:
				if ks[0]==curID:
					print('ks[0] %d ==curID %d' % (ks[0], curID))
					found=1
					print('W before update', W)
					W.pop(pos)	
					W.insert(pos, [curID, lb])
					Wk=sorted(W, reverse=True, key=itemgetter(1))
					W=Wk
					t=W[-1][1]

					print('W after update', W)
					break		
				
				else:

					pos+=1

			if found==0:	

				W.pop(-1)
				W.insert(len(W), [curID, lb])		
				Wk=sorted(W, reverse=True, key=itemgetter(1))
				W=Wk
				t=W[-1][1]

	return [W, t, upperBoundsDict]
						
def updateUpperBounds(upperBoundsDict, currentPerformances, hashMapsList, numOfChoices):

	if numOfChoices==2:

		for b in upperBoundsDict:

			if b in hashMapsList[0] and b not in hashMapsList[1]:
				newUb=hashMapsList[0].get(b)+currentPerformances[1]

			elif b not in hashMapsList[0] and b in hashMapsList[1]:
				newUb=hashMapsList[1].get(b)+currentPerformances[0]

			elif b in hashMapsList[0] and b in hashMapsList[1]:
				newUb=hashMapsList[0].get(b)+hashMapsList[1].get(b)

			upperBoundsDict[b]=newUb

	
	elif numOfChoices==3:

		for b in upperBoundsDict:

			if b in hashMapsList[0] and b not in hashMapsList[1] and not in hashMapsList[2]:
				newUb=hashMapsList[0].get(b)+currentPerformances[1]+currentPerformances[2]

			elif b not in hashMapsList[0] and b in hashMapsList[1] and not in hashMapsList[2]:
				newUb=hashMapsList[1].get(b)+currentPerformances[0]+currentPerformances[2]

			elif b not in hashMapsList[0] and b not in hashMapsList[1] and b in hashMapsList[2]:
				newUb=hashMapsList[2].get(b)+currentPerformances[0]+currentPerformances[1]

			elif b in hashMapsList[0] and b in hashMapsList[1] and b not in hashMapsList[2]:
				newUb=hashMapsList[0].get(b)+hashMapsList[1].get(b)+currentPerformances[2]

			elif b not in hashMapsList[0] and b in hashMapsList[1] and b in hashMapsList[2]:
				newUb=hashMapsList[1].get(b)+hashMapsList[2].get(b)+currentPerformances[0]

			elif b in hashMapsList[0] and b not in hashMapsList[1] and b in hashMapsList[2]:
				newUb=hashMapsList[0].get(b)+hashMapsList[2].get(b)+currentPerformances[1]

			elif b in hashMapsList[0] and b in hashMapsList[1] and b in hashMapsList[2]:
				newUb=hashMapsList[0].get(b)+hashMapsList[1].get(b)+hashMapsList[2].get(b)

			upperBoundsDict[b]=newUb

	elif numOfChoices==4:

			if b in hashMapsList[0] and b not in hashMapsList[1] and not in hashMapsList[2] and b not in hashMapsList[3]:
				newUb=hashMapsList[0].get(b)+currentPerformances[1]+currentPerformances[2]+currentPerformances[3]

			elif b not in hashMapsList[0] and b in hashMapsList[1] and not in hashMapsList[2] and b not in hashMapsList[3]:
				newUb=hashMapsList[1].get(b)+currentPerformances[0]+currentPerformances[2]+currentPerformances[3]

			elif b not in hashMapsList[0] and b not in hashMapsList[1] and b in hashMapsList[2] and b not in hashMapsList[3]:
				newUb=hashMapsList[2].get(b)+currentPerformances[0]+currentPerformances[1]+currentPerformances[3]

			elif b not in hashMapsList[0] and b not in hashMapsList[1] and b not in hashMapsList[2] and b in hashMapsList[3]:
				newUb=hashMapsList[3].get(b)+currentPerformances[0]+currentPerformances[1]+currentPerformances[2]

			elif b in hashMapsList[0] and b in hashMapsList[1] and b not in hashMapsList[2] and b not in hashMapsList[3]:
				newUb=hashMapsList[0].get(b)+hashMapsList[1].get(b)+currentPerformances[2]+currentPerformances[3]

			elif b in hashMapsList[0] and b not in hashMapsList[1] and b in hashMapsList[2] and b not in hashMapsList[3]:
				newUb=hashMapsList[0].get(b)+hashMapsList[2].get(i)+currentPerformances[1]+currentPerformances[3]

			elif b in hashMapsList[0] and b not in hashMapsList[1] and b not in hashMapsList[2] and b in hashMapsList[3]:
				newUb=hashMapsList[0].get(b)+hashMapsList[3].get(i)+currentPerformances[1]+currentPerformances[2]

			elif b not in hashMapsList[0] and b in hashMapsList[1] and b in hashMapsList[2] and b not in hashMapsList[3]:
				newUb=hashMapsList[1].get(b)+hashMapsList[2].get(b)+currentPerformances[0]+currentPerformances[3]

			elif b not in hashMapsList[0] and b in hashMapsList[1] and b not in hashMapsList[2] and b in hashMapsList[3]:
				newUb=hashMapsList[1].get(b)+hashMapsList[3].get(b)+currentPerformances[0]+currentPerformances[2]

			elif b not in hashMapsList[0] and b not in hashMapsList[1] and b in hashMapsList[2] and b in hashMapsList[3]:
				newUb=hashMapsList[2].get(b)+hashMapsList[3].get(b)+currentPerformances[0]+currentPerformances[1]

			elif b not in hashMapsList[0] and b in hashMapsList[1] and b in hashMapsList[2] and b in hashMapsList[3]:
				newUb=hashMapsList[1].get(b)+hashMapsList[2].get(b)+hashMapsList[3].get(b)+currentPerformances[0]

			elif b in hashMapsList[0] and b not in hashMapsList[1] and b in hashMapsList[2] and b in hashMapsList[3]:
				newUb=hashMapsList[0].get(b)+hashMapsList[2].get(b)+hashMapsList[3].get(b)+currentPerformances[1]

			elif b in hashMapsList[0] and b in hashMapsList[1] and b not in hashMapsList[2] and b in hashMapsList[3]:
				newUb=hashMapsList[0].get(b)+hashMapsList[1].get(b)+hashMapsList[3].get(b)+currentPerformances[2]

			elif b in hashMapsList[0] and b in hashMapsList[1] and b in hashMapsList[2] and b not in hashMapsList[3]:
				newUb=hashMapsList[0].get(b)+hashMapsList[1].get(b)+hashMapsList[2].get(b)+currentPerformances[3]

			elif b in hashMapsList[0] and b in hashMapsList[1] and b in hashMapsList[2]:
				newUb=hashMapsList[0].get(b)+hashMapsList[1].get(b)+hashMapsList[2].get(b)

			upperBoundsDict[b]=newUb

	'''
	elif numOfChoices==5:
	'''	
	upperBoundsDictK=sorted(upperBoundsDict.items(), reverse=True, key=lambda kv: kv[1])
	upperBoundsDict=dict(upperBoundsDictK)
	return upperBoundsDict

def lara(currentIds, currentPerformances, hashMapsList, t, T, W, upperBoundsDict, numOfChoices, numOfAccesses, k):

	Wk=sorted(W, reverse=True, key=itemgetter(1))
	W=Wk
	
	if t<T: #growingPhase
		
		if numOfChoices==2:

			numOfAccesses+=2

			f1Lb, f1Ub, f2Lb, f2Ub=calcBounds(hashMapsList, currentPerformances, numOfChoices)

			upperBoundsDict[currentIds[0]]=f1Ub
			upperBoundsDict[currentIds[1]]=f2Ub
			upperBoundsDict= updateUpperBounds(upperBoundsDict, currentPerformances, hashMapsList)
			upperBoundsDictK=sorted(upperBoundsDict.items(), reverse=True, key=lambda kv: kv[1])
			upperBoundsDict=dict(upperBoundsDictK)

			W, t, upperBoundsDict=insertInW(f1Lb, currentIds[0], upperBoundsDict, W, t, k)	
			W, t, upperBoundsDict=insertInW(f2Lb, currentIds[1], upperBoundsDict, W, t, k)
			return [W, t, T, upperBoundsDict, numOfAccesses, 0]
		'''
		elif numOfChoices==3:

			numOfAccesses+=3
			f1Lb, f1Ub, f2Lb, f2Ub, f3Lb, f3Ub=calcBounds(hashMapsList, currentPerformances, numOfChoices)
			upperBoundsDict[currentIds[0]]=f1Ub 
			upperBoundsDict[currentIds[1]]=f2Ub
			upperBoundsDict[currentIds[2]]=f3Ub
			upperBoundsDictK=sorted(upperBoundsDict.items(), reverse=True, key=lambda kv: kv[1])
			upperBoundsDict=dict(upperBoundsDictK)

			W, t, upperBoundsDict=insertInW(f1Lb, currentIds[0], upperBoundsDict, W, t, k)
			W, t, upperBoundsDict=insertInW(f2Lb, currentIds[1], upperBoundsDict, W, t, k)
			W, t, upperBoundsDict=insertInW(f3Lb, currentIds[2], upperBoundsDict, W, t, k)

		elif numOfChoices==4:

			numOfAccesses+=4
			f1Lb, f1Ub, f2Lb, f2Ub, f3Lb, f3Ub, f4Lb, f4Ub=calcBounds(hashMapsList, currentPerformances, numOfChoices)
			upperBoundsDict[currentIds[0]]=f1Ub 
			upperBoundsDict[currentIds[1]]=f2Ub
			upperBoundsDict[currentIds[2]]=f3Ub
			upperBoundsDict[currentIds[3]]=f4Ub
			upperBoundsDictK=sorted(upperBoundsDict.items(), reverse=True, key=lambda kv: kv[1])
			upperBoundsDict=dict(upperBoundsDictK)

			W, t, upperBoundsDict=insertInW(f1Lb, currentIds[0], upperBoundsDict, W, t, k)
			W, t, upperBoundsDict=insertInW(f2Lb, currentIds[1], upperBoundsDict, W, t, k)
			W, t, upperBoundsDict=insertInW(f3Lb, currentIds[2], upperBoundsDict, W, t, k)
			W, t, upperBoundsDict=insertInW(f4Lb, currentIds[3], upperBoundsDict, W, t, k)

		elif numOfChoices==5:

			numOfAccesses+=5
			f1Lb, f1Ub, f2Lb, f2Ub, f3Lb, f3Ub, f4Lb, f4Ub, f5Lb, f5Ub=calcBounds(hashMapsList, currentPerformances, numOfChoices)
			upperBoundsDict[currentIds[0]]=f1Ub 
			upperBoundsDict[currentIds[1]]=f2Ub
			upperBoundsDict[currentIds[2]]=f3Ub
			upperBoundsDict[currentIds[3]]=f4Ub
			upperBoundsDict[currentIds[4]]=f5Ub
			upperBoundsDictK=sorted(upperBoundsDict.items(), reverse=True, key=lambda kv: kv[1])
			upperBoundsDict=dict(upperBoundsDictK)

			W, t, upperBoundsDict=insertInW(f1Lb, currentIds[0], upperBoundsDict, W, t, k)
			W, t, upperBoundsDict=insertInW(f2Lb, currentIds[1], upperBoundsDict, W, t, k)
			W, t, upperBoundsDict=insertInW(f3Lb, currentIds[2], upperBoundsDict, W, t, k)
			W, t, upperBoundsDict=insertInW(f4Lb, currentIds[3], upperBoundsDict, W, t, k)
			W, t, upperBoundsDict=insertInW(f5Lb, currentIds[4], upperBoundsDict, W, t, k)
		'''
		

	else: #shrinkingPhase
		#keeping only the upperbounds that are not in W 
		for ks in W:
			if ks[0] in upperBoundsDict:
				del upperBoundsDict[ks[0]]

		upperBoundsDictK=sorted(upperBoundsDict.items(), reverse=True, key=lambda kv: kv[1])
		upperBoundsDict=dict(upperBoundsDictK)
		Wk=sorted(W, reverse=True, key=itemgetter(1))
		W=Wk
		t=W[-1][1]

		print('upperBoundsDict', upperBoundsDict)
		print('W', W)
		print('numOfAccesses', numOfAccesses)

		if t<next(iter(upperBoundsDict.values())): #the first value in upperBoundsDict

			if numOfChoices==2:

				f1Lb, f1Ub, f2Lb, f2Ub=calcBounds(hashMapsList, currentPerformances, numOfChoices)
				
				numOfAccesses+=1
				
				found=0
				pos=0

				for ks in W:
					if ks[0]==currentIds[0]: #update W
						found=1
						W.pop(pos)
						W.insert(pos, [currentIds[0], f1Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[-1][1]
						break					
					else:
						pos+=1

				if found==0:	#update UpperBoundDict
					if currentIds[0] in hashMapsList[1]:
						upperBoundsDict[currentIds[0]]=f1Ub
						upperBoundsDictK=sorted(upperBoundsDict.items(), reverse=True, key=lambda kv: kv[1])
						upperBoundsDict=dict(upperBoundsDictK)
					else:
						pass
			
				#CHECKING NOW AGAIN	
				if T==0 or t>=next(iter(upperBoundsDict.values())):
					return [W, t, T, upperBoundsDict, numOfAccesses, 1]

				#NEXT
				numOfAccesses+=1
				
				found=0
				pos=0

				for ks in W:
					if ks[0]==currentIds[1]: #update W
						found=1
						W.pop(pos)
						W.insert(pos, [currentIds[1], f2Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[-1][1]
						break					
					else:
						pos+=1

				if found==0:	#update UpperBoundDict
					if currentIds[1] in hashMapsList[0]:
						upperBoundsDict[currentIds[1]]=f1Ub
						upperBoundsDictK=sorted(upperBoundsDict.items(), reverse=True, key=lambda kv: kv[1])
						upperBoundsDict=dict(upperBoundsDictK)
					else:
						pass
				
				#CHECKING NOW AGAIN	
				if T==0 or t>=next(iter(upperBoundsDict.values())):
					return [W, t, T, upperBoundsDict, numOfAccesses, 1]

				return [W, t, T, upperBoundsDict, numOfAccesses, 0]
			'''

			elif numOfChoices==3:

			elif numOfChoices==4:

			elif numOfChoices==5:
			'''
		elif T==0 or t>=next(iter(upperBoundsDict.values())):

			return [W, t, T, upperBoundsDict, numOfAccesses, 1]



if __name__ == '__main__':
	
	inputs=getINput()
	chosenCategories=inputs[0]
	k=inputs[1]
	counter=0
	with open('topks.csv', 'w', encoding='UTF-8') as rp1: 
		csv_writer = csv.writer(rp1, delimiter=',')
		for topks in topKEvaluation(chosenCategories, k):
			if k==0:
				print('No results. 0 num of numOfAccesses. Terminate.')
				break
			elif counter<k:
				csv_writer.writerow(topks[:-1])
				print(topks[:-1])
				counter+=1
			if counter==k-1:
				accesses=['NUMBER OF ACCESSES', topks[-1]]
				csv_writer.writerow(accesses)
				print('numOfAccesses', topks[-1])
				break