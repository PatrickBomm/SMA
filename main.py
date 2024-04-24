from tandemQueue import TandemQueue
from utils import calculate_results, create_seeds, write_result_1, write_result_2

# Prompt the user to input simulation configurations
config = {
    'fila_1_arrival_limits': list(map(int, input("Enter arrival limits for queue 1 [min, max]: ").split(','))),
    'fila_1_serv_limits': list(map(int, input("Enter service limits for queue 1 [min, max]: ").split(','))),
    'fila_2_serv_limits': list(map(int, input("Enter service limits for queue 2 [min, max]: ").split(','))),
    'fila_1_serv': int(input("Enter number of servers in queue 1: ")),
    'fila_1_cap': int(input("Enter capacity of queue 1: ")),
    'fila_2_serv': int(input("Enter number of servers in queue 2: ")),
    'fila_2_cap': int(input("Enter capacity of queue 2: "))
}

# List of seeds for simulation
seeds = [0.9920, 0.0001, 0.5530, 0.2760, 0.3397]

# Lists to store simulation results
fila_1_simu = []
fila_2_simu = []

simulation_number = int(input("Enter simulation number: "))
# Loop over each seed to execute simulations
for seed in seeds:
    # Generate a list of seeds based on the current seed
    seeds_list = create_seeds(seed, simulation_number)
    # Update seeds in the configurations
    config['seeds'] = seeds_list
    # Initialize the tandem queue simulation with the configurations
    tandem_queue = TandemQueue(config)
    # Execute the simulation and store the final states of the queues
    states_1, states_2 = tandem_queue.scheduler(2.5000)
    fila_1_simu.append(states_1[3:])
    fila_2_simu.append(states_2[3:])

# Calculate the results of the simulations
result1 = calculate_results(fila_1_simu, config['fila_1_cap'])
result2 = calculate_results(fila_2_simu, config['fila_2_cap'])

# Write the results of the queue states to a file
write_result_2([fila_1_simu, fila_2_simu], 'state_results.txt')
# Write the summarized results to a file
write_result_1([result1, result2], 'results.txt')

print('Results on files: results.txt | state_results.txt')