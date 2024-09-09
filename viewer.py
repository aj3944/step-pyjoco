from dm_control import mjcf
from dm_control import suite
from dm_control import viewer


# Parse from path
mjcf_model = mjcf.from_path("./step.xml")
with open("step.xml") as f:
  mjcf_model = mjcf.from_file(f)
import numpy as np

with open("step.xml") as f:
  xml_string = f.read()

try: 
  mjcf_model = mjcf.from_xml_string(xml_string)
  print(type(mjcf_model))  # <type 'mjcf.RootElement'>

  physics = mjcf.Physics.from_mjcf_model(mjcf_model)
except Exception as e:
  print(e)
env = suite.load(domain_name="humanoid", task_name="stand")
action_spec = env.action_spec()

# Define a uniform random policy.
def random_policy(time_step):
  del time_step  # Unused.
  return np.random.uniform(low=action_spec.minimum,
                           high=action_spec.maximum,
                           size=action_spec.shape)

viewer.launch(env,  policy=random_policy)
