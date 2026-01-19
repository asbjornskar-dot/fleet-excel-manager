import streamlit as st
import pandas as pd
from pathlib import Path

# Placeholder imports – these will be wired properly next
# The goal of this step is to verify end-to-end flow
from core.model import Vehicle
from core.sync import sync_vehicle

st.set_page_config(page_title="Fleet Excel Manager", layout="centered")

st.title("Fleet Excel Manager")
st.write("Last opp Excel-fil for behandling og eksport.")

uploaded_file = st.file_uploader(
    "Velg Excel-fil",
    type=["xlsx"]
)

if uploaded_file is not None:
    st.success("Fil lastet opp")

    # Save uploaded file temporarily
    temp_dir = Path("tmp")
    temp_dir.mkdir(exist_ok=True)
    temp_file = temp_dir / uploaded_file.name

    with open(temp_file, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.write("Behandler fil...")

    # NOTE:
    # Full processing pipeline (DB + mapping + export)
    # will be connected in the next step.
    # For now, this verifies Streamlit + file handling.

    st.success("Fil mottatt og klar for prosessering.")

    st.write("Eksportfiler vil bli tilgjengelige her.")

    st.download_button(
        label="Last ned bilpleiehallen.xlsx",
        data=b"",
        file_name="bilpleiehallen.xlsx",
        disabled=True
    )

    st.download_button(
        label="Last ned Full_oversikt.xlsx",
        data=b"",
        file_name="Full_oversikt.xlsx",
        disabled=True
    )

    st.download_button(
        label="Last ned Admin.xlsx",
        data=b"",
        file_name="Admin.xlsx",
        disabled=True
    )

else:
    st.info("Ingen fil lastet opp enno.")
