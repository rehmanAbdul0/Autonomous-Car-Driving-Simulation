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

# Create a DataFrame from the extracted data for the average fitness plot
fitness_data = pd.DataFrame({
    'Generation': generations,
    'Average Fitness': fitness_values
})

# Plotting the average fitness per generation
plt.figure(figsize=(10, 5))
plt.bar(fitness_data['Generation'], fitness_data['Average Fitness'], color='blue')
plt.xlabel('Generation Number')
plt.ylabel('Average Fitness')
plt.title('Average Fitness Per Generation')
plt.xticks(fitness_data['Generation'])  # Ensure all generation numbers appear on x-axis
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

# Plotting the ratio as a single bar
plt.figure(figsize=(5, 5))
plt.bar('Ratio', ratio, color='green')  # Plotting the ratio as a single bar
plt.ylabel('Ratio of Total Average Fitness to Total Population Size')
plt.title('Ratio of Total Average Fitness to Total Population Size')
plt.text(0, ratio, f'Gen 0 Pop Size: {first_population_size}', va='bottom', ha='center')  # Display Gen 0 pop size
plt.tight_layout()
plt.show()
