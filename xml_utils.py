from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate

def sign_xml(xml_string, key_path):
    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)
    return private_key.sign(xml_string.encode(), padding.PKCS1v15(), hashes.SHA256())

def verify_signature(xml_string, signature, cert_path):
    with open(cert_path, "rb") as cert_file:
        cert = load_pem_x509_certificate(cert_file.read())
    public_key = cert.public_key()
    try:
        public_key.verify(signature, xml_string.encode(), padding.PKCS1v15(), hashes.SHA256())
        return True
    except Exception as e:
        print("❌ Signature verification error:", e)
        return False
