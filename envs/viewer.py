from dm_control import mjcf
from dm_control import suite
from dm_control import viewer

import numpy as np

# with open("../step.xml") as f:
#   xml_string = f.read()
# mjcf_model = mjcf.from_xml_string(xml_string)



env = suite.load(domain_name="humanoid", task_name="stand")
action_spec = env.action_spec()

# Define a uniform random policy.
def random_policy(time_step):
  del time_step  # Unused.
  return np.random.uniform(low=action_spec.minimum,
                           high=action_spec.maximum,
                           size=action_spec.shape)

viewer.launch(env,  policy=random_policy)
