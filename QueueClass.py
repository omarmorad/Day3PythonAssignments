import collections


class Queue:
    def __init__(self):
        self._items = []
        print("Queue Created")

    def insert(self, value):
        self._items.append(value)
        print("Item Inserted")

    def pop(self):
        if self.is_empty():
            print("Warning ...Queue is Empty")
            return None
        else:
            return self._items.pop(0)

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __str__(self):
        return str(self._items)

print("testing queue")
q1 = Queue()
print(f"Is empty? {q1.is_empty()}")
q1.insert(10)
q1.insert(20)
q1.insert(30)
print(q1)
print(f"Is empty? {q1.is_empty()}")
print(f"Length: {len(q1)}")
print(f"Popped: {q1.pop()}")
print(f"Popped: {q1.pop()}")
print(q1)
print(f"Popped: {q1.pop()}")
print(f"Is empty? {q1.is_empty()}")
print(f"Popped from empty: {q1.pop()}")
print("-" * 25)