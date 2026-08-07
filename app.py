import os
import json
import time
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

DB_FILE = "larix_database.json"

class LarixServer(BaseHTTPRequestHandler):
    
    def get_about_and_script(self):
        return """
        <div id="aboutModal" class="modal-overlay" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); z-index: 2000; align-items: center; justify-content: center;" onclick="closeAboutModalOutside(event)">
            <div class="modal-box" style="background: #ffffff; padding: 30px; border-radius: 8px; max-width: 600px; width: 90%; max-height: 85vh; overflow-y: auto; box-shadow: 0 4px 15px rgba(0,0,0,0.2); position: relative; margin: auto;">
                <span class="close-btn" style="position: absolute; top: 15px; right: 20px; font-size: 28px; font-weight: bold; color: #aaa; cursor: pointer;" onclick="closeAboutModal()">&times;</span>
                <h2 style="color:#2e6f40;margin-top:0;text-align:center;font-size:24px;border-bottom:2px solid #2e6f40;padding-bottom:10px;">About Our Project Team</h2>
                <div class="group-photo-wrapper" style="text-align:center; margin-bottom:15px;">
                    <img class="group-photo" src="/logo.png" alt="LARIX Group Photo" style="max-width:120px; height:120px; border-radius:50%; object-fit:cover;" onerror="this.style.display='none';">
                </div>
                <div class="modal-h2" style="color:#2e6f40; font-weight:bold; font-size:18px; margin-top:15px;">Vision</div>
                <div class="mv-text" style="font-size:14px; line-height:1.5; margin-bottom:10px;">To be the leading school reference platform that provides highly organized and accurate literature resources to help high school students write their research papers with ease and confidence.</div>
                <div class="modal-h2" style="color:#2e6f40; font-weight:bold; font-size:18px; margin-top:15px;">Mission</div>
                <div class="mv-text" style="font-size:14px; line-height:1.5; margin-bottom:15px;">The LARIX platform aims to support student researchers by providing a simple web-based repository that delivers exact keyword search results and pre-saved text summaries, eliminating manual data errors and saving valuable study time.</div>
                
                <div class="modal-h2" style="color:#2e6f40; font-weight:bold; font-size:18px; margin-top:20px; border-top:1px solid #eee; padding-top:10px;">The Research Developers</div>
                <div class="team-member" style="margin-bottom:15px;">
                    <div class="member-name" style="font-weight:bold; color:#1e4b2b;">Ma. Samantha Sophia P. Gelido</div>
                    <div class="member-role" style="font-size:13px; font-style:italic; color:#555;">Role: Team Leader & Main Compiler</div>
                    <div class="member-bio" style="font-size:13px; line-height:1.4;">Ma. Samantha Sophia P. Gelido is a 17-year-old STEM student at Guisguis National High School. She manages the group's task list and leads the team in gathering, checking, and putting together the reference files for the website database.</div>
                </div>
                <div class="team-member" style="margin-bottom:15px;">
                    <div class="member-name" style="font-weight:bold; color:#1e4b2b;">Sunshine M. Mertola</div>
                    <div class="member-role" style="font-size:13px; font-style:italic; color:#555;">Role: Data Organizer & Compiler</div>
                    <div class="member-bio" style="font-size:13px; line-height:1.4;">Sunshine M. Mertola is a 17-year-old STEM student at Guisguis National High School. She helps collect academic materials online and specializes in sorting the files into their correct folders to make the database easy to browse.</div>
                </div>
                <div class="team-member" style="margin-bottom:15px;">
                    <div class="member-name" style="font-weight:bold; color:#1e4b2b;">Romnick M. Mayo</div>
                    <div class="member-role" style="font-size:13px; font-style:italic; color:#555;">Role: Data Organizer & Compiler</div>
                    <div class="member-bio" style="font-size:13px; line-height:1.4;">Romnick M. Mayo is a 17-year-old STEM student at Guisguis National High School. He helps compile research links and works on formatting and cleaning up the text summaries before they are uploaded to the platform system.</div>
                </div>
                <div class="team-member" style="margin-bottom:15px;">
                    <div class="member-name" style="font-weight:bold; color:#1e4b2b;">Justine T. Dayag</div>
                    <div class="member-role" style="font-size:13px; font-style:italic; color:#555;">Role: Data Organizer & Compiler</div>
                    <div class="member-bio" style="font-size:13px; line-height:1.4;">Justine T. Dayag is a 16-year-old STEM student at Guisguis National High School. He assists in gathering reference files, labels the database folders accurately, and helps test the platform's search functions to ensure everything works correctly.</div>
                </div>
            </div>
        </div>
        """
    def get_application_script(self):
        return """
        <div id="pwaBanner" class="pwa-banner" style="display:none;"><p class="pwa-text"><strong>LARIX Repository App</strong><br>Add to your homescreen for instant offline access.</p><button id="pwaInstallBtn" class="pwa-btn">Install</button></div>
        <script>
            function toggleSidebar(){
                const s=document.getElementById('sidebar'),o=document.getElementById('sidebarOverlay');
                s.classList.toggle('active'); if(o) o.style.display=s.classList.contains('active')?'block':'none';
            }
            function openAboutModal(){ document.getElementById('aboutModal').style.display='flex'; toggleSidebar(); }
            function closeAboutModal(){ document.getElementById('aboutModal').style.display='none'; }
            function closeAboutModalOutside(e){ if(e.target.id==='aboutModal') closeAboutModal(); }
            
            const sf = document.getElementById('searchForm');
            if(sf) {
                sf.addEventListener('submit',function(){
                    const q=document.getElementById('searchInput').value.trim();
                    if(q){
                        let h=JSON.parse(localStorage.getItem('larix_history')||'[]');
                        if(!h.includes(q)){ h.unshift(q); if(h.length>5) h.pop(); localStorage.setItem('larix_history',JSON.stringify(h)); }
                    }
                });
            }
            
            function renderHistory(){
                const l=document.getElementById('historyList'); if(!l) return;
                const h=JSON.parse(localStorage.getItem('larix_history')||'[]');
                if(h.length===0){ l.innerHTML='<p style="color:#aaa;font-style:italic;margin:5px 0;">No history recorded.</p>'; return; }
                l.innerHTML=h.map(q=>`<a href="/?query=${encodeURIComponent(q)}" class="history-item">🔍 ${q}</a>`).join('');
            }
            function toggleSaveResearch(btn, id, title, link){
                let s=JSON.parse(localStorage.getItem('larix_saved')||'[]'); const idx=s.findIndex(item=>item.id===id);
                if(idx>-1){ s.splice(idx,1); btn.classList.remove('saved'); btn.innerHTML='☆'; }
                else{ s.push({id:id,title:title,link:link}); btn.classList.add('saved'); btn.innerHTML='★'; }
                localStorage.setItem('larix_saved',JSON.stringify(s)); renderSavedList();
            }
            function renderSavedList(){
                const l=document.getElementById('savedList'); if(!l) return;
                const s=JSON.parse(localStorage.getItem('larix_saved')||'[]');
                if(s.length===0){ l.innerHTML='<p style="color:#aaa;font-style:italic;margin:5px 0;">No saved researches yet.</p>'; return; }
                l.innerHTML=s.map(item=>`<li class="saved-item" style="margin-bottom:8px;font-size:14px;"><a class="saved-item-link" href="${item.link}" target="_blank" style="color:#2e6f40;text-decoration:none;">${item.title}</a><span class="remove-saved" onclick="removeSavedItem('${item.id}')" style="color:#d32f2f; margin-left:10px; cursor:pointer; font-size:12px;">✕</span></li>`).join('');
                document.querySelectorAll('.save-btn').forEach(btn=>{ const id=btn.getAttribute('data-id'); if(s.some(item=>item.id===id)){ btn.classList.add('saved'); btn.innerHTML='★'; } });
            }
            function removeSavedItem(id){ let s=JSON.parse(localStorage.getItem('larix_saved')||'[]'); s=s.filter(item=>item.id!==id); localStorage.setItem('larix_saved',JSON.stringify(s)); renderSavedList(); }
            function clearData(){ if(confirm("Are you sure you want to clear your local data?")){ localStorage.removeItem('larix_history'); localStorage.removeItem('larix_saved'); renderHistory(); renderSavedList(); } }
            let deferredPrompt; window.addEventListener('beforeinstallprompt',(e)=>{ e.preventDefault(); deferredPrompt=e; const pb=document.getElementById('pwaBanner'); if(pb) pb.style.display='flex'; });
            const pib = document.getElementById('pwaInstallBtn');
            if(pib) {
                pib.addEventListener('click',async()=>{ if(deferredPrompt){ deferredPrompt.prompt(); deferredPrompt=null; const pb=document.getElementById('pwaBanner'); if(pb) pb.style.display='none'; } });
            }
            window.addEventListener('DOMContentLoaded',()=>{ renderHistory(); renderSavedList(); });
        </script></body></html>
        """
    def render_html_page(self, results_html="", speed_metric="", query_val=""):
        html_template = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>LARIX Repository | Guisguis NHS</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: linear-gradient(to bottom, #e8f5e9 0%, #ffffff 400px, #ffffff 100%); background-attachment: fixed; color: #1e392a; margin: 0; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; text-align: center; padding-top: 40px; position: relative; }}
        .menu-btn {{ position: fixed; top: 15px; left: 15px; font-size: 24px; background: #ffffff; border: 2px solid #2e6f40; color: #2e6f40; cursor: pointer; padding: 5px 12px; border-radius: 4px; font-weight: bold; z-index: 999; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .menu-btn:hover {{ background: #e8f5e9; }}
        .sidebar {{ position: fixed; top: 0; left: -280px; width: 250px; height: 100%; background: #ffffff; box-shadow: 2px 0 10px rgba(0,0,0,0.1); z-index: 1001; transition: 0.3s ease; padding: 20px; text-align: left; overflow-y: auto; border-right: 4px solid #2e6f40; }}
        .sidebar.active {{ left: 0; }}
        .sidebar-overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.4); z-index: 1000; }}
        .sidebar-h3 {{ color: #2e6f40; border-bottom: 2px solid #e8f5e9; padding-bottom: 5px; margin-top: 20px; font-size: 16px; font-weight: bold; }}
        .menu-link {{ display: block; background: #2e6f40; color: white; border: none; padding: 10px; border-radius: 4px; cursor: pointer; font-weight: bold; text-align: center; text-decoration: none; margin-bottom: 10px; font-size: 14px; }}
        .menu-link:hover {{ background: #1e4b2b; }}
        .main-logo {{ max-width: 140px; height: 140px; border-radius: 50%; object-fit: cover; border: 3px solid #2e6f40; }}
        input[type="text"] {{ flex: 1; padding: 12px; border: 2px solid #2e6f40; border-radius: 4px; font-size: 16px; outline: none; background-color: #ffffff; }}
        button[type="submit"] {{ background-color: #2e6f40; color: white; border: none; padding: 12px 28px; border-radius: 4px; font-size: 16px; cursor: pointer; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        button[type="submit"]:hover {{ background-color: #1e4b2b; }}
        .metrics {{ background-color: #e8f5e9; padding: 12px; border-radius: 4px; color: #1e4b2b; font-weight: bold; max-width: 600px; margin: 0 auto 20px auto; font-size: 14px; text-align: left; border-left: 4px solid #2e6f40; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }}
        .results-wrapper {{ max-width: 600px; margin: 0 auto; text-align: left; }}
        .result-card {{ border: 1px solid #c8e6c9; padding: 20px; border-radius: 4px; margin-bottom: 15px; background-color: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.03); position: relative; }}
        .result-title {{ font-size: 18px; color: #2e6f40; font-weight: bold; margin-bottom: 5px; max-width: 85%; }}
        .result-citation {{ font-style: italic; color: #555; margin-bottom: 10px; font-size: 14px; }}
        .result-snippet {{ background-color: #fafafa; border-left: 4px solid #2e6f40; padding: 12px; margin: 10px 0; font-size: 15px; line-height: 1.5; color: #111; }}
        .result-link {{ display: inline-block; font-size: 13px; color: #2e6f40; text-decoration: none; }}
        .save-btn {{ position: absolute; top: 20px; right: 20px; background: none; border: none; font-size: 22px; color: #ccc; cursor: pointer; padding: 0; outline: none; }}
        .save-btn.saved {{ color: #2e6f40; }}
        .history-item {{ display: block; padding: 6px 0; text-decoration: none; color: #333; font-size: 14px; }}
        .history-item:hover {{ color: #2e6f40; }}
    </style></head><body>
    <button class="menu-btn" onclick="toggleSidebar()">☰</button>
    <div class="sidebar-overlay" id="sidebarOverlay" onclick="toggleSidebar()"></div>
    <div class="sidebar" id="sidebar">
        <h3 class="sidebar-h3">LARIX Menu</h3>
        <a href="/" class="menu-link" style="background:#1e392a;">🏠 Home</a>
        <button onclick="openAboutModal()" class="menu-link">ℹ️ About Us</button>
        
        <h3 class="sidebar-h3">Favorites & Saved Vault</h3>
        <ul id="savedList" class="saved-list"></ul>
        
        <h3 class="sidebar-h3">Recent Search History</h3>
        <div id="historyList" class="history-list"></div>
        <hr style="border:0; border-top:1px solid #e8f5e9; margin:20px 0;">
        <button onclick="clearData()" style="width:100%; background:#d32f2f; color:white; border:none; padding:10px; border-radius:4px; cursor:pointer; font-weight:bold;">Clear Data</button>
    </div>

    <div class="container">
        <div style="margin-bottom: 15px;">
            <img src="/logo.png" class="main-logo" alt="LARIX Logo" onerror="this.src='https://placehold.co';">
        </div>
        <h1 style="color:#2e6f40; margin-bottom:5px; font-size:36px; font-weight:bold; letter-spacing:1px;">LARIX</h1>
        <div style="font-size:15px; color:#555; font-style:italic; margin-bottom:30px; line-height:1.6;">
            Development of a Web-Based Literature Indexer and Review of Related Literature Repository in<br>
            Guisguis National High School<br>
            <span style="font-size:13px; color:#2e6f40; font-weight:bold;">Published in 2026</span>
        </div>
        
        <form id="searchForm" method="GET" action="/" style="display:flex; gap:10px; max-width:600px; margin:0 auto 20px auto;">
            <input type="text" name="query" id="searchInput" placeholder="Enter keyword" value="{query_val}" required>
            <button type="submit">Search</button>
        </form>
        
        {speed_metric}
        
        <div class="results-wrapper">
            {results_html}
        </div>
    </div>
"""
        return html_template.format(query_val=query_val, speed_metric=speed_metric, results_html=results_html) + self.get_about_and_script() + self.get_application_script()

    def do_GET(self):
        if self.path == "/logo.png":
            if os.path.exists("logo.png"):
                self.send_response(200); self.send_header("Content-type", "image/png"); self.end_headers()
                with open("logo.png", "rb") as f: self.wfile.write(f.read())
                return
            else:
                self.send_response(404); self.end_headers(); return

                parsed_url = urllib.parse.urlparse(self.path); params = urllib.parse.parse_qs(parsed_url.query)
        self.send_response(200); self.send_header("Content-type", "text/html; charset=utf-8"); self.end_headers()
        u_q = params.get("query", [""]).strip().lower() if isinstance(params.get("query"), list) else params.get("query", "").strip().lower()
        if not isinstance(u_q, str): u_q = params.get("query", [""]).strip().lower() if params.get("query") else ""
        if u_q:
            start_time = time.perf_counter(); m_i = []
            if os.path.exists(DB_FILE):
                with open(DB_FILE, "r", encoding="utf-8") as f: database = json.load(f)
                for index, entry in enumerate(database):
                    entry["id"] = f"doc_{index}"
                    if u_q in entry.get("keyword", "") or u_q in entry.get("title", "").lower(): m_i.append(entry)
            retrieval_speed = time.perf_counter() - start_time
            speed_metric = f'<div class="metrics">LARIX Performance Metrics: Found {len(m_i)} result(s) in {retrieval_speed:.6f} seconds.</div>'
            results_html = ""
            if m_i:
                for item in m_i:
                    raw_title = item.get("title", "No Title"); escaped_title = raw_title.replace("'", "\\'").replace('"', '\\"')
                    apa_citation = item.get("rrl_apa", "No APA citation available."); link_url = item.get("link", "#"); author_year = item.get("author_year", "N/A")
                    abs_raw = item.get("abstract", "No abstract details recorded."); snip_raw = item.get("snippet", "No snippet available.")
                    
                    # Safe text-clipping framework execution metrics
                    if len(abs_raw) > 160: abs_layout = f'<span class="text-short">{abs_raw[:155]}...</span><span class="text-full" style="display:none;">{abs_raw}</span><button class="read-more-btn" onclick="toggleReadMore(this)">Read More...</button>'
                    else: abs_layout = f'<span>{abs_raw}</span>'
                    if len(snip_raw) > 160: snip_layout = f'<span class="text-short">"{snip_raw[:155]}..."</span><span class="text-full" style="display:none;">"{snip_raw}"</span><button class="read-more-btn" onclick="toggleReadMore(this)">Read More...</button>'
                    else: snip_layout = f'<span>"{snip_raw}"</span>'
                    
                    results_html += f"""<div class="result-card"><button class="save-btn" data-id="{item['id']}" onclick="toggleSaveResearch(this, '{item['id']}', '{escaped_title}', '{link_url}')">&#9734;</button><div class="result-title">{raw_title}</div><div class="result-citation">Citation Reference: ({author_year})</div><div style="background:#f1f8e9; padding:10px; font-size:13px; border-radius:4px; margin:8px 0; border:1px dashed #2e6f40; color:#1e392a; text-align:left; line-height:1.4;"><strong>APA 7th Edition Citation:</strong><br>{apa_citation}</div><div style="font-size:14px; color:#555; margin:8px 0; line-height:1.4; text-align:justify;"><strong>Abstract:</strong> {abs_layout}</div><div class="result-snippet"><strong>Ready-to-Use RRL Snippet:</strong><br>{snip_layout}</div><a class="result-link" href="${{link_url}}" target="_blank">View Verified Source Link</a></div>"""
            else: results_html = "<p style='text-align: center; color: #cc0000; font-weight: bold; background: #ffebee; padding: 15px; border-radius: 4px; border-left: 4px solid #cc0000; text-align: left; line-height: 1.4;'>No results found related to your keyword. Please try another term.</p>"
            response_content = self.render_html_page(results_html, speed_metric, query_val=u_q)
        else: response_content = self.render_html_page()
        self.wfile.write(response_content.encode("utf-8"))
if __name__ == "__main__":
    port_string = os.environ.get("PORT", "10000")
    server = HTTPServer(("0.0.0.0", int(port_string)), LarixServer)
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()
