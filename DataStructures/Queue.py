from Memory.Memory import memory_Block

memory = memory_Block()
class Queue:

    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def get(self, index):
        return self.items[index]

    def printQueue(self):
        print '\n'
        print("Cuadruplos:")
        i = 0
        while i < len(self.items):
            a = len(self.items) - i - 1
            quad = self.get(a)
            i += 1
            if quad.left_operand is not None:
                print(("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                   quad.result))
            else:
                print(("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                   quad.result))


    def isEmpty(self):
        return self.items == []
