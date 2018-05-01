from VariablesTable import vars_Table

class functions_Directory:
    def __init__(self):
        self.functions = {}

    # Insertar funcion en el directorio
    def insertFunction(self, functionName, type, startCuadNumber):
        self.functions[functionName] = {'type': type, 'startQuadNumber':startCuadNumber,
                                        'paramTypes':[], 'paramAddresses': [], 'variables': vars_Table()}

    # Checar si la funcion existe
    def findFunction(self, functionName):
        return self.functions.has_key(functionName)

    # Regresar valor para revisar el tipo de funcion que es
    def getFunctionType(self, functionName):
        function = self.functions[functionName]
        return function['type']

   
    # Regresar el numero de quadruplo de inicio de una funcion
    def getStartQuadNumber(self, functionName):
        function = self.functions[functionName]
        return function['startQuadNumber']

    
    # Guardar el numero de cuadruplo de inicio de una funcion
    def setStartQuadNumber(self, functionName, startQuadNumber):
        if self.findFunction(functionName):
            function = self.functions[functionName]
            function['startQuadNumber'] = startQuadNumber

  
    # Agregar lista de los tipos de los paramatros a un registro de funciones
    def addParameterType(self, functionName, parameterType):
        if self.findFunction(functionName):
            function = self.functions[functionName]
            function['paramTypes'].append(parameterType)

    
    # Agregar lista de direcciones de los parametros a un registro de funciones
    def addParameterAddress(self, functionName, parameterAddress):
        if self.findFunction(functionName):
            function = self.functions[functionName]
            function['paramAddresses'].append(parameterAddress)

   
    # Regresar lista de tipos de los parametros
    def getParameterTypes(self, functionName):
        function = self.functions[functionName]
        return function['paramTypes']

    
    # Regresar lista de las direcciones de los parametros
    def getParameterAddresses(self, functionName):
        function = self.functions[functionName]
        return function['paramAddresses']

    
    # Validar que los tipos de parametros de una llamada de funcion coincidan 
    def validateParameters(self, functionName, argumentTypes):
        function = self.functions[functionName]

        if self.findFunction(functionName):
            return function['paramTypes'] == argumentTypes

   
    # Insertar una variable a la Tabla de variables de una funcion
    def addFunctionVariable(self, functionName, variableName, variableType, address):
        function = self.functions[functionName]

        if function['variables'].findVariable(variableName):
            return False
        else:
            function['variables'].insertVariable(variableName, variableType, address)
            return True

    
    # Regresar variable de una Tabla de variables de una funcion
    def getFunctionVariable(self, functionName, variableName):
        function = self.functions[functionName]
        variables = function["variables"]

        variable = variables.get(variableName)

        return variable

    
    # Buscar una direcion virtual y regresar el id en caso de que exista
    def getFunctionIdByAddress(self, scope, virtualAddress):
        function = self.functions[scope]
        return function['variables'].getIdByAddress(virtualAddress)

   
    # Agregar dimension a una variable
    def addDimensionToVariable(self, functionName, variableName, dimension):
        function = self.functions[functionName]
        function['variables'].addDimension(variableName, dimension)

    
    # Regresar dimension de una variable
    def getVariableDimension(self, functionName, variableName):
        function = self.functions[functionName]
        return function['variables'].getDimension(variableName)
