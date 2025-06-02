import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

def summarize_abstracts(abstracts: list[str]) -> str:
    llm = ChatOpenAI(
        temperature=0.3,
        model=os.getenv("OPENAI_MODEL_NAME"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base=os.getenv("OPENAI_API_BASE")
    )

    prompt = PromptTemplate.from_template("""
    You are an expert scientific summarizer. Given multiple research paper abstracts, write a concise summary with:

    - Key topics covered
    - Main findings
    - Techniques used

    Write 3–5 bullet points. Use formal academic tone.

    Abstracts:
    {abstracts}

    Summary:
    """)

    chain = LLMChain(llm=llm, prompt=prompt)
    combined = "\n\n".join(abstracts)
    return chain.run(abstracts=combined).strip()