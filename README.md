<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>ProbeSuite</title>

  <style>
    body {
      margin: 0;
      font-family: "Courier New", monospace;
      background: radial-gradient(circle at top, #151a2e, #0b0f1a);
      color: #e6e6e6;
      line-height: 1.6;
    }

    header {
      text-align: center;
      padding: 60px 20px;
      animation: fadeIn 1.8s ease;
    }

    .logo {
      color: #00ff9c;
      font-size: 12px;
      white-space: pre;
      display: inline-block;
      animation: float 3s ease-in-out infinite alternate;
    }

    h1 {
      font-size: 3rem;
      margin: 25px 0 10px;
      color: #f39c12;
      text-shadow: 0 0 15px rgba(243,156,18,0.6);
    }

    h2 {
      color: #00ccff;
      margin-top: 40px;
    }

    .subtitle {
      color: #bbb;
      font-size: 1.2rem;
      margin-bottom: 20px;
    }

    section {
      max-width: 900px;
      margin: auto;
      padding: 40px 25px;
      animation: fadeUp 1.2s ease;
    }

    ul {
      margin-left: 20px;
    }

    code {
      background: #1a1f36;
      padding: 4px 7px;
      border-radius: 4px;
      color: #f1c40f;
    }

    pre {
      background: #11162a;
      padding: 18px;
      border-radius: 8px;
      overflow-x: auto;
      box-shadow: 0 0 20px rgba(0,0,0,0.4);
    }

    .gif {
      display: block;
      margin: 40px auto;
      max-width: 100%;
    }

    footer {
      text-align: center;
      padding: 40px 20px;
      font-size: 0.9rem;
      color: #aaa;
    }

    @keyframes float {
      from { transform: translateY(0); }
      to { transform: translateY(-15px); }
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(-25px); }
      to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeUp {
      from { opacity: 0; transform: translateY(25px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>

<body>

<header>
<pre class="logo">
 ____  ____   ___  ____   _____ _____       ___ __ __   
|  _ \|  _ \ / _ \| __ ) | ____/ ___|| | | |_ _|_   _|  
| |_) | |_) | | | |  _ \ |  _| \___ \| | | || |  | |  
|  __/|  _ <| |_| | |_) ||____  __) || |_| || |  | |  
|_|   |_| \_\___/|____/ |____/|____/ \___/|___| |_|  
                                                         
                         /
              \         / /
               \\',    / //
                \\//,_/ //,
                 \_-//' /  //<,
                   \ ///  >  \\`__/__
                   /,)-^>> _\`
                   (/   \ //\
                       // _//\\
                     ((` ((  
</pre>

<h1>ProbeSuite</h1>
<p class="subtitle">Modular Offensive Security Toolkit</p>

<img class="gif" src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" alt="animation">
</header>

<section>
<h2>🧠 About</h2>
<p>
<strong>ProbeSuite</strong> is a modular offensive security toolkit designed to support the
entire penetration testing lifecycle. It brings together essential tools for
professional pentesters, red teamers, and cybersecurity researchers.
</p>
</section>

<section>
<h2>🔍 Pentesting Phases</h2>
<ul>
  <li>Information Gathering</li>
  <li>OSINT</li>
  <li>Scanning & Enumeration</li>
  <li>Vulnerability Assessment</li>
  <li>Exploitation</li>
  <li>Post-Exploitation</li>
  <li>Reporting</li>
</ul>
</section>

<section>
<h2>✨ Features</h2>
<ul>
  <li>Modular and extensible architecture</li>
  <li>Tools grouped by pentesting phases</li>
  <li>Real-world offensive security workflow</li>
  <li>Reporting-oriented structure</li>
</ul>
</section>

<section>
<h2>📦 Requirements</h2>
<ul>
  <li>Python 3.9+</li>
  <li>Git</li>
  <li>Linux-based OS (recommended)</li>
</ul>
</section>

<section>
<h2>🚀 Installation</h2>
<pre><code>git clone https://github.com/Yescrypt/ProbeSuite.git
cd ProbeSuite
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt</code></pre>
</section>

<section>
<h2>▶️ Usage</h2>
<pre><code>python app/main.py</code></pre>
</section>

<section>
<h2>📊 Reporting</h2>
<p>
ProbeSuite helps organize findings and outputs to generate structured
penetration testing reports suitable for technical teams and decision-makers.
</p>
</section>

<section>
<h2>⚠️ Disclaimer</h2>
<p>
This project is intended for educational purposes and authorized security
testing only. Do not use it against systems without explicit permission.
</p>
</section>

<footer>
<p><strong>Author:</strong> Yescrypt</p>
<p>Offensive Security · Penetration Testing · Red Teaming</p>
</footer>

</body>
</html>
