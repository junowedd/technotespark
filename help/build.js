import fs from "fs";
import { marked } from "marked";
import slugify from "slugify";
import hljs from "highlight.js";

/* =========================
   1. Callout Preprocessing
========================= */
function transformCallouts(md) {
  return md
    .replace(/:::note\s+([\s\S]*?):::/g,
      (_, c) => `<div class="callout note"><strong>Note</strong><p>${c.trim()}</p></div>`
    )
    .replace(/:::tip\s+([\s\S]*?):::/g,
      (_, c) => `<div class="callout tip"><strong>Tip</strong><p>${c.trim()}</p></div>`
    )
    .replace(/:::warning\s+([\s\S]*?):::/g,
      (_, c) => `<div class="callout warning"><strong>Warning</strong><p>${c.trim()}</p></div>`
    );
}

/* =========================
   2. Markdown + TOC Renderer
========================= */
const toc = [];
const renderer = new marked.Renderer();

renderer.heading = (text, level) => {
  if (level === 2 || level === 3) {
    const id = slugify(text, { lower: true, strict: true });
    toc.push({ text, level, id });
    return `<h${level} id="${id}">${text}</h${level}>`;
  }
  return `<h${level}>${text}</h${level}>`;
};

marked.setOptions({
  renderer,
  highlight(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(code, { language: lang }).value;
    }
    return hljs.highlightAuto(code).value;
  }
});

/* =========================
   3. Build TOC HTML
========================= */
function buildTOC(items) {
  let html = `<ul class="toc-list">`;
  let openSub = false;

  items.forEach(item => {
    if (item.level === 2) {
      if (openSub) {
        html += `</ul></li>`;
        openSub = false;
      }
      html += `<li><a href="#${item.id}">${item.text}</a>`;
    }
    if (item.level === 3) {
      if (!openSub) {
        html += `<ul>`;
        openSub = true;
      }
      html += `<li><a href="#${item.id}">${item.text}</a></li>`;
    }
  });

  if (openSub) html += `</ul></li>`;
  html += `</ul>`;
  return html;
}

/* =========================
   4. Load & Process Markdown
========================= */
let md = fs.readFileSync("content/index.md", "utf-8");
md = transformCallouts(md);

const contentHtml = marked(md);
const tocHtml = buildTOC(toc);

/* =========================
   5. Theme + Code JS
========================= */
const scripts = `
<script>
const toggleBtn = document.getElementById("theme-toggle");
const root = document.documentElement;
const saved = localStorage.getItem("theme");

if (saved) {
  root.setAttribute("data-theme", saved);
  toggleBtn.textContent = saved === "dark" ? "☀️" : "🌙";
}

toggleBtn.addEventListener("click", () => {
  const current = root.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  root.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
  toggleBtn.textContent = next === "dark" ? "☀️" : "🌙";
});

document.querySelectorAll("pre > code").forEach(code => {
  const pre = code.parentElement;
  pre.classList.add("code-block");

  const rawLines = code.innerText.split("\n");
  const htmlLines = code.innerHTML.split("\n");
  code.innerHTML = "";

  htmlLines.forEach((line, i) => {
    const row = document.createElement("span");
    row.className = "line";

    const ln = document.createElement("span");
    ln.className = "ln";
    ln.textContent = i + 1;

    const content = document.createElement("span");
    content.innerHTML = line || " ";

    row.appendChild(ln);
    row.appendChild(content);
    code.appendChild(row);
  });

  const btn = document.createElement("button");
  btn.className = "copy-btn";
  btn.textContent = "Copy";

  btn.addEventListener("click", () => {
    const clean = rawLines.map(l => l.replace(/^([+-])/, "")).join("\n");
    navigator.clipboard.writeText(clean);
    btn.textContent = "Copied";
    btn.classList.add("copied");
    setTimeout(() => {
      btn.textContent = "Copy";
      btn.classList.remove("copied");
    }, 1500);
  });

  pre.appendChild(btn);
});
</script>
`;

/* =========================
   6. Inject into Template
========================= */
const template = fs.readFileSync("templates/page.html", "utf-8");

const finalHtml = template
  .replace("{{title}}", "Help Documentation")
  .replace("{{description}}", "Product help and documentation")
  .replace("{{toc}}", tocHtml)
  .replace("{{content}}", contentHtml)
  .replace("{{scripts}}", scripts);

/* =========================
   7. Write Output
========================= */
fs.writeFileSync("build/index.html", finalHtml);

console.log("✔ Help page built successfully");
