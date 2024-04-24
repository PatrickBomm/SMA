import numpy as np
from tabulate import tabulate

def calculate_results(data_list, capacity):
    """
    Calculates the results of the simulation based on the data list and capacity.

    Parameters:
        data_list (list): List of simulation data.
        capacity (int): Capacity of the queue.

    Returns:
        list: List of calculated results.
    """
    # Set numpy printing options
    np.set_printoptions(precision=4, suppress=True)

    # Convert the data list into a numpy array
    data_array = np.array(data_list)

    # Calculate the column means
    column_means = np.mean(data_array, axis=0)

    # Initialize the list to store the results
    results = []

    # Iterate over the capacity plus one
    for i in range(capacity + 1):
        # Calculate the result for each state
        result = [i, column_means[i + 1], (column_means[i + 1] / column_means[0]) * 100]
        results.append(result)

    # Add the total result
    results.append(['TOTAL', column_means[0], 100])

    return results

def create_seeds(seed, n):
    """
    Creates a list of seeds based on the initial seed and the number of seeds required.

    Parameters:
        seed (float): Initial seed value.
        n (int): Number of seeds to generate.

    Returns:
        list: List of generated seeds.
    """
    seeds = []
    for i in range(n):
        seeds.append(seed)
        seed = (seed * 5) % 1
    return seeds

def calculate_auxiliary_result(data_list, capacity):
    """
    Calculates auxiliary results based on the simulation data list and capacity.

    Parameters:
        data_list (list): List of simulation data.
        capacity (int): Capacity of the queue.

    Returns:
        list: List of calculated auxiliary results.
    """
    results = []
    for i in range(capacity + 1):
        result = [i, data_list[-1][i + 1], (data_list[-1][i + 1] / data_list[-1][0]) * 100]
        results.append(result)

    # Add the total result
    results.append(['TOTAL', data_list[-1][0], 100])

    return results

def write_result_1(results, file_name):
    """
    Writes the results to a file in a formatted manner.

    Parameters:
        results (list): List of results to write.
        file_name (str): Name of the file to write to.
    """
    with open(file_name, 'w') as file:
        for i, result in enumerate(results):
            # Write the queue number
            file.write('Queue ' + str(i + 1) + '\n')
            # Write the formatted results
            file.write(tabulate(result, headers=['State', 'Accumulated Time', 'Probability (%)']) + '\n\n')

def write_result_2(results, file_name):
    """
    Writes the results to a file in a formatted manner.

    Parameters:
        results (list): List of results to write.
        file_name (str): Name of the file to write to.
    """
    with open(file_name, 'w') as file:
        for i, result in enumerate(results):
            # Write the queue number
            file.write('Queue ' + str(i + 1) + '\n')
            # Write the formatted results
            file.write(str(tabulate(result)) + '\n')
        # Add a newline at the end of the file
        file.write('\n')
