
# Simple Chat Agent

A lightweight conversational AI built with the OpenAI API that maintains full chat history for contextual conversations.

## ✨ Features

- **Persistent Chat History**: Maintains conversation context across multiple turns
- **Simple CLI Interface**: Easy-to-use command-line chat experience
- **Configurable Model**: Supports `gpt-4o-mini` (default) or `gpt-4o`
- **Environment-Based Security**: API key management via `.env` file
- **Graceful Exit**: Type `quit`, `exit`, or `bye` to end conversation


## 📋 Prerequisites

- Python 3.8+
- OpenAI API key from [platform.openai.com](https://platform.openai.com)
- Required packages: `openai`, `python-dotenv`


## 🚀 Quick Start

### 1. Clone \& Install Dependencies

```bash
pip install openai python-dotenv
```


### 2. Set Up Environment

Create a `.env` file in your project root (or update the hardcoded path in code):

```
OPENAI_API_KEY=your-api-key-here
```


### 3. Run the Chat Agent

```bash
python chat_agent.py
```


## 💬 Usage

```
Chat Agent Started! (Type 'quit' to exit)
--------------------------------------------------

You: Hello, how are you?
Assistant: I'm doing great, thanks for asking! How can I help you today?

You: quit
Goodbye!
```


## ⚙️ Configuration

### API Key Setup (2 Options)

**Option 1: Environment Variable (Recommended)**

```python
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

**Option 2: Direct Key**

```python
client = OpenAI(api_key="your-api-key-here")
```


### Model Parameters

```python
model="gpt-4o-mini"  # Fast & cost-effective
# model="gpt-4o"     # Higher quality responses
temperature=0.7      # Creativity level (0-2)
max_tokens=500       # Max response length
```


## 🛠️ Customization

- **System Prompt**: Modify the initial `messages` list
- **Model**: Change `gpt-4o-mini` to any supported OpenAI model
- **Temperature**: Adjust between 0 (deterministic) and 2 (creative)
- **Environment Path**: Update `env_path` for your `.env` location


## 📁 Project Structure

```
chat_agent/
├── chat_agent.py      # Main application
├── Variables.env      # Environment variables (gitignored)
├── README.md         # This file
└── requirements.txt  # Dependencies
```


## 🔧 Troubleshooting

| Issue | Solution |
| :-- | :-- |
| `Error: Invalid API key` | Verify `OPENAI_API_KEY` in `.env` file |
| `ModuleNotFoundError` | Run `pip install openai python-dotenv` |
| `FileNotFoundError` | Check `env_path` matches your `.env` location |
| Rate limits | Upgrade OpenAI plan or add retry logic |

## 🚀 Next Steps

Enhance your agent with:

- Streaming responses
- Conversation persistence to file/database
- Multi-model support
- Custom system prompts
- Voice input/output


## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

***

**Built with ❤️ using OpenAI API**

***

Would you like me to add a `requirements.txt` file, enhance any specific section, or customize it for a particular deployment scenario (like GitHub repo or enterprise use)?

