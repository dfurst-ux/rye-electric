from flask import Flask, request, jsonify, send_file
import requests
import tempfile
import os
from fill_packet import fill_pdf

app = Flask(__name__)

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://mqwbteytnawzljcszeur.supabase.co')
SERVICE_KEY = os.environ.get('SERVICE_KEY', '')

@app.route('/fill-pdf', methods=['POST'])
def fill_pdf_endpoint():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        # Download blank packet from Supabase
        pdf_res = requests.get(
            f'{SUPABASE_URL}/storage/v1/object/public/onboarding-pdfs/packet.pdf'
        )
        if not pdf_res.ok:
            return jsonify({'error': f'Could not fetch blank PDF: {pdf_res.status_code}'}), 500

        # Write blank PDF to temp file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_in:
            tmp_in.write(pdf_res.content)
            tmp_in_path = tmp_in.name

        # Write filled PDF to temp file
        tmp_out_path = tmp_in_path.replace('.pdf', '_filled.pdf')
        fill_pdf(data, tmp_in_path, tmp_out_path)

        # Upload filled PDF to Supabase
        hire_name = f"{data.get('first_name','')}-{data.get('last_name','')}"
        import time
        file_name = f"{hire_name}-{int(time.time())}.pdf"

        with open(tmp_out_path, 'rb') as f:
            upload_res = requests.post(
                f'{SUPABASE_URL}/storage/v1/object/onboarding-pdfs/{file_name}',
                headers={
                    'Content-Type': 'application/pdf',
                    'apikey': SERVICE_KEY,
                    'Authorization': f'Bearer {SERVICE_KEY}'
                },
                data=f.read()
            )

        upload_data = upload_res.json()

        # Clean up
        os.unlink(tmp_in_path)
        os.unlink(tmp_out_path)

        if upload_data.get('Key'):
            pdf_url = f"{SUPABASE_URL}/storage/v1/object/public/{upload_data['Key']}"
            return jsonify({'url': pdf_url})
        else:
            return jsonify({'error': 'Upload failed', 'detail': upload_data}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
