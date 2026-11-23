from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import os

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/aircraft"):
            url = "https://opendata.adsb.fi/api/v3/lat/51.8747/lon/-0.3683/dist/35"
            try:
                request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urlopen(request, timeout=15) as response:
                    data = response.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(data)
            except Exception as error:
                message = str(error).encode()
                self.send_error(502, message.decode())
            return

        if self.path.split("?")[0] == "/luton_airport_live_dashboard.html":
            try:
                with open("luton_airport_live_dashboard.html", "r", encoding="utf-8") as file:
                    page = file.read()
                page = page.replace(
                    "https://opendata.adsb.fi/api/v3/lat/${LAT}/lon/${LON}/dist/35",
                    "/aircraft"
                )
                content = page.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception:
                self.send_error(500, "Could not load dashboard")
            return

        super().do_GET()
port = int(os.environ.get("PORT", 8000))
print(f"Luton dashboard server running on port {port}")

ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
