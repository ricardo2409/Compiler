#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ply.yacc as yacc
import sys

sys.path.append(".")

from scanner import tokens
from DataStructures.FunctionsDirectory import functions_Directory
from DataStructures.Stack import Stack
from DataStructures.VariablesTable import vars_Table
from DataStructures.Quadruple import Quadruple
from DataStructures.Queue import Queue
from DataStructures.SemanticCube import semantic_Cube
from Memory.Memory import memory_Block
from VirtualMachine.VirtualMachine import virtual_Machine
#-----------------------------------------------------------------

# Directorios
functionsDirectory = functions_Directory()
semanticCube = semantic_Cube()
funcReturn = {}

# Memoria
memory = memory_Block()

# Scope para manejo de las variables
currentScope = ""
globalScope = ""
calledFunction = ""

# Contadores
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

# Variables para el manejo de dimensiones
dimenVar = ""
dimenSupLim = 0

# Variables globales
endprocnumber = 0
returns = 0

# Maquina Virtual
vm = None

# Valores predefinidos para las variables
defaultInt = 0
defaultFloat = 0.0
defaultBool = False
defaultString = 'Null'
# Variable para validación de funcion con return
functionWithReturn = False

# Reglas Gramaticales
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
    # Crea el cuadruplo del main
    gotoMain(p)

