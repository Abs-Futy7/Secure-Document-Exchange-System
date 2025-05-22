import requests
from xml_utils import sign_xml
from datetime import datetime, timezone

def send_secure_document():
    xml = f"""<CriticalDocument id="doc123">
  <SenderID>MINISTRY 1_SEG01</SenderID>
  <ReceiverID>MINISTRY 2_SEG01</ReceiverID>
  <TimestampForSignature>{datetime.now(timezone.utc).isoformat()}Z</TimestampForSignature>
  <Payload>
    <SensitiveData>Lunch party at Saturday</SensitiveData>
    <Instructions>Deliver by 0300.</Instructions>
  </Payload>
</CriticalDocument>"""

    signature = sign_xml(xml, 'certs/sender.key')

    response = requests.post(
        "https://localhost:5001/receive",
        json={"xml": xml, "signature": signature.hex()},
        cert=('certs/sender.crt', 'certs/sender.key'),
        verify='certs/rootCA.pem'
    )

    print("Response:", response.text)

if __name__ == "__main__":
    send_secure_document()
