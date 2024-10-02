import os
from langchain.llms import GooglePalm
from langchain.prompts import PromptTemplate
import json

api_key = 'AIzaSyB5MJwoZfpm3PLNLOrhhbzhuVYw0GvTXEQ'

def extractConcepts(context: str, metadata={}):
    llm = GooglePalm(google_api_key=api_key, temperature=0.2)

    concept_system = """
    Your task is extract the key concepts (and non personal entities) mentioned in the given context.
            Extract only the most important and atomistic concepts, if  needed break the concepts down to the simpler concepts.
            Categorize the concepts in one of the following categories:
            [event, concept, place, object, document, organisation, condition, misc]
            Format your output as a list of json with the following format:
            [   
                {
                    "entity": The Concept,
                    "importance": The concontextual importance of the concept on a scale of 1 to 5 (5 being the highest),
                    "category": The Type of Concept,
                }, 
                { }, 
            ]
    """.strip()

    concept_prompt = PromptTemplate.from_template("""
    {sys}
                    
    context: {cext}
    output:""")

    msg = concept_prompt.format(sys=concept_system, cext=context)
    response = llm.invoke(msg)

    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None

    return result

def extractGraphs(context: str, metadata={}):
    
    llm = GooglePalm(google_api_key=api_key, temperature=0.2)

    graph_system = """
    You are a network graph maker who extracts terms and their relations from a given context.
        You are provided with a context chunk (delimited by ```) Your task is to extract the ontology
        of terms mentioned in the given context. These terms should represent the key concepts as per the context
        Thought 1: While traversing through each sentence, Think about the key terms mentioned in it.
            Terms may include object, entity, location, organization, person,
            condition, acronym, documents, service, concept, etc.
            Terms should be as atomistic as possible
        Thought 2: Think about how these terms can have one on one relation with other terms.
            Terms that are mentioned in the same sentence or the same paragraph are typically related to each other.
            Terms can be related to many other terms
        Thought 3: Find out the relation between each such related pair of terms.
        Format your output as a list of json. Each element of the list contains a pair of terms
        and the relation between them, like the following:
        [
        {
            "node_1": "A concept from extracted ontology",
            "node_2": "A related concept from extracted ontology",
            "edge": "relationship between the two concepts, node_1 and node_2 in one or two sentences"
        }, {...}
        ]
    """.strip()

    graph_prompt = PromptTemplate.from_template("""
    {sys}

    context: ```{cext}```
    output: """)

    msg = graph_prompt.format(sys=graph_system, cext=context)
    response = llm.invoke(msg)

    try:
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except:
        print("\n\nERROR ### Here is the buggy response: ", response, "\n\n")
        result = None

    return result