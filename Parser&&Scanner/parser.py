import ply.yacc as yacc
import sys

sys.path.append(".")

from scanner import tokens
from DataStructures.FunctionsDirectory import functions_Directory
from DataStructures.Stack import Stack
from DataStructures.VariablesTable import vars_Table
from DataStructures.Quadruple import Quadruple
from DataStructures.Queue import Queue
#from SemanticCube.SemanticCube import semantic_Cube
#from Memory.Memory import memory_Block
#from VirtualMachine.VirtualMachine import virtual_Machine
#-----------------------------------------------------------------

# Directories
functionsDirectory = functions_Directory()
#semanticCube = semantic_Cube()
funcReturn = {}

# Memory
#memory = memory_Block()

# Scope management variables
currentScope = ""
globalScope = ""
calledFunction = ""

# Counter variables
quadCounter = 1
argumCounter = 0

# Stacks
operatorsStack = Stack()
operandsStack = Stack()
typesStack = Stack()
jumpsStack = Stack()
returnStack = Stack()
predefParamStack = Stack()

# Queues
quadQueue = Queue()
argumentQueue = Queue()
argumTypeQueue = Queue()

# Dimension management variables
dimenVar = ""
dimenSupLim = 0

# Global variables
color = ""
endprocnumber = 0
returns = 0

# Virtual Machine
vm = None

# Default Values
defaultInt = 0
defaultFloat = 0.0
defaultBool = False
defaultString = 'Null'

# Validation variables
functionWithReturn = False


# Grammar rules
def p_PROGRAM(p):
    '''
    program : PROGRAM ID add_global_function SEMICOLON goto_main vars function main endProgram
    '''

def p_end(p):
    '''
    endProgram :
    '''
    endProgram(p)

def p_add_global_function(p):
    '''
    add_global_function :
    '''
    # Call function to add global function to FunctionsDirectory
    storeGlobalFunc(p)

def p_MAIN(p):
    '''
    main : INTTYPE MAIN change_to_global LPAREN RPAREN add_jump_to_main block
    '''

def p_change_to_global(p):
    '''
    change_to_global :
    '''
    changeToGlobal(p)

def p_goto_main(p):
    '''
    goto_main :
    '''
    # Create Quadruple to jump to main
    gotoMain(p)

def p_add_jump_to_main(p):
    '''
    add_jump_to_main :
    '''
    # Fill the jump quadruple of the first quadruple
    addJumpToMain(p)

def p_BLOCK(p):
    '''
    block : LBRACE blockprima RBRACE
    '''

def p_BLOCKPRIMA(p):
    '''
    blockprima : statute blockprima
               | empty
    '''

def p_STATUTE(p):
    '''
    statute : assignment
            | condition
            | write
            | read
            | cycle
            | functioncall SEMICOLON
            | return
    '''

def p_CONDITION(p):
    '''
    condition : IF LPAREN sexpression RPAREN do_condition_operation block else
    '''
    # Call function to fill the jumps
    doEndConditionOperation(p)

def p_do_condition_operation(p):
    '''
    do_condition_operation :
    '''
    # Do the condition operations and quadruples
    doConditionOperation(p)

def p_ELSE(p):
    '''
    else : ELSE do_else_operation block
         | empty
    '''

def p_do_else_operation(p):
    '''
    do_else_operation :
    '''
    # Do the else operations and quadruples
    doElseOperation(p)

def p_VARS(p):
    '''
    vars : VAR type ID array_declaration store_variable SEMICOLON vars
         | empty
    '''

def p_store_variable(p):
    '''
    store_variable :
    '''
    # Store Variable in VarsTable of the current scope
    storeVariable(p)

def p_ARRAY_DECLARATION(p):
    '''
    array_declaration : LBRACKET dimen_variable sexpression calculate_dimen RBRACKET
                      | empty
    '''

def p_dimen_variable(p):
    '''
    dimen_variable :
    '''
    dimenVariable(p)

def p_calulate_dimen(p):
    '''
    calculate_dimen :
    '''
    calculateDimen(p)

def p_TYPE(p):
    '''
    type : INTTYPE
         | FLOATTYPE
         | STRINGTYPE
         | BOOLTYPE
    '''
    p[0] = p[1]


def p_ASSIGNMENT(p):
    '''
    assignment : ID push_id_operand array ASSIGN push_operator sexpression SEMICOLON
    '''
    # Do the assignment operations and quadruples
    doAssignOperation(p)

def p_push_id_operand(p):
    '''
    push_id_operand :
    '''
    # Push operand to stack
    pushOperand(p)

def p_push_operator(p):
    '''
    push_operator :
    '''
    # Push operator to stack
    pushOperator(p)

def p_SEXPRESSION(p):
    '''
    sexpression : negation expression do_not_operation
    '''

def p_EXPRESSION_NEGATION(p):
    '''
    negation : NOT push_operator
             | empty
    '''

def p_do_not_operation(p):
    '''
    do_not_operation :
    '''
    # Do the not operations and quadruples for expressions
    doNotOperation(p)

def p_EXPRESSION(p):
    '''
    expression : expression relationaloperators push_operator exp do_relational_operation
               | exp
    '''

