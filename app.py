import streamlit as st
from pathlib import Path

from db.database import SessionLocal, init_db
from io.import_excel import import_excel
from io.export_excel import export_excels

st.set_page_config(page_title="Fleet Excel Manager", layout="centered")

st.title("Fleet Excel Manager")

uploaded_file = st.file_uploader(
    "Last opp Excel-fil",
    type=["xlsx"]
)

if uploaded_file is not None:
    init_db()
    session = SessionLocal()

    temp_dir = Path("tmp")
    temp_dir.mkdir(exist_ok=True)
    temp_file = temp_dir / uploaded_file.name

    with open(temp_file, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner("Behandler fil..."):
        import_excel(
            session=session,
            excel_path=str(temp_file),
            source="full",
        )

        export_excels(session=session)

    st.success("Ferdig! Last ned filer:")

    for filename in [
        "bilpleiehallen.xlsx",
        "Full_oversikt.xlsx",
        "Admin.xlsx",
    ]:
        if Path(filename).exists():
            with open(filename, "rb") as f:
                st.download_button(
                    label=f"Last ned {filename}",
                    data=f.read(),
                    file_name=filename,
                )

else:
    st.info("Last opp ei Excel-fil for å starte.")
