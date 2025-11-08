import asyncio
import os
from netra import EvaluationScore, Netra
from dotenv import load_dotenv
load_dotenv()


async def main():
    
    # V1 Agent Test Run
    from library_assistant_v1 import get_library_agent_response

    dataset = Netra.evaluation.get_dataset(dataset_id="8900c125-c1a7-4f54-a68c-3e621269f7e3")

    result = Netra.evaluation.run_test_suite(
        name="Library Assistant v1",
        data=dataset,
        task=get_library_agent_response,
    )

    # V2 Agent Test Run17598458-62c4-46a4-bae7-eec3d0bca1c6
    # def accuracy_evaluator(input, output, expected_output):
    #     if expected_output == output:
    #         return EvaluationScore(metric_type="accuracy", score=1)
 
    #     return EvaluationScore(metric_type="accuracy", score=0)


    # from library_assistant_v2 import get_library_agent_response

    # dataset = Netra.evaluation.get_dataset(dataset_id="8900c125-c1a7-4f54-a68c-3e621269f7e3")

    # result = Netra.evaluation.run_test_suite(
    #     name="Library Assistant v2",
    #     data=dataset,
    #     task=get_library_agent_response,
    #     evaluators=[accuracy_evaluator],
    # )


    # V3 Dataset Entry via SDK
    # from netra.evaluation import DatasetEntry
    # from netra import Netra
    
    # from dotenv import load_dotenv

    # headers = f"x-api-key={os.environ['NETRA_API_KEY']}"

    # Netra.init(
    #     app_name="openai-eval-feature",
    #     disable_batch=True,
    #     environment="dev",
    #     headers=headers,
    # )


    # local_dataset = [
    #     DatasetEntry(
    #         input="What books are on my shelf?", 
    #         expected_output={"output":"You have the following books on your shelf: \n\n1. Dune by Frank Herbert - $14.99 (Available) \n2. The Pragmatic Programmer by Andrew Hunt, David Thomas - $39.99 (Available) \n3. Clean Code by Robert C. Martin - $34.95 (Not Available)"}, 
    #         tags=["library, books"]),
    #     DatasetEntry(
    #         input="What is the price of book 1?", 
    #         expected_output={"output":"The price of book 1 is $14.99"}, 
    #         tags=["library, books"]),
    #     DatasetEntry(
    #         input="Order 2 copies of Dune by Frank Herbert", 
    #         expected_output={"output":"2 copies of Dune by Frank Herbert have been ordered."}, 
    #         tags=["library, books"]),
    # ]

    # dataset_id = Netra.evaluation.create_dataset(name="Test-Dataset")
    # for entry in local_dataset:
    #     Netra.evaluation.add_dataset_entry(dataset_id=dataset_id, item=entry)

    
if __name__ == "__main__":
    asyncio.run(main())