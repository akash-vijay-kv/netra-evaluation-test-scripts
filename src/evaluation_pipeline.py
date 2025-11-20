import asyncio
import os
from netra import Netra
from netra.evaluation import EvaluationScore
from dotenv import load_dotenv
load_dotenv()


async def main():

    def custom_score(input, output, expected_output):
        # 
        #      
        #      Your custom logic
        #
        #
        return EvaluationScore(
            metric_type="contextuality",
            score=1,
        )

    from copywriting_assistant import get_copywriting_agent_response

    dataset = Netra.evaluation.get_dataset(
        dataset_id="d0c9c011-401d-41c3-a0f4-0dacc2ede87f")

    result = Netra.evaluation.run_test_suite(
        name="Copywriting Assistant v1",
        data=dataset,
        task=get_copywriting_agent_response,
        evaluators=[custom_score]
    )


#    from compliance_assistant import get_rag_agent_response

#    dataset = Netra.evaluation.get_dataset(dataset_id="58ca9e30-cfde-4a36-b329-47e6f14684a5")

#    result = Netra.evaluation.run_test_suite(
#        name="Compliance Assistant",
#        data=dataset,
#        task=get_rag_agent_response,
#    )


if __name__ == "__main__":
    asyncio.run(main())
