import asyncio
import os
from netra import Netra
from netra.evaluation import DatasetItem
from dotenv import load_dotenv
load_dotenv()


async def main():
    headers = f"x-api-key={os.getenv('NETRA_API_KEY')}"
    Netra.init(app_name="test", headers=headers, debug_mode=True)

    # response = Netra.evaluation.create_dataset(
    #     name="test-v5-create-dataset",
    #     tags=["tag-1", "test-tag-2"]
    # )
    # print(response)

    # item1 = DatasetItem(
    #     input="Test Query 4 for evaluation - who is the current Prime Minister of India?",
    #     expected_output="The current Prime Minister of India is Narendra Modi"
    # )

    # item2 = DatasetItem(
    #     input={
    #         "question": "What is 2+2?",
    #         "context": "Math problem"
    #     },
    #     expected_output={
    #         "answer": "4",
    #         "confidence": 0.95
    #     }
    # )

    # response = Netra.evaluation.add_dataset_item(dataset_id="df735a66-e849-457f-9dc6-6b1f122ae574", item=item1)
    # print(response)

    # response = Netra.evaluation.get_dataset(dataset_id="8e069cec-3443-402e-99e5-c920357a9318")
    # print(response)

    from netra.evaluation import BaseEvaluator, EvaluatorConfig, EvaluatorOutput, ScoreType

    class MyEvaluator(BaseEvaluator):
        def evaluate(self, context):

            return EvaluatorOutput(
                evaluator_name="my_evaluator",
                result=1,
                is_passed=True,
                reason="Match",
            )

    from copywriting_assistant import get_copywriting_agent_response

    dataset = Netra.evaluation.get_dataset(
        dataset_id="0f256725-177a-48d1-a7f3-a79643f98bd8")

    result = Netra.evaluation.run_test_suite(
        name="Copywriting Assistant v1",
        data=dataset,
        task=get_copywriting_agent_response,
        evaluators=[
            MyEvaluator(
                EvaluatorConfig(
                    name="my_evaluator",
                    label="My Custom Evaluator",
                    score_type=ScoreType.NUMERICAL,
                )
            )
        ]
    )


    # dataset = Netra.evaluation.get_dataset(
    #     dataset_id="0f256725-177a-48d1-a7f3-a79643f98bd8")

    # result = Netra.evaluation.run_test_suite(
    #     name="Copywriting Assistant v1",
    #     data=dataset,
    #     task=get_copywriting_agent_response,
    # )


if __name__ == "__main__":
    asyncio.run(main())
