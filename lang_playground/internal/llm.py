from datetime import date

from langchain.chains.openai_functions import create_structured_output_runnable
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from lang_playground.schemas.career.v1_models import ResumeModel


async def parse_resume(pdf_contents: str, model: str = "gpt-3.5-turbo-16k") -> ResumeModel:
    today_date = date.today().strftime("%Y-%m-%d")
    llm = ChatOpenAI(model=model, temperature=0)
    system_prompt = f"""\
You are a sophisticated algorithm designed to extract information into structured formats.

Conditions:
```
1. For fields with specific allowed values (like 'employment_type', 'graduation_status', 'category'), ensure the extracted value matches one of the permitted options.
2. Please express data representing date information in the form of datetime.date(`yyyy-MM-dd`).
3. If you can't find the exact day for some of your data, put the first day of the month for the start (e.g. `from`) and the last day of the month for the end (e.g. `to`).
3. If you can't pick a suitable data or can't find it, do not generate text.
```

Additional Information:
```
Today: {today_date}
```
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
        ]
    )

    runnable = create_structured_output_runnable(ResumeModel, llm, prompt)
    result: ResumeModel = runnable.invoke({"input": pdf_contents})
    return result
