// node_modules/@socialplayer/vimeo-plugin/dist/chunk-IUG6XWSG.mjs
var l = () => {
  let a = /* @__PURE__ */ new Set();
  async function n(o) {
    return a.has(o) ? Promise.resolve() : new Promise(function(r, i) {
      let e = document.createElement("script");
      e.src = o, e.onload = function() {
        a.add(o), r();
      }, e.onerror = function() {
        i(new Error(`Failed to load script: ${o}`));
      }, document.head.appendChild(e);
    });
  }
  return n;
};
var t = l();
var h = { install() {
  return { loadVimeoUrl: async ({ id: n, source: o }) => {
    let r = document.getElementById(n);
    await t("https://player.vimeo.com/api/player.js"), new window.Vimeo.Player(r, { url: o, playsinline: true }).ready().then(() => {
      let e = r.querySelector("iframe");
      e.style.width = "100%", e.style.height = "100%";
    });
  } };
} };
export {
  h as vimeoPlugin
};
//# sourceMappingURL=@socialplayer_vimeo-plugin.js.map
