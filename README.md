# ⚖️ NyayaDiary

**NyayaDiary** is a premium, responsive citizen legal empowerment platform. It combines a state-of-the-art Retrieval-Augmented Generation (RAG) assistant with a catalog of 58 fundamental citizen rights, offering immediate, legally-grounded answers to everyday Indian legal queries.

---

## 🌟 Key Features

### 🤖 Intelligent Legal RAG Assistant
* **Context-Aware Responses**: Queries are matched against a FAISS vector database containing 10 major Indian legal acts.
* **Prebuilt Vector Index**: Shipped directly with prebuilt FAISS embeddings (`faiss_index.bin`) and text chunks to ensure zero-delay startup without memory overhead on cloud hosts.
* **Deduplicated Source Citations**: References display clean filenames and group page numbers together (e.g. `constitution.pdf (pages: 76, 122)`) instead of repeating file badges.

### 📜 "Know Your Rights" Catalog (58+ Rights)
* **Interactive Rights Directory**: Explore 58 vital citizen rights (including internet access, equality, tenant protections, inheritance, and arrest guidelines) categorized with clean vector icons.
* **Indian-English Accent Text-to-Speech (TTS)**: Features built-in voice playback configured with an Indian-English (`en-IN`) accent so users can listen to descriptions of their rights.

### 💬 Premium User Experience
* **Voice Input**: Features built-in microphone integration utilizing the Web Speech API for real-time speech-to-text querying.
* **LocalStorage Chat Persistence**: Saves chats locally. Includes a dedicated section for **Bookmarked Chats**, inline renaming, and deletion.
* **Smart Auto-Cleanup**: Automatically filters out duplicate empty chats and clean-discards sessions that have no interaction.
* **Interactive Settings Modal**: Click your profile badge to change your display name or wipe conversation history.
* **Mobile-Responsive Drawer**: Responsive layout with drawer animations that seamlessly slides off-screen on mobile devices.

---

## 🛠️ Technology Stack

* **Frontend**: Vanilla HTML5, TailwindCSS (v3), JavaScript, Google Fonts, and Google Material Symbols.
* **Backend**: FastAPI, Uvicorn, LangChain, SentenceTransformers (`all-MiniLM-L6-v2`), FAISS (CPU), and Groq Cloud API.
* **Knowledge Base Sources**:
  1. Constitution of India
  2. Bharatiya Nyaya Sanhita (BNS)
  3. Code of Criminal Procedure (CrPC)
  4. Indian Penal Code (IPC)
  5. Information Technology Act, 2000
  6. Consumer Protection Act, 2019
  7. RTI Act, 2005
  8. RERA Act, 2016
  9. Rent Control Act
  10. Motor Vehicles Act

---

## 📂 Project Structure

```text
├── frontend/
│   ├── index.html        # Premium product landing page
│   └── chat.html         # Live RAG assistant and rights directory interface
├── nyayadiary-backend/
│   ├── data/             # Original PDF sources
│   ├── rag/              # Ingestion, embedding, and query logic
│   │   ├── faiss_index.bin  # Prebuilt FAISS vector indexes
│   │   └── texts.pkl        # Text chunk mapping
│   ├── main.py           # FastAPI entrypoint
│   └── requirements.txt  # Backend dependencies
├── .gitignore            # Version control exclusions
├── requirements.txt      # Root-level requirements fallback for Render
└── README.md             # Project documentation
```

---

## 🚀 Local Setup

### 1. Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd nyayadiary-backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `nyayadiary-backend` folder and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
5. Run the FastAPI development server:
   ```bash
   uvicorn main:app --reload
   ```

### 2. Frontend Setup
Open the `frontend` folder using any static web server (such as Python's built-in HTTP server):
```bash
python -m http.server 3000 --directory frontend
```
Open `http://localhost:3000` in your browser.

---

## 🌐 Production Deployment

### Backend (Render)
1. Link your GitHub repository in Render and create a new **Web Service**.
2. Set **Build Command**: `pip install -r requirements.txt`
3. Set **Start Command**: `cd nyayadiary-backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Under **Environment**, add the key `GROQ_API_KEY` with your credentials.
5. Deploy.

### Frontend (Vercel)
1. Import the repository in Vercel.
2. Set the **Root Directory** to `frontend`.
3. Click **Deploy**.
4. *(Optional)* If your Render URL differs from `https://nyayadiary-backend.onrender.com`, update line 409 in `frontend/chat.html` with your actual backend URL and push the changes.
