<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ProbeSuite</title>

<style>
body {
    font-family: 'Courier New', monospace;
    background-color: #0f111a;
    color: #e0e0e0;
    margin: 0;
    line-height: 1.6;
}

/* HEADER */
header {
    text-align: center;
    padding: 60px 20px;
    animation: fadeIn 1.5s ease-in-out;
}

/* LOGO */
pre.logo {
    font-size: 12px;
    color: #00ff99;
    display: inline-block;
    animation: floatLogo 3s ease-in-out infinite alternate;
}

/* TITLES */
h1 {
    margin-top: 20px;
    font-size: 2.6em;
    color: #ffcc00;
    text-shadow: 0 0 12px #ffcc00;
}

h2 {
    color: #00ccff;
}

/* SECTIONS */
section {
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
    border-left: 4px solid #ffcc00;
    animation: fadeUp 1s ease forwards;
}

/* CODE */
pre code {
    display: block;
    background: #1a1a2e;
    padding: 15px;
    color: #ffcc00;
    overflow-x: auto;
    border-radius: 6px;
}

ul {
    margin-left: 20px;
}

/* FOOTER */
footer {
    text-align: center;
    padding: 40px;
    color: #777;
}

/* ANIMATIONS */
@keyframes floatLogo {
    from { transform: translateY(0); }
    to { transform: translateY(-15px); }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-30px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(30px); }
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
|_|   |_| \_ \___/|____/ |____/|____/ \___/|___| |_|  
                               /
                \             / /
                 \' ,      / //
                  \//,   _/ //,
                   \_-//' /  //<,
                     \ ///  >  \`__/__
                     /,)-^>> _\` \
                     (/   \ //\
                         // _//\\
                       ((` ((
</pre>

<h1>ProbeSuite</h1>
<p><strong>Modular Offensive Security Toolkit</strong></p>
</header>

<section>
<h2>✨ Features</h2>
<ul>
<li>Modular and extensible architecture</li>
<li>Tools organized by penetration testing phases</li>
<li>Attack surface & reconnaissance focused</li>
<li>Real-world pentesting workflows</li>
<li>Reporting-oriented structure</li>
</ul>
</section>

<section>
<h2>📦 Requirements</h2>
<ul>
<li>Python 3.9+</li>
<li>Git</li>
<li>Linux (recommended)</li>
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
<p>ProbeSuite helps organize findings and outputs into structured penetration testing reports for technical teams and decision-makers.</p>
</section>

<section>
<h2>⚠️ Disclaimer</h2>
<p>This project is intended <strong>for educational and authorized testing only</strong>. Unauthorized use is prohibited.</p>
</section>

<section>
<h2>🤝 Contributing</h2>
<p>Fork the repository and submit a pull request to contribute.</p>
</section>

<footer>
Author: Yescrypt · Offensive Security · Pentesting · Red Teaming
</footer>

</body>
</html>