def p_RELATIONAL_OPERATORS(p):
    '''
    relationaloperators : LESS
                        | GREATER
                        | EQUAL
                        | NOTEQUAL
                        | LESSOREQUAL
                        | GREATEROREQUAL
                        | AND
                        | OR
    '''
    p[0] = p[1]

def p_do_relational_operation(p):
    '''
    do_relational_operation :
    '''
    # Do operations and quadruples for the relational operations
    operator = operatorsStack.top()
    if operator == '<' or operator == '>' or operator == '==' or operator == '!=' or operator == '<=' or \
                    operator == '>=' or operator == '||' or operator == '&&':
        doOperations(p)

def p_EXP(p):
    '''
    exp : exp mathoperators1 push_operator term do_math_operation1
        | term
    '''

def p_MATH_OPERATORS1(p):
    '''
    mathoperators1 : PLUS
                   | MINUS
    '''
    p[0] = p[1]

def p_do_math_operation1(p):
    '''
    do_math_operation1 :
    '''
    # Do operations and quadruples for the plus and minus operations
    operator = operatorsStack.top()
    if operator == '+' or operator == '-':
        doOperations(p)

def p_TERM(p):
    '''
    term : term mathoperators2 push_operator factor do_math_operation2
         | factor
    '''

def p_MATH_OPERATORS2(p):
    '''
    mathoperators2 : TIMES
                   | DIVIDE
    '''
    p[0] = p[1]

def p_do_math_operation2(p):
    '''
    do_math_operation2 :
    '''
    # Do operations and quadruples for times and divide operations
    operator = operatorsStack.top()
    if operator == '*' or operator == '/':
        doOperations(p)

def p_FACTOR(p):
    '''
    factor : LPAREN push_false_bottom sexpression RPAREN pop_false_bottom
           | varConst
    '''

def p_push_false_bottom(p):
    '''
    push_false_bottom :
    '''
    operatorsStack.push('(')

def p_pop_false_bottom(p):
    '''
    pop_false_bottom :
    '''
    operatorsStack.pop()

def p_CONSTANT(p):
    '''
    varConst : ID push_id_operand array
             | FLOAT push_float_operand
             | INT push_int_operand
             | bool push_bool_operand
             | STRING push_string_operand
             | functioncall
    '''

def p_ARRAY(p):
    '''
    array : LBRACKET access_dimen_var sexpression validate_index RBRACKET
          | empty
    '''

def p_validate_index(p):
    '''
    validate_index :
    '''
    validateIndex(p)

def p_access_dimen_var(p):
    '''
    access_dimen_var :
    '''
    accessDimenVariable(p)

def p_BOOL(p):
    '''
    bool : TRUE
         | FALSE
    '''
    p[0] = p[1]

def p_push_float_operand(p):
    '''
    push_float_operand :
    '''
    # Push float operand
    pushFloatOperand(p)

def p_push_int_operand(p):
    '''
    push_int_operand :
    '''
    # Push int operand
    pushIntOperand(p)

def p_push_bool_operand(p):
    '''
    push_bool_operand :
    '''
    # Push boolean operand
    pushBoolOperand(p)

def p_push_string_operand(p):
    '''
    push_string_operand :
    '''
    # Push string operand
    pushStringOperand(p)

def p_FUNCTIONCALL(p):
    '''
    functioncall : ID check_function_existance LPAREN generate_era funcargum RPAREN validate_arguments
    '''

def p_check_existance_function(p):
    '''
    check_function_existance :
    '''
    checkFunctionExistance(p)

def p_generate_era(p):
    '''
    generate_era :
    '''
    generateEra(p)

def p_validate_arguments(p):
    '''
    validate_arguments :
    '''
    validateArguments(p)

def p_FUNCARGUM(p):
    '''
    funcargum : sexpression store_argument funcargumprima
              | empty
    '''

def p_FUNCARGUM_PRIMA(p):
    '''
    funcargumprima : COMMA sexpression store_argument funcargumprima
                   | empty
    '''

def p_store_argument(p):
    '''
    store_argument :
    '''
    storeArgument(p)

def p_FUNCTION(p):
    '''
    function : FUNCTION functiontype ID store_function LPAREN parameter RPAREN vars add_func_quad_start block end_process function
             | empty
    '''

def p_FUNCTION_TYPE(p):
    '''
    functiontype : VOID
                 | type
    '''
    p[0] = p[1]

def p_add_func_quad_start(p):
    '''
    add_func_quad_start :
    '''
    addFunctionQuadStart(p)

def p_store_function(p):
    '''
    store_function :
    '''
    storeFunction(p)

def p_end_process(p):
    '''
    end_process :
    '''
    endProcess(p)

def p_RETURN(p):
    '''
    return : RETURN sexpression SEMICOLON
    '''
    returnOperation(p)

def p_PARAMETER(p):
    '''
    parameter : type ID store_parameter array parameterprima
              | empty
    '''

def p_PARAMETERPRIMA(p):
    '''
    parameterprima : COMMA type ID store_parameter parameterprima
                   | empty
    '''

def p_store_parameter(p):
    '''
    store_parameter :
    '''
    storeParameter(p)

def p_WRITE(p):
    '''
    write : PRINT LPAREN sexpression RPAREN SEMICOLON
    '''
    # Do Write quadruples
    doWriteOperation(p)

