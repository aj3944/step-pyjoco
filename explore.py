
from absl import app

from dm_control.locomotion.examples import basic_cmu_2019
from dm_control import viewer


def main(unused_argv):
  viewer.launch(environment_loader=basic_cmu_2019.cmu_humanoid_run_gaps)

if __name__ == '__main__':
  app.run(main)