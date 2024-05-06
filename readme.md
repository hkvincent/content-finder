# LlamaIndex Search Interface

This application provides a graphical user interface to interact with the LlamaIndex library, allowing users to index documents and perform searches on the indexed data. It uses OpenAI's embedding and language models to enhance search capabilities.

## Features

- Browse for and select a directory to index.
- Index documents found within the selected directory.
- Perform text queries against the indexed documents.
- Display search results in an interactive and user-friendly format.

## Requirements

- Python 3.7 or higher
- `tkinter` for the GUI
- `llama_index` library
- `dotenv` for environment management
- OpenAI API key

## Setup

1. **Clone the repository:**
  clone the repository to your local machine using the following command:
  ```bash
  git clone
  ```

2. **Install dependencies:**
Ensure you have Python and pip installed, then run:
pip install -r requirements.txt


3. **Environment Configuration:**
Create a `.env` file in the root directory of the project and add your OpenAI API key:
OPENAI_API_KEY='your_openai_api_key_here'
OPENAI_BASE_URL='https://api.openai.com/v1'
OPENAI_MODEL='gpt-3.5-turbo'
OPENAI_EMBED_MODEL='text-embedding-ada-002'



## Usage

1. **Start the Application:**
Run the program by executing:
python main.py


2. **Index Folder:**
Use the 'Browse' button to select the directory you wish to index. The application will automatically index the documents in the selected directory.

3. **Search Queries:**
Enter a query in the 'Enter Search Query' field and click 'Search'. Results will be displayed in the main text area.

## Troubleshooting

- **API Key Errors:** Ensure your `.env` file is correctly configured with your OpenAI API key.
- **Dependency Issues:** Make sure all required Python packages are installed. Re-run `pip install -r requirements.txt` if unsure.
- **Indexing Errors:** Verify that the directory selected contains readable documents and that you have permission to read the files.

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your enhancements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
