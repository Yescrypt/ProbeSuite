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
        padding: 0;
        line-height: 1.5;
    }
    header {
        text-align: center;
        padding: 50px 20px;
        animation: fadeIn 2s ease-in-out;
    }
    pre.logo {
        font-size: 12px;
        white-space: pre;
        color: #00ff99;
        display: inline-block;
        animation: floatLogo 3s ease-in-out infinite alternate;
    }
    h1 {
        margin: 20px 0 10px 0;
        font-size: 2.5em;
        color: #ffcc00;
        text-shadow: 0 0 10px #ffcc00;
    }
    section {
        max-width: 900px;
        margin: 40px auto;
        padding: 20px;
        border-left: 4px solid #ffcc00;
        animation: fadeUp 1s ease-in-out;
    }
    h2 {
        color: #00ccff;
        margin-top: 20px;
    }
    ul {
        margin: 10px 0 10px 20px;
    }
    code {
        background-color: #1a1a2e;
        padding: 3px 6px;
        border-radius: 4px;
        color: #ffcc00;
    }
    pre code {
        display: block;
        padding: 15px;
        overflow-x: auto;
    }
    @keyframes floatLogo {
        0% { transform: translateY(0px); }
        100% { transform: translateY(-15px); }
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
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
                                             \\' ,      / //
                                              \//,   _/ //,
                                               \_-//' /  //<,
                                                 \ ///  >  \\`__/__
                                                 /,)-^>> _\` \
                                                 (/   \ //\
                                                     // _//\\
                                                   ((` ((
    </pre>
    <h1>ProbeSuite</h1>
    <p><strong>Modular Offensive Security Toolkit</strong></p>
</header>

<section>
    <h2>Features ✨</h2>
    <ul>
        <li>Modular and extensible architecture</li>
        <li>Tools organized by penetration testing phases</li>
        <li>Focus on reconnaissance and attack surface analysis</li>
        <li>Designed for real-world penetration testing workflows</li>
        <li>Reporting-oriented project structure</li>
    </ul>
</section>

<section>
    <h2>Requirements 📦</h2>
    <ul>
        <li>Python 3.9+</li>
        <li>Git</li>
        <li>Linux-based operating system (recommended)</li>
    </ul>
</section>

<section>
    <h2>Installation 🚀</h2>
    <pre><code>git clone https://github.com/Yescrypt/ProbeSuite.git
cd ProbeSuite
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
</code></pre>
</section>

<section>
    <h2>Usage ▶️</h2>
    <pre><code>python app/main.py</code></pre>
</section>

<section>
    <h2>Reporting 📊</h2>
    <p>ProbeSuite is built with reporting in mind. Collected findings and outputs can be organized to generate structured penetration testing reports suitable for technical teams and decision-makers.</p>
</section>

<section>
    <h2>Disclaimer ⚠️</h2>
    <p>This project is intended <strong>for educational purposes and authorized security testing only</strong>. Do not use ProbeSuite against systems without explicit permission. The author assumes no responsibility for misuse or illegal activities.</p>
</section>

<section>
    <h2>Contributing 🤝</h2>
    <p>Contributions, improvements, and suggestions are welcome. Feel free to fork the repository and submit a pull request.</p>
</section>

<footer style="text-align:center; margin:50px 0; color:#777;">
    <p>Author: Yescrypt | Focus: Offensive Security · Penetration Testing · Red Teaming</p>
</footer>

</body>
</html>
