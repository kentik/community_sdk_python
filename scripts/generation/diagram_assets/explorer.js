/* Explorer for house-style diagrams. It wires each svg inside an .explorer
   box to its entry in the JSON blocks #diagram-data, keyed by the svg id. */
(() => {
  "use strict";
  // A page with several explorers has one data block per explorer.
  const DATA = Object.assign(
    {},
    ...[...document.querySelectorAll('script[id="diagram-data"]')].map((s) => JSON.parse(s.textContent || "{}")),
  );

  function el(tag, attrs = {}, children = []) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "text") e.textContent = v;
      else e.setAttribute(k, v);
    }
    for (const c of children) if (c) e.append(c);
    return e;
  }

  // Selection follows data edges only. A request edge lights up when it
  // touches the selected part, but stays out of the closure: otherwise the
  // call half of a two-way exchange makes every caller "need" the others.
  // Requests are access paths that a person opens, and calls.
  function explorer(svg, onSelect) {
    const nodes = [...svg.querySelectorAll(".node[data-id]")];
    const segs = [...svg.querySelectorAll(".edge[data-links]")];
    const hiMarker = svg.querySelector('marker[id$="-ah-hi"]');
    const links = {};
    for (const s of segs) {
      const label = s.querySelector(".elabel")?.textContent || "";
      const request = s.classList.contains("access") || s.classList.contains("call");
      for (const k of s.dataset.links.split(",")) {
        const [from, to] = k.split(">");
        links[k] ??= { from, to, request, label: "" };
        if (!links[k].label) links[k].label = label;
      }
      const path = s.querySelector("path[marker-end]");
      if (path) path.dataset.marker = path.getAttribute("marker-end");
    }

    function closure(start, dir) {
      const seen = {};
      const stack = [start];
      while (stack.length) {
        const n = stack.pop();
        for (const l of Object.values(links)) {
          if (l.request) continue;
          const [a, b] = dir === "up" ? [l.to, l.from] : [l.from, l.to];
          if (a === n && !seen[b] && b !== start) { seen[b] = true; stack.push(b); }
        }
      }
      return seen;
    }

    // A marker cannot inherit the stroke of its path, so a lit wire swaps
    // to the second marker that the kit puts in every svg.
    function paintMarkers() {
      for (const s of segs) {
        const p = s.querySelector("path[data-marker]");
        if (!p || !hiMarker) continue;
        const lit = s.classList.contains("hi") || s.classList.contains("flow");
        p.setAttribute("marker-end", lit ? `url(#${hiMarker.id})` : p.dataset.marker);
      }
    }

    function clear() {
      svg.classList.remove("dimming");
      for (const n of nodes) n.classList.remove("sel", "lit");
      for (const s of segs) s.classList.remove("hi", "flow");
      paintMarkers();
    }

    function select(id) {
      const up = closure(id, "up");
      const down = closure(id, "down");
      const lit = { [id]: true, ...up, ...down };
      svg.classList.add("dimming");
      for (const s of segs) {
        let hi = false;
        let flow = false;
        for (const k of s.dataset.links.split(",")) {
          const l = links[k];
          if (l.request) {
            if (l.from === id || l.to === id) { flow = true; lit[l.from] = true; lit[l.to] = true; }
            continue;
          }
          if (up[l.from] && (up[l.to] || l.to === id)) hi = true;
          if ((down[l.from] || l.from === id) && down[l.to]) flow = true;
        }
        s.classList.toggle("hi", hi);
        s.classList.toggle("flow", flow && !hi);
      }
      for (const n of nodes) {
        n.classList.toggle("sel", n.dataset.id === id);
        n.classList.toggle("lit", !!lit[n.dataset.id]);
      }
      paintMarkers();
      onSelect(id);
    }

    function showPath(keys) {
      clear();
      svg.classList.add("dimming");
      const set = new Set(keys);
      const lit = {};
      for (const s of segs) {
        const on = s.dataset.links.split(",").filter((k) => set.has(k));
        s.classList.toggle("hi", on.length > 0);
        for (const k of on) { lit[links[k].from] = true; lit[links[k].to] = true; }
      }
      for (const n of nodes) n.classList.toggle("lit", !!lit[n.dataset.id]);
      paintMarkers();
    }

    for (const n of nodes) {
      n.addEventListener("click", () => select(n.dataset.id));
      n.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); select(n.dataset.id); }
      });
    }
    return { select, clear, showPath, links };
  }

  function wire(svg) {
    const d = DATA[svg.id] || {};
    const parts = d.parts || {};
    const words = d.words || {};
    const card = document.querySelector(`[data-detail-for="${svg.id}"]`);
    const chipBox = document.querySelector(`[data-paths-for="${svg.id}"]`);
    const chips = [];
    const title = (id) => parts[id]?.title || id;
    const hint = d.hint || "Select a part to see what it needs and where its data goes.";

    function press(key) {
      for (const c of chips) c.setAttribute("aria-pressed", String(key !== null && c.dataset.path === key));
    }

    function heading(h, text) {
      card.replaceChildren(el("div", { class: "head" }, [el("h3", { text: h }), el("p", { class: "role", text })]));
    }

    function rel(list) {
      if (!list.length) return el("p", { class: "none", text: "Nothing in this diagram." });
      return el("div", { class: "rel" }, list.map((r) => {
        const b = el("button", { type: "button" }, [title(r.id), el("span", { text: r.label })]);
        b.addEventListener("click", () => { press(null); ex.select(r.id); });
        return b;
      }));
    }

    function render(id) {
      if (!card) return;
      const p = parts[id] || {};
      const ups = [];
      const downs = [];
      const requests = [];
      for (const l of Object.values(ex.links)) {
        if (l.request) { if (l.from === id || l.to === id) requests.push(l); continue; }
        if (l.to === id) ups.push({ id: l.from, label: l.label });
        if (l.from === id) downs.push({ id: l.to, label: l.label });
      }
      const head = el("div", { class: "head" }, [el("h3", { text: title(id) })]);
      if (p.role) head.append(el("p", { class: "role", text: p.role }));
      if (p.badge) head.append(el("p", {}, [el("span", { class: `badge ${p.badge.tone || ""}`, text: p.badge.text })]));
      const left = el("div");
      if (p.facts?.length) left.append(el("h4", { text: "Facts" }), el("ul", {}, p.facts.map((f) => el("li", { text: f }))));
      if (p.setting) left.append(el("h4", { text: "Setting" }), el("div", { class: "setting", text: p.setting }));
      if (p.text) left.append(el("p", { text: p.text }));
      const right = el("div", {}, [el("h4", { text: words.from || "Gets data from" }), rel(ups), el("h4", { text: words.to || "Sends data to" }), rel(downs)]);
      if (requests.length) {
        const text = requests.map((l) => `${title(l.from)} to ${title(l.to)}: ${l.label}`).join(". ");
        right.append(el("h4", { text: "Requests" }), el("p", { class: "none", text: `${text}.` }));
      }
      card.replaceChildren(head, el("div", { class: "cols" }, [left, right]));
      if (p.stops) card.append(el("div", { class: "stops" }, [el("h4", { text: "If it stops" }), el("p", { text: p.stops })]));
      if (p.evidence) card.append(el("p", { class: "evidence" }, [el("b", { text: "Evidence  " }), p.evidence]));
    }

    const ex = explorer(svg, (id) => { press(null); render(id); });
    for (const [k, label] of Object.entries(d.links || {})) if (ex.links[k]) ex.links[k].label = label;

    if (chipBox && d.paths) {
      const all = el("button", { class: "chip", type: "button", "aria-pressed": "false", "data-path": "", text: "All paths" });
      all.addEventListener("click", () => { press(""); ex.clear(); if (card) heading("All paths", hint); });
      chips.push(all);
      for (const [key, path] of Object.entries(d.paths)) {
        const fam = path.family === "neutral" ? "neu" : path.family || "neu";
        const b = el("button", { class: "chip", type: "button", "aria-pressed": "false", "data-path": key, "data-tone": fam }, [
          el("span", { class: "dot", style: `background:var(--${fam}-border)` }), path.label || key,
        ]);
        b.addEventListener("click", () => {
          press(key);
          ex.showPath(path.links || []);
          if (card) heading(path.title || path.label || key, path.text || "");
        });
        chips.push(b);
      }
      chipBox.replaceChildren(...chips);
    }

    if (d.select) ex.select(d.select);
    else if (card) heading("Select a part", hint);
  }

  for (const svg of document.querySelectorAll(".explorer svg[id]")) wire(svg);
})();
