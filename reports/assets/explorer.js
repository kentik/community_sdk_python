/* Explorer for report diagrams built with diagram_kit.py. */
(() => {
  "use strict";
  const DATA = JSON.parse(document.getElementById("diagram-data")?.textContent || "{}");

  function el(tag, attrs = {}, children = []) {
    const element = document.createElement(tag);
    for (const [key, value] of Object.entries(attrs)) {
      if (key === "text") element.textContent = value;
      else element.setAttribute(key, value);
    }
    for (const child of children) if (child) element.append(child);
    return element;
  }

  function explorer(svg, onSelect) {
    const nodes = [...svg.querySelectorAll(".node[data-id]")];
    const segments = [...svg.querySelectorAll(".edge[data-links]")];
    const highlightMarker = svg.querySelector('marker[id$="-ah-hi"]');
    const links = {};

    for (const segment of segments) {
      const label = segment.querySelector(".elabel")?.textContent || "";
      const request = segment.classList.contains("access") || segment.classList.contains("call");
      for (const key of segment.dataset.links.split(",")) {
        const [from, to] = key.split(">");
        links[key] ??= { from, to, request, label: "" };
        if (!links[key].label) links[key].label = label;
      }
      const path = segment.querySelector("path[marker-end]");
      if (path) path.dataset.marker = path.getAttribute("marker-end");
    }

    function closure(start, direction) {
      const seen = {};
      const stack = [start];
      while (stack.length) {
        const node = stack.pop();
        for (const link of Object.values(links)) {
          if (link.request) continue;
          const [from, to] = direction === "up" ? [link.to, link.from] : [link.from, link.to];
          if (from === node && !seen[to] && to !== start) {
            seen[to] = true;
            stack.push(to);
          }
        }
      }
      return seen;
    }

    function paintMarkers() {
      for (const segment of segments) {
        const path = segment.querySelector("path[data-marker]");
        if (!path || !highlightMarker) continue;
        const highlighted = segment.classList.contains("hi") || segment.classList.contains("flow");
        path.setAttribute("marker-end", highlighted ? `url(#${highlightMarker.id})` : path.dataset.marker);
      }
    }

    function clear() {
      svg.classList.remove("dimming");
      for (const node of nodes) node.classList.remove("sel", "lit");
      for (const segment of segments) segment.classList.remove("hi", "flow");
      paintMarkers();
    }

    function select(id) {
      const upstream = closure(id, "up");
      const downstream = closure(id, "down");
      const lit = { [id]: true, ...upstream, ...downstream };
      svg.classList.add("dimming");
      for (const segment of segments) {
        let highlighted = false;
        let flowing = false;
        for (const key of segment.dataset.links.split(",")) {
          const link = links[key];
          if (link.request) {
            if (link.from === id || link.to === id) {
              flowing = true;
              lit[link.from] = true;
              lit[link.to] = true;
            }
            continue;
          }
          if (upstream[link.from] && (upstream[link.to] || link.to === id)) highlighted = true;
          if ((downstream[link.from] || link.from === id) && downstream[link.to]) flowing = true;
        }
        segment.classList.toggle("hi", highlighted);
        segment.classList.toggle("flow", flowing && !highlighted);
      }
      for (const node of nodes) {
        node.classList.toggle("sel", node.dataset.id === id);
        node.classList.toggle("lit", !!lit[node.dataset.id]);
      }
      paintMarkers();
      onSelect(id);
    }

    function showPath(keys) {
      clear();
      svg.classList.add("dimming");
      const selected = new Set(keys);
      const lit = {};
      for (const segment of segments) {
        const active = segment.dataset.links.split(",").filter((key) => selected.has(key));
        segment.classList.toggle("hi", active.length > 0);
        for (const key of active) {
          lit[links[key].from] = true;
          lit[links[key].to] = true;
        }
      }
      for (const node of nodes) node.classList.toggle("lit", !!lit[node.dataset.id]);
      paintMarkers();
    }

    for (const node of nodes) {
      node.addEventListener("click", () => select(node.dataset.id));
      node.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          select(node.dataset.id);
        }
      });
    }
    return { select, clear, showPath, links };
  }

  function wire(svg) {
    const data = DATA[svg.id] || {};
    const parts = data.parts || {};
    const card = document.querySelector(`[data-detail-for="${svg.id}"]`);
    const chipBox = document.querySelector(`[data-paths-for="${svg.id}"]`);
    const chips = [];
    const title = (id) => parts[id]?.title || id;
    const hint = data.hint || "Select a part to see its role, evidence, and impact.";

    function press(key) {
      for (const chip of chips) chip.setAttribute("aria-pressed", String(key !== null && chip.dataset.path === key));
    }

    function showHeading(heading, text) {
      if (!card) return;
      card.replaceChildren(el("div", { class: "head" }, [el("h3", { text: heading }), el("p", { class: "role", text })]));
    }

    function relations(items, instance) {
      if (!items.length) return el("p", { class: "none", text: "Nothing in this diagram." });
      return el("div", { class: "rel" }, items.map((item) => {
        const button = el("button", { type: "button" }, [title(item.id), el("span", { text: item.label })]);
        button.addEventListener("click", () => { press(null); instance.select(item.id); });
        return button;
      }));
    }

    function render(id, instance) {
      if (!card) return;
      const part = parts[id] || {};
      const incoming = [];
      const outgoing = [];
      const requests = [];
      for (const link of Object.values(instance.links)) {
        if (link.request) {
          if (link.from === id || link.to === id) requests.push(link);
          continue;
        }
        if (link.to === id) incoming.push({ id: link.from, label: link.label });
        if (link.from === id) outgoing.push({ id: link.to, label: link.label });
      }
      const heading = el("div", { class: "head" }, [el("h3", { text: title(id) })]);
      if (part.role) heading.append(el("p", { class: "role", text: part.role }));
      if (part.badge) heading.append(el("p", {}, [el("span", { class: `badge ${part.badge.tone || ""}`, text: part.badge.text })]));
      const facts = el("div");
      if (part.facts?.length) facts.append(el("h4", { text: "Facts" }), el("ul", {}, part.facts.map((fact) => el("li", { text: fact }))));
      if (part.setting) facts.append(el("h4", { text: "Setting" }), el("div", { class: "setting", text: part.setting }));
      if (part.text) facts.append(el("p", { text: part.text }));
      const relationsBox = el("div", {}, [el("h4", { text: "Gets data from" }), relations(incoming, instance), el("h4", { text: "Sends data to" }), relations(outgoing, instance)]);
      if (requests.length) {
        relationsBox.append(el("h4", { text: "Requests" }), el("p", { class: "none", text: `${requests.map((link) => `${title(link.from)} to ${title(link.to)}: ${link.label}`).join(". ")}.` }));
      }
      card.replaceChildren(heading, el("div", { class: "cols" }, [facts, relationsBox]));
      if (part.stops) card.append(el("div", { class: "stops" }, [el("h4", { text: "If it stops" }), el("p", { text: part.stops })]));
      if (part.evidence) card.append(el("p", { class: "evidence" }, [el("b", { text: "Evidence  " }), part.evidence]));
    }

    const instance = explorer(svg, (id) => { press(null); render(id, instance); });
    for (const [key, label] of Object.entries(data.links || {})) if (instance.links[key]) instance.links[key].label = label;
    if (chipBox && data.paths) {
      const all = el("button", { class: "chip", type: "button", "aria-pressed": "false", "data-path": "", text: "All paths" });
      all.addEventListener("click", () => { press(""); instance.clear(); showHeading("All paths", hint); });
      chips.push(all);
      for (const [key, path] of Object.entries(data.paths)) {
        const family = path.family === "neutral" ? "neu" : path.family || "neu";
        const button = el("button", { class: "chip", type: "button", "aria-pressed": "false", "data-path": key }, [el("span", { class: "dot", style: `background:var(--${family}-border)` }), path.label || key]);
        button.addEventListener("click", () => { press(key); instance.showPath(path.links || []); showHeading(path.title || path.label || key, path.text || ""); });
        chips.push(button);
      }
      chipBox.replaceChildren(...chips);
    }
    if (data.select) instance.select(data.select);
    else showHeading("Select a part", hint);
  }

  for (const svg of document.querySelectorAll(".explorer svg[id]")) wire(svg);
})();
