import sys
import time
import resource

size=9
squareSize=3
method="MAC"

class Variable:

    def __init__(self,value,index):
        self.value=value
        self.index=index
        self.domain=[]
        self.previousDomain=[]
        if value in range(1,size+1):
            self.domain=list([value])
        else:
            self.domain=list(range(1,size+1))    

        self.domainStack=[]

    def setValue(self,value):
        if not value in self.domain:
            return
        self.previousDomain=self.domain
        self.domain=list([value]) 
        self.value=value


    def removeValue(self):    
        self.value=0
        self.domain=self.previousDomain
        self.previousDomain=[]
   
class Sudoku:

    def __init__(self, board):
    
        self.noOfBacktracks=0
        #constraints associated with sudoku if 0 no constraint if 1 associated constraints
        self.constraintMatrix=[[0 for i in range(size*size)] for j in range(size*size)]
        #index to variable dictionary for getting variable at an index at any time
        self.dict={}        
        index=0
        
        for i in range(size):
            for j in range(size):
                temp=board[index]
                if temp=='.':
                    currVariable=Variable(0,index)
                else:
                    currVariable=Variable(int(temp),index)
      
                self.dict[index]=currVariable
                index=index+1       
         
        #setting up the constraint matrix    
        for i in range(size):
            for j in range(size):
                x=i*size+j
                #for square cosntraints
                squareEndRow = int(i/squareSize+1)*squareSize-1
                squareEndColumn = int(j/squareSize+1)*squareSize-1
                squareStartColumn = squareEndColumn-squareSize+1

                #constraint along rows
                for k in range(i+1,size):
                    y=k*size+j
                    self.constraintMatrix[x][y]=1
                    self.constraintMatrix[y][x]=1

                #constraint along columns
                for k in range(j+1,size):
                    y=i*size+k
                    self.constraintMatrix[x][y]=1
                    self.constraintMatrix[y][x]=1

                #constraint along sub squares
                for k in range(i+1,squareEndRow+1):
                    for kk in range(squareStartColumn,squareEndColumn+1):
                        y=k*size+kk
                        self.constraintMatrix[x][y]=1
                        self.constraintMatrix[y][x]=1
         
        #reducing the domains of the variable
        for i in range(len(self.dict)):
            if(self.reduceDomains(self.dict[i])):
                print "Inconsistent initial sudoku"

    # Changes the domain of first variable in given constraint to make it arc consistent.
    def arcConsistency(self,constraint):
        
        flag=0
        reducedDomain=[]        
        for i in range(len(constraint[1].domain)):
            value = constraint[1].domain[i]
            flag=0
            for otherValue in constraint[0].domain:
                if value != otherValue:
                    flag=1
                    break
            if flag==0:
                reducedDomain.append(value)

        for val in reducedDomain:
            constraint[1].domain.remove(val)   

        #if domain needs to be reduce then true
        if len(reducedDomain)>0:
            return 1
        else: 
            return 0  

    def reduceDomains(self,currVar):
        constraints=[]  
        
        if method=="MAC":
            for i in range(len(self.dict)):
                self.dict[i].domainStack.append(list(self.dict[i].domain))

        for var in self.getConstrainedVariables(currVar.index):
            constraints.append((currVar,var))
        while(constraints):
            # to make it a queue implementing from front
            currConstraint=constraints.pop(0);
            if(self.arcConsistency(currConstraint)):

                if len(currConstraint[1].domain)==0:
                    return 1
                for var in self.getConstrainedVariables(currConstraint[1].index):
                    constraints.append((currConstraint[1], var));       
        return 0  
                  
    def checkComplete(self):

        for i in range(len(self.dict)):
            if self.dict[i].value==0:
                return 0
        return 1 
             

    def getConstrainedVariables(self,variableIndex):
        #return variables with all the constraints

        constrainedVariables=[]
        for i in range(size*size):
            if self.constraintMatrix[variableIndex][i]==1:
                constrainedVariables.append(self.dict[i])
        return constrainedVariables        

    def checkConsistency(self,selectedValue,selectedVariable):

        constrainedVariables=self.getConstrainedVariables(selectedVariable.index)
        for var in constrainedVariables:
            if var.value==selectedValue:
                return 0
        return 1

    #not for BT 
    def selectMinimumVariable(self):

        minValue=size+1
        newVar=None
        for i in range(len(self.dict)):
            var=self.dict[i]
            if var.value==0 and minValue>len(var.domain):
                newVar=var
                minValue=len(var.domain)
                if minValue==1:
                    break
        return newVar

    #not for BT and MRV in decreasing order
    def getDomainValues(self,selectedVariable):

        getAllValues=[]
        valuesList=[]
        index=0
        constrainedVariables=self.getConstrainedVariables(selectedVariable.index)
        for val in selectedVariable.domain:
            allValues=0
            flag=0
            for var in constrainedVariables:
                for i in var.domain:
                    if i!=val:
                        allValues=allValues+1
            #index=len(getAllValues)
            for i in range(len(valuesList)):      
                if allValues>=getAllValues[i]:
                    index=i
                    flag=1
            
                    break 
            
            if flag==1:
                getAllValues.insert(index,allValues)
                valuesList.insert(index,val)
            else:
                getAllValues.insert(len(getAllValues),allValues)                
                valuesList.insert(len(getAllValues),val)
            
            #getAllValues.insert(index, getAllValues)
            #valuesList.insert(index, val)
        #print "Domain list"        
        #print getAllValues
        #print "return"
        #print valuesList        
        return valuesList
    
    def solve(self):

        if self.checkComplete():
            return 1
        if method=="BT":
            for i in range(len(self.dict)):
                if self.dict[i].value==0:
                    var=self.dict[i]
                    break
        else:                
            var=self.selectMinimumVariable()
        #print ("variablechosen")+str(var.index)
            
        if method=="BT" or method=="MRV":
            #domainValues=list(var.domain)
            domainValues=var.domain
        else:
            domainValues=self.getDomainValues(var)
        
        #print ("Domain")+str(domainValues)

        for domain in domainValues:        
            if self.checkConsistency(domain,var):
                var.setValue(domain)
                if method=="MAC":
                   if (self.reduceDomains(var)==1):
                        #inconcsistent so getting back the previous values
                        for i in range(len(self.dict)):
                            self.dict[i].domain=self.dict[i].domainStack.pop()
                        var.removeValue() 

                        continue;

                output=self.solve()

                if output!=None:
                    return output
                if method=="MAC":   
                    for i in range(len(self.dict)):
                        self.dict[i].domain=self.dict[i].domainStack.pop()                    
                var.removeValue()                

        self.noOfBacktracks=self.noOfBacktracks+1
        return None            


    def __str__(self):
 
        sudokuString=""
        for i in range(len(self.dict)):
                  sudokuString= sudokuString+str(self.dict[i].value)
        return sudokuString   

