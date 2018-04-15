class vars_Table:
    def __init__(self):
        self.variables = {}

    # Insert new variable to the table
    def insertVariable(self, name, type, virtualAddress):
        self.variables[name] = [type, virtualAddress]

    def addDimension(self, name, dimension):
        self.variables[name].append({'dimension': dimension})

    def getDimension(self, name):
        if len(self.variables[name]) > 2:
            variable = self.variables[name]
            varAux = variable[2]
            return varAux['dimension']
        else:
            return None

    # Check if variable exists
    def lookupVariable(self, name):
        return self.variables.has_key(name)

    # Return variable's values
    def get(self, name):
        if self.variables.has_key(name):
            return (name, self.variables[name])
        else:
            return None

    # Search by virtual address and return id if exists
    def getIdByAddress(self, virtualAddress):
        for variable in self.variables:
            variableInfo = self.variables[variable]
            if virtualAddress in variableInfo:
                return variable
