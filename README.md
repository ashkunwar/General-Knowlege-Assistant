# General Knowledge Assistant

This repository contains the implementation of a General Knowledge Assistant built using Streamlit and LangChain. The assistant leverages the Groq API for LLM capabilities and integrates tools like Wikipedia API for retrieving factual information. It is designed to answer general knowledge questions, provide logical reasoning, and write essays on various topics.


## Features
- **Groq API Integration**: Utilizes the Groq LLM (llama-3.1-70b) for generating responses.
- **Wikipedia API**: Searches Wikipedia for accurate and up-to-date information when required.
- **Streamlit Interface**: A user-friendly web application interface for interactive question-answering.
- **Reasoning Tool**: Combines logical reasoning and factual information for high-quality responses.
- **Essay Writing**: Automatically generates essays with titles when requested.

## Prerequisites
- Python 3.8 or higher
- A valid Groq API key

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/ashkunwar/general-knowledge-assistant.git
   cd general-knowledge-assistant
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the Streamlit environment:
   ```bash
   streamlit run app.py
   ```

## Usage
1. **API Key**: Enter your Groq API key in the sidebar to initialize the assistant.
2. **Ask Questions**: Input your general knowledge question in the text area and click "Find my answer."
3. **Essay Writing**: Simply ask the assistant to write an essay, and it will provide a titled essay in response.
4. **Response History**: The assistant maintains a conversation history for easy reference.

## Deployed Application
Check out the live application here: [General Knowledge Assistant App](https://general-knowlege-assistant.streamlit.app/)

## File Structure
- `app.py`: The main Streamlit application file.
- `requirements.txt`: Contains the list of dependencies for the project.

## Key Components
- **StreamlitCallbackHandler**: Ensures real-time updates to the Streamlit interface during response generation.
- **WikipediaAPIWrapper**: Custom wrapper for integrating Wikipedia search functionality.
- **LangChain Tools**: Combines the Groq LLM with additional tools for enhanced reasoning and answering capabilities.

## Example
1. **Question**: "What is the capital of France?"
   - **Response**: "The capital of France is Paris."

2. **Essay Request**: "Write an essay on climate change."
   - **Response**:
     ```
     Title: The Impact of Climate Change on Our Planet
     Climate change is one of the most pressing issues of our time... (full essay continues)
     ```

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any feature additions or bug fixes.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, please contact [Ashank Kunwar](https://github.com/ashkunwar).

