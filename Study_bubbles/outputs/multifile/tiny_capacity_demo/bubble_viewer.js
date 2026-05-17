(async function initViewer() {
  const titleEl = document.getElementById("topic-title");
  const subtitleEl = document.getElementById("topic-subtitle");
  const svg = document.getElementById("map-svg");
  const detailsEl = document.getElementById("node-details");
  const pathsEl = document.getElementById("study-paths");
  const searchInput = document.getElementById("search-input");
  const searchCountEl = document.getElementById("search-count");
  const groupFiltersEl = document.getElementById("group-filters");
  const clearBtn = document.getElementById("clear-filters");

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
    if (mode === "single-file") return toSingleFileHref(topicRef);
    return toMultifileHref(topicRef);
  }

  function renderExternalLinks(links) {
    if (!Array.isArray(links) || links.length === 0) return "";
    const items = links
      .map(
        (link) =>
          `<li><a href="${escapeHtml(link.href || "#")}" target="_blank" rel="noopener noreferrer">${escapeHtml(link.label || "Link")}</a></li>`
      )
      .join("");
    return `<p><strong>External Links:</strong></p><ul>${items}</ul>`;
  }

  function renderChildTopics(childTopics, mode) {
    if (!Array.isArray(childTopics) || childTopics.length === 0) return "";
    const items = childTopics
      .map((child) => {
        const href = topicRefToHref(child.topic, mode);
        return `<li><a href="${escapeHtml(href)}">${escapeHtml(child.label || child.topic || "Child Topic")}</a></li>`;
      })
      .join("");
    return `<p><strong>Child Topics:</strong></p><ul>${items}</ul>`;
  }

  function renderParentTopic(parentTopic, mode) {
    if (!parentTopic || typeof parentTopic !== "object") return "";
    const href = topicRefToHref(parentTopic.topic, mode);
    return `<p><strong>Parent Topic:</strong> <a href="${escapeHtml(href)}">${escapeHtml(parentTopic.label || "Back")}</a></p>`;
  }

  function nodeSearchText(node) {
    return [
      node.label,
      node.definition,
      node.whyItMatters,
      node.safeSentence,
      node.note && node.note.summary,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
  }

  let currentTopic = null;
  let currentMode = "multifile";
  let activeFilter = "All";
  let searchTerm = "";
  let selectedNodeId = null;
  const nodeElements = new Map();
  const linkElements = [];

  function renderDetails(node, topic, mode) {
    const noteSummary = node.note && node.note.summary ? node.note.summary : "N/A";
    const hasOneChildTopic = Array.isArray(node.childTopics) && node.childTopics.length === 1;
    const doubleClickHint = hasOneChildTopic
      ? `<p><em>Double-click this bubble to open: ${escapeHtml(node.childTopics[0].label || node.childTopics[0].topic || "Child Topic")}</em></p>`
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
      ${renderChildTopics(node.childTopics, mode)}
      ${renderParentTopic(topic.parentTopic, mode)}
    `;
  }

  function renderPaths(paths) {
    pathsEl.innerHTML = "";
    if (!paths || paths.length === 0) {
      const li = document.createElement("li");
      li.textContent = "No study paths.";
      pathsEl.appendChild(li);
      return;
    }

    for (const path of paths) {
      const li = document.createElement("li");
      li.innerHTML = `<strong>${escapeHtml(path.label)}</strong><br>${escapeHtml(path.description || "")}`;
      pathsEl.appendChild(li);
    }
  }

  function setSelectedNode(nodeId) {
    selectedNodeId = nodeId;
    for (const [id, el] of nodeElements.entries()) {
      if (id === nodeId) {
        el.group.classList.add("is-active");
      } else {
        el.group.classList.remove("is-active");
      }
    }
    const node = (currentTopic.nodes || []).find((n) => n.id === nodeId);
    if (node) renderDetails(node, currentTopic, currentMode);
  }

  function shouldNodeBeVisible(node) {
    const groupMatch = activeFilter === "All" || node.group === activeFilter;
    if (!groupMatch) return false;

    if (!searchTerm.trim()) return true;
    return nodeSearchText(node).includes(searchTerm.trim().toLowerCase());
  }

  function applyVisibility() {
    if (!currentTopic) return;

    const visibleNodeIds = new Set();
    let matchCount = 0;

    for (const node of currentTopic.nodes || []) {
      const visible = shouldNodeBeVisible(node);
      const nodeEl = nodeElements.get(node.id);
      if (!nodeEl) continue;

      if (visible) {
        nodeEl.group.style.opacity = "1";
        visibleNodeIds.add(node.id);
        if (searchTerm.trim()) matchCount += 1;
      } else {
        nodeEl.group.style.opacity = "0.15";
      }
    }

    for (const linkEl of linkElements) {
      const srcVisible = visibleNodeIds.has(linkEl.sourceId);
      const tgtVisible = visibleNodeIds.has(linkEl.targetId);
      linkEl.el.style.opacity = srcVisible && tgtVisible ? "0.85" : "0.1";
    }

    if (searchCountEl) {
      if (searchTerm.trim()) {
        searchCountEl.textContent = `${matchCount} match${matchCount === 1 ? "" : "es"}`;
      } else {
        searchCountEl.textContent = "";
      }
    }

    if (selectedNodeId && !visibleNodeIds.has(selectedNodeId)) {
      selectedNodeId = null;
      detailsEl.innerHTML = "<p>Select a visible bubble to view details.</p>";
      for (const [, el] of nodeElements.entries()) {
        el.group.classList.remove("is-active");
      }
    }
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

  function drawTopic(topic, mode) {
    currentTopic = topic;
    currentMode = mode;
    activeFilter = "All";
    searchTerm = "";
    selectedNodeId = null;
    if (searchInput) searchInput.value = "";
    if (searchCountEl) searchCountEl.textContent = "";

    titleEl.textContent = topic.title || "StudyBubble Topic";
    subtitleEl.textContent = topic.subtitle || "";

    svg.innerHTML = "";
    nodeElements.clear();
    linkElements.length = 0;

    const nodes = Array.isArray(topic.nodes) ? topic.nodes : [];
    const links = Array.isArray(topic.links) ? topic.links : [];
    const nodeById = new Map(nodes.map((n) => [n.id, n]));

    const width = 1000;
    const y = 260;
    const margin = 100;
    const step = nodes.length > 1 ? (width - margin * 2) / (nodes.length - 1) : 0;

    const positioned = nodes.map((node, i) => ({
      ...node,
      x: margin + step * i,
      y,
      r: node.size === "detail" ? 40 : node.size === "support" ? 48 : 56,
    }));

    const positionById = new Map(positioned.map((n) => [n.id, n]));

    for (const link of links) {
      const source = positionById.get(link.source);
      const target = positionById.get(link.target);
      if (!source || !target) continue;

      const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      line.setAttribute("class", "link-line");
      line.setAttribute("x1", String(source.x));
      line.setAttribute("y1", String(source.y));
      line.setAttribute("x2", String(target.x));
      line.setAttribute("y2", String(target.y));
      svg.appendChild(line);
      linkElements.push({ el: line, sourceId: link.source, targetId: link.target });
    }

    for (const node of positioned) {
      const group = document.createElementNS("http://www.w3.org/2000/svg", "g");
      group.setAttribute("class", "bubble-node");
      group.setAttribute("tabindex", "0");

      const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      circle.setAttribute("class", "bubble-circle");
      circle.setAttribute("cx", String(node.x));
      circle.setAttribute("cy", String(node.y));
      circle.setAttribute("r", String(node.r));

      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("class", "bubble-label");
      text.setAttribute("x", String(node.x));
      text.setAttribute("y", String(node.y));
      text.textContent = node.label;

      group.appendChild(circle);
      group.appendChild(text);

      function activate() {
        setSelectedNode(node.id);
      }

      function navigateToSingleChildTopic() {
        const childTopics = Array.isArray(node.childTopics) ? node.childTopics : [];
        if (childTopics.length !== 1) return;
        const href = topicRefToHref(childTopics[0].topic, mode);
        if (!href || href === "#") return;
        window.location.href = href;
      }

      group.addEventListener("click", activate);
      group.addEventListener("dblclick", () => {
        activate();
        navigateToSingleChildTopic();
      });
      group.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          activate();
        }
      });

      const childTopics = Array.isArray(node.childTopics) ? node.childTopics : [];
      if (childTopics.length === 1) {
        const childLabel = childTopics[0].label || childTopics[0].topic || "child topic";
        group.setAttribute("title", `Double-click to open ${childLabel}`);
      }

      svg.appendChild(group);
      nodeElements.set(node.id, { group, node });
    }

    renderGroupFilters(topic);
    renderPaths(topic.paths || []);

    if (nodes.length > 0) {
      setSelectedNode(nodes[0].id);
    }

    applyVisibility();
  }

  async function loadTopic() {
    const embedded = document.getElementById("studybubble-topic-data");
    if (embedded) {
      return JSON.parse(embedded.textContent || "{}");
    }
    const response = await fetch("topic.studybubble.json");
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  }

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

      if (groupFiltersEl) {
        for (const b of groupFiltersEl.querySelectorAll(".filter-btn")) {
          b.classList.toggle("is-active", b.textContent === "All");
        }
      }
      for (const [, el] of nodeElements.entries()) {
        el.group.classList.remove("is-active");
      }

      detailsEl.innerHTML = "<p>Select a bubble to view details.</p>";
      applyVisibility();
    });
  }

  try {
    const topic = await loadTopic();
    const mode = document.getElementById("studybubble-topic-data") ? "single-file" : "multifile";
    drawTopic(topic, mode);
  } catch (error) {
    titleEl.textContent = "Failed to load topic";
    subtitleEl.textContent = String(error);
    detailsEl.innerHTML = `<p>Could not load <code>topic.studybubble.json</code>.</p>`;
  }
})();
