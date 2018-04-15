from VariablesTable import vars_Table

class functions_Directory:
    def __init__(self):
        self.functions = {}

    # Insert function to the directory
    def insertFunction(self, functionName, type, startCuadNumber):
        self.functions[functionName] = {'type': type, 'startQuadNumber':startCuadNumber,
                                        'paramTypes':[], 'paramAddresses': [], 'variables': vars_Table()}

    # check if function exists
    def lookupFunction(self, functionName):
        return self.functions.has_key(functionName)

    # Return the type of a function
    def getFunctionType(self, functionName):
        function = self.functions[functionName]
        return function['type']

    # Return the starting quad number of a function
    def getStartQuadNumber(self, functionName):
        function = self.functions[functionName]
        return function['startQuadNumber']

    # Save the starting quad number of a function
    def setStartQuadNumber(self, functionName, startQuadNumber):
        if self.lookupFunction(functionName):
            function = self.functions[functionName]
            function['startQuadNumber'] = startQuadNumber

    # Add list of parameter types to a function record
    def addParameterType(self, functionName, parameterType):
        if self.lookupFunction(functionName):
            function = self.functions[functionName]
            function['paramTypes'].append(parameterType)

    # Add list of parameter addresses to a function record
    def addParameterAddress(self, functionName, parameterAddress):
        if self.lookupFunction(functionName):
            function = self.functions[functionName]
            function['paramAddresses'].append(parameterAddress)

    # Return list of parameter types
    def getParameterTypes(self, functionName):
        function = self.functions[functionName]
        return function['paramTypes']

    # Return list of parameter addresses
    def getParameterAddresses(self, functionName):
        function = self.functions[functionName]
        return function['paramAddresses']

    # Validate parameters types match from functioncall
    def validateParameters(self, functionName, argumentTypes):
        function = self.functions[functionName]

        if self.lookupFunction(functionName):
            return function['paramTypes'] == argumentTypes

    # Insert variable to the VarsTable of a function
    def addFunctionVariable(self, functionName, variableName, variableType, address):
        function = self.functions[functionName]

        if function['variables'].lookupVariable(variableName):
            return False
        else:
            function['variables'].insertVariable(variableName, variableType, address)
            return True

    # Return variable from a VarsTable of a function
    def getFunctionVariable(self, functionName, variableName):
        function = self.functions[functionName]
        variables = function["variables"]

        variable = variables.get(variableName)

        return variable

    # Search by virtual address and return id if exists
    def getFunctionIdByAddress(self, scope, virtualAddress):
        function = self.functions[scope]
        return function['variables'].getIdByAddress(virtualAddress)

    # Add dimension to a variable
    def addDimensionToVariable(self, functionName, variableName, dimension):
        function = self.functions[functionName]
        function['variables'].addDimension(variableName, dimension)

    # Return dimension from a variable
    def getVariableDimension(self, functionName, variableName):
        function = self.functions[functionName]
        return function['variables'].getDimension(variableName)
