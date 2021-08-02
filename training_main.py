from __future__ import absolute_import
from __future__ import print_function

import os
import datetime
from shutil import copyfile

from simulation_while_training import Simulation
from generator import TrafficGenerator
from memory import Memory
from model import TrainModel
from visualization import Visualization
from utils import import_train_configuration, set_sumo, set_train_path


if __name__ == "__main__":

    config = import_train_configuration(config_file='training_settings.ini')    
    sumo_cmd = set_sumo(False, 'sumo_config.sumocfg', 5400)
    path = set_train_path('models')

    Model = TrainModel(
        config['num_layers'], 
        config['width_layers'], 
        config['batch_size'], 
        config['learning_rate'], 
        input_dim= config['num_states'],               #num of states
        output_dim=config['num_actions']                #num of actions
    )

    TrafficGen = TrafficGenerator(
        config['max_steps'],            #max steps
        config['n_cars_generated']      #n cars generated
    )
        
    Simulation = Simulation(
        Model,
        Memory,
        TrafficGen,
        sumo_cmd,
        config['gamma'],            #gamma value
        config['max_steps'],        #max steps during simulation
        config['green_duration'],   #green duration
        config['yellow_duration'],
        config['num_states'],
        config['num_actions'],
        config['training_epochs']
    )

    Visualization = Visualization(path, dpi= 96)
    
    Memory =Memory(
        config['memory_size_max'],
        config['memory_size_min']
        )
    
    episode = 0
    timestamp_start = datetime.datetime.now()
    
    while episode < config['total_episodes']:
        print('\n     Episode', str(episode+1), 'of 100')
        epsilon = 1.0 - (episode / 100)  # set the epsilon for this episode according to epsilon-greedy policy
        simulation_time, training_time = Simulation.run(episode, epsilon)  # run the simulation
        print('Simulation time:', simulation_time, 's - Training time:', training_time, 's - Total:', round(simulation_time+training_time, 1), 's')
        episode += 1

    print("\n----- Start time:", timestamp_start)
    print("----- End time:", datetime.datetime.now())
    print("----- Session info saved at:", path)

    Model.save_model(path)

    
