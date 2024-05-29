# OpenAI_FunctionCalling
## Using Pre-built AI models in Fabric (OpenAI GPT-4)
Utilizing inbuilt OpenAI resource in Fabric - you dont need a seperate deployed openai resource :)

Demo also utilizes Function Calling in OpenAI GPT4, and keeps the chat history updated with the responses it sends to and gets from the function. 
This way the the llm always has the best context of where the dialog is moving.

## Using Azure OpenAI outside of Fabric (OpenAI GPT-4o)
Sample notebook configured to use a deployed GPT-4o model in Azure OpenAI outside of Fabric. The demo also utilizes Function Calling and calls Azure AI Search to retrieve information from both keyword and vector index (Hybrid Search) to accomplish RAG.
