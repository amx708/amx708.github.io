/*
 * tdx-link.js — 伯克希尔数据中心本地软件专属工具条
 * ---------------------------------------------------------------
 * 仅在本地 127.0.0.1 / localhost 生效；公网 github.io 自动静默（不渲染、不发请求）。
 * 功能：
 *   1) 在任意公司详情页（URL 含 -co-XXXXXX）右下角显示「通达信联动」按钮，
 *      点击经本地启动器的 /api/open_tdx/<code> 联动通达信切入该股 K 线。
 *   2) 扫描页面所有指向公司详情页（href 含 -co-XXXXXX）的链接，在其后
 *      注入一个小「📈」快捷联动入口；点它直接联动通达信，不影响原链接
 *      跳公司详情页。适用于银行/白酒/AI 等所有产业链列表页与工具页。
 *
 * 历史说明：曾内置「龙头复盘神器」悬浮入口（依赖本地 8765 服务），已于
 * 2026-08-09 随后端下线一并移除。
 */
(function () {
  "use strict";
  var host = location.hostname;
  if (host !== "127.0.0.1" && host !== "localhost") return; // 公网静默

  function getCode() {
    var m = location.pathname.match(/co-(\d{6})/);
    return m ? m[1] : null;
  }

  function toast(msg, isErr) {
    var t = document.getElementById("tdx-toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "tdx-toast";
      t.style.cssText =
        "position:fixed;left:50%;top:18px;transform:translateX(-50%);z-index:99999;" +
        "background:rgba(20,24,33,.94);color:#fff;padding:10px 16px;border-radius:8px;" +
        "font:14px/1.5 system-ui,'Microsoft YaHei',sans-serif;max-width:80vw;" +
        "box-shadow:0 4px 18px rgba(0,0,0,.3);transition:opacity .3s;pointer-events:none;";
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.style.opacity = "1";
    t.style.color = isErr ? "#ff8a8a" : "#fff";
    clearTimeout(t._t);
    t._t = setTimeout(function () { t.style.opacity = "0"; }, 2800);
  }

  function openTdx(code) {
    fetch("/api/open_tdx/" + code)
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (d.ok) {
          toast("已联动通达信：" + code);
        } else {
          toast("联动失败：" + (d.msg || "请确认本地服务已启动"), true);
        }
      })
      .catch(function (e) { toast("联动失败：" + e, true); });
  }

  function styleBtn(b, color) {
    b.style.cssText =
      "cursor:pointer;border:none;border-radius:20px;padding:9px 15px;color:#fff;" +
      "background:" + color + ";box-shadow:0 3px 12px rgba(0,0,0,.28);" +
      "font:13px/1.2 system-ui,'Microsoft YaHei',sans-serif;white-space:nowrap;";
  }

  // 公司名 → 股票代码 映射（来自 _extract_company_codes.py 扫描所有链索引页）
  // 用于给没有 -co-XXXXXX URL 但文本是公司名的链接（如链索引页表格行）注入联动入口
  var companyCodes = null;

  function loadCompanyCodes(cb) {
    if (companyCodes) { cb(companyCodes); return; }
    fetch("/static/company-codes.json")
      .then(function (r) { return r.ok ? r.json() : {}; })
      .then(function (d) { companyCodes = d || {}; cb(companyCodes); })
      .catch(function () { companyCodes = {}; cb(companyCodes); });
  }

  // 在所有指向公司详情页的 <a> 后插入一个小「📈」快捷联动入口
  // 两条匹配路径：
  //   A) href 含 -co-XXXXXX（如 berkshire-commodity-co-000060.html）
  //   B) 链接文本命中 company-codes.json 的公司名（链索引页表格行等）
  function injectCoLinkButtons() {
    var links = document.querySelectorAll("a");
    var pending = [];
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      if (a.dataset.tdxInjected) continue;
      var href = a.getAttribute("href") || "";
      var m = href.match(/co-(\d{6})/);
      if (m) {
        injectBtn(a, m[1]);
        continue;
      }
      // 文本可能是 "招商银行" 这种短中文名，留给异步 mapping 处理
      var txt = (a.textContent || "").trim();
      if (txt && txt.length <= 12 && !/[\s\|]/.test(txt)) {
        pending.push(a);
      }
    }
    if (!pending.length) return;
    loadCompanyCodes(function (map) {
      // 预按 key 长度降序，便于「最长前缀匹配」优先（如卡片正文「贵州茅台 链中国…」也能命中）
      var keys = Object.keys(map).sort(function (a, b) { return b.length - a.length; });
      for (var j = 0; j < pending.length; j++) {
        var el = pending[j];
        if (el.dataset.tdxInjected) continue;
        var name = (el.textContent || "").trim();
        var code = map[name];
        if (!code) {
          // 前缀匹配：文本以某公司名开头（卡片/长链接场景）
          for (var ki = 0; ki < keys.length; ki++) {
            if (name.indexOf(keys[ki]) === 0) { code = map[keys[ki]]; break; }
          }
        }
        if (code) injectBtn(el, code);
      }
    });
  }

  function injectBtn(a, code) {
    a.dataset.tdxInjected = "1";
    var btn = document.createElement("span");
    btn.textContent = "📈";
    btn.title = "联动通达信：" + code;
    btn.style.cssText =
      "display:inline-block;margin-left:4px;cursor:pointer;" +
      "font-size:0.9em;opacity:0.55;transition:opacity .2s,transform .2s;" +
      "user-select:none;vertical-align:middle;line-height:1;";
    btn.onmouseover = function () {
      this.style.opacity = "1";
      this.style.transform = "scale(1.25)";
    };
    btn.onmouseout = function () {
      this.style.opacity = "0.55";
      this.style.transform = "scale(1)";
    };
    // IIFE 捕获 code，避免闭包共享导致全部按钮都用最后一次的 code
    btn.onclick = (function (c) {
      return function (e) {
        e.preventDefault();
        e.stopPropagation();
        openTdx(c);
      };
    })(code);
    a.parentNode.insertBefore(btn, a.nextSibling);
  }

  function build() {
    if (document.getElementById("tdx-link-bar")) return;
    var bar = document.createElement("div");
    bar.id = "tdx-link-bar";
    bar.style.cssText =
      "position:fixed;right:14px;bottom:14px;z-index:99998;display:flex;" +
      "flex-direction:column;gap:8px;align-items:flex-end;" +
      "font:13px system-ui,'Microsoft YaHei',sans-serif;";

    var code = getCode();
    if (code) {
      var b1 = document.createElement("button");
      b1.textContent = "📈 通达信联动 " + code;
      styleBtn(b1, "#2f7d4f");
      b1.onclick = function () { openTdx(code); };
      bar.appendChild(b1);
    }

    document.body.appendChild(bar);

    // 列表页/工具页：所有指向公司详情页的链接旁注入 📈 联动入口
    injectCoLinkButtons();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build);
  else build();
})();
