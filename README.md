# Kink Tool 

A premium, AI-powered web application that helps users discover their perfect adult star match based on personalized preferences. Built with Streamlit and Google's Gemini AI, wrapped in a beautiful, handcrafted glassmorphism UI.

## Features
- **AI-Powered Matching**: Uses Google's `gemini-1.5-flash` (or custom models) to intelligently process user preferences (sexuality, age range, body features).
- **Premium UI/UX**: Features a highly responsive, custom-built CSS glassmorphism interface floating over an animated, dynamic fractal gradient background.
- **Dynamic Image Fetching**: Automatically retrieves high-quality thumbnails of the matched stars using the Wikipedia API, with smart fallbacks for unlisted names.
- **Structured JSON Prompts**: Uses Langchain to strictly enforce formatted JSON outputs from the LLM, ensuring reliable frontend rendering.

## Live Demo
https://kink-tool-9dfm6xrmdjwfusad26mqkw.streamlit.app/

---

## 🛠️ Installation & Setup (Local)

### 1. Clone the repository
```bash
git clone https://github.com/AyushSGO07/Kink-Tool.git
cd Kink-Tool
```

### 2. Install dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Setup your Environment Variables
Create a `.env` file in the root directory and add your Google Gemini API Key:
```env
GOOGLE_API_KEY="your-api-key-here"
```

### 4. Run the app
Start the Streamlit server:
```bash
streamlit run Kink_Tool.py
```

---

## 📁 File Structure
- `Kink_Tool.py`: The main Streamlit application containing the UI, CSS, and API logic.
- `prompt.json`: The Langchain prompt template defining the AI's behavior and JSON schema.
- `requirements.txt`: Python dependencies required to run the app.
- `.env`: (Ignored via git) Stores sensitive API keys.

## Design
The application interface uses raw CSS injected into Streamlit to override defaults. It features:
- Backdrop-filter blurring for frosted glass effects
- Soft glowing borders and shadows
- Smooth cubic-bezier hover transitions
- Scaled up, readable typography using the *Inter* font family.

## License
This project is for educational and entertainment purposes. Ensure you comply with Google Gemini's API terms of service when deploying applications that handle mature themes.
