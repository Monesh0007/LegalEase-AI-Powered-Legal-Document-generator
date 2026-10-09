import os
from datetime import date
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="LegalEase AI", page_icon="⚖️", layout="wide")

DOCUMENT_TYPES = {
    "Non-Disclosure Agreement (NDA)": [
        "Disclosing party", "Receiving party", "Purpose of disclosure",
        "Confidential information", "Duration (e.g. 2 years)", "Governing jurisdiction"
    ],
    "Rental Agreement": [
        "Landlord full name", "Tenant full name", "Property address",
        "Monthly rent", "Security deposit", "Lease start date", "Lease end date",
        "Notice period", "Governing jurisdiction"
    ],
    "Employment Offer Letter": [
        "Employer/company name", "Candidate full name", "Job title",
        "Work location", "Annual/monthly compensation", "Start date",
        "Employment type", "Governing jurisdiction"
    ],
    "Legal Notice (General Draft)": [
        "Sender full name and address", "Recipient full name and address",
        "Background / facts", "Issue or alleged breach", "Requested resolution",
        "Deadline for response", "Governing jurisdiction"
    ],
    "Service Agreement": [
        "Service provider", "Client", "Services to be provided",
        "Fees and payment schedule", "Project start/end dates",
        "Confidentiality requirements", "Termination terms", "Governing jurisdiction"
    ],
}

DISCLAIMER = (
    "LegalEase creates a preliminary draft for review, not legal advice. Laws and required "
    "clauses vary by jurisdiction. Have a qualified lawyer review the document before signing "
    "or sending it. Do not enter highly sensitive personal information."
)

def fallback_draft(doc_type, details):
    rows = "\n".join(f"- **{key}:** {value or '[To be completed]'}" for key, value in details.items())
    return f"""# {doc_type}

**Draft date:** {date.today().isoformat()}

## Parties and key terms
{rows}

## Draft document
This document is a preliminary template prepared from the information provided above. The parties
should verify all names, dates, amounts, obligations, and jurisdiction-specific requirements before
using it.

### 1. Purpose and scope
The parties agree to the terms described in this document and to act in good faith in carrying out
their respective obligations.

### 2. Responsibilities
Each party will perform the responsibilities applicable to them as described in the agreed terms.
Any changes should be recorded in writing and acknowledged by both parties.

### 3. Term and termination
The duration, renewal, and termination conditions should be completed and checked for compliance
with applicable law before this document is used.

### 4. Disputes and governing law
The parties should specify the appropriate governing law and dispute-resolution process for their
jurisdiction. This section must be reviewed by a qualified legal professional.

### 5. Entire agreement
Once reviewed and signed by the parties, this document is intended to record their understanding
of the matters expressly described in it.

## Signatures

**Party 1:** __________________________  **Date:** ______________

**Party 2:** __________________________  **Date:** ______________

---
**Important:** This is a generic starting point, not a jurisdiction-specific legal instrument.
Please obtain legal review before relying on it.
"""

def generate_with_openai(doc_type, details, api_key):
    from openai import OpenAI
    client = OpenAI(api_key=api_key)
    prompt = f"""
Create a clear, structured FIRST DRAFT of a {doc_type}.
Use only the supplied facts; do not invent names, dates, legal citations, or terms.
If important information is missing, insert [TO BE COMPLETED] and list those items at the end.
Use neutral language and headings. State assumptions explicitly. Do not claim the document is
guaranteed enforceable or provide definitive legal advice. Include a brief note that a qualified
lawyer in the stated jurisdiction should review it before use.

User-provided details:
{details}
"""
    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=prompt
    )
    return response.output_text

st.title("⚖️ LegalEase AI")
st.caption("AI-assisted legal document drafting — create a first draft from structured details.")

with st.sidebar:
    st.header("About")
    st.write("Choose a document type, enter the key details, and generate a draft.")
    st.warning(DISCLAIMER)
    st.markdown("---")
    st.write("**AI mode:** " + ("Enabled" if os.getenv("OPENAI_API_KEY") else "Template fallback"))
    st.caption("Set OPENAI_API_KEY in your environment to enable AI drafting.")

doc_type = st.selectbox("Choose document type", list(DOCUMENT_TYPES.keys()))
st.info("Enter only information you are comfortable processing in this application.")
with st.form("document_form"):
    details = {}
    left, right = st.columns(2)
    for idx, field in enumerate(DOCUMENT_TYPES[doc_type]):
        target = left if idx % 2 == 0 else right
        with target:
            details[field] = st.text_area(field, height=75, placeholder=f"Enter {field.lower()}...")
    extra = st.text_area("Additional clauses or context (optional)", placeholder="Add any extra requirements...")
    submitted = st.form_submit_button("Generate document", type="primary", use_container_width=True)

if submitted:
    if not any(v.strip() for v in details.values()) and not extra.strip():
        st.error("Please enter at least one detail before generating a draft.")
    else:
        details["Additional clauses or context"] = extra
        with st.spinner("Preparing your draft..."):
            api_key = os.getenv("OPENAI_API_KEY", "").strip()
            try:
                if api_key:
                    draft = generate_with_openai(doc_type, details, api_key)
                else:
                    draft = fallback_draft(doc_type, details)
                st.session_state["draft"] = draft
                st.session_state["draft_type"] = doc_type
            except Exception as exc:
                st.error(f"AI generation failed. Showing a template draft instead. Details: {exc}")
                st.session_state["draft"] = fallback_draft(doc_type, details)
                st.session_state["draft_type"] = doc_type

if "draft" in st.session_state:
    st.markdown("---")
    st.subheader(f"Generated draft: {st.session_state.get('draft_type', 'Document')}")
    st.markdown(st.session_state["draft"])
    st.download_button(
        "Download draft as Markdown",
        data=st.session_state["draft"],
        file_name="legalease_draft.md",
        mime="text/markdown",
        use_container_width=True
    )
    st.caption(DISCLAIMER)
