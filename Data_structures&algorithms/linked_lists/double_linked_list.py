class Node:
    def __init__(self, data=None, nxt=None, prev=None):
        self.data = data
        self.next = nxt
        self.prev = prev


class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def print_forward(self):
        if self.head is None:
            print("Linked list is empty")
            return
        itr = self.head
        llstr = ''
        while itr:
            llstr += str(itr.data) + ' --> ' if itr.next else str(itr.data)
            itr = itr.next
        print(llstr)

    def print_backward(self):
        if self.tail is None:
            print("Linked list is empty")
            return
        itr = self.tail
        llstr = ''
        while itr:
            llstr += str(itr.data) + ' --> ' if itr.prev else str(itr.data)
            itr = itr.prev
        print(llstr)

    def get_length(self):
        count = 0
        itr = self.head
        while itr:
            count += 1
            itr = itr.next

        return count

    def insert_at_beginning(self, data):
        if self.tail is None:
            self.tail = self.head = Node(data)
        node = Node(data, self.head)
        self.head.prev = node
        self.head = node

    def insert_at_end(self, data):
        if self.head is None:
            self.head = self.tail = Node(data)
            return
        node = Node(data, prev=self.tail)
        self.tail.next = node
        self.tail = node

    def insert_at(self, index, data):
        length = self.get_length()
        if index < 0 or index > length:
            raise Exception("Invalid Index")

        if index == 0:
            self.insert_at_beginning(data)
            return
        if index == length:
            self.insert_at_end(data)
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                node = Node(data, itr.next, itr)
                itr.next.prev = node
                itr.next = node
                break

            itr = itr.next
            count += 1

    def remove_at(self, index):
        if index < 0 or index >= self.get_length():
            raise Exception("Invalid Index")

        if index == 0:
            self.head = self.head.next
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                itr.next = itr.next.next
                itr.next.prev = itr
                break

            itr = itr.next
            count += 1

    def insert_values(self, data_list):
        self.head = None
        for data in data_list:
            self.insert_at_end(data)

    def insert_after_value(self, data_prev, data_to_insert):
        if self.head is None:
            return

        itr = self.head
        while itr:
            if itr.data == data_prev:
                node = Node(data_to_insert, itr.next, itr)
                itr.next.prev = node
                itr.next = node
                return
            itr = itr.next
        raise Exception("Value not in list")

    def remove_by_value(self, data):
        if self.head is None:
            return

        itr = self.head
        if itr.data == data:
            self.head = itr.next
            return
        while itr.next:
            if itr.next.data == data:
                itr.next.next.prev = itr
                itr.next = itr.next.next
                return
            itr = itr.next
        raise Exception("Value not in list")


if __name__ == '__main__':
    ll = DoubleLinkedList()
    ll.insert_values(["banana", "mango", "grapes", "orange"])
    ll.insert_at_end("figs")
    ll.insert_at(0, "jackfruit")
    ll.insert_after_value("orange", "kiwi")
    ll.print_forward()
    ll.print_backward()
    ll.insert_after_value("mango", "apple")
    ll.print_forward()
    ll.print_backward()
    ll.remove_by_value("orange")
    ll.print_forward()
    ll.print_backward()
