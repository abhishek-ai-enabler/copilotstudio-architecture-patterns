import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import puppeteer from "puppeteer-core";

const root = fileURLToPath(new URL("../../", import.meta.url));
const read = f => readFileSync(path.join(root, f));
const text = f => read(f).toString("utf8");
const sha = bytes => createHash("sha256").update(bytes).digest("hex");
const check = process.argv.includes("--check");
const groups = ["reference-architectures", "solution-ideas", "decision-patterns", "technical-patterns"];
const products = JSON.parse(text("assets/platforms/products.json"));
const mapping = new Map();
for (const line of text("tools/diagrams/platforms.txt").split("\n").filter(l => l && !l.startsWith("#"))) {
  const [slug, ...entries] = line.split(/\s+/);
  assert(!mapping.has(slug), `Duplicate diagram ${slug}`);
  const roles = Object.fromEntries(entries.map(e => e.split(":")));
  assert.equal(Object.keys(roles).length, entries.length);
  mapping.set(slug, roles);
}
const icons = {};
for (const [id, product] of Object.entries(products)) {
  if (!product.sha256) continue;
  const bytes = read(`assets/platforms/${id}.svg`);
  assert.equal(sha(bytes), product.sha256, `Changed official artwork: ${id}`);
  icons[id] = `data:image/svg+xml;base64,${bytes.toString("base64")}`;
}
const dir = "assets/flows";
mkdirSync(path.join(root, dir), {recursive: true});
const manifestFile = `${dir}/manifest.json`;
const prior = check ? JSON.parse(text(manifestFile)) : {};
const manifest = {};
const browser = await puppeteer.launch({...(process.env.CHROME_PATH
  ? {executablePath:process.env.CHROME_PATH} : {channel:"chrome"}), headless: true});
let rendered = 0;
try {
  const page = await browser.newPage();
  await page.setViewport({width: 1600, height: 1000, deviceScaleFactor: 1.5});
  await page.setOfflineMode(true);
  await page.addScriptTag({path: path.join(root, "tools/diagrams/node_modules/mermaid/dist/mermaid.min.js")});
  await page.evaluate(() => {
    mermaid.initialize({startOnLoad: false, securityLevel: "strict", theme: "neutral",
      sequence: {mirrorActors: false, useMaxWidth: false, actorMargin: 42, width: 168}});
    document.body.style.cssText = "background:white;margin:0;";
  });
  const files = groups.flatMap(g => readdirSync(path.join(root,g)).filter(f => f.endsWith(".md")).sort().map(f => `${g}/${f}`));
  const build = sha(Buffer.concat([read("tools/diagrams/render.mjs"), read("tools/diagrams/package-lock.json")]));
  for (const file of [...files, "COMPONENTS.md", "COPILOT-CREDITS.md"]) {
    const markdown = text(file);
    const slug = path.basename(file, ".md");
    const pattern = files.includes(file);
    const blocks = [...markdown.matchAll(/^```mermaid\n([\s\S]*?)^```/gm)].map(m => m[1]);
    if (pattern) {
      assert.equal(blocks.length, 2, file);
      assert.match(blocks[0], /^flowchart /);
      assert.match(blocks[1], /^sequenceDiagram\n/);
      assert(markdown.includes(`](../${dir}/${slug}.png)`), `Missing flow image in ${file}`);
    }
    for (const source of blocks) {
      const flow = pattern && source.startsWith("sequenceDiagram");
      const roles = flow ? mapping.get(slug) : {};
      if (flow) {
        assert(roles, `Missing map for ${file}`);
        const participants = [...source.matchAll(/^\s*(?:participant|actor)\s+(\w+) as /gm)].map(m => m[1]);
        assert.deepEqual(Object.keys(roles).sort(), participants.sort(), `Lifeline map mismatch: ${file}`);
      }
      const labels = {};
      for (const [actor,id] of Object.entries(roles)) {
        if (id === "-") continue;
        assert(Object.hasOwn(products,id), `Unknown product ${id} in ${file}`);
        labels[actor] = {name:products[id].name, image:icons[id] || null};
      }
      if (flow) assert(Object.values(labels).some(p => p.image), `No eligible icon in ${file}`);
      try {
        await page.evaluate(async (source, labels) => {
          const box = document.createElement("main");
          document.body.replaceChildren(box);
          const {svg} = await mermaid.render("diagram", source, box);
          box.innerHTML = svg;
          const el = box.querySelector("svg");
          if (!el || el.querySelector(".error-icon") || el.getBBox().width <= 0) throw Error("Empty diagram");
          if (!Object.keys(labels).length) return;
          const vb = el.viewBox.baseVal;
          const top = vb.y, pad = 65;
          el.setAttribute("viewBox", `${vb.x} ${top-pad} ${vb.width} ${vb.height+pad}`);
          el.setAttribute("width", vb.width);
          el.setAttribute("height", vb.height);
          el.style.cssText = "display:block;background:white;max-width:none";
          for (const [id,{name,image}] of Object.entries(labels)) {
            const anchor = el.querySelector(`.actor-top[name="${id}"]`);
            if (!anchor) throw Error(`Missing actor ${id}`);
            const bounds = anchor.getBBox();
            const x = bounds.x + bounds.width/2;
            if (image) {
              const verify = new Image();
              verify.src = image;
              await verify.decode();
              const logo = document.createElementNS(el.namespaceURI,"image");
              Object.entries({x:x-18,y:top-pad+3,width:36,height:36,href:image}).forEach(([k,v])=>logo.setAttribute(k,v));
              el.append(logo);
            }
            const label = document.createElementNS(el.namespaceURI,"text");
            label.setAttribute("x",x); label.setAttribute("y",top-7);
            label.setAttribute("text-anchor","middle");
            label.style.cssText = "font: bold 13px Arial,sans-serif;fill:#253247";
            label.textContent = name;
            el.append(label);
            const l = label.getBBox();
            if (l.x < vb.x || l.x+l.width > vb.x+vb.width) throw Error(`Clipped product: ${name}`);
          }
        }, source, labels);
      } catch (e) { throw new Error(`${file}: ${e.message}`, {cause:e}); }
      rendered++;
      if (!flow) continue;
      const input = sha(JSON.stringify([build,source,roles,labels]));
      const imagePath = `${dir}/${slug}.png`;
      if (!check) await page.$("main > svg").then(el => el.screenshot({path:path.join(root,imagePath)}));
      const bytes = read(imagePath);
      assert.equal(bytes.subarray(1,4).toString(), "PNG", imagePath);
      manifest[slug] = {input, png:sha(bytes)};
    }
  }
  assert.deepEqual([...mapping.keys()].sort(), Object.keys(manifest).sort(), "Orphan or missing map");
  assert.deepEqual(readdirSync(path.join(root, dir)).filter(f=>f.endsWith(".png")).sort(),
    Object.keys(manifest).map(s=>s+".png").sort(), "Orphan or missing PNG");
  if (check) assert.deepEqual(manifest,prior,"Stale flow assets: run npm run render and review the images");
  else writeFileSync(path.join(root,manifestFile),JSON.stringify(manifest,null,2)+"\n");
  console.log(`${rendered} Mermaid diagrams rendered; ${Object.keys(manifest).length} platform flows ${check?"verified":"written"}.`);
} finally { await browser.close(); }
