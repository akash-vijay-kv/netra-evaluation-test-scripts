# Test Scripts for Netra Evaluation

This repository contains test scripts for Netra Evaluation. 



## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a .env file in the root directory and add the secrets as mentioned in the .env.example file:


## Usage

Run the copywriting assistant with the different queires to generate sample dataset items:

Once you have generated the sample traces using the above commands, add them to your dataset. Then add the respective dataset id to the evaluation_pipeline.py file and run the evaluation pipeline.

```bash
python3 src/evaluation_pipeline.py
```
