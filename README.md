# Document verification Tool

This is a language translation tool built using Flask and OpenAI's GPT-4 model. Users can upload text file with the information written in it and check the information text from it OpenAI Database the this information is correct or not and will provide corrected information.

## Getting Started

### Running Locally

1. **Clone the repository:**

   ```bash
   git clone https://github.com/inoor18/Document-Verification-using-openAI.git
   cd Document-Verification-using-openAI

   ```

2. **Setup virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate

   ```

3. **Install required dependencies:**

   ```bash
   pip install -r requirements.txt

   ```

4. **Create environment variable file:**

   ```bash
   touch .env
   Paste the following line in .env file.Replace API_KEY with Open AI API key
   OPENAI_API_KEY="API_KEY"

   ```

5. **Run the app:**

```bash
cd web_interface
python3 app.py

Open your browser and navigate to http://127.0.0.1:5000/.
```
