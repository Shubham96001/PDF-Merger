import io
import os
from flask import Flask, request, send_file, jsonify, send_from_directory
from pypdf import PdfWriter, PdfReader

app = Flask(__name__, static_folder='.', static_url_path='')

# ── Serve the frontend ──────────────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ── PDF Processing endpoint ─────────────────────────────────────────────────
@app.route('/api/process', methods=['POST'])
def process_pdf():
    tool = request.form.get('tool')
    if not tool:
        return jsonify({'error': 'Missing tool parameter'}), 400

    uploaded_files = request.files.getlist('files')
    if not uploaded_files or all(f.filename == '' for f in uploaded_files):
        return jsonify({'error': 'No files uploaded'}), 400

    writer = PdfWriter()

    try:
        if tool == 'merge':
            for f in uploaded_files:
                reader = PdfReader(io.BytesIO(f.read()))
                writer.append(reader)

        elif tool == 'rotate':
            rotation = int(request.form.get('rotation', '90'))
            f = uploaded_files[0]
            reader = PdfReader(io.BytesIO(f.read()))
            for page in reader.pages:
                page.rotate(rotation)
                writer.add_page(page)

        elif tool == 'password':
            password = request.form.get('password', '')
            if not password:
                return jsonify({'error': 'Password cannot be empty'}), 400
            f = uploaded_files[0]
            reader = PdfReader(io.BytesIO(f.read()))
            for page in reader.pages:
                writer.add_page(page)
            writer.encrypt(password)

        else:
            return jsonify({'error': f'Unknown tool: {tool}'}), 400

        output = io.BytesIO()
        writer.write(output)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'processed_{tool}.pdf'
        )

    except Exception as e:
        return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500


if __name__ == '__main__':
    print("=" * 55)
    print("  PDF Processor Server Running!")
    print("  Open: http://localhost:8000")
    print("=" * 55)
    app.run(port=8000, debug=False)
