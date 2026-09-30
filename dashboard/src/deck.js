/* ---------- presentation mode: open the page with #slides (or press P) ----------
   Horizontal deck for recording the pitch video. Each section becomes a slide whose
   charts animate in; the right arrow first runs the slide's scripted steps (the same
   interactions the pitch script performs by hand) and only then moves on.
   Keys: right/space/PageDown next, left/PageUp back, 1-9 jump, C camera area,
   H hide HUD, T light/dark, F fullscreen, P leave. Plain ASCII on purpose (build.py). */
(function(){
"use strict";
const DK = L.deck;
const isDeck = () => /^#slides\b/.test(location.hash);
addEventListener("hashchange", () => { if (isDeck() !== document.body.classList.contains("deck")) location.reload(); });

// link into the presentation mode from the normal page header
const eb = document.querySelector("header.top .eyebrow");
if (eb) { const s = document.createElement("span"); s.className = "dk-link"; s.innerHTML = `<a href="#slides">${DK.link}</a>`; eb.appendChild(s); }
if (!isDeck()) {
  addEventListener("keydown", e => { if ((e.key === "p" || e.key === "P") && !e.metaKey && !e.ctrlKey && !e.altKey) location.hash = "slides"; });
  return;
}

/* slide order follows video/pitch_script.md (forecast comes right after the rule) */
const ORDER = ["top", "quem", "empates", "regra", "previsao", "juizes", "custo", "fila", "fim"];
const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
const store = { get(k){ try { return localStorage.getItem(k); } catch(e){ return null; } }, set(k,v){ try { localStorage.setItem(k,v); } catch(e){} } };

/* ---- tween engine: one rAF loop; finishAll() snaps every running tween to its end ---- */
const ease = t => 1 - Math.pow(1 - t, 3);
const easeIO = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;
let tweens = [], looping = false, gen = 0;
function loop(now){
  tweens = tweens.filter(tw => {
    if (tw.done) return false;
    const t = Math.min(1, Math.max(0, (now - tw.t0) / tw.dur));
    tw.fn(tw.ez(t));
    if (t >= 1) { tw.done = true; tw.res(); return false; }
    return true;
  });
  if (tweens.length) requestAnimationFrame(loop); else looping = false;
}
function tween(dur, delay, fn, ez = ease){
  return new Promise(res => {
    fn(0);
    if (reduce) { fn(1); res(); return; }
    tweens.push({ fn, ez, res, dur, t0: performance.now() + delay, done: false });
    if (!looping) { looping = true; requestAnimationFrame(loop); }
  });
}
function finishAll(){ const ts = tweens; tweens = []; ts.forEach(tw => { if (!tw.done) { tw.done = true; tw.fn(1); tw.res(); } }); }
const wait = ms => tween(ms, 0, () => {});

/* ---- chart animations (work on whatever the dashboard code drew) ---- */
const svgRects = svg => [...svg.querySelectorAll("rect")].filter(r => { const f = r.getAttribute("fill"); return f && f !== "transparent" && !r.closest("clipPath"); });
function bars(id, axis, o = {}){
  const svg = $(id); if (!svg) return;
  const rs = svgRects(svg), n = rs.length, span = o.span ?? 450, d0 = o.delay ?? 0;
  rs.forEach((r, i) => {
    const d = d0 + (n > 1 ? i * span / (n - 1) : 0);
    if (axis === "y") {
      const y = +r.getAttribute("y"), h = +r.getAttribute("height"), b = y + h;
      tween(o.dur ?? 650, d, t => { r.setAttribute("y", b - h*t); r.setAttribute("height", h*t); });
    } else {
      const x = +r.getAttribute("x"), w = +r.getAttribute("width"), right = o.fromRight && o.fromRight(r);
      tween(o.dur ?? 700, d, t => { r.setAttribute("width", w*t); if (right) r.setAttribute("x", x + w*(1 - t)); });
    }
  });
  fadeText(svg, d0 + span * .6);
}
function fadeText(svg, delay){ svg.querySelectorAll("text").forEach(t => tween(450, delay, v => { t.style.opacity = v; })); }
function fadeIn(nodes, delay, dur = 400){ nodes.forEach(n => tween(dur, delay, v => { n.style.opacity = v; })); }
function wipe(id, dur = 1500, delay = 250){
  const svg = $(id); if (!svg) return;
  let cp = svg.querySelector("clipPath.dk-wipe");
  if (!cp) {
    const cid = "dkw-" + id;
    cp = el("clipPath", { id: cid, class: "dk-wipe", clipPathUnits: "userSpaceOnUse" }, el("defs", {}, svg));
    el("rect", { x: -40, y: -40, width: 0, height: 4000 }, cp);
    svg.querySelectorAll("path").forEach(p => p.setAttribute("clip-path", `url(#${cid})`));
  }
  const r = cp.firstChild, W = svg.viewBox.baseVal.width + 80;
  tween(dur, delay, t => r.setAttribute("width", W*t), easeIO);
  fadeIn([...svg.querySelectorAll("circle")], delay + dur * .8);
}
function dots(id, delay = 100){
  const svg = $(id); if (!svg) return;
  const cs = [...svg.querySelectorAll("g circle")];
  cs.forEach((c, i) => { const r = +c.getAttribute("r"); c.dataset.r = c.dataset.r || r;
    tween(380, delay + ((i * 7919) % cs.length) / cs.length * 900, t => c.setAttribute("r", Math.max(0, c.dataset.r * t)), t => { const s = 1.7; t -= 1; return t*t*((s+1)*t + s) + 1; }); });
}
function flipRank(fn){                      // FLIP: rows slide to their new position
  const box = $("rank"), key = r => r.querySelector("b").textContent;
  const before = {}; [...box.children].forEach(r => before[key(r)] = r.getBoundingClientRect().top);
  fn();
  const z = zoomOf(box);
  [...box.children].forEach(r => { const dy = (before[key(r)] - r.getBoundingClientRect().top) / z; if (!dy) return;
    r.style.transition = "none"; tween(750, 80, t => { r.style.transform = `translateY(${dy*(1 - t)}px)`; }, easeIO); });
}
function rankIn(delay){ [...$("rank").children].forEach((r, i) => { r.style.transition = "none"; tween(500, delay + i*120, t => { r.style.opacity = t; r.style.transform = `translateX(${(1 - t)*-24}px)`; }); }); }
function countUp(root, delay){
  const dec = L.dec, th = dec === "," ? "." : ",";
  root.querySelectorAll(".readout b, .kpi b").forEach(b => {
    const s = b.textContent, m = s.match(/\d[\d.,]*/); if (!m) return;
    const raw = m[0].replace(/[.,]$/, ""), decimals = raw.includes(dec) ? raw.split(dec)[1].length : 0;
    const v = parseFloat(raw.split(th).join("").replace(dec, "."));
    if (!isFinite(v) || v === 0) return;
    const group = raw.includes(th), pre = s.slice(0, m.index), post = s.slice(m.index + raw.length);
    const f = x => { let [i, fr] = x.toFixed(decimals).split("."); if (group) i = i.replace(/\B(?=(\d{3})+(?!\d))/g, th); return i + (fr ? dec + fr : ""); };
    tween(1100, delay, t => { b.textContent = t >= 1 ? s : pre + f(v*t) + post; });
  });
}
/* drive a range input the way a hand on the slider would (fires the dashboard's own "input" handler) */
function sweepRange(id, to, msPerStep = 170){
  const inp = $(id), from = +inp.value; if (from === to) return Promise.resolve();
  let last = from;
  return tween(Math.abs(to - from) * msPerStep, 0, t => { const v = Math.round(from + (to - from)*t);
    if (v !== last) { last = v; inp.value = v; inp.dispatchEvent(new Event("input")); } }, easeIO);
}
function setRange(id, v){ const inp = $(id); inp.value = v; inp.dispatchEvent(new Event("input")); }
let ladK = 1;
function sweepLad(to, msPerStep = 230){
  const from = ladK; ladK = to; if (!HOOK.lad || from === to) return Promise.resolve();
  let last = from;
  return tween(Math.abs(to - from) * msPerStep, 0, t => { const v = Math.round(from + (to - from)*t); if (v !== last) { last = v; HOOK.lad(v); } }, easeIO);
}
const click = id => $(id).click();
const clickEx = i => { const b = $("ex-" + i); if (b) b.click(); };
const exAnim = d => { bars("ex-strip", "y", { span: 700, delay: d, dur: 500 }); bars("ex-bars", "x", { span: 350, delay: d + 250 }); };

/* ---- per-slide script: reset() state, anim() on entry, steps[] on the right arrow ---- */
const CFG = {
  quem:     { reset(){ clickEx(0); }, anim(){ exAnim(350); },
              steps: [1, 2, 3].filter(i => D.exemplos[i]).map(i => () => { clickEx(i); exAnim(0); countUp($("ex-read"), 0); }) },
  empates:  { reset(){ setRange("k-emp", 1); }, anim(){ bars("emp-chart", "y", { delay: 350, span: 200 }); },
              steps: [() => sweepRange("k-emp", 12, 210)] },
  regra:    { reset(){ click("r-soma"); },
              anim(){ rankIn(450); bars("dec-chart", "x", { delay: 900, span: 500, fromRight: r => r.getAttribute("fill") === "var(--halluc)" }); },
              steps: [() => flipRank(() => click("r-lex"))] },
  previsao: { reset(){ click("p-alpha"); }, anim(){ dots("p-chart", 400); },
              steps: [() => { click("p-glob"); dots("p-chart", 0); }, () => { click("p-alpha"); dots("p-chart", 0); }] },
  juizes:   { reset(){ ladK = 1; if (HOOK.lad) HOOK.lad(1); }, anim(){ wipe("lad-chart", 1600, 400); },
              steps: [() => sweepLad(5), () => sweepLad(8), () => sweepLad(12)] },
  custo:    { reset(){ setRange("kc", 12); }, anim(){ bars("tok-chart", "x", { delay: 400, span: 350 }); bars("cpu-chart", "x", { delay: 900, span: 500 }); },
              steps: [() => sweepRange("kc", 8, 260), () => sweepRange("kc", 1, 200)] },
  fila:     { reset(){ setRange("bud", 4); }, anim(){ wipe("q-chart", 1500, 400); },
              steps: [() => sweepRange("bud", 7, 500)] }
};

/* ---- build the deck ---- */
const wrap = document.querySelector(".wrap");
const nodeOf = id => id === "top" ? wrap.querySelector("header.top") : id === "fim" ? wrap.querySelector("footer") : $(id);
const slides = [];
let secN = 0;
ORDER.forEach(id => {
  const node = nodeOf(id); if (!node) return;
  const sl = document.createElement("div"); sl.className = "deck-slide"; sl.dataset.id = id;
  const inner = document.createElement("div"); inner.className = "deck-in";
  inner.appendChild(node); sl.appendChild(inner); wrap.appendChild(sl); slides.push(sl);
  if (node.matches("section")) {
    const num = node.querySelector(".num"); secN++; if (num) num.textContent = num.textContent.replace(/^\s*\d+/, String(secN));
    [...node.querySelector(".txt").children].forEach((c, i) => { c.classList.add("dk-rev"); c.style.setProperty("--d", i); });
    const viz = node.querySelector(".viz"); viz.classList.add("dk-rev"); viz.style.setProperty("--d", 1);
  } else {
    if (id === "fim") { const h = document.createElement("div"); h.className = "dk-end"; h.textContent = DK.endTitle; node.prepend(h); }
    [...node.querySelectorAll(":scope > *, .kpis > .kpi")].filter(c => !c.classList.contains("kpis")).forEach((c, i) => { c.classList.add("dk-rev"); c.style.setProperty("--d", i); });
  }
});
document.body.classList.add("deck");
const lang = document.querySelector(".langsw a"); if (lang) lang.href = lang.getAttribute("href") + "#slides";
const dl = document.querySelector(".dk-link a"); if (dl) { dl.textContent = DK.exit; dl.href = "#"; }

const hud = document.createElement("div"); hud.className = "dk-hud"; hud.innerHTML = `<span class="dk-dots"></span><span class="dk-count"></span>`;
const prog = document.createElement("div"); prog.className = "dk-prog";
const hint = document.createElement("div"); hint.className = "dk-hint"; hint.textContent = DK.hint;
const cam = document.createElement("div"); cam.className = "dk-cam"; cam.textContent = DK.cam;
document.body.append(hud, prog, hint, cam);

/* camera area: 0 off, 1 frame shown and space reserved, 2 space reserved only */
let camMode = +(store.get("dk-cam") || 0);
function applyCam(){ document.body.classList.toggle("dk-cam1", camMode === 1); fit(); }

/* ---- fit each slide to the viewport (zoom the 1600px canvas) ---- */
const zoomOf = n => +(n.closest(".deck-in")?.style.zoom || 1);
function fit(){
  const W = innerWidth, H = innerHeight, mt = .07*H, mb = .07*H;
  const camH = camMode ? .03*H + .22*W*9/16 + .03*H : 0;
  slides.forEach(sl => { sl.firstChild.style.zoom = 1; });
  slides.forEach(sl => {
    const inner = sl.firstChild, ch = inner.offsetHeight;
    const guard = inner.querySelector(":scope > section .txt") || inner;
    const gb = guard.getBoundingClientRect().bottom - inner.getBoundingClientRect().top;
    let z = Math.min(W * .9 / 1600, (H - mt - mb) / ch);
    if (camMode) z = Math.min(z, (H - camH - mt) / gb);
    let top = Math.max(mt, (H - ch*z) / 2);
    if (camMode) top = Math.max(mt, Math.min(top, H - camH - gb*z));
    inner.style.zoom = z; sl.style.paddingTop = top + "px";
  });
}

/* ---- navigation ---- */
let cur = -1, step = 0;
function hudUpd(){
  const c = CFG[slides[cur].dataset.id], n = c && c.steps ? c.steps.length : 0;
  hud.querySelector(".dk-count").textContent = `${cur + 1} / ${slides.length}`;
  hud.querySelector(".dk-dots").innerHTML = Array.from({ length: n }, (_, i) => `<i class="${i < step ? "on" : ""}"></i>`).join("");
  prog.style.width = (100 * cur / (slides.length - 1)) + "%";
}
function go(i, instant){
  i = Math.max(0, Math.min(slides.length - 1, i));
  finishAll(); gen++;
  const sl = slides[i], id = sl.dataset.id, c = CFG[id];
  document.body.classList.toggle("dk-jump", !!instant || reduce);
  wrap.style.transform = `translateX(${-i * innerWidth}px)`;
  slides.forEach(s => s.classList.remove("in"));
  cur = i; step = 0;
  if (c && c.reset) c.reset();
  void sl.offsetWidth; sl.classList.add("in");
  countUp(sl, 500);
  if (c && c.anim) c.anim();
  history.replaceState(null, "", "#slides/" + (i + 1));
  hudUpd();
}
function next(){
  const c = CFG[slides[cur].dataset.id];
  if (c && c.steps && step < c.steps.length) { finishAll(); c.steps[step++](); hudUpd(); }
  else if (cur < slides.length - 1) go(cur + 1);
}
addEventListener("keydown", e => {
  if (e.metaKey || e.ctrlKey || e.altKey) return;
  const k = e.key, onRange = document.activeElement && document.activeElement.type === "range";
  if ((k === "ArrowRight" || k === "ArrowLeft") && onRange) return;
  if (k === "ArrowRight" || k === "PageDown" || k === " " || k === "Enter" && !(document.activeElement && document.activeElement.tagName === "BUTTON")) { e.preventDefault(); next(); }
  else if (k === "ArrowLeft" || k === "PageUp" || k === "Backspace") { e.preventDefault(); go(cur - 1); }
  else if (k === "Home") go(0);
  else if (k === "End") go(slides.length - 1);
  else if (/^[1-9]$/.test(k)) go(+k - 1);
  else if (k === "c" || k === "C") { camMode = (camMode + 1) % 3; store.set("dk-cam", camMode); applyCam(); }
  else if (k === "h" || k === "H") document.body.classList.toggle("dk-nohud");
  else if (k === "t" || k === "T") { const r = document.documentElement, dark = r.dataset.theme ? r.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; r.dataset.theme = dark ? "light" : "dark"; }
  else if (k === "f" || k === "F") { if (document.fullscreenElement) document.exitFullscreen(); else document.documentElement.requestFullscreen().catch(() => {}); }
  else if (k === "p" || k === "P") location.hash = "";
});
// a clicked button or slider must not swallow the next space / arrow press
document.addEventListener("pointerup", e => { const t = e.target.closest("button,input"); if (t) setTimeout(() => t.blur(), 0); });
addEventListener("resize", () => { fit(); go(cur, true); });

applyCam();
const start = parseInt((location.hash.split("/")[1] || "1"), 10) - 1;
go(isFinite(start) ? start : 0, true);
if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
hint.classList.add("show"); setTimeout(() => hint.classList.remove("show"), 4500);
})();
