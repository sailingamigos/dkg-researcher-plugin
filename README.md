# OriginTrail DKG AI-powered copilot plugin for scientific research

This repository contains source code for AI-powered copilot plugin for scientific research that combines the OriginTrail DKG with LLMs. 
The plugin is designed to help retrieve scientific papers, analyze their results, and manage citations within the Microsoft Word copilot. 

Such plugin should allow more effective and efficient research by providing access to information that could be verified and analyzed for the knowledge discovery. Key benefits of this plugin include ensuring data verifiability and trust by using decentralized knowledge graph, as well as facilitating machine learning over trusted data.

<img width="1176" alt="Screenshot 2023-07-22 at 20 51 47" src="https://github.com/sailingamigos/dkg-researcher-plugin/assets/128464297/8853b83e-80f6-4103-8ffa-560f986ce245">

# Description

This project aims to build an AI-powered copilot plugin for scientific research that enhances the capabilities of LLMs by integrating a trust and verification layer through DKG. The first phase of the project involves retrieving 10k scientific papers related to machine learning field using the https://github.com/allenai/s2-folks API and publishing their metadata to the DKG.

In the following phase, the focus will be on the implentation of the plugin. This plugin will have a LLM interface anad will be able to interact with the published data in the first phase. The plugin is divided into two layers: a base layer that sets up the infrastructure for the AI plugin and an application layer that adds scientific research specific logic.

## Base layer

The base layer is an extensible layer that implements core components of the plugin. It acts as a gateway to the DKG and allows building of the application layer on the top of that. The plugin is designed to be stateless and to include application-agnostic components, such as the DKG client, cache, LLM client, and a frontend API to various LLMs.

## Application layer

Application layer is customized to assist with scientific research needs. The application layer will allow manipulation and interaction with the data published on the DKG. The list of features is ordered in such a way that each feature depends on the previous one and inherits its functionalities, enabling easier development. Key features of the application layer include:

 - **Knowledge Retrieval:** Accessing scientific papers information from the DKG by providing its metadata, ensuring verifiable and trusted data.
 - **Text-to-SPARQL:** Transforming natural language queries into SPARQL queries, performing search and retrieval of specific data from the DKG.
 - **Inference:** By utilizing data from the DKG, this feature will allow users to perform predictions, clustering, and similarity checks of the scientific papers information.
 - **Data Population:** Allowing users to add their research papers to the DKG, this plugin handles authorization with Metamask.
 - **Visualization:** Visually representing information about scientific papers in a graph form to allow analyis, discovery, and identifying outliers.

### Knowledge Retrieval

This plugin demonstrates basic DKG operations like retrieving an asset from the DKG with verifiable proofs from the blockchain. It will integrate the dkg.js within the plugin and will have a connection to one of the public OriginTrail networks.

### Text-to-SPARQL

This plugin demonstrates integration with LLM models for extracting entities and relations from natural language. It also utilizes external services to construct SPARQL queries for information retrieval.

### Inference

This plugin demonstrates the power of graph neural networks by performing inference on graph data retrieved from the network. It provides an AI layer that can be utilized for analytics purposes.

## Data Population

This plugin demonstrates integration with authentication services, such as MetaMask, allowing usage in the web3 domain.

**Visualization**

This plugin showcases the visualization of connected data provided by the DKG. It utilizes the visualization tools of the nOS and demonstrates the delivery of different formats to the end user through LLMs.

## Milestones and User Stories

This project has 6 milestones, each with its own definition of done (DoD). Here is a brief list of the milestones along with basic user stories:

 - Data collection
   - Retrieve 10k scientific papers related to machine learning from https://github.com/allenai/s2-folks
   - Convert the retrieved scientific papers into knowledge assets, so they are structured according to the existing ontologies and referenced between
   - Publish the knowledge assets to the DKG, so they can be retrieved and verified through the plugin
 - Knowledge Retrieval
   - As a user, I can ask the plugin to retrieve a paper with specific title from an author
   - As a user, I can ask the plugin to retrieve all papers from an author
   - As a user, I can manually verify the integrity proofs and ownership of retrieved assets
 - Text-to-SPARQL
   - As a user, I can ask the plugin in natural language to create a paragraph that overviews relevant papers related to a field or a scientific method with their results
   - As a user, I can ask the plugin in natural language to create a paragraph that compares my results against the most relevant ones from the DKG
   - As a user, I can ask the plugin to retrieve the most relevant papers in a field based on number of citations
   - As a user, I can ask the plugin to perform similarity check and find similar papers to the provided one
 - Inference
   - As a user, I can ask the plugin to identify research areas that are less saturated
   - As a user, I can ask the plugin to perform clustering of scientific methods in a field
   - As a user, I can ask the plugin to predict number of papers per field through months/years
   - As a user, I can ask the plugin to perform clustering of papers and authors based on their cross-citations
 - Data Population
   - As a user, I can ask the plugin to authenticate via Metamask
   - As a user, I can ask the plugin to store new knowledge assets describing scientific papers in the DKG
 - Visualization
   - As a user, I can ask the plugin to visualize an with its metadata and all connected assets

## Project Timeline

To be defined with the Steering committee at ChatDKG Office Hours.

## Expected Outcomes

Upon the completion of this project, a list of findings will be presented and the plugin will be submitted for listing on the OpenAI marketplace.

<hr>

_Please note that this is a draft proposal and can be modified based on feedback._
