import csv
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

				performance1=normalization(int(data1[1]), maxv1) 
				performance2=normalization(int(data2[1]), maxv2) 
				hashMap1.update({int(data1[0]): performance1})
				hashMap2.update({int(data2[0]): performance2})	
				T=performance1+performance2
				currentIds=[data1[0], data2[0]]
				currentPerformances=[performance1, performance2]
				hashMapsList=[hashMap1, hashMap2]
				R=lara(currentIds, currentPerformances, hashMapsList, t, T, W, upperBoundsDict, numOfChoices, numOfAccesses)
				W=R[0]
				canYield=R[1]
				if canYield==1:
					print(W)
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
				R=lara(currentIds, currentPerformances, hashMapsList, t, T, W, upperBoundsDict, numOfChoices, numOfAccesses)
				W=R[0]
				canYield=R[1]
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
				R=lara(currentIds, currentPerformances, hashMapsList, t, T, W, upperBoundsDict, numOfChoices, numOfAccesses)
				print('im here')
				W=R[0]
				canYield=R[1]
				if canYield==1:
					for ks in W:
						topKPlayer=hashMap.get(ks[0])
						yield [str(topKPlayer[0]), int(topKPlayer[cat[0]+1]), int(topKPlayer[cat[1]+1]), int(topKPlayer[cat[2]+1]), int(topKPlayer[cat[3]+1]), numOfAccesses]

		elif numOfChoices==5: #cat[0] cat[1] cat[2] cat[3] cat[4]

			for row in zip(df1,df2,df3,df4,df5):
				data1,data2, data3, data4=fixData(row, numOfChoices)

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
				R=lara(currentIds, currentPerformances, hashMapsList, t, T, W, upperBoundsDict, numOfChoices, numOfAccesses)
				W=R[0]
				canYield=R[1]
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


