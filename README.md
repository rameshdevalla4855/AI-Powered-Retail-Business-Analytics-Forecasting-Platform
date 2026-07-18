# RetailIQ AI

RetailIQ AI is an end-to-end AI-powered retail analytics platform built with Python and Streamlit. It combines business analytics, forecasting, segmentation, recommendation, and a natural-language analytics experience.

## Run locally

```bash
pip install -r requirements.txt
streamlit run dashboard/Home.py
```

## Project structure

- dashboard/: Streamlit app pages and reusable components
- src/: Backend analytics, forecasting, recommendation, segmentation, and data loading modules
- data/: Raw, cleaned, and processed datasets
- models/: Trained model artifacts

## Deployment

The app is prepared for Streamlit Community Cloud using the entry point in streamlit_app.py.
