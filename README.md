# OpenSCAD Humanoid with MuJoCo Controls

## Description

This repository contains the design and control code for an open-source humanoid robot. The design of the robot is created using OpenSCAD, a script-based 3D CAD modeler, allowing for parametric and fully customizable design files. The control of the humanoid is managed using Python, interfacing with the MuJoCo (Multi-Joint dynamics with Contact) physics engine, which provides a realistic simulation environment for the robot.

## Features
- **Parametric Design**: The humanoid robot's structure is fully defined in OpenSCAD, enabling users to modify dimensions, joint angles, and other physical properties easily.
- **Python Control Scripts**: Control algorithms written in Python, allowing users to simulate, test, and refine control strategies for the humanoid's movements.
- **MuJoCo Integration**: The repository leverages MuJoCo's advanced physics simulation capabilities to create a realistic environment for testing the robot's dynamics and control systems.
- **Customizable Components**: Users can design and simulate various components, such as arms, legs, and sensors, to suit different research and development needs.
- **Simulation Environment**: Pre-built environments in MuJoCo for testing walking, balancing, and complex maneuvers.

## Getting Started
1. **Clone the Repository**: Start by cloning the repository to your local machine.
2. **OpenSCAD Design**: Customize the humanoid design using the provided OpenSCAD files.
3. **Python & MuJoCo Setup**: Follow the setup instructions to install Python dependencies and configure MuJoCo for your system.
4. **Run Simulations**: Use the provided Python scripts to simulate the humanoid's behavior in MuJoCo, with various control strategies available.

## Prerequisites
- OpenSCAD installed for editing and viewing the 3D models.
- Python 3.x with necessary libraries (e.g., NumPy, MuJoCo Python bindings).
- MuJoCo installed and properly configured with a valid license.

## Usage
- **Customization**: Modify the `step_bot.scad` file to change the humanoid's design parameters.
- **Control Algorithms**: Implement and test control algorithms in Python using the provided templates.
- **Simulation**: Run the simulation scripts to observe the robot's performance under different conditions.

## Contributing
Contributions are welcome! Feel free to fork the repository, make your changes, and submit a pull request. Please make sure to document any new features or modifications.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
For any questions, suggestions, or contributions, please reach out to aj3944@nyu.edu.

---

This repository bridges the gap between mechanical design and control systems, enabling researchers, educators, and enthusiasts to explore humanoid robotics in an open-source and customizable environment.