def lara(currentIds, currentPerformances, hashMapsList, t, T, W, upperBoundsDict, numOfChoices, numOfAccesses):
	print('W $$$$$$$$$$', W)
	#growingPhase
	if t<T:

		if numOfChoices==2:
			numOfAccesses+=2
			#update lower bounds
			for i in hashMapsList[0]:

				if i not in hashMapsList[1]:

					f1Lb=hashMapsList[0].get(i)	
					f1Ub=hashMapsList[0].get(i)+currentPerformances[1]		
				else:			
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)
				
				upperBoundsDict[i]=f1Ub
			
				if f1Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							print('before updated W: ', W)
							W.pop(pos)
							W.insert(pos, [i,f1Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f1Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						print('W:', W)
						t=W[0][1]
						print('t', t)
							

					
			for i in hashMapsList[1]:

				if i not in hashMapsList[0]:

					f2Lb=hashMapsList[1].get(i)	
					f2Ub=hashMapsList[1].get(i)+currentPerformances[0]
					
				elif i in hashMapsList[0]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[0].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[0].get(i)

				upperBoundsDict[i]=f2Ub

				if f2Lb>t:
					print('before updated W:', W)
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f2Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f2Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						print('W:', W)
						t=W[0][1]
						print('t', t)

		elif numOfChoices==3:
			numOfAccesses+=3
			#update lower bounds
			for i in hashMapsList[0]:

				if i not in hashMapsList[1] and i not in hashMapsList[2]:
					f1Lb=hashMapsList[0].get(i)
					f1Ub=hashMapsList[0].get(i)+currentPerformances[1]+currentPerformances[2]

				elif i in hashMapsList[1] and i not in hashMapsList[2]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+currentPerformances[2]

				elif i not in hashMapsList[1] and i in hashMapsList[2]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+currentPerformances[1]

				elif i in hashMapsList[1] and i in hashMapsList[2]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)

				upperBoundsDict[i]=f1Ub

				if f1Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f1Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f1Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]

			for i in hashMapsList[1]:

				if i not in hashMapsList[0] and i not in hashMapsList[2]:
					f2Lb=hashMapsList[1].get(i)		
					f2Ub=hashMapsList[1].get(i)+currentPerformances[0]+currentPerformances[2]

				elif i in hashMapsList[0] and i not in hashMapsList[2]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)
					f2Ub==hashMapsList[0].get(i)+hashMapsList[1].get(i)+currentPerformances[2]

				elif i not in hashMapsList[0] and i in hashMapsList[2]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[0]

				elif i in hashMapsList[0] and i in hashMapsList[2]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)

				upperBoundsDict[f2Ub]=i
				
				if f2Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f2Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f2Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]

			for i in hashMapsList[2]:

				if i not in hashMapsList[0] and i not in hashMapsList[1]:
					f3Lb=hashMapsList[2].get(i)	
					f3Ub=hashMapsList[2].get(i)+currentPerformances[0]+currentPerformances[1]	

				elif i in hashMapsList[0] and i not in hashMapsList[1]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+currentPerformances[1]	

				elif i not in hashMapsList[0] and i in hashMapsList[1]:
					f3Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f3Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[0]	

				elif i in hashMapsList[0] and i in hashMapsList[1]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)	

				upperBoundsDict[i]=f3Ub

				if f3Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f3Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f3Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]
						


		elif numOfChoices==4:
			numOfAccesses+=4
			#update lower bounds
			for i in hashMapsList[0]:

				if i not in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[3]:
					f1Lb=hashMapsList[0].get(i)	
					f1Ub=hashMapsList[0].get(i)+currentPerformances[1]+currentPerformances[2]+currentPerformances[3]

				elif i in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[3]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+currentPerformances[2]+currentPerformances[3]

				elif i not in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[3]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+currentPerformances[1]+currentPerformances[3]

				elif i not in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[3]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[3].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[3].get(i)+currentPerformances[1]+currentPerformances[2]

				elif i in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[3]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[3]

				elif i in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[3]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+currentPerformances[2]

				elif i not in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[3]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[1]

				elif i in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[3]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)

				upperBoundsDict[i]=f1Ub
			
				if f1Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f1Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f1Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]


			for i in hashMapsList[1]:

				if i not in hashMapsList[0] and i not in hashMapsList[2] and i not in hashMapsList[3]:
					f2Lb=hashMapsList[1].get(i)
					f2Lb=hashMapsList[1].get(i)+currentPerformances[0]+currentPerformances[2]+currentPerformances[3]

				elif i in hashMapsList[0] and i not in hashMapsList[2] and i not in hashMapsList[3]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+currentPerformances[2]+currentPerformances[3]

				elif i not in hashMapsList[0] and i in hashMapsList[2] and i not in hashMapsList[3]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[0]+currentPerformances[3]

				elif i not in hashMapsList[0] and i not in hashMapsList[2] and i in hashMapsList[3]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[3].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[2]

				elif i in hashMapsList[0] and i in hashMapsList[2] and i not in hashMapsList[3]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[3]

				elif i in hashMapsList[0] and i not in hashMapsList[2] and i in hashMapsList[3]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+currentPerformances[2]

				elif i not in hashMapsList[0] and i in hashMapsList[2] and i in hashMapsList[3]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[0]

				elif i in hashMapsList[0] and i in hashMapsList[2] and i in hashMapsList[3]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)

				upperBoundsDict[i]=f2Ub

				if f2Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f2Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f2Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]


			for i in hashMapsList[2]:

				if i not in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[3]:
					f3Lb=hashMapsList[2].get(i)		
					f3Ub=hashMapsList[2].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[3]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[3]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+currentPerformances[1]+currentPerformances[3]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[3]:
					f3Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f3Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[0]+currentPerformances[3]

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[3]:
					f3Lb=hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f3Ub=hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[1]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[3]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[3]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[3]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[1]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[3]:
					f3Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f3Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[0]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[3]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)

				upperBoundsDict[i]=f3Ub

				if f3Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f3Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f3Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]


			for i in hashMapsList[3]:

				if i not in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[2]:
					f4Lb=hashMapsList[3].get(i)		
					f4Ub=hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[2]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[2]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[3].get(i)+currentPerformances[1]+currentPerformances[2]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[2]:
					f4Lb=hashMapsList[1].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[1].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[2]

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[2]:
					f4Lb=hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[1]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[2]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+currentPerformances[2]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[2]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[1]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[2]:
					f4Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[0]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[2]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)

				upperBoundsDict[i]=f4Ub

				if f4Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f4Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f4Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]


		elif numOfChoices==5:
			numOfAccesses+=5
			#update lower bounds
			for i in hashMapsList[0]:

				if i not in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)		
					f1Ub=hashMapsList[0].get(i)+currentPerformances[1]+currentPerformances[2]+currentPerformances[3]+currentPerformances[4]

				elif i in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+currentPerformances[2]+currentPerformances[3]+currentPerformances[4]

				elif i not in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+currentPerformances[1]+currentPerformances[3]+currentPerformances[4]

				elif i not in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[3].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[3].get(i)+currentPerformances[1]+currentPerformances[2]+currentPerformances[4]

				elif i not in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[4].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[4].get(i)+currentPerformances[1]+currentPerformances[2]+currentPerformances[3]

				elif i in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[3]+currentPerformances[4]

				elif i in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+currentPerformances[2]+currentPerformances[4]

				elif i in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[4].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[4].get(i)+currentPerformances[2]+currentPerformances[3]

				elif i not in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[1]+currentPerformances[4]

				elif i not in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[1]+currentPerformances[3]

				elif i not in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[3] and i in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[1]+currentPerformances[2]

				elif i not in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[3] and i in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[1]

				elif i in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[3] and i in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[2]

				elif i in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[3]

				elif i in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[4]

				elif i in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[3] and i in hashMapsList[4]:
					f1Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f1Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)

				upperBoundsDict[i]=f1Ub

				if f1Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f1Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f1Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]


			for i in hashMapsList[1]:

				if i not in hashMapsList[0] and i not in hashMapsList[2] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f2Lb=hashMapsList[1].get(i)	
					f2Ub=hashMapsList[1].get(i)+currentPerformances[0]+currentPerformances[2]+currentPerformances[3]+currentPerformances[4]	

				elif i in hashMapsList[0] and i not in hashMapsList[2] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+currentPerformances[2]+currentPerformances[3]+currentPerformances[4]

				elif i not in hashMapsList[0] and i in hashMapsList[2] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[0]+currentPerformances[3]+currentPerformances[4]

				elif i not in hashMapsList[0] and i not in hashMapsList[2] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[3].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[2]+currentPerformances[4]

				elif i not in hashMapsList[0] and i not in hashMapsList[2] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[4].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[2]+currentPerformances[3]

				elif i in hashMapsList[0] and i in hashMapsList[2] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[3]+currentPerformances[4]

				elif i in hashMapsList[0] and i not in hashMapsList[2] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+currentPerformances[2]+currentPerformances[4]

				elif i in hashMapsList[0] and i not in hashMapsList[2] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[4].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[4].get(i)+currentPerformances[2]+currentPerformances[3]

				elif i not in hashMapsList[0] and i in hashMapsList[2] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[4]

				elif i not in hashMapsList[0] and i in hashMapsList[2] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[3]

				elif i not in hashMapsList[0] and i not in hashMapsList[2] and i in hashMapsList[3] and i in hashMapsList[4]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[2]


				elif i not in hashMapsList[0] and i in hashMapsList[2] and i in hashMapsList[3] and i in hashMapsList[4]:
					f2Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f2Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]

				elif i in hashMapsList[0] and i not in hashMapsList[2] and i in hashMapsList[3] and i in hashMapsList[4]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[2]

				elif i in hashMapsList[0] and i in hashMapsList[2] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[3]

				elif i in hashMapsList[0] and i in hashMapsList[2] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[4]

				elif i in hashMapsList[0] and i in hashMapsList[2] and i in hashMapsList[3] and i in hashMapsList[4]:
					f2Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f2Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)

				upperBoundsDict[i]=f2Ub

				if f2Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f2Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f2Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]

			for i in hashMapsList[2]:

				if i not in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f3Lb=hashMapsList[2].get(i)		
					f3Ub=hashMapsList[2].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[3]+currentPerformances[4]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+currentPerformances[1]+currentPerformances[3]+currentPerformances[4]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f3Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f3Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[0]+currentPerformances[3]+currentPerformances[4]

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f3Lb=hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f3Ub=hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[4]

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f3Lb=hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f3Ub=hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[3]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[3] and i not in hashMapsList[4]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+currentPerformances[3]+currentPerformances[4]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[1]+currentPerformances[4]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[1]+currentPerformances[3]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f3Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[4]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f3Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f3Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[3]

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[3] and i in hashMapsList[4]:
					f3Lb=hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f3Ub=hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[1]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[3] and i in hashMapsList[4]:
					f3Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f3Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[3] and i in hashMapsList[4]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[1]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[3] and i in hashMapsList[4]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[3]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[3] and i not in hashMapsList[4]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f3Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[4]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[3] and i in hashMapsList[4]:
					f3Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f3Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)

				upperBoundsDict[i]=f3Ub

				if f3Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f3Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f3Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]


			for i in hashMapsList[3]:

				if i not in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[4]:
					f4Lb=hashMapsList[3].get(i)		
					f4Ub=hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[2]+currentPerformances[4]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[4]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[3].get(i)+currentPerformances[1]+currentPerformances[2]+currentPerformances[4]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[4]:
					f4Lb=hashMapsList[1].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[1].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[2]+currentPerformances[4]

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[4]:
					f4Lb=hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[4]

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[4]:
					f4Lb=hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f4Ub=hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[2]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[4]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+currentPerformances[2]+currentPerformances[4]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[4]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[1]+currentPerformances[4]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[4]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[1]+currentPerformances[2]


				elif i not in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[4]:
					f4Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[0]+currentPerformances[4]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[4]:
					f4Lb=hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f4Ub=hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[2]

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[4]:
					f4Lb=hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f4Ub=hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[1]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[4]:
					f4Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f4Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[4]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[1]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[4]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[2]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[4]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+currentPerformances[4]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[4]:
					f4Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f4Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)

				upperBoundsDict[i]=f4Ub

				if f4Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f4Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f4Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]



			for i in hashMapsList[4]:

				if i not in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[3]:
					f5Lb=hashMapsList[4].get(i)	
					f5Ub=hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[2]+currentPerformances[3]	

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[3]:
					f5Lb=hashMapsList[0].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[0].get(i)+hashMapsList[4].get(i)+currentPerformances[1]+currentPerformances[2]+currentPerformances[3]	

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[3]:
					f5Lb=hashMapsList[1].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[1].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[2]+currentPerformances[3]	

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[3]:
					f5Lb=hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[3]	

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[3]:
					f5Lb=hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[1]+currentPerformances[2]	

				elif i in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[2] and i not in hashMapsList[3]:
					f5Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[4].get(i)+currentPerformances[2]+currentPerformances[3]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[3]:
					f5Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[1]+currentPerformances[3]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[3]:
					f5Lb=hashMapsList[0].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[0].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[1]+currentPerformances[2]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[3]:
					f5Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[3]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[3]:
					f5Lb=hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[2]

				elif i not in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[3]:
					f5Lb=hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]+currentPerformances[1]

				elif i not in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[3]:
					f5Lb=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[0]

				elif i in hashMapsList[0] and i not in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[3]:
					f5Lb=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[0].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[1]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i not in hashMapsList[2] and i in hashMapsList[3]:
					f5Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)+currentPerformances[2]

				elif i in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[2] and i not in hashMapsList[3]:
					f5Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[4].get(i)+currentPerformances[3]


				elif i in hashMapsList[0] and i in hashMapsList[1] and i in hashMapsList[2] and i in hashMapsList[3]:
					f5Lb=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)
					f5Ub=hashMapsList[0].get(i)+hashMapsList[1].get(i)+hashMapsList[2].get(i)+hashMapsList[3].get(i)+hashMapsList[4].get(i)

				upperBoundsDict[i]=f5Ub

				if f5Lb>t:
					found=0
					pos=0
					for ks in W:
						if ks[0]==i:
							found=1
							W.pop(pos)
							W.insert(pos, [i,f5Lb])
							Wk=sorted(W, reverse=True, key=itemgetter(1))
							W=Wk
							t=W[0][1]
							break		
						else:
							pos+=1
	
					if found==0:
						W.insert(0, [i, f5Lb])
						Wk=sorted(W, reverse=True, key=itemgetter(1))
						W=Wk
						t=W[0][1]

		return [W,0]




	#shrinkingPhase
	else:

		upperBoundsDictK=sorted(upperBoundsDict.items(), reverse=True, key=lambda kv: kv[1])
		upperBoundsDict=dict(upperBoundsDictK)
		#print('upperBoundsDict: ', upperBoundsDict)

		if t<next(iter(upperBoundsDict.values())): #the first value in upperBoundsDict
		
			if numOfChoices==2:
				print('w is:', W)
				numOfAccesses+=1

				if currentIds[0] in hashMapsList[1]:
					newUb=hashMapsList[1].get(currentIds[0])+currentPerformances[0]
				
				upperBoundsDict[currentIds[0]]=newUb
				upperBoundsDictK=sorted(upperBoundsDict.items(), key=lambda kv: kv[1])
				upperBoundsDict=dict(upperBoundsDictK)

				if t>=next(iter(upperBoundsDict.values())):
					return [W,1]


				numOfAccesses+=1


				if currentIds[1] in hashMapsList[0]:
					newUb=hashMapsList[0].get(currentIds[1])+currentPerformances[1]

				upperBoundsDict[currentIds[1]]=newUb				
				upperBoundsDictK=sorted(upperBoundsDict.items(), key=lambda kv: kv[1])
				upperBoundsDict=dict(upperBoundsDictK)
				if t>=next(iter(upperBoundsDict.values())):
					return [W,1]



			elif numOfChoices==3:

				numOfAccesses+=1

				if currentIds[0] in hashMapsList[1] and currentIds[0] not in hashMapsList[2]:
					newUb=hashMapsList[1].get(currentIds[0])+hashMapsList[2].get(hashMapsList[2].keys()[-2])+currentPerformances[0] #-2 wste na parei to prwteleytaio(giati diavasa to new sti praksi aas min to exw anoiksei akomi)				

				elif currentIds[0] not in hashMapsList[1] and currentIds[0] in hashMapsList[2]:
					newUb=hashMapsList[2].get(currentIds[0])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+currentPerformances[0] #-2 wste na parei to prwteleytaio(giati diavasa to new sti praksi aas min to exw anoiksei akomi)

				elif currentIds[0] in hashMapsList[1] and currentIds[0] in hashMapsList[2]:
					newUb=hashMapsList[1].get(currentIds[0])+hashMapsList[2].get(currentIds[0])+currentPerformances[0] #-2 wste na parei to prwteleytaio(giati diavasa to new sti praksi aas min to exw anoiksei akomi)
	

				upperBoundsDict[currentIds[0]]=newUb
				upperBoundsDictK=sorted(upperBoundsDict.items(), key=lambda kv: kv[1])
				upperBoundsDict=dict(upperBoundsDictK)
				if t>=next(iter(upperBoundsDict.values())):
					return [W,1]


				numOfAccesses+=1


				if currentIds[1] in hashMapsList[0] and currentIds[1] not in hashMapsList[2]:
					newUb=hashMapsList[0].get(currentIds[1])+hashMapsList[2].get(hashMapsList[2].keys()[-2])+currentPerformances[1]	

				elif currentIds[1] not in hashMapsList[0] and currentIds[1] in hashMapsList[2]:
					newUb=hashMapsList[2].get(currentIds[1])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+currentPerformances[1] 

				elif currentIds[1] in hashMapsList[0] and currentIds[1] in hashMapsList[2]:
					newUb=hashMapsList[0].get(currentIds[1])+hashMapsList[2].get(currentIds[1])+currentPerformances[1] 
				

				upperBoundsDict[currentIds[1]]=newUb
				upperBoundsDictK=sorted(upperBoundsDict.items(), key=lambda kv: kv[1])
				upperBoundsDict=dict(upperBoundsDictK)
				if t>=next(iter(upperBoundsDict.values())):
					return [W,1]


				numOfAccesses+=1


				if currentIds[2] in hashMapsList[0] and currentIds[2] not in hashMapsList[1]:
					newUb=hashMapsList[0].get(currentIds[2])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+currentPerformances[2]
					
				elif currentIds[2] not in hashMapsList[0] and currentIds[2] in hashMapsList[1]:
					newUb=hashMapsList[1].get(currentIds[2])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+currentPerformances[2] 

				elif currentIds[2] in hashMapsList[0] and currentIds[2] in hashMapsList[1]:
					newUb=hashMapsList[0].get(currentIds[2])+hashMapsList[1].get(currentIds[2])+currentPerformances[2] 


				upperBoundsDict[currentIds[2]]=newUb
				upperBoundsDictK=sorted(upperBoundsDict.items(), key=lambda kv: kv[1])
				upperBoundsDict=dict(upperBoundsDictK)
				if t>=next(iter(upperBoundsDict.values())):
					return [W,1]


			elif numOfChoices==4:

				numOfAccesses+=1

				if currentIds[0] in hashMapsList[1] and currentIds[0] not in hashMapsList[2] and currentIds[0] not in hashMapsList[3]:
					newUb=hashMapsList[1].get(currentIds[0])+hashMapsList[2].get(hashMapsList[2].keys()[-2])+hashMapsList[3].get(hashMapsList[3].keys()[-2])+currentPerformances[0] 			

				elif currentIds[0] not in hashMapsList[1] and currentIds[0] in hashMapsList[2] and currentIds[0] not in hashMapsList[3]:
					newUb=hashMapsList[2].get(currentIds[0])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+hashMapsList[3].get(hashMapsList[3].keys()[-2])+currentPerformances[0] 

				elif currentIds[0] not in hashMapsList[1] and currentIds[0] not in hashMapsList[2] and currentIds[0] in hashMapsList[3]:
					newUb=hashMapsList[3].get(currentIds[0])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+hashMapsList[2].get(hashMapsList[2].keys()[-2])+currentPerformances[0] 

				elif currentIds[0] in hashMapsList[1] and currentIds[0] in hashMapsList[2] and currentIds[0] not in hashMapsList[3]:
					newUb=hashMapsList[1].get(currentIds[0])+hashMapsList[2].get(currentIds[0])+hashMapsList[3].get(hashMapsList[3].keys()[-2])+currentPerformances[0]
			
				elif currentIds[0] in hashMapsList[1] and currentIds[0] not in hashMapsList[2] and currentIds[0] in hashMapsList[3]:
					newUb=hashMapsList[1].get(currentIds[0])+hashMapsList[3].get(currentIds[0])+hashMapsList[2].get(hashMapsList[2].keys()[-2])+currentPerformances[0]

				elif currentIds[0] not in hashMapsList[1] and currentIds[0] in hashMapsList[2] and currentIds[0] in hashMapsList[3]:
					newUb=hashMapsList[2].get(currentIds[0])+hashMapsList[3].get(currentIds[0])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+currentPerformances[0]

				elif currentIds[0] in hashMapsList[1] and currentIds[0] in hashMapsList[2] and currentIds[0] in hashMapsList[3]:
					newUb=hashMapsList[1].get(currentIds[0])+hashMapsList[2].get(currentIds[0])+hashMapsList[3].get(currentIds[0])+currentPerformances[0]

				upperBoundsDict[currentIds[0]]=newUb
				upperBoundsDictK=sorted(upperBoundsDict.items(), key=lambda kv: kv[1])
				upperBoundsDict=dict(upperBoundsDictK)
				if t>=next(iter(upperBoundsDict.values())):
					return [W,1]


				numOfAccesses+=1


				if currentIds[1] in hashMapsList[0] and currentIds[1] not in hashMapsList[2] and currentIds[1] not in hashMapsList[3]:
					newUb=hashMapsList[0].get(currentIds[1])+hashMapsList[2].get(hashMapsList[2].keys()[-2])+hashMapsList[3].get(hashMapsList[3].keys()[-2])+currentPerformances[1] 			

				elif currentIds[1] not in hashMapsList[0] and currentIds[1] in hashMapsList[2] and currentIds[1] not in hashMapsList[3]:
					newUb=hashMapsList[2].get(currentIds[1])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+hashMapsList[3].get(hashMapsList[3].keys()[-2])+currentPerformances[1] 

				elif currentIds[1] not in hashMapsList[0] and currentIds[1] not in hashMapsList[2] and currentIds[1] in hashMapsList[3]:
					newUb=hashMapsList[3].get(currentIds[1])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+hashMapsList[2].get(hashMapsList[2].keys()[-2])+currentPerformances[1] 

				elif currentIds[1] in hashMapsList[0] and currentIds[1] in hashMapsList[2] and currentIds[1] not in hashMapsList[3]:
					newUb=hashMapsList[0].get(currentIds[1])+hashMapsList[2].get(currentIds[1])+hashMapsList[3].get(hashMapsList[3].keys()[-2])+currentPerformances[1]
			
				elif currentIds[1] in hashMapsList[0] and currentIds[1] not in hashMapsList[2] and currentIds[1] in hashMapsList[3]:
					newUb=hashMapsList[0].get(currentIds[1])+hashMapsList[3].get(currentIds[1])+hashMapsList[2].get(hashMapsList[2].keys()[-2])+currentPerformances[1]

				elif currentIds[1] not in hashMapsList[0] and currentIds[1] in hashMapsList[2] and currentIds[1] in hashMapsList[3]:
 					newUb=hashMapsList[2].get(currentIds[1])+hashMapsList[3].get(currentIds[1])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+currentPerformances[1]

				elif currentIds[1] in hashMapsList[0] and currentIds[1] in hashMapsList[2] and currentIds[1] in hashMapsList[3]:
					newUb=hashMapsList[0].get(currentIds[1])+hashMapsList[2].get(currentIds[1])+hashMapsList[3].get(currentIds[1])+currentPerformances[1]


				upperBoundsDict[currentIds[1]]=newUb
				upperBoundsDictK=sorted(upperBoundsDict.items(), key=lambda kv: kv[1])
				upperBoundsDict=dict(upperBoundsDictK)
				if t>=next(iter(upperBoundsDict.values())):
					return [W,1]



				numOfAccesses+=1


				if currentIds[2] in hashMapsList[0] and currentIds[2] not in hashMapsList[1] and currentIds[2] not in hashMapsList[3]:
					newUb=hashMapsList[0].get(currentIds[2])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+hashMapsList[3].get(hashMapsList[3].keys()[-2])+currentPerformances[2] 			

				elif currentIds[2] not in hashMapsList[0] and currentIds[2] in hashMapsList[1] and currentIds[2] not in hashMapsList[3]:
					newUb=hashMapsList[1].get(currentIds[2])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+hashMapsList[3].get(hashMapsList[3].keys()[-2])+currentPerformances[2] 

				elif currentIds[2] not in hashMapsList[0] and currentIds[2] not in hashMapsList[1] and currentIds[2] in hashMapsList[3]:
					newUb=hashMapsList[3].get(currentIds[2])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+currentPerformances[2] 

				elif currentIds[2] in hashMapsList[0] and currentIds[2] in hashMapsList[1] and currentIds[2] not in hashMapsList[3]:
					newUb=hashMapsList[0].get(currentIds[2])+hashMapsList[1].get(currentIds[1])+hashMapsList[3].get(hashMapsList[3].keys()[-2])+currentPerformances[2]
			
				elif currentIds[2] in hashMapsList[0] and currentIds[2] not in hashMapsList[1] and currentIds[2] in hashMapsList[3]:
					newUb=hashMapsList[0].get(currentIds[2])+hashMapsList[3].get(currentIds[2])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+currentPerformances[2]

				elif currentIds[2] not in hashMapsList[0] and currentIds[2] in hashMapsList[1] and currentIds[2] in hashMapsList[3]:
					newUb=hashMapsList[1].get(currentIds[1])+hashMapsList[3].get(currentIds[2])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+currentPerformances[2]

				elif currentIds[2] in hashMapsList[0] and currentIds[2] in hashMapsList[1] and currentIds[2] in hashMapsList[3]:
					newUb=hashMapsList[0].get(currentIds[2])+hashMapsList[1].get(currentIds[2])+hashMapsList[3].get(currentIds[2])+currentPerformances[2]

				upperBoundsDict[currentIds[2]]=newUb
				upperBoundsDictK=sorted(upperBoundsDict.items(), key=lambda kv: kv[1])
				upperBoundsDict=dict(upperBoundsDictK)
				if t>=next(iter(upperBoundsDict.values())): #to prwto value tou dict
					return [W,1]


				numOfAccesses+=1


				if currentIds[3] in hashMapsList[0] and currentIds[3] not in hashMapsList[1] and currentIds[3] not in hashMapsList[2]:
					newUb=hashMapsList[0].get(currentIds[3])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+hashMapsList[2].get(hashMapsList[2].keys()[-2])+currentPerformances[3] 			

				elif currentIds[3] not in hashMapsList[0] and currentIds[3] in hashMapsList[1] and currentIds[3] not in hashMapsList[2]:
					newUb=hashMapsList[1].get(currentIds[3])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+hashMapsList[2].get(hashMapsList[2].keys()[-2])+currentPerformances[3] 

				elif currentIds[3] not in hashMapsList[0] and currentIds[3] not in hashMapsList[1] and currentIds[3] in hashMapsList[2]:
					newUb=hashMapsList[2].get(currentIds[3])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+currentPerformances[3] 

				elif currentIds[3] in hashMapsList[0] and currentIds[3] in hashMapsList[1] and currentIds[3] not in hashMapsList[2]:
					newUb=hashMapsList[0].get(currentIds[3])+hashMapsList[1].get(currentIds[1])+hashMapsList[3].get(hashMapsList[3].keys()[-2])+currentPerformances[3]
			
				elif currentIds[3] in hashMapsList[0] and currentIds[3] not in hashMapsList[1] and currentIds[3] in hashMapsList[2]:
					newUb=hashMapsList[0].get(currentIds[3])+hashMapsList[2].get(currentIds[3])+hashMapsList[1].get(hashMapsList[1].keys()[-2])+currentPerformances[3]

				elif currentIds[3] not in hashMapsList[0] and currentIds[3] in hashMapsList[1] and currentIds[3] in hashMapsList[2]:
					newUb=hashMapsList[1].get(currentIds[3])+hashMapsList[2].get(currentIds[3])+hashMapsList[0].get(hashMapsList[0].keys()[-2])+currentPerformances[3]

				elif currentIds[3] in hashMapsList[0] and currentIds[3] in hashMapsList[1] and currentIds[3] in hashMapsList[2]:
					newUb=hashMapsList[0].get(currentIds[3])+hashMapsList[1].get(currentIds[3])+hashMapsList[2].get(currentIds[3])+currentPerformances[3]

				upperBoundsDict[currentIds[3]]=newUb
				upperBoundsDictK=sorted(upperBoundsDict.items(), key=lambda kv: kv[1])
				upperBoundsDict=dict(upperBoundsDictK)
				if t>=next(iter(upperBoundsDict.values())):
					return [W,1]



			elif numOfChoices==5:
				numOfAccesses+=1

		else:

			return [W,1]



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
			else:
				accesses=['NUMBER OF ACCESSES', topks[-1]]
				csv_writer.writerow(accesses)
				print('numOfAccesses', topks[-1])
				break
	 
