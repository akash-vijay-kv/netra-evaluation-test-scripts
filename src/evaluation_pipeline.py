import asyncio
import os
from netra import Netra
from dotenv import load_dotenv
load_dotenv()


async def main():

    headers = f"x-api-key={os.getenv('NETRA_API_KEY')}"
    Netra.init(app_name="Evaluation Pipeline", headers=headers, debug_mode=True)

    """
    Turn Based Evaluation
    --------------------------------------------------
    """

    from copywriting_assistant import get_copywriting_agent_response

    dataset = Netra.evaluation.get_dataset(
        dataset_id="07f35fb2-dd69-4c89-979c-43145e2e5c2d")

    result = Netra.evaluation.run_test_suite(
        name="Copywriting Assistant v1",
        data=dataset,
        task=get_copywriting_agent_response,
    )



if __name__ == "__main__":
    asyncio.run(main())