def p_READ(p):
    '''
    read : ID push_id_operand array ASSIGN push_operator INPUT LPAREN RPAREN SEMICOLON
    '''
    # Do Read quadruples
    doReadOperation(p)

def p_CYCLE(p):
    '''
    cycle : WHILE push_cycle_jump LPAREN sexpression RPAREN do_while_operation block
    '''
    # Fill Cycle quadruples jumps
    doEndCycleOperations(p)

def p_push_cycle_jump(p):
    '''
    push_cycle_jump :
    '''
    # Push jump reference to jumps stack
    pushCycleJump(p)

def p_do_while_operation(p):
    '''
    do_while_operation :
    '''
    # Do Cycle quadruples
    doCycleOperations(p)


def p_EMPTY(p):
    '''
    empty :
    '''
    pass

# NoYacc FUNCTIONS..................
def storeGlobalFunc(p):
    global currentScope
    global globalScope

    # Save the current function name
    globalScope = p[-1]
    currentScope = p[-1]

    # Create function directory variable
    functionsDirectory.insertFunction(currentScope, 'void', None)
    print("storeGlobalFunction", currentScope, functionsDirectory.getFunctionType(currentScope))

def changeToGlobal(p):
    global currentScope
    global globalScope

    # Set the currentScope to the globalScope
    currentScope = globalScope
    # Add the quad number where main function starts
    functionsDirectory.setStartQuadNumber(globalScope, quadCounter)
    print("changeToGlobal", currentScope, functionsDirectory.getStartQuadNumber(globalScope))

def addJumpToMain(p):
    global quadCounter

    # Get number of pending quad to fill
    end = jumpsStack.pop()
    # Get reverse position of Queue
    quadNumber = (quadQueue.size()) - end
    # Get quad to fill
    quad = quadQueue.get(quadNumber)
    # Full quads jump
    quad.addJump(quadCounter)

    print("addJumpToMain", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand, quad.result),
          "line: " + str(p.lexer.lineno))

def gotoMain(p):
    global quadCounter

    # Push number of quad to be jumpfilled
    jumpsStack.push(quadCounter)
    # Create gotomain quadruple
    quad = Quadruple(quadCounter, 'goto', None, None, None)
    # Increment quadCounter
    quadCounter += 1
    # Add quad to the QuadQueue
    quadQueue.enqueue(quad)

    print("gotoMain",
          ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand, quad.result),
          "line: " + str(p.lexer.lineno))

def storeVariable(p):
    global currentScope
    global dimenVar
    global dimenSupLim

    # Get varable name and type
    varId = p[-2]
    varType = p[-3]

    # Set default value depending on the variable type
    if varType == 'int':
        value = defaultInt
    elif varType == 'float':
        value = defaultFloat
    elif varType == 'bool':
        value = defaultBool
    elif varType == 'string':
        value = defaultString

    # Check if the current scope is the main program
    if currentScope == globalScope:
        # Check if the variable is dimensional or not
        if dimenVar != '':
            # Store the dimensional variable into memory
            virtualAddress = memory.storeDimensionVarToMemory(value, varType, dimenSupLim)
        else:
            # Store the variable into memory
            virtualAddress = memory.storeVariableToMemory(value, varType)
    else:
        # Check if the variable is dimensional or not
        if dimenVar != '':
            # Check if the temporal is dimensional or not
            virtualAddress = memory.storeDimensionTempToMemory(value, varType, dimenSupLim)
        else:
            # Store the dimensional temporal into memory
            virtualAddress = memory.storeTempToMemory(value, varType)

    # Check if the virtual address
    if virtualAddress == None:
        errorCannotAllocate(p, varId)
    else:
        # varId needs to be changed to virtual address
        if not functionsDirectory.addFunctionVariable(currentScope, varId, varType, virtualAddress):
            # Execute Variable Already Declared Error
            errorVariableAlreadyDeclared(p, varId)
        else:
            # Push the virtual address of the variable to operandsStack
            operandsStack.push(virtualAddress)
            # Push the type of the variable to operandsStack
            typesStack.push(varType)
            # Check if the variable is dimensional
            if dimenVar != '':
                # Add dimension to the variable on the VarsTable
                functionsDirectory.addDimensionToVariable(currentScope, varId, dimenSupLim)
                # Restore dimensional global variables
                dimenSupLim = 0
                dimenVar = ''

            print("storeVariable", currentScope, functionsDirectory.getFunctionVariable(currentScope, varId),
                      "line: " + str(p.lexer.lineno))

def pushOperand(p):
    global currentScope

    # Get variable name
    varId = p[-1]
    # Get Variable from the current scope varsTable
    funcVar = functionsDirectory.getFunctionVariable(currentScope, varId)

    # Check if the variables exists in the current scope
    if funcVar is None:
        funcVar = functionsDirectory.getFunctionVariable(globalScope, varId)
        # Check of the variable exists in the global scope
        if funcVar is None:
            # Execute Variable Not Declared Error
            errorVariableNotDeclared(p, varId)
        else:
            # Get Variable Info
            funcVarInfo = funcVar[1]
            # Variable type
            funcVarType = funcVarInfo[0]
            # Variable name
            funcVarId = funcVarInfo[1]
            # Push variable name to operands stack
            operandsStack.push(funcVarId)
            # Push variables type to types stack
            typesStack.push(funcVarType)
    else:
        # Get Variable Info
        funcVarInfo = funcVar[1]
        # Variable type
        funcVarType = funcVarInfo[0]
        # Variable name
        funcVarId = funcVarInfo[1]
        # Push variable name to operands stack
        operandsStack.push(funcVarId)
        # Push variables type to types stack
        typesStack.push(funcVarType)

    print("pushIdOperand", operandsStack.top(), typesStack.top())

