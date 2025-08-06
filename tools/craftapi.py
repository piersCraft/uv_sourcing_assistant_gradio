from dotenv import load_dotenv
import os
from pydantic import BaseModel 
import asyncio
import aiohttp
import pandas as pd

_ = load_dotenv()

################################# - Models - #################################

class GraphQlFragment(BaseModel):
    name: str
    on_type: str
    fields: str

class GraphQlVariables(BaseModel):
    domain: str

class Payload(BaseModel):
    query: str
    variables: GraphQlVariables

class Company(BaseModel):
    id: int
    slug: str
    displayName: str
    shortDescription: str
    craftUrl: str
    logo: dict[str,str]
    companyType: str

class ApiResponse(BaseModel):
    data: dict[str, Company]

class Companies(BaseModel):
    companies: list[Company]


async def fetch_company(session, domain: str) -> Company:
    """
    Make a request to the Craft API
    """
    url = os.getenv("URL_CRAFT_QUERY")
    headers = {"X-Craft-Api-Key": f"{os.getenv('KEY_CRAFT_SOLENG')}", "Content-Type": "application/json"}

    firmographics = GraphQlFragment(
        name="company",
        on_type="Company",
        fields=""" id slug displayName shortDescription craftUrl logo { url } companyType """)
    query = f"""query company($domain: String!) {{ company(domain: $domain) {{ ...{firmographics.name} }} }} fragment {firmographics.name} on {firmographics.on_type} {{ {firmographics.fields} }}"""
    variables = GraphQlVariables(domain=domain)
    payload = Payload(query=query,variables=variables).model_dump()

    async with session.post(url, json=payload, headers=headers) as response:
        result = await response.json()

        return Company.model_validate(result["data"]["company"]) 

async def fetch_companies() -> Companies:
    domains = ["apple.com","vodafone.com","google.com"]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_company(session, domain) for domain in domains]
        results = await asyncio.gather(*tasks)

        return Companies(companies=results)

################################# - MAIN - #################################D
async def main():
    results = await fetch_companies()
    return results

if __name__ == "__main__":
    asyncio.run(main())
    df = pd.json_normalize(results.model_dump()["companies"])
    print(df)
