/* Step-through controls for Mermaid 12 sequence diagrams. Under each diagram it
   adds one button per branch of an alt box, and Back and Next buttons that light
   one message at a time. The chosen branch colors its band, its own participants
   and the activation bars, and fades the parts of the other branches. */
(() => {
  "use strict";
  const DIM = "0.15";
  // The same outcome or transport has the same color on every page; the explorers use blue and violet too.
  const TONES = [
    [/no response/i, "yellow"],
    [/401|auth/i, "orange"],
    [/error|fail/i, "red"],
    [/success/i, "green"],
    [/grpc/i, "violet"],
    [/rest/i, "blue"],
  ];
  const toneOf = (name, i) => (TONES.find(([re]) => re.test(name)) || [null, ["cyan", "orange"][i % 2]])[1];

  function controls(svg) {
    const lines = [...svg.querySelectorAll(".messageLine0, .messageLine1")];
    const texts = [...svg.querySelectorAll(".messageText")];
    if (!lines.length || texts.length < lines.length) return;
    const y = (el) => parseFloat(el.getAttribute("y1") || el.getAttribute("y") || "0");
    // A <br/> splits a message into several texts above its line; a self-message is a path with no y.
    const lineY = (l) => (l.hasAttribute("y1") ? y(l) : l.getBBox().y);
    const owned = lines.map(() => []);
    for (const t of texts) {
      const i = lines.findIndex((l) => lineY(l) >= y(t) - 1);
      owned[i < 0 ? lines.length - 1 : i].push(t);
    }
    if (owned.some((ts) => !ts.length)) return;
    const steps = lines.map((line, i) => ({
      line,
      texts: owned[i],
      y: y(owned[i][0]),
      label: owned[i].map((t) => t.textContent.trim()).join(" "),
    }));

    const labels = [...svg.querySelectorAll(".loopText, .sectionTitle")].map((t) => ({ el: t, name: t.textContent.trim().replace(/^\[|\]$/g, ""), y: y(t) }));
    const loopLines = [...svg.querySelectorAll(".loopLine")];
    const bottom = Math.max(...loopLines.map((l) => Math.max(y(l), parseFloat(l.getAttribute("y2") || "0"))), 0);
    const top = labels.length ? labels[0].y : Infinity;
    const xs = loopLines.flatMap((l) => [parseFloat(l.getAttribute("x1") || "0"), parseFloat(l.getAttribute("x2") || "0")]);
    const rows = [...new Set(loopLines.filter((l) => l.getAttribute("y1") === l.getAttribute("y2")).map(y))].sort((a, b) => a - b);
    const branches = labels.map((label, i) => {
      const end = i + 1 < labels.length ? labels[i + 1].y : bottom;
      const tone = toneOf(label.name, i);
      label.el.style.fill = `var(--${tone}-text)`;
      let band = null;
      if (rows.length === labels.length + 1) {
        band = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        band.setAttribute("x", String(Math.min(...xs)));
        band.setAttribute("y", String(rows[i]));
        band.setAttribute("width", String(Math.max(...xs) - Math.min(...xs)));
        band.setAttribute("height", String(rows[i + 1] - rows[i]));
        band.style.fill = `var(--${tone}-pale)`;
        svg.insertBefore(band, svg.querySelector(":scope > g"));
      }
      const inRow = (el) => {
        const t = parseFloat(el.getAttribute("y") || "0");
        return rows.length === labels.length + 1 && t >= rows[i] && t <= rows[i + 1];
      };
      const gray = [...svg.querySelectorAll("rect.rect, rect.note, text.noteText")].filter(inRow);
      return { name: label.name, tone, band, gray, keep: steps.filter((s) => s.y < top || s.y > bottom || (s.y > label.y && s.y < end)) };
    });

    // A participant that only one branch talks to takes that branch's color.
    const parts = new Map();
    for (const g of svg.querySelectorAll("g")) {
      const name = g.querySelector(":scope > text.actor")?.textContent.trim();
      if (!name) continue;
      const box = g.getBBox();
      const part = parts.get(name) || { els: [], x: box.x + box.width / 2 };
      part.els.push(g);
      parts.set(name, part);
    }
    if (!parts.size) return;
    for (const l of svg.querySelectorAll("line.actor-line")) {
      const x = parseFloat(l.getAttribute("x1") || "0");
      const part = [...parts.values()].find((p) => Math.abs(p.x - x) < 2);
      if (part) part.els.push(l);
    }
    const nearest = (x) => [...parts.values()].reduce((a, b) => (Math.abs(b.x - x) < Math.abs(a.x - x) ? b : a));
    for (const s of steps) {
      const ends = s.line.hasAttribute("x1")
        ? [s.line.getAttribute("x1"), s.line.getAttribute("x2")].map(Number)
        : [s.line.getBBox().x];
      s.parts = ends.map(nearest);
    }
    const common = new Set(steps.filter((s) => branches.every((b) => b.keep.includes(s))).flatMap((s) => s.parts));
    for (const b of branches) {
      const others = new Set(branches.filter((o) => o !== b).flatMap((o) => o.keep.flatMap((s) => s.parts)));
      b.parts = [...new Set(b.keep.flatMap((s) => s.parts))].filter((p) => !common.has(p) && !others.has(p));
      for (const p of b.parts) {
        for (const el of p.els) {
          if (el.matches("line.actor-line")) { el.style.stroke = `var(--${b.tone}-border)`; continue; }
          for (const shape of el.querySelectorAll("rect, circle, line, path")) {
            shape.style.stroke = `var(--${b.tone}-border)`;
            if (!shape.matches("line")) shape.style.fill = `var(--${b.tone}-pale)`;
          }
          for (const t of el.querySelectorAll("text")) t.style.fill = `var(--${b.tone}-text)`;
        }
      }
    }

    const bar = document.createElement("div");
    bar.className = "kx seq-steps";
    const status = document.createElement("p");
    status.className = "seq-status";
    status.setAttribute("aria-live", "polite");
    const button = (text, onClick, tone) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "chip";
      if (tone) {
        b.dataset.tone = tone;
        const dot = document.createElement("span");
        dot.className = "dot";
        b.append(dot);
      }
      b.append(text);
      b.addEventListener("click", onClick);
      return b;
    };

    let current = -1;
    let shown = steps;
    let tone = null;
    const acts = [...svg.querySelectorAll('rect[class^="activation"]')].map((el) => {
      const box = el.getBBox();
      const part = nearest(box.x + box.width / 2);
      return { el, owner: branches.find((b) => b.parts.includes(part)) };
    });

    function paint() {
      for (const s of steps) {
        const inPath = shown.includes(s);
        const index = shown.indexOf(s);
        const visible = inPath && (current < 0 || index <= current);
        const lit = inPath && index === current;
        s.line.style.opacity = visible ? "1" : DIM;
        for (const t of s.texts) {
          t.style.opacity = visible ? "1" : DIM;
          t.style.fontWeight = lit ? "700" : "";
          t.style.fill = lit && tone ? `var(--${tone}-text)` : "";
        }
        s.line.style.strokeWidth = lit ? "3" : "";
        s.line.style.stroke = lit && tone ? `var(--${tone}-border)` : "";
      }
      for (const b of branches) {
        const on = shown === steps || shown === b.keep ? "1" : "0.3";
        if (b.band) b.band.style.opacity = on;
        for (const el of [...b.gray, ...b.parts.flatMap((p) => p.els)]) el.style.opacity = on;
      }
      // A bar on a shared part follows the chosen path; a bar on a branch part keeps its branch color.
      for (const a of acts) {
        const t = a.owner ? a.owner.tone : tone;
        a.el.style.fill = t ? `var(--${t}-strong)` : "var(--neu-fill)";
        a.el.style.stroke = t ? `var(--${t}-border)` : "var(--neu-border)";
        a.el.style.strokeWidth = "2";
        a.el.style.opacity = !a.owner || shown === steps || shown === a.owner.keep ? "1" : "0.3";
      }
      if (tone) bar.dataset.tone = tone;
      else delete bar.dataset.tone;
      if (current < 0) {
        status.textContent = `${shown.length} steps. Press Next to follow them one at a time.`;
      } else {
        status.textContent = `Step ${current + 1} of ${shown.length}: ${shown[current].label}`;
      }
      back.disabled = current < 0;
      next.disabled = current >= shown.length - 1;
    }

    // Each call takes one branch of the alt box, so the first branch starts selected.
    const choose = (b, keep, pathTone) => { shown = keep; tone = pathTone; current = -1; press(b); paint(); };
    const branchButtons = branches.map((branch) => {
      const b = button(branch.name, () => choose(b, branch.keep, branch.tone), branch.tone);
      return b;
    });
    const all = button("Show all", () => choose(all, steps, null));
    function press(active) {
      for (const b of [...branchButtons, all]) b.setAttribute("aria-pressed", String(b === active));
    }

    const back = button("Back", () => { current = Math.max(-1, current - 1); paint(); });
    const next = button("Next", () => {
      // Stepping through every branch would suggest that a call runs all of them.
      if (shown === steps && branchButtons.length) choose(branchButtons[0], branches[0].keep, branches[0].tone);
      current = Math.min(shown.length - 1, current + 1);
      paint();
    });
    back.classList.add("seq-nav");
    next.classList.add("seq-nav");

    const group = (label, buttons) => {
      const g = document.createElement("div");
      g.className = "seq-group";
      g.setAttribute("role", "group");
      g.setAttribute("aria-label", label);
      g.append(...buttons);
      return g;
    };
    if (branchButtons.length) bar.append(group("Choose a path", [...branchButtons, all]));
    bar.append(group("Step through", [back, next]), status);
    // Mermaid draws the diagram again when the color mode changes, so replace the old bar.
    const anchor = svg.closest(".mermaid-container") || svg.closest(".mermaid");
    if (!anchor) return;
    const old = anchor.nextElementSibling;
    if (old?.classList.contains("seq-steps")) old.replaceWith(bar);
    else anchor.after(bar);
    if (branchButtons.length) choose(branchButtons[0], branches[0].keep, branches[0].tone);
    else paint();
  }

  function scan() {
    for (const svg of document.querySelectorAll('svg[aria-roledescription="sequence"]')) {
      if (svg.dataset.steps) continue;
      svg.dataset.steps = "1";
      controls(svg);
    }
  }

  // Mermaid draws the diagrams after the page loads, so wait for each one.
  new MutationObserver(scan).observe(document.body, { childList: true, subtree: true });
  scan();
})();
