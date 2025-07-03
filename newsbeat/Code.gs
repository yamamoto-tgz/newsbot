function beat() {
  const channels = [
    ["atmarkit", "https://rss.itmedia.co.jp/rss/2.0/ait.xml"],
    ["codezine", "https://codezine.jp/rss/new/20/index.xml"],
    ["gizmodo", "https://www.gizmodo.jp/index.xml"],
    ["itmedia", "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml"],
    ["zenn", "https://zenn.dev/feed"],
    ["lifehacker", "https://www.lifehacker.jp/feed/"],
    ["gigazine", "https://gigazine.net/news/rss_2.0/"],
    ["hatena", "https://b.hatena.ne.jp/hotentry/it.rss"],
    ["dznet", "http://feed.japan.zdnet.com/rss/index.rdf"],
    ["forest", "https://forest.watch.impress.co.jp/data/rss/1.0/wf/feed.rdf"],
    ["gbusiness", "https://www.gamebusiness.jp/rss20/index.rdf"],
    ["gihyo", "https://gihyo.jp/feed/rss2"],
    ["nhk", "https://www.nhk.or.jp/rss/news/cat0.xml"],
  ];

  channels.forEach((channel) => {
    const baseUrl = PropertiesService.getScriptProperties().getProperty("NB_API_BASE_URL");
    send(channel[1], `${baseUrl}/xml/${channel[0]}`);
  });
}

function send(src, dst) {
  const xml = UrlFetchApp.fetch(src).getContentText();

  UrlFetchApp.fetch(dst, {
    method: "post",
    contentType: "application/xml",
    payload: xml,
  });
}
