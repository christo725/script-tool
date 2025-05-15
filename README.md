# Video Script Generation Tool

A Streamlit application that converts articles into video scripts with customizable settings for different video types and presentation styles.

## Features
- Multiple video type templates (Broadcast News, TikTok, Opinion, Kids News)
- AI model selection (Claude, GPT-4, Gemini)
- Customizable presenter settings
- Adjustable tone, information density, and length
- Multi-language support
- Opinion/stance injection options
- Professional two-column script output format

## Deployment on Streamlit Cloud

1. Fork this repository to your GitHub account
2. Visit [Streamlit Cloud](https://share.streamlit.io/)
3. Sign in with your GitHub account
4. Click "New app"
5. Select this repository and the main branch
6. Set the main file path as `app.py`
7. Add the following secrets in the Streamlit Cloud dashboard:
   - `ANTHROPIC_API_KEY`
   - `OPENAI_API_KEY`
   - `GOOGLE_API_KEY`

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your API keys:
   ```
   ANTHROPIC_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here
   GOOGLE_API_KEY=your_key_here
   ```
5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Security Notes
- Never commit your API keys to the repository
- Always use environment variables for sensitive data
- Regularly update dependencies for security patches 