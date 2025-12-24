#!/usr/bin/env python3
import argparse
import json
import os
import textwrap

DATA = {
    "title": "Your Product",
    "tagline": "A clear, short value proposition that explains what you do.",
    "cta": {"label": "Get Started", "href": "#signup"},
    "features": [
        {"title": "Fast setup", "body": "Go from zero to live in minutes."},
        {"title": "Simple pricing", "body": "Transparent plans with no surprises."},
        {"title": "Real results", "body": "Focused features that drive outcomes."},
    ],
    "faq": [
        {"q": "Who is this for?", "a": "Teams who want a simple, focused landing page."},
        {"q": "Do I need a backend?", "a": "No, this is a static page."},
    ],
}

INDEX_HTML = """\
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Landing Page</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <main class="page">
      <section class="hero">
        <div class="hero-copy">
          <p class="eyebrow">Launch fast</p>
          <h1 id="title"></h1>
          <p id="tagline" class="tagline"></p>
          <div class="cta-row">
            <a id="cta" class="cta" href="#"></a>
            <a class="cta secondary" href="#features-section">See features</a>
          </div>
          <p class="note">No credit card required. Ship in a day.</p>
        </div>
        <div class="hero-card">
          <p class="hero-label">Starter kit</p>
          <ul class="hero-list">
            <li>Static bundle, no backend</li>
            <li>Editable content in data.json</li>
            <li>Vercel config included</li>
          </ul>
        </div>
      </section>

      <section id="features-section" class="features">
        <h2 class="section-title">Features</h2>
        <div id="features" class="grid"></div>
      </section>

      <section class="faq">
        <h2 class="section-title">FAQ</h2>
        <div id="faq" class="stack"></div>
      </section>

      <section id="signup" class="signup">
        <h2 class="section-title">Get started</h2>
        <p>Drop in your signup form or waitlist link.</p>
        <button class="cta secondary" type="button">Join the waitlist</button>
      </section>
    </main>

    <script src="script.js" defer></script>
  </body>
</html>
"""

