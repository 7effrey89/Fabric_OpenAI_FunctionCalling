#!/usr/bin/env python
# coding: utf-8

# ## OpenAI Function Calling
# 
# New notebook

# 
# #### Run the cell below to install the required packages for Copilot
# 

# https://learn.microsoft.com/en-us/fabric/data-science/ai-services/ai-services-overview

# ## Ensure necessary libraries

# In[5]:


get_ipython().run_line_magic('pip', 'install openai==0.28.1')
get_ipython().run_line_magic('pip', 'install json')


# ## Use OpenAI models In Microsoft Fabric without without spinning openAI resource in Azure.

# In[6]:


import openai

#predefined models : https://learn.microsoft.com/en-us/fabric/data-science/ai-services/ai-services-overview
response = openai.ChatCompletion.create(
    deployment_id='gpt-4', # deployment_id could be one of {gpt-35-turbo, gpt-35-turbo-16k}
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Knock knock."},
        {"role": "assistant", "content": "Who's there?"},
        {"role": "user", "content": "Orange."},
    ],
    temperature=0,
)

print(f"{response.choices[0].message.role}: {response.choices[0].message.content}")


# ## Tools our LLM can use:
# 1. Regular Python Function (assign_room_number)
# 2. Regular Python Function calling an external API (extract_weather_info)

# In[7]:


import requests
from datetime import datetime
import random
import json

#Defining functions available for LLM
def assign_room_number(FirstName, LastName, Country, City):
    
    #Call external API or utilize Python functionality

    print("Python Function: 'assign_room_number' was triggered.\nNow assigning user to room..")

    random_number = random.randint(1, 10)

    returnvalue = f"Booking confirmed: FirstName: {FirstName} | LastName: {LastName}. Country: {Country} | City: {City} | Hotel room: {random_number}"

    print("Python Function: 'assign_room_number' finished and provided following value: \n" + returnvalue)

    return returnvalue

def extract_weather_info(lat, long):
    
    latitude = lat 
    longitude = long 

    #hardcoding for demo purpose
    latitude = "55.6761"  # Example: Copenhagen
    longitude = "12.5683" #

    print("Python Function: 'extract_weather_info' was triggered.\nNow calling external api..")

    # Construct the API endpoint
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"

    # Make the GET request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        current_weather = data.get('current_weather')
        # if current_weather:
        #     temperature = current_weather.get('temperature')
        #     wind_speed = current_weather.get('windspeed')
        #     time = current_weather.get('time', datetime.utcnow().isoformat())
        #     print(f"Current weather at {latitude}, {longitude} (Copenhagen):")
        #     print(f"Temperature: {temperature}°C")
        #     print(f"Wind Speed: {wind_speed} km/h")
        #     print(f"Time: {time}")
        # else:
        #     print("Current weather data not found.")
        print("Python Function: 'extract_weather_info' finished and provided following value: \n" + json.dumps(data))
    else:
        print("Failed to retrieve data.")
    
    return data

    
# Demo of the function outputs
display("assign_room_number:" + assign_room_number("jef","lai", "DK", "Cph"))
display("")
display("")
display("extract_weather_info:" + json.dumps(extract_weather_info(1,1)))


# - ## Configuration of LLM, 
# - ## Description of the "tools" the LLM can use
# - ## Enabling LLM to use a tool
# - ## Updating the chat history to provide LLM of context

# In[13]:


import openai
import json

custom_functions = [
    {
        'name': 'assign_room_number',
        'description': 'Get the user information from the body of the input text, and assign a hotel room number to the user',
        'parameters': {
            'type': 'object',
            'properties': {
                'FirstName': {
                    'type': 'string',
                    'description': 'First Name of the person'
                },
                'LastName': {
                    'type': 'string',
                    'description': 'Last Name of the person'
                },
                'Country': {
                    'type': 'string',
                    'description': 'Country the person lives in'
                },
                'City': {
                    'type': 'string',
                    'description': 'City the person lives in'
                }
                ,
                'Roomnumber': {
                    'type': 'integer',
                    'description': 'number of a hotel room'
                }
            },
            "required": ["Firstname", "Lastname", "Country", "City"]
        }
    },
    {
        "name": "extract_weather_info",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "latitude"
                },
                "longitude": {
                    "type": "number",
                    "description": "longitude"
                },
                "temperature": {
                    "type": "string",
                    "description": "temperature at city"
                }
            },
            "required": ["latitude", "longitude"]
        }
    }
]

#Configuration of the LLM
def Call_LLM_Agent(chat_history):
    return (openai.ChatCompletion.create(
        deployment_id='gpt-4', # deployment_id could be one of {gpt-35-turbo, gpt-35-turbo-16k}
        messages=chat_history,
        functions = custom_functions,
        function_call = 'auto',
        temperature=0)
    )
    #predefined models : https://learn.microsoft.com/en-us/fabric/data-science/ai-services/ai-services-overview

#Instructions to the LLM for how to execute a "Tool", and log the actions and results between user, tool, and llm to provide the LLM context of what has happend so far
def LLM_logic(response, chat_history):
    #Getting assistant message 
    response_message = response.choices[0].message

    # Call python function
    if dict(response_message).get('function_call'):
            
        # Which function call was invoked
        function_called = response_message.function_call.name
        
        # Extracting the arguments
        function_args  = json.loads(response_message.function_call.arguments)
        
        # Function names
        available_functions = {
            "assign_room_number": assign_room_number,
            "extract_weather_info": extract_weather_info
        }
        
        #determine which function to call
        fuction_to_call = available_functions[function_called]

        # append assistant's to history that we call the function and the passed arguments
        chat_history.append({"role": "assistant", "content": "null", "function_call": {"name": "" + function_called + "", "arguments": "" + json.dumps(function_args)}})

        # execute the function, and get return value from function
        custom_function_response = fuction_to_call(*list(function_args .values()))

        # append assistant's to history the result/response from the custom function
        chat_history.append({"role": "function", "name": function_called, "content": json.dumps(custom_function_response)})
        
        #after function has finished, and delivered result back to the chat history, assistant looks at chat history and provides a response to the user.
        final_message = Call_LLM_Agent(chat_history)
        final_message = final_message.choices[0].message.content
    else:
        #if not using function calling, return the llm response to user
        final_message = response_message.content

    print("\nFinal message:\n")
    print(final_message)


# In[14]:


#Start demo1: Example demonstrates LLM will choose the right tool to assign a hotel room to the user based on the conversation.
chat_history1=[
        {"role": "system", "content": "You are a helpful booking assistant in a hotel set in the world to register information about users and provide them with a room"},
        {"role": "user", "content": "My name is Jeffrey Lai"},
        {"role": "assistant", "content": "Where do you live?"},
        {"role": "user", "content": "in a city called Copenhagen that is really lovely."},
        {"role": "assistant", "content": "Which country is Copenhagen located in?"},
        {"role": "user", "content": "a small place they call Denmark which is often confused with Sweden or Germany..."},
    ]

response1 = Call_LLM_Agent(chat_history1)
LLM_logic(response1, chat_history1)


# In[15]:


#Start demo2: Example demonstrates LLM will choose the right tool to assign a get the latest weather forecast of copenhagen based on the conversation.. Same code is applied for demo1.

chat_history2=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "can you tell me what the weather is like in copenhagen?"},
    ]

response2 = Call_LLM_Agent(chat_history2)
LLM_logic(response2, chat_history2)

