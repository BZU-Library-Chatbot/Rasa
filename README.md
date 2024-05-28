# Rasa

This repository contains the chatbot model for the BZU Library Chatbot, powered by Rasa. The chatbot enhances the user experience by providing quick responses to users' questions and efficient access to library resources, information, and services.

## Overview

The BZU Library Chatbot is designed to streamline library services at the BZU library. It serves as an assistant, helping users quickly find information and access library resources through a conversational interface.

## Prerequisites

- Anaconda
- Python >= 3.11
- Microsoft Visual C++ 14.0 or greater
- Rasa >= 3.0

## Install

First, ensure you have Anaconda and the required tools installed. Then, create a new conda environment and install the required packages.

1. **Create and activate conda environment**:

   ```bash
   conda create --name rasa_env python=3.11
   conda activate rasa_env
   ```

2. **Install required packages**:

   ```bash
   pip install --upgrade pip setuptools wheel
   pip install --upgrade packaging
   pip install freetype-py scikit-learn matplotlib tensorflow dask ujson rasa
   ```

## Usage

To run the Rasa server:

1. **Train the Rasa model**:

   ```bash
   rasa train
   ```

2. **Run the Rasa server**:

   ```bash
   rasa run --enable-api --cors="*"
   ```

## Authors

👤 **Raghad Aqel**
👤 **Aziza Karakra**
👤 **Tariq Quraan**

- GitHub: Aziza Karakra(https://github.com/azizakarakra)
- LinkedIn: Aziza Karakra(https://www.linkedin.com/in/aziza-karakra-8a8231253/)
- GitHub: Tariq Quraan(https://github.com/RoOtT24)
- LinkedIn: Tariq Quraan(https://www.linkedin.com/in/tariq-quraan-42a079248/)
- GitHub: Raghad Aqel(https://github.com/Raghad-Aqel)
- LinkedIn: Raghad Aqel(https://www.linkedin.com/in/raghad-aqel-6ba112260/)
