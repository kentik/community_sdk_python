// Tabs for a report page: the HTML view and its Markdown twin. Without
// this script both panels show, one under the other, and the tabs work as
// plain anchor links.
(() => {
  const bar = document.querySelector('[role="tablist"].report-tabs');
  if (!bar) return;
  const tabs = [...bar.querySelectorAll('[role="tab"]')];
  const panels = tabs.map((tab) => document.getElementById(tab.getAttribute('aria-controls')));

  // Mermaid measures text, so it can draw only in a visible panel.
  function drawMermaid() {
    const nodes = panels.flatMap((panel) => (panel.hidden ? [] : [...panel.querySelectorAll('pre.mermaid:not([data-processed])')]));
    if (window.mermaid && nodes.length) window.mermaid.run({ nodes });
  }

  function show(index, focus) {
    tabs.forEach((tab, i) => {
      const on = i === index;
      tab.setAttribute('aria-selected', String(on));
      tab.tabIndex = on ? 0 : -1;
      panels[i].hidden = !on;
    });
    if (focus) tabs[index].focus();
    drawMermaid();
  }

  // A hash that names an element inside a panel opens that panel first.
  function follow() {
    const id = decodeURIComponent(location.hash.slice(1));
    const target = id && document.getElementById(id);
    const index = target ? panels.findIndex((panel) => panel.contains(target)) : -1;
    show(Math.max(index, 0), false);
    if (target && target !== panels[index]) target.scrollIntoView();
  }

  tabs.forEach((tab, i) => {
    tab.addEventListener('click', (event) => {
      event.preventDefault();
      history.replaceState(null, '', `#${panels[i].id}`);
      show(i, false);
    });
    tab.addEventListener('keydown', (event) => {
      const step = { ArrowRight: 1, ArrowLeft: -1 }[event.key];
      if (!step) return;
      event.preventDefault();
      const next = (i + step + tabs.length) % tabs.length;
      history.replaceState(null, '', `#${panels[next].id}`);
      show(next, true);
    });
  });
  addEventListener('hashchange', follow);
  document.addEventListener('mermaid-ready', drawMermaid);
  follow();
})();