def pushOperator(p):
    # Get operator
    operator = p[-1]
    # Push operator to operators stack
    operatorsStack.push(operator)

    print('push_operator', operatorsStack.top())

def pushFloatOperand(p):
    global operandsStack
    global operatorsStack

    # Get operand
    operand = p[-1]
    # Store constant to memory and get virtual address
    virtualAddress = memory.storeConstantToMemory(operand, 'float')
    # Push operand to operands stack
    operandsStack.push(virtualAddress)
    # Push type to operands stack
    typesStack.push('float')

    print("push_float_operand", operandsStack.top(), typesStack.top())

def pushIntOperand(p):
    global operandsStack
    global operatorsStack

    # Get operand
    operand = p[-1]
    # Store constant to memory and get virtual address
    virtualAddress = memory.storeConstantToMemory(operand, 'int')
    # Push operand to operands stack
    operandsStack.push(virtualAddress)
    # Push type to operands stack
    typesStack.push('int')

    print("push_int_operand", operandsStack.top(), typesStack.top())

def pushBoolOperand(p):
    global operandsStack
    global operatorsStack

    # Get operand
    operand = p[-1]
    if operand == 'true':
        operand = True
    elif operand == 'false':
        operand = False

    # Store constant to memory and get virtual address
    virtualAddress = memory.storeConstantToMemory(operand, 'bool')
    # Push operand to operands stack
    operandsStack.push(virtualAddress)
    # Push type to operands stack
    typesStack.push('bool')

    print("push_bool_operand", operandsStack.top(), typesStack.top())

def pushStringOperand(p):
    global operandsStack
    global operatorsStack

    # Get operand
    operand = p[-1]
    # Store constant to memory and get virtual address
    virtualAddress = memory.storeConstantToMemory(operand, 'string')
    # Push operand to operands stack
    operandsStack.push(virtualAddress)
    # Push type to operands stack
    typesStack.push('string')

    print("push_string_operand", operandsStack.top(), typesStack.top())

def doReadOperation(p):
    global quadCounter

    # Pop operand from operands stack
    operand = operandsStack.pop()
    # Pop type from types stack
    type = typesStack.pop()
    # Pop operator from operators stack
    operator = operatorsStack.pop()

    # Create quadruple for Read operation
    quad = Quadruple(quadCounter, 'READ', type, None, operand)
    # Add quad to QuadQueue
    quadQueue.enqueue(quad)
    # Increment QuadCounter
    quadCounter += 1

    print("read", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand, quad.result),
          "line: " + str(p.lexer.lineno))

def doWriteOperation(p):
    global quadCounter

    # Pop operand from operands stack
    operand = operandsStack.pop()
    # Pop type from types stack
    popType = typesStack.pop()
    # Create quadruple for Write operation
    quad = Quadruple(quadCounter, 'WRITE', operand, None, None)
    # Add quad to QuadQueue
    quadQueue.enqueue(quad)
    # Increment QuadCounter
    quadCounter += 1

    print("write", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand, quad.result),
          "line: " + str(p.lexer.lineno))


