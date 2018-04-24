import ply.yacc as yacc
import sys

sys.path.append(".")

from DataStructures.FunctionsDirectory import functions_Directory
from Memory.Memory import memory_Block
from DataStructures.Stack import Stack


class virtual_Machine:

    def __init__(self, quadQueue, memory, functionsDirectory):
        self.memory = memory
        self.functionsDirectory = functionsDirectory
        self.quadQueue = quadQueue

        print memory.memoryBlock
        quadQueue.printQueue()
        print '\n'
        # Execute quadruples operations
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

    # Execute operations from quadruples
    def executeQuadruples(self):

        instructionPointer = 0

        valuesStack = Stack()
        functionsStack = Stack()
        savedIPs = Stack()
        speed = 8

        while instructionPointer < self.quadQueue.size():

            quadLocation = self.quadQueue.size() - instructionPointer - 1
            quad = self.quadQueue.get(quadLocation)

            leftOperand = quad.left_operand
            rightOperand = quad.right_operand
            resultAddress = quad.result
            print('Este es el operator ' + quad.operator)

            if isinstance(quad.left_operand, list):
                if len(quad.left_operand) == 1:
                    leftOperand = self.memory.getValueByAddress(quad.left_operand[0])
            if isinstance(quad.right_operand, list):
                if len(quad.right_operand) == 1:
                    rightOperand = self.memory.getValueByAddress(quad.right_operand[0])
            if isinstance(quad.result, list):
                if len(quad.result) == 1:
                    resultAddress = self.memory.getValueByAddress(quad.result[0])

            if quad.operator == '+':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                 #              quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                #print ('Left Operand Value', leftOperandValue)
                #print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue + rightOperandValue
                #print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '-':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                #print ('Left Operand Value', leftOperandValue)
                #print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue - rightOperandValue
                #print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '*':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                #print ('Left Operand Value', leftOperandValue)
                #print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue * rightOperandValue
                #print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '/':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #     quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                #print ('Left Operand Value', leftOperandValue)
                #print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue / rightOperandValue
                #print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '!':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                #print ('Left Operand Value', leftOperandValue)

                result = not(leftOperandValue)
                #print ('Result Value', result, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, result)

            elif quad.operator == '=':
                # print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                #print ('Left Operand Value', leftOperandValue)

                #print ('Result Value', leftOperandValue, ' on address', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, leftOperandValue)

            elif quad.operator == '<':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                #print ('Left Operand Value', leftOperandValue)
                #print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue < rightOperandValue
                #print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '>':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                #print ('Left Operand Value', leftOperandValue)
                #print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue > rightOperandValue
                #print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '<=':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                #print ('Left Operand Value', leftOperandValue)
                # print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue <= rightOperandValue
                # print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '>=':
                # print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                # print ('Left Operand Value', leftOperandValue)
                # print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue >= rightOperandValue
                # print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '==':
                # print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)
                #print ('Left Operand Value', leftOperandValue)
                #print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue == rightOperandValue
                #print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '||':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #     quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)

                #print ('Left Operand Value', leftOperandValue)
                #print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue or rightOperandValue
                #print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '&&':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)

                #print ('Left Operand Value', leftOperandValue)
                #print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue and rightOperandValue
                #print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == '!=':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                rightOperandValue = self.memory.getValueByAddress(rightOperand)

                #print ('Left Operand Value', leftOperandValue)
                #print ('Right Operand Value', rightOperandValue)

                resultValue = leftOperandValue != rightOperandValue
                #print ('Result Value', resultValue, ' on address ', resultAddress)

                self.memory.modifyValueByAddress(resultAddress, resultValue)

            elif quad.operator == 'WRITE':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)

                print ('Left Operand Value', leftOperandValue)

                print leftOperandValue

            elif quad.operator == 'READ':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #     quad.result)

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
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #     quad.result)

                instructionPointer = resultAddress - 2

            elif quad.operator == 'gotof':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                if leftOperandValue == False:
                    instructionPointer = resultAddress - 2

            elif quad.operator == 'gosub':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #     quad.result)

                savedIPs.push(quad.quad_number)
                instructionPointer = resultAddress - 2

            elif quad.operator == 'RETURN':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)

                #print ('leftoperand',self.memory.getValueByAddress(resultAddress))

                self.memory.modifyValueByAddress(rightOperand, leftOperandValue)
                instructionPointer = resultAddress - 2

                #print ('resultAddress',self.memory.getValueByAddress(resultAddress))

            elif quad.operator == 'ENDPROC':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                # quad.result)

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
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #quad.result)

                function = self.functionsDirectory.functions[leftOperand]
                varTable = function['variables']
                variables = varTable.variables

                for variable in variables:
                    variableInfo = variables[variable]

                    variableVirtualAddress = variableInfo[1]
                    #print('return variableVirtualAddress ', variableVirtualAddress)
                    variableValue = self.memory.getValueByAddress(variableVirtualAddress)
                    #print('return variableValue ', variableValue)
                    valuesStack.push(variableValue)
                    #print('valuesStack        ', valuesStack.items)

                functionsStack.push(leftOperand)

            elif quad.operator == 'VER':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                index = self.memory.getValueByAddress(leftOperand)

                #print ('index', index)
                #print ('inf lim', rightOperand)
                #print ('sup lim', resultAddress)

                if not (index >= rightOperand and index <= resultAddress):
                    print("ERROR: Array index is out of bounds.")
                    sys.exit()

            elif quad.operator == 'PARAM':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                #      quad.result)

                leftOperandValue = self.memory.getValueByAddress(leftOperand)
                #print ('Left Operand Value', leftOperandValue)

                self.memory.modifyValueByAddress(resultAddress, leftOperandValue)
                #self.memory.modifyValueByAddress(resultAddress, result)

            elif quad.operator == 'END':
                #print("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,quad.result)
                print("Quadruplo END")
                sys.exit()

            instructionPointer += 1
