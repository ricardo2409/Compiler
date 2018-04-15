import ply.yacc as yacc
import sys

sys.path.append("..")

from scanner import tokens
from DataStructures.FunctionsDirectory import functions_Directory
from DataStructures.Stack import Stack
from DataStructures.VariablesTable import vars_Table
from DataStructures.Quadruple import Quadruple
from DataStructures.Queue import Queue
from SemanticCube.SemanticCube import semantic_Cube
from Memory.Memory import memory_Block
from VirtualMachine.VirtualMachine import virtual_Machine
#-----------------------------------------------------------------

# Directories
functionsDirectory = functions_Directory()
semanticCube = semantic_Cube()
funcReturn = {}

# Memory
memory = memory_Block()

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