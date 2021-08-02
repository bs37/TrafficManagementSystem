from __future__ import absolute_import
from __future__ import print_function

import os
from shutil import copyfile
import numpy as np
from testing_simulation import Simulation
from generator import TrafficGenerator
from model import TestModel
from visualization import Visualization
from utils import import_test_configuration, set_sumo, set_test_path


if __name__ == "__main__":

    config = import_test_configuration(config_file='testing_settings.ini')
    sumo_cmd = set_sumo(config['gui'], config['sumocfg_file_name'], config['max_steps'])
    model_path, plot_path = set_test_path(config['models_path_name'], config['model_to_test'])

    Model = TestModel(
        input_dim=config['num_states'],
        model_path=model_path
    )

    # array = np.arange(12).reshape(4,3)

    # print("""enter the values in this way: 
    #             in_out direction 

    #             'W_N' 'W_E' 'W_S'
    #             'N_W' 'N_E' 'N_S'
    #             'E_W' 'E_N' 'E_S'
    #             'S_W' 'S_N' 'S_E'

    #             for example W_N means vehicles coming from west and will go in north direction
    #             """)

    # for i in range(4):
    #     for j in range(3):
    #         array[i][j]=int(input())

                

    TrafficGen = TrafficGenerator(
        config['max_steps'], 
        config['n_cars_generated']
    )

    Visualization = Visualization(
        plot_path, 
        dpi=96
    )
        
    Simulation = Simulation(
        Model,
        TrafficGen,
        sumo_cmd,
        config['max_steps'],
        config['green_duration'],
        config['yellow_duration'],
        config['num_states'],
        config['num_actions']
    )

    print('\n----- Test episode')
    simulation_time = Simulation.run(config['episode_seed'])  # run the simulation
    print('Simulation time:', simulation_time, 's')

    print("----- Testing info saved at:", plot_path)

    copyfile(src='testing_settings.ini', dst=os.path.join(plot_path, 'testing_settings.ini'))

    Visualization.save_data_and_plot(data=Simulation.reward_episode, filename='reward', xlabel='Action step', ylabel='Reward')
    Visualization.save_data_and_plot(data=Simulation.queue_length_episode, filename='queue', xlabel='Step', ylabel='Queue lenght (vehicles)')
