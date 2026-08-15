import streamlit as st
import tempfile
import os

from src.pipeline import process_statement
from src.exporter import export_csv, export_excel


st.set_page_config(
    page_title="Bank Statement Processor",
    layout="wide"
)


st.title("Bank Statement Processing & Classification System")

st.write(
    "Upload a bank statement PDF to extract, validate, "
    "classify and export transaction data."
)


uploaded_file = st.file_uploader(
    "Upload Bank Statement PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    if st.button("Process Statement"):

        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            pdf_path = temp_file.name

        try:

            # Process statement
            result = process_statement(
                pdf_path
            )

            # --------------------------------
            # Account details
            # --------------------------------

            st.subheader("Account Details")

            account_details = result[
                "account_details"
            ]

            st.write(
                account_details
            )

            # --------------------------------
            # PDF information
            # --------------------------------

            st.subheader("Document Information")

            st.write(
                "PDF Type:",
                result["pdf_type"]
            )

            st.write(
                "Pages:",
                result["page_count"]
            )

            # --------------------------------
            # Transactions
            # --------------------------------

            st.subheader(
                "Processed Transactions"
            )

            transactions = result[
                "transactions"
            ]

            st.dataframe(
                transactions,
                use_container_width=True
            )

            # --------------------------------
            # Validation
            # --------------------------------

            st.subheader("Validation")

            validation = result[
                "validation"
            ]

            if not any(validation.values()):

                st.success(
                    "All validation checks passed."
                )

            else:

                st.warning(
                    "Some validation issues were detected."
                )

                st.json(validation)

            # --------------------------------
            # Export
            # --------------------------------

            st.subheader("Export")

            os.makedirs(
                "output",
                exist_ok=True
            )

            csv_path = export_csv(
                transactions,
                "output/transactions.csv"
            )

            excel_path = export_excel(
                transactions,
                "output/transactions.xlsx"
            )

            with open(
                csv_path,
                "rb"
            ) as file:

                st.download_button(
                    label="Download CSV",
                    data=file,
                    file_name="transactions.csv",
                    mime="text/csv"
                )

            with open(
                excel_path,
                "rb"
            ) as file:

                st.download_button(
                    label="Download Excel",
                    data=file,
                    file_name="transactions.xlsx",
                    mime=(
                        "application/vnd.openxmlformats-"
                        "officedocument.spreadsheetml.sheet"
                    )
                )

        except Exception as e:

            st.error(
                f"Processing failed: {str(e)}"
            )

        finally:

            # Remove temporary uploaded PDF
            if os.path.exists(pdf_path):

                os.remove(pdf_path)