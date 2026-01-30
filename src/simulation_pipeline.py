import asyncio
import os
from netra import Netra
from dotenv import load_dotenv
load_dotenv()


async def main():

    headers = f"x-api-key={os.getenv('NETRA_API_KEY')}"
    Netra.init(app_name="Simulation Pipeline", headers=headers, debug_mode=True)

    """
    Simulation Based Evaluation
    --------------------------------------------------
    """
    
    from milestone_agent_wrapper import call_customer_service_api

    result = Netra.simulation.run_simulation(
        name="Milestone Agent v1",
        dataset_id="4268a0c9-e235-4279-9213-a2e56f52c7d6",
        context={"Metadata": "Customer Support"},
        task=call_customer_service_api,
    )



if __name__ == "__main__":
    asyncio.run(main())