def doNotOperation(p):
    global semanticCube
    global quadCounter

    # Check if the operators stack is not empty
    if not operatorsStack.isEmpty():
        # Check if the top operator is a negation '!'
        if operatorsStack.top() == '!':
            # Retrieve operand from operands stack
            operand = operandsStack.pop()
            # Retrieve type from types stack
            type = typesStack.pop()
            # Retrieve operator from operators stack
            operator = operatorsStack.pop()

            # Check if type is bool or not
            if type != 'bool':
                resultType = 'Error'
            else:
                resultType = 'bool'
                value = defaultBool

            # Check if the result type is bool or not
            if resultType != 'bool':
                # Execute type missmatch error
                errorTypeMismatch(p)
            else:
                # Store variable to memory and get virtual address
                virtualAddress = memory.storeTempToMemory(value, resultType)
                # Create quadruple for the negation operation
                quad = Quadruple(quadCounter, operator, operand, None,
                                 virtualAddress)  # Last parameter should be the VirtualAddress
                # Add quad to QuadQueue
                quadQueue.enqueue(quad)
                # Push temporal variable to operands stack
                operandsStack.push(virtualAddress)
                # Push temporal variables type to types stack
                typesStack.push(resultType)
                # Increment QuadCounter
                quadCounter += 1

                print("doNotOperation",("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                quad.result), str(p.lexer.lineno))

def doConditionOperation(p):
    global quadCounter

    # Get the type of the evaluated expression
    expressionType = typesStack.pop()
    # Get the result of the expression
    expressionResult = operandsStack.pop()

    # Check if expressions type is boolean or not
    if expressionType != 'bool':
        # Execute type missmatch error
        errorTypeMismatch(p)
    else:
        # Create quadruple to jump if condition is false
        quad = Quadruple(quadCounter, 'gotof', expressionResult, None, None)
        # Add quadruple to QuadQueue
        quadQueue.enqueue(quad)
        # Push number of quad to be jumpfilled
        jumpsStack.push(quadCounter - 1)
        # Increment QuadCounter
        quadCounter += 1

        print("doConditionOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                                    quad.right_operand, quad.result), "line: " +str(p.lexer.lineno))

def doEndConditionOperation(p):
    global quadCounter

    # Get number of pending quad to fill
    end = jumpsStack.pop()
    # Get reverse position of Queue
    quadNumber = (quadQueue.size() - 1) - end
    # Get quad to fill
    quad = quadQueue.get(quadNumber)
    # Full quads jump
    quad.addJump(quadCounter)

    print("doEndConditionOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                                   quad.right_operand, quad.result), "line: " + str(p.lexer.lineno))

def doElseOperation(p):
    global quadCounter

    # Create quadruple to jump if else
    quad = Quadruple(quadCounter, 'goto', None, None, None)
    # Add quad to QuadQueue
    quadQueue.enqueue(quad)
    # Get number of pending quad to fill
    false = jumpsStack.pop()
    # Get reverse position of Queue
    quadNumber = (quadQueue.size() - 1) - false
    # Push number of quad to be jumpfilled
    jumpsStack.push(quadCounter - 1)
    # Increment QuadCounter
    quadCounter += 1
    # Add quad to QuadQueue
    quad = quadQueue.get(quadNumber)
    # Full quads jump
    quad.addJump(quadCounter)

    print("doElseOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                                quad.right_operand, quad.result), "line: " +str(p.lexer.lineno))

def doAssignOperation(p):
    global semanticCube
    global quadCounter

    # Retrieve right operand of the assignment
    rightOperand = operandsStack.pop()
    # Retrieve right type of the assignment
    rightType = typesStack.pop()
    # Retrieve left operand of the assignment
    leftOperand = operandsStack.pop()
    # Retrieve right type of the assignment
    leftType = typesStack.pop()
    # Retrieve operator of the assignment
    operator = operatorsStack.pop()

    if rightType == 'void':
        errorNotReturnFunction(p)
    else:
        # Do the semantic evaluation of the assignment
        resultType = semanticCube.getType(leftType, rightType, operator)

        # Check if the result type is Error or not
        if resultType == 'Error':
            # Execute type missmatch error
            errorTypeMismatch(p)
        else:
            # Create cuadruple for assignment
            quad = Quadruple(quadCounter, operator, rightOperand, None, leftOperand)
            # Add quad to QuadQueue
            quadQueue.enqueue(quad)
            # Increment QuadCounter
            quadCounter += 1

            print("doAssignOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                  quad.right_operand, quad.result), "line: " +str(p.lexer.lineno))

def doOperations(p):
    global semanticCube
    global quadCounter

    # Retrieve right operand of the operation
    rightOperand = operandsStack.pop()
    # Retrieve right type of the operation
    rightType = typesStack.pop()
    # Retrieve left operand of the operation
    leftOperand = operandsStack.pop()
    # Retrieve right type of the operation
    leftType = typesStack.pop()
    # Retrieve operator of the operation
    operator = operatorsStack.pop()

    # Do the semantic evaluation of the operation
    resultType = semanticCube.getType(leftType, rightType, operator)

    # Set default value depending on the variable type
    if resultType == 'int':
        value = defaultInt
    elif resultType == 'float':
        value = defaultFloat
    elif resultType == 'bool':
        value = defaultBool
    elif resultType == 'string':
        value = defaultString

    # Check if the result type is Error or not
    if resultType == 'Error':
        # Execute type missmatch error
        errorTypeMismatch(p)
    else:
        # Store variable into memory
        virtualAddress = memory.storeTempToMemory(value, resultType)
        # Create cuadruple for assignment
        quad = Quadruple(quadCounter, operator, leftOperand, rightOperand, virtualAddress)
        # Add quad to QuadQueue
        quadQueue.enqueue(quad)
        # Push temporals virtual address to operands stack
        operandsStack.push(virtualAddress)
        # Push temporal variables type to types stack
        typesStack.push(resultType)
        # Increment QuadCounter
        quadCounter += 1

        print("doOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
              quad.result))

def pushCycleJump(p):
    global quadCounter

    # Push quad to be jumpfilled
    jumpsStack.push(quadCounter)
    print('pushCycleJump', jumpsStack.top())

def doCycleOperations(p):
    global quadCounter

    # Get the type of the evaluated expression
    expressionType = typesStack.pop()
    # Get the result of the expression
    expressionResult = operandsStack.pop()

    # Check if expressions type is boolean or not
    if expressionType != 'bool':
        # Execute type missmatch error
        errorTypeMismatch(p)
    else:
        # Create quadruple to jump if cycle condition if false
        quad = Quadruple(quadCounter, 'gotof', expressionResult, None, None)
        # Add quad to QuadCounter
        quadQueue.enqueue(quad)
        # Push quad to be jumpfilled
        jumpsStack.push(quadCounter - 1)
        print('doCycleOperations', jumpsStack.top())
        print('doCycleOperations', jumpsStack.items)
        # Increment QuadCounter
        quadCounter += 1

        print("doCycleOperations", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                                       quad.right_operand, quad.result), "line: " + str(p.lexer.lineno))

def doEndCycleOperations(p):
    global quadCounter

    # Get number of pending quad to fill
    end = jumpsStack.pop()
    # Get number of quad to return
    retrn = jumpsStack.pop()
    # Get reverse position of Queue
    quadNumber = (quadQueue.size() - 1) - end
    # Get reverse position of Queue
    returnJump = (quadQueue.size() - 1) - retrn
    # Get quad to fill
    endQuad = quadQueue.get(quadNumber)

    # Create quadruple to return in cycle
    quad = Quadruple(quadCounter, 'goto', None, None, end)
    # Add quad to QuadQueue
    quadQueue.enqueue(quad)
    # Increment QuadCounter
    quadCounter += 1
    # Fill quads jump
    endQuad.addJump(quadCounter)

    print("doEndCycleOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                                   quad.right_operand, quad.result), "line: " + str(p.lexer.lineno))

def storeFunction(p):
    global currentScope

    # Get function name and type
    funcId = p[-1]
    funcType = p[-2]

    # Set default value depending on the variables type
    if funcType == 'int':
        value = defaultInt
    elif funcType == 'float':
        value = defaultFloat
    elif funcType == 'bool':
        value = defaultBool
    elif funcType == 'string':
        value = defaultString

    # ...........RECURSIVENESS..............
    # Check if the function type is void or not
    if funcType != 'void':
        # Store the functions returning variable space
        virtualAddress = memory.storeVariableToMemory(value, funcType)
        # Add return variable
        functionsDirectory.addFunctionVariable(globalScope, funcId, funcType, virtualAddress)

        print("storeFunction Virtual Address", virtualAddress)

    # Check if the function already exists
    if functionsDirectory.lookupFunction(funcId):
        # Execute Variable Already Declared Error
        errorFunctionAlreadyDeclared(p, funcId)
    else:
        # Change the scope to the current local (Function)
        currentScope = funcId
        # Store function into the functions directory
        functionsDirectory.insertFunction(funcId, funcType, None)

        print("storeFunction", currentScope, functionsDirectory.getFunctionType(funcId),
              "line: " + str(p.lexer.lineno))

def storeParameter(p):
    global currentScope

    # Get parameter name and type
    paramId = p[-1]
    paramType = p[-2]

    # Set default value depending on the variables type
    if paramType == 'int':
        value = defaultInt
    elif paramType == 'float':
        value = defaultFloat
    elif paramType == 'bool':
        value = defaultBool
    elif paramType == 'string':
        value = defaultString

    # Store the parameter into memory
    virtualAddress = memory.storeTempToMemory(value, paramType)

    print("storeParameter Virtual Address", globalScope, virtualAddress)

    # Add variable to functions vars table
    if functionsDirectory.addFunctionVariable(currentScope, paramId, paramType, virtualAddress):
        # Add parameter type to the function
        functionsDirectory.addParameterType(currentScope, paramType)
        # Add parameter virtual address to the function
        functionsDirectory.addParameterAddress(currentScope, virtualAddress)

        print("storeParameter1", currentScope, functionsDirectory.getFunctionVariable(currentScope, virtualAddress),
              "line: " + str(p.lexer.lineno))
        print("storeParameter2", currentScope, functionsDirectory.getParameterAddresses(currentScope),
              "line: " + str(p.lexer.lineno))

def addFunctionQuadStart(p):
    global quadCounter
    global currentScope

    # Add the quad number where main function starts
    functionsDirectory.setStartQuadNumber(currentScope, quadCounter)

    print("addFunctionQuadStart", currentScope, functionsDirectory.getStartQuadNumber(currentScope),
          "line: " + str(p.lexer.lineno))

def returnOperation(p):
    global quadCounter
    global functionWithReturn
    global endprocnumber
    global returns

    # Get the functions type
    functionType = functionsDirectory.getFunctionType(currentScope)

    # Check if the function type is void or not
    if functionType == 'void':
        errorVoidFunction(p)
    else:
        # Set the variable that identifies if the function has return or not
        functionWithReturn = True
        # Get return operand
        operand = operandsStack.pop()
        # Get return operands type
        type = typesStack.pop()
        # Get the returning functions variable
        functionVariable = functionsDirectory.getFunctionVariable(globalScope, currentScope)
        funcVirtualAddress = functionVariable[1][1]
        # Check if the operands type is the same as the function type
        if type != functionType:
            errorReturnWrongType(p)
        else:
            returns += 1
            returnStack.push(quadCounter)
            # Create quadruple for the negation operation
            quad = Quadruple(quadCounter, 'RETURN', operand, funcVirtualAddress, None)
            # Add quad to QuadQueue
            quadQueue.enqueue(quad)
            # Push temporal variable to operands stack
            operandsStack.push(funcVirtualAddress)
            # Push temporal variables type to types stack
            typesStack.push(functionType)
            # Increment QuadCounter
            quadCounter += 1

            print("returnOperation", currentScope, ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                              quad.result),
                  "line: " + str(p.lexer.lineno))

def endProcess(p):
    global quadCounter
    global returns
    print('returns.........', returns)
    # Get the functions type
    functionType = functionsDirectory.getFunctionType(currentScope)
    # Save quad number to bie jumpfilled
    funcReturn[currentScope] = quadCounter
    # Save
    endprocnumber = quadCounter
    for i in range(0, returns):
        # Get number of pending quad to fill
        end = returnStack.pop()
        # Get reverse position of Queue
        quadNumber = (quadQueue.size()) - end
        # Get quad to fill
        quad = quadQueue.get(quadNumber)
        # Full quads jump
        quad.addJump(quadCounter)
        print("endProcess", currentScope,
          ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
           quad.result),
          "line: " + str(p.lexer.lineno))

    # Check if the functions type is void or not
    if functionType != 'void':
        # Check if the function has return or not
        if not functionWithReturn:
            errorFunctionNoReturn(p)
        else:
            # Create quadruple for the end process
            quad = Quadruple(quadCounter, 'ENDPROC', None, None, None)
            # Add quad to QuadQueue
            quadQueue.enqueue(quad)
            # Increment QuadCounter
            quadCounter += 1
    else:
        # Create quadruple for the end process
        quad = Quadruple(quadCounter, 'ENDPROC', None, None, None)
        # Add quad to QuadQueue
        quadQueue.enqueue(quad)
        # Increment QuadCounter
        quadCounter += 1

    returns = 0
    # When function ends, clear temporal memory
    memory.clearTempMemory()

def checkFunctionExistance(p):
    global calledFunction

    # Get the function that is called
    calledFunction = p[-1]

    # Check if the function exists or not
    if not functionsDirectory.lookupFunction(calledFunction):
        # Execute Variable Already Declared Error
        errorFunctionDoesNotExist(p, calledFunction)
    else:
        print("checkFunctionExistance", currentScope, functionsDirectory.getFunctionType(calledFunction),
              "line: " + str(p.lexer.lineno))


def storeArgument(p):
    # Get the argument
    argument = operandsStack.pop()
    # Get the argument type
    argumentType = typesStack.pop()
    # Push the argument to the argument stack
    argumentQueue.enqueue(argument)
    # Push the argument type to the argument type stack
    argumTypeQueue.enqueue(argumentType)

def validateArguments(p):
    global argumentQueue
    global argumTypeQueue
    global calledFunction
    global quadCounter
    global argumCounter

    # Get the list of parameter addresses
    paramAddresses = functionsDirectory.getParameterAddresses(calledFunction)

    # Check if the arguments of the call are the same than the functions declaration
    if not functionsDirectory.validateParameters(calledFunction, argumTypeQueue.items):
        errorArgumentsMissmatch(p)
    else:
        while not argumentQueue.isEmpty():
            # Create quadruple for ERA operation
            quad = Quadruple(quadCounter, 'PARAM', argumentQueue.dequeue(), None, paramAddresses[argumCounter])
            # Add quad to QuadQueue
            quadQueue.enqueue(quad)
            # Increment QuadCounter
            quadCounter += 1
            # Increment argumCounter
            argumCounter += 1

            print("validateArguments 1", currentScope,
                  ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                   quad.result),
                  "line: " + str(p.lexer.lineno))

        startQuad = functionsDirectory.getStartQuadNumber(calledFunction)
        # Create quadruple for the gosub operation
        quad = Quadruple(quadCounter, 'gosub', calledFunction, None, startQuad)
        # Add quad to QuadQueue
        quadQueue.enqueue(quad)
        # Increment QuadCounter
        quadCounter += 1


        print("validateArguments 2", currentScope,
              ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
               quad.result),
              "line: " + str(p.lexer.lineno))

        # Get functions type
        functionType = functionsDirectory.getFunctionType(calledFunction)
        # Check if the functions is void or not
        if functionType == 'void':
            # Push Error Tag if the function is void
            operandsStack.push('Error')
            # Push the functions type to the typesStack
            typesStack.push(functionType)
        else:
            # Get the functions returning variable
            funcVar = functionsDirectory.getFunctionVariable(globalScope, calledFunction)
            # Get variable virtual address
            varVirtualAddress = funcVar[1][1]
            # Push functions name to the operands stack
            operandsStack.push(varVirtualAddress)
            # Push functions type to the typesStack
            typesStack.push(functionType)
            # Increment Temporal Variables Counter
            print("validateArguments 3", currentScope, "line: " + str(p.lexer.lineno))

        # Clear arguments elements
        argumentQueue = Queue()
        argumTypeQueue = Queue()
        calledFunction = ""
        argumCounter = 0


def accessDimenVariable(p):
    global dimenSupLim

    # Get the dimensional variable name
    varId = p[-3]
    print varId

    # Get the superior limit of the variable
    functionLocal = functionsDirectory.functions[currentScope]
    varTableLocal = functionLocal['variables']
    if not varTableLocal.lookupVariable(varId):
        functionGlobal = functionsDirectory.functions[globalScope]
        varTableGlobal = functionGlobal['variables']
        if not varTableGlobal.lookupVariable(varId):
            errorVariableNotDeclared(p, varId)
        else:
            dimension = functionsDirectory.getVariableDimension(globalScope, varId)
            # Set global superior limit
            dimenSupLim = dimension

            print("accessDimenVariable", globalScope, dimension)
    else:
        dimension = functionsDirectory.getVariableDimension(currentScope, varId)
        # Set global superior limit
        dimenSupLim = dimension

        print("accessDimenVariable", currentScope, dimension)

def dimenVariable(p):
    global dimenVar

    # Get dimensional variable
    dimenVar = p[-2]

def calculateDimen(p):
    global dimenVar
    global dimenSupLim

    # Get index of dimensional variable
    index = operandsStack.pop()
    # Get index type of dimensional variable
    indexType = typesStack.pop()

    # Check if the index type is int or not
    if indexType != 'int':
        errorTypeMismatch(p)
    else:
        # Get the dimension size
        dimenSize = memory.getValueByAddress(index)

        print ('dimenSize', dimenSize)
        # Get superior limit from the dimention size
        dimenSupLim = dimenSize-1

        print ('dimenSupLim', dimenSupLim)

def validateIndex(p):
    global quadCounter

    # Get index of dimensional variable
    index = operandsStack.pop()
    # Get index type of dimensional variable
    indexType = typesStack.pop()
    print memory.memoryBlock[index]
    # Check if the index type is int or not
    if indexType != 'int':
        errorArgumentsMissmatch(p)
    else:
        # Create quadruple for the VERIFICATION
        quad = Quadruple(quadCounter, 'VER', index, 0, dimenSupLim)
        # Add quad to QuadQueue
        quadQueue.enqueue(quad)
        # Increment quadCounter
        quadCounter += 1

        # Get the base address of the dimensional variable
        dimenVarBaseAddress = operandsStack.pop()
        # Get the dimensional variable type
        dimenVarType = typesStack.pop()
        # Store de dimensional variable base address into memory
        baseAddress = memory.storeTempToMemory(dimenVarBaseAddress, 'int')
        # Store de dimensional variable base address into memory to get the actual address of the index
        virtualAddress = memory.storeTempToMemory(dimenVarBaseAddress, dimenVarType)

        # Create quadruple to get indexed address
        quad = Quadruple(quadCounter, '+', index, baseAddress, virtualAddress)
        # Add quad to QuadQueue
        quadQueue.enqueue(quad)
        # Increment quadCounter
        quadCounter += 1
        # Push indexed address to operands stack
        operandsStack.push([virtualAddress])
        # Push dimensional variable type
        typesStack.push(dimenVarType)

        print(
        "validateIndex", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand, quad.result),
        "line: " + str(p.lexer.lineno))

