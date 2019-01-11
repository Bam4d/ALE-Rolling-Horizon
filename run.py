from environment import ALEEnvironment
from RHEA import RollingHorizonEvolutionaryAlgorithm

if __name__ == '__main__':

    ale = ALEEnvironment('./roms/breakout.bin')
    rollout_length = 100
    rhea = RollingHorizonEvolutionaryAlgorithm(rollout_length, ale, 0.2, 30, ignore_frames=0)

    rhea.run()




