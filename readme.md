# Secure Document Exchange System (SEG)

This project demonstrates a secure communication system between two government ministries exchanging sensitive XML documents using:

- **Mutual TLS (mTLS)** for encrypted, authenticated channels
- **Digital signatures** for data integrity and sender verification
- **Self-signed Certificate Authority (CA)** and X.509 certificates for trust establishment
- **FastAPI** as the receiver server
- **Python requests** as the sender client

---

## Architecture

- **SEG-Sender:** Prepares, signs, and securely transmits XML documents via HTTPS with client certificate authentication.
- **SEG-Receiver:** FastAPI server that authenticates the sender via mTLS, verifies the XML signature, and returns the original XML document.

---

## Features

- Full mutual TLS authentication between sender and receiver
- RSA-SHA256 digital signatures for XML documents
- Certificate generation with OpenSSL including SAN for localhost
- Clear console logging of security events and errors

---

## Prerequisites

- Python 3.8+
- OpenSSL
- Git (optional)

---

## Setup Instructions

### 1. Clone the repository (or download source)

```bash
git clone https://github.com/Abs-Futy7/Secure-Document-Exchange-System.git
cd Secure-Document-Exchange-System
```

### 2. Create and activate a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate certificates

Navigate to the `certs` directory and run the following commands:

```bash
# Create Root CA
openssl genrsa -out rootCA.key 4096
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 3650 -out rootCA.pem -subj "/C=US/O=SecureGov/CN=RootCA"

# Create sender certificate
openssl genrsa -out sender.key 2048
openssl req -new -key sender.key -out sender.csr -subj "/C=US/O=Ministry1/CN=sender"
openssl x509 -req -in sender.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out sender.crt -days 365 -sha256

# Create receiver certificate with SAN for localhost
# Create config file 'receiver_openssl.cnf' with SAN extension (see example in docs)
openssl genrsa -out receiver.key 2048
openssl req -new -key receiver.key -out receiver.csr -config receiver_openssl.cnf
openssl x509 -req -in receiver.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial \
-out receiver.crt -days 365 -sha256 -extfile receiver_openssl.cnf -extensions req_ext
```

---

## Running the System

### Start the SEG-Receiver

```bash
python seg_receiver.py
```

You should see Uvicorn server logs indicating it’s running with TLS.

### Run the SEG-Sender (in a new terminal)

```bash
python seg_sender.py
```

The sender will output:

```
Response: {"status":"Success"}
```

The receiver console will log:

```
✅ mTLS Verified. Signature Verified.
📄 Received XML:
<Your XML document>
```

---

## Project Structure

```
Secure-Document-Exchange-System/
├── certs/                   # Certificates and keys
├── seg_receiver.py          # FastAPI receiver server
├── seg_sender.py            # Sender client script
├── xml_utils.py             # Signing and verification helpers
├── requirements.txt         # Python dependencies
├── Screenshot                 # Additional module directory (see below)
│   └── image.png           
└── README.md                # This file
```

---

## Screenshot

![Screenshot of Secure Document Exchange System UI](Screenshot/receiever.png)
![Screenshot of Secure Document Exchange System UI](Screenshot/sender.png)

---

## How It Works

1. Sender signs the XML document with its private key.
2. Sender sends the XML and signature to the receiver over HTTPS using mTLS.
3. Receiver verifies the client certificate against the root CA.
4. Receiver verifies the digital signature using sender’s public certificate.
5. If all checks pass, the receiver accepts and logs the XML document.

---

## Security Notes

- Mutual TLS ensures both parties trust each other.
- Digital signatures prevent tampering and impersonation.
- Self-signed root CA simplifies the trust model for this prototype.

---

## License

This project is released under the MIT License.

---

## Contact

For questions or support, please contact [Your Name] at [your.email@example.com].

---

Would you like me to help you generate the `receiver_openssl.cnf` example or prepare a `.gitignore` too?