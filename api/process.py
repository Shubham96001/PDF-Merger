import io
import os
from pypdf import PdfWriter, PdfReader
from http.server import BaseHTTPRequestHandler
import cgi

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse multipart form data
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            pdict['CONTENT-LENGTH'] = int(self.headers.get('Content-Length'))
            
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers.get('content-type')},
                keep_blank_values=True
            )
            
            tool = form.getvalue("tool")
            
            if not tool:
                self.send_error(400, "Missing tool parameter")
                return

            writer = PdfWriter()
            files_field = form["files"]
            if not isinstance(files_field, list):
                files_field = [files_field]
            
            if tool == "merge":
                for f in files_field:
                    reader = PdfReader(io.BytesIO(f.file.read()))
                    writer.append(reader)
                    
            elif tool == "split":
                f = files_field[0]
                pages_str = form.getvalue("pages", "")
                reader = PdfReader(io.BytesIO(f.file.read()))
                total_pages = len(reader.pages)
                
                # very basic parse like "1-3,5"
                pages_to_extract = set()
                for part in pages_str.split(','):
                    part = part.strip()
                    if '-' in part:
                        start, end = part.split('-')
                        start, end = int(start)-1, int(end)-1
                        for p in range(start, end+1):
                            if 0 <= p < total_pages:
                                pages_to_extract.add(p)
                    else:
                        if part.isdigit():
                            p = int(part)-1
                            if 0 <= p < total_pages:
                                pages_to_extract.add(p)
                                
                for p in sorted(list(pages_to_extract)):
                    writer.add_page(reader.pages[p])

            elif tool == "compress":
                f = files_field[0]
                reader = PdfReader(io.BytesIO(f.file.read()))
                for page in reader.pages:
                    writer.add_page(page)
                for page in writer.pages:
                    page.compress_content_streams()

            elif tool == "rotate":
                f = files_field[0]
                rotation = int(form.getvalue("rotation", "90"))
                reader = PdfReader(io.BytesIO(f.file.read()))
                for page in reader.pages:
                    page.rotate(rotation)
                    writer.add_page(page)

            elif tool == "password":
                f = files_field[0]
                password = form.getvalue("password", "")
                reader = PdfReader(io.BytesIO(f.file.read()))
                for page in reader.pages:
                    writer.add_page(page)
                writer.encrypt(password)

            else:
                self.send_error(400, "Unknown tool")
                return

            output = io.BytesIO()
            writer.write(output)
            output.seek(0)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/pdf')
            self.send_header('Content-Disposition', f'attachment; filename="processed_{tool}.pdf"')
            self.end_headers()
            self.wfile.write(output.read())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error processing PDF: {str(e)}".encode('utf-8'))
