import pandas as pd
import matplotlib.pyplot as plt

# Define the path to the text file
file_path = 'generation_fitness.txt'

# Initialize lists to store data
generations = []
fitness_values = []
population_sizes = []
first_population_size = None  # To store the population size of the first generation

# Read from the file
with open(file_path, 'r') as file:
    lines = file.readlines()

    # Process each line to extract generation, fitness, and population size data
    for line in lines:
        if 'Generation:' in line:
            generation = int(line.split(':')[1].strip())
            generations.append(generation)
        elif 'Average Fitness:' in line:
            fitness = float(line.split(':')[1].strip())
            fitness_values.append(fitness)
        elif 'Population Size:' in line:
            population_size = int(line.split(':')[1].strip())
            population_sizes.append(population_size)
            if first_population_size is None:  # Only set for the first generation
                first_population_size = population_size

# Calculate the total average fitness and total population size
total_fitness = sum(fitness_values)
total_population = sum(population_sizes)

# Calculate the ratio
ratio = total_fitness / total_population

# Extending generation data for ratio bar, converting all to strings for compatibility
extended_generations = [str(g) for g in generations] + ["Performance"]

# Extending fitness values with the ratio
extended_fitness_values = fitness_values + [ratio]

# Plotting both the average fitness per generation and the ratio on the same plot
plt.figure(figsize=(12, 6))
plt.bar(extended_generations, extended_fitness_values, color=['blue']*len(generations) + ['green'])
plt.xlabel('Generation Number')
plt.ylabel('Average Fitness')
plt.title('Average Fitness Per Generation with Performance Ratio')
plt.xticks(extended_generations)  # Ensure all generation numbers and "Performance" label appear on x-axis
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Clearing the contents of the text file after plotting
with open(file_path, 'w') as file:
    pass  # Open the file in write mode to clear it
