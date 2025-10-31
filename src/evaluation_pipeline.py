import asyncio
from netra import Netra
from dotenv import load_dotenv
load_dotenv()


async def main():
    
    # V1 Agent Test Run
    from library_assistant_v1 import get_library_agent_response

    dataset = Netra.evaluation.get_dataset(dataset_id="17265fe3-ef5b-43ec-a358-555a189fc0a4")

    result = Netra.evaluation.run_test_suite(
        name="Library Assistant v1",
        data=dataset,
        task=get_library_agent_response,
    )


    # V2 Agent Test Run
    # from library_assistant_v2 import get_library_agent_response

    # dataset = Netra.evaluation.get_dataset(dataset_id="17265fe3-ef5b-43ec-a358-555a189fc0a4")

    # result = Netra.evaluation.run_test_suite(
    #     name="Library Assistant v2",
    #     data=dataset,
    #     task=get_library_agent_response,
    # )

if __name__ == "__main__":
    asyncio.run(main())