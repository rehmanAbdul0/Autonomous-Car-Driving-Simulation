import pygame
import os
import math
import sys
import neat
import time

pygame.init()
# screen size
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 650
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#displaying track 
TRACK = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "track.png")), (SCREEN_WIDTH, SCREEN_HEIGHT))
pop = None  
record_fitness = 0 

# Define the traffic signal and start with green color
rect_pos = (490, 490)
rect_size = (10, 70)
rect_color = (0, 255, 0) 
# timer for traffic signal
start_time = time.time()
color_change_interval = 3
#traffic lights toogle colors
def toggle_color(color):
    # Toggle between red and green
    if color == (255, 0, 0):
        return (0, 255, 0)  # Green
    else:
        return (255, 0, 0)  # Red
    
# Define check points (array of rectangles)
check_points = [
    {'pos': (1000, 460), 'size': (10, 80), 'color': (0, 0, 255)},
    {'pos': (1000, 250), 'size': (120, 10), 'color': (0, 0, 255)},
    {'pos': (800, 110), 'size': (10, 80), 'color': (0, 0, 255)},
    {'pos': (300, 350), 'size': (130, 10), 'color': (0, 0, 255)},
    {'pos': (300, 470), 'size': (10, 80), 'color': (0, 0, 255)},
]
# drawing potholes as black circle
potholes = [
    {'pos': (1020, 325), 'radius': 50, 'color': (0, 0, 0)},
]

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load(os.path.join("Assets", "redcar.png"))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(500, 520))
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0  #move forward
        self.rotation_vel = 5
        self.alive = True
        self.radars = []
        self.car_speed=6
        self.checkpoints_passed = 0
        self.fitness = 0
        self.crossed_checkpoints = set()
        
    #car sensors basic functions calling
    def update(self):
        self.radars.clear()
        self.drive()
        self.rotate()
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.collision()
        self.data()
    
    #speed
    def drive(self):
        self.rect.center += self.vel_vector * self.car_speed

    #detect collision and destroy car
    def collision(self):

        global pop

        #handling checkpoints
        for index, checkpoint in enumerate(check_points):
            checkpoint_rect = pygame.Rect(checkpoint['pos'], checkpoint['size'])
            if self.rect.colliderect(checkpoint_rect) and index not in self.crossed_checkpoints:
                self.crossed_checkpoints.add(index)  # Mark this checkpoint as crossed
                self.checkpoints_passed += 1
                self.fitness += self.checkpoints_passed * 100
            elif not self.rect.colliderect(checkpoint_rect) and index in self.crossed_checkpoints:
                # This allows re-crossing the checkpoint if the car moves away and comes back
                self.crossed_checkpoints.remove(index)

        # Check for pothole collisions
        for pothole in potholes:
            pothole_center_x, pothole_center_y = pothole['pos']
            distance_to_pothole = math.sqrt((self.rect.centerx - pothole_center_x) ** 2 + (self.rect.centery - pothole_center_y) ** 2)
            if distance_to_pothole <= pothole['radius']:
                self.alive = False 

        length = 45 #collosion sensor position
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 18)) * length),
                                 int(self.rect.center[1] - math.sin(math.radians(self.angle + 18)) * length)]
        collision_point_left = [int(self.rect.center[0] + math.cos(math.radians(self.angle - 18)) * length),
                                int(self.rect.center[1] - math.sin(math.radians(self.angle - 18)) * length)]

        # Die on Collision
        if SCREEN.get_at(collision_point_right) == pygame.Color(2, 105, 31, 255) \
                or SCREEN.get_at(collision_point_left) == pygame.Color(2, 105, 31, 255):
            self.alive = False

        # Draw Collision Points
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_right, 4)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_left, 4)
    
    #staring of car handel
    def rotate(self):
        if self.direction == 1: #left
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        if self.direction == -1: #right
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)

    #radars of car detecting obstacles road edges grasses
    def radar(self, radar_angle):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])
        screen_width, screen_height = SCREEN.get_size()  # Get current screen dimensions

        while not SCREEN.get_at((x, y)) == pygame.Color(2, 105, 31, 255) and length < 200:
            length += 1
            x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
            y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)
        
            # Check if x, y are within the screen bounds
            if x < 0 or x >= screen_width or y < 0 or y >= screen_height:
                break  # Exit the loop if out of bounds

        # Check if within the rectangle bounds
            if x >= rect_pos[0] and x <= rect_pos[0] + rect_size[0] and y >= rect_pos[1] and y <= rect_pos[1] + rect_size[1]:
                if rect_color == (255, 0, 0):  
                    self.car_speed=0
                    continue  
                else:
                    self.car_speed=6
                    continue 

                    
            # Check collision with potholes
            for pothole in potholes:
                pothole_center_x, pothole_center_y = pothole['pos']
                distance_to_pothole = math.sqrt((x - pothole_center_x) ** 2 + (y - pothole_center_y) ** 2)
                if distance_to_pothole <= pothole['radius']:
                    # Stop extending the radar line at the edge of the pothole
                    break
            else:
                continue  # Continue while loop if no pothole was detected
            break 
                        

        # Draw Radar
        pygame.draw.line(SCREEN, (255, 255, 255, 255), self.rect.center, (x, y), 1)
        pygame.draw.circle(SCREEN, (0, 255, 0, 0), (x, y), 3)

        dist = int(math.sqrt(math.pow(self.rect.center[0] - x, 2) + math.pow(self.rect.center[1] - y, 2)))
        self.radars.append([radar_angle, dist])

    #collecting data from radar for  input
    def data(self):
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        return input

