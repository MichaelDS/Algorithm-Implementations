

class Queue(object):
    def __init__(self, arr = []):
        self.in_stack = []
        self.out_stack = list(reversed(arr))
    def enqueue(self, x):
        self.in_stack.append(x)
    def dequeue(self):
        if not self.out_stack:
            self.out_stack = self.in_stack
            self.in_stack = []
            self.out_stack.reverse()
        return self.out_stack.pop()
    def isEmpty(self):
        return not (self.in_stack or self.out_stack)
    def __str__(self):
        return str(list(reversed(self.in_stack)) + self.out_stack)
