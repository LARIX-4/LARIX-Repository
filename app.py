from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import json
import time
import os

DB_FILE = "larix_database.json"

class LarixServer(BaseHTTPRequestHandler):
    
    def render_html_page(self, results_html="", speed_metric="", query_val=""):
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>LARIX Repository | Guisguis NHS</title>
            
            <meta name="apple-mobile-web-app-capable" content="yes">
            <meta name="apple-mobile-web-app-status-bar-style" content="default">
            <meta name="apple-mobile-web-app-title" content="LARIX App">
            
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    background: linear-gradient(to bottom, #e8f5e9 0%, #ffffff 400px, #ffffff 100%);
                    background-attachment: fixed;
                    color: #1e392a; 
                    margin: 0; 
                    padding: 20px; 
                }}
                .container {{ max-width: 800px; margin: 0 auto; text-align: center; padding-top: 20px; }}
                
                .logo-container {{ margin-bottom: 15px; }}
                .logo-img {{ width: 120px; height: 120px; border-radius: 50%; object-fit: cover; background-color: #ffffff; border: 3px solid #2e6f40; box-shadow: 0 4px 8px rgba(0,0,0,0.05); }}
                h1 {{ color: #2e6f40; margin: 5px 0; font-size: 36px; letter-spacing: 1px; text-align: center; }}
                .app-description {{ font-size: 15px; color: #446a50; max-width: 650px; margin: 0 auto 20px auto; line-height: 1.5; font-weight: 500; text-align: center; }}
                
                .nav-bar {{ margin-bottom: 30px; text-align: center; }}
                .nav-link {{ background-color: #ffffff; border: 2px solid #2e6f40; color: #2e6f40; font-weight: bold; font-size: 14px; cursor: pointer; padding: 8px 20px; border-radius: 20px; transition: all 0.3s ease; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
                .nav-link:hover {{ background-color: #2e6f40; color: white; }}
                
                .search-box {{ display: flex; gap: 10px; max-width: 600px; margin: 0 auto 20px auto; }}
                input[type="text"] {{ flex: 1; padding: 12px; border: 2px solid #2e6f40; border-radius: 4px; font-size: 16px; outline: none; background-color: #ffffff; }}
                button[type="submit"] {{ background-color: #2e6f40; color: white; border: none; padding: 12px 28px; border-radius: 4px; font-size: 16px; cursor: pointer; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                button[type="submit"]:hover {{ background-color: #1e4b2b; }}
                
                .metrics {{ background-color: #e8f5e9; padding: 12px; border-radius: 4px; color: #1e4b2b; font-weight: bold; max-width: 600px; margin: 0 auto 20px auto; font-size: 14px; text-align: left; border-left: 4px solid #2e6f40; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
                .results-wrapper {{ max-width: 600px; margin: 0 auto; text-align: left; }}
                .result-card {{ border: 1px solid #c8e6c9; padding: 20px; border-radius: 4px; margin-bottom: 15px; background-color: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.03); }}
                .result-title {{ font-size: 18px; color: #2e6f40; font-weight: bold; margin-bottom: 5px; }}
                .result-citation {{ font-style: italic; color: #555; margin-bottom: 10px; font-size: 14px; }}
                .result-snippet {{ background-color: #fafafa; border-left: 4px solid #2e6f40; padding: 12px; margin: 10px 0; font-size: 15px; line-height: 1.5; color: #111; }}
                .result-link {{ display: inline-block; font-size: 13px; color: #2e6f40; text-decoration: none; }}
                .result-link:hover {{ text-decoration: underline; }}
                
                .modal-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 1000; justify-content: center; align-items: center; }}
                .modal-box {{ background: white; width: 90%; max-width: 650px; max-height: 85vh; padding: 30px; border-radius: 8px; border-top: 8px solid #2e6f40; overflow-y: auto; text-align: left; position: relative; }}
                .close-btn {{ position: absolute; top: 15px; right: 20px; font-size: 28px; color: #aaa; cursor: pointer; font-weight: bold; }}
                .close-btn:hover {{ color: #2e6f40; }}
                .modal-h2 {{ color: #2e6f40; border-bottom: 2px solid #e8f5e9; padding-bottom: 5px; margin-top: 25px; font-size: 20px; font-weight: bold; }}
                .mv-text {{ font-size: 14px; line-height: 1.5; background: #f9f9f9; padding: 12px; border-left: 4px solid #2e6f40; margin-top: 8px; color: #222; }}
                
                .group-photo-wrapper {{ text-align: center; margin-bottom: 20px; }}
                .group-photo {{ width: 100%; max-height: 220px; object-fit: cover; border-radius: 6px; border: 1px solid #c8e6c9; }}
                .team-member {{ margin-top: 15px; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px dashed #e8f5e9; }}
                .team-member:last-child {{ border-bottom: none; }}
                .member-name {{ font-weight: bold; color: #2e6f40; font-size: 16px; margin: 0; }}
                .member-role {{ font-size: 12px; color: #2e6f40; font-weight: bold; background-color: #e8f5e9; display: inline-block; padding: 2px 8px; border-radius: 10px; margin: 4px 0; }}
                .member-bio {{ font-size: 14px; line-height: 1.5; color: #333; margin-top: 4px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo-container">
                    <img class="logo-img" src="logo.png" alt="LARIX Logo" onerror="this.onerror=null; this.src='https://placeholder.com'">
                </div>
                
                <h1>LARIX</h1>
                <div class="app-description">Development of a Web-Based Literature Indexer and Review of Related Literature Repository in Guisguis National High School</div>
                
                <div class="nav-bar">
                    <button class="nav-link" onclick="openAboutModal()">About Us</button>
                </div>
                
                <form method="GET" action="/">
                    <div class="search-box">
                        <input type="text" name="query" placeholder="Enter keyword" value="{query_val}" required>
                        <button type="submit">Search</button>
                    </div>
                </form>
                
                <div class="results-wrapper">
                    {speed_metric}
                    {results_html}
                </div>
            </div>
            <div id="aboutModal" class="modal-overlay" onclick="closeAboutModalOutside(event)">
                <div class="modal-box">
                    <span class="close-btn" onclick="closeAboutModal()">&times;</span>
                    
                    <h2 style="color: #2e6f40; margin-top: 0; text-align: center; font-size: 24px; border-bottom: 2px solid #2e6f40; padding-bottom: 10px;">About Our Project Team</h2>
                    
                    <div class="group-photo-wrapper">
                        <img class="group-photo" src="group_photo.png" alt="LARIX Development Group Photo" onerror="this.style.display='none';">
                    </div>
                    
                    <div class="modal-h2">Vision</div>
                    <div class="mv-text">To be the leading school reference platform that provides clean, highly organized, and accurate literature resources to help high school students write their research papers with ease and confidence.</div>
                    
                    <div class="modal-h2">Mission</div>
                    <div class="mv-text">The LARIX platform aims to support student researchers by providing a simple web-based repository that delivers exact keyword search results and pre-saved text summaries, eliminating manual data errors and saving valuable study time.</div>
                    
                    <div class="modal-h2">The Research Developers</div>
                    
                    <div class="team-member">
                        <div class="member-name">Ma. Samantha Sophia P. Gelido</div>
                        <div class="member-role">Role: Team Leader & Main Compiler</div>
                        <div class="member-bio">Ma. Samantha Sophia P. Gelido is a 17-year-old STEM student at Guisguis National High School. She manages the group's task list and leads the team in gathering, checking, and putting together the reference files for the website database.</div>
                    </div>
                    
                    <div class="team-member">
                        <div class="member-name">Sunshine M. Mertola</div>
                        <div class="member-role">Role: Data Organizer & Compiler</div>
                        <div class="member-bio">Sunshine M. Mertola is a 17-year-old STEM student at Guisguis National High School. She helps collect academic materials online and specializes in sorting the files into their correct folders to make the database easy to browse.</div>
                    </div>
                    
                    <div class="team-member">
                        <div class="member-name">Romnick M. Mayo</div>
                        <div class="member-role">Role: Data Organizer & Compiler</div>
                        <div class="member-bio">Romnick M. Mayo is a 17-year-old STEM student at Guisguis National High School. He helps compile research links and works on formatting and cleaning up the text summaries before they are uploaded to the platform system.</div>
                    </div>
                    
                    <div class="team-member">
                        <div class="member-name">Justine T. Dayag</div>
                        <div class="member-role">Role: Data Organizer & Compiler</div>
                        <div class="member-bio">Justine T. Dayag is a 16-year-old STEM student at Guisguis National High School. He assists in gathering reference files, labels the database folders accurately, and helps test the platform's search functions to ensure everything works correctly.</div>
                    </div>
                </div>
            </div>
            
            <script>
                function openAboutModal() {{
                    document.getElementById('aboutModal').style.display = 'flex';
                }}
                function closeAboutModal() {{
                    document.getElementById('aboutModal').style.display = 'none';
                }}
                function closeAboutModalOutside(e) {{
                    if(e.target.id === 'aboutModal') closeAboutModal();
                }}
                
                window.addEventListener('beforeinstallprompt', (e) => {{
                    console.log('LARIX application listener registered for user home screen installation sequence handlers.');
                }});
            </script>
        </body>
        </html>
        """

    def do_GET(self):
        # Image delivery path logic to safely route and render binary graphic assets over the web network
        if self.path == "/logo.png":
            if os.path.exists("logo.png"):
                self.send_response(200)
                self.send_header("Content-type", "image/png")
                self.end_headers()
                with open("logo.png", "rb") as image_file:
                    self.wfile.write(image_file.read())
                return

        parsed_url = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed_url.query)
        
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        
        if "query" in params:
            user_query = params["query"].strip().lower()
            start_time = time.perf_counter()
            
            matched_items = []
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r", encoding="utf-8") as f:
                    database = json.load(f)
                for entry in database:
                    if user_query in entry["keyword"] or user_query in entry["title"].lower():
                        matched_items.append(entry)
                        
            end_time = time.perf_counter()
            retrieval_speed = end_time - start_time
            
            speed_metric = f"""
            <div class="metrics">
                LARIX Performance Metrics: Found {len(matched_items)} result(s) in {retrieval_speed:.6f} seconds.
            </div>
            """
            
            results_html = ""
            if matched_items:
                for item in matched_items:
                    results_html += f"""
                    <div class="result-card">
                        <div class="result-title">{item['title']}</div>
                        <div class="result-citation">Citation Reference: ({item['author_year']})</div>
                        <div class="result-snippet"><strong>Ready-to-Use RRL Snippet:</strong><br>"{item['snippet']}"</div>
                        <a class="result-link" href="{item['link']}" target="_blank">View Verified Source Link</a>
                    </div>
                    """
            else:
                results_html = "<p style='text-align: center; color: #666;'>No matching references found in the repository.</p>"
                
            response_content = self.render_html_page(results_html, speed_metric, query_val=params["query"])
        else:
            response_content = self.render_html_page()
            
        self.wfile.write(response_content.encode("utf-8"))

if __name__ == "__main__":
    # Dynamically bind to cloud framework runtime ports to deploy global internet links safely
    port_string = os.environ.get("PORT", "10000")
    PORT = int(port_string)
    
    server = HTTPServer(("0.0.0.0", PORT), LarixServer)
    print(f"LARIX Website is running smoothly on port {PORT}!")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
