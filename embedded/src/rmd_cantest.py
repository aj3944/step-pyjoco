import myactuator_rmd_py as rmd
driver = rmd.CanDriver("can0")
actuator = rmd.ActuatorInterface(driver, 1)
actuator.getVersionDate()
# 2023020601
# actuator.sendPositionAbsoluteSetpoint(180.0, 500.0)
# temperature: 19, current: 0.1, shaft speed: 1, shaft angle: 0
actuator.shutdownMotor()