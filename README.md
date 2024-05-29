# OpenAI_FunctionCalling
## Using Pre-built AI models in Fabric (OpenAI GPT-4)
Utilizing inbuilt OpenAI resource in Fabric - you dont need a seperate deployed openai resource :)

Demo also utilizes Function Calling in OpenAI GPT4, and keeps the chat history updated with the responses it sends to and gets from the function. 
This way the the llm always has the best context of where the dialog is moving.

## Using Azure OpenAI outside of Fabric (OpenAI GPT-4o)
Sample notebook configured to use a deployed GPT-4o model in Azure OpenAI outside of Fabric. The demo also utilizes Function Calling and calls Azure AI Search to retrieve information from both keyword and vector index (Hybrid Search) to accomplish RAG.

The index used in this demo is created usin the wizard experience: "Import and vectorize data" in AI Search: 
<img width="517" alt="image" src="https://github.com/7effrey89/OpenAI_FunctionCalling/assets/30802073/5121f91c-e3ab-44af-8143-faa829ccf9f6">



The final index look like this after the brochures have been ingested :
![image](https://github.com/7effrey89/OpenAI_FunctionCalling/assets/30802073/465b80c5-ccdd-48c8-8431-81228a5bd644)
