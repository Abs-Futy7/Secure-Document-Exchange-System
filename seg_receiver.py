from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from xml_utils import verify_signature
import uvicorn
import ssl

app = FastAPI()

@app.post("/receive")
async def receive_document(request: Request):
    try:
        data = await request.json()
        xml = data['xml']
        signature = bytes.fromhex(data['signature'])

        if not verify_signature(xml, signature, 'certs/sender.crt'):
            return JSONResponse(content={"error": "Signature verification failed."}, status_code=400)

        print("✅ mTLS Verified. Signature Verified.")
        print("📄 Received XML:\n", xml)
        return {"status": "Success"}

    except Exception as e:
        print("❌ Error:", str(e))
        return JSONResponse(content={"error": str(e)}, status_code=400)

if __name__ == "__main__":
    uvicorn.run("seg_receiver:app",
                host="0.0.0.0",
                port=5001,
                ssl_certfile="certs/receiver.crt",
                ssl_keyfile="certs/receiver.key",
                ssl_ca_certs="certs/rootCA.pem",
                ssl_cert_reqs=ssl.CERT_REQUIRED)
