# Testbed Simulator App

This is an app that runs on the MFI Testbed workstation that serves as a stand-in for the automated assembly testbed. It communicates with Human-Robot Interface (HRI) terminals at the:
1. Stock Room
2. Kitting Station
3. Assembly WorkCell #1
4. Assembly WorkCell #2
5. Display Station
in order to guide human workers to execute the tasks that will later be automated by partner testbed projects.

The Testbed simulator uses the same web-API interfaces as the fully automated assembly testbed, designed with swapability in mind. It is separated from the offboard infrastructed required to manage the fleet of AMRs that run on the MFI workstation.


## Installation (TODO: update based on new workspace structure)

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/my-multi-page-streamlit-app.git
   ```

2. Navigate to the project directory:

   ```bash
   cd testbed_simulator_app
   ```

3. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

5. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the app, execute the following command:

```bash
streamlit run Home.py
```

This will start the Streamlit development server and open the app in your default web browser.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

Copyright (c) [2023] [Siddhant Wadhwa, Carnegie Mellon University]
```