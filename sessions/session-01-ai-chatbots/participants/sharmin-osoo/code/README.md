Welcome! This **AI Chatbot** is your specialized mini-assistant for networking, community building, and finding relevant professional events near you.

## ✨ Project Overview

The **Event & Community Finder** is a conversational tool designed to streamline the process of finding local, relevant events from platforms like Meetup and Eventbrite.

### 🎯 The Core Functionality

The chatbot is specifically engineered to gather three key pieces of information from the user:

1.  **📍 Location:** Where the user is.
2.  **🗓️ Availability:** Which days the user is free.
3.  **📚 Focus Area:** Whether they seek **Tech**, **Business**, or **Career-focused** events (with the ability to refine further, e.g., 'Tech events focused on AI agents').

Once the inputs are gathered, the chatbot searches external platforms for available events.

### 💡 Expected Output

The assistant returns a short, highly useful list of matches including:
Market size and potential Market size in the next 3-5 years
– Competitors (both big and small)
– Common customer pain points
– Current market conditions & Feasibility
– Recommendations on utilising Technology to stay ahead and Systems for efficiency
– Raising Capital / Funding (local perspective, most suitable way based on their scenario) - this is optional and only return if the user requests

# How to set up 

### 1. Install Dependencies

```bash
pip install -r code/requirements.txt
```

### 2. Set Up Your API Key

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your-gemini-api-key-here
```

Get your API key: [Gemini API Key Setup Guide](../../getting-started/gemini-api-key-setup.md)


#### what is included:
chatbot.py - building of the chatbot, where we call the api, create conversation memory, and add parameters
requirements.txt - ptyhon dependencies
.env - where the API key is kept


### 3. Run the Demo

```bash
python wcc_demo.py
```


# How to run it 



# What i learned

 Model Parameters: Explored the impact of parameters like temperature (controlling randomness and creativity), and the optimal use of Top P for token selection (e.g., setting probabilities to equal 85%).
 Object-Oriented Programming (OOP): Had the opportunity to refresh and apply OOP principles in the code structure.
# Challenges faced
Initial System Prompt: The first system prompt was aiming to output a table which did not work so well when it was formatted, which made the response confusing. 
Re-acquaintance: Getting back into the rhythm of Python coding after a break, and integrating with Streamlit for the first time as the chat interface.

# Future improvements 2.0

Enhanced UI/UX: Create a more intuitive and user-friendly interface.

Context Window Integration: Implement a context window for the AI model to access external, rich information, providing more tailored and well-rounded responses.

Performance: Optimize the model's setup to potentially reduce thinking/response time.

Feature Expansion: Add functionality for users to save preferences to a file or subscribe to weekly digests.

Framework Suggestions: Integrate the ability for the AI to provide relevant professional frameworks alongside event suggestions.



