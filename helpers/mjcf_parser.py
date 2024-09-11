from dm_control import mjcf


with open("step.xml") as f:
  xml_string = f.read()
mjcf_model = mjcf.from_xml_string(xml_string)



print(mjcf_model)  # <type 'mjcf.RootElement'>


my_geom = mjcf_model.worldbody.body['pelvis'].body['step_bot_left_hip_yaw_link'].body['step_bot_left_hip_pitch_link'].geom['knee']
print(isinstance(mjcf_model, mjcf.Element)) # True
print(my_geom.name)    # 'my_geom'
print(my_geom.pos)     # np.array([0., 1., 2.], dtype=float)
print(my_geom.dclass)  # 'brick'\
