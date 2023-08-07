// node_modules/@socialplayer/core/dist/chunk-ITKLQDRO.mjs
var i = ({ id: s }) => {
  let e = (n) => {
    for (let t in n) {
      let o = n[t], l2 = (u) => {
        o({ ...u, id: s });
      };
      n[t] = l2;
    }
  }, c = { playbackActions: {}, use: (n, t) => {
    let o = n.install({}, t);
    return e(o), Object.assign(c.playbackActions, o), o;
  } };
  for (let n of i.$pluginsQueue) {
    let t = n();
    e(t), Object.assign(c.playbackActions, t);
  }
  return c;
};
i.$pluginsQueue = [];
i.use = (s, e) => {
  i.$pluginsQueue.push(() => s.install({}, e));
};

// node_modules/@socialplayer/vue/dist/chunk-UBUGDGNK.mjs
var l = (a) => {
  let { playbackActions: c } = i(a);
  return { playbackActions: c };
};
l.use = i.use;
export {
  l as useSocialPlayer
};
//# sourceMappingURL=@socialplayer_vue.js.map
