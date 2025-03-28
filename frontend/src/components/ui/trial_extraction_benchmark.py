# ✅ Module: trial_extraction_benchmark.py
# Purpose: Extract trials from your PostgreSQL (Presqrl) database for a given therapeutic area,
# then run 3-way comparison: Direct parse, LlamaExtract, LangChain/GPT

import psycopg2
import requests
import json
from llama_index.extract import ExtractionAgent
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser
from langchain.pydantic_v1 import BaseModel, Field
from typing import List

# === Define schema ===
class TrialSchema(BaseModel):
    NCT_ID: str
    Title: str = None
    Status: str = None
    Who: str = None
    What: str = None
    Where: str = None
    When: str = None
    Why: str = None
    Phase: str = None
    Design_Model: str = None
    Endpoints: str = None
    Sample_Size: str = None
    Timeline: str = None
    Assessment_Methods: str = None

# === Connect to Presqrl DB ===
def get_trials_from_db(area: str, limit: int = 10):
    conn = psycopg2.connect(
        dbname="presqrl",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT nct_id
        FROM trials
        WHERE therapeutic_area = %s
        LIMIT %s;
    """, (area, limit))
    nct_ids = [row[0] for row in cur.fetchall()]
    cur.close()
    conn.close()
    return nct_ids

# === Direct Parse from ClinicalTrials.gov API ===
def parse_ctgov_direct(nct_id):
    url = f"https://clinicaltrials.gov/api/v2/studies/{nct_id}?fmt=json"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    data = r.json()
    # extract structured parts only (e.g., Title, Phase)
    return {
        "NCT_ID": nct_id,
        "Title": data.get("ProtocolSection", {}).get("IdentificationModule", {}).get("OfficialTitle", None),
        "Status": data.get("ProtocolSection", {}).get("StatusModule", {}).get("OverallStatus", None),
        "Phase": data.get("ProtocolSection", {}).get("DesignModule", {}).get("PhaseList", {}).get("Phase", [None])[0]
    }

# === LlamaExtract Option ===
llama_agent = ExtractionAgent.from_name("ClinicalTrialSchema")
def extract_with_llama(summary_text):
    result = llama_agent.extract(summary_text)
    return result.to_dict()

# === LangChain Option ===
class LangTrialSchema(BaseModel):
    NCT_ID: str = Field(...)
    Title: str = Field(None)
    Status: str = Field(None)
    Who: str = Field(None)
    What: str = Field(None)
    Where: str = Field(None)
    When: str = Field(None)
    Why: str = Field(None)
    Phase: str = Field(None)
    Design_Model: str = Field(None)
    Endpoints: str = Field(None)
    Sample_Size: str = Field(None)
    Timeline: str = Field(None)
    Assessment_Methods: str = Field(None)

langchain_parser = StructuredOutputParser.from_orm(LangTrialSchema)
prompt_template = PromptTemplate(
    template="""
    Extract the following fields from this trial summary:
    {format_instructions}
    Summary:
    {summary}
    """,
    input_variables=["summary"],
    partial_variables={"format_instructions": langchain_parser.get_format_instructions()}
)
llm = ChatOpenAI(temperature=0, model="gpt-4")

def extract_with_langchain(summary_text, nct_id):
    prompt = prompt_template.format(summary=summary_text)
    output = llm(prompt)
    parsed = langchain_parser.parse(output.content)
    parsed.NCT_ID = nct_id
    return parsed.dict()

# === Main Benchmark Function ===
def run_trial_benchmark(area="Oncology", limit=10):
    nct_ids = get_trials_from_db(area, limit)
    results = []
    for nct in nct_ids:
        summary_text = requests.get(f"https://clinicaltrials.gov/study/{nct}").text
        direct = parse_ctgov_direct(nct)
        llama = extract_with_llama(summary_text)
        lang = extract_with_langchain(summary_text, nct)
        results.append({
            "NCT_ID": nct,
            "direct": direct,
            "llama": llama,
            "langchain": lang
        })
    return results
