import asyncio
import os
from netra import EvaluationScore, Netra
from dotenv import load_dotenv
load_dotenv()


async def main():
    
   from copywriting_assistant import get_copywriting_agent_response

   dataset = Netra.evaluation.get_dataset(dataset_id="758aa765-5bdb-4c62-bb37-b1c575d9e846")

   result = Netra.evaluation.run_test_suite(
       name="Copywriting Assistant v1",
       data=dataset,
       task=get_copywriting_agent_response,
   )

    
if __name__ == "__main__":
    asyncio.run(main())