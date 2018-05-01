import ply.yacc as yacc
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append(".")

from DataStructures.FunctionsDirectory import functions_Directory
from Memory.Memory import memory_Block
from DataStructures.Stack import Stack


class virtual_Machine:

    def __init__(self, quadQueue, memory, functionsDirectory):
        self.quadQueue = quadQueue
        self.memory = memory
        self.functionsDirectory = functionsDirectory
        print('Bloque de Memoria: ')
        print memory.memoryBlock
        #Imprime los quadruplos
        quadQueue.printQueue()
        print '\n'
        self.executeQuadruples()


    def isInt(self, value):
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    def isFloat(self, value):
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def executeQuadruples(self):

        #Apuntador a los quadruplos
        instructionPointer = 0
        valuesStack = Stack()
        functionsStack = Stack()
        savedIPs = Stack()

        #While que recorre todos los quadruplos
        while instructionPointer < self.quadQueue.size():

            quadLocation = self.quadQueue.size() - instructionPointer - 1
            quad = self.quadQueue.get(quadLocation)
            leftOperand = quad.left_operand
            rightOperand = quad.right_operand
            resultAddress = quad.result
            #print('Este es el operator ' + quad.operator)

            if isinstance(quad.left_operand, list):
                if len(quad.left_operand) == 1:
                    leftOperand = self.memory.getValueByAddress(quad.left_operand[0])
                    #print('Este es el left operand ' + str(leftOperand))
            if isinstance(quad.right_operand, list):
                if len(quad.right_operand) == 1:
                    rightOperand = self.memory.getValueByAddress(quad.right_operand[0])
            if isinstance(quad.result, list):
                if len(quad.result) == 1:
                    resultAddress = self.memory.getValueByAddress(quad.result[0])

            if quad.operator == '+':
                
                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue + rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '-':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue - rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '*':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue * rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '/':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue / rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '!':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                result = not(leftOperandValue)
                self.memory.modifyValueByAddress(resultAddress, result)

            elif quad.operator == '=':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                self.memory.modifyValueByAddress(resultAddress, leftOperandValue)

            elif quad.operator == '<':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue < rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '>':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue > rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '<=':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue <= rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '>=':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue >= rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '==':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue == rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '||':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue or rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '&&':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue and rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '!=':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                resultValue = leftOperandValue != rightOperandValue
                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == 'WRITE':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                print ('Print: ', leftOperandValue)

            elif quad.operator == 'READ':

                input = raw_input()
                if self.isInt(input):
                    if leftOperand == 'int':
                        self.memory.modifyValueByAddress(resultAddress, int(input))
                    else:
                        print('Error: Input type mismatch, expecting ' + str(leftOperand))
                        sys.exit()
                elif self.isFloat(input):
                    if leftOperand == 'float':
                        self.memory.modifyValueByAddress(resultAddress, float(input))
                    else:
                        print('Error: Input type mismatch, expecting ' + str(leftOperand))
                        sys.exit()
                elif input == 'true':
                    if leftOperand == 'bool':
                        self.memory.modifyValueByAddress(resultAddress, True)
                    else:
                        print('Error: Input type mismatch, expecting ' + str(leftOperand))
                        sys.exit()
                elif input == 'false':
                    if leftOperand == 'bool':
                        self.memory.modifyValueByAddress(resultAddress, False)
                    else:
                        print('Error: Input type mismatch, expecting ' + str(leftOperand))
                        sys.exit()
                else:
                    if leftOperand == 'string':
                        self.memory.modifyValueByAddress(resultAddress, str(input))
                    else:
                        print('Error: Input type mismatch, expecting ' + str(leftOperand))
                        sys.exit()


            elif quad.operator == 'goto':

                instructionPointer = resultAddress - 2

            elif quad.operator == 'gotof':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                if leftOperandValue == False:
                    instructionPointer = resultAddress - 2

            elif quad.operator == 'gosub':

                savedIPs.push(quad.quad_number)
                instructionPointer = resultAddress - 2

            elif quad.operator == 'RETURN':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                self.memory.modifyValueByAddress(rightOperand, leftOperandValue)
                instructionPointer = resultAddress - 2

            elif quad.operator == 'ENDPROC':

                if not functionsStack.isEmpty():
                    functionName = functionsStack.pop()
                    function = self.functionsDirectory.functions[functionName]
                    varTable = function['variables']
                    variables = varTable.variables

                    for variable in variables:
                        variableInfo = variables[variable]
                        variableVirtualAddress = variableInfo[1]
                        self.memory.modifyValueByAddress(variableVirtualAddress, valuesStack.pop())

                instructionPointer = savedIPs.pop() - 1

            elif quad.operator == 'ERA':

                function = self.functionsDirectory.functions[leftOperand]
                varTable = function['variables']
                variables = varTable.variables

                for variable in variables:
                    variableInfo = variables[variable]
                    variableVirtualAddress = variableInfo[1]
                    variableValue = self.memory.getValueByAddress(variableVirtualAddress)
                    valuesStack.push(variableValue)

                functionsStack.push(leftOperand)

            elif quad.operator == 'VER':

                index = self.memory.getValueByAddress(leftOperand)

                if not (index >= rightOperand and index <= resultAddress):
                    print("ERROR: Array index is out of bounds.")
                    sys.exit()

            elif quad.operator == 'PARAM':

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                self.memory.modifyValueByAddress(resultAddress, leftOperandValue)

            elif quad.operator == 'DRAWBARCHART':
 
                plt.figure()   
                plt.title("Bar Chart")
                plt.xlabel("X")
                plt.ylabel("Y")
                plt.bar(self.memory.getValueByAddress(leftOperand[0]), self.memory.getValueByAddress(leftOperand[1]), align='center')
                plt.bar(self.memory.getValueByAddress(leftOperand[2]), self.memory.getValueByAddress(leftOperand[3]), align='center')
                plt.bar(self.memory.getValueByAddress(leftOperand[4]), self.memory.getValueByAddress(leftOperand[5]), align='center')
                plt.bar(self.memory.getValueByAddress(leftOperand[6]), self.memory.getValueByAddress(leftOperand[7]), align='center')
                plt.plot()
               

            elif quad.operator == 'DRAWDOTCHART':

                plt.figure()    
                plt.title("Dot Chart")
                plt.xlabel("X")
                plt.ylabel("Y")
                plt.plot([self.memory.getValueByAddress(leftOperand[0]),self.memory.getValueByAddress(leftOperand[2]),self.memory.getValueByAddress(leftOperand[4]),self.memory.getValueByAddress(leftOperand[6])],[self.memory.getValueByAddress(leftOperand[1]),self.memory.getValueByAddress(leftOperand[3]),self.memory.getValueByAddress(leftOperand[5]),self.memory.getValueByAddress(leftOperand[7])],'ro')
                plt.axis([0, 6, 0, 20])
                

            elif quad.operator == 'DRAWLINECHART':

                plt.figure()   
                plt.title("Line Chart")
                plt.xlabel("X")
                plt.ylabel("Y")
                plt.plot([self.memory.getValueByAddress(leftOperand[0]),self.memory.getValueByAddress(leftOperand[1]),self.memory.getValueByAddress(leftOperand[2]),self.memory.getValueByAddress(leftOperand[3]),self.memory.getValueByAddress(leftOperand[4]),self.memory.getValueByAddress(leftOperand[5]),self.memory.getValueByAddress(leftOperand[6]),self.memory.getValueByAddress(leftOperand[7])])
                plt.axis([0, 6, 0, 20])

            elif quad.operator == 'DRAWHISTCHART':

                plt.figure() 
                # Crea semilla random
                np.random.seed(19680801)
                mu, sigma = self.memory.getValueByAddress(leftOperand[0]), self.memory.getValueByAddress(leftOperand[1])
                x = mu + sigma * np.random.randn(10000)
                # Datos para histograma
                n, bins, patches = plt.hist(x, 50, normed=1, facecolor='g', alpha=0.75)
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.title('Histogram Chart')
                plt.axis([40, 160, 0, 0.03])
                plt.grid(True)

            elif quad.operator == 'DRAWPOLYCHART':

                plt.figure()   
                plt.title("Polygons Chart")
                # evenly sampled time at 200ms intervals
                t = np.arange(self.memory.getValueByAddress(leftOperand[0]),self.memory.getValueByAddress(leftOperand[1]),self.memory.getValueByAddress(leftOperand[2]))
                # red dashes, blue squares and green triangles
                plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
                
            elif quad.operator == 'END':
                print("Quadruplo END")
                plt.show()
                sys.exit()

            instructionPointer += 1
