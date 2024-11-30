# Parsly-v4
Medical content generation system powered by AWS services

## Project Structure
- `.github/workflows/`: CI/CD configurations
- `src/frontend/`: Streamlit UI code
- `src/backend/`: Lambda functions
- `src/config/`: AWS resources setup
- `src/tests/`: Unit and integration tests
- `src/diagrams/`: Architecture diagrams
- `src/scripts/`: Helper scripts

## Setup
1. Install dependencies:
   ```bash
   pip install -r src/frontend/requirements.txt
   pip install -r src/backend/requirements.txt
   ```
2. Configure AWS credentials
3. Deploy infrastructure:
   ```bash
   sam build && sam deploy
   ```
4. Run frontend locally:
   ```bash
   streamlit run src/frontend/app.py
   ```
