# Animal-Behavior-Analysis-Platform

## Introduction

This repository is the implementation of the "AI-enabled Animal Behavior Analysis with High Usability: A Case Study on Open-field Experiments" manuscript, involving behavior recognition, pose recognition, and natural language processing. To avoid memory issues, these three parts need to be deployed on different servers. Each server needs to be equipped with a GPU, and the GPU performance needs to be adjusted according to the model used.

For example, when choosing to use the QWen72B model or a larger-scale model to provide better services in natural language processing, the GPU performance needs to be increased to support the operation of the 72B model.

## Deployment Guide

1. **Behavior Recognition**: Deploy on one server, ensuring that the server is equipped with an appropriate GPU, and adjust the GPU performance based on the selected model. Project dependencies are listed in the requirements.txt file under the behavior folder.
2. **Pose Recognition**: Deploy on another server, also requiring consideration for GPU performance adjustment. Project dependencies are listed in the requirements.txt file under the pose folder.
3. **Natural Language Processing**: Deploy on a third server, adjust GPU performance according to the selected model (such as QWen72B) to support running larger models. Project dependencies are listed in the requirements.txt file under the natural_language folder.

**Note**: The server for App deployment does not require a GPU; you can choose a moderately performing server to deploy the application.

Please ensure that each server meets the GPU performance requirements to avoid memory issues.

## Contact Information

For any questions or further assistance, please contact: [159119942@qq.com]