def p_add_jump_to_main(p):
    '''
    add_jump_to_main :
    '''
    # Llena el campo del jump en el cuadruplo del main creado anteriormente
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
            | predefined
            | return
    '''

def p_CONDITION(p):
    '''
    condition : IF LPAREN sexpression RPAREN do_condition_operation block else
    '''
    # Llena los jumps de los cuadruplos de condición
    doEndConditionOperation(p)

def p_do_condition_operation(p):
    '''
    do_condition_operation :
    '''
    # Hace las operaciones de condición y los cuadruplos
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
    # Hace las operaciones de else y los cuadruploss
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
    # Guarda las variables en la tabla de variables con su scope correspondiente
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
    # Hace las operaciones de asignación y los cuadruplos
    doAssignOperation(p)

def p_push_id_operand(p):
    '''
    push_id_operand :
    '''
    # Introduce el operando en el stack
    pushOperand(p)

def p_push_operator(p):
    '''
    push_operator :
    '''
    # Introduce el operador en el stack
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
    # Hace la operación de not y su cuadruplo
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
    # Hace la operacion de los relacionaes y su cuadruplo
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
    # Hace la operacion del más y menos y su cuadruplo
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
    # Hace la operacion de la multiplicación y división y su cuadruplo
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
             | predefined
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
    # Introduce el operando float
    pushFloatOperand(p)

def p_push_int_operand(p):
    '''
    push_int_operand :
    '''
    # Introduce el operando int
    pushIntOperand(p)

def p_push_bool_operand(p):
    '''
    push_bool_operand :
    '''
    # Introduce el operando bool
    pushBoolOperand(p)

def p_push_string_operand(p):
    '''
    push_string_operand :
    '''
    # Introduce el operando string
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

def p_FUNCARGUM(p):
    '''
    funcargum : sexpression store_argument funcargumprima
              | empty
    '''
    
def p_validate_arguments(p):
    '''
    validate_arguments :
    '''
    validateArguments(p)

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
    # Crea los cuadruplos del write
    doWriteOperation(p)

def p_READ(p):
    '''
    read : ID push_id_operand array ASSIGN push_operator INPUT LPAREN RPAREN SEMICOLON
    '''
    # Crea los cuadruplos del read
    doReadOperation(p)

def p_CYCLE(p):
    '''
    cycle : WHILE push_cycle_jump LPAREN sexpression RPAREN do_while_operation block
    '''
    # Llena los saltos de los cuadruplos de ciclos
    doEndCycleOperations(p)

def p_push_cycle_jump(p):
    '''
    push_cycle_jump :
    '''
    # Introduce el salto al cuadruplo del ciclo
    pushCycleJump(p)

def p_do_while_operation(p):
    '''
    do_while_operation :
    '''
    # Hace los cuadruplos de los ciclos
    doCycleOperations(p)

def p_PREDEFINED(p):
    '''
    predefined : drawbarchart
               | drawdotchart
               | drawlinechart
               | drawhistchart
               | drawpolychart
    '''

def p_DRAWBARCHART(p):    
    '''
    drawbarchart : DRAWBARCHART LPAREN sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument RPAREN SEMICOLON
    '''
    # Crea el cuadruplo para crear la BarChart
    drawBarChart(p)

def p_DRAWDOTCHART(p):    
    '''
    drawdotchart : DRAWDOTCHART LPAREN sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument RPAREN SEMICOLON
    '''
    # Crea el cuadruplo para crear la DotChart
    drawDotChart(p)

def p_DRAWLINECHART(p):    
    '''
    drawlinechart : DRAWLINECHART LPAREN sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument RPAREN SEMICOLON
    '''
    # Crea el cuadruplo para crear la LineChart
    drawLineChart(p)

def p_DRAWHISTCHART(p):    
    '''
    drawhistchart : DRAWHISTCHART LPAREN sexpression store_predefined_argument COMMA sexpression store_predefined_argument RPAREN SEMICOLON
    '''
    # Crea el cuadruplo para crear la HistChart
    drawHistChart(p)

def p_DRAWPOLYCHART(p):    
    '''
    drawpolychart : DRAWPOLYCHART LPAREN sexpression store_predefined_argument COMMA sexpression store_predefined_argument COMMA sexpression store_predefined_argument RPAREN SEMICOLON
    '''
    # Crea el cuadruplo para crear la PolyChart
    drawPolyChart(p)

def p_store_predefined_argument(p):
    '''
    store_predefined_argument :
    '''
    # Guarda los argumentos pasados como parámetros en predefParamStack
    storePredefinedArgument(p)

def p_EMPTY(p):
    '''
    empty :
    '''
    pass

# NoYacc Funciones
def storeGlobalFunc(p):
    global currentScope
    global globalScope

    #Guarda en globalScope y CurrentScope el nombre de la función actual
    globalScope = p[-1]
    currentScope = p[-1]

    # Crea el directorio de funciones con el nombre de la función actual
    functionsDirectory.insertFunction(currentScope, 'void', None)
    print("storeGlobalFunction", currentScope, functionsDirectory.getFunctionType(currentScope))

def changeToGlobal(p):
    global currentScope
    global globalScope

    currentScope = globalScope
    # Agrega el número del cuadruplo donde empieza el main
    functionsDirectory.setStartQuadNumber(globalScope, quadCounter)
    print("changeToGlobal", currentScope, functionsDirectory.getStartQuadNumber(globalScope))

def addJumpToMain(p):
    global quadCounter

    # Obtiene el número del salto pendiente a agregar a cuadruplo 
    end = jumpsStack.pop()
    # Obtiene el número del cuadruplo correspondiente
    quadNumber = (quadQueue.size()) - end
    # Obtiene el cuadruplo a llenar
    quad = quadQueue.get(quadNumber)
    # Agrega salto a cuadruplo
    quad.addJump(quadCounter)

    print("addJumpToMain", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand, quad.result),
          "line: " + str(p.lexer.lineno))

def gotoMain(p):
    global quadCounter

    # Agrega a JumpsStack el número del cuadruplo a ser llenado
    jumpsStack.push(quadCounter)
    # Crea el cuadruplo gotomain
    quad = Quadruple(quadCounter, 'goto', None, None, None)
    # Agrega el cuadruplo a la queue de Cuadruplos
    quadQueue.enqueue(quad)
    # Incrementa el contador de cuadruplos
    quadCounter += 1

    print("gotoMain",
          ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand, quad.result),
          "line: " + str(p.lexer.lineno))

def storeVariable(p):
    global currentScope
    global dimenVar
    global dimenSupLim

    # Obtiene el nombre de la variable y su tipo
    varId = p[-2]
    varType = p[-3]

    # Asigna a value el valor default del tipo correspondiente de la variable
    if varType == 'int':
        value = defaultInt
    elif varType == 'float':
        value = defaultFloat
    elif varType == 'bool':
        value = defaultBool
    elif varType == 'string':
        value = defaultString

    # Checa si el scope actual es el main
    if currentScope == globalScope:
        # Checa si la variable es dimensionada
        if dimenVar != '':
            # Guarda la variable dimensional en memoria
            virtualAddress = memory.storeDimensionVarToMemory(value, varType, dimenSupLim)
        else:
            # Guarda la variable no dimensional en memoria
            virtualAddress = memory.storeVariableToMemory(value, varType)
    else:
        # El scope actual no es main
        if dimenVar != '':
            # Checa si la variable temporal es dimensionada y la guarda en memoria
            virtualAddress = memory.storeDimensionTempToMemory(value, varType, dimenSupLim)
        else:
            # Guarda la variable temporal no dimensionada en memoria
            virtualAddress = memory.storeTempToMemory(value, varType)

    # Checa si se pudo guardar la variable
    if virtualAddress == None:
        #Despliega error
        errorCannotAllocate(p, varId)
    else:
        # Checa si la variable ya estaba declarada
        if not functionsDirectory.addFunctionVariable(currentScope, varId, varType, virtualAddress):
            # Despliega el error correspondiente
            errorVariableAlreadyDeclared(p, varId)
        else:
            # Introduce la dirección virtual en operandsStack
            operandsStack.push(virtualAddress)
            # Introduce el tipo en typesStack
            typesStack.push(varType)
            # Checa si la variable es dimensional para guardar su dimensión en su espacio correspondiente
            if dimenVar != '':
                # Agrega la dimensión a la variable en la table de variables
                functionsDirectory.addDimensionToVariable(currentScope, varId, dimenSupLim)
                # Reset a los valores para su reutilización
                dimenSupLim = 0
                dimenVar = ''

            print("storeVariable", currentScope, functionsDirectory.getFunctionVariable(currentScope, varId),
                      "line: " + str(p.lexer.lineno))

def pushOperand(p):
    global currentScope

    # Obtiene el nombre de la variable
    varId = p[-1]
    # Obtiene la variable de la tabla de variables del scope actual
    funcVar = functionsDirectory.getFunctionVariable(currentScope, varId)

    # Checa si la variable existe en la tabla de variables del scope actual
    if funcVar is None:
        funcVar = functionsDirectory.getFunctionVariable(globalScope, varId)
        # Checa si la varible existe en el scope global
        if funcVar is None:
            # No existe en scope actual ni scope global y se despliega el error
            errorVariableNotDeclared(p, varId)
        else:
            # Obtiene la varible
            funcVarInfo = funcVar[1]
            # Obtener el tipo de la variable
            funcVarType = funcVarInfo[0]
            # Obtener el nombre de la variable
            funcVarId = funcVarInfo[1]
            # Insertar el nombre en el typesStack
            operandsStack.push(funcVarId)
            # Insertar el tipo en el typesStack
            typesStack.push(funcVarType)
    else:
        # Obtiene la varible
        funcVarInfo = funcVar[1]
        # Obtener el tipo de la variable
        funcVarType = funcVarInfo[0]
        # Obtener el nombre de la variable
        funcVarId = funcVarInfo[1]
        # Insertar el nombre en el typesStack
        operandsStack.push(funcVarId)
        # Insertar el nombre en el typesStack
        typesStack.push(funcVarType)

    print("pushIdOperand", operandsStack.top(), typesStack.top())

def pushOperator(p):
    # Obtener el operador
    operator = p[-1]
    # Introduce el operador en el operatorStack
    operatorsStack.push(operator)

    print('push_operator', operatorsStack.top())

def pushFloatOperand(p):
    global operandsStack
    global operatorsStack

    # Obtener el operando
    operand = p[-1]
    # Guarda la memoria constante en memoria y obtiene la dirección virtual
    virtualAddress = memory.storeConstantToMemory(operand, 'float')
    # Introduce la dirección en el operandsStack
    operandsStack.push(virtualAddress)
    # Introduce el tipo en el typesStack
    typesStack.push('float')

    print("push_float_operand", operandsStack.top(), typesStack.top())

def pushIntOperand(p):
    global operandsStack
    global operatorsStack

    # Obtener el operando
    operand = p[-1]
    # Guarda la memoria constante en memoria y obtiene la dirección virtual
    virtualAddress = memory.storeConstantToMemory(operand, 'int')
    # Introduce la dirección en el operandsStack
    operandsStack.push(virtualAddress)
    # Introduce el tipo en el typesStack
    typesStack.push('int')

    print("push_int_operand", operandsStack.top(), typesStack.top())

def pushBoolOperand(p):
    global operandsStack
    global operatorsStack

    # Obtener el operando
    operand = p[-1]
    if operand == 'true':
        operand = True
    elif operand == 'false':
        operand = False

    # Guarda la memoria constante en memoria y obtiene la dirección virtual
    virtualAddress = memory.storeConstantToMemory(operand, 'bool')
    # Introduce la dirección en el operandsStack
    operandsStack.push(virtualAddress)
    # Introduce el tipo en el typesStack
    typesStack.push('bool')

    print("push_bool_operand", operandsStack.top(), typesStack.top())

def pushStringOperand(p):
    global operandsStack
    global operatorsStack

    # Obtener el operando
    operand = p[-1]
    # Guarda la memoria constante en memoria y obtiene la dirección virtual
    virtualAddress = memory.storeConstantToMemory(operand, 'string')
    # Introduce la dirección en el operandsStack
    operandsStack.push(virtualAddress)
    # Introduce el tipo en el typesStack
    typesStack.push('string')

    print("push_string_operand", operandsStack.top(), typesStack.top())

def doReadOperation(p):
    global quadCounter

    # Obtiene el operando de operandStack
    operand = operandsStack.pop()
    # Obtiene el tipo de typesStack
    type = typesStack.pop()
    # Crea el cuadruplo para el read
    quad = Quadruple(quadCounter, 'READ', type, None, operand)
    # Agrega el cuadruplo a la queue
    quadQueue.enqueue(quad)
    # Incrementa el contador
    quadCounter += 1

    print("read", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand, quad.result),
          "line: " + str(p.lexer.lineno))

def doWriteOperation(p):
    global quadCounter

    # Obtiene el operando de operandStack
    operand = operandsStack.pop()
    # Obtiene el tipo de typesStack
    popType = typesStack.pop()
    # Crea el cuadruplo para el write
    quad = Quadruple(quadCounter, 'WRITE', operand, None, None)
    # Agrega el cuadruplo a la queue
    quadQueue.enqueue(quad)
    # Incrementa el contador
    quadCounter += 1

    print("write", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand, quad.result),
          "line: " + str(p.lexer.lineno))


def doNotOperation(p):
    global semanticCube
    global quadCounter

    # Checa que el operatorStack no esté vacio
    if not operatorsStack.isEmpty():
        # Checa que el operador de arriba sea un '!'
        if operatorsStack.top() == '!':
            # Obtener el operando
            operand = operandsStack.pop()
            # Obtener el tipo
            type = typesStack.pop()
            # Obtener el operador
            operator = operatorsStack.pop()

            # Checa que el tipo sea bool
            if type != 'bool':
                resultType = 'Error'
            else:
                resultType = 'bool'
                #Cambia el valor a false
                value = defaultBool

            # Checa si el resultado del tipo es bool
            if resultType != 'bool':
                # Despliega el error typeMismatch
                errorTypeMismatch(p)
            else:
                # Guarda el valor en memoria temporal y obtiene su dirección
                virtualAddress = memory.storeTempToMemory(value, resultType)
                # Crea el cuadruplo de la negación
                quad = Quadruple(quadCounter, operator, operand, None,
                                 virtualAddress)  # Last parameter should be the VirtualAddress
                # Agrega el cuadruplo a la queue
                quadQueue.enqueue(quad)
                # Inserta la variable temporal al operandsStack
                operandsStack.push(virtualAddress)
                # Inserta el tipo temporal al typesStack
                typesStack.push(resultType)
                # Incrementa el contador de cuadruplos
                quadCounter += 1

                print("doNotOperation",("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                quad.result), str(p.lexer.lineno))

def doConditionOperation(p):
    global quadCounter

    # Obtener el tipo de la expresión
    expressionType = typesStack.pop()
    # Obtener el resultado de la expresión
    expressionResult = operandsStack.pop()
    # Checa si la expresión es bool
    if expressionType != 'bool':
        # Despliega el error de type mismatch
        errorTypeMismatch(p)
    else:
        # Crea el cuadruplo de gotof
        quad = Quadruple(quadCounter, 'gotof', expressionResult, None, None)
        # Agrega el cuadruplo a la queue
        quadQueue.enqueue(quad)
        # Inserta el cuadruplo anterior a ser llenado a la jumpStack
        jumpsStack.push(quadCounter - 1)
        # Incrementa el contador
        quadCounter += 1

        print("doConditionOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                                    quad.right_operand, quad.result), "line: " +str(p.lexer.lineno))

def doEndConditionOperation(p):
    global quadCounter

    # Obtener el numero del salto pendiente
    end = jumpsStack.pop()
    # Obtener el número del cuadruplo pendiente
    quadNumber = (quadQueue.size() - 1) - end
    # Obtener el cuadruplo a llenar
    quad = quadQueue.get(quadNumber)
    # Agrega el jump al cuadruplo
    quad.addJump(quadCounter)

    print("doEndConditionOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                                   quad.right_operand, quad.result), "line: " + str(p.lexer.lineno))

def doElseOperation(p):
    global quadCounter

    # Crear el cuadruplo del goto vacío al final del else
    quad = Quadruple(quadCounter, 'goto', None, None, None)
    # Agregar el cuadruplo a la queue
    quadQueue.enqueue(quad)
    # Obtiene el número pendiente del salto a llenar
    num = jumpsStack.pop()
    # Obtiene el numero del último cuadruplo
    quadNumber = (quadQueue.size() - 1) - num
    # Inserta el numero del cuadruplo a ser llenado
    jumpsStack.push(quadCounter - 1)
    # Incrementa el contador
    quadCounter += 1
    # Obtiene el cuadruplo de la queue
    quad = quadQueue.get(quadNumber)
    # Le agrega el salto al cuadruplo correspondiente
    quad.addJump(quadCounter)

    print("doElseOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                                quad.right_operand, quad.result), "line: " +str(p.lexer.lineno))

def doAssignOperation(p):
    global semanticCube
    global quadCounter

    # Obtiene el operando derecho
    rightOperand = operandsStack.pop()
    # Obtiene el tipo derecho
    rightType = typesStack.pop()
    # Obtiene el operando izquierdo
    leftOperand = operandsStack.pop()
    # Obtiene el tipo derecho
    leftType = typesStack.pop()
    # Obtiene el operador
    operator = operatorsStack.pop()

    if rightType == 'void':
        errorNotReturnFunction(p)
    else:
        # Obtener el resultado del cubo semántico con tipo izquierdo, tipo derecho y el operador
        resultType = semanticCube.getType(leftType, rightType, operator)

        # Checa el resultado que mandó el cubo semántico
        if resultType == 'Error':
            errorTypeMismatch(p)
        else:
            # Crea el cuadruplo de la asignación
            quad = Quadruple(quadCounter, operator, rightOperand, None, leftOperand)
            # Agrega el cuadruplo a la queue
            quadQueue.enqueue(quad)
            # Incrementa el contador
            quadCounter += 1

            print("doAssignOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                  quad.right_operand, quad.result), "line: " +str(p.lexer.lineno))

def doOperations(p):
    global semanticCube
    global quadCounter

    # Obtiene el operando derecho
    rightOperand = operandsStack.pop()
    # Obtiene el tipo derecho
    rightType = typesStack.pop()
    # Obtiene el operando izquierdo
    leftOperand = operandsStack.pop()
    # Obtiene el tipo izquierdo
    leftType = typesStack.pop()
    # Obtiene el operador correspondiente
    operator = operatorsStack.pop()

    # Obtener el resultado del cubo semántico con tipo izquierdo, tipo derecho y el operador
    resultType = semanticCube.getType(leftType, rightType, operator)

    # Asignar el valor por default dependiendo del tipo
    if resultType == 'int':
        value = defaultInt
    elif resultType == 'float':
        value = defaultFloat
    elif resultType == 'bool':
        value = defaultBool
    elif resultType == 'string':
        value = defaultString

    # Checa si el resultado del cubo semántico es error
    if resultType == 'Error':
       
        #Ejecuta error type missmatch
        errorTypeMismatch(p)
    else:
        # Guarda la variable en memoria temporal y obtiene la dirección virtual
        virtualAddress = memory.storeTempToMemory(value, resultType)
        # Crea el cuadruplo
        quad = Quadruple(quadCounter, operator, leftOperand, rightOperand, virtualAddress)
        # Agrega el cuadruplo a la queue
        quadQueue.enqueue(quad)
        # Inserta la dirección en el operandStack
        operandsStack.push(virtualAddress)
        # Inserta el tipo resultante en el typeStack
        typesStack.push(resultType)
        # Incrementa el contador
        quadCounter += 1

        print("doOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
              quad.result))

def pushCycleJump(p):
    global quadCounter

    # Inserta el número de cuadruplo a ser llenado
    jumpsStack.push(quadCounter)
    print('pushCycleJump', jumpsStack.top())

def doCycleOperations(p):
    global quadCounter

    # Obtiene el tipo de la expresión
    expressionType = typesStack.pop()
    # Obtiene el resultado de la expresión
    expressionResult = operandsStack.pop()

    # Checa si la expresión es booleana
    if expressionType != 'bool':
        # Despliega el error de type mismatch
        errorTypeMismatch(p)
    else:
        # Crea el cuadruplo de gotof de la condición false vacío
        quad = Quadruple(quadCounter, 'gotof', expressionResult, None, None)
        # Agrega el cuadruplo a la queue
        quadQueue.enqueue(quad)
        # Agrega el número del cuadrúplo a ser rellenado después
        jumpsStack.push(quadCounter - 1)
        print('doCycleOperations', jumpsStack.top())
        print('doCycleOperations', jumpsStack.items)
        # Incrementa el contador
        quadCounter += 1

        print("doCycleOperations", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                                       quad.right_operand, quad.result), "line: " + str(p.lexer.lineno))

def doEndCycleOperations(p):
    global quadCounter

    # Obtiene el número pendiente de cuadruplo a llenar
    end = jumpsStack.pop()
    # Obtiene el número de cuadruplo a regresar
    retrn = jumpsStack.pop()
    # Obtiene la posición del cuadruplo a llenar
    quadNumber = (quadQueue.size() - 1) - end
    # Obtiene la posición del cuadruplo a regresar
    returnJump = (quadQueue.size() - 1) - retrn
    # Obtiene el cuadruplo a llenar
    endQuad = quadQueue.get(quadNumber)

    # Crea el cuadruplo a regresar
    quad = Quadruple(quadCounter, 'goto', None, None, end)
    # Agrega el cuadruplo a la queue
    quadQueue.enqueue(quad)
    # Incrementa contador
    quadCounter += 1
    # Agrega el salto al cuadruplo
    endQuad.addJump(quadCounter)

    print("doEndCycleOperation", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand,
                                   quad.right_operand, quad.result), "line: " + str(p.lexer.lineno))

def storeFunction(p):
    global currentScope

    # Obtiene el nombre y tipo de la función
    funcId = p[-1]
    funcType = p[-2]

    # Asigna a value el valor default del tipo correspondiente de la función
    if funcType == 'int':
        value = defaultInt
    elif funcType == 'float':
        value = defaultFloat
    elif funcType == 'bool':
        value = defaultBool
    elif funcType == 'string':
        value = defaultString

    # RECURSIVIDAD
    # Asignar el valor por default dependiendo del tipo
    if funcType != 'void':
        # Guarda la funcón en memoría y obtiene la dirección
        virtualAddress = memory.storeVariableToMemory(value, funcType)
        # Agrega la función en el directorio de funciones
        functionsDirectory.addFunctionVariable(globalScope, funcId, funcType, virtualAddress)

        print("storeFunction Virtual Address", virtualAddress)

    # Checa si la función ya existe
    if functionsDirectory.findFunction(funcId):
        # Error de función ya declarada
        errorFunctionAlreadyDeclared(p, funcId)
    else:
        # Cambia el scope a la función
        currentScope = funcId
        # Guarda la función y su tipo en el directorio de variables
        functionsDirectory.insertFunction(funcId, funcType, None)

        print("storeFunction", currentScope, functionsDirectory.getFunctionType(funcId),
              "line: " + str(p.lexer.lineno))

def storeParameter(p):
    global currentScope

    # Obtiene el nombre y tipo del parámetro
    paramId = p[-1]
    paramType = p[-2]

    # Asigna a value el valor default del tipo correspondiente del parámetro
    if paramType == 'int':
        value = defaultInt
    elif paramType == 'float':
        value = defaultFloat
    elif paramType == 'bool':
        value = defaultBool
    elif paramType == 'string':
        value = defaultString

    # Guarda el parámetro en la memory temporal
    virtualAddress = memory.storeTempToMemory(value, paramType)

    print("storeParameter Virtual Address", globalScope, virtualAddress)

    # Agrega la función a la tabla de variables
    if functionsDirectory.addFunctionVariable(currentScope, paramId, paramType, virtualAddress):
        # Agrega el tipo del parámetro de la función
        functionsDirectory.addParameterType(currentScope, paramType)
        # Agrega la dirección del parámetro de la función
        functionsDirectory.addParameterAddress(currentScope, virtualAddress)

        print("storeParameter1", currentScope, functionsDirectory.getFunctionVariable(currentScope, virtualAddress),
              "line: " + str(p.lexer.lineno))
        print("storeParameter2", currentScope, functionsDirectory.getParameterAddresses(currentScope),
              "line: " + str(p.lexer.lineno))

def addFunctionQuadStart(p):
    global quadCounter
    global currentScope

    # Agrega el número del cuadruplo donde inicia el main
    functionsDirectory.setStartQuadNumber(currentScope, quadCounter)

    print("addFunctionQuadStart", currentScope, functionsDirectory.getStartQuadNumber(currentScope),
          "line: " + str(p.lexer.lineno))

def returnOperation(p):
    global quadCounter
    global functionWithReturn
    global endprocnumber
    global returns

    # Obtiene el tipo de la función
    functionType = functionsDirectory.getFunctionType(currentScope)

    # Checa si la función es void
    if functionType == 'void':
        errorVoidFunction(p)
    else:
        # Cambiar la variable que identifica que una función tiene valor de retorno
        functionWithReturn = True
        # Obtiene el operando
        operand = operandsStack.pop()
        # Obtiene el tipo de retorno
        type = typesStack.pop()
        functionVariable = functionsDirectory.getFunctionVariable(globalScope, currentScope)
        funcVirtualAddress = functionVariable[1][1]
        # Checa si el tipo de retorno es diferente al de la función
        if type != functionType:
            errorReturnWrongType(p)
        else:
            #Contador de retornos para recursividad
            returns += 1
            returnStack.push(quadCounter)
            # Crea cuadruplo para el return
            quad = Quadruple(quadCounter, 'RETURN', operand, funcVirtualAddress, None)
            # Agrega cuadruplo a la queue
            quadQueue.enqueue(quad)
            # Inserta la dirección virtual al operandsStack
            operandsStack.push(funcVirtualAddress)
            # Inserta el tipo al typeStack
            typesStack.push(functionType)
            # Incrementa el contador
            quadCounter += 1

            print("returnOperation", currentScope, ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                              quad.result),
                  "line: " + str(p.lexer.lineno))

def endProcess(p):
    global quadCounter
    global returns
    print('returns.........', returns)
    # Obtiene el tipo de la función
    functionType = functionsDirectory.getFunctionType(currentScope)
    funcReturn[currentScope] = quadCounter
    endprocnumber = quadCounter
    #Ciclo para la cantidad de retorno
    for i in range(0, returns):
        # Obtiene el número del cuadruplo pendiente a llenar
        end = returnStack.pop()
        # Obtiene la posición del cuadruplo
        quadNumber = (quadQueue.size()) - end
        # Obtiene el cuadruplo a llenar
        quad = quadQueue.get(quadNumber)
        # Llena el cuadruplo con el salto correspondiente
        quad.addJump(quadCounter)
        print("endProcess", currentScope,
          ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
           quad.result),
          "line: " + str(p.lexer.lineno))

    # Checa si la función es void
    if functionType != 'void':
        # Checa si la función tiene un return
        if not functionWithReturn:
            errorFunctionNoReturn(p)
        else:
            # Crea cuadruplo con ENDPROC
            quad = Quadruple(quadCounter, 'ENDPROC', None, None, None)
            # AAgrega cuadruplo a la queue
            quadQueue.enqueue(quad)
            # Incrementa contador
            quadCounter += 1
    else:
        # Crea cuadruplo con ENDPROC
        quad = Quadruple(quadCounter, 'ENDPROC', None, None, None)
        # Agrega cuadruplo a la queue
        quadQueue.enqueue(quad)
        # Incrementa contador
        quadCounter += 1
    #Resetea variable de retornos
    returns = 0
    # Cuando termina la función se limpia la memoria temporal
    memory.clearTempMemory()

def checkFunctionExistance(p):
    global calledFunction
    # Obtiene la función llamada
    calledFunction = p[-1]
    # Checa si la función existe 
    if not functionsDirectory.findFunction(calledFunction):
        # Error de función no existe
        errorFunctionDoesNotExist(p, calledFunction)
    else:
        print("checkFunctionExistance", currentScope, functionsDirectory.getFunctionType(calledFunction),
              "line: " + str(p.lexer.lineno))

def generateEra(p):
    global quadCounter
    # Obtiene el nombre de la función
    funcId = p[-3]
    # Crea el cuadruplo de ERA
    quad = Quadruple(quadCounter,'ERA', funcId, None, None)
    # Agrega cuadruplo a la queue
    quadQueue.enqueue(quad)
    # Incrementa contador
    quadCounter += 1
    print("generateEra", currentScope,
          ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
           quad.result),
          "line: " + str(p.lexer.lineno))

def storeArgument(p):
    # Obtiene el argumento
    argument = operandsStack.pop()
    # Obtiene el tipo del argumento
    argumentType = typesStack.pop()
    # Inserta el argumento a la argumentQueue
    argumentQueue.enqueue(argument)
    # Inserta el tipo del argumento a la argumentTypeQueue
    argumTypeQueue.enqueue(argumentType)

def validateArguments(p):
    global argumentQueue
    global argumTypeQueue
    global calledFunction
    global quadCounter
    global argumCounter

    # Lista de direcciones de parámetros
    paramAddresses = functionsDirectory.getParameterAddresses(calledFunction)
    # Checa si los parámetros son del mismo tipo que lo que son declarados
    if not functionsDirectory.validateParameters(calledFunction, argumTypeQueue.items):
        errorArgumentsMissmatch(p)
    else:
        while not argumentQueue.isEmpty():
            # Crea el cuadruplo de PARAM
            quad = Quadruple(quadCounter, 'PARAM', argumentQueue.dequeue(), None, paramAddresses[argumCounter])
            # Agrega cuadruplo a la queue
            quadQueue.enqueue(quad)
            # Incrementa contador
            quadCounter += 1
            # Incrementa contador de argumentos
            argumCounter += 1

            print("validateArguments 1", currentScope,
                  ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                   quad.result),
                  "line: " + str(p.lexer.lineno))

        startQuad = functionsDirectory.getStartQuadNumber(calledFunction)
        # Crea el cuadruplo de gosub
        quad = Quadruple(quadCounter, 'gosub', calledFunction, None, startQuad)
        # Agrega cuadruplo a la queue
        quadQueue.enqueue(quad)
        # Incrementa contador
        quadCounter += 1

        print("validateArguments 2", currentScope,
              ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
               quad.result),
              "line: " + str(p.lexer.lineno))

        # Obtiene el tipo de la función
        functionType = functionsDirectory.getFunctionType(calledFunction)
        # Checa si la función es void
        if functionType == 'void':
            # Inserta error en la operandStack para tratar después
            operandsStack.push('Error')
            # Inserta el tipo a la typeStack
            typesStack.push(functionType)
        else:
            # Obtiene la variable de retorno de la función
            funcVar = functionsDirectory.getFunctionVariable(globalScope, calledFunction)
            # Obtiene la direcciñon virtual de la variable
            varVirtualAddress = funcVar[1][1]
            # Inserta el nombre de la variable
            operandsStack.push(varVirtualAddress)
            # Inserta el tipo de la variable
            typesStack.push(functionType)
            print("validateArguments 3", currentScope, "line: " + str(p.lexer.lineno))

        # Limpia las variables y contadores
        argumentQueue = Queue()
        argumTypeQueue = Queue()
        calledFunction = ""
        argumCounter = 0

def storePredefinedArgument(p):
    global currentScope

    # Obtiene el operando
    operand = operandsStack.pop()
    # Obtiene el tipo
    type = typesStack.pop()

    # Checa si los argumentos son de un tipo válido
    if type != 'int' and type != 'float' and type != 'bool':
        errorArgumentTypeMissmatch(p)
    else:
        # Inserta el parámetro de la función en el predefParamStack
        predefParamStack.push(operand)

        print("storePredefinedArgument", currentScope, operand,
              "line: " + str(p.lexer.lineno))

def drawBarChart(p):
    global predefParamStack
    global quadCounter
    # Crea el cuadruplo de DRAWBARCHART
    quad = Quadruple(quadCounter, 'DRAWBARCHART', predefParamStack.items, None, None)
    # Inserta el cuadruplo a la queue
    quadQueue.enqueue(quad)
    # Incrementa contador
    quadCounter += 1
    # Resetea el stack de parametros
    predefParamStack = Stack()

def drawDotChart(p):
    global predefParamStack
    global quadCounter
    # Crea el cuadruplo de DRAWDOTCHART
    quad = Quadruple(quadCounter, 'DRAWDOTCHART', predefParamStack.items, None, None)
    # Inserta el cuadruplo a la queue
    quadQueue.enqueue(quad)
    # Incrementa contador
    quadCounter += 1
    # Resetea el stack de parametros
    predefParamStack = Stack()

def drawLineChart(p):
    global predefParamStack
    global quadCounter
    # Crea el cuadruplo de DRAWLINECHART
    quad = Quadruple(quadCounter, 'DRAWLINECHART', predefParamStack.items, None, None)
    # Inserta el cuadruplo a la queue
    quadQueue.enqueue(quad)
    # Incrementa contador
    quadCounter += 1
    # Resetea el stack de parametros
    predefParamStack = Stack()

def drawHistChart(p):
    global predefParamStack
    global quadCounter
    # Crea el cuadruplo de DRAWHISTCHART
    quad = Quadruple(quadCounter, 'DRAWHISTCHART', predefParamStack.items, None, None)
    # Inserta el cuadruplo a la queue
    quadQueue.enqueue(quad)
    # Incrementa contador
    quadCounter += 1
    # Resetea el stack de parametros
    predefParamStack = Stack()

def drawPolyChart(p):
    global predefParamStack
    global quadCounter
    # Crea el cuadruplo de DRAWPOLYCHART
    quad = Quadruple(quadCounter, 'DRAWPOLYCHART', predefParamStack.items, None, None)
    # Inserta el cuadruplo a la queue
    quadQueue.enqueue(quad)
    # Incrementa contador
    quadCounter += 1
    # Resetea el stack de parametros
    predefParamStack = Stack()

def accessDimenVariable(p):
    global dimenSupLim

    # Obtiene el nombre de la variable dimensionada
    varId = p[-3]
    print varId

    # Obtiene el limite superior de la variable
    functionLocal = functionsDirectory.functions[currentScope]
    varTableLocal = functionLocal['variables']
    if not varTableLocal.findVariable(varId):
        functionGlobal = functionsDirectory.functions[globalScope]
        varTableGlobal = functionGlobal['variables']
        if not varTableGlobal.findVariable(varId):
            errorVariableNotDeclared(p, varId)
        else:
            #Si está en globalScope
            dimension = functionsDirectory.getVariableDimension(globalScope, varId)
            dimenSupLim = dimension

            print("accessDimenVariable", globalScope, dimension)
    else:
        #Sí está en currentScope
        dimension = functionsDirectory.getVariableDimension(currentScope, varId)
        dimenSupLim = dimension

        print("accessDimenVariable", currentScope, dimension)

def dimenVariable(p):
    global dimenVar

    # Obtiene variable dimensionada
    dimenVar = p[-2]

def calculateDimen(p):
    global dimenVar
    global dimenSupLim

    # Obtiene index de variable dimensionada
    index = operandsStack.pop()
    # Obtiene el tipo de la variable dimensionada
    indexType = typesStack.pop()

    # Checa si el index es int
    if indexType != 'int':
        errorTypeMismatch(p)
    else:
        # Obtiene el tamaño de la dimensión
        dimenSize = memory.getValueByAddress(index)
        print ('dimenSize', dimenSize)
    
        # Obtiene el limite superior del tamaño de la dimension
        dimenSupLim = dimenSize - 1
        print ('dimenSupLim', dimenSupLim)

def validateIndex(p):
    global quadCounter
    # Obtiene el index de la variable dimensionada
    index = operandsStack.pop()
    # Obtiene el tipo de la variable dimensionada
    indexType = typesStack.pop()
    print memory.memoryBlock[index]
    # Checa si el index es int
    if indexType != 'int':
        errorArgumentsMissmatch(p)
    else:
        # Crea el cuadruplo de VER
        quad = Quadruple(quadCounter, 'VER', index, 0, dimenSupLim)
        # Inserta el cuadruplo a la queue
        quadQueue.enqueue(quad)
        # Incrementa contador
        quadCounter += 1
        # Obtiene la dirección base de la variable dimensionada
        dimenVarBaseAddress = operandsStack.pop()
        # Obtiene el tipo de la variable dimensionada
        dimenVarType = typesStack.pop()
        # Guarda la variable en memoria temporal y obtiene la dirección base
        baseAddress = memory.storeTempToMemory(dimenVarBaseAddress, 'int')
        # Guarda la variable en memoria temporal y obtiene la dirección virtual
        virtualAddress = memory.storeTempToMemory(dimenVarBaseAddress, dimenVarType)

        # Crea el cuadruplo de + después de la verificación
        quad = Quadruple(quadCounter, '+', index, baseAddress, virtualAddress)
        # Inserta el cuadruplo a la queue
        quadQueue.enqueue(quad)
        # Incrementa contador
        quadCounter += 1
        # Inserta la direccion en operandStack
        operandsStack.push([virtualAddress])
        # Inserta el tipo en typeStack
        typesStack.push(dimenVarType)

        print(
        "validateIndex", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand, quad.result),
        "line: " + str(p.lexer.lineno))

def endProgram(p):
    global quadQueue

    # Crea el cuadruplo de END
    quad = Quadruple(quadCounter, "END", None, None, None)
    # Inserta el cuadruplo a la queue
    quadQueue.enqueue(quad)

    print("endProgram", ("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                          quad.result))
    print("Correct Sintax.\n\n")

   

    #Crea Maquina Virtual con quadruplos, bloque de memoria y directorio de funciones
    vm = virtual_Machine(quadQueue, memory, functionsDirectory)

# Funciones de errores
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

# Contruir parser
parser = yacc.yacc()

print("Introduce el nombre del archivo: ")
filename = raw_input()

file = open("./Pruebas/"+str(filename), 'r')

parser.parse(file.read())
