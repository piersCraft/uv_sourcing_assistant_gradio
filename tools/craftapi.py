from dotenv import load_dotenv
import os
import requests
from requests import Response
from pydantic import BaseModel 

################################# - Models - #################################

class GraphQlQuery(BaseModel):
    query: str
    variables: str | None

class GraphQlFragment(BaseModel):
    name: str
    on_type: str
    fields: str

class GraphQlVariables(BaseModel):
    domain: str

class CraftPayload(BaseModel):
    query: str
    variables: GraphQlVariables

class CraftCompanyDetails(BaseModel):
    id: int
    slug: str
    displayName: str
    shortDescription: str
    craftUrl: str
    logo: dict[str,str]
    companyType: str

class CraftCompany(BaseModel):
    company: dict[str,CraftCompanyDetails]

class CraftResponse(BaseModel):
    data: dict[str, CraftCompany]

################################# - Function - #################################

_ = load_dotenv()
craft_key: str = os.getenv("KEY_CRAFT_SOLENG")
craft_url: str = os.getenv("URL_CRAFT_QUERY")

# Instantiate company query fragment
fragment_company = GraphQlFragment(
    name="company",
    on_type="Company",
    fields=""" id slug displayName shortDescription craftUrl logo { url } companyType """)

# Build graphQL query string
def constructQuery(fragment: GraphQlFragment) -> str:
    query_string: str = f"""query company($domain: String!) {{ company(domain: $domain) {{ ...{fragment.name} }} }} fragment {fragment.name} on {fragment.on_type} {{ {fragment.fields} }}"""
    return query_string

# Fetch company data
def fetchSubjectCompany(domain: str) -> CraftCompanyDetails:
    query = constructQuery(fragment_company)
    variables = GraphQlVariables(id=id)
    response: Response = requests.post(url=craft_url,headers={"X-Craft-Api-Key": craft_key},json=CraftPayload(query=query, variables=variables).model_dump())
    subjectCompany = CraftCompanyDetails.model_validate(response.json()['data']['company'])
    return subjectCompany

################################# - MAIN - #################################D

def main():
    domain: str = "apple.com"
    subject_company = fetchSubjectCompany(domain)
    print(subject_company.model_dump())


if __name__ == "__main__":
    main()
