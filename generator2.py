import numpy as np
import math

class TrafficGenerator:
    def __init__(self, max_steps, n_cars_generated):
        self._array = TrafficGenerator.input(int())
        self._n_cars_generated = sum(array)  # how many cars per episode
        self._max_steps = max_steps

        def input():
            array = np.arange(12).reshape(4,3)

            print("""enter the values in this way: 
                in_out direction 

                'W_N' 'W_E' 'W_S'
                'N_W' 'N_E' 'N_S'
                'E_W' 'E_N' 'E_S'
                'S_W' 'S_N' 'S_E'

                for example W_N means vehicles coming from west and will go in north direction
                """)

            for i in range(4):
                for j in range(3):
                    array[i][j]=int(input())

                    return array        


        def generate_routefile(self, seed):
            """
            Generation of the route of every car for one episode
            """
            np.random.seed(seed)  # make tests reproducible

        # the generation of cars is distributed according to a weibull distribution
            timings = np.random.weibull(2, self._n_cars_generated)
            timings = np.sort(timings)

        # reshape the distribution to fit the interval 0:max_steps
            car_gen_steps = []
            min_old = math.floor(timings[1])
            max_old = math.ceil(timings[-1])
            min_new = 0
            max_new = self._max_steps
            for value in timings:
                car_gen_steps = np.append(car_gen_steps, ((max_new - min_new) / (max_old - min_old)) * (value - max_old) + max_new)

            car_gen_steps = np.rint(car_gen_steps)  # round every value to int -> effective steps when a car will be generated

        # produce the file for cars generation, one car per line
            with open("intersection/episode_routes.rou.xml", "w") as routes:
                print("""<routes>
                    <vType accel="1.0" decel="4.5" id="standard_car" length="5.0" minGap="2.5" maxSpeed="25" sigma="0.5" />

                    <route id="W_N" edges="W2TL TL2N"/>
                    <route id="W_E" edges="W2TL TL2E"/>
                    <route id="W_S" edges="W2TL TL2S"/>
                    <route id="N_W" edges="N2TL TL2W"/>
                    <route id="N_E" edges="N2TL TL2E"/>
                    <route id="N_S" edges="N2TL TL2S"/>
                    <route id="E_W" edges="E2TL TL2W"/>
                    <route id="E_N" edges="E2TL TL2N"/>
                    <route id="E_S" edges="E2TL TL2S"/>
                    <route id="S_W" edges="S2TL TL2W"/>
                    <route id="S_N" edges="S2TL TL2N"/>
                    <route id="S_E" edges="S2TL TL2E"/>""", file=routes)

            
                for counter, step in enumerate(car_gen_steps):
                    i = np.random.randint(0,4)
                    j = np.random.randint(0,3)

                    if(array[i][j]>0):
                        if(i,j==0,0):
                            print('    <vehicle id="W_N_%i" type="standard_car" route="W_N" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        elif(i,j==0,1):
                            print('    <vehicle id="W_E_%i" type="standard_car" route="W_E" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        elif(i,j==0,2):
                            print('    <vehicle id="W_S_%i" type="standard_car" route="W_S" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        elif(i,j==1,0):  
                            print('    <vehicle id="N_W_%i" type="standard_car" route="N_W" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        elif(i,j==1,1):
                            print('    <vehicle id="N_E_%i" type="standard_car" route="N_E" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)                        
                        elif(i,j==1,2):
                            print('    <vehicle id="N_S_%i" type="standard_car" route="N_S" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        elif(i,j==2,0):
                            print('    <vehicle id="E_W_%i" type="standard_car" route="E_W" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        elif(i,j==2,1):
                            print('    <vehicle id="E_N_%i" type="standard_car" route="E_N" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        elif(i,j==2,2):
                            print('    <vehicle id="E_S_%i" type="standard_car" route="E_S" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        elif(i,j==3,0):
                            print('    <vehicle id="S_W_%i" type="standard_car" route="S_W" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        elif(i,j==3,1):
                            print('    <vehicle id="S_N_%i" type="standard_car" route="S_N" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        elif(i,j==3,2):
                            print('    <vehicle id="S_E_%i" type="standard_car" route="S_E" depart="%s" departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                        else:
                            print("error")

                        array[i][j]-=1


                print("</routes>", file=routes)