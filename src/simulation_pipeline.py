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
    
    # from milestone_agent_wrapper import call_customer_service_api
    from customer_service_agent import call_customer_service_bot

    result = Netra.simulation.run_simulation(
        name="Customer Service Agent v1",
        dataset_id="e62d0a9f-018e-4790-9fc9-16107f7b489a",
        context={"Metadata": "Customer Support"},
        task=call_customer_service_bot,
    )



if __name__ == "__main__":
    asyncio.run(main())
