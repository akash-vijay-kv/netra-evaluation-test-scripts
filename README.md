# Test Scripts for Netra Evaluation

This repository contains test scripts for Netra Evaluation. 


The repository includes a simulation-based evaluation entrypoint in `src/simulation_pipeline.py` that runs Netra simulations against a configured dataset.


## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Netra SDK:
```bash
pip install <path-to-netra-sdk-local-repo>
```

3. Create a `.env` file in the root directory and add the secrets as mentioned in `.env.example`.

   Required by `src/simulation_pipeline.py`:
   - `NETRA_API_KEY`


## Usage

### Run simulation-based evaluation

`src/simulation_pipeline.py` initializes Netra and runs a simulation against the dataset configured in the script.

```bash
python3 src/simulation_pipeline.py
```

To switch which agent you are simulating, edit `src/simulation_pipeline.py`:
- Uncomment the block for the agent you want (Milestone Agent / Customer Service Agent).
- Or keep the default `ChatKitAgent` block enabled.

If you want to run against a different dataset, update the `dataset_id` argument in the enabled `Netra.simulation.run_simulation(...)` call.