def endProgram(p):
    global quadQueue

    # Create ending quad
    quad = Quadruple(quadCounter, "END", None, None, None)
    # Add quad to QuadQueue
    quadQueue.enqueue(quad)

    print("endProgram", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                          quad.result))
    print("Correct Sintax.\n\n")

    # Show list of quadruples
    #quadQueue.printQueue()

    vm = virtual_Machine(quadQueue, memory, functionsDirectory)

# Error functions
def p_error(p):
    print('ERROR: Syntax Error in line: ' + str(p.lexer.lineno))
    sys.exit()

def errorTypeMismatch(p):
    print('ERROR: Type mismatch in line ' + str(p.lexer.lineno))
    sys.exit()

def errorVariableNotDeclared(p, varId):
    print('Error: variable ' + str(varId) + ' not declared in line ' + str(p.lexer.lineno))
    sys.exit()

def errorVariableAlreadyDeclared(p, varId):
    print('Error: variable ' + str(varId) + ' already declared in line ' + str(p.lexer.lineno))
    sys.exit()

def errorFunctionAlreadyDeclared(p, funcId):
    print('Error: Function ' + str(funcId) + ' already declared in line ' + str(p.lexer.lineno))
    sys.exit()

def errorReturnWrongType(p):
    print('Error: Returning wrong type from function in line ' + str(p.lexer.lineno))
    sys.exit()

def errorFunctionNoReturn(p):
    print('Error: Function has no return statement in line ' + str(p.lexer.lineno))
    sys.exit()

def errorVoidFunction(p):
    print('Error: Void function trying to return in line ' + str(p.lexer.lineno))
    sys.exit()

def errorFunctionDoesNotExist(p, funcId):
    print('Error: Function ' + str(funcId) + ' does not exists in line ' + str(p.lexer.lineno))
    sys.exit()

def errorArgumentTypeMissmatch(p):
    print('Error: Argument type missmatch in line ' + str(p.lexer.lineno))
    sys.exit()

def errorArgumentsMissmatch(p):
    print('Error: Arguments missmatch function declaration in line ' + str(p.lexer.lineno))
    sys.exit()

def errorCannotAllocate(p, varId):
    print('Error: Can not allocate variable ' + str(varId) + ' in memory in line ' + str(p.lexer.lineno))
    sys.exit()

def errorNotReturnFunction(p):
    print('Error: Function not returning anything in line ' + str(p.lexer.lineno))
    sys.exit()

# Build parser
parser = yacc.yacc()

print("Introduce el nombre del archivo: ")
filename = raw_input()

file = open("./Pruebas/"+str(filename), 'r')

parser.parse(file.read())