# Fire-detection-Mesh-Network-AWS

This project describes an early forest fire detection system using IoT components and a mesh network. The system employs Raspberry Pi 4, DS18B20 temperature sensors, MQ135 gas sensors, and Raspberry Pi cameras to monitor forest conditions. Data collected from these sensors is transmitted to AWS cloud for analysis and real-time monitoring, enabling early fire detection to minimize damage to wildlife.


Key aspects of the system include:

Hardware setup: Multiple nodes are deployed in the forest, each equipped with sensors to detect temperature and smoke, as well as a camera to capture images

Mesh network: The system uses a wireless mesh network with the BATMAN routing protocol to ensure communication between nodes, even in areas with limited connectivity

Data collection: Sensors collect temperature and air quality data, while cameras capture images every 5 seconds

Cloud integration: The collected data is sent to AWS cloud services for storage and analysis

Fire detection: AWS Rekognition is used to classify images and detect the presence of fire

Alerting system: When fire is detected, the system triggers an email alert using AWS SNS (Simple Notification Service)
