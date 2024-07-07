import threading, queue, time

class Table:
    def __init__(self, number=int):
        self.number = number
        self.is_busy = False

class Cafe:
    def __init__(self, tables):
        self.queue = queue.Queue()
        self.tables = tables
        self.active_customers = 0
        self.all_customers_served = threading.Event()

    def customer_arrival(self):
        for customer in range(1, 21):
            print(f'Посетитель номер {customer} прибыл')
            self.active_customers += 1
            cus = Customer(customer, self)
            cus.start()
            time.sleep(1)

    def serve_customer(self, customer):
        if len(self.tables) == 0:
            print(f'Посетитель номер {customer.number} ожидает свободный стол')
            self.queue.put(customer)
            return

        table = self.tables.pop(0)
        print(f'Посетитель номер {customer.number} сел за стол {table.number}')
        time.sleep(5)
        print(f'Посетитель номер {customer.number} покушал и ушёл')
        self.tables.append(table)

        self.active_customers -= 1
        if self.active_customers == 0:
            self.all_customers_served.set()

        if not self.queue.empty():
            next_customer = self.queue.get()
            self.serve_customer(next_customer)

class Customer(threading.Thread):
    def __init__(self, number, cafe):
        super().__init__()
        self.number = number
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self)

table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]
cafe = Cafe(tables)

customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

customer_arrival_thread.join()
cafe.all_customers_served.wait()