#to remove specific car 
def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)

# font and style for displaying on window
def display_stats(screen, text, position, font_size=24, color=(0,0,0)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

#main function
def eval_genomes(genomes, config):
    global cars, ge, nets, pop, record_fitness, start_time, rect_color  

    cars = []
    ge = []
    nets = []
    gen_fitness = 0 
    fitness_sum = 0 
    num_cars = len(genomes)

    # Iterate through genomes, initialize cars, neural networks, and set initial fitness.
    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    run = True
    start_time = time.time()  # Start timer for traffic signal color change
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.blit(TRACK, (0, 0))
        #drawing check points
        for point in check_points:
            pygame.draw.rect(SCREEN, point['color'], pygame.Rect(point['pos'], point['size']))
        #drawing potholes
        for pothole in potholes:
            pygame.draw.circle(SCREEN, pothole['color'], pothole['pos'], pothole['radius'])
        #drawing traffic signals
        # Manage the rectangle color toggle based on time
        current_time = time.time()
        if current_time - start_time > color_change_interval:
            rect_color = toggle_color(rect_color)  # Toggle the color
            start_time = current_time  # Reset the timer
        
        pygame.draw.rect(SCREEN, rect_color, (*rect_pos, *rect_size))

        # Drawing and updating of cars and other game elements on window
        display_stats(SCREEN, f"Generation: {pop.generation}", (50, 20))
        display_stats(SCREEN, f"Cars Alive: {len(cars)}", (50, 50))

        #writng to txt file for plotting graph
        if len(cars) == 0:
            avg_fitness = fitness_sum / num_cars if num_cars > 0 else 0
            # Save to file
            with open("generation_fitness.txt", "a") as file:
                file.write(f"Generation: {pop.generation}\n")
                file.write(f"Average Fitness: {avg_fitness:.5f}\n")
                file.write(f"Population Size: {num_cars}\n")
            break
        
        # Reset generation max fitness for each generation
        gen_fitness = 0

        #updating fitness sum 
        for i in range(len(cars)-1, -1, -1):
            car = cars[i].sprite
            if not car.alive:
                fitness_sum += ge[i].fitness  
                remove(i)

        for i, car in enumerate(cars):
            # Check if the car is moving by seeing if its speed is greater than zero
            if car.sprite.vel_vector.length() > 0:
                ge[i].fitness=car.sprite.fitness  # Increment fitness only if the car is moving
                # Update generation max fitness if the current car's fitness is higher
                gen_fitness = max(gen_fitness, ge[i].fitness)
                # Update record_fitness if the current car's fitness is higher
                record_fitness = max(record_fitness, ge[i].fitness)
                # Display the index of the car along with its fitness
                display_stats(SCREEN, f"Car {i+1} Fitness: {ge[i].fitness}", (50, 140 + i*30))
            
            #remove car
            if not car.sprite.alive:
                remove(i)

        # Display generation max fitness
        display_stats(SCREEN, f"Generation max Fitness: {gen_fitness}", (50, 80))
        # Display record fitness
        display_stats(SCREEN, f"Record Fitness: {record_fitness}", (50, 110))


        #set threshhold that will decide based on neurons output
        for i, car in enumerate(cars):
            output = nets[i].activate(car.sprite.data())
            if output[0] > 0.7:
                car.sprite.direction = 1
            if output[1] > 0.7:
                car.sprite.direction = -1
            if output[0] <= 0.7 and output[1] <= 0.7:
                car.sprite.direction = 0

        # Update cars and draw them
        for car in cars:
            car.draw(SCREEN)
            car.update()

        pygame.display.update()

# Setup NEAT Neural Network
def run(config_path):
    global pop

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.run(eval_genomes, 50)

#config file for neat
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)