class vars_Table:
    def __init__(self):
        self.variables = {}

   
    # Insertar nueva variable a la tabla
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

    
    # Checar si la variable existe
    def findVariable(self, name):
        return self.variables.has_key(name)

    
    # Regresar el valor de la variable
    def get(self, name):
        if self.variables.has_key(name):
            return (name, self.variables[name])
        else:
            return None

    
    # Buscar por direccion virtual y retornar id en caso de que exista
    def getIdByAddress(self, virtualAddress):
        for variable in self.variables:
            variableInfo = self.variables[variable]
            if virtualAddress in variableInfo:
                return variable
