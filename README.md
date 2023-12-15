


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/DockDockGo/amr_fleet_offboard_infra_frontend.git
   ```

2. Navigate to the project directory:

   ```bash
   cd amr_fleet_offboard_infra_frontend
   ```

3. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

5. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

6. Change https://github.com/DockDockGo/amr_fleet_offboard_infra_frontend/blob/85df3925460e07cdb42c286959ad6e06bd029f2c/utils.py#L11 to contain the discoverable IP address of the machine running the backend server (https://github.com/DockDockGo/amr_fleet_offboard_infra_backend/tree/master)

7. If you'd like the ability to use the reset page of this webapp in order to clear any previous missions from the database, this app must be run on the same machine as the backend server, and https://github.com/DockDockGo/amr_fleet_offboard_infra_frontend/blob/85df3925460e07cdb42c286959ad6e06bd029f2c/pages/80_%F0%9F%8E%9B%EF%B8%8F_Reset_Fleet_Infra_Missions.py#L18 needs to be updated to the full path of the backend server's django project directory.

## Usage

To run the app, execute the following command:

```bash
streamlit run Home.py
```

This will start the Streamlit development server and open the app in your default web browser. The url containing the port in use will be printed to console output.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

Copyright (c) [2023] [Siddhant Wadhwa, Carnegie Mellon University]
```
