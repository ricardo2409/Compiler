import sys

class memory_Block:
    def __init__(self):
        self.memoryBlock = {}
        # Contador de variables, constantes y temporales
        self.varCounter = 0
        self.constCounter = 0
        self.tempCounter = 0
        # Tipos de Variables
        self.intVarCounter = 0
        self.floatVarCounter = 0
        self.boolVarCounter = 0
        self.stringVarCounter = 0
        # Tipos de constantes
        self.intConstCounter = 0
        self.floatConstCounter = 0
        self.boolConstCounter = 0
        self.stringConstCounter = 0
        # Tipos de Temporales
        self.intTempCounter = 0
        self.floatTempCounter = 0
        self.boolTempCounter = 0
        self.stringTempCounter = 0

    # Segmentos de Memoria
    VarStart = 0
    ConstStart = 2000
    TempStart = 4000
    MemorySize = 6000

    def storeVariableToMemory(self, value, type):
        if (self.VarStart + self.varCounter) < self.ConstStart:
            intStart = self.VarStart
            floatStart = self.VarStart + 500
            boolStart = self.VarStart + 1000
            stringStart = self.VarStart + 1500

            if type == 'int':
                if self.varCounter < floatStart:
                    self.varCounter += 1
                    self.intVarCounter += 1
                    virtualAddress = intStart + (self.intVarCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de Integers llena')
                    return None
            elif type == 'float':
                if self.varCounter < boolStart:
                    self.varCounter += 1
                    self.floatVarCounter += 1
                    virtualAddress = floatStart + (self.floatVarCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de Floats llena')
                    return None
            elif type == 'bool':
                if self.varCounter < stringStart:
                    self.varCounter += 1
                    self.boolVarCounter += 1
                    virtualAddress = boolStart + (self.boolVarCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de Boolean llena')
                    return None
            elif type == 'string':
                if self.varCounter < self.ConstStart:
                    self.varCounter += 1
                    self.stringVarCounter += 1
                    virtualAddress = stringStart + (self.stringVarCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de String llena')
                    return None


    def storeConstantToMemory(self, value, type):
        if (self.ConstStart + self.constCounter) < self.TempStart:
            intStart = self.ConstStart
            floatStart = self.ConstStart + 500
            boolStart = self.ConstStart + 1000
            stringStart = self.ConstStart + 1500

            if type == 'int':
                if self.constCounter < floatStart:
                    self.constCounter += 1
                    self.intConstCounter += 1
                    virtualAddress = intStart + (self.intConstCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de Integers Constante llena')
                    return None
            elif type == 'float':
                if self.constCounter < boolStart:
                    self.constCounter += 1
                    self.floatConstCounter += 1
                    virtualAddress = floatStart + (self.floatConstCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de Float Constante llena')
                    return None
            elif type == 'bool':
                if self.constCounter < stringStart:
                    self.constCounter += 1
                    self.boolConstCounter += 1
                    virtualAddress = boolStart + (self.boolConstCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de Boolean Constante llena')
                    return None
            elif type == 'string':
                if self.constCounter < self.TempStart:
                    self.constCounter += 1
                    self.stringConstCounter += 1
                    virtualAddress = stringStart + (self.stringConstCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de String Constante llena')
                    return None

    def storeTempToMemory(self, value, type):
        if (self.TempStart + self.tempCounter) < self.MemorySize:
            intStart = self.TempStart
            floatStart = self.TempStart + 500
            boolStart = self.TempStart + 1000
            stringStart = self.TempStart + 1500

            if type == 'int':
                if self.tempCounter < floatStart:
                    self.tempCounter += 1
                    self.intTempCounter += 1
                    virtualAddress = intStart + (self.intTempCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de Integers Temporal llena')
                    return None
            elif type == 'float':
                if self.tempCounter < boolStart:
                    self.tempCounter += 1
                    self.floatTempCounter += 1
                    virtualAddress = floatStart + (self.floatTempCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de Float Temporal llena')
                    return None
            elif type == 'bool':
                if self.tempCounter < stringStart:
                    self.tempCounter += 1
                    self.boolTempCounter += 1
                    virtualAddress = boolStart + (self.boolTempCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de Boolean Temporal llena')
                    return None
            elif type == 'string':
                if self.tempCounter < self.MemorySize:
                    self.tempCounter += 1
                    self.stringTempCounter += 1
                    virtualAddress = stringStart + (self.stringTempCounter - 1)
                    self.memoryBlock[virtualAddress] = value
                    return virtualAddress
                else:
                    print('Memoria de String Temporal llena')
                    return None

    def storeDimensionVarToMemory(self, value, type, dimension):
        baseAddress = self.storeVariableToMemory(value, type)
        for i in range(0, dimension):
            trash = self.storeVariableToMemory(value, type)
        return baseAddress

    def storeDimensionTempToMemory(self, value, type, dimension):
        baseAddress = self.storeTempToMemory(value, type)
        for i in range(0, dimension):
            trash = self.storeTempToMemory(value, type)
        return baseAddress

    def storeDimensionConstToMemory(self, value, type, dimension):
        baseAddress = self.storeConstantToMemory(value, type)
        for i in range(0, dimension):
            trash = self.storeConstantToMemory(value, type)
        return baseAddress

    def getValueByAddress(self, virtualAddress):
        if self.memoryBlock.has_key(virtualAddress):
            return self.memoryBlock[virtualAddress]
        else:
            print 'Address is empty'

    def modifyValueByAddress(self, virtualAddress, value):
        if self.memoryBlock.has_key(virtualAddress):
            self.memoryBlock[virtualAddress] = value
        else:
            print 'Address is empty'

    def deleteValueByAddress(self, virtualAddress):
        if self.memoryBlock.has_key(virtualAddress):
            del self.memoryBlock[virtualAddress]
        else:
            print 'Address is empty'

    def clearMemory(self):
        self.varCounter = 0
        self.constCounter = 0
        self.tempCounter = 0
        # VarsTypes
        self.intVarCounter = 0
        self.floatVarCounter = 0
        self.boolVarCounter = 0
        self.stringVarCounter = 0
        # ConstTypes
        self.intConstCounter = 0
        self.floatConstCounter = 0
        self.boolConstCounter = 0
        self.stringConstCounter = 0
        # TempTypes
        self.intTempCounter = 0
        self.floatTempCounter = 0
        self.boolTempCounter = 0
        self.stringTempCounter = 0

    def clearTempMemory(self):
        # TempTypes
        self.intTempCounter = 0
        self.floatTempCounter = 0
        self.boolTempCounter = 0
        self.stringTempCounter = 0
        self.tempCounter = 0