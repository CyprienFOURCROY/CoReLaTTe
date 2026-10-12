from typing import List, Tuple, Union
import os

import openai
from dotenv import load_dotenv

from utilities.utils import get_text_after_last_think_tag


load_dotenv()

ERROR_LLM_PROVIDER = openai.OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("API_BASE_URL") or None,
)

MAIN_LLM_PROVIDER = openai.OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("API_BASE_URL") or None,
)

MAIN_LLM = os.getenv("MAIN_LLM", "gpt-5")
ERROR_LLM = os.getenv("ERROR_LLM", MAIN_LLM)


def clean_code(raw_code: str) -> str:
    """
    Extract pure Python code from an LLM response.
    """

    raw_code = get_text_after_last_think_tag(raw_code).strip()

    if "```python" in raw_code:
        return (
            raw_code
            .split("```python", 1)[1]
            .split("```", 1)[0]
            .strip()
        )

    if "```" in raw_code:
        return raw_code.split("```", 1)[0].strip()

    return raw_code


def get_pandas_code(
    dataset_name: str,
    question: str,
    schema: str,
    temperature: float = 0,
    error_code: Union[
        Tuple[str, str],
        List[Tuple[str, str]],
        None
    ] = None,
    model: Union[str, None] = None,
) -> str:

    instructions = """
You are a pandas expert.

You must generate executable Python code for the CoReLaTTe benchmark.

Rules:

- Return ONLY Python code.
- Do NOT return markdown.
- Do NOT return explanations.
- Do NOT print anything.
- Do NOT use display().
- Do NOT use input().
- Do NOT read any files.
- Do NOT use pd.read_csv().
- Do NOT use pd.read_parquet().
- Do NOT use pd.read_stata().

The generated code MUST define:

def run_query(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    ...

The function receives all tables through the dictionary 'tables'.

Example:

df_portad = tables["ii_portad"]
df_in = tables["ii_in"]

The function MUST return a pandas DataFrame.

If the answer is scalar, wrap it inside a one-row DataFrame.

Example:

return pd.DataFrame(
    {"average_age": [avg_age]}
)

Use ONLY columns present in the schema.
Use ONLY tables present in the schema.
"""

    if error_code is None:

        user_prompt = f"""
Dataset:
{dataset_name}

Schema:
{schema}

Question:
{question}

Instructions:
{instructions}
"""

    else:

        if isinstance(error_code, tuple):
            previous_attempts = [error_code]
        else:
            previous_attempts = error_code

        last_code, last_error = previous_attempts[-1]

        user_prompt = f"""
The previous code failed.

Dataset:
{dataset_name}

Schema:
{schema}

Question:
{question}

Instructions:
{instructions}

Failed code:

{last_code}

Error:

{last_error}

Please generate corrected code.
"""

        if len(previous_attempts) > 1:

            user_prompt += "\n\nEarlier failures:\n"

            for i, (code, error) in enumerate(
                previous_attempts[:-1],
                start=1,
            ):
                user_prompt += f"""

Attempt {i}

Code:

{code}

Error:

{error}

"""

    current_provider = (
        ERROR_LLM_PROVIDER
        if error_code
        else MAIN_LLM_PROVIDER
    )

    current_model = model or (
        ERROR_LLM
        if error_code
        else MAIN_LLM
    )

    request = {
        "model": current_model,
        "messages": [
            {
            "role": "user",
            "content": user_prompt,
            }
        ],
        "max_completion_tokens": 5000,
    }

    # GPT-5 only accepts default temperature
    if not current_model.startswith("gpt-5"):
        request["temperature"] = temperature

    response = current_provider.chat.completions.create(
        **request
    )

    raw_code = response.choices[0].message.content

    return clean_code(raw_code)