# AI-Powered HCP CRM (Life Sciences)

An intelligent, full-stack Customer Relationship Management (CRM) prototype designed for Pharmaceutical Sales Representatives. This application uses an AI agent to listen to natural language descriptions of meetings with Healthcare Professionals (HCPs) and automatically updates a structured CRM form, seamlessly saving the data to a PostgreSQL database.

## 🚀 Architecture & Tech Stack

This project was built to strictly satisfy the assignment requirements:

- **Frontend:** React.js
- **State Management:** Redux Toolkit (`react-redux`, `@reduxjs/toolkit`)
- **Backend:** Python 3.x with FastAPI
- **AI Agent Framework:** LangGraph (`langgraph`, `langchain-core`)
- **LLM Provider:** Groq (Model: `llama-3.3-70b-versatile` for reliable tool execution)
- **Database:** PostgreSQL with SQLAlchemy (`psycopg2-binary`)

## 🛠️ AI Tool Integration (LangGraph)

The LangGraph agent is equipped with **5 specific tools** to handle HCP interactions:

1.  **`log_interaction_tool` (Mandatory):** Extracts HCP Name, date, topics, sentiment, and materials from a new meeting description.
2.  **`edit_interaction_tool` (Mandatory):** Allows the user to naturally correct specific fields (e.g., _"Change the sentiment to positive"_).
3.  **`fetch_hcp_history_tool`:** Retrieves mock historical data about a specific doctor's preferences and past meetings.
4.  **`suggest_materials_tool`:** Recommends specific pharmaceutical brochures or clinical trial PDFs based on the medical topic discussed.
5.  **`generate_follow_ups_tool`:** Analyzes the meeting sentiment and topics to automatically generate actionable next steps.

---

## ⚙️ Local Setup Instructions

### Prerequisites

- Node.js
- Python
- PostgreSQL & DBeaver (or another SQL client)
- A free API key from [Groq](https://console.groq.com/keys)

### 1. Database Setup

1. Open DBeaver and connect to your local PostgreSQL server.
2. Create a new database named **`hcp_crm`**.
3. (SQLAlchemy will automatically create the required tables when the backend starts).

### 2. Backend Setup (FastAPI & AI)

1. Open a terminal and navigate to the backend directory:
   ```bash
   cd hcp-crm-backend
   ```
2. Create and activate a virtual environment:
   ````bash
   python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On Mac/Linux:
    source venv/bin/activate
    ```
   ````
3. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic python-dotenv langchain-groq langgraph sqlalchemy psycopg2-binary
   ```
4. Configure Environment Variables:
   - Create a file named .env in the hcp-crm-backend folder.
   - Add your Groq API key:
     ```Code snippet
     GROQ_API_KEY=gsk_your_actual_key_here
     ```

5. Update Database Credentials:
   - Open **`database.py`** and ensure the **`SQLALCHEMY_DATABASE_URL`** matches your local Postgres credentials.

6. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

   The backend will run on http://127.0.0.1:8000

### 3. Frontend Setup (React & Redux)

1. Open a new terminal and navigate to the frontend directory:
   `bash cd hcp-crm-frontend `

2. Install dependencies:
   `bash npm install`

3. Start the React development server:
   `bash npm start`

- The app will open automatically at http://localhost:3000

### 🧪 How to Use the App

Once both servers are running, try chatting with the AI on the right side of the screen.

### Test Prompt 1 (Logging & Follow-ups):

"I met with Dr. Sharma today. We discussed the new OncoBoost trials. He seemed very positive about it."
(Watch the form auto-fill the details and automatically generate follow-up actions).

### Test Prompt 2 (Editing):

"Actually, change the sentiment to neutral."
(Watch the radio button change on the left panel).

### Test Prompt 3 (Tool Invocation):

"What materials should I send him based on our conversation?"
(Watch the AI use the materials tool to suggest Oncology PDFs).

Check your PostgreSQL interactions table in DBeaver to verify that the final meeting state was permanently saved!