STYLES = """\
:root {
  --bg: #f6f2ec;
  --ink: #1d1a15;
  --accent: #0f5e4b;
  --accent-2: #d67a3c;
  --muted: #5e564d;
  --card: #fffdf9;
  --stroke: #eadfd2;
  --shadow: rgba(31, 22, 13, 0.12);
  --font-display: "Optima", "Avenir Next", "Segoe UI", sans-serif;
  --font-body: "Iowan Old Style", "Garamond", "Georgia", serif;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--font-body);
  background:
    radial-gradient(900px 500px at 12% -10%, rgba(15, 94, 75, 0.16), transparent 60%),
    radial-gradient(700px 480px at 88% 5%, rgba(214, 122, 60, 0.14), transparent 65%),
    linear-gradient(180deg, #f6f2ec 0%, #efe7dc 100%);
  color: var(--ink);
}

a { color: inherit; }

.page {
  max-width: 1040px;
  margin: 0 auto;
  padding: 72px 24px 96px;
}

.page > section {
  opacity: 0;
  transform: translateY(12px);
  animation: fadeUp 0.7s ease forwards;
}
.page > section:nth-of-type(1) { animation-delay: 0.05s; }
.page > section:nth-of-type(2) { animation-delay: 0.15s; }
.page > section:nth-of-type(3) { animation-delay: 0.25s; }
.page > section:nth-of-type(4) { animation-delay: 0.35s; }

.hero {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 3fr) minmax(0, 2fr);
  gap: 28px;
  padding: 36px;
  background: var(--card);
  border-radius: 22px;
  border: 1px solid var(--stroke);
  box-shadow: 0 18px 40px var(--shadow);
  overflow: hidden;
}

.hero::before {
  content: "";
  position: absolute;
  top: -120px;
  right: -120px;
  width: 280px;
  height: 280px;
  background: radial-gradient(circle, rgba(15, 94, 75, 0.18), transparent 70%);
  pointer-events: none;
}

.hero-copy h1 {
  font-family: var(--font-display);
  font-size: clamp(2.4rem, 4vw, 3.6rem);
  margin: 0 0 12px;
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.14em;
  font-size: 12px;
  color: var(--muted);
  margin: 0 0 16px;
}

.tagline {
  font-size: 18px;
  color: var(--muted);
  max-width: 520px;
  margin: 0 0 16px;
}

.cta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 20px;
  background: var(--accent);
  color: #fff;
  text-decoration: none;
  border-radius: 999px;
  font-weight: 600;
  font-family: var(--font-display);
  border: none;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 10px 24px rgba(15, 94, 75, 0.25);
}

.cta:hover {
  transform: translateY(-1px);
}

.cta.secondary {
  background: transparent;
  color: var(--accent);
  border: 1px solid var(--accent);
  box-shadow: none;
}

.note {
  margin: 16px 0 0;
  color: var(--muted);
  font-size: 14px;
}

.hero-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  border: 1px solid var(--stroke);
  box-shadow: 0 12px 24px rgba(31, 22, 13, 0.08);
}

.hero-label {
  font-family: var(--font-display);
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 12px;
  color: var(--muted);
  margin: 0 0 12px;
}

.hero-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 10px;
}

.hero-list li {
  position: relative;
  padding-left: 18px;
}

.hero-list li::before {
  content: "";
  position: absolute;
  left: 0;
  top: 8px;
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: var(--accent-2);
}

.section-title {
  font-family: var(--font-display);
  font-size: clamp(1.5rem, 2.6vw, 2.1rem);
  margin: 0 0 16px;
}

.features,
.faq,
.signup {
  margin-top: 56px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.card {
  background: var(--card);
  padding: 20px;
  border-radius: 14px;
  border: 1px solid var(--stroke);
  box-shadow: 0 10px 24px rgba(31, 22, 13, 0.08);
}

.card h3 {
  font-family: var(--font-display);
  margin-top: 0;
}

.stack {
  display: grid;
  gap: 12px;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(14px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .page > section {
    animation: none;
    opacity: 1;
    transform: none;
  }
  .cta { transition: none; }
}

@media (max-width: 840px) {
  .hero {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .page { padding: 48px 18px 72px; }
  .hero { padding: 28px; }
}
"""

SCRIPT = """\
async function loadData() {
  const res = await fetch("./data.json");
  if (!res.ok) return null;
  return await res.json();
}

function renderFeatures(features) {
  const container = document.getElementById("features");
  container.innerHTML = "";
  features.forEach((item) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `<h3>${item.title}</h3><p>${item.body}</p>`;
    container.appendChild(card);
  });
}

function renderFaq(items) {
  const container = document.getElementById("faq");
  container.innerHTML = "";
  items.forEach((item) => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `<strong>${item.q}</strong><p>${item.a}</p>`;
    container.appendChild(card);
  });
}

async function init() {
  const data = await loadData();
  if (!data) return;

  document.title = data.title;
  document.getElementById("title").textContent = data.title;
  document.getElementById("tagline").textContent = data.tagline;

  const cta = document.getElementById("cta");
  cta.textContent = data.cta.label;
  cta.href = data.cta.href;

  renderFeatures(data.features || []);
  renderFaq(data.faq || []);
}

init();
"""

VERCEL = """\
{
  "cleanUrls": true,
  "trailingSlash": false
}
"""


def write_file(path, content, force):
    if os.path.exists(path) and not force:
        print(f"skip: {path}")
        return
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)
        if not content.endswith("\n"):
            handle.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a static landing page bundle.")
    parser.add_argument("--out", default=".", help="Output directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    write_file(os.path.join(args.out, "data.json"), json.dumps(DATA, indent=2), args.force)
    write_file(os.path.join(args.out, "index.html"), textwrap.dedent(INDEX_HTML), args.force)
    write_file(os.path.join(args.out, "styles.css"), textwrap.dedent(STYLES), args.force)
    write_file(os.path.join(args.out, "script.js"), textwrap.dedent(SCRIPT), args.force)
    write_file(os.path.join(args.out, "vercel.json"), textwrap.dedent(VERCEL), args.force)


if __name__ == "__main__":
    main()
