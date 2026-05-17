(async function initViewer() {
  const titleEl = document.getElementById("topic-title");
  const subtitleEl = document.getElementById("topic-subtitle");
  const svg = document.getElementById("map-svg");
  const miniSvg = document.getElementById("minimap-svg");
  const detailsEl = document.getElementById("node-details");
  const pathsEl = document.getElementById("study-paths");
  const searchInput = document.getElementById("search-input");
  const searchCountEl = document.getElementById("search-count");
  const groupFiltersEl = document.getElementById("group-filters");
  const clearBtn = document.getElementById("clear-filters");
  const headerTopEl = document.querySelector(".header-top");
  const dragToggleBtn = document.getElementById("drag-toggle");
  const focusToggleBtn = document.getElementById("focus-toggle");
  const fitBtn = document.getElementById("fit-view");
  const resetViewBtn = document.getElementById("reset-view");
  const zoomHudEl = document.getElementById("zoom-hud");
  const modeHudEl = document.getElementById("mode-hud");
  const ctxMenuEl = document.getElementById("context-menu");

  const NS = "http://www.w3.org/2000/svg";
  let currentTopic = null;
  let currentMode = "multifile";
  let activeFilter = "All";
  let searchTerm = "";
  let selectedNodeId = null;
  let focusedNodeId = null;
  let activePathNodeIds = new Set();
  let activePathId = null;
  let dragMode = false;

  const nodeElements = new Map();
  const linkElements = [];
  const nodeOrder = [];
  const graphById = new Map();
  const groupById = new Map();

  const view = { tx: 0, ty: 0, scale: 1 };
  let isPanning = false;
  let panStart = { x: 0, y: 0, tx: 0, ty: 0 };
  let dragNodeId = null;
  let dragOffset = { x: 0, y: 0 };
  let ctxNodeId = null;

  const width = 1200;
  const height = 700;

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");
  }

  function toSingleFileHref(topicRef) {
    if (!topicRef) return "#";
    return String(topicRef).replace(/\.studybubble\.json$/i, ".html");
  }

  function toMultifileHref(topicRef) {
    if (!topicRef) return "#";
    const fileName = String(topicRef).split(/[\\/]/).pop() || "";
    const topicId = fileName.replace(/\.studybubble\.json$/i, "");
    return `../${topicId}/index.html`;
  }

  function topicRefToHref(topicRef, mode) {
    return mode === "single-file" ? toSingleFileHref(topicRef) : toMultifileHref(topicRef);
  }

  function topicJsonToHtmlName(topicRef) {
    if (!topicRef) return "";
    return String(topicRef).split(/[\\/]/).pop().replace(/\.studybubble\.json$/i, ".html");
  }

  function navigateToTopicRef(topicRef, mode) {
    const href = topicRefToHref(topicRef, mode);
    if (!href || href === "#") return;
    window.location.href = href;
  }

  function defaultOpenLabel(topicRef) {
    const htmlName = topicJsonToHtmlName(topicRef);
    const base = htmlName.replace(/\.html$/i, "").replaceAll("_", " ");
    return `Open ${base || "Child Topic"}`;
  }

  function nodeRadius(size) {
    if (size === "core") return 62;
    if (size === "support") return 50;
    return 40;
  }

  function wrapLabel(text, maxCharsPerLine) {
    const words = String(text || "").split(/\s+/).filter(Boolean);
    if (words.length === 0) return [""];
    const lines = [];
    let current = words[0];
    for (let i = 1; i < words.length; i += 1) {
      const candidate = `${current} ${words[i]}`;
      if (candidate.length <= maxCharsPerLine) current = candidate;
      else {
        lines.push(current);
        current = words[i];
      }
    }
    lines.push(current);
    return lines.slice(0, 3);
  }

  function nodeSearchText(node) {
    return [
      node.label,
      node.definition,
      node.whyItMatters,
      node.safeSentence,
      node.note && node.note.summary,
      node.note && node.note.commonTrap,
      node.note && node.note.interviewAnswer,
    ].filter(Boolean).join(" ").toLowerCase();
  }

  function renderExternalLinks(links) {
    if (!Array.isArray(links) || links.length === 0) return "";
    const items = links.map(
      (link) => `<li><a href="${escapeHtml(link.href || "#")}" target="_blank" rel="noopener noreferrer">${escapeHtml(link.label || "Link")}</a></li>`
    ).join("");
    return `<p><strong>External Links:</strong></p><ul>${items}</ul>`;
  }

  function renderChildTopics(childTopics, mode) {
    if (!Array.isArray(childTopics) || childTopics.length === 0) return "";
    const items = childTopics.map((child) => {
      const href = topicRefToHref(child.topic, mode);
      return `<li><a href="${escapeHtml(href)}">${escapeHtml(child.label || child.topic || "Child Topic")}</a></li>`;
    }).join("");
    return `<p><strong>Child Topics:</strong></p><ul>${items}</ul>`;
  }

  function renderChildTopicButtons(childTopics, mode) {
    if (!Array.isArray(childTopics) || childTopics.length === 0) return "";
    const buttons = childTopics.map((child) => {
      const href = topicRefToHref(child.topic, mode);
      if (!href || href === "#") return "";
      const text = child.label ? child.label : defaultOpenLabel(child.topic);
      return `<button type="button" class="nav-topic-btn child-topic-btn" data-nav-href="${escapeHtml(href)}">${escapeHtml(text)}</button>`;
    }).filter(Boolean).join("");
    if (!buttons) return "";
    return `<div class="nav-section"><p><strong>Child Topic Navigation:</strong></p><div class="nav-button-row">${buttons}</div></div>`;
  }

  function renderParentTopic(parentTopic, mode) {
    if (!parentTopic || typeof parentTopic !== "object") return "";
    const href = topicRefToHref(parentTopic.topic, mode);
    return `<p><strong>Parent Topic:</strong> <a href="${escapeHtml(href)}">${escapeHtml(parentTopic.label || "Back")}</a></p>`;
  }

  function renderTopicParentButton(topic, mode) {
    if (!headerTopEl) return;
    const existing = document.getElementById("topic-parent-nav");
    if (existing) existing.remove();
    const parentTopic = topic && topic.parentTopic && typeof topic.parentTopic === "object" ? topic.parentTopic : null;
    if (!parentTopic || !parentTopic.topic) return;
    const href = topicRefToHref(parentTopic.topic, mode);
    if (!href || href === "#") return;
    const wrap = document.createElement("div");
    wrap.id = "topic-parent-nav";
    wrap.className = "topic-parent-nav";
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "nav-topic-btn parent-topic-btn";
    btn.textContent = parentTopic.label || "Back";
    btn.addEventListener("click", () => navigateToTopicRef(parentTopic.topic, mode));
    wrap.appendChild(btn);
    headerTopEl.appendChild(wrap);
  }

  function applyViewTransform() {
    const viewport = document.getElementById("map-viewport");
    if (viewport) {
      viewport.setAttribute("transform", `translate(${view.tx} ${view.ty}) scale(${view.scale})`);
    }
    if (zoomHudEl) zoomHudEl.textContent = `${Math.round(view.scale * 100)}%`;
    renderMinimapViewport();
  }

  function resetViewTransform() {
    view.tx = 0;
    view.ty = 0;
    view.scale = 1;
    applyViewTransform();
  }

  function fitView() {
    if (graphById.size === 0) return;
    let minX = Infinity;
    let minY = Infinity;
    let maxX = -Infinity;
    let maxY = -Infinity;
    for (const node of graphById.values()) {
      minX = Math.min(minX, node.x - node.r);
      maxX = Math.max(maxX, node.x + node.r);
      minY = Math.min(minY, node.y - node.r);
      maxY = Math.max(maxY, node.y + node.r);
    }
    const pad = 40;
    minX -= pad; minY -= pad; maxX += pad; maxY += pad;
    const sx = width / Math.max(1, maxX - minX);
    const sy = height / Math.max(1, maxY - minY);
    view.scale = Math.max(0.45, Math.min(1.35, Math.min(sx, sy)));
    view.tx = (width - (minX + maxX) * view.scale) / 2;
    view.ty = (height - (minY + maxY) * view.scale) / 2;
    applyViewTransform();
  }

  function clientToWorld(clientX, clientY) {
    if (!svg) return { x: 0, y: 0 };
    const rect = svg.getBoundingClientRect();
    const sx = (clientX - rect.left) * (width / rect.width);
    const sy = (clientY - rect.top) * (height / rect.height);
    return { x: (sx - view.tx) / view.scale, y: (sy - view.ty) / view.scale };
  }

  function updateModeHud() {
    if (!modeHudEl) return;
    modeHudEl.textContent = dragMode ? "Drag mode" : "Pan mode";
  }

  function getConnectedNodeIds(nodeId) {
    const ids = new Set([nodeId]);
    for (const link of linkElements) {
      if (link.sourceId === nodeId) ids.add(link.targetId);
      if (link.targetId === nodeId) ids.add(link.sourceId);
    }
    return ids;
  }

  function updateHighlights() {
    const connectedIds = focusedNodeId ? getConnectedNodeIds(focusedNodeId) : new Set();
    for (const [id, nodeEl] of nodeElements.entries()) {
      nodeEl.group.classList.toggle("is-connected", connectedIds.has(id) && id !== focusedNodeId);
    }
    for (const link of linkElements) {
      const isPath = activePathNodeIds.has(link.sourceId) && activePathNodeIds.has(link.targetId);
      link.el.classList.toggle("is-path", isPath);
      const connected = focusedNodeId && (link.sourceId === focusedNodeId || link.targetId === focusedNodeId || (connectedIds.has(link.sourceId) && connectedIds.has(link.targetId)));
      link.el.classList.toggle("is-connected", !!connected);
      link.el.classList.toggle("is-dim", !!focusedNodeId && !connected);
    }
  }

  function renderDetails(node, topic, mode) {
    const noteSummary = node.note && node.note.summary ? node.note.summary : "N/A";
    const hasOneChildTopic = Array.isArray(node.childTopics) && node.childTopics.length === 1;
    const hasParentTopic = !!(topic && topic.parentTopic && topic.parentTopic.topic);
    const doubleClickHint = hasOneChildTopic
      ? `<p><em>Double-click this bubble to open: ${escapeHtml(node.childTopics[0].label || node.childTopics[0].topic || "Child Topic")}</em></p>`
      : hasParentTopic
      ? `<p><em>Double-click this bubble to go back to parent topic: ${escapeHtml(topic.parentTopic.label || topic.parentTopic.topic || "Back")}</em></p>`
      : "";
    detailsEl.innerHTML = `
      <p><strong>Label:</strong> ${escapeHtml(node.label)}</p>
      <p><strong>Group:</strong> ${escapeHtml(node.group)}</p>
      <p><strong>Definition:</strong> ${escapeHtml(node.definition)}</p>
      <p><strong>Why It Matters:</strong> ${escapeHtml(node.whyItMatters || "")}</p>
      <p><strong>Safe Sentence:</strong> ${escapeHtml(node.safeSentence || "")}</p>
      <p><strong>Note:</strong> ${escapeHtml(noteSummary)}</p>
      ${doubleClickHint}
      ${renderExternalLinks(node.externalLinks)}
      ${renderChildTopicButtons(node.childTopics, mode)}
      ${renderChildTopics(node.childTopics, mode)}
      ${renderParentTopic(topic.parentTopic, mode)}
    `;
    for (const button of detailsEl.querySelectorAll(".nav-topic-btn[data-nav-href]")) {
      button.addEventListener("click", () => {
        const href = button.getAttribute("data-nav-href");
        if (!href || href === "#") return;
        window.location.href = href;
      });
    }
  }

  function setSelectedNode(nodeId, alsoFocus = false) {
    selectedNodeId = nodeId;
    if (alsoFocus) focusedNodeId = nodeId;
    for (const [id, el] of nodeElements.entries()) {
      el.group.classList.toggle("is-active", id === nodeId);
    }
    const node = graphById.get(nodeId);
    if (node) renderDetails(node, currentTopic, currentMode);
    updateHighlights();
  }

  function shouldNodeBeVisible(node) {
    const groupMatch = activeFilter === "All" || node.group === activeFilter;
    if (!groupMatch) return false;
    if (!searchTerm.trim()) return true;
    return nodeSearchText(node).includes(searchTerm.trim().toLowerCase());
  }

  function applyVisibility() {
    const visibleIds = new Set();
    let matchCount = 0;
    for (const node of graphById.values()) {
      const visible = shouldNodeBeVisible(node);
      const nodeEl = nodeElements.get(node.id);
      if (!nodeEl) continue;
      nodeEl.group.style.opacity = visible ? "1" : "0.15";
      if (visible) {
        visibleIds.add(node.id);
        if (searchTerm.trim()) matchCount += 1;
      }
    }
    for (const linkEl of linkElements) {
      const srcVisible = visibleIds.has(linkEl.sourceId);
      const tgtVisible = visibleIds.has(linkEl.targetId);
      linkEl.el.style.opacity = srcVisible && tgtVisible ? "" : "0.1";
    }
    if (searchCountEl) {
      searchCountEl.textContent = searchTerm.trim() ? `${matchCount} match${matchCount === 1 ? "" : "es"}` : "";
    }
    if (selectedNodeId && !visibleIds.has(selectedNodeId)) {
      selectedNodeId = null;
      focusedNodeId = null;
      detailsEl.innerHTML = "<p>Select a visible bubble to view details.</p>";
    }
    updateHighlights();
  }

  function renderGroupFilters(topic) {
    if (!groupFiltersEl) return;
    groupFiltersEl.innerHTML = "";
    const groups = ["All", ...((topic.groups || []).map((g) => g.label).filter(Boolean))];
    for (const groupName of groups) {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "filter-btn";
      btn.textContent = groupName;
      if (groupName === activeFilter) btn.classList.add("is-active");
      btn.addEventListener("click", () => {
        activeFilter = groupName;
        for (const b of groupFiltersEl.querySelectorAll(".filter-btn")) {
          b.classList.toggle("is-active", b.textContent === groupName);
        }
        applyVisibility();
      });
      groupFiltersEl.appendChild(btn);
    }
  }

  function renderPaths(paths) {
    if (!pathsEl) return;
    pathsEl.innerHTML = "";
    if (!paths || paths.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No study paths.";
      pathsEl.appendChild(li);
      return;
    }
    for (const path of paths) {
      const li = document.createElement("li");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "path-item-btn";
      btn.dataset.pathId = path.id || path.label || "";
      btn.innerHTML = `<strong>${escapeHtml(path.label)}</strong><br>${escapeHtml(path.description || "")}`;
      btn.addEventListener("click", () => {
        const thisPathId = path.id || path.label || "";
        if (activePathId === thisPathId) {
          activePathId = null;
          activePathNodeIds = new Set();
        } else {
          activePathId = thisPathId;
          activePathNodeIds = new Set(path.nodeIds || []);
        }
        for (const b of pathsEl.querySelectorAll(".path-item-btn")) {
          b.classList.toggle("is-active", b.dataset.pathId === activePathId);
        }
        updateHighlights();
      });
      li.appendChild(btn);
      pathsEl.appendChild(li);
    }
  }

  function renderMinimap() {
    if (!miniSvg) return;
    miniSvg.innerHTML = "";
    for (const link of linkElements) {
      const source = graphById.get(link.sourceId);
      const target = graphById.get(link.targetId);
      if (!source || !target) continue;
      const line = document.createElementNS(NS, "line");
      line.setAttribute("x1", String(source.x));
      line.setAttribute("y1", String(source.y));
      line.setAttribute("x2", String(target.x));
      line.setAttribute("y2", String(target.y));
      line.setAttribute("stroke", "#64748b");
      line.setAttribute("stroke-width", "1.5");
      line.setAttribute("opacity", "0.8");
      miniSvg.appendChild(line);
    }
    for (const node of graphById.values()) {
      const dot = document.createElementNS(NS, "circle");
      dot.setAttribute("cx", String(node.x));
      dot.setAttribute("cy", String(node.y));
      dot.setAttribute("r", String(Math.max(5, node.r / 6)));
      dot.setAttribute("fill", "#60a5fa");
      dot.setAttribute("stroke", "#e2e8f0");
      dot.setAttribute("stroke-width", "1");
      miniSvg.appendChild(dot);
    }
    const viewportRect = document.createElementNS(NS, "rect");
    viewportRect.setAttribute("id", "mini-viewport");
    viewportRect.setAttribute("fill", "none");
    viewportRect.setAttribute("stroke", "#f8fafc");
    viewportRect.setAttribute("stroke-width", "2");
    miniSvg.appendChild(viewportRect);
    renderMinimapViewport();
  }

  function renderMinimapViewport() {
    const rect = document.getElementById("mini-viewport");
    if (!rect) return;
    rect.setAttribute("x", String((-view.tx) / view.scale));
    rect.setAttribute("y", String((-view.ty) / view.scale));
    rect.setAttribute("width", String(width / view.scale));
    rect.setAttribute("height", String(height / view.scale));
  }

  function buildLayout(nodes, topic) {
    const marginX = 120;
    const minY = 90;
    const maxY = 610;
    const visualCenterY = 330;
    const groups = (topic.groups || []).map((g) => g.label).filter(Boolean);
    const groupedNodes = new Map();
    for (const node of nodes) {
      const key = node.group || "Ungrouped";
      if (!groupedNodes.has(key)) groupedNodes.set(key, []);
      groupedNodes.get(key).push(node);
    }
    const groupOrder = [...groups, ...[...groupedNodes.keys()].filter((k) => !groups.includes(k))];
    const activeGroups = groupOrder.filter((k) => groupedNodes.has(k));
    const groupCount = Math.max(activeGroups.length, 1);
    const groupSpan = groupCount > 1 ? (width - marginX * 2) / (groupCount - 1) : 0;
    const positioned = [];
    for (let gIndex = 0; gIndex < activeGroups.length; gIndex += 1) {
      const groupName = activeGroups[gIndex];
      const groupNodes = groupedNodes.get(groupName) || [];
      const centerX = marginX + groupSpan * gIndex;
      const columns = Math.max(2, Math.ceil(Math.sqrt(groupNodes.length)));
      const colGap = 130;
      const rowGap = 122;
      for (let i = 0; i < groupNodes.length; i += 1) {
        const node = groupNodes[i];
        const col = i % columns;
        const row = Math.floor(i / columns);
        const rowOffset = (row - 0.5) * rowGap;
        const colOffset = (col - (columns - 1) / 2) * colGap;
        positioned.push({
          ...node,
          x: centerX + colOffset,
          y: Math.max(minY, Math.min(maxY, visualCenterY + rowOffset)),
          r: nodeRadius(node.size),
        });
      }
    }
    for (let iter = 0; iter < 110; iter += 1) {
      for (let i = 0; i < positioned.length; i += 1) {
        for (let j = i + 1; j < positioned.length; j += 1) {
          const a = positioned[i];
          const b = positioned[j];
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const dist = Math.hypot(dx, dy) || 0.0001;
          const minDist = a.r + b.r + 34;
          if (dist < minDist) {
            const push = (minDist - dist) / 2;
            const ux = dx / dist;
            const uy = dy / dist;
            a.x -= ux * push; a.y -= uy * push;
            b.x += ux * push; b.y += uy * push;
          }
        }
      }
      for (const n of positioned) {
        n.x = Math.max(marginX - 20, Math.min(width - marginX + 20, n.x));
        n.y = Math.max(minY, Math.min(maxY, n.y));
      }
    }
    return positioned;
  }

  function drawTopic(topic, mode) {
    currentTopic = topic;
    currentMode = mode;
    activeFilter = "All";
    searchTerm = "";
    selectedNodeId = null;
    focusedNodeId = null;
    activePathNodeIds = new Set();
    activePathId = null;
    if (searchInput) searchInput.value = "";
    if (searchCountEl) searchCountEl.textContent = "";
    titleEl.textContent = topic.title || "StudyBubble Topic";
    subtitleEl.textContent = topic.subtitle || "";
    renderTopicParentButton(topic, mode);

    svg.innerHTML = "";
    nodeElements.clear();
    linkElements.length = 0;
    graphById.clear();
    groupById.clear();
    nodeOrder.length = 0;

    svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    const nodes = Array.isArray(topic.nodes) ? topic.nodes : [];
    const links = Array.isArray(topic.links) ? topic.links : [];
    const positioned = buildLayout(nodes, topic);
    const positionById = new Map(positioned.map((n) => [n.id, n]));

    const viewport = document.createElementNS(NS, "g");
    viewport.setAttribute("id", "map-viewport");
    svg.appendChild(viewport);

    const linkLayer = document.createElementNS(NS, "g");
    const nodeLayer = document.createElementNS(NS, "g");
    viewport.appendChild(linkLayer);
    viewport.appendChild(nodeLayer);

    for (const p of positioned) {
      graphById.set(p.id, p);
      groupById.set(p.id, p.group);
      nodeOrder.push(p.id);
    }

    for (const link of links) {
      const source = positionById.get(link.source);
      const target = positionById.get(link.target);
      if (!source || !target) continue;
      const line = document.createElementNS(NS, "line");
      line.setAttribute("class", "link-line");
      line.setAttribute("x1", String(source.x));
      line.setAttribute("y1", String(source.y));
      line.setAttribute("x2", String(target.x));
      line.setAttribute("y2", String(target.y));
      linkLayer.appendChild(line);
      linkElements.push({ el: line, sourceId: link.source, targetId: link.target });
    }

    for (const node of positioned) {
      const group = document.createElementNS(NS, "g");
      group.setAttribute("class", "bubble-node");
      group.setAttribute("tabindex", "0");
      group.dataset.nodeId = node.id;

      const circle = document.createElementNS(NS, "circle");
      circle.setAttribute("class", "bubble-circle");
      circle.setAttribute("cx", String(node.x));
      circle.setAttribute("cy", String(node.y));
      circle.setAttribute("r", String(node.r));

      const text = document.createElementNS(NS, "text");
      text.setAttribute("class", "bubble-label");
      text.setAttribute("x", String(node.x));
      text.setAttribute("y", String(node.y));
      const maxCharsPerLine = node.size === "core" ? 13 : node.size === "support" ? 11 : 10;
      const lines = wrapLabel(node.label, maxCharsPerLine);
      const lineHeight = 16;
      const startOffset = -((lines.length - 1) * lineHeight) / 2;
      for (let i = 0; i < lines.length; i += 1) {
        const tspan = document.createElementNS(NS, "tspan");
        tspan.setAttribute("x", String(node.x));
        tspan.setAttribute("dy", i === 0 ? String(startOffset) : String(lineHeight));
        tspan.textContent = lines[i];
        text.appendChild(tspan);
      }

      group.appendChild(circle);
      group.appendChild(text);
      nodeLayer.appendChild(group);
      nodeElements.set(node.id, { group, node, circle, text });

      function activate(alsoFocus = false) {
        setSelectedNode(node.id, alsoFocus);
      }
      function openSingleChild() {
        const childTopics = Array.isArray(node.childTopics) ? node.childTopics : [];
        if (childTopics.length === 1) navigateToTopicRef(childTopics[0].topic, mode);
      }
      function openParent() {
        const parentTopic = topic && topic.parentTopic && typeof topic.parentTopic === "object" ? topic.parentTopic : null;
        if (parentTopic && parentTopic.topic) navigateToTopicRef(parentTopic.topic, mode);
      }

      group.addEventListener("click", () => activate());
      group.addEventListener("dblclick", () => {
        activate();
        const childTopics = Array.isArray(node.childTopics) ? node.childTopics : [];
        if (childTopics.length === 1) openSingleChild();
        else openParent();
      });
      group.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          activate(true);
        }
      });
      group.addEventListener("contextmenu", (event) => {
        event.preventDefault();
        activate();
        ctxNodeId = node.id;
        if (!ctxMenuEl) return;
        ctxMenuEl.style.left = `${event.clientX + 8}px`;
        ctxMenuEl.style.top = `${event.clientY + 8}px`;
        ctxMenuEl.classList.add("open");
        ctxMenuEl.setAttribute("aria-hidden", "false");
      });
      group.addEventListener("mousedown", (event) => {
        if (!dragMode || event.button !== 0) return;
        event.preventDefault();
        dragNodeId = node.id;
        const world = clientToWorld(event.clientX, event.clientY);
        dragOffset = { x: world.x - node.x, y: world.y - node.y };
        svg.classList.add("is-dragging");
      });

      const childTopics = Array.isArray(node.childTopics) ? node.childTopics : [];
      if (childTopics.length === 1) group.setAttribute("title", `Double-click to open ${childTopics[0].label || childTopics[0].topic || "child topic"}`);
      else if (topic.parentTopic && topic.parentTopic.topic) group.setAttribute("title", `Double-click to go back to ${topic.parentTopic.label || topic.parentTopic.topic || "parent topic"}`);
    }

    renderGroupFilters(topic);
    renderPaths(topic.paths || []);
    if (nodes.length > 0) setSelectedNode(nodes[0].id);
    resetViewTransform();
    fitView();
    renderMinimap();
    applyVisibility();
    updateModeHud();
  }

  function refreshNodeGeometry(nodeId) {
    const n = graphById.get(nodeId);
    const el = nodeElements.get(nodeId);
    if (!n || !el) return;
    el.circle.setAttribute("cx", String(n.x));
    el.circle.setAttribute("cy", String(n.y));
    el.text.setAttribute("x", String(n.x));
    el.text.setAttribute("y", String(n.y));
    for (const tspan of el.text.querySelectorAll("tspan")) {
      tspan.setAttribute("x", String(n.x));
    }
    for (const link of linkElements) {
      if (link.sourceId === nodeId) {
        link.el.setAttribute("x1", String(n.x));
        link.el.setAttribute("y1", String(n.y));
      } else if (link.targetId === nodeId) {
        link.el.setAttribute("x2", String(n.x));
        link.el.setAttribute("y2", String(n.y));
      }
    }
    if (miniSvg) renderMinimap();
  }

  function handleKeyboard(event) {
    if (!currentTopic || !nodeOrder.length) return;
    const idx = Math.max(0, nodeOrder.indexOf(selectedNodeId || nodeOrder[0]));
    if (event.key === "Escape") {
      selectedNodeId = null;
      focusedNodeId = null;
      detailsEl.innerHTML = "<p>Select a bubble to view details.</p>";
      for (const [, el] of nodeElements.entries()) el.group.classList.remove("is-active");
      updateHighlights();
      return;
    }
    if (event.key.toLowerCase() === "f" && selectedNodeId) {
      focusedNodeId = focusedNodeId === selectedNodeId ? null : selectedNodeId;
      updateHighlights();
      return;
    }
    if (!["ArrowRight", "ArrowLeft", "ArrowDown", "ArrowUp", "Tab"].includes(event.key)) return;
    event.preventDefault();
    const next = event.key === "ArrowLeft" || (event.key === "Tab" && event.shiftKey)
      ? (idx - 1 + nodeOrder.length) % nodeOrder.length
      : (idx + 1) % nodeOrder.length;
    setSelectedNode(nodeOrder[next]);
  }

  function loadTopic() {
    const embedded = document.getElementById("studybubble-topic-data");
    if (embedded) return Promise.resolve(JSON.parse(embedded.textContent || "{}"));
    return fetch("topic.studybubble.json").then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    });
  }

  if (svg) {
    svg.addEventListener("wheel", (event) => {
      event.preventDefault();
      const world = clientToWorld(event.clientX, event.clientY);
      const factor = event.deltaY < 0 ? 1.1 : 0.92;
      const nextScale = Math.max(0.4, Math.min(2.2, view.scale * factor));
      view.tx = world.x * (view.scale - nextScale) + view.tx;
      view.ty = world.y * (view.scale - nextScale) + view.ty;
      view.scale = nextScale;
      applyViewTransform();
    }, { passive: false });

    svg.addEventListener("mousedown", (event) => {
      if (event.button !== 0 || dragMode) return;
      if (event.target.closest(".bubble-node")) return;
      isPanning = true;
      panStart = { x: event.clientX, y: event.clientY, tx: view.tx, ty: view.ty };
      svg.classList.add("is-panning");
    });
  }

  window.addEventListener("mousemove", (event) => {
    if (dragNodeId) {
      const world = clientToWorld(event.clientX, event.clientY);
      const n = graphById.get(dragNodeId);
      if (!n) return;
      n.x = world.x - dragOffset.x;
      n.y = world.y - dragOffset.y;
      refreshNodeGeometry(dragNodeId);
      return;
    }
    if (!isPanning) return;
    view.tx = panStart.tx + (event.clientX - panStart.x);
    view.ty = panStart.ty + (event.clientY - panStart.y);
    applyViewTransform();
  });

  window.addEventListener("mouseup", () => {
    isPanning = false;
    dragNodeId = null;
    svg.classList.remove("is-panning");
    svg.classList.remove("is-dragging");
  });

  document.addEventListener("click", (event) => {
    if (ctxMenuEl && !ctxMenuEl.contains(event.target)) {
      ctxMenuEl.classList.remove("open");
      ctxMenuEl.setAttribute("aria-hidden", "true");
    }
  });

  if (ctxMenuEl) ctxMenuEl.addEventListener("click", (event) => {
    const btn = event.target.closest(".ctx-item");
    if (!btn || !ctxNodeId) return;
    const action = btn.dataset.action;
    if (action === "reset") {
      resetViewTransform();
      focusedNodeId = null;
      updateHighlights();
      ctxMenuEl.classList.remove("open");
      ctxMenuEl.setAttribute("aria-hidden", "true");
      return;
    }
    if (!ctxNodeId) {
      ctxMenuEl.classList.remove("open");
      ctxMenuEl.setAttribute("aria-hidden", "true");
      return;
    }
    if (action === "pin") setSelectedNode(ctxNodeId);
    else if (action === "focus") {
      focusedNodeId = ctxNodeId;
      updateHighlights();
    } else if (action === "filter") {
      const group = groupById.get(ctxNodeId);
      if (group) {
        activeFilter = group;
        if (groupFiltersEl) {
          for (const b of groupFiltersEl.querySelectorAll(".filter-btn")) {
            b.classList.toggle("is-active", b.textContent === group);
          }
        }
        applyVisibility();
      }
    }
    ctxMenuEl.classList.remove("open");
    ctxMenuEl.setAttribute("aria-hidden", "true");
  });

  if (searchInput) {
    searchInput.addEventListener("input", () => {
      searchTerm = searchInput.value || "";
      applyVisibility();
    });
  }

  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      searchTerm = "";
      if (searchInput) searchInput.value = "";
      activeFilter = "All";
      selectedNodeId = null;
      focusedNodeId = null;
      activePathNodeIds = new Set();
      activePathId = null;
      if (groupFiltersEl) {
        for (const b of groupFiltersEl.querySelectorAll(".filter-btn")) {
          b.classList.toggle("is-active", b.textContent === "All");
        }
      }
      if (pathsEl) {
        for (const b of pathsEl.querySelectorAll(".path-item-btn")) {
          b.classList.remove("is-active");
        }
      }
      detailsEl.innerHTML = "<p>Select a bubble to view details.</p>";
      applyVisibility();
      resetViewTransform();
    });
  }

  if (dragToggleBtn) {
    dragToggleBtn.addEventListener("click", () => {
      dragMode = !dragMode;
      dragToggleBtn.classList.toggle("is-active", dragMode);
      updateModeHud();
    });
  }
  if (focusToggleBtn) {
    focusToggleBtn.addEventListener("click", () => {
      if (!selectedNodeId) return;
      focusedNodeId = focusedNodeId === selectedNodeId ? null : selectedNodeId;
      focusToggleBtn.classList.toggle("is-active", !!focusedNodeId);
      updateHighlights();
    });
  }
  if (fitBtn) fitBtn.addEventListener("click", fitView);
  if (resetViewBtn) resetViewBtn.addEventListener("click", resetViewTransform);
  document.addEventListener("keydown", handleKeyboard);

  try {
    const topic = await loadTopic();
    const mode = document.getElementById("studybubble-topic-data") ? "single-file" : "multifile";
    drawTopic(topic, mode);
  } catch (error) {
    titleEl.textContent = "Failed to load topic";
    subtitleEl.textContent = String(error);
    detailsEl.innerHTML = "<p>Could not load topic data.</p>";
  }
})();
