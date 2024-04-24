class TandemQueue:
    def __init__(self, settings) -> None:
        """
        Initialize the Tandem Queue simulation with the given settings.

        Args:
            settings (dict): A dictionary containing simulation settings.
        """
        self.queue1 = 0
        self.queue2 = 0
        self.current_time = 0.0
        self.arrival_limits_queue1 = settings["fila_1_arrival_limits"]
        self.service_limits_queue1 = settings["fila_1_serv_limits"]
        self.service_limits_queue2 = settings["fila_2_serv_limits"]
        self.seeds = settings["seeds"]
        self.current_seed_index = 0
        self.capacity_queue1 = settings["fila_1_cap"]
        self.capacity_queue2 = settings["fila_2_cap"]
        self.servers_queue1 = settings["fila_1_serv"]
        self.servers_queue2 = settings["fila_2_serv"]

    def scheduler(self, start_time):
        """
        Run the scheduler to simulate the tandem queue system.

        Args:
            start_time (float): The start time of the simulation.

        Returns:
            tuple: A tuple containing the final states of queue 1 and queue 2.
        """
        self.event_queue = []
        self.state_log_queue1 = []
        self.state_log_queue2 = []

        # Initialize state arrays for each queue
        initial_state_queue1 = [None, self.queue1, self.queue2, self.current_time] + [
            0.0
        ] * (self.capacity_queue1 + 1)
        initial_state_queue2 = [None, self.queue1, self.queue2, self.current_time] + [
            0.0
        ] * (self.capacity_queue2 + 1)
        self.state_log_queue1.append(initial_state_queue1)
        self.state_log_queue2.append(initial_state_queue2)

        # Add initial event without randomization
        self.event_queue.append(["ARR1", start_time, 0.0])
        while self.current_seed_index < len(self.seeds):
            self.event_queue.sort(key=lambda x: x[1])
            current_event = self.event_queue.pop(0)
            previous_time = self.current_time
            self.current_time = current_event[1]

            self.handle_event(current_event)
            self.update_state(current_event, previous_time)

        return self.state_log_queue1[-1], self.state_log_queue2[-1]

    def handle_event(self, event):
        """
        Handle events in the tandem queue simulation.

        Args:
            event (list): A list representing the current event.
        """
        event_type = event[0]
        if event_type == "ARR1":
            self.handle_arrival_queue1()
        elif event_type == "SERV2":
            self.handle_service_queue2()
        elif event_type == "PASS1to2":
            self.handle_passage_queue1_to_queue2()

    def handle_arrival_queue1(self):
        """
        Handle arrival events in queue 1.
        """
        if self.queue1 < self.capacity_queue1:
            self.queue1 += 1
            if self.queue1 <= self.servers_queue1:
                self.schedule_event(
                    "PASS1to2", self.current_time, self.service_limits_queue1
                )
        self.schedule_event("ARR1", self.current_time, self.arrival_limits_queue1)

    def handle_service_queue2(self):
        """
        Handle service events in queue 2.
        """
        self.queue2 -= 1
        if self.queue2 > 0:
            self.schedule_event("SERV2", self.current_time, self.service_limits_queue2)

    def handle_passage_queue1_to_queue2(self):
        """
        Handle passage events from queue 1 to queue 2.
        """
        self.queue1 -= 1
        if self.queue1 >= self.servers_queue1:
            self.schedule_event(
                "PASS1to2", self.current_time, self.service_limits_queue1
            )
        if self.queue2 < self.capacity_queue2:
            self.queue2 += 1
            if self.queue2 <= self.servers_queue2:
                self.schedule_event(
                    "SERV2", self.current_time, self.service_limits_queue2
                )

    def update_state(self, event, previous_time):
        """
        Update the state of the queues based on the current event.

        Args:
            event (list): A list representing the current event.
            previous_time (float): The previous time in the simulation.
        """
        self.update_state_for_queue(
            self.state_log_queue1, event, previous_time, self.queue1
        )
        self.update_state_for_queue(
            self.state_log_queue2, event, previous_time, self.queue2
        )

    def update_state_for_queue(self, log, event, previous_time, queue_size):
        """
        Update the state of a specific queue based on the current event.

        Args:
            log (list): A list representing the state log of the queue.
            event (list): A list representing the current event.
            previous_time (float): The previous time in the simulation.
            queue_size (int): The size of the queue.
        """
        last_state = log[-1]
        new_state = last_state.copy()
        new_state[0] = event[0]
        new_state[1] = self.queue1
        new_state[2] = self.queue2
        new_state[3] = self.current_time

        time_difference = self.current_time - previous_time
        new_state[4 + queue_size] += time_difference
        log.append(new_state)

    def schedule_event(self, event_type, current_time, limits):
        """
        Schedule a new event in the event queue.

        Args:
            event_type (str): The type of event to schedule.
            current_time (float): The current time in the simulation.
            limits (list): The limits for the event duration.
        """
        duration = self.draw_random(limits)
        new_event = [event_type, current_time + duration, duration]
        self.event_queue.append(new_event)

    def draw_random(self, limits):
        """
        Draw a random number within the given limits.

        Args:
            limits (list): The limits for the random number.

        Returns:
            float: A random number within the specified limits.
        """
        if self.current_seed_index == len(self.seeds):
            return 0
        self.current_seed_index += 1
        return (limits[1] - limits[0]) * self.seeds[
            self.current_seed_index - 1
        ] + limits[0]
