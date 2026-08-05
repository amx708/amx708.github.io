/*
 * 伯克希尔数据中心 — 站点统计加载器
 * -------------------------------------------------------------
 * 全站每个 HTML 页面都在 </body> 前通过 <script src="/analytics.js">
 * 加载本文件。本文件只负责“决定是否加载统计 SDK”，不内联任何统计代码。
 *
 * 激活方式（拿到 ID 后只改这一处，重新部署本文件即全站生效）：
 *   1. 去 https://tongji.baidu.com 注册免费站点，拿到“站点ID”
 *      （即 hm.js? 后面那串，形如 1234abcd5678ef90 ）
 *   2. 把下面 BAIDU_SITE_ID 的空字符串改成你的站点 ID
 *   3. 部署本文件，全站 3134 个页面立即开始计数
 *
 * 未配置 ID 时本文件直接 return，零网络请求、零副作用（占位未激活态）。
 * -------------------------------------------------------------
 */
(function () {
  // ↓↓↓ 拿到百度统计站点 ID 后填到这里 ↓↓↓
  var BAIDU_SITE_ID = "";

  // 未激活：保持静默，不加载任何第三方脚本
  if (!BAIDU_SITE_ID) {
    return;
  }

  // 百度统计 hm.js 标准接入（与官方自动生成的代码一致）
  var _hmt = (window._hmt = window._hmt || []);
  (function () {
    var hm = document.createElement("script");
    hm.src = "https://hm.baidu.com/hm.js?" + BAIDU_SITE_ID;
    hm.async = true;
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(hm, s);
  })();
})();
