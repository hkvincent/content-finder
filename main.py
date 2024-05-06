import os
import shutil
import tkinter as tk
from tkinter import filedialog, scrolledtext, Checkbutton, IntVar, messagebox
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    ServiceContext,
)
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from dotenv import load_dotenv


class LlamaIndexGUI:
    def __init__(self, master):
        self.master = master
        master.title("LlamaIndex Search Interface")

        # Configure the grid to allow for dynamic resizing
        master.grid_rowconfigure(3, weight=1)  # Give weight to the results field row
        master.grid_columnconfigure(
            1, weight=1
        )  # Allow the index path entry and results field to expand

        # Controls Row
        self.load_type = IntVar()
        self.file_checkbutton = Checkbutton(
            master,
            text="Single File",
            variable=self.load_type,
            command=self.toggle_load_type,
        )
        self.file_checkbutton.grid(row=0, column=0, sticky="ew")
        self.delete_button = tk.Button(
            master, text="Delete Storage", command=self.delete_storage
        )
        self.delete_button.grid(row=0, column=3, sticky="ew", padx=5)

        # Entry for Index Path
        tk.Label(master, text="Index Path:").grid(row=1, column=0, sticky="w")
        self.index_path_entry = tk.Entry(master)
        self.index_path_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5)
        self.browse_button = tk.Button(master, text="Browse", command=self.browse_path)
        self.browse_button.grid(row=1, column=3, sticky="ew")

        # Search Entry
        tk.Label(master, text="Enter Search Query:").grid(row=2, column=0, sticky="w")
        self.query_entry = tk.Entry(master)
        self.query_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=5)
        self.search_button = tk.Button(
            master, text="Search", command=self.perform_search
        )
        self.search_button.grid(row=2, column=3, sticky="ew")

        # Text Field for Results
        self.results_field = scrolledtext.ScrolledText(master)
        self.results_field.grid(
            row=3, column=0, columnspan=4, sticky="nsew", padx=5, pady=5
        )

        # Initialize index
        self.index = None

    def toggle_load_type(self):
        # Change button text based on the checkbox
        if self.load_type.get() == 1:
            self.browse_button.config(text="Browse File")
        else:
            self.browse_button.config(text="Browse Folder")

    def browse_path(self):
        if self.load_type.get() == 1:
            path_selected = filedialog.askopenfilename()
        else:
            path_selected = filedialog.askdirectory()
        if path_selected:
            self.index_path_entry.delete(0, tk.END)
            self.index_path_entry.insert(0, path_selected)
            self.initialize_index(path_selected)

    def initialize_index(self, index_path):
        try:
            # Load index if already exists
            storage_context = StorageContext.from_defaults(persist_dir="./storage")
            service_context = get_service_context()
            self.index = load_index_from_storage(
                storage_context, service_context=service_context
            )
        except Exception as e:
            print("Failed to load index:", e)
            service_context = get_service_context()
            if self.load_type.get() == 1:
                documents = [load_single_file(index_path)]
            else:
                documents = SimpleDirectoryReader(
                    index_path, recursive=True, filename_as_id=True
                ).load_data()
            self.index = VectorStoreIndex.from_documents(
                documents, service_context=service_context
            )
            self.index.storage_context.persist()
        self.results_field.insert(tk.END, "Index initialized successfully.\n")

    def perform_search(self):
        query = self.query_entry.get()
        if not self.index:
            self.results_field.insert(tk.END, "Index is not initialized.\n")
            return
        response = self.index.as_query_engine().query(query)
        self.results_field.insert(
            tk.END,
            f"{query} Results:\n{response}\n{response.get_formatted_sources()}\n",
        )

    def delete_storage(self):
        # Confirm deletion with the user
        if messagebox.askyesno(
            "Confirm Deletion", "Are you sure you want to delete the storage?"
        ):
            try:
                shutil.rmtree("./storage")
                self.results_field.insert(tk.END, "Storage deleted successfully.\n")
            except Exception as e:
                self.results_field.insert(tk.END, f"Failed to delete storage: {e}\n")


def load_single_file(file_path):
    with open(file_path, "r") as file:
        return {"text": file.read()}  # Simulating a document object


def get_service_context():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    llm_model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    embed_model = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-ada-002")
    llm_engine = OpenAI(model=llm_model, api_key=api_key, api_base=api_base)
    embed_engine = OpenAIEmbedding(
        model=embed_model, api_key=api_key, api_base=api_base
    )
    return ServiceContext.from_defaults(llm=llm_engine, embed_model=embed_engine)


if __name__ == "__main__":
    root = tk.Tk()
    gui = LlamaIndexGUI(root)
    root.mainloop()
