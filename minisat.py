import sys
import time
import subprocess

size=9
squareSize=3

class Sudoku:
    def __init__(self, board):
        #index to variable dictionary for getting variable at an index at any time
        self.dict={}
        
        #initialisation of board values
        index=0
        for i in range(size):
            for j in range(size):
                temp=board[index]
                if temp=='.':
                    currVariable=0
                else:
                    currVariable=int(temp)
                self.dict[index]=currVariable                
                index=index+1

    def __str__(self):
 
        sudokuString=""
        for i in range(len(self.dict)):
                  sudokuString= sudokuString+str(self.dict[i])
        #sudokuString=sudokuString+"\n"
        return sudokuString   
    
    def checkComplete(self):

        for i in range(len(self.dict)):
            if self.dict[i].value==0:
                return 0
        return 1 

    def getRowClauses(self):

    	string=""
    	count=0
    	for i in range(0,size*size*size,size*size):
    		count=0
    		p=0
    		while (count<size):   			
    			count=count+1
    			count2=0
    			j=i+1+p
    			while (count2<9):
    				count2=count2+1
    				string=string+str(j)+" "
    				j=j+size
    				#print(j)
    			string=string+"0"+"\n"
    			p=p+1	
    	#print string
    	return string

    def getColumnClauses(self):

    	string=""
    	for i in range(1,size*size+1):
    		count=0
    		j=i
    		while (count<size):
    			count=count+1
    			string=string+str(j)+" "
    			j=j+size*size
    		string=string+"0"+"\n"	
    	#print string
    	return string	

    def getBoxClauses(self):
		string=""		
		for i in range(squareSize):
			for j in range(squareSize):
				for value in range(size):
					for k in range(squareSize):
						for l in range(squareSize):
							val= (k+i*squareSize)*size*size+(l+j*squareSize)*size
							string=string+str(value+val+1)+" "
					
					string=string+"0"+"\n"
		#print string
		return string		

    def getVariableClauses(self):

    	#clauses that atleast one should be true
    	string=""
    	for i in range(len(self.dict)):
    		for j in range(size):
    			string=string+str(size*i+j+1)+" "
    		string=string+"0"+"\n"

    	#clauses that atmost one is true
    	string=string+self.getClauses()
    	#print string
    	return string		
	
    def getClauses(self):
		string=""
		for i in range(1,size*size*size,size):
			for j in range(i,i+size):
				for k in range(j+1,i+size):
					string=string+str(-j)+" "+str(-k)+" "+"0"+"\n"
		#print string
		return string
	
    def convertToDimacs(self):
    	filestr=""
    	valuedVariables=[]
    	filestr=filestr+"p cnf"+" "+str(size*size*size)+" "
    	
    	#calculating number of clauses

    	#for each row,column,box,atleast one =81 constraints + atmostmone one =81*n(n-1)/2 
    	totalClauses=((size*size)*(8+size*size-size))/2 
    	
    	for i in range(len(self.dict)):
    		if self.dict[i]!=0:
    			valuedVariables.append(i)
    	totalClauses=totalClauses+len(valuedVariables)
    	filestr=filestr+str(totalClauses)+"\n"
    	
    	#already assigned constraints
    	for index in valuedVariables:
    		filestr=filestr+str(index*size+self.dict[index])+" "+"0"+"\n"

    	filestr=filestr+self.getRowClauses()
    	filestr=filestr+self.getColumnClauses()
    	filestr=filestr+self.getBoxClauses()
    	filestr=filestr+self.getVariableClauses()
    	#print filestr	
    	return filestr

    def readMinisatOutput(self,file):
		f1=open(file,"r")
		line=f1.readline()
		count=0
		string=""
		while line:
			line=line.strip()
			if count==0 and line=="UNSAT":
				string=string+"No solution exists"
				break	
		
			if count==1:
				values=line.split(" ")
				for value in values:
					value=int(value)
					if value>0:
						index=(value-1)/size
						newValue=value%size
						if newValue==0:
							newValue=size
						#changing values of sudoku object
						self.dict[index]=newValue		
						string=string+str(newValue)
			count=count+1
			line=f1.readline()	
		f1.close
		#print string

if len(sys.argv)!=3:
    print "Invalid arguments"
    sys.exit(0)


#reading of file
counter=0    
totalTime=0 
newSudoku=[]
filename="final"+"minisat"+".txt"
minisatPath=sys.argv[2]

input_file=sys.argv[1]
f1=open(input_file,"r")
line=f1.readline()
sudokuLine=line.split("\r")
#print sudokuLine

for sudoku in sudokuLine:
    counter=counter+1
    if len(sudoku)==0:
        continue
    newSudoku.append(Sudoku(sudoku))
    #if counter==5:
    #    break
f1.close()

for sudoku in newSudoku:
    string=""
    initialTime=time.time()
    string=sudoku.convertToDimacs()
    f=open("minisat.txt", "w")
    f.write(string)
    f.close()
    try:
        subprocess.call([minisatPath, "minisat.txt", "minisatoutput.txt"])
    except OSError:
        print("Please recheck the path.")    
    sudoku.readMinisatOutput("minisatoutput.txt")
    stopTime=time.time()
    timeTaken=stopTime-initialTime;
    print  str("%.4f" %timeTaken)+"\t\t\t"
    totalTime=totalTime+timeTaken

print "Total time taken"+" "+str("%.4f" % totalTime)
counter2=0
#printing solution
f2=open(filename,"w")
for sudoku in newSudoku:   
    f2.write(str(sudoku))
    counter2=counter2+1
    if counter2!=counter:
        f2.write("\n")