if len(sys.argv)!=2:
    print "Invalid arguments"
    sys.exit(0)

totalTime=0
#reading of file
counter=0
counter2=0    
input_file=sys.argv[1]
f1=open(input_file,"r")
line=f1.readline()
sudokuLine=line.split("\r")
#print sudokuLine
newSudoku=[]

for sudoku in sudokuLine:
    counter=counter+1
    if len(sudoku)==0:
        continue
    newSudoku.append(Sudoku(sudoku))
    #print "New Sudoku"
    if counter==1:
        break
f1.close()    

print "Time taken"+"\t\t"+"No of backtracks"+"\t\t\t"+"Resources"

#solving sudoku        
for sudoku in newSudoku:
    #print(sudoku)
    initialTime=time.time()
    sudoku.solve()
    stopTime=time.time()
    timeTaken=stopTime-initialTime;
    totalTime=totalTime+timeTaken
    print str("%.4f" %timeTaken)+"\t\t\t"+str(sudoku.noOfBacktracks)+"\t\t\t\t\t\t"+str(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024) 
    #print "New Sudoku"
print "Total time taken"+" "+str("%.4f" % totalTime)
filename="output_"+method+".txt"

#printing solution
f2=open(filename,"w")
for sudoku in newSudoku: 
    counter2=counter2+1  
    f2.write(str(sudoku))
    if counter2!=counter:
        f2.write("\n") 