# Challenge_Latitudo40
The Implementations and codes of Challenge by Latitudo40

## Team Green Avengers

![Teamlogo](./Documentation/images/greenavengers_logo.png)


## Project Overview

### Description of the Problem

#### FlowChart of our Process
![Flowchart](./Documentation/diagrams/flowchart.png)

#### The Problem That the Challenge Proposes
The challenge "ForestNav: Autonomous Carbon Storage Mapping for Climate Change Mitigation," proposed by the firm Latitudo40, aims to enhance the on-board systems of an existing ground rover. Its primary objective is to estimate Above Ground Biomass (AGB) through the elaboration of data gathered from both on-board sensors and satellites. AGB plays a crucial role in the carbon cycle, serving as a substantial reservoir of carbon absorbed from the atmosphere via photosynthesis. Accurately estimating AGB is vital for comprehending an ecosystem's carbon storage capacity, evaluating forest resources, and effectively managing carbon sequestration efforts to mitigate climate change. Our primary focus is to develop an innovative method to use ground data to estimate AGB values, enabling us to predict the amount of carbon storage related to an area.

![roverimg1](./Documentation/images/rover1.jpg)
![roverimg2](./Documentation/images/rover2.jpg)
![roverimg3](./Documentation/images/rover3.jpg)

#### How the Problem Proposed is Solved Currently
The rover Laura is a compact crawler vehicle designed for navigating uneven terrains, particularly in rugged forest environments and cultivated farmland. It is equipped with a comprehensive array of sensors, including stereo cameras and LiDAR, as well as onboard electronics such as GNSS receivers and various processing units. Additionally, a display is mounted on the rover to facilitate direct interaction with operators.

The stereo camera consists of two horizontally aligned RGB lenses, enabling depth perception by superimposing the two images to produce 3D pictures. LiDAR (Light Detection and Ranging) is a remote sensing technology that measures distances to objects or surfaces using laser pulses. This data is used for real-time 3D mapping of targeted areas and for object detection. LiDAR is highly valued for its accuracy, efficiency, and ability to capture detailed spatial information, making it applicable in geomatics, forestry, autonomous navigation, and environmental monitoring. The sensor currently mounted on the Laura rover provides 360-degree environmental scanning capabilities, enabling fast and accurate mapping and detection of nearby objects.

Communication with Laura can be established via WiFi or LAN cable. Movements can be directly controlled using a radio-controller or through ROS (Robot Operating System) via a specifically designed keyboard. ROS includes a 3D visualizer called RViz, which allows real-time monitoring of images acquired by the visual sensors (LiDAR and stereo camera) from Laura’s display.

What distinguishes Laura is its flexibility, allowing the integration of additional sensors to enhance data collection capabilities and improve data precision. This versatility ensures that Laura can effectively gather comprehensive data across various environments, making it a crucial tool for scientific research and environmental monitoring. Laura has already been tested in a vineyard environment, where it was remotely controlled to monitor the health status of the vegetation. The next steps involve the implementation of autonomous navigation algorithms to replace remote control, improving existing equipment to increase efficiency and expand usability, and automating data management and interpretation, which is currently performed manually. Our team has primarily focused on the last aspect, aiming to enhance the overall functionality and application of the Laura rover.


### Sample Output

![sampleoutput](./Documentation/images/output.png)