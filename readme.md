## Project Guide

This repository contains **four projects**. Follow the steps below to set up and run each project.

### Setup Instructions
1. **Create a Virtual Environment** (Recommended)
   ```sh
   python -m venv venv
   source venv/bin/activate  ## On macOS/Linux
   venv\Scripts\activate  ## On Windows
   ```

2. **Install Required Packages**
   ```sh
   pip install -r requirements.txt
   ```

---

### Project 1: **Semantic Search**
- Navigate to the **`src/`** folder.
- Run the `semantic_search.py` script:
  ```sh
  python semantic_search.py
  ```

---

### Project 2: **Healthcare Prediction**
- This project is implemented as a Jupyter Notebook.
- Open `healthcare_prediction.ipynb` (located in the root folder) and execute the cells sequentially.
  ```sh
  jupyter notebook healthcare_prediction.ipynb
  ```

---

### Project 3: **Churn Prediction**
- This project is also a Jupyter Notebook.
- Open the notebook inside the root folder and execute the cells.
  ```sh
  jupyter notebook project3_notebook.ipynb
  ```

---

### Project 4: **Interactive Query System**
- Navigate to the **`src/`** folder.
- Run the `query.py` script:
  ```sh
  python query.py
  ```
- The script will prompt you for a query and continue the conversation.
- If you type **"start"**, it will begin a new session.
- Otherwise, it will retain the previous chat and continue.
- **API Key Requirement:** Ensure you add your API key to the src/retrieve file before running.

---

### Future Steps in RAG

To further enhance the RAG pipeline by incorporating the following improvements:

**Query Expansion** - Expanding queries to improve retrieval.

**Re-ranking Methods** - Improving the ranking of retrieved documents.

**Fusion Methods** - Combining results from multiple retrieval strategies.

**Metadata Filtering** - Filtering retrieved documents based on metadata.

**Adding Metadata** - Enriching documents with metadata for better context.

Due to time constraints, we were unable to extensively implement these features, but we may explore them in the future.

### Notes
- Ensure that all dependencies are installed before running the projects.
- If you encounter any issues, check your Python version and installed packages.


