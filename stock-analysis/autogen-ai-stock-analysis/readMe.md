# Stock Analysis with ReAct Agent Pattern

This project demonstrates a stock analysis tool using the ReAct agent pattern. The tool fetches stock data, analyzes it based on Warren Buffett's investment principles, and provides a recommendation.

## Setup

### 1. Set up the OpenAI API Key

You need to set up your OpenAI API key to use the ConversableAgent. Create a `.env` file in the root directory of the project and add your API key:

```plaintext
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Install Requirements

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 3. Run the Main Script

Execute the `main.py` script to start the stock analysis:

```bash
python main.py
```

## Project Structure

- `main.py`: The main script that sets up the agents, registers functions, and initiates the chat for stock analysis.
- `warren_buffet_investement_principles.txt`: A text file containing Warren Buffett's investment principles.
- `tools/`: Directory containing tools like `yahoo_finance_tool`.

## ReAct Agent Pattern

This project uses the ReAct (Reasoning and Acting) agent pattern, where two agents interact with each other to perform tasks:

- **Assistant Agent**: Suggests tool calls and provides analysis.
- **User Proxy Agent**: Executes tool calls and interacts with the assistant agent.

### Usage of Tools

The project registers several functions as tools that the agents can use:

- `yahoo_finance_tool`: Fetches stock data for a given ticker symbol.
- `read_file`: Reads the content of a file.
- `write_file`: Writes content to a file.

### Prompt

The user message prompt guides the assistant agent to perform the following steps:

1. Fetch stock data using `yahoo_finance_tool`.
2. Read Warren Buffett's investment principles from `warren_buffet_investement_principles.txt`.
3. Analyze the stock based on these principles.
4. Provide pros and cons of investing in the stock.
5. Summarize the company evaluation and provide a recommendation.
6. Give a Warren Buffett buy recommendation score from 0 to 10.
7. Write the result to `stock_analysis.md`.

## Example Output

The output will be written to `stock_analysis.md` and will include:

- Pros why Warren Buffett would invest in the company.
- Cons why Warren Buffett wouldn't invest in the company.
- Company Evaluation Summary.
- Warren Buffett Buy Recommendation.