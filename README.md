# Autonomous Car Driving Simulation

## Overview
This project is a self-driving car simulation using **Pygame** and **NEAT (NeuroEvolution of Augmenting Topologies)**. The AI learns to navigate a track, avoiding obstacles and obeying traffic rules through evolutionary reinforcement learning.

## Features
- **AI-controlled car** that learns through genetic algorithms
- **Track with checkpoints** to guide the vehicle
- **Traffic signal system** that switches colors every 3 seconds
- **Obstacle detection** including potholes on the road
- **Graphical analysis** of AI performance over generations

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Required Python libraries:
  ```sh
  pip install pygame neat-python matplotlib pandas
  ```

### Running the Simulation
1. Clone the repository or extract the zip file.
2. Navigate to the project directory.
3. Run the simulation:
   ```sh
   python main.py
   ```

### Viewing Performance Graphs
To visualize the AI's fitness progression:
```sh
python graph.py
```

## File Structure
```
📁 Autonomous Car Driving Simulation
│── main.py                  # Runs the simulation
│── graph.py                 # Generates fitness graphs
│── config.txt               # NEAT configuration file
│── generation_fitness.txt   # Logs AI performance over generations
│── Assets/                  # Contains images for the car and track
│── REPORT/                  # Includes project report and flowchart
```

## How It Works
1. **Neural Network Training**: The AI cars start with random behaviors and evolve through multiple generations.
2. **Fitness Function**: The car's performance is measured based on how far it progresses on the track.
3. **Selection & Mutation**: The best-performing cars pass their traits to the next generation.
4. **Graph Analysis**: The `graph.py` script helps analyze performance trends.

## Author
Developed as part of the **Autonomous Driving Simulation Project**.

## License
This project is for educational purposes and research only.

