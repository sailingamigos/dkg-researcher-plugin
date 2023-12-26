# DKG Copilot

This repository is a grant project supported by https://github.com/OriginTrail/ChatDKG. It contains source code for AI-powered GPT (copilot) for scientific research that combines the OriginTrail Decentralized Knowledge Graph with LLMs. The copilot is designed to help retrieve information on scientific papers, analyze their results, and manage citations.

The copilot should allows for more effective and efficient research by providing access to information that could be verified and analyzed utilizing the OriginTrail Decentralized Knowledge Graph (DKG). Key benefits of this copilot include ensuring data verifiability and trust by using the DKG, as well as performing machine learning algorithms over trusted data.

## Copilot in action

In the sections below, there are various use cases and further research opportunities for the copilot.

### Literature Review and Hypothesis Generation Assistance

Example: https://chat.openai.com/share/cbfb7da5-1afa-4fbe-8d71-3c8c75a8806e

The copilot assists in creating a comprehensive and up-to-date literature review. It analyzes the user's research topic and abstracts retrieved from the DKG. Then, it summarizes key findings, highlights trends, and identifies gaps in current research. Additionally, it helps researchers generate new hypotheses based on existing literature.

### Clustering for Research Trend Analysis and Similarity Search

Example: https://chat.openai.com/share/2c223cc6-9b8c-4623-a562-083368b4bd3c

Copilot can use clustering algorithms to analyze trends in scientific research and group them based on vectors embedding similarity. This can help in identifying emerging fields, popular methodologies, or collaboration patterns. Use topic modeling to identify under-researched areas within a specific field. This can guide researchers towards topics that are ripe for exploration.

Copilot uses clustering algorithms to analyze trends in scientific research and groups them based on abstracts embedding similarity. This helps in identifying emerging fields and under-researched areas within a specific field. This guides researchers towards topics that have wide range of opportunities for further research.

### Regression Analysis for Citation Prediction

Example: https://chat.openai.com/share/06844f72-fa7f-4b39-a174-7835b50c7449

Copilot creates a model that predicts the future citation count of papers or fields, which can be an indicator of their impact and relevance in the field. This serves as a valuable indicator of the potential impact and relevance of these papers or fields within the academic landscape. By forecasting citation counts, researchers gain valuable insights into the long-term influence and significance of their/other work.

### Research Collaboration Network Analysis (Future)

The copilot could help researchers identify potential collaborators. It could analyze authorship data from papers in the database to suggest researchers with similar interests or complementary expertise.

### Funding Opportunity Identification (Future)

The copilot could assist researchers in identifying potential funding sources. By analyzing the topics, content, and results of their work, the copilot can suggest relevant grants, scholarships, or funding parties.

### Sentiment Analysis for Research Impact Assessment (Future)

Copilot could perform sentiment analysis on citations and references to evaluate the impact of research papers in the academic community. This means it could assess the overall sentiment associated with citations and references, and it could also track how the sentiment around a paper changes over time, giving researchers valuable insights into how their work is perceived as industry evolves.

## Project specification

A detailed project specification with architecture and sequence diagrams is available [here](docs/project-specification.md).

## Timeline

The project has been executed in two phases: beta and release version. The beta version includes setting up the environment and verifying the approach with Semantic Scholar data and the ScholarlyArticle ontology, without AI Cortex. The beta version will be released and made public for early feedback.

![](docs/beta-version.png)

The release version will improve accuracy, introduce AI Cortex, and update the DKG with ArXiv data and ontology.

![](docs/release-version.png)

## Expected outcomes

Upon the completion of this project, a list of findings will be presented and the copilot will be available at the OpenAI marketplace.

## Next steps

The next steps involve implementing the future use cases mentioned above. This includes retrieving blockchain proofs for assets along with the requested data. As a fallback option, we plan to introduce an embedding-based RAG if generated sparql query is incorrect.

Additionally, our goal is to test smaller models and refine them using reinforcement learning based on human feedback to achieve better results. Also, we want to test the OT World API, and integrate the Twitter API with the DKG copilot.

<hr>

_Document version: 1.0.0-beta_

_Last changed: 26th Dec 2023_
