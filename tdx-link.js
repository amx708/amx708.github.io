/**
 * 伯克希尔数据中心 — 通达信个股联动
 * 用法：在 HTML 底部 <script src="tdx-link.js"></script>
 * 前提：先运行 tdx-bridge.py（监听 127.0.0.1:8765）
 */
(function () {
  const BRIDGE_URL = "http://127.0.0.1:8765/jump?code=";

  // 判断是否为 A 股 6 位代码（沪深北）
  function isAshare(code) {
    if (!/^\d{6}$/.test(code)) return false;
    const c0 = code[0];
    // 0=深主板/中小板  3=创业板  6=沪主板  68=科创板  69=沪B/沪cdr  8=北交所  9=沪B  5=沪基金/可转债
    return /[036859]/.test(c0);
  }

  // 提取文本中的 6 位代码
  function extractCode(text) {
    const m = String(text).match(/\b(\d{6})\b/);
    return m && isAshare(m[1]) ? m[1] : null;
  }

  // 把目标元素中的代码变成可点击链接
  function linkify(el) {
    if (!el || el.dataset?.tdxLinked) return;
    const code = extractCode(el.textContent);
    if (!code) return;

    // 如果元素里只有纯文本，直接包装
    const a = document.createElement("a");
    a.href = "#";
    a.className = "tdx-stock-link";
    a.dataset.code = code;
    a.title = `点击跳转通达信：${code}`;
    a.innerHTML = el.innerHTML; // 保留原有内容

    // 样式
    a.style.cssText = "color:#2563eb;text-decoration:none;border-bottom:1px dashed #93c5fd;cursor:pointer;transition:.15s;";

    el.innerHTML = "";
    el.appendChild(a);
    el.dataset.tdxLinked = "1";
  }

  // 页面加载后执行
  function init() {
    // 1) 详情页标题：h1 下的 span 里的 6 位代码
    document.querySelectorAll("h1 span").forEach(linkify);

    // 2) 任何 class 包含 code / stock-code 的元素
    document.querySelectorAll(".code, .stock-code, [data-stock-code]").forEach(linkify);

    // 3) 表格/卡片中的 td.code, .cc 等
    document.querySelectorAll(".cc, td.code, .stock-code-link").forEach(linkify);

    // 点击事件委托
    document.addEventListener("click", function (e) {
      const a = e.target.closest("a.tdx-stock-link");
      if (!a) return;
      e.preventDefault();
      const code = a.dataset.code;
      if (!code) return;

      // 发送请求给本地桥梁
      fetch(BRIDGE_URL + encodeURIComponent(code))
        .then((r) => r.json())
        .then((data) => {
          if (data.ok) {
            showTip(`已联动通达信：${code}`);
          } else {
            showTip(`联动失败：${data.error || "未知错误"}`, true);
          }
        })
        .catch(() => {
          showTip("未检测到 tdx-bridge.py，请先双击运行它并保持窗口打开", true);
        });
    });
  }

  // 右下角提示
  function showTip(msg, isErr) {
    let box = document.getElementById("tdx-tip");
    if (!box) {
      box = document.createElement("div");
      box.id = "tdx-tip";
      box.style.cssText =
        "position:fixed;right:18px;bottom:18px;z-index:9999;padding:10px 16px;border-radius:8px;font-size:13px;box-shadow:0 4px 14px rgba(0,0,0,.15);transition:opacity .3s;opacity:0;";
      document.body.appendChild(box);
    }
    box.style.background = isErr ? "#fee2e2" : "#dcfce7";
    box.style.color = isErr ? "#991b1b" : "#166534";
    box.style.border = isErr ? "1px solid #fecaca" : "1px solid #bbf7d0";
    box.textContent = msg;
    box.style.opacity = "1";
    clearTimeout(box._t);
    box._t = setTimeout(() => (box.style.opacity = "0"), 3000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
