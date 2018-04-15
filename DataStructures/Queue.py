class Queue:

    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def get(self, index):
        return self.items[index]

    def printQueue(self):
        print("LIST OF QUADRUPLES:")
        i = 0
        while i < len(self.items):
            a = len(self.items) - i - 1
            quad = self.get(a)
            i += 1
            print(("Quad " + str(quad.quad_number), quad.operator, quad.left_operand, quad.right_operand,
                   quad.result))
