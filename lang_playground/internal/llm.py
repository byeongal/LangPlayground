from langchain.chains.openai_functions import create_structured_output_runnable
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from lang_playground.schemas.career.v1_models import ResumeModel


async def parse_resume(pdf_contents: str, model: str = "gpt-3.5-turbo-16k") -> ResumeModel:
    # today_date = datetime.date.today()
    llm = ChatOpenAI(model=model, temperature=0)
    system_prompt = """\
You are a sophisticated algorithm designed to extract information into structured formats.

Make sure to answer in the correct format.
"""
    command_prompt = """\
Here is the input:
```
{input}
```

Extract the information according to the given format and constraints.
"""
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            (
                "human",
                command_prompt,
            ),
            ("human", "Tip: "),
        ]
    )

    runnable = create_structured_output_runnable(ResumeModel, llm, prompt)
    result: ResumeModel = runnable.invoke({"input": pdf_contents})
    return result
