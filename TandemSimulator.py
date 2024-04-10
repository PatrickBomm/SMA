import numpy as np


class Queue:
    def __init__(
        self,
        service_interval_range,
        servers,
        capacity,
        id,
        arrival_interval_range=(1, 4),
        next_queue=None,
    ):
        self.service_interval_range = service_interval_range
        self.arrival_interval_range = arrival_interval_range
        self.servers = servers
        self.capacity = capacity
        self.id = id
        self.next_queue = next_queue
        self.queue = []
        self.in_service = []
        self.completed = 0
        self.lost = 0
        self.total_service_time = 0
        self.total_customers_arrived = 0
        self.customer_id = 0
        self.events = []

    def generate_service_time(self):
        return np.random.uniform(*self.service_interval_range)

    def process_arrival(self, time):
        self.customer_id += 1
        if len(self.queue) + len(self.in_service) < self.capacity:
            self.queue.append((self.customer_id, time))
            self.events.append(
                f"Time {time:.2f}: Customer {self.customer_id} arrived at Queue {self.id}"
            )
        else:
            self.lost += 1
            self.events.append(
                f"Time {time:.2f}: Customer {self.customer_id} lost at Queue {self.id}"
            )

    def start_service(self, current_time):
        while len(self.in_service) < self.servers and self.queue:
            customer_id, arrival_time = self.queue.pop(0)
            service_time = self.generate_service_time()
            self.total_service_time += service_time
            departure_time = current_time + service_time
            self.in_service.append((customer_id, departure_time))
            self.events.append(
                f"Time {current_time:.2f}: Customer {customer_id} started service at Queue {self.id}"
            )

    def process_departures(self, current_time):
        for customer in list(self.in_service):
            if customer[1] <= current_time:
                self.in_service.remove(customer)
                self.completed += 1
                self.events.append(
                    f"Time {current_time:.2f}: Customer {customer[0]} completed service at Queue {self.id}"
                )
                if self.next_queue is not None:
                    self.next_queue.process_arrival(customer[1])

    def statistics(self, total_time):
        total_customers = self.completed + self.lost
        percent_lost = (self.lost / total_customers * 100) if total_customers else 0
        percent_completed = (
            (self.completed / total_customers * 100) if total_customers else 0
        )
        average_service_time = (
            (self.total_service_time / self.completed) if self.completed else 0
        )
        return (
            percent_lost,
            percent_completed,
            total_customers,
            total_time,
            average_service_time,
        )


class QueueNetwork:
    def __init__(self, queues):
        self.queues = queues

    def simulate(self, num_events, start_time):
        time = start_time
        self.queues[0].process_arrival(time)
        for _ in range(num_events - 1):
            time += np.random.exponential(
                1
            )
            self.queues[0].process_arrival(time)
            for queue in self.queues:
                queue.start_service(time)
                queue.process_departures(time)
        self.total_time = time

    def save_events_to_file(self, filename):
        with open(filename, "w") as file:
            for queue in self.queues:
                for event in queue.events:
                    file.write(event + "\n")

    def print_statistics(self):
        for queue in self.queues:
            stats = queue.statistics(self.total_time)
            print(f"\nQueue {queue.id} Statistics:")
            print(f"Percent Lost: {stats[0]:.2f}%")
            print(f"Percent Completed: {stats[1]:.2f}%")
            print(f"Total Customers: {stats[2]}")
            print(f"Total Time: {stats[3]:.2f}")
            print(f"Average Service Time: {stats[4]:.2f}")


def configure_queue(id):
    print(f"\nConfiguração da Fila {id}:")
    while True:
        try:
            service_input = (
                input("Informe o intervalo de tempo de serviço (ex: 3 4): ")
                .strip()
                .split()
            )
            if len(service_input) != 2:
                raise ValueError(
                    "É necessário informar dois números para o intervalo de tempo de serviço."
                )
            service_start, service_end = map(float, service_input)
            break  # Sai do loop se a entrada for válida
        except ValueError as e:
            print(f"Erro: {e}. Tente novamente.")

    servers = int(input("Informe o número de servidores: "))
    capacity = int(input("Informe a capacidade da fila: "))
    arrival_input = input(
        "Informe o intervalo de tempo de chegada entre dois valores (ex: 1 4) ou 0 para usar o padrão (1 4): "
    ).strip()
    if arrival_input == "0":
        arrival_interval_range = (1, 4)  # Valores padrão
    else:
        arrival_start, arrival_end = map(float, arrival_input.split())
        arrival_interval_range = (arrival_start, arrival_end)

    return Queue(
        service_interval_range=(service_start, service_end),
        servers=servers,
        capacity=capacity,
        id=id,
        arrival_interval_range=arrival_interval_range,
    )


def main():
    queues = []
    num_queues = int(input("Informe o número de filas na rede: "))
    for i in range(1, num_queues + 1):
        queues.append(configure_queue(i))

    network = QueueNetwork(queues)
    for i in range(num_queues - 1):
        queues[i].next_queue = queues[i + 1]
    num_events = int(input("\nInforme o número de eventos: "))
    start_time = float(input("Informe o tempo de início da simulação: "))

    network.simulate(
        num_events,
        start_time,
    )

    events_file_path = "simulation_events.txt"
    network.save_events_to_file(events_file_path)
    print(f"\nEventos salvos em: {events_file_path}")

    network.print_statistics()


if __name__ == "__main__":
    main()
