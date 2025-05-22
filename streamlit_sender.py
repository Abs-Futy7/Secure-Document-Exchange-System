import streamlit as st
import requests
from xml_utils import sign_xml
from datetime import datetime, timezone

st.set_page_config(page_title="Secure XML Sender", layout="centered")
st.title("🔒 Secure XML Sender")

# Input fields for document fields
with st.form("xml_form"):
    sender_id = st.text_input("Sender ID", "MINISTRY 1_SEG01")
    receiver_id = st.text_input("Receiver ID", "MINISTRY 2_SEG01")
    sensitive_data = st.text_area("Sensitive Data", "Lunch party at Saturday", height=100)
    instructions = st.text_area("Instructions", "Deliver by 0300.", height=80)

    submitted = st.form_submit_button("Generate & Send XML")

if submitted:
    # Generate XML with current timestamp
    timestamp = datetime.now(timezone.utc).isoformat() + "Z"
    xml = f"""<CriticalDocument id="doc123">
  <SenderID>{sender_id}</SenderID>
  <ReceiverID>{receiver_id}</ReceiverID>
  <TimestampForSignature>{timestamp}</TimestampForSignature>
  <Payload>
    <SensitiveData>{sensitive_data}</SensitiveData>
    <Instructions>{instructions}</Instructions>
  </Payload>
</CriticalDocument>"""

    st.subheader("Generated XML")
    st.code(xml, language="xml")

    try:
        signature = sign_xml(xml, 'certs/sender.key')
        signature_hex = signature.hex()
        st.success("🔐 XML signed successfully.")

        url = "https://localhost:5001/receive"
        response = requests.post(
            url,
            json={"xml": xml, "signature": signature_hex},
            cert=('certs/sender.crt', 'certs/sender.key'),
            verify='certs/rootCA.pem'
        )
        st.info("📡 Sent to receiver endpoint.")
        st.write(f"Response status code: {response.status_code}")
        try:
            st.json(response.json())
        except Exception:
            st.write(response.text)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Fill the form and click 'Generate & Send XML' to sign and send your document securely.")
