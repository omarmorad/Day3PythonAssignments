import json
import os
import collections


class QueueOutOfRangeException(Exception):
    pass


class NamedSizedQueue:
    _instances={}
    def __init__(self, name, size):
        if not isinstance(size, int) or size <= 0:
            raise ValueError("size must be a positive integer")
        if not isinstance(name, str):
            raise ValueError("name must be a string")
        if name in NamedSizedQueue._instances:
            raise ValueError(f"name must be unique... '{name}'already  exists")
        self.name = name
        self.max_size = size
        self._items = collections.deque()
        NamedSizedQueue._instances[self.name] = self
        print(f"Queue '{self.name}' created with max size {self.max_size}")
    def insert(self, value):
        if len(self._items) >= self.max_size:
            raise QueueOutOfRangeException(f"Queue '{self.name}' is full")
        self._items.append(value)
        print(f"Item '{value}' inserted into queue '{self.name}'")
    def pop(self):
        if self.is_empty():
            print(f"cannot pop from empty queue '{self.name}'")
            return None
        else:
            return self._items.popleft()
    def is_empty(self):
        return len(self._items) == 0
    def is_full(self):
        return len(self._items) == self.max_size
    def __len__(self):
        return len(self._items)
    def __str__(self):
        return f"NamedSizedQueue(name='{self.name}', size={self.max_size}, items={list(self._items)})"
    @classmethod
    def get_queue_by_name(cls,name):
        #return NamedSizedQueue._instances[name] old way
        return NamedSizedQueue._instances.get(name) #better+safer

    @classmethod
    def get_all_queue_names(cls):
        return list(cls._instances.keys())

    @classmethod
    def save(cls,filename="queues_data.json"):
        data_to_save={}
        for name, instance in cls._instances.items():
            data_to_save[name] = {
                "size": instance.max_size,
                "items": list(instance._items)
            }
        try:
            with open(filename,"w") as f:
                json.dump(data_to_save,f,indent=4)
                print(f"Successfully saved state of {len(data_to_save)} queues to '{filename}'.")
        except (IOError, OSError) as e:
            print(f"Error saving state of {len(data_to_save)} queues to '{filename}': {e}")
    #this method is mostly AI i tried to implmemnt in some ways ..didnt work so it doesnt count im leaving it here only for reference
    @classmethod
    def load(cls, filename="queues_data.json"):

        if not os.path.exists(filename):
            print(f"Load file '{filename}' not found. No queues loaded.")
            return False

        try:
            with open(filename, 'r') as f:
                loaded_data = json.load(f)
            cls._instances.clear()
            print("Cleared existing tracked queues.")

            count = 0
            for name, data in loaded_data.items():
                try:
                    if not isinstance(data, dict) or 'size' not in data or 'items' not in data:
                        print(f"Skipping load for queue '{name}' due to invalid data format.")
                        continue
                    if not isinstance(data['items'], list):
                        print(f"Skipping load for queue '{name}' due to invalid items format (expected list).")
                        continue

                    new_queue = cls(name=name, size=data['size'])
                    new_queue._items = collections.deque(data['items'])
                    count += 1
                except ValueError as ve:
                    print(f"Skipping load for queue '{name}' due to error during init: {ve}")
                except KeyError as ke:
                    print(f"Skipping load for queue '{name}' due to missing data field: {ke}")

            print(f"Successfully loaded and recreated {count} queues from '{filename}'.")
            print(f"Currently tracked queues: {cls.get_all_queue_names()}")
            return True

        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading queues from '{filename}': {e}")

            cls._instances.clear()
            return False
        except Exception as e:
            print(f"An unexpected error occurred during loading from '{filename}': {e}")
            cls._instances.clear()
            return False


print("\n--- Testing NamedSizedQueue with JSON Save/Load ---")
try:
    nq1_json = NamedSizedQueue("Tasks_JSON", 3)

    nq2_json = NamedSizedQueue("Messages_JSON", 2)



    nq1_json.insert("Task A")
    nq1_json.insert("Task B")
    nq1_json.insert("Task C")
    nq2_json.insert("Msg 1")
    print(nq1_json)
    print(nq2_json)

    print("\n--- Testing Save/Load (JSON) ---")
    save_filename = "my_queues_data.json"
    NamedSizedQueue.save(save_filename)
    NamedSizedQueue._instances.clear()
    print(f"Manually cleared instances. Tracked queues: {NamedSizedQueue.get_all_queue_names()}")

    NamedSizedQueue.load(save_filename)

    loaded_nq1 = NamedSizedQueue.get_queue_by_name("Tasks_JSON")
    loaded_nq2 = NamedSizedQueue.get_queue_by_name("Messages_JSON")
    print(f"Loaded Queue 1: {loaded_nq1}")
    print(f"Loaded Queue 2: {loaded_nq2}")

    if loaded_nq1:
        print(f"Is loaded queue 1 full? {loaded_nq1.is_full()}")
    if loaded_nq2:
        print(f"Popped from loaded queue 2: {loaded_nq2.pop()}")
        print(f"Loaded Queue 2 after pop: {loaded_nq2}")

    # if os.path.exists(save_filename):
    #     os.remove(save_filename)
    #     print(f"Cleaned up '{save_filename}'.")

except (ValueError, QueueOutOfRangeException) as e:
    print(f"An error occurred: {e}")

print("-" * 25)