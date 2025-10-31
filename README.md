# Test Scripts for Netra Evaluation

This repository contains test scripts for Netra Evaluation. 


The test scripts mimics the behavior of a library assistant agent that can perform the following tasks:
- Fetch current shelf books
- Get book info
- Place orders


## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Netra SDK:
```bash
pip install <path-to-netra-sdk-local-repo>
```

3. Create a .env file in the root directory and add the secrets as mentioned in the .env.example file:


## Usage

Run the library_assistant_v1 with the following queries to generate sample dataset items:

1. What all books are in my shelf?

```bash
python3 src/library_assistant_v1.py --query "What all books are in my shelf?" 
```

2. Get me details about The Pragmatic Programmer

```bash
python3 src/library_assistant_v1.py --query "Get me details about The Pragmatic Programmer" 
```

3. What all books do I have on my shelf and can you order 2 copies of Dune?

```bash
python3 src/library_assistant_v1.py --query "What all books do I have on my shelf and can you order 2 copies of Dune?" 
```

Once you have generated the sample traces using the above commands, add them to your dataset. Then add the respective dataset id to the evaluation_pipeline.py file and run the evaluation pipeline.

```bash
python3 src/evaluation_pipeline.py
```

By default, the evaluation pipeline will run the evaluation for the library assistant v1 agent. To run the evaluation for the library assistant v2 agent, uncomment the respective code block in the evaluation_pipeline.py file.

Once the two evaluations are complete, you will be able to see that the library assistant v2 underperformed.

Now feel free to experiment with the evaluation pipeline.