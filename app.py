import streamlit as st
import pandas as pd

from db.database import SessionLocal, init_db
from io.import_excel import import_excel
from io.export_excel import export_excels

st.set_page_config(page_title="Fleet Excel Manager", layout="wide")

st.title("Fleet Excel Manager")
st.write("Last opp Excel-fil. Kontroller data før nedlasting.")

uploaded_file = st.file_uploader(
    "Velg Excel-fil",
    type=["xlsx"]
)

if uploaded_file:
    init_db()
    session = SessionLocal()

    with st.spinner("Behandler fil..."):
        preview_rows = import_excel(
            session=session,
            excel_path=uploaded_file,
            source="upload",
        )

        exported_files = export_excels(session)

    st.success("Data tolka frå Excel")

    df_preview = pd.DataFrame(preview_rows)

    # Enkle hjelpekontrollar
    st.subheader("Forhåndsvisning")
    st.dataframe(df_preview, use_container_width=True)

    missing_res = df_preview["reservation_number"].isna().sum()
    missing_vin = df_preview["vin"].isna().sum()

    st.info(
        f"Mangler reservasjonsnummer: {missing_res} | "
        f"Mangler VIN: {missing_vin}"
    )

    st.subheader("Last ned filer")
    for filename, buffer in exported_files.items():
        st.download_button(
            label=f"Last ned {filename}",
            data=buffer,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
else:
    st.info("Last opp ei Excel-fil for å starte.")
