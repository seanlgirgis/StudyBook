from IPython.display import HTML, display
import random, string

_id = ''.join(random.choices(string.ascii_lowercase, k=6))

display(HTML(f"""
<div style="font-family:monospace;background:#1e1e1e;color:#d4d4d4;
            border-radius:8px;padding:14px;width:320px;user-select:none;">
  <div id="td-{_id}" style="font-size:2.4em;text-align:center;
                             letter-spacing:4px;padding:8px 0;">00:00</div>
  <div style="display:flex;gap:8px;justify-content:center;margin-top:8px;">
    <button id="btn-start-{_id}"
      style="background:#0e639c;color:#fff;border:none;border-radius:4px;
             padding:6px 16px;cursor:pointer;font-family:monospace;">Start</button>
    <button id="btn-stop-{_id}"
      style="background:#5a5a5a;color:#fff;border:none;border-radius:4px;
             padding:6px 16px;cursor:pointer;font-family:monospace;">Stop</button>
    <button id="btn-reset-{_id}"
      style="background:#5a5a5a;color:#fff;border:none;border-radius:4px;
             padding:6px 16px;cursor:pointer;font-family:monospace;">Reset</button>
    <button id="btn-copy-{_id}"
      style="background:#16825d;color:#fff;border:none;border-radius:4px;
             padding:6px 16px;cursor:pointer;font-family:monospace;">Copy</button>
  </div>
  <div id="tm-{_id}" style="text-align:center;font-size:0.78em;
                              color:#4ec9b0;height:18px;margin-top:6px;"></div>
</div>

<script>
(function() {{
  var disp  = document.getElementById('td-{_id}');
  var msg   = document.getElementById('tm-{_id}');
  var start = null, elapsed = 0, iv = null, running = false;

  function fmt(ms) {{
    var s = Math.floor(ms / 1000);
    var m = Math.floor(s / 60).toString().padStart(2, '0');
    return m + ':' + (s % 60).toString().padStart(2, '0');
  }}

  document.getElementById('btn-start-{_id}').addEventListener('click', function() {{
    if (!running) {{
      running = true;
      start = Date.now() - elapsed;
      iv = setInterval(function() {{
        elapsed = Date.now() - start;
        disp.innerText = fmt(elapsed);
      }}, 500);
    }}
  }});

  document.getElementById('btn-stop-{_id}').addEventListener('click', function() {{
    if (running) {{ running = false; clearInterval(iv); }}
  }});

  document.getElementById('btn-reset-{_id}').addEventListener('click', function() {{
    running = false; clearInterval(iv);
    elapsed = 0; disp.innerText = '00:00'; msg.innerText = '';
  }});

  document.getElementById('btn-copy-{_id}').addEventListener('click', function() {{
    var txt = '# solved in ' + disp.innerText;
    if (navigator.clipboard) {{
      navigator.clipboard.writeText(txt).then(function() {{
        msg.innerText = 'Copied — ' + txt;
        setTimeout(function() {{ msg.innerText = ''; }}, 2500);
      }});
    }} else {{
      msg.innerText = txt;
    }}
  }});
}})();
</script>
"""))
