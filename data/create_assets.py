import os
import json
import time
import numpy as np
from semanticscholar import SemanticScholar
sch = SemanticScholar()

def check_id_exists(array_of_objects, target_id):
    for obj in array_of_objects:
        if '@id' in obj and obj['@id'] == target_id:
            return True
    return False

PAPERS_LIMIT = 10
ASSETS_LIMIT = 100

papers = sch.search_paper('artificial intelligence', fields_of_study=['Computer Science'], limit=PAPERS_LIMIT).items

# Create a list to store the entries
papers_graph = []
publications_graph = []

for i, paper in enumerate(papers):
    if len(papers_graph) >= ASSETS_LIMIT:
        break

    # Append the entries to the list
    entry = {
        "@context": "https://schema.org",
        "@id": paper.paperId,
        "@type": "ScholarlyArticle",
        "isPartOf": paper.publicationVenue.id if paper.publicationVenue else None,
        "name": paper.title,
        "author": [x.name for x in paper.authors],
        "url": paper.url,
        "abstract": paper.abstract,
        "year": paper.year,
        "about": paper.fieldsOfStudy,
        "citation": []
    }

    if 'DOI' in paper.externalIds:
        entry['doi'] = paper.externalIds['DOI']
        citations = sch.get_paper_citations(paper.externalIds['DOI'], limit=10)
        for item in citations.items:
            entry['citation'].append(item.paper.paperId)
            if not check_id_exists(papers_graph, item.paper.paperId):
                papers.append(item.paper)

    print(f"Processing paper {i+1} with title {entry['name']} and {len(entry['citation'])} citations")

    papers_graph.append(entry)
    if paper.publicationVenue and not check_id_exists(publications_graph, paper.publicationVenue.id):
        publications_graph.append({
            "@context": "https://schema.org",
            "@id": paper.publicationVenue.id,
            "@type": [
                "PublicationVolume",
                "Periodical"
            ],
            "name": paper.publicationVenue.name,
            "issn": paper.publicationVenue.issn,
            "url": paper.publicationVenue.url,
            "volumeNumber": paper.journal.volume if paper.journal else None,
            "year": paper.year,
        })

    time.sleep(2)

# Create a JSON-LD object containing the retrieved papers
papers_jsonld_data = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": papers_graph
}
# Create a JSON-LD object containing the retrieved papers
publications_jsonld_data = {
    "@context": "https://schema.org",
    "@type": "ItemList",
    "itemListElement": papers_graph
}

# Convert JSON-LD object to JSON string
papers_json_data = json.dumps(papers_jsonld_data, indent=4)
publications_json_data = json.dumps(papers_jsonld_data, indent=4)

script_dir = os.path.dirname(os.path.abspath(__file__))

# Write the JSON data to a file
with open(os.path.join(script_dir, "papers.json"), "w") as json_file:
    json_file.write(papers_json_data)
with open(os.path.join(script_dir, "publications.json"), "w") as json_file:
    json_file.write(publications_json_data)

print("JSON data has been saved.")
print(f"Total papers processed: {len(papers_graph)}")
print(f"Total publications processed: {len(publications_graph)}")
