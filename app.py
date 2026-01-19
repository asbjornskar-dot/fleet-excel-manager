import streamlit as st
from pathlib import Path

from db.database import SessionLocal, init_db
from io.import_excel import import_excel
from io.export_excel import export_excels

st.set_page_config(page_title="Fleet Excel Manager", layout="centered")

st.title("Fleet Excel Manager")
st.write("Last opp Excel-fil. Filer blir generert for nedlasting.")

uploaded_file = st.file_uploader(
    "Velg Excel-fil",
    type=["xlsx"]
)

if uploaded_file:
    init_db()
    session = SessionLocal()

    with st.spinner("Behandler fil..."):
        import_excel(
            session=session,
            excel_path=uploaded_file,
            source="upload",
        )

        exported_files = export_excels(session)

    st.success("Ferdig! Last ned filer:")

    for filename, buffer in exported_files.items():
        st.download_button(
            label=f"Last ned {filename}",
            data=buffer,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
else:
    st.info("Last opp ei Excel-fil for å starte.")
