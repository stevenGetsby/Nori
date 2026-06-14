var NoriApp = (() => {
  // desktop_all.jsx
  var T = {
    // Brand
    primary: "#D6FF00",
    // Fuschia
    primaryHov: "#b8e000",
    primaryTint: "#f5ffe0",
    iris: "#4B4DED",
    irisHov: "#3537c7",
    irisTint: "#EFEFFD",
    peach: "#F3DBDA",
    peachTint: "#fdf5f5",
    // Onyx scale
    navy: "#0e0e2c",
    navyMid: "#4a4a68",
    navyLight: "#8c8ca1",
    navySoft: "#c4c4d4",
    // Surfaces
    surface: "#ECF1F4",
    // Dorian
    surfaceWh: "#fafcfe",
    // Cloud
    white: "#ffffff",
    hairline: "rgba(14,14,44,.08)",
    hairlineSoft: "rgba(14,14,44,.05)",
    // Semantic
    success: "#31D0AA",
    successTint: "#e0faf4",
    warn: "#fb8c00",
    error: "#e53935",
    // Shadows
    shadowXs: "0 1px 2px rgba(14,14,44,.035), 0 1px 5px rgba(14,14,44,.025)",
    shadowSm: "0 5px 14px rgba(14,14,44,.055), 0 1px 2px rgba(14,14,44,.035)",
    shadowMd: "0 12px 28px rgba(14,14,44,.075), 0 2px 5px rgba(14,14,44,.045)",
    shadowLg: "0 22px 54px rgba(14,14,44,.095), 0 4px 12px rgba(14,14,44,.055)",
    shadowXl: "0 34px 80px rgba(14,14,44,.13), 0 8px 22px rgba(14,14,44,.07)",
    shadowBtn: "0 7px 18px rgba(14,14,44,.08), 0 1px 2px rgba(14,14,44,.04), inset 0 -1px 0 rgba(14,14,44,.10)",
    // Type
    fontSans: "'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', sans-serif",
    fontSerif: "'Fraunces', Georgia, serif",
    fontMono: "'DM Mono', 'Monaco', monospace",
    // Motion
    spring: "cubic-bezier(.22, 1, .36, 1)",
    ease: "cubic-bezier(.25, .1, .25, 1)",
    softSurface: "rgba(255,255,255,.78)"
  };
  window.T = T;
  var NORI_LOGO_SRC = "./src/nori-onion-logo.png";
  window.NORI_LOGO_SRC = NORI_LOGO_SRC;
  var ONION_BURST_ASSETS = [
    "./src/onion-burst-collage.png",
    "./src/onion-burst-star.png",
    "./src/onion-burst-real.png",
    "./src/onion-burst-ring.png",
    "./src/onion-burst-ink.png"
  ];
  var Icon = ({ name, size = 18, color = "currentColor", stroke = 1.6, style }) => {
    const props = {
      width: size,
      height: size,
      viewBox: "0 0 24 24",
      fill: "none",
      stroke: color,
      strokeWidth: stroke,
      strokeLinecap: "round",
      strokeLinejoin: "round",
      style
    };
    const paths = {
      attach: /* @__PURE__ */ React.createElement("path", { d: "M21 12.5l-8.5 8.5a5.5 5.5 0 0 1-7.8-7.8l9-9a3.7 3.7 0 0 1 5.2 5.2l-8.5 8.5a1.8 1.8 0 0 1-2.6-2.6L15.5 8" }),
      globe: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "9" }), /* @__PURE__ */ React.createElement("path", { d: "M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18" })),
      send: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M22 2L11 13" }), /* @__PURE__ */ React.createElement("path", { d: "M22 2l-7 20-4-9-9-4 20-7Z" })),
      arrowRight: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M5 12h14" }), /* @__PURE__ */ React.createElement("path", { d: "M13 5l7 7-7 7" })),
      arrowUp: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 19V5" }), /* @__PURE__ */ React.createElement("path", { d: "M5 12l7-7 7 7" })),
      arrowLeft: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M19 12H5" }), /* @__PURE__ */ React.createElement("path", { d: "M11 19l-7-7 7-7" })),
      chevronDown: /* @__PURE__ */ React.createElement("path", { d: "M6 9l6 6 6-6" }),
      chevronLeft: /* @__PURE__ */ React.createElement("path", { d: "M15 6l-6 6 6 6" }),
      chevronRight: /* @__PURE__ */ React.createElement("path", { d: "M9 6l6 6-6 6" }),
      plus: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 5v14" }), /* @__PURE__ */ React.createElement("path", { d: "M5 12h14" })),
      close: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M18 6L6 18" }), /* @__PURE__ */ React.createElement("path", { d: "M6 6l12 12" })),
      check: /* @__PURE__ */ React.createElement("path", { d: "M5 12.5l5 5 9-12" }),
      sparkle: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8" })),
      star: /* @__PURE__ */ React.createElement("path", { d: "M12 3l2.8 6.2 6.7.6-5.1 4.5 1.6 6.7L12 17.5 5.9 21l1.6-6.7L2.4 9.8l6.7-.6L12 3z" }),
      heart: /* @__PURE__ */ React.createElement("path", { d: "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z" }),
      bookmark: /* @__PURE__ */ React.createElement("path", { d: "M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z" }),
      eye: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "3" })),
      edit: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" }), /* @__PURE__ */ React.createElement("path", { d: "M18.5 2.5a2.1 2.1 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" })),
      image: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "3", width: "18", height: "18", rx: "2" }), /* @__PURE__ */ React.createElement("circle", { cx: "8.5", cy: "8.5", r: "1.5" }), /* @__PURE__ */ React.createElement("path", { d: "M21 15l-5-5L5 21" })),
      calendar: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "4", width: "18", height: "18", rx: "3" }), /* @__PURE__ */ React.createElement("path", { d: "M16 2v4M8 2v4M3 10h18" })),
      file: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" }), /* @__PURE__ */ React.createElement("path", { d: "M14 2v6h6" })),
      save: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M17 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14V7z" }), /* @__PURE__ */ React.createElement("path", { d: "M7 3v6h8" }), /* @__PURE__ */ React.createElement("path", { d: "M9 21v-6h6" })),
      copy: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "9", y: "9", width: "11", height: "11", rx: "2" }), /* @__PURE__ */ React.createElement("path", { d: "M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" })),
      lock: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "5", y: "10", width: "14", height: "11", rx: "2" }), /* @__PURE__ */ React.createElement("path", { d: "M8 10V7a4 4 0 0 1 8 0v3" })),
      search: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "11", cy: "11", r: "7" }), /* @__PURE__ */ React.createElement("path", { d: "M21 21l-4.3-4.3" })),
      chat: /* @__PURE__ */ React.createElement("path", { d: "M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" }),
      library: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z" }), /* @__PURE__ */ React.createElement("path", { d: "M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z" })),
      home: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 9.5l9-7 9 7V20a2 2 0 0 1-2 2h-4v-7H9v7H5a2 2 0 0 1-2-2z" })),
      splitView: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "5", width: "18", height: "14", rx: "4" }), /* @__PURE__ */ React.createElement("path", { d: "M11.5 5v14" })),
      grid: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "3", width: "7", height: "7" }), /* @__PURE__ */ React.createElement("rect", { x: "14", y: "3", width: "7", height: "7" }), /* @__PURE__ */ React.createElement("rect", { x: "3", y: "14", width: "7", height: "7" }), /* @__PURE__ */ React.createElement("rect", { x: "14", y: "14", width: "7", height: "7" })),
      expand: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M15 3h6v6" }), /* @__PURE__ */ React.createElement("path", { d: "M9 21H3v-6" }), /* @__PURE__ */ React.createElement("path", { d: "M21 3l-7 7" }), /* @__PURE__ */ React.createElement("path", { d: "M3 21l7-7" })),
      collapse: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M4 14h6v6" }), /* @__PURE__ */ React.createElement("path", { d: "M20 10h-6V4" }), /* @__PURE__ */ React.createElement("path", { d: "M14 10l7-7" }), /* @__PURE__ */ React.createElement("path", { d: "M3 21l7-7" })),
      download: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" }), /* @__PURE__ */ React.createElement("path", { d: "M7 10l5 5 5-5" }), /* @__PURE__ */ React.createElement("path", { d: "M12 15V3" })),
      upload: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" }), /* @__PURE__ */ React.createElement("path", { d: "M17 8l-5-5-5 5" }), /* @__PURE__ */ React.createElement("path", { d: "M12 3v12" })),
      sync: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M21 12a9 9 0 0 1-15 6.7L3 16" }), /* @__PURE__ */ React.createElement("path", { d: "M3 12a9 9 0 0 1 15-6.7L21 8" }), /* @__PURE__ */ React.createElement("path", { d: "M21 3v5h-5" }), /* @__PURE__ */ React.createElement("path", { d: "M3 21v-5h5" })),
      transform: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M16 3l4 4-4 4" }), /* @__PURE__ */ React.createElement("path", { d: "M20 7H4" }), /* @__PURE__ */ React.createElement("path", { d: "M8 21l-4-4 4-4" }), /* @__PURE__ */ React.createElement("path", { d: "M4 17h16" })),
      phone: /* @__PURE__ */ React.createElement("rect", { x: "6", y: "2", width: "12", height: "20", rx: "2" }),
      pen: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 19l7-7 3 3-7 7-3-3z" }), /* @__PURE__ */ React.createElement("path", { d: "M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z" }), /* @__PURE__ */ React.createElement("path", { d: "M2 2l7.6 7.6" }), /* @__PURE__ */ React.createElement("circle", { cx: "11", cy: "11", r: "2" })),
      sliders: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("line", { x1: "4", y1: "21", x2: "4", y2: "14" }), /* @__PURE__ */ React.createElement("line", { x1: "4", y1: "10", x2: "4", y2: "3" }), /* @__PURE__ */ React.createElement("line", { x1: "12", y1: "21", x2: "12", y2: "12" }), /* @__PURE__ */ React.createElement("line", { x1: "12", y1: "8", x2: "12", y2: "3" }), /* @__PURE__ */ React.createElement("line", { x1: "20", y1: "21", x2: "20", y2: "16" }), /* @__PURE__ */ React.createElement("line", { x1: "20", y1: "12", x2: "20", y2: "3" }), /* @__PURE__ */ React.createElement("line", { x1: "1", y1: "14", x2: "7", y2: "14" }), /* @__PURE__ */ React.createElement("line", { x1: "9", y1: "8", x2: "15", y2: "8" }), /* @__PURE__ */ React.createElement("line", { x1: "17", y1: "16", x2: "23", y2: "16" })),
      user: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "8", r: "4" }), /* @__PURE__ */ React.createElement("path", { d: "M4 21a8 8 0 0 1 16 0" })),
      play: /* @__PURE__ */ React.createElement("path", { d: "M5 3l14 9-14 9V3z" }),
      paperPlane: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M22 2L11 13" }), /* @__PURE__ */ React.createElement("path", { d: "M22 2l-7 20-4-9-9-4 20-7Z" })),
      document: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "4", y: "3", width: "16", height: "18", rx: "2" }), /* @__PURE__ */ React.createElement("path", { d: "M8 8h8M8 12h8M8 16h5" })),
      video: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "2", y: "6", width: "14", height: "12", rx: "2" }), /* @__PURE__ */ React.createElement("path", { d: "M22 8l-6 4 6 4z" })),
      bilibili: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "6", width: "18", height: "14", rx: "3" }), /* @__PURE__ */ React.createElement("circle", { cx: "9", cy: "13", r: ".8", fill: "currentColor" }), /* @__PURE__ */ React.createElement("circle", { cx: "15", cy: "13", r: ".8", fill: "currentColor" }), /* @__PURE__ */ React.createElement("path", { d: "M8 4l3 2M16 4l-3 2" })),
      minus: /* @__PURE__ */ React.createElement("path", { d: "M5 12h14" }),
      sparkles: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 3l1.8 4.2L18 9l-4.2 1.8L12 15l-1.8-4.2L6 9l4.2-1.8z" }), /* @__PURE__ */ React.createElement("path", { d: "M19 14l.9 2.1L22 17l-2.1.9L19 20l-.9-2.1L16 17l2.1-.9z" })),
      quote: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 14h6v7H3z" }), /* @__PURE__ */ React.createElement("path", { d: "M14 14h6v7h-6z" }), /* @__PURE__ */ React.createElement("path", { d: "M3 14V9a4 4 0 0 1 4-4" }), /* @__PURE__ */ React.createElement("path", { d: "M14 14V9a4 4 0 0 1 4-4" })),
      book: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M4 4h7a3 3 0 0 1 3 3v14a2 2 0 0 0-2-2H4z" }), /* @__PURE__ */ React.createElement("path", { d: "M20 4h-7a3 3 0 0 0-3 3v14a2 2 0 0 1 2-2h8z" })),
      paperclip: /* @__PURE__ */ React.createElement("path", { d: "M21 12.5l-8.5 8.5a5.5 5.5 0 0 1-7.8-7.8l9-9a3.7 3.7 0 0 1 5.2 5.2l-8.5 8.5a1.8 1.8 0 0 1-2.6-2.6L15.5 8" }),
      settings: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "3" }), /* @__PURE__ */ React.createElement("path", { d: "M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" })),
      bell: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9" }), /* @__PURE__ */ React.createElement("path", { d: "M13.7 21a2 2 0 0 1-3.4 0" })),
      refresh: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 12a9 9 0 0 1 15-6.7L21 8M21 3v5h-5" })),
      skip: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M5 4l10 8-10 8z" }), /* @__PURE__ */ React.createElement("line", { x1: "19", y1: "5", x2: "19", y2: "19" })),
      palette: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "9" }), /* @__PURE__ */ React.createElement("circle", { cx: "7", cy: "10", r: "1.3", fill: "currentColor" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "7", r: "1.3", fill: "currentColor" }), /* @__PURE__ */ React.createElement("circle", { cx: "17", cy: "10", r: "1.3", fill: "currentColor" }), /* @__PURE__ */ React.createElement("circle", { cx: "16", cy: "15", r: "1.3", fill: "currentColor" }), /* @__PURE__ */ React.createElement("path", { d: "M12 21a3 3 0 0 1-3-3 2 2 0 0 1 2-2h2a2 2 0 0 0 2-2" })),
      target: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "9" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "5" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "1.5", fill: "currentColor" })),
      lightbulb: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M9 18h6" }), /* @__PURE__ */ React.createElement("path", { d: "M10 22h4" }), /* @__PURE__ */ React.createElement("path", { d: "M15.5 14a5 5 0 1 0-7 0c.6.6 1 1.4 1 2.3V18h5v-1.7c0-.9.4-1.7 1-2.3z" })),
      moon: /* @__PURE__ */ React.createElement("path", { d: "M21 14.4A7.8 7.8 0 0 1 9.6 3 8.8 8.8 0 1 0 21 14.4z" }),
      chart: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 3v18h18" }), /* @__PURE__ */ React.createElement("path", { d: "M7 14l3-3 4 4 5-6" })),
      trending: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M22 7l-9 9-5-5-7 7" }), /* @__PURE__ */ React.createElement("path", { d: "M16 7h6v6" })),
      layers: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M12 2L2 7l10 5 10-5-10-5z" }), /* @__PURE__ */ React.createElement("path", { d: "M2 17l10 5 10-5" }), /* @__PURE__ */ React.createElement("path", { d: "M2 12l10 5 10-5" })),
      list: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("line", { x1: "8", y1: "6", x2: "21", y2: "6" }), /* @__PURE__ */ React.createElement("line", { x1: "8", y1: "12", x2: "21", y2: "12" }), /* @__PURE__ */ React.createElement("line", { x1: "8", y1: "18", x2: "21", y2: "18" }), /* @__PURE__ */ React.createElement("line", { x1: "3", y1: "6", x2: "3.01", y2: "6" }), /* @__PURE__ */ React.createElement("line", { x1: "3", y1: "12", x2: "3.01", y2: "12" }), /* @__PURE__ */ React.createElement("line", { x1: "3", y1: "18", x2: "3.01", y2: "18" })),
      moreH: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "5", cy: "12", r: "1.2", fill: "currentColor" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "1.2", fill: "currentColor" }), /* @__PURE__ */ React.createElement("circle", { cx: "19", cy: "12", r: "1.2", fill: "currentColor" })),
      moreV: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "5", r: "1.2", fill: "currentColor" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "12", r: "1.2", fill: "currentColor" }), /* @__PURE__ */ React.createElement("circle", { cx: "12", cy: "19", r: "1.2", fill: "currentColor" })),
      link: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1" }), /* @__PURE__ */ React.createElement("path", { d: "M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1" })),
      folder: /* @__PURE__ */ React.createElement("path", { d: "M3 7a2 2 0 0 1 2-2h4l2 3h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" }),
      flag: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M4 22V4" }), /* @__PURE__ */ React.createElement("path", { d: "M4 4h13l-2 4 2 4H4" })),
      headphone: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("path", { d: "M3 18v-6a9 9 0 0 1 18 0v6" }), /* @__PURE__ */ React.createElement("path", { d: "M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3z" }), /* @__PURE__ */ React.createElement("path", { d: "M3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z" })),
      /* brand glyphs */
      xhs: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("rect", { x: "3", y: "3", width: "18", height: "18", rx: "4" })),
      nori: null
      // logo handled separately
    };
    return /* @__PURE__ */ React.createElement("svg", { ...props }, paths[name]);
  };
  var NoriLogo = ({ size = 28, dark = true, framed = true }) => {
    return /* @__PURE__ */ React.createElement("div", { style: {
      width: size,
      height: size,
      borderRadius: framed ? size * 0.34 : 0,
      background: framed ? dark ? "rgba(255,255,255,.82)" : "rgba(14,14,44,.9)" : "transparent",
      border: framed ? "1px solid rgba(14,14,44,.055)" : "none",
      boxShadow: framed ? "0 10px 24px rgba(14,14,44,.06), inset 0 1px 0 rgba(255,255,255,.86)" : "none",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0,
      overflow: "hidden"
    } }, /* @__PURE__ */ React.createElement(
      "img",
      {
        src: NORI_LOGO_SRC,
        alt: "Nori",
        style: {
          width: framed ? "72%" : "100%",
          height: framed ? "72%" : "100%",
          objectFit: "contain",
          display: "block",
          filter: dark ? "none" : "invert(1)"
        }
      }
    ));
  };
  window.Icon = Icon;
  window.NoriLogo = NoriLogo;
  var useViewport = () => {
    const [width, setWidth] = React.useState(() => window.innerWidth);
    React.useEffect(() => {
      const onResize = () => setWidth(window.innerWidth);
      window.addEventListener("resize", onResize);
      return () => window.removeEventListener("resize", onResize);
    }, []);
    return {
      width,
      isCompact: width < 1180,
      isTablet: width < 980,
      isMobile: width < 760
    };
  };
  var PlatformLogo = ({ kind, size = 20 }) => {
    const base = {
      width: size,
      height: size,
      borderRadius: size * 0.32,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      overflow: "hidden",
      flexShrink: 0
    };
    if (kind === "xhs") {
      return /* @__PURE__ */ React.createElement("span", { style: {
        ...base,
        background: "#ff2442",
        color: "#fff",
        fontSize: size * 0.36,
        fontWeight: 800,
        letterSpacing: 0,
        boxShadow: "inset 0 1px 0 rgba(255,255,255,.24)"
      } }, "RED");
    }
    if (kind === "dy") {
      return /* @__PURE__ */ React.createElement("span", { style: { ...base, background: "#111", padding: 0 } }, /* @__PURE__ */ React.createElement(
        "img",
        {
          src: "/static/vendor/douyin-icon.png",
          alt: "Douyin",
          style: { width: "100%", height: "100%", objectFit: "cover" }
        }
      ));
    }
    if (kind === "bili") {
      return /* @__PURE__ */ React.createElement("span", { style: {
        ...base,
        background: "#ffffff",
        color: "#fb7299",
        border: "1px solid rgba(251,114,153,.18)",
        boxShadow: "0 2px 8px rgba(251,114,153,.12)"
      } }, /* @__PURE__ */ React.createElement(Icon, { name: "bilibili", size: size * 0.76, color: "currentColor" }));
    }
    return /* @__PURE__ */ React.createElement("span", { style: { ...base, background: T.success, color: "#fff", fontSize: size * 0.52, fontWeight: 800 } }, "\u5FAE");
  };
  var GLOBAL_RECENT_SESSIONS = [
    "\u4E0A\u6D77\u996D\u5E97\u63A8\u8350 \xB7 \u5F53\u524D",
    "\u4E0B\u73ED\u540E\u5C0F\u9986\u5730\u56FE",
    "\u4EBA\u5747 80 \u7EA6\u996D\u6E05\u5355",
    "\u4EA7\u54C1\u6D4B\u8BC4 \xB7 AI \u89C6\u9891\u5DE5\u5177\u6A2A\u8BC4",
    "\u6781\u7B80\u901A\u52E4\u7A7F\u642D\u4E00\u5468 OOTD",
    "\u5496\u5561\u5165\u95E8 12 \u4E2A\u540D\u8BCD",
    "\u6211\u548C\u6211\u7684\u732B \xB7 7 \u4E2A\u77AC\u95F4"
  ];
  var Sidebar = ({ active, onNew, onNavigate = () => {
  }, sessions = [], collapsed = false, onToggle = () => {
  } }) => {
    return /* @__PURE__ */ React.createElement("aside", { style: {
      width: collapsed ? 66 : 220,
      flexShrink: 0,
      background: "linear-gradient(180deg, rgba(250,252,254,.98), rgba(247,249,252,.96))",
      display: "flex",
      flexDirection: "column",
      padding: collapsed ? "12px 9px" : "16px 12px",
      height: "100%",
      borderRight: "1px solid rgba(14,14,44,.075)",
      boxShadow: "8px 0 28px rgba(14,14,44,.018)",
      backdropFilter: "blur(20px) saturate(1.12)",
      transition: `width .42s ${T.spring}, padding .42s ${T.spring}`
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 9, justifyContent: collapsed ? "center" : "flex-start", padding: collapsed ? "3px 2px 22px" : "3px 10px 22px" } }, !collapsed && /* @__PURE__ */ React.createElement(NoriLogo, { size: 22, framed: false }), !collapsed && /* @__PURE__ */ React.createElement("span", { style: { fontSize: 16, fontWeight: 720, letterSpacing: 0, color: T.navy } }, "Nori"), /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: onToggle,
        "aria-label": collapsed ? "\u5C55\u5F00\u5BFC\u822A\u680F" : "\u6536\u8D77\u5BFC\u822A\u680F",
        style: {
          marginLeft: collapsed ? 0 : "auto",
          width: 30,
          height: 30,
          borderRadius: 11,
          border: `1px solid ${T.hairlineSoft}`,
          background: "rgba(255,255,255,.70)",
          color: T.navyLight,
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          boxShadow: collapsed ? T.shadowSm : "inset 0 1px 0 rgba(255,255,255,.78)",
          transition: `transform .28s ${T.spring}, box-shadow .28s ${T.spring}, background .28s ${T.ease}`
        },
        onMouseEnter: (e) => {
          e.currentTarget.style.transform = "translateY(-1px)";
          e.currentTarget.style.boxShadow = T.shadowSm;
        },
        onMouseLeave: (e) => {
          e.currentTarget.style.transform = "translateY(0)";
          e.currentTarget.style.boxShadow = collapsed ? T.shadowSm : "inset 0 1px 0 rgba(255,255,255,.72)";
        }
      },
      /* @__PURE__ */ React.createElement(Icon, { name: "splitView", size: 16, color: "currentColor" })
    )), /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: () => onNew && onNew(),
        style: {
          height: collapsed ? 38 : 40,
          borderRadius: collapsed ? 13 : 11,
          border: "none",
          background: `linear-gradient(135deg, ${T.iris}, #686AF4)`,
          color: T.white,
          display: "flex",
          alignItems: "center",
          justifyContent: collapsed ? "center" : "space-between",
          padding: collapsed ? 0 : "0 14px",
          fontSize: 13,
          fontWeight: 650,
          cursor: "pointer",
          marginBottom: 14,
          boxShadow: "0 14px 28px rgba(75,77,237,.18), inset 0 1px 0 rgba(255,255,255,.18)",
          transition: `transform .28s ${T.spring}, background .24s ${T.ease}, box-shadow .28s ${T.spring}`
        },
        onMouseEnter: (e) => {
          e.currentTarget.style.transform = "translateY(-1px)";
          e.currentTarget.style.boxShadow = "0 18px 34px rgba(75,77,237,.24), inset 0 1px 0 rgba(255,255,255,.22)";
        },
        onMouseLeave: (e) => {
          e.currentTarget.style.transform = "translateY(0)";
          e.currentTarget.style.boxShadow = "0 14px 28px rgba(75,77,237,.18), inset 0 1px 0 rgba(255,255,255,.18)";
        }
      },
      /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement(Icon, { name: "plus", size: collapsed ? 15 : 16, color: "currentColor" }), !collapsed && /* @__PURE__ */ React.createElement("span", null, "\u65B0\u5EFA\u5185\u5BB9"))
    ), /* @__PURE__ */ React.createElement("nav", { style: { display: "flex", flexDirection: "column", gap: 5 } }, [
      { id: "home", label: "\u521B\u4F5C", icon: "home" },
      { id: "library", label: "\u8D44\u4EA7", icon: "library" },
      { id: "insights", label: "\u6D1E\u5BDF", icon: "chart" },
      { id: "mine", label: "\u6211\u7684", icon: "user" }
    ].map((item) => /* @__PURE__ */ React.createElement(
      "a",
      {
        key: item.id,
        href: "#",
        onClick: (e) => {
          e.preventDefault();
          onNavigate(item.id);
          if (item.id !== "home" && !collapsed) onToggle();
        },
        style: {
          display: "flex",
          alignItems: "center",
          gap: collapsed ? 0 : 9,
          justifyContent: collapsed ? "center" : "flex-start",
          padding: collapsed ? "0" : "0 12px",
          height: collapsed ? 38 : 40,
          borderRadius: collapsed ? 13 : 10,
          fontSize: 13,
          fontWeight: active === item.id ? 680 : 560,
          color: active === item.id ? T.iris : T.navyMid,
          background: active === item.id ? "rgba(75,77,237,.105)" : "transparent",
          textDecoration: "none",
          transition: `background .24s ${T.ease}, color .24s ${T.ease}, transform .28s ${T.spring}, box-shadow .28s ${T.spring}`,
          marginBottom: collapsed ? 7 : 0,
          boxShadow: active === item.id ? "inset 0 1px 0 rgba(255,255,255,.74)" : "none"
        },
        onMouseEnter: (e) => {
          if (active !== item.id) e.currentTarget.style.background = "rgba(14,14,44,.028)";
        },
        onMouseLeave: (e) => {
          if (active !== item.id) e.currentTarget.style.background = "transparent";
        }
      },
      /* @__PURE__ */ React.createElement(Icon, { name: item.icon, size: collapsed ? 15 : 16, color: active === item.id ? T.iris : T.navyMid }),
      !collapsed && item.label
    ))), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 22, paddingTop: 18, borderTop: `1px solid ${T.hairline}`, flex: 1, overflow: "hidden", display: "flex", flexDirection: "column" } }, !collapsed && /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11, fontWeight: 620, letterSpacing: 0, color: T.navyLight, padding: "0 10px 10px" } }, "\u6700\u8FD1"), !collapsed && /* @__PURE__ */ React.createElement("div", { style: { overflowY: "auto", display: "flex", flexDirection: "column", gap: 1 } }, GLOBAL_RECENT_SESSIONS.map((s, i) => /* @__PURE__ */ React.createElement(
      "a",
      {
        key: i,
        href: "#",
        style: {
          padding: collapsed ? "8px 0" : "6px 10px",
          borderRadius: 6,
          fontSize: 11.5,
          color: T.navyLight,
          fontWeight: 450,
          textDecoration: "none",
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
          transition: "background .12s",
          textAlign: collapsed ? "center" : "left"
        },
        onMouseEnter: (e) => e.currentTarget.style.background = "rgba(14,14,44,.03)",
        onMouseLeave: (e) => e.currentTarget.style.background = "transparent"
      },
      collapsed ? `${i + 1}` : s
    )))), /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          display: "flex",
          alignItems: "center",
          gap: 10,
          justifyContent: collapsed ? "center" : "flex-start",
          padding: collapsed ? "8px 0" : "10px",
          borderRadius: collapsed ? 16 : 10,
          marginTop: 12,
          cursor: "pointer",
          transition: "background .12s"
        },
        onMouseEnter: (e) => e.currentTarget.style.background = T.surface,
        onMouseLeave: (e) => e.currentTarget.style.background = "transparent"
      },
      /* @__PURE__ */ React.createElement("div", { style: {
        width: collapsed ? 36 : 28,
        height: collapsed ? 36 : 28,
        borderRadius: "50%",
        background: `linear-gradient(135deg, ${T.iris}, ${T.peach})`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: T.white,
        fontSize: collapsed ? 12 : 11,
        fontWeight: 700,
        boxShadow: collapsed ? T.shadowSm : "none"
      } }, "L"),
      !collapsed && /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexDirection: "column", minWidth: 0, flex: 1 } }, /* @__PURE__ */ React.createElement("span", { style: { fontSize: 12, fontWeight: 600, color: T.navy } }, "Luna"), /* @__PURE__ */ React.createElement("span", { style: { fontSize: 10, color: T.navyLight } }, "Pro \xB7 87 / 200 \u6B21")),
      !collapsed && /* @__PURE__ */ React.createElement(Icon, { name: "moreH", size: 14, color: T.navyLight })
    ));
  };
  var OnionBurst = ({ active, mobile }) => {
    const pieces = [
      { src: ONION_BURST_ASSETS[0], x: -104, y: -70, r: -13, s: 0.54, d: "0ms" },
      { src: ONION_BURST_ASSETS[1], x: 86, y: -78, r: 14, s: 0.45, d: "45ms" },
      { src: ONION_BURST_ASSETS[2], x: 116, y: 10, r: 11, s: 0.47, d: "90ms" },
      { src: ONION_BURST_ASSETS[3], x: -118, y: 18, r: -8, s: 0.43, d: "120ms" },
      { src: ONION_BURST_ASSETS[4], x: 28, y: -112, r: 6, s: 0.41, d: "155ms" }
    ];
    if (!active) return null;
    return /* @__PURE__ */ React.createElement("div", { "aria-hidden": "true", style: { position: "absolute", left: "50%", top: "46%", width: 1, height: 1, pointerEvents: "none", zIndex: 3 } }, pieces.map((piece, i) => /* @__PURE__ */ React.createElement(
      "img",
      {
        key: `${piece.src}-${i}`,
        src: piece.src,
        alt: "",
        style: {
          position: "absolute",
          width: mobile ? 40 : 54,
          height: mobile ? 40 : 54,
          objectFit: "contain",
          mixBlendMode: "multiply",
          "--x": `${mobile ? piece.x * 0.62 : piece.x}px`,
          "--y": `${mobile ? piece.y * 0.62 : piece.y}px`,
          "--r": `${piece.r}deg`,
          filter: "drop-shadow(0 10px 20px rgba(14,14,44,.08))",
          animation: `onionPop 1.45s ${piece.d} ${T.spring} both`
        }
      }
    )), [0, 1, 2, 3, 4, 5].map((i) => /* @__PURE__ */ React.createElement("span", { key: i, style: {
      position: "absolute",
      left: 0,
      top: 0,
      width: i % 2 ? 5 : 4,
      height: i % 2 ? 5 : 4,
      borderRadius: "50%",
      background: i % 3 === 0 ? T.primary : i % 3 === 1 ? T.iris : T.peach,
      "--spark-x": `${mobile ? [-74, 68, 116, -110, 28, -18][i] * 0.62 : [-74, 68, 116, -110, 28, -18][i]}px`,
      "--spark-y": `${mobile ? [-50, -60, 52, 44, -112, 88][i] * 0.62 : [-50, -60, 52, 44, -112, 88][i]}px`,
      boxShadow: "0 0 16px currentColor",
      animation: `sparkPop 1.2s ${i * 48}ms ${T.spring} both`
    } })));
  };
  var HeroHeadline = ({ compact, mobile }) => {
    const [burst, setBurst] = React.useState(false);
    const triggerBurst = () => {
      setBurst(false);
      window.requestAnimationFrame(() => setBurst(true));
    };
    React.useEffect(() => {
      if (!burst) return void 0;
      const timer = window.setTimeout(() => setBurst(false), 1700);
      return () => window.clearTimeout(timer);
    }, [burst]);
    return /* @__PURE__ */ React.createElement("div", { style: {
      position: "relative",
      width: "100%",
      marginBottom: mobile ? 14 : 18,
      textAlign: "center"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      left: "50%",
      top: "46%",
      width: mobile ? 170 : 300,
      height: mobile ? 88 : 120,
      borderRadius: "50%",
      background: "radial-gradient(circle, rgba(214,255,0,.12), rgba(243,217,218,.10) 46%, rgba(75,77,237,.055) 62%, transparent 76%)",
      opacity: 0.38,
      transform: "translate3d(-50%, -50%, 0)",
      filter: "blur(24px)",
      pointerEvents: "none"
    } }), /* @__PURE__ */ React.createElement(OnionBurst, { active: burst, mobile }), /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: triggerBurst,
        "aria-label": "\u89E6\u53D1 Nori \u6D0B\u8471\u95EA\u5149",
        className: burst ? "noriWord noriWordSpark" : "noriWord",
        style: {
          position: "relative",
          zIndex: 4,
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          border: "none",
          background: "transparent",
          padding: "0 8px 2px",
          cursor: "pointer",
          color: T.navy,
          fontFamily: T.fontSerif,
          fontSize: mobile ? 38 : compact ? 54 : 62,
          lineHeight: 0.92,
          fontWeight: 700,
          fontStyle: "italic",
          letterSpacing: 0
        }
      },
      "Nori"
    ), /* @__PURE__ */ React.createElement("p", { style: {
      position: "relative",
      zIndex: 1,
      margin: mobile ? "8px 0 0" : "12px 0 0",
      color: T.navyLight,
      fontSize: mobile ? 12 : 13,
      lineHeight: 1.55,
      fontWeight: 520,
      letterSpacing: 0
    } }, "\u61C2\u4F60\uFF0C\u4F1A\u8FDB\u5316\u7684\u81EA\u5A92\u4F53\u8D26\u53F7\u4EE3\u7406"));
  };
  var FormatTag = ({ label, sub, onCancel }) => /* @__PURE__ */ React.createElement("div", { style: {
    display: "inline-flex",
    alignItems: "center",
    gap: 6,
    padding: "4px 6px 4px 10px",
    borderRadius: 999,
    background: T.irisTint,
    color: T.iris,
    fontSize: 12,
    fontWeight: 600,
    marginBottom: 10
  } }, label, sub ? ` \xB7 ${sub}` : "", /* @__PURE__ */ React.createElement("button", { onClick: onCancel, style: {
    width: 18,
    height: 18,
    borderRadius: "50%",
    border: "none",
    cursor: "pointer",
    background: "rgba(75,77,237,.15)",
    color: T.iris,
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center"
  } }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 10, stroke: 2.4 })));
  var HomeComposer = ({ value, onChange, onSubmit, format, onClearFormat, compact, mobile }) => {
    const [focused, setFocused] = React.useState(false);
    const prompts = [
      "\u8BA9 Nori \u751F\u6210\u4E00\u7EC4\u57CE\u5E02\u63A2\u5E97\u7684\u5C0F\u7EA2\u4E66\u56FE\u6587",
      "\u8BA9 Nori \u6253\u9020\u4E00\u4E2A\u5973\u6027\u6210\u957F\u535A\u4E3B\u7684\u8D26\u53F7",
      "\u8BA9 Nori \u751F\u6210\u4E00\u7BC7\u6709\u5173\u4E8E AI \u6700\u65B0\u62A5\u9053\u7684\u516C\u4F17\u53F7\u6587\u7AE0",
      "\u8BA9 Nori \u8BBE\u8BA1\u4E00\u7EC4\u901A\u52E4\u7A7F\u642D\u9009\u9898",
      "\u8BA9 Nori \u62C6\u89E3\u4E00\u4E2A\u5496\u5561\u54C1\u724C\u7684\u5185\u5BB9\u589E\u957F\u8DEF\u5F84",
      "\u8BA9 Nori \u628A\u7075\u611F\u53D8\u6210\u4E00\u5468\u77ED\u89C6\u9891\u811A\u672C"
    ];
    const [promptIndex, setPromptIndex] = React.useState(0);
    React.useEffect(() => {
      const timer = window.setInterval(() => {
        setPromptIndex((i) => (i + 1) % prompts.length);
      }, 2600);
      return () => window.clearInterval(timer);
    }, []);
    return /* @__PURE__ */ React.createElement("div", { style: {
      position: "relative",
      background: "linear-gradient(180deg, rgba(255,255,255,.94), rgba(250,252,254,.82))",
      borderRadius: mobile ? 20 : 24,
      border: `1.4px solid ${focused ? "rgba(75,77,237,.22)" : "rgba(75,77,237,.11)"}`,
      boxShadow: focused ? `0 0 0 4px rgba(75,77,237,.055), 0 20px 46px rgba(14,14,44,.065), 0 16px 42px rgba(49,208,170,.045), inset 0 1px 0 rgba(255,255,255,.95)` : "0 16px 42px rgba(14,14,44,.052), 0 12px 36px rgba(49,208,170,.032), inset 0 1px 0 rgba(255,255,255,.9)",
      padding: mobile ? "13px 13px 11px" : compact ? "16px 18px 14px" : "17px 20px 14px",
      transition: `border .28s ${T.ease}, box-shadow .36s ${T.spring}, transform .36s ${T.spring}`,
      backdropFilter: "blur(26px) saturate(1.2)",
      overflow: "hidden",
      animation: focused ? "prismBorder 2.8s ease-in-out infinite" : "none"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      inset: 0,
      background: "radial-gradient(circle at 12% 18%, rgba(214,255,0,.11), transparent 32%), radial-gradient(circle at 92% 12%, rgba(75,77,237,.055), transparent 25%)",
      pointerEvents: "none"
    } }), /* @__PURE__ */ React.createElement("div", { style: { position: "relative", zIndex: 1 } }, format && /* @__PURE__ */ React.createElement(FormatTag, { label: format.label, sub: format.sub, onCancel: onClearFormat }), /* @__PURE__ */ React.createElement("div", { style: { position: "relative" } }, !value && /* @__PURE__ */ React.createElement(
      "div",
      {
        key: promptIndex,
        style: {
          position: "absolute",
          left: 0,
          top: 0,
          right: 0,
          color: T.navyLight,
          fontSize: mobile ? 14 : 15,
          fontWeight: 570,
          lineHeight: 1.55,
          pointerEvents: "none",
          animation: `templateTicker 2.6s ${T.spring} both`,
          whiteSpace: mobile ? "normal" : "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis"
        }
      },
      prompts[promptIndex]
    ), /* @__PURE__ */ React.createElement(
      "textarea",
      {
        value,
        onChange: (e) => onChange(e.target.value),
        onFocus: () => setFocused(true),
        onBlur: () => setFocused(false),
        onKeyDown: (e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (value.trim()) onSubmit();
          }
        },
        placeholder: "",
        rows: mobile ? 3 : 2,
        style: {
          width: "100%",
          border: "none",
          outline: "none",
          background: "transparent",
          resize: "none",
          fontSize: mobile ? 14 : 15,
          fontWeight: 570,
          lineHeight: 1.55,
          color: T.navy,
          fontFamily: T.fontSans,
          minHeight: mobile ? 74 : 76,
          maxHeight: 124,
          position: "relative",
          zIndex: 1
        }
      }
    )), /* @__PURE__ */ React.createElement("div", { style: {
      display: "flex",
      alignItems: mobile ? "stretch" : "center",
      justifyContent: "space-between",
      gap: 10,
      marginTop: mobile ? 2 : 6,
      flexDirection: mobile ? "column" : "row"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 6, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement(ToolPill, { icon: "paperclip", label: "\u9644\u4EF6" }), /* @__PURE__ */ React.createElement(ToolPill, { icon: "sparkle", label: "\u4F18\u5316" })), /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: () => value.trim() && onSubmit(),
        disabled: !value.trim(),
        style: {
          width: mobile ? "100%" : 38,
          height: mobile ? 36 : 38,
          borderRadius: mobile ? 999 : "50%",
          border: "none",
          cursor: value.trim() ? "pointer" : "not-allowed",
          background: value.trim() ? T.navy : "rgba(14,14,44,.075)",
          color: value.trim() ? T.white : T.navyLight,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 8,
          boxShadow: value.trim() ? "0 10px 22px rgba(14,14,44,.16), inset 0 1px 0 rgba(255,255,255,.10)" : "none",
          transition: `transform .26s ${T.spring}, box-shadow .26s ${T.spring}, background .2s ${T.ease}, color .2s ${T.ease}`
        },
        onMouseEnter: (e) => {
          if (value.trim()) e.currentTarget.style.transform = "translateY(-1px) scale(1.02)";
        },
        onMouseLeave: (e) => {
          e.currentTarget.style.transform = "translateY(0) scale(1)";
        }
      },
      /* @__PURE__ */ React.createElement(Icon, { name: "paperPlane", size: 13, stroke: 2 }),
      mobile && /* @__PURE__ */ React.createElement("span", { style: { fontSize: 13, fontWeight: 600 } }, "Start crafting")
    ))));
  };
  var HomeIpModeBar = ({ mobile, onAccountPlan, onViewProfile, planned }) => {
    const [freeMode, setFreeMode] = React.useState(false);
    const isIpMode = planned && !freeMode;
    const icon = isIpMode ? "check" : freeMode ? "unlock" : "lock";
    const title = isIpMode ? "\u5DF2\u5F00\u542F IP \u6A21\u5F0F \xB7 \u4E0A\u6D77\u5C0F\u996D\u5E97\u4E3B\u7406\u4EBA" : freeMode ? "\u81EA\u7531\u6A21\u5F0F \xB7 \u5185\u5BB9\u4E0D\u5173\u8054 IP" : "\u5B8C\u6210\u8D26\u53F7\u89C4\u5212\uFF0C\u89E3\u9501 IP \u6A21\u5F0F";
    const desc = isIpMode ? "\u771F\u5B9E\u5230\u5E97 \xB7 \u83DC\u54C1\u7A33\u5B9A \xB7 \u5148\u7ED3\u8BBA\u518D\u5C55\u5F00" : freeMode ? "" : "\u6309\u95E8\u5E97\u6C14\u8D28\u548C\u7ECF\u8425\u65B9\u5F0F\u751F\u6210";
    return /* @__PURE__ */ React.createElement("div", { style: {
      width: "100%",
      minHeight: mobile ? 52 : 54,
      borderRadius: mobile ? 20 : 22,
      border: planned && !freeMode ? `1px solid rgba(14,14,44,.08)` : `1px dashed rgba(14,14,44,.16)`,
      background: "rgba(255,255,255,.86)",
      boxShadow: planned && !freeMode ? "0 12px 26px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.9)" : "inset 0 1px 0 rgba(255,255,255,.9)",
      display: "flex",
      alignItems: mobile ? "flex-start" : "center",
      justifyContent: "space-between",
      gap: 12,
      padding: mobile ? "13px 14px" : "0 18px",
      marginBottom: 12,
      flexDirection: mobile ? "column" : "row"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10, minWidth: 0 } }, /* @__PURE__ */ React.createElement("span", { style: {
      width: isIpMode || freeMode ? 10 : 28,
      height: isIpMode || freeMode ? 10 : 28,
      borderRadius: isIpMode || freeMode ? "50%" : 10,
      background: isIpMode ? T.success : freeMode ? "rgba(14,14,44,.18)" : T.irisTint,
      border: isIpMode || freeMode ? "none" : `1px solid ${T.hairlineSoft}`,
      color: isIpMode ? T.success : freeMode ? T.navyMid : T.iris,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0
    } }, !isIpMode && !freeMode && /* @__PURE__ */ React.createElement(Icon, { name: icon === "unlock" ? "lock" : icon, size: 13 })), /* @__PURE__ */ React.createElement("div", { style: { minWidth: 0, color: T.navyMid, fontSize: mobile ? 13 : 14, lineHeight: 1.42 } }, /* @__PURE__ */ React.createElement("span", { style: { color: T.navy, fontWeight: isIpMode ? 640 : 680 } }, title), desc && /* @__PURE__ */ React.createElement("span", null, " \xB7 ", desc))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 12, flexShrink: 0 } }, isIpMode && /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: onViewProfile,
        style: {
          border: "none",
          background: "transparent",
          color: T.navyMid,
          cursor: "pointer",
          fontSize: 13,
          fontWeight: 660,
          padding: "6px 4px"
        }
      },
      "\u67E5\u770B"
    ), (!isIpMode || freeMode) && /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: onAccountPlan,
        style: {
          border: freeMode ? `1px solid ${T.hairlineSoft}` : "none",
          background: freeMode ? "rgba(255,255,255,.72)" : T.navy,
          color: freeMode ? T.navy : T.white,
          cursor: "pointer",
          fontSize: 12.5,
          fontWeight: 700,
          height: 32,
          padding: "0 12px",
          borderRadius: 999,
          display: "inline-flex",
          alignItems: "center",
          gap: 6,
          boxShadow: freeMode ? "none" : "0 10px 20px rgba(14,14,44,.12)"
        }
      },
      freeMode ? "\u5F00\u542F" : "\u5F00\u59CB",
      /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 12 })
    ), isIpMode && /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: () => setFreeMode(true),
        style: {
          border: "none",
          background: "rgba(255,255,255,.72)",
          color: T.navy,
          cursor: "pointer",
          fontSize: 13,
          fontWeight: 700,
          height: 36,
          padding: "0 14px",
          borderRadius: 999,
          boxShadow: `inset 0 0 0 1px ${T.hairlineSoft}`
        }
      },
      "\u5173\u95ED"
    )));
  };
  var FormatPicker = ({ format, onPick, compact, mobile }) => {
    const [openCat, setOpenCat] = React.useState(null);
    const cats = [
      { key: "xhs", icon: "image", label: "\u5C0F\u7EA2\u4E66\u56FE\u6587" },
      { key: "wechat", icon: "document", label: "\u516C\u4F17\u53F7\u957F\u6587" },
      { key: "video", icon: "video", label: "\u6296\u97F3\u77ED\u89C6\u9891" },
      { key: "wechatShort", icon: "video", label: "\u516C\u4F17\u53F7\u77ED\u89C6\u9891" },
      { key: "drama", icon: "play", label: "\u6F2B\u5267" },
      { key: "podcast", icon: "headphone", label: "\u64AD\u5BA2" },
      { key: "ins", icon: "image", label: "Ins post" }
    ];
    const subs = {
      xhs: ["\u7206\u6B3E\u79CD\u8349", "\u653B\u7565\u5E72\u8D27", "\u751F\u6D3B\u8BB0\u5F55", "\u4EA7\u54C1\u6D4B\u8BC4"],
      wechat: ["\u6DF1\u5EA6\u957F\u6587", "\u89C2\u70B9\u4E13\u680F", "\u4EBA\u7269\u8BBF\u8C08", "\u884C\u4E1A\u5206\u6790"],
      video: ["\u79D1\u666E\u89C6\u9891", "\u4EA7\u54C1\u5BA3\u4F20", "\u6F2B\u5267", "\u53E3\u64AD"],
      wechatShort: ["\u95E8\u5E97\u77ED\u7247", "\u6D3B\u52A8\u9884\u544A", "\u4E3B\u7406\u4EBA\u51FA\u955C", "\u83DC\u54C1\u5C55\u793A"],
      drama: ["\u5267\u60C5\u79CD\u8349", "\u4EBA\u7269\u5173\u7CFB", "\u53CD\u8F6C\u94A9\u5B50", "\u8FDE\u8F7D\u811A\u672C"],
      podcast: ["\u8BBF\u8C08\u63D0\u7EB2", "\u5355\u4EBA\u53E3\u64AD", "\u64AD\u5BA2\u5207\u7247", "\u8282\u76EE\u5927\u7EB2"],
      ins: ["\u4E5D\u5BAB\u683C", "Reels \u5C01\u9762", "Story", "Carousel"]
    };
    const current = openCat ? cats.find((c) => c.key === openCat) : null;
    return /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexWrap: "wrap", gap: 8, justifyContent: mobile ? "center" : "flex-start" } }, cats.map((c) => {
      const isOpen = openCat === c.key;
      const isPicked = format && format.cat === c.key;
      return /* @__PURE__ */ React.createElement(
        "button",
        {
          key: c.key,
          onClick: () => setOpenCat(isOpen ? null : c.key),
          style: {
            minHeight: 32,
            padding: compact ? "0 10px" : "0 12px",
            borderRadius: 99,
            border: `1px solid ${isOpen || isPicked ? "rgba(14,14,44,.32)" : T.hairlineSoft}`,
            background: isOpen || isPicked ? T.navy : "rgba(255,255,255,.72)",
            color: isOpen || isPicked ? T.white : T.navyMid,
            fontSize: 12.5,
            fontWeight: 520,
            cursor: "pointer",
            display: "inline-flex",
            alignItems: "center",
            gap: 6,
            boxShadow: isOpen || isPicked ? "0 10px 24px rgba(14,14,44,.12)" : "0 6px 16px rgba(14,14,44,.035)",
            transition: `transform .28s ${T.spring}, background .22s ${T.ease}, border .22s ${T.ease}, box-shadow .28s ${T.spring}`,
            backdropFilter: "blur(14px) saturate(1.18)"
          }
        },
        /* @__PURE__ */ React.createElement(Icon, { name: c.icon, size: 13 }),
        c.label
      );
    })), current && /* @__PURE__ */ React.createElement("div", { style: {
      marginTop: 10,
      display: "flex",
      flexWrap: "wrap",
      gap: 8,
      animation: `fadeIn .28s ${T.spring}`,
      justifyContent: mobile ? "center" : "flex-start"
    } }, subs[current.key].map((s, i) => /* @__PURE__ */ React.createElement(
      "button",
      {
        key: i,
        onClick: () => {
          onPick({ cat: current.key, label: current.label, sub: s });
          setOpenCat(null);
        },
        style: {
          background: "rgba(255,255,255,.82)",
          border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 16,
          padding: "8px 12px",
          textAlign: "left",
          cursor: "pointer",
          display: "flex",
          flexDirection: "column",
          gap: 2,
          minWidth: mobile ? 124 : 136,
          transition: `transform .28s ${T.spring}, border .22s ${T.ease}, box-shadow .28s ${T.spring}`,
          boxShadow: "0 8px 18px rgba(14,14,44,.04)"
        },
        onMouseEnter: (e) => {
          e.currentTarget.style.borderColor = "rgba(75,77,237,.4)";
          e.currentTarget.style.transform = "translateY(-1px)";
        },
        onMouseLeave: (e) => {
          e.currentTarget.style.borderColor = T.hairlineSoft;
          e.currentTarget.style.transform = "translateY(0)";
        }
      },
      /* @__PURE__ */ React.createElement("span", { style: { fontSize: 12.5, fontWeight: 600, color: T.navy } }, s),
      /* @__PURE__ */ React.createElement("span", { style: { fontSize: 10.5, color: T.navyLight } }, current.label, " \xB7 ", s)
    ))));
  };
  var ToolPill = ({ icon, label, active, onClick }) => {
    const [hov, setHov] = React.useState(false);
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        type: "button",
        onClick,
        onMouseEnter: () => setHov(true),
        onMouseLeave: () => setHov(false),
        style: {
          height: 32,
          padding: "0 12px",
          borderRadius: 99,
          background: active ? "rgba(239,239,253,.92)" : hov ? "rgba(255,255,255,.88)" : "rgba(255,255,255,.68)",
          border: `1px solid ${active ? "rgba(75,77,237,.22)" : "rgba(14,14,44,.08)"}`,
          color: active ? T.iris : T.navyMid,
          display: "inline-flex",
          alignItems: "center",
          gap: 6,
          fontSize: 12.5,
          fontWeight: active ? 690 : 580,
          cursor: "pointer",
          transform: hov ? "translateY(-1px)" : "translateY(0)",
          transition: `transform .24s ${T.spring}, background .24s ${T.ease}, border .24s ${T.ease}, color .24s ${T.ease}`
        }
      },
      /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 14 }),
      label
    );
  };
  var SectionTitle = ({ title, action, mobile }) => /* @__PURE__ */ React.createElement("div", { style: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 16,
    marginBottom: mobile ? 12 : 16
  } }, /* @__PURE__ */ React.createElement("h2", { style: {
    margin: 0,
    color: T.navy,
    fontSize: mobile ? 18 : 21,
    lineHeight: 1.2,
    fontWeight: 720,
    letterSpacing: 0
  } }, title), action && /* @__PURE__ */ React.createElement("button", { style: {
    border: "none",
    background: "transparent",
    color: T.navyLight,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    gap: 6,
    fontSize: mobile ? 12.5 : 13.5,
    fontWeight: 520,
    padding: "6px 0"
  } }, action, /* @__PURE__ */ React.createElement(Icon, { name: "chevronRight", size: 13 })));
  var InspirationCard = ({ item, index, onUse }) => {
    const [buttonHover, setButtonHover] = React.useState(false);
    return /* @__PURE__ */ React.createElement(
      "article",
      {
        style: {
          breakInside: "avoid",
          marginBottom: 16,
          borderRadius: 18,
          overflow: "hidden",
          background: "rgba(255,255,255,.82)",
          border: `1px solid ${T.hairlineSoft}`,
          boxShadow: "0 9px 22px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.86)",
          animation: `fadeInScale .48s ${index % 5 * 42}ms ${T.spring} both`,
          transition: `transform .34s ${T.spring}, box-shadow .34s ${T.spring}`
        },
        onMouseEnter: (e) => {
          e.currentTarget.style.transform = "translateY(-3px)";
          e.currentTarget.style.boxShadow = "0 16px 34px rgba(14,14,44,.065), inset 0 1px 0 rgba(255,255,255,.9)";
        },
        onMouseLeave: (e) => {
          e.currentTarget.style.transform = "translateY(0)";
          e.currentTarget.style.boxShadow = "0 9px 22px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.86)";
        }
      },
      /* @__PURE__ */ React.createElement("div", { style: { overflow: "hidden", borderRadius: "18px 18px 0 0", background: T.surface } }, /* @__PURE__ */ React.createElement(
        "img",
        {
          src: item.image,
          alt: "",
          style: {
            width: "100%",
            aspectRatio: item.ratio,
            objectFit: "cover",
            display: "block",
            transition: `transform .68s ${T.spring}, filter .4s ${T.ease}`
          },
          onMouseEnter: (e) => {
            e.currentTarget.style.transform = "scale(1.055)";
            e.currentTarget.style.filter = "saturate(1.04)";
          },
          onMouseLeave: (e) => {
            e.currentTarget.style.transform = "scale(1)";
            e.currentTarget.style.filter = "saturate(1)";
          }
        }
      )),
      /* @__PURE__ */ React.createElement("div", { style: { padding: "13px 13px 12px" } }, /* @__PURE__ */ React.createElement("h3", { style: { margin: 0, color: T.navy, fontSize: 14, lineHeight: 1.32, fontWeight: 700, letterSpacing: 0 } }, item.title), /* @__PURE__ */ React.createElement("p", { style: { margin: "4px 0 12px", color: T.navyMid, fontSize: 11.5, lineHeight: 1.45, fontWeight: 450 } }, item.desc), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "inline-flex", alignItems: "center", gap: 10, color: T.navyMid, fontSize: 11.5, fontWeight: 600 } }, /* @__PURE__ */ React.createElement("span", { style: { display: "inline-flex", alignItems: "center", gap: 5 } }, /* @__PURE__ */ React.createElement(Icon, { name: "star", size: 14, color: "#f7c600" }), item.stars), /* @__PURE__ */ React.createElement("span", { style: { display: "inline-flex", alignItems: "center", gap: 5 } }, /* @__PURE__ */ React.createElement(Icon, { name: "heart", size: 14, color: "#ff5f8f" }), item.likes)), /* @__PURE__ */ React.createElement(
        "button",
        {
          onClick: () => onUse && onUse(item),
          onMouseEnter: () => setButtonHover(true),
          onMouseLeave: () => setButtonHover(false),
          style: {
            height: 30,
            padding: "0 11px",
            borderRadius: 12,
            border: `1px solid ${buttonHover ? "rgba(14,14,44,.16)" : T.hairlineSoft}`,
            background: buttonHover ? T.navy : "rgba(246,248,251,.92)",
            color: buttonHover ? T.white : T.navyMid,
            display: "inline-flex",
            alignItems: "center",
            gap: 6,
            cursor: "pointer",
            fontSize: 11.5,
            fontWeight: 620,
            boxShadow: buttonHover ? "0 10px 20px rgba(14,14,44,.12)" : "inset 0 1px 0 rgba(255,255,255,.82)",
            transform: buttonHover ? "translateY(-1px)" : "translateY(0)",
            transition: `transform .24s ${T.spring}, background .2s ${T.ease}, color .2s ${T.ease}, box-shadow .24s ${T.spring}`
          }
        },
        "\u4F7F\u7528",
        /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 13 })
      )))
    );
  };
  var InspirationDetailView = ({ item, onBack, onUse }) => {
    if (!item) return null;
    const prompt = `\u53C2\u8003\u300C${item.title}\u300D\u7684\u6784\u56FE\uFF1A\u4FDD\u7559\u771F\u5B9E\u5E97\u94FA\u7167\u7247\u8D28\u611F\uFF0C\u6807\u9898\u653E\u5728\u753B\u9762\u4E0B\u4E09\u5206\u4E4B\u4E00\uFF0C\u6574\u4F53\u66F4\u50CF\u4E0A\u6D77\u996D\u5E97\u63A2\u5E97\u5C01\u9762\uFF0C\u5C11\u4E00\u70B9\u6A21\u677F\u611F\u3002`;
    return /* @__PURE__ */ React.createElement("section", { style: {
      width: "100%",
      maxWidth: 960,
      margin: "0 auto",
      borderRadius: 22,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.86)",
      boxShadow: "0 18px 42px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.86)",
      padding: 16,
      display: "grid",
      gridTemplateColumns: "minmax(220px, 320px) minmax(0, 1fr)",
      gap: 18
    } }, /* @__PURE__ */ React.createElement("button", { onClick: onBack, style: { position: "absolute", opacity: 0, pointerEvents: "none" } }), /* @__PURE__ */ React.createElement("div", { style: { borderRadius: 18, overflow: "hidden", background: T.surface, border: `1px solid ${T.hairlineSoft}` } }, /* @__PURE__ */ React.createElement("img", { src: item.image, alt: "", style: { width: "100%", aspectRatio: "1 / 1", objectFit: "cover", display: "block" } })), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 12, alignContent: "start" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 12, alignItems: "flex-start" } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 11.5, fontWeight: 720, marginBottom: 6 } }, item.category), /* @__PURE__ */ React.createElement("h3", { style: { margin: 0, color: T.navy, fontSize: 22, lineHeight: 1.22, fontWeight: 760 } }, item.title)), /* @__PURE__ */ React.createElement("button", { onClick: onBack, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 13 }))), /* @__PURE__ */ React.createElement("p", { style: { margin: 0, color: T.navyMid, fontSize: 13.2, lineHeight: 1.72 } }, item.desc, "\u3002\u9002\u5408\u63D0\u53D6\u5C01\u9762\u6784\u56FE\u3001\u6807\u9898\u8282\u594F\u548C\u63D0\u793A\u8BCD\u7ED3\u6784\u3002"), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, [
      ["\u6807\u9898", item.title],
      ["\u6587\u6848", "\u628A\u573A\u666F\u8BF4\u6E05\u695A\uFF0C\u628A\u51B3\u7B56\u6210\u672C\u964D\u4E0B\u6765\uFF0C\u8BA9\u7528\u6237\u77E5\u9053\u4E3A\u4EC0\u4E48\u73B0\u5728\u5C31\u503C\u5F97\u6536\u85CF\u3002"],
      ["\u63D0\u793A\u8BCD", prompt]
    ].map(([label, value]) => /* @__PURE__ */ React.createElement("div", { key: label, style: { borderRadius: 14, background: "rgba(250,252,254,.72)", border: `1px solid ${T.hairlineSoft}`, padding: 11 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 11.5, fontWeight: 700, marginBottom: 5 } }, label), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 12.8, lineHeight: 1.62 } }, value)))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => onUse?.({ item, prompt }), style: { ...pillButtonStyle(true), height: 38, borderRadius: 13, fontSize: 13 } }, "\u76F4\u63A5\u4F7F\u7528", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 14 })))));
  };
  var InspirationDiscovery = ({ mobile, compact, onUseInspiration }) => {
    const [category, setCategory] = React.useState("\u5168\u90E8");
    const [search, setSearch] = React.useState("");
    const [usedTitle, setUsedTitle] = React.useState("");
    const [detail, setDetail] = React.useState(null);
    const categories = ["\u5168\u90E8", "\u77ED\u89C6\u9891", "\u56FE\u6587", "\u63A8\u9001\u6587\u7AE0", "\u6F2B\u5267", "\u5176\u4ED6"];
    const images = [
      "./src/inspiration-skill-card.png",
      "https://images.unsplash.com/photo-1512290923902-8a9f81dc236c?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1460317442991-0ec209397118?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1519052537078-e6302a4968d4?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1442512595331-e89e73853f31?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=900&q=80",
      "https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=900&q=80"
    ];
    const titles = ["\u7F8E\u62C9\u5FB7\u7F8E\u7532", "\u5973\u6027\u6210\u957F\u8D26\u53F7\u5C01\u9762", "AI \u65B0\u95FB\u901F\u9012", "\u57CE\u5E02\u751F\u6D3B\u63D0\u6848", "\u4EA7\u54C1\u79CD\u8349\u6A21\u677F", "\u5496\u5561\u9986\u5185\u5BB9\u7B56\u5C55", "\u54C1\u724C\u89C6\u89C9\u7075\u611F", "\u6CBB\u6108\u7CFB\u98DF\u8C31", "\u4E3B\u7406\u4EBA\u5E55\u540E\u624B\u5E10", "\u77E5\u8BC6 IP \u9009\u9898\u5E93", "\u732B\u54AA\u680F\u76EE\u5316\u65E5\u5E38", "\u5496\u5561\u5165\u95E8\u5361\u7247", "\u8FD0\u52A8\u53CD\u5DEE\u5185\u5BB9", "\u8F7B\u719F\u7A7F\u642D\u811A\u672C", "\u5EFA\u7B51\u7A7A\u95F4\u53D9\u4E8B"];
    const items = images.map((image, i) => ({
      image,
      title: titles[i],
      category: categories[i % (categories.length - 1) + 1],
      desc: i === 0 ? "\u4E00\u4E2A\u6709\u5173\u624B\u7F8E\u7532\u5982\u4F55\u62CD\u7167\u624D\u597D\u770B\u7684 skill" : ["\u5C01\u9762\u3001\u6807\u9898\u3001\u811A\u672C\u4E0E\u5206\u53D1\u5EFA\u8BAE\u4E00\u4F53\u751F\u6210", "\u9002\u5408\u505A\u6210\u8D26\u53F7\u957F\u671F\u680F\u76EE\u4E0E\u5185\u5BB9\u8D44\u4EA7", "\u4ECE\u89C6\u89C9\u53C2\u8003\u63D0\u70BC\u53EF\u590D\u7528\u7684\u5185\u5BB9\u6A21\u677F"][i % 3],
      stars: [500, 820, 640, 320, 980, 760, 440][i % 7],
      likes: [3200, 1860, 2480, 910, 4020, 1650, 2880][i % 7],
      ratio: ["1 / 1.02", "1 / 1.28", "1 / 0.92", "1 / 1.16", "1 / 0.78"][i % 5]
    }));
    const filtered = items.filter((item) => category === "\u5168\u90E8" || item.category === category).filter((item) => !search.trim() || `${item.title} ${item.desc} ${item.category}`.toLowerCase().includes(search.trim().toLowerCase()));
    if (detail) {
      return /* @__PURE__ */ React.createElement(InspirationDetailView, { item: detail, onBack: () => setDetail(null), onUse: ({ item, prompt }) => {
        setUsedTitle(item.title);
        setDetail(null);
        onUseInspiration?.({ item, prompt });
      } });
    }
    return /* @__PURE__ */ React.createElement("section", { style: {
      width: "100%",
      maxWidth: mobile ? "100%" : compact ? 820 : 960,
      margin: "0 auto"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      display: "flex",
      alignItems: mobile ? "flex-start" : "center",
      justifyContent: "space-between",
      gap: 16,
      marginBottom: mobile ? 12 : 16,
      flexDirection: mobile ? "column" : "row"
    } }, /* @__PURE__ */ React.createElement(SectionTitle, { title: "\u7075\u611F\u53D1\u73B0", mobile }), /* @__PURE__ */ React.createElement("div", { style: {
      display: "flex",
      gap: mobile ? 8 : 10,
      overflowX: "auto",
      paddingBottom: mobile ? 4 : 0,
      maxWidth: "100%",
      alignItems: "center",
      flexWrap: mobile ? "wrap" : "nowrap"
    } }, categories.map((cat, i) => /* @__PURE__ */ React.createElement("button", { key: cat, onClick: () => setCategory(cat), style: {
      height: mobile ? 32 : 34,
      padding: "0 14px",
      borderRadius: 999,
      border: `1px solid ${category === cat ? "transparent" : "rgba(14,14,44,.08)"}`,
      background: category === cat ? T.navy : "rgba(255,255,255,.72)",
      color: category === cat ? T.white : T.navyMid,
      fontSize: mobile ? 12 : 12.5,
      fontWeight: category === cat ? 700 : 580,
      cursor: "pointer",
      whiteSpace: "nowrap",
      boxShadow: category === cat ? "0 10px 20px rgba(14,14,44,.12)" : "0 5px 12px rgba(14,14,44,.03)"
    } }, cat)), /* @__PURE__ */ React.createElement("label", { style: {
      height: mobile ? 32 : 34,
      width: mobile ? "100%" : 176,
      borderRadius: 999,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.74)",
      display: "inline-flex",
      alignItems: "center",
      gap: 7,
      padding: "0 11px",
      color: T.navyLight,
      boxShadow: "0 5px 12px rgba(14,14,44,.03), inset 0 1px 0 rgba(255,255,255,.78)"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "search", size: 13 }), /* @__PURE__ */ React.createElement(
      "input",
      {
        value: search,
        onChange: (e) => setSearch(e.target.value),
        placeholder: "\u641C\u7D22\u7075\u611F",
        style: { minWidth: 0, flex: 1, border: "none", outline: "none", background: "transparent", color: T.navy, fontSize: 12.5, fontFamily: T.fontSans }
      }
    )))), usedTitle && /* @__PURE__ */ React.createElement("div", { style: { margin: "-4px 0 10px", color: T.success, fontSize: 12, fontWeight: 650 } }, "\u5DF2\u5957\u7528\u7075\u611F\uFF1A", usedTitle), /* @__PURE__ */ React.createElement("div", { style: {
      columnCount: mobile ? 1 : compact ? 3 : 4,
      columnGap: mobile ? 14 : 16
    } }, filtered.map((item, i) => /* @__PURE__ */ React.createElement(InspirationCard, { key: `${item.title}-${i}`, item, index: i, onUse: (picked) => setDetail(picked) }))));
  };
  var HomeContentCalendar = ({ mobile, compact, onPick }) => {
    const calendar = [
      { day: "\u5468\u4E00", date: "05/18", type: "\u56FE\u6587", title: "\u7B2C\u4E00\u6B21\u6765\u5E97\u91CC\uFF0C\u5148\u70B9\u8FD9 3 \u9053\u62DB\u724C\u83DC" },
      { day: "\u5468\u4E8C", date: "05/19", type: "\u77ED\u89C6\u9891", title: "\u540E\u53A8\u5907\u83DC 30 \u79D2\uFF0C\u770B\u770B\u4E00\u7897\u996D\u600E\u4E48\u88AB\u8BA4\u771F\u505A\u597D" },
      { day: "\u5468\u4E09", date: "05/20", type: "\u56FE\u6587", title: "\u9644\u8FD1\u4E0A\u73ED\u65CF\u5348\u9910\u4E0D\u8E29\u96F7\u83DC\u5355" },
      { day: "\u5468\u56DB", date: "05/21", type: "\u957F\u6587", title: "\u4E00\u5BB6\u5C0F\u5E97\u600E\u4E48\u628A\u56DE\u5934\u5BA2\u7559\u4F4F" },
      { day: "\u5468\u4E94", date: "05/22", type: "\u77ED\u89C6\u9891", title: "\u987E\u5BA2\u6700\u5E38\u95EE\u7684 5 \u4E2A\u95EE\u9898" }
    ];
    return /* @__PURE__ */ React.createElement("section", { style: {
      width: "100%",
      maxWidth: mobile ? "100%" : compact ? 820 : 960,
      margin: "0 auto"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", gap: 14, marginBottom: 16 } }, /* @__PURE__ */ React.createElement(SectionTitle, { title: "\u5185\u5BB9\u65E5\u5386", mobile }), /* @__PURE__ */ React.createElement("button", { style: {
      border: "none",
      background: "transparent",
      color: T.navyLight,
      cursor: "pointer",
      display: "inline-flex",
      alignItems: "center",
      gap: 6,
      fontSize: 13,
      fontWeight: 620
    } }, "\u67E5\u770B\u5168\u90E8", /* @__PURE__ */ React.createElement(Icon, { name: "chevronRight", size: 14 }))), /* @__PURE__ */ React.createElement("div", { style: {
      display: "grid",
      gridTemplateColumns: mobile ? "1fr" : compact ? "repeat(2, minmax(0, 1fr))" : "repeat(5, minmax(0, 1fr))",
      gap: 14
    } }, calendar.map((item, index) => /* @__PURE__ */ React.createElement(
      "button",
      {
        key: `${item.day}-${index}`,
        onClick: () => onPick(`[\u5185\u5BB9\u65E5\u5386 \xB7 ${item.type}] ${item.title}`),
        style: {
          minHeight: mobile ? 132 : 158,
          borderRadius: 20,
          border: `1px solid ${index === 0 ? "rgba(75,77,237,.18)" : T.hairlineSoft}`,
          background: index === 0 ? "rgba(239,239,253,.60)" : "rgba(255,255,255,.78)",
          boxShadow: index === 0 ? "0 16px 34px rgba(75,77,237,.08), inset 0 1px 0 rgba(255,255,255,.78)" : "0 10px 26px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.78)",
          padding: 16,
          cursor: "pointer",
          textAlign: "left",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          gap: 14,
          transition: `transform .28s ${T.spring}, box-shadow .28s ${T.spring}, border-color .22s ${T.ease}`
        },
        onMouseEnter: (e) => {
          e.currentTarget.style.transform = "translateY(-3px)";
          e.currentTarget.style.boxShadow = "0 20px 44px rgba(14,14,44,.085), inset 0 1px 0 rgba(255,255,255,.82)";
        },
        onMouseLeave: (e) => {
          e.currentTarget.style.transform = "translateY(0)";
          e.currentTarget.style.boxShadow = index === 0 ? "0 16px 34px rgba(75,77,237,.08), inset 0 1px 0 rgba(255,255,255,.78)" : "0 10px 26px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.78)";
        }
      },
      /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 10, alignItems: "flex-start" } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 14, fontWeight: 680 } }, item.day), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 4, color: T.navyLight, fontSize: 11.5, fontFamily: T.fontMono } }, item.date)), /* @__PURE__ */ React.createElement("span", { style: {
        height: 26,
        padding: "0 9px",
        borderRadius: 999,
        background: "rgba(255,255,255,.78)",
        border: `1px solid ${T.hairlineSoft}`,
        color: index === 0 ? T.iris : T.navyLight,
        display: "inline-flex",
        alignItems: "center",
        fontSize: 11.5,
        fontWeight: 650
      } }, item.type)),
      /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 14.5, lineHeight: 1.5, fontWeight: 620 } }, item.title))
    ))));
  };
  var HomePage = ({ onSubmit, onOpenAssets, onOpenInsights, onOpenMine, onAccountPlan, accountPlanDraft, recentProject, onOpenProject, onOpenInspiration, focusInspirationKey }) => {
    const { isCompact, isTablet, isMobile } = useViewport();
    const [text, setText] = React.useState("");
    const [format, setFormat] = React.useState(null);
    const [navCollapsed, setNavCollapsed] = React.useState(false);
    const [sleepMode, setSleepMode] = React.useState(false);
    const [sleepHelp, setSleepHelp] = React.useState(false);
    const inspirationRef = React.useRef(null);
    const submit = () => {
      if (text.trim()) {
        onSubmit(format ? `[${format.label} \xB7 ${format.sub}] ${text.trim()}` : text.trim());
      }
    };
    const sessions = [
      "\u731B\u7537\u559C\u6B22\u7684\u7C89\u8272\u690D\u7269 \xB7 \u5C0F\u7EA2\u4E66\u56FE\u6587",
      "\u4E0A\u6D77\u996D\u5E97\u63A8\u8350 \xB7 \u5C0F\u7EA2\u4E66\u56FE\u6587",
      "\u4E0B\u73ED\u540E\u5C0F\u9986\u5730\u56FE",
      "\u4EA7\u54C1\u6D4B\u8BC4 \xB7 AI \u89C6\u9891\u5DE5\u5177\u6A2A\u8BC4",
      "\u6781\u7B80\u901A\u52E4\u7A7F\u642D\u4E00\u5468 OOTD",
      "\u5496\u5561\u5165\u95E8 12 \u4E2A\u540D\u8BCD",
      "\u6211\u548C\u6211\u7684\u732B \xB7 7 \u4E2A\u77AC\u95F4"
    ];
    React.useEffect(() => {
      if (!focusInspirationKey) return;
      window.setTimeout(() => inspirationRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }), 120);
    }, [focusInspirationKey]);
    return /* @__PURE__ */ React.createElement(
      "div",
      {
        onClick: () => {
          if (sleepHelp) setSleepHelp(false);
        },
        style: {
          display: "flex",
          height: "100%",
          width: "100%",
          background: "linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)",
          padding: 0
        }
      },
      /* @__PURE__ */ React.createElement("div", { style: {
        display: "flex",
        flex: 1,
        background: "transparent",
        borderRadius: 0,
        boxShadow: "none",
        overflow: "hidden"
      } }, !isTablet && /* @__PURE__ */ React.createElement(
        Sidebar,
        {
          active: "home",
          onNew: () => {
            setNavCollapsed(true);
            onSubmit("");
          },
          onNavigate: (id) => {
            if (id === "home") return;
            if (id === "library") onOpenAssets && onOpenAssets();
            if (id === "insights") onOpenInsights && onOpenInsights();
            if (id === "mine") onOpenMine && onOpenMine();
          },
          sessions,
          collapsed: navCollapsed,
          onToggle: () => setNavCollapsed((v) => !v)
        }
      ), /* @__PURE__ */ React.createElement("main", { style: {
        flex: 1,
        display: "flex",
        flexDirection: "column",
        overflow: "auto",
        position: "relative",
        background: "linear-gradient(180deg, #FFFFFF 0%, #FBFCFE 52%, #F7F9FC 100%)"
      } }, /* @__PURE__ */ React.createElement("div", { style: {
        position: "absolute",
        inset: 0,
        background: "radial-gradient(circle at 50% 8%, rgba(214,255,0,.10), transparent 18%), radial-gradient(circle at 68% 18%, rgba(75,77,237,.045), transparent 22%), radial-gradient(circle at 72% 52%, rgba(49,208,170,.035), transparent 24%)",
        pointerEvents: "none"
      } }), /* @__PURE__ */ React.createElement("div", { style: {
        height: isMobile ? 50 : 46,
        padding: isMobile ? "0 16px" : "0 22px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexShrink: 0,
        position: "relative",
        zIndex: 1
      } }, isTablet ? /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement(NoriLogo, { size: 26 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 14, fontWeight: 720, color: T.navy, letterSpacing: 0 } }, "Nori"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 10.5, color: T.navyLight } }, "creative system"))) : /* @__PURE__ */ React.createElement("div", { "aria-hidden": "true", style: { width: 38, height: 38 } }), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, position: "relative" } }, /* @__PURE__ */ React.createElement(
        "button",
        {
          onClick: (e) => {
            e.stopPropagation();
            setSleepMode((v) => !v);
            setSleepHelp((v) => !v);
          },
          style: {
            height: 36,
            borderRadius: 14,
            border: `1px solid ${sleepMode ? "rgba(75,77,237,.18)" : T.hairlineSoft}`,
            background: sleepMode ? "rgba(239,239,253,.92)" : "rgba(255,255,255,.74)",
            color: sleepMode ? T.iris : T.navyMid,
            display: "inline-flex",
            alignItems: "center",
            gap: 9,
            padding: isMobile ? "0 10px" : "0 12px",
            cursor: "pointer",
            boxShadow: sleepMode ? "0 10px 24px rgba(75,77,237,.10), inset 0 1px 0 rgba(255,255,255,.78)" : "0 6px 16px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.78)",
            backdropFilter: "blur(16px) saturate(1.18)",
            transition: `background .22s ${T.ease}, border-color .22s ${T.ease}, color .22s ${T.ease}, box-shadow .24s ${T.ease}`
          },
          "aria-pressed": sleepMode,
          "aria-label": "\u7761\u7720\u6A21\u5F0F"
        },
        /* @__PURE__ */ React.createElement(Icon, { name: "moon", size: 14, color: "currentColor" }),
        !isMobile && /* @__PURE__ */ React.createElement("span", { style: { fontSize: 12.5, fontWeight: 700 } }, "\u7761\u7720\u6A21\u5F0F"),
        /* @__PURE__ */ React.createElement("span", { style: {
          width: 30,
          height: 18,
          borderRadius: 999,
          background: sleepMode ? T.iris : "rgba(14,14,44,.12)",
          padding: 2,
          display: "inline-flex",
          justifyContent: sleepMode ? "flex-end" : "flex-start",
          flexShrink: 0
        } }, /* @__PURE__ */ React.createElement("span", { style: { width: 13, height: 13, borderRadius: "50%", background: T.white, boxShadow: "0 1px 3px rgba(14,14,44,.18)" } }))
      ), sleepHelp && /* @__PURE__ */ React.createElement(
        "div",
        {
          onClick: (e) => e.stopPropagation(),
          style: {
            position: "absolute",
            right: 78,
            top: 44,
            width: isMobile ? 260 : 318,
            padding: 14,
            borderRadius: 18,
            border: `1px solid ${T.hairlineSoft}`,
            background: "rgba(255,255,255,.94)",
            boxShadow: "0 18px 44px rgba(14,14,44,.12), inset 0 1px 0 rgba(255,255,255,.82)",
            color: T.navyMid,
            fontSize: 12.8,
            lineHeight: 1.65,
            zIndex: 20
          }
        },
        /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 13.2, fontWeight: 760, marginBottom: 6 } }, "\u7761\u7720\u6A21\u5F0F"),
        "\u5F00\u542F\u540E\uFF0CNori \u4F1A\u5728\u4F60\u4F11\u606F\u65F6\u6301\u7EED\u5B66\u4E60\u7206\u6B3E\u5185\u5BB9\u3001\u6574\u7406\u53EF\u590D\u7528 Skill\uFF0C\u5E76\u5728\u7B2C\u4E8C\u5929\u628A\u53EF\u7528\u7684\u9009\u9898\u548C\u7ED3\u6784\u653E\u8FDB\u521B\u4F5C\u5EFA\u8BAE\u3002"
      ), /* @__PURE__ */ React.createElement("button", { style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "bell", size: 15, color: T.navyLight })), /* @__PURE__ */ React.createElement("button", { style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "settings", size: 15, color: T.navyLight })))), /* @__PURE__ */ React.createElement("div", { style: {
        flex: 1,
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-start",
        maxWidth: isMobile ? "100%" : 1220,
        width: "100%",
        margin: "0 auto",
        padding: isMobile ? "14px 18px 36px" : isTablet ? "28px 46px 60px" : "44px 84px 78px",
        gap: isMobile ? 34 : 62,
        position: "relative",
        zIndex: 1
      } }, /* @__PURE__ */ React.createElement("section", { style: {
        position: "relative",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: isMobile ? "10px 0 0" : "24px 0 0"
      } }, /* @__PURE__ */ React.createElement(HeroHeadline, { compact: isCompact, mobile: isMobile }), /* @__PURE__ */ React.createElement("div", { style: { width: "100%", maxWidth: isMobile ? "100%" : 820 } }, /* @__PURE__ */ React.createElement(
        HomeIpModeBar,
        {
          mobile: isMobile,
          onAccountPlan,
          onViewProfile: onOpenMine,
          planned: !!accountPlanDraft
        }
      ), /* @__PURE__ */ React.createElement(
        HomeComposer,
        {
          value: text,
          onChange: setText,
          onSubmit: submit,
          format,
          onClearFormat: () => setFormat(null),
          compact: isCompact,
          mobile: isMobile
        }
      ), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 14, display: "flex", justifyContent: "center" } }, /* @__PURE__ */ React.createElement(FormatPicker, { format, onPick: setFormat, compact: isCompact, mobile: isMobile })))), /* @__PURE__ */ React.createElement(HomeContentCalendar, { mobile: isMobile, compact: isCompact, onPick: onSubmit }), /* @__PURE__ */ React.createElement("div", { ref: inspirationRef }, /* @__PURE__ */ React.createElement(InspirationDiscovery, { mobile: isMobile, compact: isCompact, onUseInspiration: onOpenInspiration })))))
    );
  };
  var iconBtnStyle = () => ({
    width: 34,
    height: 34,
    borderRadius: 12,
    border: `1px solid ${T.hairlineSoft}`,
    background: "rgba(255,255,255,.74)",
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    transition: `transform .28s ${T.spring}, box-shadow .28s ${T.spring}, background .22s ${T.ease}`,
    boxShadow: "0 6px 16px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.78)",
    backdropFilter: "blur(16px) saturate(1.18)"
  });
  window.HomePage = HomePage;
  window.Sidebar = Sidebar;
  window.iconBtnStyle = iconBtnStyle;
  var ASSET_ITEMS = [
    {
      id: "pink-plants",
      title: "\u6DF1\u84DD\u5E55\u5E03\u4E0B\u7684\u7C89\u8776\u5170\uFF0C\u8C01\u61C2\u8FD9\u79CD\u53CD\u5DEE\u611F\uFF1F",
      platform: "\u5C0F\u7EA2\u4E66",
      type: "\u56FE\u6587",
      time: "\u4ECA\u5929 21:18",
      status: "\u5DF2\u751F\u6210",
      height: 214,
      palette: ["#103f5f", "#1d6f58", "#f4a8bf", "#de7fa3", "#fff8fb"],
      tags: ["\u7C89\u8272\u690D\u7269", "\u5BA4\u5185\u7EFF\u690D"]
    },
    {
      id: "coffee-walk",
      title: "\u4E0A\u6D77\u5496\u5561\u9986 City Walk Top 10 \u8DEF\u7EBF",
      platform: "\u5C0F\u7EA2\u4E66",
      type: "\u89C6\u9891",
      time: "\u6628\u5929 18:42",
      status: "\u8349\u7A3F",
      height: 258,
      palette: ["#d9d0bd", "#7c6b58", "#f3e7d7", "#a47758", "#fffaf2"],
      tags: ["\u57CE\u5E02\u6F2B\u6B65", "\u5496\u5561\u9986"]
    },
    {
      id: "rental-guide",
      title: "\u79DF\u623F\u907F\u96F7\u6307\u5357\uFF1A\u770B\u623F\u524D\u5FC5\u987B\u95EE\u6E05\u695A\u7684 18 \u4EF6\u4E8B",
      platform: "\u516C\u4F17\u53F7",
      type: "\u7EAF\u6587\u5B57",
      time: "5 \u6708 5 \u65E5",
      status: "\u5DF2\u53D1\u5E03",
      height: 184,
      palette: ["#f7f9fc", "#d7e0eb", "#4b4ded", "#31d0aa", "#0e0e2c"],
      tags: ["\u751F\u6D3B\u7ECF\u9A8C", "\u6E05\u5355"]
    },
    {
      id: "ai-video-tools",
      title: "AI \u89C6\u9891\u5DE5\u5177\u6A2A\u8BC4\uFF1A\u4ECE\u811A\u672C\u5230\u6210\u7247\u7684\u771F\u5B9E\u4F53\u9A8C",
      platform: "B\u7AD9",
      type: "\u89C6\u9891",
      time: "5 \u6708 4 \u65E5",
      status: "\u5DF2\u751F\u6210",
      height: 244,
      palette: ["#20284a", "#5c66a8", "#f3dbda", "#d6ff00", "#ffffff"],
      tags: ["AI\u5DE5\u5177", "\u6D4B\u8BC4"]
    },
    {
      id: "ootd",
      title: "\u6781\u7B80\u901A\u52E4\u7A7F\u642D\u4E00\u5468 OOTD",
      platform: "\u77ED\u89C6\u9891",
      type: "\u89C6\u9891",
      time: "5 \u6708 3 \u65E5",
      status: "\u8349\u7A3F",
      height: 268,
      palette: ["#e8ebee", "#1d2330", "#b8c2cb", "#f3dbda", "#ffffff"],
      tags: ["\u7A7F\u642D", "\u901A\u52E4"]
    },
    {
      id: "coffee-terms",
      title: "\u5496\u5561\u5165\u95E8 12 \u4E2A\u540D\u8BCD\uFF0C\u4E00\u6B21\u8BB2\u6E05\u695A",
      platform: "\u516C\u4F17\u53F7",
      type: "\u7EAF\u6587\u5B57",
      time: "5 \u6708 2 \u65E5",
      status: "\u5DF2\u751F\u6210",
      height: 178,
      palette: ["#fffaf2", "#efe1cc", "#8a6545", "#31d0aa", "#0e0e2c"],
      tags: ["\u77E5\u8BC6\u79D1\u666E", "\u5496\u5561"]
    },
    {
      id: "cat-moments",
      title: "\u6211\u548C\u6211\u7684\u732B\uFF1A7 \u4E2A\u9002\u5408\u53D1\u56FE\u6587\u7684\u751F\u6D3B\u77AC\u95F4",
      platform: "\u5C0F\u7EA2\u4E66",
      type: "\u56FE\u6587",
      time: "4 \u6708 29 \u65E5",
      status: "\u5DF2\u53D1\u5E03",
      height: 222,
      palette: ["#fdf5f5", "#95a5a6", "#f0b5c8", "#4b4ded", "#ffffff"],
      tags: ["\u751F\u6D3B\u8BB0\u5F55", "\u5BA0\u7269"]
    },
    {
      id: "product-manager",
      title: "2026 \u5E74 AI \u4EA7\u54C1\u7ECF\u7406\u5FC5\u5907\u80FD\u529B\u5730\u56FE",
      platform: "\u516C\u4F17\u53F7",
      type: "\u56FE\u6587",
      time: "4 \u6708 26 \u65E5",
      status: "\u5DF2\u751F\u6210",
      height: 202,
      palette: ["#ecf1f4", "#c8d8e6", "#4b4ded", "#d6ff00", "#0e0e2c"],
      tags: ["\u804C\u573A", "AI"]
    },
    {
      id: "launch-copy",
      title: "\u65B0\u54C1\u53D1\u5E03\u6587\u6848\uFF1A\u4ECE\u9884\u70ED\u5230\u8F6C\u5316\u7684 5 \u4E2A\u7248\u672C",
      platform: "\u5C0F\u7EA2\u4E66",
      type: "\u7EAF\u6587\u5B57",
      time: "4 \u6708 22 \u65E5",
      status: "\u8349\u7A3F",
      height: 188,
      palette: ["#ffffff", "#efeefd", "#4b4ded", "#f3dbda", "#0e0e2c"],
      tags: ["\u8425\u9500\u6587\u6848", "\u53D1\u5E03"]
    }
  ];
  var AssetVisual = ({ item }) => {
    if (item.type === "\u7EAF\u6587\u5B57") {
      return /* @__PURE__ */ React.createElement("div", { style: {
        height: 178,
        padding: 14,
        background: `linear-gradient(145deg, ${item.palette[0]}, ${item.palette[1]})`,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between"
      } }, /* @__PURE__ */ React.createElement("div", { style: {
        width: 30,
        height: 30,
        borderRadius: 10,
        background: "rgba(255,255,255,.82)",
        color: item.palette[2],
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        boxShadow: "inset 0 1px 0 rgba(255,255,255,.72)"
      } }, /* @__PURE__ */ React.createElement(Icon, { name: "document", size: 13 })), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 16.5, lineHeight: 1.24, fontWeight: 740, color: T.navy, letterSpacing: 0 } }, item.title)));
    }
    return /* @__PURE__ */ React.createElement("div", { style: { height: 178, position: "relative", overflow: "hidden", background: item.palette[0] } }, /* @__PURE__ */ React.createElement(FlowerVisual, { palette: item.palette }), /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      inset: 0,
      background: item.type === "\u89C6\u9891" ? "linear-gradient(180deg, rgba(0,0,0,.02), rgba(0,0,0,.44))" : "linear-gradient(180deg, rgba(255,255,255,.04), rgba(0,0,0,.32))"
    } }), item.type === "\u89C6\u9891" && /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      left: 12,
      top: 12,
      width: 32,
      height: 32,
      borderRadius: "50%",
      background: "rgba(255,255,255,.86)",
      color: T.navy,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      boxShadow: "0 10px 22px rgba(14,14,44,.14)",
      backdropFilter: "blur(10px)"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "play", size: 12 })), /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      left: 13,
      right: 13,
      bottom: 13,
      color: T.white
    } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 16.5, lineHeight: 1.18, fontWeight: 760, letterSpacing: 0, textShadow: "0 2px 10px rgba(0,0,0,.24)" } }, item.title)));
  };
  var assetStatusTone = (status) => {
    if (status === "\u5DF2\u53D1\u5E03") return { bg: T.successTint, fg: T.success };
    if (status === "\u8349\u7A3F") return { bg: T.irisTint, fg: T.iris };
    return { bg: T.primaryTint, fg: T.navy };
  };
  var FilterChip = ({ active, children, onClick, count }) => /* @__PURE__ */ React.createElement(
    "button",
    {
      onClick,
      style: {
        height: 34,
        padding: "0 12px",
        borderRadius: 12,
        border: `1px solid ${active ? "rgba(75,77,237,.16)" : T.hairlineSoft}`,
        background: active ? T.irisTint : "rgba(255,255,255,.76)",
        color: active ? T.iris : T.navyMid,
        boxShadow: active ? "0 7px 18px rgba(75,77,237,.08), inset 0 1px 0 rgba(255,255,255,.78)" : "none",
        cursor: "pointer",
        fontSize: 12.5,
        fontWeight: 700,
        display: "inline-flex",
        alignItems: "center",
        gap: 7,
        transition: `transform .28s ${T.spring}, background .22s ${T.ease}, box-shadow .28s ${T.spring}, color .22s ${T.ease}`
      },
      onMouseEnter: (e) => {
        e.currentTarget.style.transform = "translateY(-1px)";
        e.currentTarget.style.boxShadow = active ? T.shadowSm : T.shadowXs;
      },
      onMouseLeave: (e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.boxShadow = active ? "inset 0 1px 0 rgba(255,255,255,.78)" : "none";
      }
    },
    children,
    typeof count === "number" && /* @__PURE__ */ React.createElement("span", { style: {
      minWidth: 20,
      height: 20,
      padding: "0 6px",
      borderRadius: 999,
      background: active ? "rgba(75,77,237,.12)" : T.surface,
      color: active ? T.iris : T.navyLight,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: 10.5,
      fontFamily: T.fontMono
    } }, count)
  );
  var AssetCard = ({ item, index, onOpen }) => /* @__PURE__ */ React.createElement(
    "article",
    {
      onClick: () => onOpen(item),
      style: {
        breakInside: "avoid",
        marginBottom: 14,
        borderRadius: 16,
        overflow: "hidden",
        minHeight: 286,
        background: "rgba(255,255,255,.86)",
        border: `1px solid ${T.hairlineSoft}`,
        boxShadow: "0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)",
        cursor: "pointer",
        position: "relative",
        animation: `fadeInScale .5s ${index * 48}ms ${T.spring} both`,
        transition: `transform .34s ${T.spring}, box-shadow .34s ${T.spring}`
      },
      onMouseEnter: (e) => {
        e.currentTarget.style.transform = "translateY(-3px)";
        e.currentTarget.style.boxShadow = "0 16px 38px rgba(14,14,44,.095), inset 0 1px 0 rgba(255,255,255,.76)";
      },
      onMouseLeave: (e) => {
        e.currentTarget.style.transform = "translateY(0)";
        e.currentTarget.style.boxShadow = "0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)";
      }
    },
    /* @__PURE__ */ React.createElement(AssetVisual, { item }),
    /* @__PURE__ */ React.createElement("div", { style: { padding: "10px 12px 11px" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "inline-flex", alignItems: "center", gap: 7, minWidth: 0 } }, /* @__PURE__ */ React.createElement(PlatformLogo, { kind: item.platform === "\u5C0F\u7EA2\u4E66" ? "xhs" : item.platform === "B\u7AD9" ? "bili" : item.platform === "\u77ED\u89C6\u9891" ? "dy" : "wechat", size: 19 }), /* @__PURE__ */ React.createElement("span", { style: { color: T.navy, fontSize: 13, lineHeight: 1.2, fontWeight: 720, whiteSpace: "nowrap" } }, item.platform)), /* @__PURE__ */ React.createElement("span", { style: {
      height: 24,
      padding: "0 9px",
      borderRadius: 999,
      background: assetStatusTone(item.status).bg,
      color: assetStatusTone(item.status).fg,
      fontSize: 11.5,
      fontWeight: 760,
      display: "inline-flex",
      alignItems: "center",
      flexShrink: 0
    } }, item.status)), /* @__PURE__ */ React.createElement("div", { style: {
      marginTop: 8,
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: 10,
      color: T.navyLight,
      fontSize: 12.2,
      lineHeight: 1.35
    } }, /* @__PURE__ */ React.createElement("span", null, item.time)))
  );
  var AssetsPage = ({ onOpenAsset, onBackHome, onOpenInsights, onOpenMine, onNewChat }) => {
    const { width, isTablet, isMobile } = useViewport();
    const [navCollapsed, setNavCollapsed] = React.useState(false);
    const [query, setQuery] = React.useState("");
    const [platform, setPlatform] = React.useState("\u5168\u90E8");
    const [type, setType] = React.useState("\u5168\u90E8");
    const [sort, setSort] = React.useState("\u6700\u65B0");
    const columnCount = isMobile ? 1 : isTablet ? 2 : Math.min(6, Math.max(4, Math.floor((width - (navCollapsed ? 132 : 292)) / 214)));
    const sessions = ASSET_ITEMS.slice(0, 6).map((item) => item.title);
    const filtered = ASSET_ITEMS.filter((item) => platform === "\u5168\u90E8" || item.platform === platform).filter((item) => type === "\u5168\u90E8" || item.type === type).filter((item) => !query.trim() || `${item.title} ${item.platform} ${item.type} ${item.tags.join(" ")}`.toLowerCase().includes(query.trim().toLowerCase()));
    const sorted = sort === "\u6700\u65E9" ? [...filtered].reverse() : filtered;
    const platforms = ["\u5168\u90E8", "\u5C0F\u7EA2\u4E66", "\u516C\u4F17\u53F7", "B\u7AD9", "\u77ED\u89C6\u9891"];
    const types = ["\u5168\u90E8", "\u56FE\u6587", "\u89C6\u9891", "\u7EAF\u6587\u5B57"];
    return /* @__PURE__ */ React.createElement("div", { style: { display: "flex", width: "100%", height: "100%", background: T.surfaceWh, overflow: "hidden" } }, !isTablet && /* @__PURE__ */ React.createElement(
      Sidebar,
      {
        active: "library",
        onNew: onNewChat,
        onNavigate: (id) => {
          if (id === "home") onBackHome();
          if (id === "insights") onOpenInsights && onOpenInsights();
          if (id === "mine") onOpenMine && onOpenMine();
        },
        sessions,
        collapsed: navCollapsed,
        onToggle: () => setNavCollapsed((v) => !v)
      }
    ), /* @__PURE__ */ React.createElement("main", { style: {
      flex: 1,
      minWidth: 0,
      overflow: "auto",
      background: "linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)",
      position: "relative"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      inset: 0,
      background: "radial-gradient(circle at 18% 12%, rgba(214,255,0,.16), transparent 18%), radial-gradient(circle at 86% 10%, rgba(75,77,237,.08), transparent 22%), radial-gradient(circle at 64% 72%, rgba(49,208,170,.07), transparent 22%)",
      pointerEvents: "none"
    } }), /* @__PURE__ */ React.createElement("div", { style: { position: "relative", zIndex: 1, maxWidth: 1640, margin: "0 auto", padding: isMobile ? "18px 18px 36px" : "28px 30px 50px" } }, isTablet && /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement(NoriLogo, { size: 28 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 15, fontWeight: 760, color: T.navy } }, "\u6211\u7684\u5185\u5BB9\u5E93"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11, color: T.navyLight } }, "\u81EA\u52A8\u4FDD\u5B58\u7684\u521B\u4F5C\u8D44\u4EA7"))), /* @__PURE__ */ React.createElement("button", { onClick: onBackHome, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "home", size: 16, color: T.navyMid }))), /* @__PURE__ */ React.createElement("header", { style: {
      display: "flex",
      alignItems: "flex-start",
      justifyContent: "space-between",
      gap: 22,
      marginBottom: 24,
      flexWrap: "wrap"
    } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12, fontWeight: 800, letterSpacing: "0.08em", textTransform: "uppercase", color: T.navyLight, marginBottom: 8 } }, "Assets"), /* @__PURE__ */ React.createElement("h1", { style: { margin: 0, fontSize: isMobile ? 28 : 38, lineHeight: 1.08, letterSpacing: 0, color: T.navy, fontWeight: 760 } }, "\u6211\u7684\u5185\u5BB9\u5E93"), /* @__PURE__ */ React.createElement("p", { style: { margin: "10px 0 0", fontSize: 13.5, lineHeight: 1.6, color: T.navyMid } }, "\u751F\u6210\u8FC7\u7684\u56FE\u6587\u3001\u89C6\u9891\u548C\u6587\u6848\u4F1A\u81EA\u52A8\u4FDD\u5B58\uFF0C\u968F\u65F6\u67E5\u770B\u3001\u7F16\u8F91\u3001\u91CD\u65B0\u53D1\u5E03\u6216\u8F6C\u6362\u5F62\u6001\u3002")), /* @__PURE__ */ React.createElement("div", { style: {
      display: "flex",
      alignItems: "center",
      gap: 10,
      flexWrap: "wrap",
      justifyContent: isMobile ? "flex-start" : "flex-end",
      width: isMobile ? "100%" : "auto"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      height: 46,
      minWidth: isMobile ? "100%" : 300,
      borderRadius: 16,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.82)",
      boxShadow: "0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.78)",
      display: "flex",
      alignItems: "center",
      gap: 10,
      padding: "0 14px",
      backdropFilter: "blur(18px)"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "search", size: 17, color: T.navyLight }), /* @__PURE__ */ React.createElement(
      "input",
      {
        value: query,
        onChange: (e) => setQuery(e.target.value),
        placeholder: "\u641C\u7D22\u5185\u5BB9\u8D44\u4EA7...",
        style: {
          flex: 1,
          border: "none",
          outline: "none",
          background: "transparent",
          color: T.navy,
          fontSize: 14,
          fontFamily: T.fontSans
        }
      }
    )), /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: () => setSort((s) => s === "\u6700\u65B0" ? "\u6700\u65E9" : "\u6700\u65B0"),
        style: {
          height: 46,
          padding: "0 16px",
          borderRadius: 16,
          border: `1px solid ${T.hairlineSoft}`,
          background: "rgba(255,255,255,.82)",
          boxShadow: "0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.78)",
          color: T.navy,
          cursor: "pointer",
          display: "inline-flex",
          alignItems: "center",
          gap: 9,
          fontSize: 13.5,
          fontWeight: 740
        }
      },
      /* @__PURE__ */ React.createElement(Icon, { name: "list", size: 16, color: T.navyMid }),
      sort
    ))), /* @__PURE__ */ React.createElement("section", { style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: 12,
      flexWrap: "wrap",
      paddingBottom: 18,
      borderBottom: `1px solid ${T.hairlineSoft}`,
      marginBottom: 24
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" } }, platforms.map((p) => /* @__PURE__ */ React.createElement(
      FilterChip,
      {
        key: p,
        active: platform === p,
        onClick: () => setPlatform(p),
        count: p === "\u5168\u90E8" ? ASSET_ITEMS.length : ASSET_ITEMS.filter((item) => item.platform === p).length
      },
      p
    ))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" } }, types.map((t) => /* @__PURE__ */ React.createElement(
      FilterChip,
      {
        key: t,
        active: type === t,
        onClick: () => setType(t)
      },
      t
    )))), /* @__PURE__ */ React.createElement("section", { style: {
      columnCount,
      columnGap: 14
    } }, sorted.map((item, index) => /* @__PURE__ */ React.createElement(AssetCard, { key: item.id, item, index, onOpen: onOpenAsset }))), sorted.length === 0 && /* @__PURE__ */ React.createElement("div", { style: {
      minHeight: 280,
      borderRadius: 22,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.72)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      color: T.navyLight,
      fontSize: 13.5,
      boxShadow: T.shadowXs
    } }, "\u6CA1\u6709\u627E\u5230\u5339\u914D\u7684\u5185\u5BB9\u8D44\u4EA7"))));
  };
  window.AssetsPage = AssetsPage;
  var SKILL_ITEMS = [
    {
      id: "xhs-viral-note",
      owner: "community",
      title: "\u5C0F\u7EA2\u4E66\u7206\u6B3E\u56FE\u6587\u62C6\u89E3\u5668",
      type: "\u5C0F\u7EA2\u4E66\u56FE\u6587",
      uses: "12.8k",
      height: 278,
      accent: T.iris,
      tint: T.irisTint,
      palette: ["#efeefd", "#4b4ded", "#d6ff00", "#f3dbda", "#0e0e2c"],
      desc: "\u628A\u4E00\u4E2A\u666E\u901A\u9009\u9898\u62C6\u6210\u6807\u9898\u94A9\u5B50\u3001\u5C01\u9762\u7ED3\u6784\u3001\u6B63\u6587\u8282\u594F\u548C\u8BC4\u8BBA\u533A\u5F15\u5BFC\uFF0C\u9002\u5408\u751F\u6D3B\u65B9\u5F0F\u3001\u6D4B\u8BC4\u548C\u77E5\u8BC6\u7C7B\u56FE\u6587\u3002",
      prompt: "\u4F7F\u7528\u300C\u5C0F\u7EA2\u4E66\u7206\u6B3E\u56FE\u6587\u62C6\u89E3\u5668\u300D\uFF1A\u8BF7\u57FA\u4E8E\u6211\u63A5\u4E0B\u6765\u8F93\u5165\u7684\u4E3B\u9898\uFF0C\u751F\u6210\u5C0F\u7EA2\u4E66\u56FE\u6587\u5185\u5BB9\u3002\u8BF7\u5305\u542B\u6807\u9898\u5907\u9009\u3001\u5C01\u9762\u6587\u6848\u3001\u6B63\u6587\u7ED3\u6784\u3001\u6807\u7B7E\u548C\u8BC4\u8BBA\u533A\u4E92\u52A8\u95EE\u9898\u3002\u4E3B\u9898\uFF1A",
      result: ["3 \u7EC4\u6807\u9898\u65B9\u5411", "\u5C01\u9762\u89C6\u89C9\u811A\u672C", "\u6B63\u6587 6 \u6BB5\u7ED3\u6784", "\u53D1\u5E03\u6807\u7B7E"]
    },
    {
      id: "longform-editorial",
      owner: "community",
      title: "\u516C\u4F17\u53F7\u957F\u6587\u7F16\u8F91\u53F0",
      type: "\u516C\u4F17\u53F7\u957F\u6587",
      uses: "8.4k",
      height: 326,
      accent: T.success,
      tint: T.successTint,
      palette: ["#e0faf4", "#31d0aa", "#0e0e2c", "#d6ff00", "#ffffff"],
      desc: "\u5C06\u96F6\u6563\u89C2\u70B9\u6574\u7406\u6210\u6709\u5F00\u5934\u3001\u6709\u8BBA\u8BC1\u3001\u6709\u6848\u4F8B\u3001\u6709\u7ED3\u5C3E\u7684\u516C\u4F17\u53F7\u957F\u6587\uFF0C\u9002\u5408\u884C\u4E1A\u89C2\u70B9\u3001\u4EA7\u54C1\u601D\u8003\u548C\u6DF1\u5EA6\u590D\u76D8\u3002",
      prompt: "\u4F7F\u7528\u300C\u516C\u4F17\u53F7\u957F\u6587\u7F16\u8F91\u53F0\u300D\uFF1A\u8BF7\u628A\u6211\u8F93\u5165\u7684\u4E3B\u9898\u6269\u5C55\u4E3A\u516C\u4F17\u53F7\u957F\u6587\u3002\u8BF7\u5148\u7ED9\u6587\u7AE0\u5927\u7EB2\uFF0C\u518D\u5199\u5B8C\u6574\u6B63\u6587\uFF0C\u5E76\u52A0\u5165\u5C0F\u6807\u9898\u3001\u6848\u4F8B\u548C\u7ED3\u5C3E\u884C\u52A8\u5EFA\u8BAE\u3002\u4E3B\u9898\uFF1A",
      result: ["\u6587\u7AE0\u5927\u7EB2", "\u5B8C\u6574\u957F\u6587", "\u5C0F\u6807\u9898\u4F18\u5316", "\u7ED3\u5C3E CTA"]
    },
    {
      id: "short-video-script",
      owner: "community",
      title: "\u77ED\u89C6\u9891 60 \u79D2\u53E3\u64AD\u811A\u672C",
      type: "\u77ED\u89C6\u9891",
      uses: "15.2k",
      height: 296,
      accent: "#a35a62",
      tint: T.peachTint,
      palette: ["#fdf5f5", "#f3dbda", "#0e0e2c", "#4b4ded", "#ffffff"],
      desc: "\u5C06\u89C2\u70B9\u538B\u7F29\u6210 60 \u79D2\u77ED\u89C6\u9891\u811A\u672C\uFF0C\u81EA\u52A8\u62C6\u5206\u524D\u4E09\u79D2\u94A9\u5B50\u3001\u53E3\u64AD\u3001\u8F6C\u573A\u548C\u7ED3\u5C3E\u5173\u6CE8\u7406\u7531\u3002",
      prompt: "\u4F7F\u7528\u300C\u77ED\u89C6\u9891 60 \u79D2\u53E3\u64AD\u811A\u672C\u300D\uFF1A\u8BF7\u57FA\u4E8E\u4E3B\u9898\u751F\u6210 60 \u79D2\u77ED\u89C6\u9891\u811A\u672C\uFF0C\u5305\u542B\u524D\u4E09\u79D2\u94A9\u5B50\u3001\u5206\u955C\u3001\u53E3\u64AD\u7A3F\u3001\u5B57\u5E55\u91CD\u70B9\u548C\u7ED3\u5C3E\u5173\u6CE8\u5F15\u5BFC\u3002\u4E3B\u9898\uFF1A",
      result: ["\u53E3\u64AD\u7A3F", "\u5206\u955C\u8282\u594F", "\u5B57\u5E55\u91CD\u70B9", "\u5C01\u9762\u6807\u9898"]
    },
    {
      id: "product-review",
      owner: "community",
      title: "\u4EA7\u54C1\u6D4B\u8BC4\u5BF9\u6BD4\u6A21\u677F",
      type: "\u5C0F\u7EA2\u4E66\u56FE\u6587",
      uses: "6.9k",
      height: 248,
      accent: T.navy,
      tint: T.surface,
      palette: ["#ecf1f4", "#c4c4d4", "#4b4ded", "#d6ff00", "#0e0e2c"],
      desc: "\u628A\u591A\u4E2A\u4EA7\u54C1\u6574\u7406\u6210\u7EF4\u5EA6\u6E05\u6670\u7684\u6A2A\u8BC4\u5361\u7247\uFF0C\u81EA\u52A8\u751F\u6210\u4F18\u7F3A\u70B9\u3001\u9002\u5408\u4EBA\u7FA4\u548C\u8D2D\u4E70\u5EFA\u8BAE\u3002",
      prompt: "\u4F7F\u7528\u300C\u4EA7\u54C1\u6D4B\u8BC4\u5BF9\u6BD4\u6A21\u677F\u300D\uFF1A\u8BF7\u6839\u636E\u6211\u8F93\u5165\u7684\u4EA7\u54C1\u6216\u5DE5\u5177\uFF0C\u751F\u6210\u6A2A\u8BC4\u5185\u5BB9\uFF0C\u5305\u542B\u5BF9\u6BD4\u7EF4\u5EA6\u3001\u4F18\u7F3A\u70B9\u3001\u9002\u5408\u4EBA\u7FA4\u3001\u7ED3\u8BBA\u548C\u63A8\u8350\u6392\u5E8F\u3002\u4EA7\u54C1\uFF1A",
      result: ["\u5BF9\u6BD4\u7EF4\u5EA6", "\u4F18\u7F3A\u70B9", "\u63A8\u8350\u6392\u5E8F", "\u8D2D\u4E70\u5EFA\u8BAE"]
    },
    {
      id: "personal-brand",
      owner: "mine",
      title: "\u4E2A\u4EBA IP \u65E5\u5E38\u5185\u5BB9\u7CFB\u7EDF",
      type: "\u5C0F\u7EA2\u4E66\u56FE\u6587",
      uses: "1.1k",
      height: 310,
      accent: T.iris,
      tint: T.irisTint,
      palette: ["#fafcfe", "#efeefd", "#4b4ded", "#f3dbda", "#0e0e2c"],
      desc: "\u4ECE\u65E5\u5E38\u7ECF\u5386\u91CC\u63D0\u70BC\u89C2\u70B9\uFF0C\u751F\u6210\u9002\u5408\u4E2A\u4EBA\u54C1\u724C\u7684\u56FE\u6587\u5185\u5BB9\uFF0C\u9002\u5408\u521B\u4F5C\u8005\u3001\u54A8\u8BE2\u5E08\u548C\u72EC\u7ACB\u5DE5\u4F5C\u8005\u3002",
      prompt: "\u4F7F\u7528\u300C\u4E2A\u4EBA IP \u65E5\u5E38\u5185\u5BB9\u7CFB\u7EDF\u300D\uFF1A\u8BF7\u628A\u6211\u8F93\u5165\u7684\u4E00\u6BB5\u65E5\u5E38\u7ECF\u5386\u63D0\u70BC\u6210\u4E2A\u4EBA\u54C1\u724C\u5185\u5BB9\uFF0C\u5305\u542B\u89C2\u70B9\u3001\u6545\u4E8B\u3001\u53CD\u601D\u3001\u6807\u9898\u548C\u4E92\u52A8\u95EE\u9898\u3002\u7ECF\u5386\uFF1A",
      result: ["\u6545\u4E8B\u94A9\u5B50", "\u4E2A\u4EBA\u89C2\u70B9", "\u6807\u9898\u7EC4", "\u4E92\u52A8\u95EE\u9898"]
    },
    {
      id: "launch-campaign",
      owner: "mine",
      title: "\u65B0\u54C1\u53D1\u5E03\u8282\u594F\u89C4\u5212",
      type: "\u516C\u4F17\u53F7\u957F\u6587",
      uses: "860",
      height: 270,
      accent: T.success,
      tint: T.successTint,
      palette: ["#e0faf4", "#31d0aa", "#f3dbda", "#d6ff00", "#0e0e2c"],
      desc: "\u4E3A\u65B0\u54C1\u53D1\u5E03\u81EA\u52A8\u89C4\u5212\u9884\u70ED\u3001\u53D1\u5E03\u3001\u590D\u76D8\u4E09\u4E2A\u9636\u6BB5\u7684\u5185\u5BB9\u8282\u594F\u548C\u6BCF\u6761\u5185\u5BB9\u7684\u4E3B\u4FE1\u606F\u3002",
      prompt: "\u4F7F\u7528\u300C\u65B0\u54C1\u53D1\u5E03\u8282\u594F\u89C4\u5212\u300D\uFF1A\u8BF7\u57FA\u4E8E\u6211\u7684\u65B0\u54C1\u4FE1\u606F\uFF0C\u8BBE\u8BA1\u4E00\u5957\u53D1\u5E03\u5185\u5BB9\u8282\u594F\uFF0C\u5305\u542B\u9884\u70ED\u3001\u53D1\u5E03\u3001\u590D\u76D8\u9636\u6BB5\uFF0C\u6BCF\u9636\u6BB5\u7ED9\u51FA\u5185\u5BB9\u4E3B\u9898\u548C\u6587\u6848\u65B9\u5411\u3002\u65B0\u54C1\uFF1A",
      result: ["\u53D1\u5E03\u8282\u594F", "\u5185\u5BB9\u4E3B\u9898", "\u6587\u6848\u65B9\u5411", "\u590D\u76D8\u6307\u6807"]
    },
    {
      id: "knowledge-card",
      owner: "community",
      title: "\u77E5\u8BC6\u5361\u7247\u7CFB\u5217\u751F\u6210\u5668",
      type: "\u5C0F\u7EA2\u4E66\u56FE\u6587",
      uses: "9.7k",
      height: 286,
      accent: T.primary,
      tint: T.primaryTint,
      palette: ["#f5ffe0", "#d6ff00", "#0e0e2c", "#4b4ded", "#ffffff"],
      desc: "\u628A\u4E00\u4E2A\u77E5\u8BC6\u70B9\u62C6\u6210 6-9 \u5F20\u5361\u7247\uFF0C\u6BCF\u5F20\u5361\u7247\u90FD\u6709\u6807\u9898\u3001\u91CD\u70B9\u53E5\u548C\u89C6\u89C9\u5EFA\u8BAE\u3002",
      prompt: "\u4F7F\u7528\u300C\u77E5\u8BC6\u5361\u7247\u7CFB\u5217\u751F\u6210\u5668\u300D\uFF1A\u8BF7\u628A\u6211\u8F93\u5165\u7684\u77E5\u8BC6\u4E3B\u9898\u62C6\u6210\u4E00\u7EC4\u56FE\u6587\u5361\u7247\uFF0C\u5305\u542B\u6BCF\u5F20\u5361\u7247\u6807\u9898\u3001\u91CD\u70B9\u53E5\u3001\u89C6\u89C9\u5EFA\u8BAE\u548C\u7ED3\u5C3E\u603B\u7ED3\u3002\u4E3B\u9898\uFF1A",
      result: ["\u5361\u7247\u5927\u7EB2", "\u91CD\u70B9\u53E5", "\u89C6\u89C9\u5EFA\u8BAE", "\u603B\u7ED3\u9875"]
    },
    {
      id: "case-study",
      owner: "community",
      title: "\u6848\u4F8B\u590D\u76D8\u957F\u6587\u6846\u67B6",
      type: "\u516C\u4F17\u53F7\u957F\u6587",
      uses: "5.3k",
      height: 336,
      accent: T.navy,
      tint: T.surface,
      palette: ["#f8fbfd", "#ecf1f4", "#0e0e2c", "#31d0aa", "#4b4ded"],
      desc: "\u628A\u9879\u76EE\u7ECF\u5386\u6574\u7406\u6210\u80CC\u666F\u3001\u52A8\u4F5C\u3001\u7ED3\u679C\u3001\u590D\u76D8\u3001\u53EF\u590D\u7528\u7ECF\u9A8C\u7684\u5B8C\u6574\u6848\u4F8B\u6587\u7AE0\u3002",
      prompt: "\u4F7F\u7528\u300C\u6848\u4F8B\u590D\u76D8\u957F\u6587\u6846\u67B6\u300D\uFF1A\u8BF7\u628A\u6211\u7684\u9879\u76EE\u7ECF\u5386\u6574\u7406\u6210\u6848\u4F8B\u590D\u76D8\u6587\u7AE0\uFF0C\u5305\u542B\u80CC\u666F\u3001\u76EE\u6807\u3001\u5173\u952E\u52A8\u4F5C\u3001\u7ED3\u679C\u6570\u636E\u3001\u5931\u8D25\u70B9\u548C\u53EF\u590D\u7528\u7ECF\u9A8C\u3002\u9879\u76EE\uFF1A",
      result: ["\u6848\u4F8B\u7ED3\u6784", "\u590D\u76D8\u95EE\u9898", "\u7ED3\u679C\u8868\u8FBE", "\u7ECF\u9A8C\u63D0\u70BC"]
    }
  ];
  var SkillArtwork = ({ skill, compact = false }) => /* @__PURE__ */ React.createElement("div", { style: {
    height: compact ? "auto" : skill.height,
    aspectRatio: compact ? "1 / 1" : "auto",
    position: "relative",
    overflow: "hidden",
    background: `linear-gradient(145deg, ${skill.palette[0]}, ${skill.palette[1]})`,
    borderRadius: compact ? 18 : 0
  } }, /* @__PURE__ */ React.createElement("div", { style: {
    position: "absolute",
    inset: 0,
    background: "radial-gradient(circle at 26% 20%, rgba(255,255,255,.72), transparent 24%), radial-gradient(circle at 80% 14%, rgba(255,255,255,.34), transparent 22%), radial-gradient(circle at 72% 78%, rgba(14,14,44,.10), transparent 30%)"
  } }), /* @__PURE__ */ React.createElement("div", { style: {
    position: "absolute",
    left: 18,
    top: 18,
    width: 42,
    height: 42,
    borderRadius: 15,
    background: "rgba(255,255,255,.78)",
    color: skill.accent,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    boxShadow: "0 14px 30px rgba(14,14,44,.10), inset 0 1px 0 rgba(255,255,255,.7)",
    backdropFilter: "blur(14px)"
  } }, /* @__PURE__ */ React.createElement(Icon, { name: skill.type === "\u77ED\u89C6\u9891" ? "video" : skill.type === "\u516C\u4F17\u53F7\u957F\u6587" ? "document" : "image", size: 18 })), /* @__PURE__ */ React.createElement("div", { style: {
    position: "absolute",
    right: -28,
    top: 40,
    width: 130,
    height: 130,
    borderRadius: 42,
    transform: "rotate(14deg)",
    background: `linear-gradient(135deg, ${skill.palette[2]}, ${skill.palette[3]})`,
    opacity: 0.92,
    boxShadow: "0 24px 52px rgba(14,14,44,.16)"
  } }), /* @__PURE__ */ React.createElement("div", { style: {
    position: "absolute",
    left: 18,
    right: 18,
    bottom: 18
  } }, /* @__PURE__ */ React.createElement("div", { style: {
    display: "inline-flex",
    height: 25,
    alignItems: "center",
    padding: "0 9px",
    borderRadius: 999,
    background: "rgba(255,255,255,.64)",
    color: T.navyMid,
    fontSize: 10.5,
    fontWeight: 800,
    backdropFilter: "blur(10px)",
    marginBottom: 10
  } }, skill.type), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 21, lineHeight: 1.14, fontWeight: 780, color: T.navy, letterSpacing: 0 } }, skill.title)));
  var SkillCard = ({ skill, index, onOpen }) => /* @__PURE__ */ React.createElement(
    "article",
    {
      onClick: () => onOpen(skill),
      style: {
        width: "100%",
        borderRadius: 22,
        overflow: "hidden",
        background: "rgba(255,255,255,.86)",
        border: `1px solid ${T.hairlineSoft}`,
        boxShadow: "0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)",
        cursor: "pointer",
        animation: `fadeInScale .5s ${index * 48}ms ${T.spring} both`,
        transition: `transform .34s ${T.spring}, box-shadow .34s ${T.spring}, border-color .24s ${T.ease}, background .24s ${T.ease}`,
        display: "grid",
        gridTemplateColumns: "minmax(132px, 180px) minmax(0, 1fr)",
        gap: 18,
        padding: 14,
        alignItems: "stretch"
      },
      onMouseEnter: (e) => {
        e.currentTarget.style.transform = "translateY(-5px) scale(1.006)";
        e.currentTarget.style.boxShadow = "0 24px 58px rgba(14,14,44,.13), inset 0 1px 0 rgba(255,255,255,.78)";
        e.currentTarget.style.borderColor = "rgba(75,77,237,.18)";
        e.currentTarget.style.background = "rgba(255,255,255,.94)";
      },
      onMouseLeave: (e) => {
        e.currentTarget.style.transform = "translateY(0) scale(1)";
        e.currentTarget.style.boxShadow = "0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)";
        e.currentTarget.style.borderColor = T.hairlineSoft;
        e.currentTarget.style.background = "rgba(255,255,255,.86)";
      }
    },
    /* @__PURE__ */ React.createElement(SkillArtwork, { skill, compact: true }),
    /* @__PURE__ */ React.createElement("div", { style: { padding: "4px 8px 4px 0", display: "flex", flexDirection: "column", minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: {
      fontSize: 18,
      lineHeight: 1.32,
      fontWeight: 740,
      color: T.navy,
      letterSpacing: 0
    } }, skill.title), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 9, color: T.navyMid, fontSize: 13.2, lineHeight: 1.68, fontWeight: 450 } }, skill.desc), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 14, display: "flex", gap: 7, flexWrap: "wrap" } }, skill.result.slice(0, 3).map((item) => /* @__PURE__ */ React.createElement("span", { key: item, style: {
      height: 28,
      padding: "0 9px",
      borderRadius: 999,
      background: "rgba(250,252,254,.78)",
      border: `1px solid ${T.hairlineSoft}`,
      color: T.navyLight,
      display: "inline-flex",
      alignItems: "center",
      fontSize: 11.2,
      fontWeight: 640
    } }, item))), /* @__PURE__ */ React.createElement("div", { style: { marginTop: "auto", paddingTop: 15, display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 } }, /* @__PURE__ */ React.createElement("span", { style: { fontSize: 11.5, color: T.navyLight, fontFamily: T.fontMono } }, skill.uses, " uses"), /* @__PURE__ */ React.createElement("span", { style: {
      height: 30,
      padding: "0 10px",
      borderRadius: 999,
      background: skill.tint,
      color: skill.accent === T.primary ? T.navy : skill.accent,
      display: "inline-flex",
      alignItems: "center",
      gap: 5,
      fontSize: 11.2,
      fontWeight: 760
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "sparkles", size: 10 }), "Skill")))
  );
  var SkillDetail = ({ skill, onBack, onUse }) => /* @__PURE__ */ React.createElement("div", { style: { maxWidth: 980, margin: "0 auto", animation: "fadeInScale .28s ease both" } }, /* @__PURE__ */ React.createElement(
    "button",
    {
      onClick: onBack,
      style: {
        height: 38,
        padding: "0 13px",
        borderRadius: 13,
        border: `1px solid ${T.hairlineSoft}`,
        background: "rgba(255,255,255,.84)",
        color: T.navyMid,
        cursor: "pointer",
        display: "inline-flex",
        alignItems: "center",
        gap: 7,
        fontSize: 12.5,
        fontWeight: 700,
        boxShadow: T.shadowXs,
        marginBottom: 18
      }
    },
    /* @__PURE__ */ React.createElement(Icon, { name: "chevronLeft", size: 14 }),
    "\u8FD4\u56DE Skill \u5E7F\u573A"
  ), /* @__PURE__ */ React.createElement("section", { style: {
    display: "grid",
    gridTemplateColumns: "minmax(0, .95fr) minmax(320px, 1.05fr)",
    gap: 24,
    alignItems: "stretch"
  } }, /* @__PURE__ */ React.createElement("div", { style: {
    borderRadius: 26,
    overflow: "hidden",
    border: `1px solid ${T.hairlineSoft}`,
    boxShadow: T.shadowLg,
    background: T.white
  } }, /* @__PURE__ */ React.createElement(SkillArtwork, { skill: { ...skill, height: 520 } })), /* @__PURE__ */ React.createElement("div", { style: {
    borderRadius: 26,
    border: `1px solid ${T.hairlineSoft}`,
    background: "rgba(255,255,255,.84)",
    boxShadow: "0 18px 44px rgba(14,14,44,.08), inset 0 1px 0 rgba(255,255,255,.78)",
    padding: 28,
    display: "flex",
    flexDirection: "column"
  } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, marginBottom: 18, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("span", { style: { height: 28, padding: "0 10px", borderRadius: 999, background: skill.tint, color: skill.accent === T.primary ? T.navy : skill.accent, display: "inline-flex", alignItems: "center", fontSize: 11.5, fontWeight: 780 } }, skill.type), /* @__PURE__ */ React.createElement("span", { style: { height: 28, padding: "0 10px", borderRadius: 999, background: T.surface, color: T.navyLight, display: "inline-flex", alignItems: "center", gap: 6, fontSize: 11.5, fontFamily: T.fontMono } }, /* @__PURE__ */ React.createElement(Icon, { name: "sparkles", size: 11 }), skill.uses, " uses")), /* @__PURE__ */ React.createElement("h1", { style: { margin: 0, fontSize: 38, lineHeight: 1.08, fontWeight: 780, letterSpacing: 0, color: T.navy } }, skill.title), /* @__PURE__ */ React.createElement("p", { style: { margin: "18px 0 24px", color: T.navyMid, fontSize: 14.5, lineHeight: 1.8 } }, skill.desc), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10, marginBottom: 24 } }, skill.result.map((item, i) => /* @__PURE__ */ React.createElement("div", { key: item, style: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    minHeight: 42,
    padding: "8px 12px",
    borderRadius: 14,
    background: "rgba(250,252,254,.82)",
    border: `1px solid ${T.hairlineSoft}`
  } }, /* @__PURE__ */ React.createElement("span", { style: { width: 24, height: 24, borderRadius: 9, background: i === 0 ? T.primary : skill.tint, color: i === 0 ? T.navy : skill.accent, display: "inline-flex", alignItems: "center", justifyContent: "center", fontSize: 10.5, fontFamily: T.fontMono, fontWeight: 800 } }, String(i + 1).padStart(2, "0")), /* @__PURE__ */ React.createElement("span", { style: { fontSize: 13, fontWeight: 680, color: T.navy } }, item)))), /* @__PURE__ */ React.createElement("div", { style: {
    marginTop: "auto",
    padding: 16,
    borderRadius: 18,
    background: `linear-gradient(135deg, ${T.primaryTint}, ${skill.tint})`,
    border: `1px solid ${T.hairlineSoft}`
  } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12, color: T.navyMid, lineHeight: 1.65, marginBottom: 14 } }, "\u4F7F\u7528\u540E\u4F1A\u81EA\u52A8\u628A Skill \u6A21\u677F\u586B\u5165\u751F\u6210\u9875\u8F93\u5165\u6846\uFF0C\u5E76\u7B49\u5F85\u4F60\u8865\u5145\u5177\u4F53\u4E3B\u9898\u3002"), /* @__PURE__ */ React.createElement(
    "button",
    {
      onClick: () => onUse(skill),
      style: {
        width: "100%",
        height: 48,
        borderRadius: 16,
        border: "none",
        background: T.navy,
        color: T.primary,
        cursor: "pointer",
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        gap: 8,
        fontSize: 14,
        fontWeight: 780,
        boxShadow: "0 14px 28px rgba(14,14,44,.18)"
      }
    },
    /* @__PURE__ */ React.createElement(Icon, { name: "sparkles", size: 16 }),
    "\u4F7F\u7528 Skill"
  )))));
  var SkillsPage = ({ onBackHome, onOpenAssets, onOpenInsights, onNewChat, onUseSkill }) => {
    const { width, isTablet, isMobile } = useViewport();
    const [navCollapsed, setNavCollapsed] = React.useState(false);
    const [scope, setScope] = React.useState("community");
    const [type, setType] = React.useState("\u5168\u90E8");
    const [query, setQuery] = React.useState("");
    const [selected, setSelected] = React.useState(null);
    const sessions = SKILL_ITEMS.slice(0, 6).map((item) => item.title);
    const types = ["\u5168\u90E8", "\u5C0F\u7EA2\u4E66\u56FE\u6587", "\u516C\u4F17\u53F7\u957F\u6587", "\u77ED\u89C6\u9891"];
    const filtered = SKILL_ITEMS.filter((skill) => skill.owner === scope).filter((skill) => type === "\u5168\u90E8" || skill.type === type).filter((skill) => !query.trim() || `${skill.title} ${skill.type} ${skill.desc}`.toLowerCase().includes(query.trim().toLowerCase()));
    return /* @__PURE__ */ React.createElement("div", { style: { display: "flex", width: "100%", height: "100%", background: T.surfaceWh, overflow: "hidden" } }, !isTablet && /* @__PURE__ */ React.createElement(
      Sidebar,
      {
        active: "skills",
        onNew: onNewChat,
        onNavigate: (id) => {
          if (id === "home") onBackHome();
          if (id === "library") onOpenAssets();
          if (id === "skills") setSelected(null);
          if (id === "insights") onOpenInsights && onOpenInsights();
        },
        sessions,
        collapsed: navCollapsed,
        onToggle: () => setNavCollapsed((v) => !v)
      }
    ), /* @__PURE__ */ React.createElement("main", { style: {
      flex: 1,
      minWidth: 0,
      overflow: "auto",
      background: "linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)",
      position: "relative"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      inset: 0,
      background: "radial-gradient(circle at 48% 8%, rgba(214,255,0,.18), transparent 18%), radial-gradient(circle at 76% 12%, rgba(75,77,237,.075), transparent 22%), radial-gradient(circle at 23% 65%, rgba(243,217,218,.20), transparent 22%)",
      pointerEvents: "none"
    } }), /* @__PURE__ */ React.createElement("div", { style: { position: "relative", zIndex: 1, maxWidth: 1640, margin: "0 auto", padding: isMobile ? "18px 18px 36px" : "28px 30px 50px" } }, selected ? /* @__PURE__ */ React.createElement(SkillDetail, { skill: selected, onBack: () => setSelected(null), onUse: onUseSkill }) : /* @__PURE__ */ React.createElement(React.Fragment, null, isTablet && /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement(NoriLogo, { size: 28 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 15, fontWeight: 760, color: T.navy } }, "Skill \u5E7F\u573A"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11, color: T.navyLight } }, "\u53EF\u590D\u7528\u521B\u4F5C\u7CFB\u7EDF"))), /* @__PURE__ */ React.createElement("button", { onClick: onBackHome, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "home", size: 16, color: T.navyMid }))), /* @__PURE__ */ React.createElement("header", { style: { display: "flex", alignItems: "flex-end", justifyContent: "space-between", gap: 20, marginBottom: 24, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12, fontWeight: 800, letterSpacing: "0.08em", textTransform: "uppercase", color: T.navyLight, marginBottom: 8 } }, "Skill Plaza"), /* @__PURE__ */ React.createElement("h1", { style: { margin: 0, fontSize: isMobile ? 28 : 38, lineHeight: 1.08, letterSpacing: 0, color: T.navy, fontWeight: 760 } }, "Skill \u5E7F\u573A"), /* @__PURE__ */ React.createElement("p", { style: { margin: "10px 0 0", fontSize: 13.5, lineHeight: 1.6, color: T.navyMid } }, "\u9009\u62E9\u4E00\u4E2A\u53EF\u590D\u7528\u7684\u521B\u4F5C\u7CFB\u7EDF\uFF0C\u8BA9 Nori \u6309\u6307\u5B9A\u7ED3\u6784\u5F00\u59CB\u751F\u6210\u3002")), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10, flexWrap: "wrap", justifyContent: isMobile ? "flex-start" : "flex-end" } }, /* @__PURE__ */ React.createElement("label", { style: {
      height: 46,
      minWidth: isMobile ? "100%" : 260,
      borderRadius: 17,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.82)",
      boxShadow: "0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.78)",
      display: "inline-flex",
      alignItems: "center",
      gap: 10,
      padding: "0 14px",
      color: T.navyLight
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "search", size: 16 }), /* @__PURE__ */ React.createElement(
      "input",
      {
        value: query,
        onChange: (e) => setQuery(e.target.value),
        placeholder: "\u641C\u7D22 Skill...",
        style: { flex: 1, minWidth: 0, border: "none", outline: "none", background: "transparent", color: T.navy, fontSize: 13.5, fontFamily: T.fontSans }
      }
    )), /* @__PURE__ */ React.createElement("div", { style: {
      height: 46,
      padding: 4,
      borderRadius: 17,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.82)",
      boxShadow: "0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.78)",
      display: "inline-flex",
      gap: 4
    } }, [
      { id: "community", label: "\u793E\u533A" },
      { id: "mine", label: "\u6211\u7684" }
    ].map((tab) => /* @__PURE__ */ React.createElement(
      "button",
      {
        key: tab.id,
        onClick: () => {
          setScope(tab.id);
          setType("\u5168\u90E8");
        },
        style: {
          height: 38,
          padding: "0 18px",
          borderRadius: 13,
          border: "none",
          background: scope === tab.id ? T.navy : "transparent",
          color: scope === tab.id ? T.white : T.navyMid,
          cursor: "pointer",
          fontSize: 13,
          fontWeight: 760,
          transition: "background .16s, color .16s"
        }
      },
      tab.label
    ))))), /* @__PURE__ */ React.createElement("section", { style: { display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", paddingBottom: 18, borderBottom: `1px solid ${T.hairlineSoft}`, marginBottom: 24 } }, types.map((t) => /* @__PURE__ */ React.createElement(FilterChip, { key: t, active: type === t, onClick: () => setType(t), count: t === "\u5168\u90E8" ? filtered.length : SKILL_ITEMS.filter((skill) => skill.owner === scope && skill.type === t).length }, t))), /* @__PURE__ */ React.createElement("section", { style: { maxWidth: 1040, margin: "0 auto", display: "grid", gap: 16 } }, filtered.map((skill, index) => /* @__PURE__ */ React.createElement(SkillCard, { key: skill.id, skill, index, onOpen: setSelected }))), filtered.length === 0 && /* @__PURE__ */ React.createElement("div", { style: { minHeight: 220, borderRadius: 22, border: `1px dashed ${T.hairline}`, background: "rgba(255,255,255,.56)", color: T.navyLight, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 13 } }, "\u6CA1\u6709\u627E\u5230\u5339\u914D\u7684 Skill")))));
  };
  window.SkillsPage = SkillsPage;
  var INSIGHT_CONTENTS = [
    { id: "c1", title: "\u4E0A\u6D77\u5C0F\u996D\u5E97\u7B2C\u4E00\u6B21\u53BB\u600E\u4E48\u70B9", platform: "RED", platformLabel: "\u5C0F\u7EA2\u4E66", exposure: "42,180", likes: "3,180", saves: "1,820", comments: "248", score: "92", next: "\u62C6\u6210\u83DC\u5355\u7CFB\u5217" },
    { id: "c2", title: "\u4E0B\u73ED\u540E 30 \u5206\u949F\u80FD\u5403\u5230\u7684\u70ED\u996D", platform: "RED", platformLabel: "\u5C0F\u7EA2\u4E66", exposure: "31,020", likes: "2,012", saves: "1,130", comments: "162", score: "86", next: "\u8865\u4E00\u7248\u5BF9\u6BD4\u56FE" },
    { id: "c3", title: "\u540E\u53A8\u5907\u83DC\u7684\u4E00\u5929", platform: "d", platformLabel: "\u6296\u97F3", exposure: "86,540", likes: "5,810", saves: "910", comments: "420", score: "89", next: "\u526A 30s \u53E3\u64AD" },
    { id: "c4", title: "\u4E3B\u7406\u4EBA\u600E\u4E48\u628A\u4E00\u7897\u996D\u505A\u7A33\u5B9A", platform: "\u5FAE", platformLabel: "\u5FAE\u4FE1", exposure: "8,600", likes: "320", saves: "410", comments: "38", score: "71", next: "\u524D 20% \u91CD\u5199" }
  ];
  var INSIGHT_OBSERVATIONS = [
    {
      type: "\u8D62\u70B9",
      time: "\u4ECA\u5929 \xB7 09:00",
      title: "\u8FD9\u5468\u300C\u7B2C\u4E00\u6B21\u53BB\u600E\u4E48\u70B9\u300D\u8DD1\u8D62\u540C\u7C7B 82%",
      body: "\u5C01\u9762\u76F4\u63A5\u628A\u300C\u4E0D\u8E29\u96F7\u83DC\u5355\u300D\u5199\u6E05\u695A\uFF0C\u524D 3 \u79D2\u5148\u7ED9\u7ED3\u8BBA\uFF0C\u518D\u8865\u62DB\u724C\u83DC\u548C\u9002\u5408\u8C01\u53BB\uFF0C\u6700\u80FD\u8BA9\u9644\u8FD1\u4E0A\u73ED\u65CF\u505C\u4E0B\u6765\u3002",
      action: "\u5EF6\u5C55\u6210\u300C\u62DB\u724C\u83DC / \u4EBA\u5747 / \u573A\u666F\u300D\u4E09\u6761\u7CFB\u5217",
      platform: "\u5C0F\u7EA2\u4E66\u4F18\u5148",
      accent: T.success
    },
    {
      type: "\u5F85\u4F18\u5316",
      time: "\u4ECA\u5929 \xB7 09:00",
      title: "\u957F\u6587\u300A\u5C0F\u996D\u5E97\u600E\u4E48\u7559\u4F4F\u56DE\u5934\u5BA2\u300B\u5B8C\u8BFB\u7387\u504F\u4F4E",
      body: "\u524D 30% \u8BFB\u5B8C\u7387\u53EA\u6709 34%\uFF0C\u95EE\u9898\u5728\u7B2C 2 \u5C0F\u8282\u5C55\u5F00\u8FC7\u5FEB\u3002\u53EF\u4EE5\u5728\u5C0F\u8282\u524D\u52A0\u4E00\u6BB5\u300C\u4E0B\u73ED\u6765\u5403\u996D\u300D\u7684\u5177\u8C61\u573A\u666F\u3002",
      action: "\u628A\u5F00\u5934\u6539\u6210\u771F\u5B9E\u5230\u5E97\u573A\u666F\uFF0C\u518D\u8FDB\u5165\u65B9\u6CD5\u8BBA",
      platform: "\u516C\u4F17\u53F7 / \u89C6\u9891\u53F7",
      accent: T.warn
    },
    {
      type: "\u673A\u4F1A",
      time: "\u6628\u5929 \xB7 18:12",
      title: "\u6700\u65B0\u673A\u4F1A\uFF1A#\u4E0A\u6D77\u996D\u5E97\u63A8\u8350 \u6B63\u5728\u4E0A\u5347",
      body: "\u8FD1 48h \u540C\u7C7B\u5185\u5BB9\u6536\u85CF\u8BC4\u8BBA\u8868\u73B0 +62%\uFF0C\u63A8\u8350\u672C\u5468\u8FFD\u4E00\u6761\u300C\u5348\u5E02\u5957\u9910 / \u62DB\u724C\u83DC / \u9002\u5408\u8C01\u53BB\u300D\u7684\u6536\u85CF\u578B\u7B14\u8BB0\u3002",
      action: "\u4ECA\u5929\u5148\u505A\u5C01\u9762\u548C\u6807\u9898 A/B\uFF0C\u660E\u65E9\u53D1\u5E03",
      platform: "\u5C0F\u7EA2\u4E66 + \u77ED\u89C6\u9891",
      accent: T.iris
    }
  ];
  var INSIGHT_HOT_TOPICS = [
    { tag: "#\u4E0A\u6D77\u996D\u5E97\u63A8\u8350", change: "+62%", note: "\u7B2C\u4E00\u6B21\u53BB\u600E\u4E48\u70B9\u3001\u83DC\u5355\u600E\u4E48\u9009\u3001\u9002\u5408\u8C01\u53BB\uFF0C\u8FD9\u7C7B\u5185\u5BB9\u7684\u6536\u85CF\u7387\u6301\u7EED\u62AC\u5347\u3002", fit: "\u5F3A\u76F8\u5173", format: "\u56FE\u6587\u5BF9\u6BD4" },
    { tag: "#\u5348\u5E02\u5957\u9910", change: "+38%", note: "\u4EBA\u5747\u53CB\u597D\u3001\u901A\u52E4\u65B9\u4FBF\u3001\u51FA\u9910\u5FEB\u7684\u5185\u5BB9\uFF0C\u66F4\u5BB9\u6613\u88AB\u9644\u8FD1\u4E0A\u73ED\u65CF\u4FDD\u5B58\u3002", fit: "\u53EF\u8FFD", format: "\u6E05\u5355\u7B14\u8BB0" },
    { tag: "#\u4E3B\u7406\u4EBA\u65E5\u5E38", change: "+12%", note: "\u771F\u5B9E\u5907\u83DC\u3001\u51FA\u9910\u548C\u5E97\u5185\u73AF\u5883\uFF0C\u66F4\u5BB9\u6613\u5EFA\u7ACB\u95E8\u5E97\u4FE1\u4EFB\u611F\u3002", fit: "\u957F\u671F\u517B\u53F7", format: "\u77ED\u89C6\u9891" }
  ];
  var INSIGHT_ACTIONS = [
    { title: "\u4E0B\u4E00\u6761\u4F18\u5148\u505A", value: "\u7B2C\u4E00\u6B21\u53BB\u600E\u4E48\u70B9", note: "\u6CBF\u7528\u9AD8\u6536\u85CF\u5C01\u9762\u8BED\u8A00\uFF0C\u6807\u9898\u66F4\u76F4\u63A5", accent: T.primary },
    { title: "\u6682\u7F13\u6295\u5165", value: "\u7EAF\u65B9\u6CD5\u8BBA\u957F\u6587", note: "\u5F53\u524D\u5B8C\u8BFB\u504F\u4F4E\uFF0C\u5148\u8865\u5230\u5E97\u6848\u4F8B", accent: T.peach },
    { title: "\u5B9A\u4F4D\u53EF\u6C89\u6DC0\u70B9", value: "\u9996\u6BB5\u94A9\u5B50\u6A21\u677F", note: "\u518D\u53D1\u5E03 2 \u6761\u5373\u53EF\u6C89\u6DC0\u4E3A\u8D26\u53F7\u5199\u4F5C\u89C4\u5219", accent: T.success }
  ];
  var DEFAULT_ACCOUNT_PLAN_CALENDAR = [
    { day: "\u5468\u4E00", type: "\u63A2\u5E97\u56FE\u6587", topic: "\u7B2C\u4E00\u6B21\u6765\u5E97\u91CC\uFF0C\u5148\u70B9\u8FD9 3 \u9053\u62DB\u724C\u83DC", ref: "@\u672C\u5730\u5403\u559D\u6307\u5357" },
    { day: "\u5468\u4E8C", type: "\u77ED\u89C6\u9891", topic: "\u540E\u53A8\u5907\u83DC 30 \u79D2\uFF0C\u770B\u770B\u4E00\u7897\u996D\u600E\u4E48\u88AB\u8BA4\u771F\u505A\u597D", ref: "@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0" },
    { day: "\u5468\u4E09", type: "\u56FE\u6587", topic: "\u9644\u8FD1\u4E0A\u73ED\u65CF\u5348\u9910\u4E0D\u8E29\u96F7\u83DC\u5355", ref: "@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240" },
    { day: "\u5468\u56DB", type: "\u957F\u6587", topic: "\u4E00\u5BB6\u5C0F\u5E97\u600E\u4E48\u628A\u56DE\u5934\u5BA2\u7559\u4F4F", ref: "@\u4E3B\u7406\u4EBA\u624B\u8BB0" },
    { day: "\u5468\u4E94", type: "\u77ED\u89C6\u9891", topic: "\u987E\u5BA2\u6700\u5E38\u95EE\u7684 5 \u4E2A\u95EE\u9898", ref: "@\u771F\u5B9E\u63A2\u5E97" },
    { day: "\u5468\u516D", type: "\u56FE\u6587", topic: "\u5468\u672B\u5E26\u670B\u53CB\u6765\u5403\uFF0C\u600E\u4E48\u70B9\u66F4\u5212\u7B97", ref: "@\u672C\u5730\u751F\u6D3B\u5BB6" },
    { day: "\u5468\u65E5", type: "\u590D\u76D8", topic: "\u8FD9\u5468\u6700\u53D7\u6B22\u8FCE\u7684\u4E00\u9053\u83DC", ref: "@\u5C0F\u5E97\u7ECF\u8425\u7B14\u8BB0" }
  ];
  var INSIGHT_PLATFORM_PROFILES = {
    overall: {
      label: "\u5168\u90E8\u5E73\u53F0",
      platform: "ALL",
      theme: T.iris,
      headline: "\u4E0A\u6D77\u5C0F\u996D\u5E97\u8D26\u53F7\u7ED3\u679C\u4F18\u5148\u770B",
      note: "\u5148\u770B\u6DA8\u7C89\u3001\u70B9\u8D5E\u3001\u6536\u85CF\u548C\u8BC4\u8BBA\uFF1B\u70B9\u51FB\u7387\u3001\u5B8C\u8BFB\u7387\u7B49\u4F5C\u4E3A\u4E0B\u4E00\u5C42\u5206\u6790\u6307\u6807\u3002",
      conclusion: "\u73B0\u5728\u9002\u5408\u53D1\u5E03\u300C\u4E0A\u6D77\u5C0F\u996D\u5E97\u7B2C\u4E00\u6B21\u53BB\u600E\u4E48\u70B9\u300D\u7684\u6536\u85CF\u578B\u5185\u5BB9\uFF1A\u5148\u7ED9\u7ED3\u8BBA\uFF0C\u518D\u7ED9\u62DB\u724C\u83DC\u3001\u9884\u7B97\u548C\u9002\u5408\u8C01\u53BB\uFF0C\u6700\u5BB9\u6613\u5E26\u6765\u4FDD\u5B58\u548C\u5230\u5E97\u610F\u613F\u3002",
      overviewCards: [
        { title: "\u5165\u53E3", value: "\u5C01\u9762\u70B9\u51FB\u7387\u7A33\u5B9A", note: "\u5C0F\u7EA2\u4E66\u548C\u89C6\u9891\u53F7\u90FD\u9002\u5408\u7EE7\u7EED\u6D4B\u5C01\u9762 A/B", accent: T.iris },
        { title: "\u7559\u5B58", value: "\u5B8C\u8BFB\u7387\u53EF\u52A0\u7801", note: "\u516C\u4F17\u53F7\u957F\u6587\u9002\u5408\u627F\u63A5\u66F4\u5B8C\u6574\u7684\u83DC\u5355\u89E3\u91CA", accent: T.success },
        { title: "\u589E\u957F", value: "\u51C0\u6DA8\u7C89\u53D8\u597D", note: "\u6296\u97F3\u77ED\u89C6\u9891\u53EF\u4EE5\u628A\u9009\u5E97\u903B\u8F91\u62C6\u6210 30 \u79D2\u7248\u672C", accent: T.primary }
      ],
      metrics: [
        { label: "\u6DA8\u7C89", value: "+1,284", delta: "+21%" },
        { label: "\u70B9\u8D5E", value: "11.9k", delta: "+18%" },
        { label: "\u6536\u85CF", value: "4.8k", delta: "+24%" },
        { label: "\u8BC4\u8BBA", value: "928", delta: "+12%" }
      ],
      analysisMetrics: [
        { label: "\u5C01\u9762\u70B9\u51FB\u7387", value: "6.0%", delta: "+0.9%" },
        { label: "\u5B8C\u64AD / \u5B8C\u8BFB\u7387", value: "50.2%", delta: "+2.4%" },
        { label: "\u6536\u85CF\u7387", value: "2.9%", delta: "+0.5%" },
        { label: "\u51C0\u6DA8\u7C89", value: "+480", delta: "+21%" }
      ],
      chart: {
        "7d": [15, 19, 22, 26, 31, 34, 38, 41, 47, 51, 57, 64],
        "30d": [18, 22, 27, 30, 35, 39, 44, 49, 54, 58, 65, 74],
        "90d": [20, 24, 28, 34, 38, 43, 48, 53, 59, 66, 73, 82]
      },
      rows: [
        { id: "a1", title: "\u4E0A\u6D77\u5C0F\u996D\u5E97\u7B2C\u4E00\u6B21\u53BB\u600E\u4E48\u70B9", platform: "RED", platformLabel: "\u5C0F\u7EA2\u4E66", exposure: "42,180", likes: "3,180", saves: "1,820", comments: "248", score: "92", next: "\u7EE7\u7EED\u505A\u7CFB\u5217\u5C01\u9762" },
        { id: "a2", title: "30 \u79D2\u770B\u61C2\u4EBA\u5747 80 \u5143\u600E\u4E48\u5403", platform: "DY", platformLabel: "\u6296\u97F3", exposure: "86,540", likes: "5,810", saves: "910", comments: "420", score: "89", next: "\u526A 3 \u79D2\u94A9\u5B50" },
        { id: "a3", title: "\u4E00\u5BB6\u5C0F\u996D\u5E97\u600E\u4E48\u628A\u56DE\u5934\u5BA2\u7559\u4F4F", platform: "WX", platformLabel: "\u5FAE\u4FE1\u516C\u4F17\u53F7", exposure: "12,480", likes: "560", saves: "620", comments: "52", score: "79", next: "\u8865\u6848\u4F8B\u622A\u56FE" }
      ]
    },
    red: {
      label: "\u5C0F\u7EA2\u4E66",
      platform: "RED",
      theme: T.iris,
      headline: "\u5C0F\u7EA2\u4E66\u8D26\u53F7\u7ED3\u679C",
      note: "\u5148\u770B\u6DA8\u7C89\u3001\u70B9\u8D5E\u3001\u6536\u85CF\u548C\u8BC4\u8BBA\uFF0C\u518D\u7528\u70B9\u51FB\u7387\u3001\u5B8C\u8BFB\u7387\u5224\u65AD\u8981\u4E0D\u8981\u6362\u5C01\u9762\u6216\u8865\u4E00\u7248\u3002",
      overviewCards: [
        { title: "\u5C01\u9762", value: "\u70B9\u51FB\u7387\u5148\u770B", note: "\u5148\u5224\u65AD\u5C01\u9762\u662F\u4E0D\u662F\u6293\u4F4F\u4E86\u4EBA", accent: T.primary },
        { title: "\u6B63\u6587", value: "\u5B8C\u8BFB\u7387\u7A33\u5B9A", note: "\u6807\u9898\u8FDB\u6765\u7684\u4EBA\u613F\u4E0D\u613F\u610F\u770B\u5B8C", accent: T.iris },
        { title: "\u6269\u6563", value: "\u6536\u85CF\u7387\u4F18\u5148", note: "\u662F\u5426\u503C\u5F97\u7EE7\u7EED\u505A\u7CFB\u5217", accent: T.success }
      ],
      metrics: [
        { label: "\u6DA8\u7C89", value: "+1,284", delta: "+24%" },
        { label: "\u70B9\u8D5E", value: "11.9k", delta: "+18%" },
        { label: "\u6536\u85CF", value: "4.8k", delta: "+24%" },
        { label: "\u8BC4\u8BBA", value: "928", delta: "+12%" }
      ],
      analysisMetrics: [
        { label: "\u5C01\u9762\u70B9\u51FB\u7387", value: "8.2%", delta: "+1.4%" },
        { label: "\u5B8C\u64AD / \u5B8C\u8BFB\u7387", value: "62.4%", delta: "+3.6%" },
        { label: "\u6536\u85CF\u7387", value: "4.3%", delta: "+0.8%" },
        { label: "\u51C0\u6DA8\u7C89", value: "+128", delta: "+24%" }
      ],
      chart: {
        "7d": [18, 24, 20, 32, 39, 34, 50, 44, 58, 52, 68, 82],
        "30d": [20, 26, 31, 34, 42, 39, 45, 52, 61, 58, 70, 88],
        "90d": [24, 29, 33, 38, 40, 48, 54, 57, 66, 72, 80, 92]
      },
      rows: [
        { id: "r1", title: "\u4E0A\u6D77\u5C0F\u996D\u5E97\u7B2C\u4E00\u6B21\u53BB\u600E\u4E48\u70B9", platform: "RED", platformLabel: "\u5C0F\u7EA2\u4E66", exposure: "42,180", likes: "3,180", saves: "1,820", comments: "248", score: "92", next: "\u62C6\u6210\u83DC\u5355\u7CFB\u5217" },
        { id: "r2", title: "\u9644\u8FD1\u4E0A\u73ED\u65CF\u5348\u9910\u4E0D\u8E29\u96F7", platform: "RED", platformLabel: "\u5C0F\u7EA2\u4E66", exposure: "31,020", likes: "2,012", saves: "1,130", comments: "162", score: "86", next: "\u8865\u4E00\u7248\u5BF9\u6BD4\u56FE" },
        { id: "r3", title: "\u628A\u4E00\u7897\u996D\u8BB2\u6E05\u695A", platform: "RED", platformLabel: "\u5C0F\u7EA2\u4E66", exposure: "28,640", likes: "1,820", saves: "980", comments: "144", score: "84", next: "\u505A 3 \u6B65\u6559\u7A0B" }
      ]
    },
    dy: {
      label: "\u6296\u97F3",
      platform: "DY",
      theme: T.success,
      headline: "\u6296\u97F3\u8D26\u53F7\u7ED3\u679C",
      note: "\u5148\u770B\u6DA8\u7C89\u3001\u70B9\u8D5E\u548C\u8BC4\u8BBA\uFF0C\u518D\u7528\u524D 3 \u79D2\u4E0E\u5B8C\u64AD\u7387\u5224\u65AD\u955C\u5934\u8282\u594F\u3002",
      overviewCards: [
        { title: "\u524D 3 \u79D2", value: "\u94A9\u5B50\u5148\u7ACB\u4F4F", note: "\u6709\u6CA1\u6709\u7559\u4E0B\u7EE7\u7EED\u770B\u7684\u7406\u7531", accent: T.success },
        { title: "\u4E2D\u6BB5", value: "\u5B8C\u64AD\u6700\u5173\u952E", note: "\u8282\u594F\u662F\u5426\u8DB3\u591F\u7D27", accent: T.iris },
        { title: "\u56DE\u6D41", value: "\u8BC4\u8BBA\u5E26\u6DA8\u7C89", note: "\u6709\u6CA1\u6709\u5F62\u6210\u4E92\u52A8\u94FE\u8DEF", accent: T.primary }
      ],
      metrics: [
        { label: "\u6DA8\u7C89", value: "+1,284", delta: "+31%" },
        { label: "\u70B9\u8D5E", value: "11.9k", delta: "+18%" },
        { label: "\u6536\u85CF", value: "4.8k", delta: "+24%" },
        { label: "\u8BC4\u8BBA", value: "928", delta: "+12%" }
      ],
      analysisMetrics: [
        { label: "\u5C01\u9762\u70B9\u51FB\u7387", value: "6.4%", delta: "+0.8%" },
        { label: "\u5B8C\u64AD / \u5B8C\u8BFB\u7387", value: "38.5%", delta: "+2.4%" },
        { label: "\u6536\u85CF\u7387", value: "2.1%", delta: "+0.4%" },
        { label: "\u51C0\u6DA8\u7C89", value: "+204", delta: "+31%" }
      ],
      chart: {
        "7d": [14, 18, 16, 22, 26, 24, 32, 40, 38, 44, 52, 60],
        "30d": [18, 21, 24, 28, 30, 36, 38, 45, 49, 54, 60, 71],
        "90d": [16, 19, 23, 27, 31, 35, 39, 42, 46, 52, 59, 68]
      },
      rows: [
        { id: "d1", title: "\u628A\u540E\u53A8\u5907\u83DC\u62CD\u6210 30 \u79D2", platform: "DY", platformLabel: "\u6296\u97F3", exposure: "86,540", likes: "5,810", saves: "910", comments: "420", score: "89", next: "\u526A 30s \u53E3\u64AD" },
        { id: "d2", title: "\u4E09\u5206\u949F\u770B\u61C2\u83DC\u5355\u600E\u4E48\u70B9", platform: "DY", platformLabel: "\u6296\u97F3", exposure: "54,210", likes: "3,260", saves: "760", comments: "198", score: "82", next: "\u8865\u7ED3\u5C3E\u5F15\u5BFC" },
        { id: "d3", title: "\u4E3B\u7406\u4EBA\u4E00\u5929\u7684\u51FA\u9910\u8282\u594F", platform: "DY", platformLabel: "\u6296\u97F3", exposure: "34,060", likes: "1,840", saves: "402", comments: "116", score: "76", next: "\u505A\u5C01\u9762 A/B" }
      ]
    },
    wx: {
      label: "\u5FAE\u4FE1\u516C\u4F17\u53F7",
      platform: "WX",
      theme: T.navy,
      headline: "\u516C\u4F17\u53F7\u8D26\u53F7\u7ED3\u679C",
      note: "\u5148\u770B\u5173\u6CE8\u3001\u70B9\u8D5E\u3001\u6536\u85CF\u548C\u8BC4\u8BBA\uFF0C\u518D\u7528\u5B8C\u8BFB\u7387\u5224\u65AD\u957F\u6587\u7ED3\u6784\u662F\u5426\u9700\u8981\u91CD\u6392\u3002",
      overviewCards: [
        { title: "\u5F00\u5934", value: "\u9996\u6BB5\u8981\u7A33", note: "\u5148\u4EA4\u4EE3\u6E05\u695A\u4E3A\u4EC0\u4E48\u8981\u770B", accent: T.navy },
        { title: "\u4E2D\u6BB5", value: "\u7ED3\u6784\u8981\u987A", note: "\u8BA9\u957F\u6587\u6709\u8282\u594F\u611F", accent: T.iris },
        { title: "\u7ED3\u5C3E", value: "\u6536\u85CF\u4E0E\u56DE\u770B", note: "\u662F\u5426\u503C\u5F97\u88AB\u4FDD\u5B58", accent: T.success }
      ],
      metrics: [
        { label: "\u6DA8\u7C89", value: "+1,284", delta: "+12%" },
        { label: "\u70B9\u8D5E", value: "11.9k", delta: "+18%" },
        { label: "\u6536\u85CF", value: "4.8k", delta: "+24%" },
        { label: "\u8BC4\u8BBA", value: "928", delta: "+12%" }
      ],
      analysisMetrics: [
        { label: "\u5C01\u9762\u70B9\u51FB\u7387", value: "4.1%", delta: "+0.3%" },
        { label: "\u5B8C\u64AD / \u5B8C\u8BFB\u7387", value: "55.2%", delta: "+1.8%" },
        { label: "\u6536\u85CF\u7387", value: "1.7%", delta: "+0.2%" },
        { label: "\u51C0\u6DA8\u7C89", value: "+56", delta: "+12%" }
      ],
      chart: {
        "7d": [12, 14, 18, 16, 22, 21, 28, 30, 34, 36, 42, 48],
        "30d": [15, 17, 20, 22, 25, 27, 32, 35, 38, 40, 46, 50],
        "90d": [18, 20, 22, 24, 28, 30, 34, 37, 40, 44, 48, 54]
      },
      rows: [
        { id: "w1", title: "\u4E0A\u6D77\u5C0F\u996D\u5E97\u600E\u4E48\u7559\u4F4F\u56DE\u5934\u5BA2", platform: "WX", platformLabel: "\u5FAE\u4FE1\u516C\u4F17\u53F7", exposure: "8,600", likes: "320", saves: "410", comments: "38", score: "71", next: "\u524D 20% \u91CD\u5199" },
        { id: "w2", title: "\u4E00\u4EFD\u83DC\u5355\u590D\u76D8\u7B14\u8BB0", platform: "WX", platformLabel: "\u5FAE\u4FE1\u516C\u4F17\u53F7", exposure: "12,480", likes: "560", saves: "620", comments: "52", score: "79", next: "\u8865\u6848\u4F8B\u622A\u56FE" },
        { id: "w3", title: "\u6BCF\u5468\u996D\u70B9\u89C2\u5BDF", platform: "WX", platformLabel: "\u5FAE\u4FE1\u516C\u4F17\u53F7", exposure: "7,240", likes: "210", saves: "330", comments: "26", score: "68", next: "\u52A0\u76EE\u5F55\u548C\u5C0F\u6807\u9898" }
      ]
    },
    sp: {
      label: "\u89C6\u9891\u53F7",
      platform: "SP",
      theme: T.peach,
      headline: "\u89C6\u9891\u53F7\u8D26\u53F7\u7ED3\u679C",
      note: "\u5148\u770B\u6DA8\u7C89\u3001\u70B9\u8D5E\u3001\u6536\u85CF\u548C\u8BC4\u8BBA\uFF0C\u518D\u7528\u5B8C\u64AD\u7387\u5224\u65AD\u771F\u5B9E\u573A\u666F\u662F\u5426\u8DB3\u591F\u6293\u4EBA\u3002",
      overviewCards: [
        { title: "\u4FE1\u4EFB", value: "\u771F\u5B9E\u573A\u666F", note: "\u6709\u6CA1\u6709\u8BA9\u4EBA\u89C9\u5F97\u9760\u8C31", accent: T.peach },
        { title: "\u8282\u594F", value: "\u7A33\u4F4F\u5B8C\u64AD", note: "\u77ED\u89C6\u9891\u7ED3\u6784\u662F\u5426\u6E05\u695A", accent: T.iris },
        { title: "\u590D\u770B", value: "\u6536\u85CF\u4E0E\u8F6C\u53D1", note: "\u662F\u5426\u503C\u5F97\u7559\u7ED9\u719F\u4EBA", accent: T.success }
      ],
      metrics: [
        { label: "\u6DA8\u7C89", value: "+1,284", delta: "+15%" },
        { label: "\u70B9\u8D5E", value: "11.9k", delta: "+18%" },
        { label: "\u6536\u85CF", value: "4.8k", delta: "+24%" },
        { label: "\u8BC4\u8BBA", value: "928", delta: "+12%" }
      ],
      analysisMetrics: [
        { label: "\u5C01\u9762\u70B9\u51FB\u7387", value: "5.3%", delta: "+0.5%" },
        { label: "\u5B8C\u64AD / \u5B8C\u8BFB\u7387", value: "44.8%", delta: "+1.6%" },
        { label: "\u6536\u85CF\u7387", value: "2.4%", delta: "+0.3%" },
        { label: "\u51C0\u6DA8\u7C89", value: "+92", delta: "+15%" }
      ],
      chart: {
        "7d": [10, 13, 15, 17, 22, 24, 26, 28, 30, 33, 37, 42],
        "30d": [11, 14, 16, 19, 21, 25, 28, 31, 34, 36, 40, 45],
        "90d": [13, 15, 18, 20, 23, 26, 30, 33, 35, 39, 42, 48]
      },
      rows: [
        { id: "s1", title: "\u793E\u533A\u5C0F\u9986\u7684\u4E00\u5929", platform: "SP", platformLabel: "\u89C6\u9891\u53F7", exposure: "14,230", likes: "680", saves: "260", comments: "40", score: "74", next: "\u52A0\u4EBA\u7269\u91C7\u8BBF" },
        { id: "s2", title: "\u95E8\u5E97\u771F\u5B9E\u51FA\u9910", platform: "SP", platformLabel: "\u89C6\u9891\u53F7", exposure: "18,520", likes: "920", saves: "310", comments: "57", score: "78", next: "\u8865\u5B57\u5E55\u6761" },
        { id: "s3", title: "\u987E\u5BA2\u5E38\u95EE 5 \u4E2A\u95EE\u9898", platform: "SP", platformLabel: "\u89C6\u9891\u53F7", exposure: "9,840", likes: "420", saves: "180", comments: "23", score: "69", next: "\u538B\u7F29\u65F6\u957F" }
      ]
    }
  };
  var insightTabs = [
    { id: "review", label: "\u6570\u636E\u590D\u76D8" },
    { id: "hot", label: "\u70ED\u70B9" }
  ];
  var LargeSegmentedTabs = ({ tabs, active, onChange, mobile, minWidth = 300 }) => /* @__PURE__ */ React.createElement("div", { style: {
    display: "grid",
    gridTemplateColumns: `repeat(${tabs.length}, minmax(0, 1fr))`,
    gap: 6,
    padding: 6,
    borderRadius: 23,
    border: `1px solid ${T.hairlineSoft}`,
    background: "rgba(255,255,255,.84)",
    boxShadow: "0 14px 30px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.80)",
    minWidth: mobile ? 0 : minWidth,
    width: mobile ? "100%" : "auto"
  } }, tabs.map((tab) => {
    const selected = active === tab.id;
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        key: tab.id,
        onClick: () => onChange(tab.id),
        style: {
          height: mobile ? 44 : 46,
          minWidth: 0,
          padding: mobile ? "0 11px" : "0 24px",
          borderRadius: 18,
          border: "none",
          background: selected ? T.navy : "transparent",
          color: selected ? T.white : T.navyMid,
          boxShadow: selected ? "0 10px 22px rgba(14,14,44,.16)" : "none",
          cursor: "pointer",
          fontSize: mobile ? 13.5 : 15,
          fontWeight: selected ? 760 : 640,
          whiteSpace: "nowrap",
          transition: `background .18s ${T.ease}, color .18s ${T.ease}, box-shadow .18s ${T.ease}, transform .18s ${T.ease}`
        },
        onMouseEnter: (e) => {
          if (!selected) e.currentTarget.style.background = "rgba(14,14,44,.035)";
        },
        onMouseLeave: (e) => {
          if (!selected) e.currentTarget.style.background = "transparent";
        }
      },
      tab.label
    );
  }));
  var InsightTopBar = ({ active, onChange, mobile }) => /* @__PURE__ */ React.createElement("header", { style: {
    display: "flex",
    flexDirection: mobile ? "column" : "row",
    alignItems: mobile ? "stretch" : "flex-end",
    justifyContent: "space-between",
    gap: mobile ? 18 : 24,
    marginBottom: mobile ? 22 : 26
  } }, /* @__PURE__ */ React.createElement("div", { style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12, fontWeight: 800, letterSpacing: "0.08em", textTransform: "uppercase", color: T.navyLight, marginBottom: 8 } }, "Insights"), /* @__PURE__ */ React.createElement("h1", { style: { margin: 0, fontSize: mobile ? 27 : 34, lineHeight: 1.14, letterSpacing: 0, color: T.navy, fontWeight: 720 } }, "\u6570\u636E\u6D1E\u5BDF")), /* @__PURE__ */ React.createElement("div", { style: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    width: mobile ? "100%" : "auto",
    justifyContent: mobile ? "space-between" : "flex-end",
    flexWrap: mobile ? "nowrap" : "wrap"
  } }, /* @__PURE__ */ React.createElement(LargeSegmentedTabs, { tabs: insightTabs, active, onChange, mobile, minWidth: 338 })));
  var InsightPanel = ({ children, style }) => /* @__PURE__ */ React.createElement("section", { style: {
    borderRadius: 26,
    background: "rgba(255,255,255,.82)",
    border: `1px solid ${T.hairlineSoft}`,
    boxShadow: "0 16px 38px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.78)",
    backdropFilter: "blur(18px) saturate(1.08)",
    overflow: "hidden",
    ...style
  } }, children);
  var InsightRangeToggle = ({ options, value, onChange, wide = false }) => /* @__PURE__ */ React.createElement("div", { style: {
    display: "inline-grid",
    gridTemplateColumns: `repeat(${options.length}, minmax(0, 1fr))`,
    gap: 3,
    padding: 4,
    borderRadius: 15,
    border: `1px solid ${T.hairlineSoft}`,
    background: "rgba(250,252,254,.78)",
    minWidth: wide ? 360 : options.length === 3 ? 196 : 176
  } }, options.map((option) => {
    const active = value === option;
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        key: option,
        onClick: () => onChange(option),
        style: {
          height: 36,
          borderRadius: 11,
          border: "none",
          background: active ? T.white : "transparent",
          color: active ? T.iris : T.navyLight,
          boxShadow: active ? "0 8px 18px rgba(14,14,44,.08)" : "none",
          fontSize: 13,
          fontWeight: 760,
          cursor: "pointer"
        }
      },
      option
    );
  }));
  var InsightMetric = ({ label, value, delta, down, mobile, compact, index, last, total = 4 }) => /* @__PURE__ */ React.createElement("div", { style: {
    minHeight: mobile ? 116 : 138,
    padding: mobile ? "21px 22px" : "28px 26px",
    borderRight: !mobile && (compact ? index % 2 === 0 : !last) ? `1px solid ${T.hairlineSoft}` : "none",
    borderBottom: mobile && !last || compact && index < total - 2 ? `1px solid ${T.hairlineSoft}` : "none",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    minWidth: 0
  } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12.5, color: T.navyLight, fontWeight: 620, marginBottom: 14 } }, label), /* @__PURE__ */ React.createElement("div", { style: { fontSize: mobile ? 26 : 28, lineHeight: 1, color: T.navy, fontWeight: 660, fontFamily: T.fontMono } }, value), /* @__PURE__ */ React.createElement("div", { style: {
    marginTop: 17,
    color: down ? T.error : T.success,
    fontSize: 12.5,
    fontWeight: 650,
    fontFamily: T.fontMono
  } }, down ? "\u2193" : "\u2191", " ", delta));
  var InsightLineChart = ({ range, platformData }) => {
    const values = platformData.chart[range];
    const points = values.map((v, i) => {
      const x = 36 + i * (808 / (values.length - 1));
      const y = 276 - v * 2.55;
      return [x, y];
    });
    const line = points.map(([x, y], i) => `${i === 0 ? "M" : "L"}${x.toFixed(1)} ${y.toFixed(1)}`).join(" ");
    const area = `${line} L844 304 L36 304 Z`;
    return /* @__PURE__ */ React.createElement("svg", { viewBox: "0 0 880 320", width: "100%", height: "100%", style: { display: "block" }, preserveAspectRatio: "none" }, /* @__PURE__ */ React.createElement("defs", null, /* @__PURE__ */ React.createElement("linearGradient", { id: `reviewChartFill-${range}`, x1: "0", x2: "0", y1: "0", y2: "1" }, /* @__PURE__ */ React.createElement("stop", { offset: "0%", stopColor: platformData.theme, stopOpacity: ".18" }), /* @__PURE__ */ React.createElement("stop", { offset: "100%", stopColor: T.success, stopOpacity: "0" }))), [64, 124, 184, 244, 304].map((y) => /* @__PURE__ */ React.createElement("line", { key: y, x1: "36", x2: "844", y1: y, y2: y, stroke: "rgba(14,14,44,.045)", strokeWidth: "1" })), /* @__PURE__ */ React.createElement("path", { d: area, fill: `url(#reviewChartFill-${range})` }), /* @__PURE__ */ React.createElement("path", { d: line, fill: "none", stroke: platformData.theme, strokeWidth: "3.2", strokeLinecap: "round", strokeLinejoin: "round" }), points.map(([x, y], i) => i % 3 === 0 || i === points.length - 1 ? /* @__PURE__ */ React.createElement("circle", { key: `${x}-${y}`, cx: x, cy: y, r: "4.2", fill: T.white, stroke: platformData.theme, strokeWidth: "2.2" }) : null));
  };
  var InsightTable = ({ rows, mobile }) => {
    if (mobile) {
      return /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10, padding: "14px 16px 18px" } }, rows.map((row) => /* @__PURE__ */ React.createElement("div", { key: row.id, style: { border: `1px solid ${T.hairlineSoft}`, borderRadius: 18, padding: 14, background: "rgba(250,252,254,.74)" } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 14, fontWeight: 820, color: T.navy } }, row.title), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 10, display: "flex", gap: 8, flexWrap: "wrap", fontSize: 12, color: T.navyLight } }, /* @__PURE__ */ React.createElement(PlatformBadge, { row }), /* @__PURE__ */ React.createElement("span", null, "\u66DD\u5149 ", row.exposure), /* @__PURE__ */ React.createElement("span", null, "\u70B9\u8D5E ", row.likes), /* @__PURE__ */ React.createElement("span", null, "\u6536\u85CF ", row.saves), /* @__PURE__ */ React.createElement("span", null, "\u8BC4\u8BBA ", row.comments), /* @__PURE__ */ React.createElement("span", null, "Nori ", row.score), /* @__PURE__ */ React.createElement("span", null, row.next)))));
    }
    return /* @__PURE__ */ React.createElement("div", { style: { overflowX: "auto" } }, /* @__PURE__ */ React.createElement("div", { style: { minWidth: 860 } }, /* @__PURE__ */ React.createElement("div", { style: {
      display: "grid",
      gridTemplateColumns: "minmax(250px, 1.35fr) 112px repeat(4, minmax(92px, .48fr)) 92px minmax(150px, .75fr)",
      minHeight: 58,
      alignItems: "center",
      color: T.navyLight,
      fontSize: 13,
      fontWeight: 820,
      borderBottom: `1px solid ${T.hairline}`,
      padding: "0 28px"
    } }, ["\u5185\u5BB9", "\u5E73\u53F0", "\u66DD\u5149", "\u70B9\u8D5E", "\u6536\u85CF", "\u8BC4\u8BBA", "\u8BC4\u5206", "\u4E0B\u4E00\u6B65"].map((item) => /* @__PURE__ */ React.createElement("div", { key: item }, item))), rows.map((row) => /* @__PURE__ */ React.createElement("div", { key: row.id, style: {
      display: "grid",
      gridTemplateColumns: "minmax(250px, 1.35fr) 112px repeat(4, minmax(92px, .48fr)) 92px minmax(150px, .75fr)",
      minHeight: 76,
      alignItems: "center",
      padding: "0 28px",
      color: T.navy,
      fontSize: 16,
      fontWeight: 760
    } }, /* @__PURE__ */ React.createElement("div", null, row.title), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement(PlatformBadge, { row })), /* @__PURE__ */ React.createElement("div", { style: { fontFamily: T.fontMono, color: T.navyMid } }, row.exposure), /* @__PURE__ */ React.createElement("div", { style: { fontFamily: T.fontMono, color: T.navyMid } }, row.likes), /* @__PURE__ */ React.createElement("div", { style: { fontFamily: T.fontMono, color: T.navyMid } }, row.saves), /* @__PURE__ */ React.createElement("div", { style: { fontFamily: T.fontMono, color: T.navyMid } }, row.comments), /* @__PURE__ */ React.createElement("div", { style: { fontFamily: T.fontMono, color: Number(row.score) >= 85 ? T.success : T.warn } }, row.score), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyMid, fontSize: 13.5, fontWeight: 680 } }, row.next)))));
  };
  var PlatformBadge = ({ row }) => {
    const bg = row.platform === "RED" ? "#f04455" : row.platform === "DY" || row.platform === "d" ? "#111111" : row.platform === "WX" ? T.success : T.iris;
    return /* @__PURE__ */ React.createElement("span", { title: row.platformLabel, style: {
      minWidth: 24,
      height: 24,
      padding: "0 6px",
      borderRadius: 7,
      background: bg,
      color: T.white,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: 9,
      fontWeight: 840,
      fontFamily: row.platform === "\u5FAE" ? T.fontSans : T.fontMono
    } }, row.platform);
  };
  var InsightReviewTab = ({ mobile, compact, platform, onPlatformChange }) => {
    const [chartRange, setChartRange] = React.useState("7d");
    const [tableRange, setTableRange] = React.useState("\u8FD1 7 \u5929");
    const [timeGranularity, setTimeGranularity] = React.useState("Daily");
    const platformData = INSIGHT_PLATFORM_PROFILES[platform] || INSIGHT_PLATFORM_PROFILES.overall;
    const metrics = platformData.metrics;
    const platformKeys = ["overall", "red", "dy", "wx", "sp"];
    return /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: mobile ? 22 : 30 } }, /* @__PURE__ */ React.createElement(InsightPanel, null, /* @__PURE__ */ React.createElement("div", { style: {
      padding: mobile ? "22px 20px 4px" : "28px 30px 6px",
      display: "flex",
      justifyContent: "flex-end",
      alignItems: mobile ? "stretch" : "flex-start",
      gap: mobile ? 14 : 18,
      flexDirection: mobile ? "column" : "row"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexWrap: "wrap", justifyContent: mobile ? "flex-start" : "flex-end", gap: 10 } }, /* @__PURE__ */ React.createElement(InsightRangeToggle, { options: ["Daily", "Weekly", "Monthly"], value: timeGranularity, onChange: setTimeGranularity }), /* @__PURE__ */ React.createElement(
      InsightRangeToggle,
      {
        options: platformKeys.map((key) => INSIGHT_PLATFORM_PROFILES[key].label),
        value: platformData.label,
        onChange: (label) => {
          const next = platformKeys.find((key) => INSIGHT_PLATFORM_PROFILES[key].label === label);
          if (next) onPlatformChange(next);
        },
        wide: !mobile
      }
    ))), /* @__PURE__ */ React.createElement("div", { style: {
      display: "grid",
      gridTemplateColumns: mobile ? "1fr" : compact ? "repeat(2, minmax(0, 1fr))" : "repeat(4, minmax(0, 1fr))"
    } }, metrics.map((metric, index) => /* @__PURE__ */ React.createElement(
      InsightMetric,
      {
        key: metric.label,
        ...metric,
        mobile,
        compact,
        index,
        total: metrics.length,
        last: index === metrics.length - 1
      }
    )))), /* @__PURE__ */ React.createElement(InsightPanel, { style: {
      padding: mobile ? 22 : 30,
      background: "linear-gradient(135deg, rgba(224,250,244,.88), rgba(245,255,224,.54))",
      border: "1px solid rgba(49,208,170,.16)",
      boxShadow: "0 18px 44px rgba(49,208,170,.08), inset 0 1px 0 rgba(255,255,255,.72)"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "flex-start", gap: 14 } }, /* @__PURE__ */ React.createElement("span", { style: {
      width: 42,
      height: 42,
      borderRadius: 16,
      background: "rgba(255,255,255,.78)",
      color: T.success,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0,
      boxShadow: "0 10px 22px rgba(49,208,170,.10)"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "sparkles", size: 18 })), /* @__PURE__ */ React.createElement("div", { style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.success, fontSize: 12.5, fontWeight: 720, marginBottom: 10 } }, "Nori \u4ECA\u65E5\u7ED3\u8BBA"), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: mobile ? 18 : 20, lineHeight: 1.56, fontWeight: 620 } }, platformData.conclusion || "\u73B0\u5728\u9002\u5408\u53D1\u5E03\u300C\u4E0A\u6D77\u5C0F\u996D\u5E97\u7B2C\u4E00\u6B21\u53BB\u600E\u4E48\u70B9\u300D\u7684\u6536\u85CF\u578B\u5185\u5BB9\u3002\u7528\u660E\u786E\u83DC\u5355\u7ED3\u8BBA\u5E26\u70B9\u51FB\uFF0C\u7528\u771F\u5B9E\u5230\u5E97\u573A\u666F\u5E26\u6536\u85CF\uFF0C\u518D\u628A\u540C\u4E00\u4E3B\u9898\u62C6\u6210\u77ED\u89C6\u9891\u548C\u957F\u6587\u627F\u63A5\u3002"), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 12, color: T.navyMid, fontSize: 13.2, lineHeight: 1.82, fontWeight: 430 } }, "\u5EFA\u8BAE\u4ECA\u5929\u5148\u505A\u4E00\u6761\u300C\u7B2C\u4E00\u6B21\u53BB\u7167\u7740\u70B9\u300D\u7684\u7248\u672C\uFF1A\u6807\u9898\u4E0D\u8981\u592A\u6587\u827A\uFF0C\u7B2C\u4E00\u5C4F\u76F4\u63A5\u7ED9\u83DC\u5355\u7ED3\u8BBA\uFF0C\u6B63\u6587\u518D\u8865\u4EBA\u5747\u3001\u4F4D\u7F6E\u548C\u907F\u5751\u63D0\u9192\u3002")))), /* @__PURE__ */ React.createElement("div", { style: {
      display: "grid",
      gridTemplateColumns: mobile ? "1fr" : "minmax(0, 1.42fr) minmax(340px, .72fr)",
      gap: mobile ? 22 : 30,
      alignItems: "stretch"
    } }, /* @__PURE__ */ React.createElement(InsightPanel, { style: { padding: mobile ? "26px 22px 22px" : "34px 36px 30px" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 16, flexWrap: "wrap", alignItems: "flex-start" } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13, color: T.navyLight, fontWeight: 650, marginBottom: 16 } }, "\u4E03\u65E5\u6838\u5FC3\u6307\u6807\u8D8B\u52BF"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "baseline", gap: 12, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("span", { style: { fontSize: mobile ? 30 : 34, lineHeight: 1, color: T.navy, fontWeight: 660, fontFamily: T.fontMono } }, platformData.analysisMetrics?.[1]?.value || platformData.metrics[1].value), /* @__PURE__ */ React.createElement("span", { style: { color: T.success, fontSize: 13.2, fontWeight: 650, fontFamily: T.fontMono } }, "\u2191 ", (platformData.analysisMetrics?.[1]?.delta || platformData.metrics[1].delta).replace("+", ""))), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 12, color: T.navyLight, fontSize: 12.5, lineHeight: 1.7, fontWeight: 430 } }, "\u8FD9\u91CC\u770B\u5206\u6790\u6570\u636E\uFF1A\u5C01\u9762\u70B9\u51FB\u7387\u3001\u5B8C\u64AD / \u5B8C\u8BFB\u7387\u3001\u6536\u85CF\u7387\u4E0E\u51C0\u6DA8\u7C89\u3002")), /* @__PURE__ */ React.createElement(InsightRangeToggle, { options: ["7d", "30d", "90d"], value: chartRange, onChange: setChartRange })), /* @__PURE__ */ React.createElement("div", { style: { height: mobile ? 230 : 336, marginTop: mobile ? 24 : 34 } }, /* @__PURE__ */ React.createElement(InsightLineChart, { range: chartRange, platformData }))), /* @__PURE__ */ React.createElement(InsightPanel, { style: { padding: mobile ? 24 : 30 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginBottom: 24 } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 13, fontWeight: 650, marginBottom: 9 } }, "\u5E73\u53F0\u9002\u914D\u5EFA\u8BAE"), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 17, lineHeight: 1.42, fontWeight: 640 } }, platformData.label, " \u5F53\u524D\u6253\u6CD5")), /* @__PURE__ */ React.createElement("span", { style: { width: 38, height: 38, borderRadius: 14, background: T.irisTint, color: platformData.theme, display: "inline-flex", alignItems: "center", justifyContent: "center", flexShrink: 0 } }, /* @__PURE__ */ React.createElement(Icon, { name: "target", size: 18 }))), platformData.overviewCards.map((item, index) => /* @__PURE__ */ React.createElement("div", { key: item.title, style: { padding: "18px 0", borderTop: `1px solid ${T.hairlineSoft}` } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "baseline", justifyContent: "space-between", gap: 12 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 14.5, fontWeight: 650 } }, item.title), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 12.5, fontFamily: T.fontMono } }, index === 0 ? "1h" : index === 1 ? "3h" : "24h")), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 9, color: T.navyMid, fontSize: 12.8, lineHeight: 1.68, fontWeight: 430 } }, item.note), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 12, height: 5, borderRadius: 999, background: "rgba(14,14,44,.055)", overflow: "hidden" } }, /* @__PURE__ */ React.createElement("div", { style: { width: `${74 - index * 12}%`, height: "100%", borderRadius: 999, background: item.accent } })))))), /* @__PURE__ */ React.createElement(InsightPanel, null, /* @__PURE__ */ React.createElement(PanelHeader, { title: "\u4ECA\u5929 Nori \u7ED9\u4F60\u7684\u89C2\u5BDF", action: "\u67E5\u770B\u5168\u90E8" }), /* @__PURE__ */ React.createElement("div", { style: { display: "grid" } }, INSIGHT_OBSERVATIONS.map((item, i) => /* @__PURE__ */ React.createElement("div", { key: item.title, style: {
      display: "grid",
      gridTemplateColumns: mobile ? "1fr" : "140px minmax(0, 1fr) minmax(230px, .58fr)",
      gap: mobile ? 12 : 24,
      padding: mobile ? "22px 20px" : "26px 30px",
      borderTop: i === 0 ? `1px solid ${T.hairlineSoft}` : `1px solid ${T.hairline}`,
      alignItems: "start"
    } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: {
      display: "inline-flex",
      alignItems: "center",
      height: 26,
      padding: "0 10px",
      borderRadius: 999,
      background: `${item.accent}18`,
      color: item.accent,
      fontSize: 12,
      fontWeight: 840
    } }, item.type), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 6, color: T.navyLight, fontSize: 13, fontFamily: T.fontMono } }, item.time)), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: mobile ? 16.5 : 17.5, lineHeight: 1.45, fontWeight: 760 } }, item.title), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 8, color: T.navyMid, fontSize: mobile ? 14 : 14.8, lineHeight: 1.76, fontWeight: 500 } }, item.body)), /* @__PURE__ */ React.createElement("div", { style: {
      borderRadius: 18,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(250,252,254,.72)",
      padding: 14,
      minWidth: 0
    } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 12, fontWeight: 820, marginBottom: 8 } }, "\u5EFA\u8BAE\u52A8\u4F5C"), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 13.2, lineHeight: 1.62, fontWeight: 650 } }, item.action), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 12, display: "flex", gap: 8, justifyContent: mobile ? "flex-start" : "space-between", flexWrap: "wrap", alignItems: "center" } }, /* @__PURE__ */ React.createElement("span", { style: { color: T.iris, fontSize: 12.5, fontWeight: 780 } }, item.platform), /* @__PURE__ */ React.createElement("button", { style: { ...pillButtonStyle(true), height: 36, padding: "0 12px", fontSize: 12.5 } }, "\u751F\u6210\u8349\u7A3F ", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 13 })))))))), /* @__PURE__ */ React.createElement(InsightPanel, null, /* @__PURE__ */ React.createElement(PanelHeader, { title: "\u5355\u6761\u5185\u5BB9\u8868\u73B0", right: /* @__PURE__ */ React.createElement(InsightRangeToggle, { options: ["\u8FD1 7 \u5929", "\u8FD1 30 \u5929"], value: tableRange, onChange: setTableRange }) }), /* @__PURE__ */ React.createElement(InsightTable, { rows: platformData.rows, mobile })));
  };
  var PanelHeader = ({ title, action, right }) => /* @__PURE__ */ React.createElement("div", { style: {
    minHeight: 82,
    padding: "0 32px",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    gap: 14,
    borderBottom: `1px solid ${T.hairlineSoft}`,
    flexWrap: "wrap"
  } }, /* @__PURE__ */ React.createElement("h2", { style: { margin: 0, color: T.navy, fontSize: 17, fontWeight: 650 } }, title), right || action && /* @__PURE__ */ React.createElement("button", { style: {
    border: "none",
    background: "transparent",
    color: T.navyLight,
    fontSize: 13.2,
    fontWeight: 650,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    gap: 8
  } }, action, /* @__PURE__ */ React.createElement(Icon, { name: "chevronRight", size: 15 })));
  var pillButtonStyle = (dark) => ({
    height: 42,
    padding: "0 17px",
    borderRadius: 14,
    border: dark ? "1px solid rgba(75,77,237,.16)" : `1px solid ${T.hairline}`,
    background: dark ? "rgba(239,239,253,.92)" : "rgba(255,255,255,.72)",
    color: dark ? T.iris : T.navy,
    boxShadow: dark ? "0 10px 22px rgba(75,77,237,.10)" : T.shadowXs,
    display: "inline-flex",
    alignItems: "center",
    gap: 7,
    fontSize: 14,
    fontWeight: 820,
    cursor: "pointer",
    whiteSpace: "nowrap"
  });
  var InsightProfileTab = ({ mobile }) => /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: mobile ? 18 : 24 } }, /* @__PURE__ */ React.createElement(InsightPanel, { style: { padding: mobile ? 22 : 30 } }, /* @__PURE__ */ React.createElement("div", { style: {
    display: "grid",
    gridTemplateColumns: mobile ? "1fr" : "minmax(0, 1.08fr) minmax(300px, .72fr)",
    gap: mobile ? 22 : 28,
    alignItems: "center"
  } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 18 } }, /* @__PURE__ */ React.createElement("img", { src: ONION_BURST_ASSETS[0], alt: "", style: { width: 62, height: 62, borderRadius: "50%", objectFit: "cover", background: T.primaryTint } }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 21, fontWeight: 760 } }, "\u8D26\u53F7\u5B9A\u4F4D"), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 7, color: T.navyLight, fontSize: 14, fontWeight: 650 } }, "\u6765\u81EA\u8D26\u53F7\u89C4\u5212\u8F93\u51FA\uFF0C\u540E\u7EED\u521B\u4F5C\u4F1A\u81EA\u52A8\u5F15\u7528"))), /* @__PURE__ */ React.createElement("div", { style: {
    borderRadius: 18,
    border: `1px solid ${T.hairlineSoft}`,
    background: "rgba(250,252,254,.74)",
    padding: 16
  } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 12, fontWeight: 760, marginBottom: 8 } }, "\u5B9A\u4F4D\u4E00\u53E5\u8BDD"), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 16, lineHeight: 1.45, fontWeight: 700 } }, "\u505A\u9644\u8FD1\u4EBA\u613F\u610F\u6536\u85CF\u7684\u4E0A\u6D77\u996D\u5E97\u63A8\u8350\u8D26\u53F7\uFF0C\u4E3B\u6253\u771F\u5B9E\u590D\u5403\u548C\u4E0D\u8E29\u96F7\u83DC\u5355\u3002")))), /* @__PURE__ */ React.createElement(InsightPanel, { style: { padding: mobile ? 22 : 30 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 13, fontWeight: 760, marginBottom: 18 } }, "\u8D26\u53F7\u5B9A\u4F4D\u4E94\u7EF4"), /* @__PURE__ */ React.createElement("div", { style: {
    display: "grid",
    gridTemplateColumns: mobile ? "1fr" : "repeat(5, minmax(0, 1fr))",
    gap: 12
  } }, [
    ["\u8D5B\u9053\u7EC6\u5206", ["\u4E0A\u6D77\u672C\u5730\u996D\u5E97", "\u793E\u533A\u5C0F\u9986", "\u4E0B\u73ED\u7EA6\u996D"]],
    ["\u76EE\u6807\u53D7\u4F17", ["25-38 \u5C81", "\u9644\u8FD1\u4E0A\u73ED\u65CF", "\u5468\u672B\u805A\u9910"]],
    ["\u4EBA\u8BBE\u6807\u7B7E", ["\u4EB2\u5207", "\u771F\u5B9E\u4E3B\u7406\u4EBA", "\u61C2\u672C\u5730\u751F\u6D3B"]],
    ["\u5185\u5BB9\u4EF7\u503C", ["\u4E0D\u8E29\u96F7\u83DC\u5355", "\u771F\u5B9E\u79CD\u8349", "\u5230\u5E97\u51B3\u7B56"]],
    ["\u8868\u8FBE\u98CE\u683C", ["\u53E3\u8BED\u5316", "\u8F7B\u677E", "\u5148\u7ED9\u7ED3\u8BBA"]]
  ].map(([title, tags]) => /* @__PURE__ */ React.createElement("div", { key: title, style: {
    borderRadius: 18,
    border: `1px solid ${T.hairlineSoft}`,
    background: "rgba(250,252,254,.72)",
    padding: 16,
    minHeight: 146
  } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 15, fontWeight: 760, marginBottom: 12 } }, title), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, flexWrap: "wrap" } }, tags.map((tag) => /* @__PURE__ */ React.createElement("span", { key: tag, style: {
    minHeight: 30,
    padding: "6px 10px",
    borderRadius: 999,
    background: "rgba(255,255,255,.78)",
    border: `1px solid ${T.hairlineSoft}`,
    color: T.navyMid,
    fontSize: 12.4,
    lineHeight: 1.35,
    fontWeight: 620
  } }, tag))))))), /* @__PURE__ */ React.createElement(InsightPanel, null, /* @__PURE__ */ React.createElement(PanelHeader, { title: "\u8FD0\u8425\u8BA1\u5212\u6458\u8981", action: "\u67E5\u770B\u5B8C\u6574\u8FD0\u8425\u8BA1\u5212" }), /* @__PURE__ */ React.createElement("div", { style: {
    display: "grid",
    gridTemplateColumns: mobile ? "1fr" : "repeat(3, minmax(0, 1fr))"
  } }, [
    ["\u9009\u9898\u5E93", "\u7B2C\u4E00\u6B21\u6765\u600E\u4E48\u70B9\u3001\u9644\u8FD1\u5348\u9910\u4E0D\u8E29\u96F7\u3001\u8001\u677F\u7684\u4E00\u5929"],
    ["\u53D1\u5E03\u8282\u594F", "\u4E00\u5468 7 \u7BC7\uFF0C\u56FE\u6587\u548C\u77ED\u89C6\u9891\u4EA4\u66FF\uFF0C\u5148\u9A8C\u8BC1\u6536\u85CF\u7387"],
    ["\u6570\u636E\u76EE\u6807", "7 \u5929\u9A8C\u8BC1\u4E00\u5957\u7A33\u5B9A\u6807\u9898\u7ED3\u6784\uFF0C\u91CD\u70B9\u770B\u6536\u85CF\u548C\u51C0\u6DA8\u7C89"]
  ].map(([title, body], index) => /* @__PURE__ */ React.createElement("div", { key: title, style: {
    padding: mobile ? 22 : 26,
    borderTop: mobile || index < 3 ? `1px solid ${T.hairlineSoft}` : "none",
    borderRight: !mobile && index < 2 ? `1px solid ${T.hairlineSoft}` : "none"
  } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.iris, fontSize: 13, fontWeight: 840, marginBottom: 10 } }, title), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 14.5, lineHeight: 1.68, fontWeight: 650 } }, body))))));
  var ToggleSwitch = ({ on }) => /* @__PURE__ */ React.createElement("span", { style: {
    width: 54,
    height: 32,
    borderRadius: 999,
    background: on ? T.success : "rgba(14,14,44,.12)",
    padding: 3,
    display: "inline-flex",
    justifyContent: on ? "flex-end" : "flex-start",
    boxShadow: "inset 0 1px 2px rgba(14,14,44,.12)"
  } }, /* @__PURE__ */ React.createElement("span", { style: { width: 26, height: 26, borderRadius: "50%", background: T.white, boxShadow: T.shadowSm } }));
  var InsightCalendarTab = ({ mobile, calendar }) => {
    const [range, setRange] = React.useState("\u672C\u5468");
    const [anchorDate, setAnchorDate] = React.useState("2026-05-18");
    const dayNumbers = ["18", "19", "20", "21", "22", "23", "24"];
    const times = ["09:00", "11:30", "14:00", "16:30", "20:00"];
    const eventColors = [
      { bg: "rgba(239,239,253,.82)", border: "rgba(75,77,237,.16)", fg: T.iris },
      { bg: "rgba(224,250,244,.78)", border: "rgba(49,208,170,.16)", fg: T.success },
      { bg: "rgba(245,255,224,.88)", border: "rgba(214,255,0,.28)", fg: "#6e8400" },
      { bg: "rgba(253,245,245,.88)", border: "rgba(243,219,218,.95)", fg: T.navyMid }
    ];
    const events = calendar.map((item, index) => ({
      ...item,
      date: dayNumbers[index] || `${18 + index}`,
      time: times[index % times.length],
      top: 34 + index % 5 * 68,
      height: index % 3 === 1 ? 92 : 78,
      tone: eventColors[index % eventColors.length]
    }));
    if (mobile) {
      return /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 18 } }, /* @__PURE__ */ React.createElement(InsightPanel, { style: { padding: 16 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10, marginBottom: 14 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 18, fontWeight: 700 } }, "2026 \u5E74 5 \u6708"), /* @__PURE__ */ React.createElement(InsightRangeToggle, { options: ["\u672C\u5468", "\u4E0B\u5468", "\u672C\u6708"], value: range, onChange: setRange }), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "minmax(0, 1fr) auto", gap: 10 } }, /* @__PURE__ */ React.createElement(
        "input",
        {
          type: "date",
          value: anchorDate,
          onChange: (e) => setAnchorDate(e.target.value),
          style: {
            height: 40,
            borderRadius: 13,
            border: `1px solid ${T.hairlineSoft}`,
            background: "rgba(255,255,255,.80)",
            color: T.navyMid,
            padding: "0 12px",
            fontFamily: T.fontSans,
            fontSize: 13,
            outline: "none"
          }
        }
      ), /* @__PURE__ */ React.createElement("button", { style: { ...pillButtonStyle(false), height: 40, borderRadius: 13, justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "plus", size: 15 }), "\u65B0\u589E\u5185\u5BB9"))), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10 } }, events.map((item, index) => /* @__PURE__ */ React.createElement("div", { key: `${item.day}-${index}`, style: {
        borderRadius: 18,
        border: `1px solid ${item.tone.border}`,
        background: item.tone.bg,
        padding: 14,
        display: "grid",
        gridTemplateColumns: "58px minmax(0, 1fr)",
        gap: 12
      } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: item.tone.fg, fontSize: 12, fontFamily: T.fontMono, fontWeight: 720 } }, item.time), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 7, color: T.navyLight, fontSize: 12, fontWeight: 650 } }, item.day)), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("span", { style: { color: item.tone.fg, fontSize: 12, fontWeight: 760 } }, item.type), /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 11.5 } }, item.date, " \u65E5")), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 7, color: T.navy, fontSize: 14.2, lineHeight: 1.5, fontWeight: 660 } }, item.topic), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 8, color: T.navyLight, fontSize: 12.2, lineHeight: 1.5 } }, item.ref)))))));
    }
    return /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 24 } }, /* @__PURE__ */ React.createElement(InsightPanel, { style: { padding: 0 } }, /* @__PURE__ */ React.createElement("div", { style: {
      height: 62,
      padding: "0 22px",
      borderBottom: `1px solid ${T.hairlineSoft}`,
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: 14
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "baseline", gap: 12 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 18, fontWeight: 700 } }, "2026 \u5E74 5 \u6708")), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "flex-end", gap: 10, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement(InsightRangeToggle, { options: ["\u672C\u5468", "\u4E0B\u5468", "\u672C\u6708"], value: range, onChange: setRange }), /* @__PURE__ */ React.createElement(
      "input",
      {
        type: "date",
        value: anchorDate,
        onChange: (e) => setAnchorDate(e.target.value),
        style: {
          height: 38,
          borderRadius: 13,
          border: `1px solid ${T.hairlineSoft}`,
          background: "rgba(255,255,255,.78)",
          color: T.navyMid,
          padding: "0 10px",
          fontFamily: T.fontSans,
          fontSize: 12.5,
          outline: "none"
        }
      }
    ), /* @__PURE__ */ React.createElement("button", { style: { ...pillButtonStyle(false), height: 38, borderRadius: 13, justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "plus", size: 15 }), "\u65B0\u589E\u5185\u5BB9"))), /* @__PURE__ */ React.createElement("div", { style: {
      display: "grid",
      gridTemplateColumns: "74px repeat(7, minmax(120px, 1fr))",
      overflowX: "auto"
    } }, /* @__PURE__ */ React.createElement("div", { style: { borderRight: `1px solid ${T.hairlineSoft}`, background: "rgba(250,252,254,.58)" } }, /* @__PURE__ */ React.createElement("div", { style: { height: 58, borderBottom: `1px solid ${T.hairlineSoft}` } }), times.map((time) => /* @__PURE__ */ React.createElement("div", { key: time, style: {
      height: 68,
      padding: "12px 12px 0",
      borderBottom: `1px solid ${T.hairlineSoft}`,
      color: T.navyLight,
      fontSize: 11.5,
      fontFamily: T.fontMono
    } }, time))), events.map((day, index) => /* @__PURE__ */ React.createElement("div", { key: `${day.day}-${index}`, style: { minWidth: 120, borderRight: index === events.length - 1 ? "none" : `1px solid ${T.hairlineSoft}`, position: "relative", minHeight: 398 } }, /* @__PURE__ */ React.createElement("div", { style: {
      height: 58,
      borderBottom: `1px solid ${T.hairlineSoft}`,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      flexDirection: "column",
      gap: 4,
      background: index === 3 ? "rgba(239,239,253,.34)" : "rgba(255,255,255,.28)"
    } }, /* @__PURE__ */ React.createElement("div", { style: { color: index === 3 ? T.iris : T.navy, fontSize: 13.2, fontWeight: 720 } }, day.day), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 11.5, fontFamily: T.fontMono } }, "05/", day.date)), times.map((time) => /* @__PURE__ */ React.createElement("div", { key: time, style: { height: 68, borderBottom: `1px solid ${T.hairlineSoft}`, background: index === 3 ? "rgba(239,239,253,.16)" : "transparent" } })), /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      left: 10,
      right: 10,
      top: day.top,
      minHeight: day.height,
      borderRadius: 16,
      border: `1px solid ${day.tone.border}`,
      background: day.tone.bg,
      boxShadow: "0 10px 22px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.66)",
      padding: 12,
      overflow: "hidden"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8, marginBottom: 8 } }, /* @__PURE__ */ React.createElement("span", { style: { color: day.tone.fg, fontSize: 11.5, fontWeight: 760 } }, day.type), /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 10.5, fontFamily: T.fontMono } }, day.time)), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 13.1, lineHeight: 1.42, fontWeight: 660 } }, day.topic), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 7, color: T.navyLight, fontSize: 11.5, lineHeight: 1.4 } }, day.ref)))))));
  };
  var MineAssetLibraryTab = ({ mobile }) => {
    const categories = ["\u5A92\u4F53\u5E93", "\u54C1\u724C\u98CE\u683C", "\u54C1\u724C\u58F0\u97F3", "\u54C1\u724C\u7B80\u4ECB", "\u539F\u59CB\u8D44\u6599"];
    const media = [
      { src: PLANNING_BENCHMARK_PHOTOS[0], title: "\u62DB\u724C\u83DC\u4FEF\u62CD", used: true },
      { src: PLANNING_BENCHMARK_PHOTOS[1], title: "\u95E8\u5E97\u73AF\u5883", used: false },
      { src: PLANNING_BENCHMARK_PHOTOS[2], title: "\u5348\u9910\u5957\u9910", used: true },
      { src: "./src/onion-burst-real.png", title: "\u83DC\u5355\u622A\u56FE", used: true },
      { src: "./src/onion-burst-collage.png", title: "\u8BC4\u8BBA\u622A\u56FE\u5408\u96C6", used: false },
      { src: "./src/inspiration-skill-card.png", title: "\u6D3B\u52A8\u6D77\u62A5\u53C2\u8003", used: true },
      { src: "./src/insight-avatar-reference.png", title: "\u8D26\u53F7\u5934\u50CF\u53C2\u8003", used: false },
      { src: "./src/onion-burst-ring.png", title: "\u54C1\u724C\u89C6\u89C9\u7D20\u6750", used: true }
    ];
    return /* @__PURE__ */ React.createElement("div", { style: {
      display: "grid",
      gridTemplateColumns: mobile ? "1fr" : "180px minmax(0, 1fr)",
      gap: mobile ? 18 : 26,
      alignItems: "start"
    } }, /* @__PURE__ */ React.createElement(InsightPanel, { style: { padding: mobile ? 10 : 12 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 2 } }, categories.map((item, index) => /* @__PURE__ */ React.createElement("button", { key: item, style: {
      height: 44,
      border: `1px solid ${index === 0 ? "rgba(75,77,237,.16)" : "transparent"}`,
      background: index === 0 ? "rgba(239,239,253,.70)" : "transparent",
      color: index === 0 ? T.iris : T.navyLight,
      cursor: "pointer",
      textAlign: "left",
      padding: "0 16px",
      borderRadius: 13,
      fontSize: 13.4,
      fontWeight: index === 0 ? 760 : 650,
      fontFamily: T.fontSans,
      boxShadow: index === 0 ? "inset 0 1px 0 rgba(255,255,255,.78)" : "none"
    } }, item)))), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: mobile ? 18 : 24 } }, /* @__PURE__ */ React.createElement(InsightPanel, { style: { padding: mobile ? 22 : 30 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 16, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("h2", { style: { margin: 0, color: T.navy, fontSize: mobile ? 28 : 34, lineHeight: 1.16, fontWeight: 710 } }, "\u5A92\u4F53\u5E93"), /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 16, fontWeight: 650 } }, "12 \u5F20\u56FE\u7247\uFF0C0 \u4E2A\u89C6\u9891")), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 28, color: T.navy, fontSize: mobile ? 19 : 22, lineHeight: 1.32, fontWeight: 720 } }, "\u6DFB\u52A0\u5A92\u4F53\u5185\u5BB9\uFF0C\u4FDD\u6301\u5185\u5BB9\u65B0\u9C9C\u5EA6"), /* @__PURE__ */ React.createElement("p", { style: { margin: "8px 0 0", maxWidth: 760, color: T.navyMid, fontSize: 14.2, lineHeight: 1.74 } }, "Nori \u4F7F\u7528\u4F60\u7684\u56FE\u7247\u548C\u89C6\u9891\uFF0C\u6839\u636E\u4F60\u7684\u8425\u9500\u6D3B\u52A8\u521B\u5EFA\u76F8\u5173\u7684\u793E\u4EA4\u5A92\u4F53\u5E16\u5B50\u3001\u516C\u4F17\u53F7\u5185\u5BB9\u548C\u77ED\u89C6\u9891\u811A\u672C\u3002")), /* @__PURE__ */ React.createElement("button", { style: { ...pillButtonStyle(true), height: 42, borderRadius: 14, justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "plus", size: 15 }), "\u6DFB\u52A0\u65B0\u5A92\u4F53"))), /* @__PURE__ */ React.createElement("div", { style: {
      display: "grid",
      gridTemplateColumns: mobile ? "repeat(2, minmax(0, 1fr))" : "repeat(4, minmax(0, 1fr))",
      gap: mobile ? 14 : 22
    } }, media.map((item, index) => /* @__PURE__ */ React.createElement("div", { key: item.title, style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: {
      position: "relative",
      aspectRatio: "1 / 1",
      borderRadius: 20,
      overflow: "hidden",
      background: T.surface,
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: "0 12px 28px rgba(14,14,44,.065)"
    } }, /* @__PURE__ */ React.createElement("img", { src: item.src, alt: "", style: { width: "100%", height: "100%", objectFit: "cover", display: "block" } }), /* @__PURE__ */ React.createElement("span", { style: {
      position: "absolute",
      left: 13,
      top: 13,
      width: 24,
      height: 24,
      borderRadius: 7,
      border: `1px solid ${T.hairline}`,
      background: "rgba(255,255,255,.88)",
      boxShadow: "0 6px 14px rgba(14,14,44,.09)"
    } }), item.used && /* @__PURE__ */ React.createElement("span", { style: {
      position: "absolute",
      left: 13,
      bottom: 13,
      height: 28,
      padding: "0 11px",
      borderRadius: 999,
      background: "rgba(255,255,255,.86)",
      color: T.navyMid,
      display: "inline-flex",
      alignItems: "center",
      fontSize: 12.2,
      fontWeight: 650,
      backdropFilter: "blur(10px)"
    } }, "\u7528\u8FC7\u7684")), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 14, color: T.navy, fontSize: 14.5, lineHeight: 1.35, fontWeight: 650, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" } }, item.title), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 5, color: T.navyLight, fontSize: 12.4, lineHeight: 1.45 } }, "\u56FE\u50CF \xB7 ", index < 4 ? "6 \u5929\u524D\u4E0A\u4F20" : "\u4ECA\u5929\u52A0\u5165"))))));
  };
  var InsightHotTab = ({ mobile }) => /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: mobile ? 18 : 24 } }, /* @__PURE__ */ React.createElement(InsightPanel, { style: { padding: mobile ? 24 : 30 } }, /* @__PURE__ */ React.createElement("div", { style: {
    display: "grid",
    gridTemplateColumns: mobile ? "1fr" : "minmax(0, 1fr) auto",
    gap: 18,
    alignItems: "center"
  } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10, marginBottom: 12 } }, /* @__PURE__ */ React.createElement("span", { style: {
    height: 28,
    padding: "0 12px",
    borderRadius: 999,
    background: T.navy,
    color: T.primary,
    fontSize: 13,
    fontWeight: 860,
    fontFamily: T.fontMono,
    display: "inline-flex",
    alignItems: "center"
  } }, "PRO"), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 13, fontWeight: 820 } }, "\u70ED\u70B9\u673A\u4F1A\u96F7\u8FBE")), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: mobile ? 21 : 24, lineHeight: 1.32, fontWeight: 740 } }, "\u4ECA\u5929\u9002\u5408\u8FFD\u300C\u4E0A\u6D77\u996D\u5E97\u63A8\u8350 / \u5348\u5E02\u5957\u9910\u300D\uFF0C\u4E0D\u5EFA\u8BAE\u8FFD\u6CDB\u5A31\u4E50\u70ED\u8BCD\u3002"), /* @__PURE__ */ React.createElement("p", { style: { margin: "12px 0 0", maxWidth: 720, color: T.navyMid, fontSize: 14.5, lineHeight: 1.7 } }, "Nori \u4F1A\u6839\u636E\u4F60\u7684\u95E8\u5E97\u5B9A\u4F4D\u8FC7\u6EE4\u70ED\u70B9\uFF0C\u53EA\u7559\u4E0B\u65E2\u6709\u589E\u957F\u7A7A\u95F4\u3001\u53C8\u4E0D\u7834\u574F\u5C0F\u996D\u5E97\u771F\u5B9E\u611F\u7684\u9009\u9898\u3002")), /* @__PURE__ */ React.createElement("button", { style: { ...pillButtonStyle(true), justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "bell", size: 16 }), "\u7ED1\u5B9A\u98DE\u4E66\u65E5\u62A5"))), /* @__PURE__ */ React.createElement("div", { style: {
    display: "grid",
    gridTemplateColumns: mobile ? "1fr" : "minmax(0, 1.35fr) minmax(320px, .72fr)",
    gap: mobile ? 18 : 24,
    alignItems: "stretch"
  } }, /* @__PURE__ */ React.createElement(InsightPanel, null, /* @__PURE__ */ React.createElement(PanelHeader, { title: "\u53EF\u8FFD\u70ED\u70B9", action: "\u5237\u65B0\u96F7\u8FBE" }), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", padding: mobile ? "0 20px 8px" : "0 26px 10px" } }, INSIGHT_HOT_TOPICS.map((topic) => /* @__PURE__ */ React.createElement("div", { key: topic.tag, style: {
    display: "grid",
    gridTemplateColumns: mobile ? "1fr" : "minmax(0, 1fr) 96px 112px auto",
    gap: 16,
    padding: "20px 0",
    borderBottom: `1px solid ${T.hairlineSoft}`,
    alignItems: "center"
  } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 16, fontWeight: 760 } }, topic.tag), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 8, color: T.navyLight, fontSize: 13.2, lineHeight: 1.62 } }, topic.note)), /* @__PURE__ */ React.createElement("div", { style: { color: T.iris, fontSize: 13, fontWeight: 820 } }, topic.fit), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyMid, fontSize: 13, fontWeight: 720 } }, topic.format), /* @__PURE__ */ React.createElement("div", { style: { color: T.success, fontSize: 16, fontWeight: 840, fontFamily: T.fontMono } }, topic.change))))), /* @__PURE__ */ React.createElement(InsightPanel, { style: { padding: mobile ? 24 : 30 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 13, fontWeight: 840, marginBottom: 12 } }, "\u63A8\u9001\u6E20\u9053"), /* @__PURE__ */ React.createElement("h2", { style: { margin: "0 0 26px", color: T.navy, fontSize: mobile ? 22 : 24, fontWeight: 740 } }, "\u98DE\u4E66 / \u5FAE\u4FE1 \u65E5\u62A5"), [
    { name: "\u98DE\u4E66", sub: "@\u5DF7\u53E3\u6696\u80C3\u5C0F\u9986 \xB7 \u6BCF\u65E5 09:00 \xB7 \u70ED\u70B9 + \u6628\u65E5\u6570\u636E", on: true, tag: "\u5DF2\u5F00\u542F" },
    { name: "\u5FAE\u4FE1", sub: '\u672A\u7ED1\u5B9A \xB7 \u901A\u8FC7\u516C\u4F17\u53F7"Nori \u64AD\u62A5"\u63A5\u6536', on: false, tag: "\u5F85\u7ED1\u5B9A" }
  ].map((row, index) => /* @__PURE__ */ React.createElement("div", { key: row.name, style: {
    display: "grid",
    gridTemplateColumns: "minmax(0, 1fr) auto",
    gap: 16,
    alignItems: "center",
    padding: "26px 0",
    borderTop: index === 0 ? `1px solid ${T.hairlineSoft}` : `1px solid ${T.hairline}`
  } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 18, fontWeight: 860 } }, row.name), /* @__PURE__ */ React.createElement("span", { style: { color: row.on ? T.success : T.navyLight, fontSize: 12, fontWeight: 820 } }, row.tag)), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 8, color: T.navyLight, fontSize: 14, lineHeight: 1.6, fontWeight: 680 } }, row.sub)), /* @__PURE__ */ React.createElement(ToggleSwitch, { on: row.on }))))));
  var InsightsPage = ({ onBackHome, onOpenAssets, onOpenMine, onNewChat, initialTab = "review" }) => {
    const { isTablet, isMobile } = useViewport();
    const [navCollapsed, setNavCollapsed] = React.useState(false);
    const [activeTab, setActiveTab] = React.useState(initialTab);
    const [platformTab, setPlatformTab] = React.useState("overall");
    const [refreshing, setRefreshing] = React.useState(false);
    const sessions = INSIGHT_CONTENTS.map((item) => item.title);
    const savedPlanCalendar = React.useMemo(() => loadPlanDraft()?.calendar || DEFAULT_ACCOUNT_PLAN_CALENDAR, []);
    React.useEffect(() => {
      setActiveTab(initialTab);
    }, [initialTab]);
    const refresh = () => {
      setRefreshing(true);
      window.setTimeout(() => setRefreshing(false), 620);
    };
    return /* @__PURE__ */ React.createElement("div", { style: {
      display: "flex",
      width: "100%",
      height: "100%",
      overflow: "hidden",
      background: T.surfaceWh,
      color: T.navy,
      fontFamily: T.fontSans
    } }, !isTablet && /* @__PURE__ */ React.createElement(
      Sidebar,
      {
        active: "insights",
        onNew: onNewChat,
        onNavigate: (id) => {
          if (id === "home") onBackHome();
          if (id === "library") onOpenAssets && onOpenAssets();
          if (id === "mine") onOpenMine && onOpenMine();
        },
        sessions,
        collapsed: navCollapsed,
        onToggle: () => setNavCollapsed((v) => !v)
      }
    ), /* @__PURE__ */ React.createElement("main", { style: {
      flex: 1,
      minWidth: 0,
      overflow: "auto",
      position: "relative",
      background: "linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      inset: 0,
      background: "radial-gradient(circle at 18% 12%, rgba(214,255,0,.14), transparent 18%), radial-gradient(circle at 82% 10%, rgba(75,77,237,.08), transparent 22%), radial-gradient(circle at 63% 72%, rgba(49,208,170,.06), transparent 22%)",
      pointerEvents: "none"
    } }), /* @__PURE__ */ React.createElement("div", { style: {
      position: "relative",
      zIndex: 1,
      maxWidth: 1640,
      margin: "0 auto",
      padding: isMobile ? "18px 18px 36px" : "28px 30px 50px"
    } }, isTablet && /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement(NoriLogo, { size: 28 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 15, fontWeight: 760, color: T.navy } }, "\u6570\u636E\u6D1E\u5BDF"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11, color: T.navyLight } }, "\u590D\u76D8\u4E0E\u70ED\u70B9\u5DE5\u4F5C\u53F0"))), /* @__PURE__ */ React.createElement("button", { onClick: onBackHome, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "home", size: 16, color: T.navyMid }))), /* @__PURE__ */ React.createElement(
      InsightTopBar,
      {
        active: activeTab,
        onChange: setActiveTab,
        mobile: isMobile
      }
    ), /* @__PURE__ */ React.createElement("div", { style: { animation: refreshing ? "fadeInScale .32s ease both" : "none" } }, activeTab === "review" && /* @__PURE__ */ React.createElement(InsightReviewTab, { mobile: isMobile, compact: isTablet && !isMobile, platform: platformTab, onPlatformChange: setPlatformTab }), activeTab === "hot" && /* @__PURE__ */ React.createElement(InsightHotTab, { mobile: isMobile })))));
  };
  window.InsightsPage = InsightsPage;
  var MinePage = ({ onBackHome, onOpenAssets, onOpenInsights, onNewChat }) => {
    const { isTablet, isMobile } = useViewport();
    const [navCollapsed, setNavCollapsed] = React.useState(false);
    const [activeTab, setActiveTab] = React.useState("profile");
    const savedPlanCalendar = React.useMemo(() => loadPlanDraft()?.calendar || DEFAULT_ACCOUNT_PLAN_CALENDAR, []);
    const sessions = ["\u6211\u7684\u8D26\u53F7\u5B9A\u4F4D", "\u672C\u5468\u5185\u5BB9\u65E5\u5386", "\u8D26\u53F7\u89C4\u5212\u6587\u6863"];
    const tabs = [
      { id: "profile", label: "\u8D26\u53F7\u5B9A\u4F4D" },
      { id: "calendar", label: "\u5185\u5BB9\u65E5\u5386" },
      { id: "assets", label: "\u8D44\u4EA7\u5E93" }
    ];
    return /* @__PURE__ */ React.createElement("div", { style: {
      display: "flex",
      width: "100%",
      height: "100%",
      overflow: "hidden",
      background: T.surfaceWh,
      color: T.navy,
      fontFamily: T.fontSans
    } }, !isTablet && /* @__PURE__ */ React.createElement(
      Sidebar,
      {
        active: "mine",
        onNew: onNewChat,
        onNavigate: (id) => {
          if (id === "home") onBackHome();
          if (id === "library") onOpenAssets && onOpenAssets();
          if (id === "insights") onOpenInsights && onOpenInsights();
        },
        sessions,
        collapsed: navCollapsed,
        onToggle: () => setNavCollapsed((v) => !v)
      }
    ), /* @__PURE__ */ React.createElement("main", { style: {
      flex: 1,
      minWidth: 0,
      overflow: "auto",
      position: "relative",
      background: "linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      inset: 0,
      background: "radial-gradient(circle at 18% 12%, rgba(214,255,0,.12), transparent 18%), radial-gradient(circle at 82% 10%, rgba(75,77,237,.07), transparent 22%), radial-gradient(circle at 63% 72%, rgba(49,208,170,.06), transparent 22%)",
      pointerEvents: "none"
    } }), /* @__PURE__ */ React.createElement("div", { style: {
      position: "relative",
      zIndex: 1,
      maxWidth: 1440,
      margin: "0 auto",
      padding: isMobile ? "18px 18px 36px" : "30px 34px 54px"
    } }, isTablet && /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement(NoriLogo, { size: 28 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 15, fontWeight: 760, color: T.navy } }, "\u6211\u7684"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11, color: T.navyLight } }, "\u8D26\u53F7\u5B9A\u4F4D\u3001\u5185\u5BB9\u65E5\u5386\u4E0E\u8D44\u4EA7\u5E93"))), /* @__PURE__ */ React.createElement("button", { onClick: onBackHome, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "home", size: 16, color: T.navyMid }))), /* @__PURE__ */ React.createElement("header", { style: {
      display: "flex",
      flexDirection: isMobile ? "column" : "row",
      justifyContent: "space-between",
      alignItems: isMobile ? "stretch" : "flex-end",
      gap: isMobile ? 18 : 24,
      marginBottom: isMobile ? 22 : 28
    } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12, fontWeight: 800, letterSpacing: "0.08em", textTransform: "uppercase", color: T.navyLight, marginBottom: 8 } }, "Mine"), /* @__PURE__ */ React.createElement("h1", { style: { margin: 0, fontSize: isMobile ? 27 : 34, lineHeight: 1.14, color: T.navy, fontWeight: 720 } }, "\u6211\u7684"), /* @__PURE__ */ React.createElement("p", { style: { margin: "10px 0 0", maxWidth: 640, fontSize: 14, lineHeight: 1.68, color: T.navyMid } }, "\u8FD9\u91CC\u653E\u4F60\u7684\u8D26\u53F7\u5B9A\u4F4D\u3001\u8FD0\u8425\u8BA1\u5212\u3001\u5185\u5BB9\u6392\u671F\u548C\u54C1\u724C\u8D44\u4EA7\u3002")), /* @__PURE__ */ React.createElement(LargeSegmentedTabs, { tabs, active: activeTab, onChange: setActiveTab, mobile: isMobile, minWidth: 338 })), activeTab === "profile" && /* @__PURE__ */ React.createElement(InsightProfileTab, { mobile: isMobile }), activeTab === "calendar" && /* @__PURE__ */ React.createElement(InsightCalendarTab, { mobile: isMobile, calendar: savedPlanCalendar }), activeTab === "assets" && /* @__PURE__ */ React.createElement(MineAssetLibraryTab, { mobile: isMobile }))));
  };
  window.MinePage = MinePage;
  var Avatar = ({ kind = "nori" }) => {
    if (kind === "user") {
      return /* @__PURE__ */ React.createElement("div", { style: {
        width: 28,
        height: 28,
        borderRadius: "50%",
        flexShrink: 0,
        background: `linear-gradient(135deg, ${T.iris}, ${T.peach})`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        color: T.white,
        fontSize: 11.5,
        fontWeight: 700
      } }, "L");
    }
    return null;
  };
  var Bubble = ({ from = "nori", children, style }) => {
    const isUser = from === "user";
    return /* @__PURE__ */ React.createElement("div", { style: {
      display: "grid",
      gridTemplateColumns: isUser ? "minmax(0, 1fr) 36px" : "minmax(0, 1fr)",
      gap: isUser ? 12 : 0,
      alignItems: "flex-start",
      animation: `${isUser ? "userMessageReveal .72s" : "messageReveal 1.04s"} ${T.ease} both`,
      width: "100%",
      ...style
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      gridColumn: 1,
      justifySelf: isUser ? "end" : "start",
      width: isUser ? "fit-content" : "100%",
      maxWidth: isUser ? "calc(100% - 52px)" : "100%",
      minWidth: 0,
      padding: isUser ? "10px 14px" : 0,
      borderRadius: isUser ? 16 : 0,
      background: isUser ? "rgba(255,255,255,.88)" : "transparent",
      color: isUser ? T.navyMid : T.navy,
      boxShadow: isUser ? "0 8px 18px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.84)" : "none",
      border: isUser ? `1px solid ${T.hairlineSoft}` : "none",
      fontSize: 14,
      lineHeight: 1.72,
      fontWeight: 440
    } }, children), isUser && /* @__PURE__ */ React.createElement("div", { style: { gridColumn: 2, justifySelf: "end", paddingTop: 1 } }, /* @__PURE__ */ React.createElement(Avatar, { kind: "user" })));
  };
  var NoriSays = ({ children, style }) => /* @__PURE__ */ React.createElement(AgentReply, { style }, children);
  var TypingDots = () => /* @__PURE__ */ React.createElement("div", { style: { display: "inline-flex", gap: 3, padding: "4px 0" } }, [0, 1, 2].map((i) => /* @__PURE__ */ React.createElement("span", { key: i, style: {
    width: 5,
    height: 5,
    borderRadius: "50%",
    background: T.navyLight,
    animation: `pulse 1.2s ${i * 0.15}s infinite`
  } })));
  var AGENT_CARD_WIDTH = "min(100%, 664px)";
  var NoriThinkingOnion = ({ style }) => /* @__PURE__ */ React.createElement("div", { style: {
    width: AGENT_CARD_WIDTH,
    display: "flex",
    alignItems: "center",
    minHeight: 30,
    animation: `agentFadeIn .22s ${T.ease} both`,
    ...style
  } }, /* @__PURE__ */ React.createElement("span", { style: {
    width: 20,
    height: 20,
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    animation: "agentOnionThink 1.18s ease-in-out infinite",
    transformOrigin: "50% 50%"
  } }, /* @__PURE__ */ React.createElement("img", { src: NORI_LOGO_SRC, alt: "", style: { width: 18, height: 18, objectFit: "contain", display: "block" } })));
  var AgentReply = ({ children, style }) => /* @__PURE__ */ React.createElement(Bubble, { from: "nori", style: { width: AGENT_CARD_WIDTH, ...style } }, /* @__PURE__ */ React.createElement("div", { style: {
    paddingTop: 1,
    color: T.navyMid,
    fontSize: 13.4,
    lineHeight: 1.74,
    fontWeight: 460,
    whiteSpace: "pre-wrap"
  } }, children));
  var AgentCardShell = ({ label = "Agent", icon = "sparkles", title, children, action, defaultOpen = true, style, bodyStyle }) => {
    const [open, setOpen] = React.useState(defaultOpen);
    return /* @__PURE__ */ React.createElement("section", { style: {
      width: AGENT_CARD_WIDTH,
      borderRadius: 20,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.82)",
      boxShadow: "0 14px 34px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.84)",
      backdropFilter: "blur(18px) saturate(1.14)",
      padding: 15,
      display: "grid",
      gap: open ? 12 : 0,
      animation: `messageReveal .72s ${T.ease} both`,
      ...style
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "minmax(0, 1fr) 30px", gap: 10, alignItems: "start" } }, /* @__PURE__ */ React.createElement("div", { style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "inline-flex", alignItems: "center", gap: 6, color: T.navyLight, fontSize: 11.2, lineHeight: 1.3, fontWeight: 650, marginBottom: 6 } }, /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 12 }), label), title && /* @__PURE__ */ React.createElement("h3", { style: { margin: 0, color: T.navy, fontSize: 15.2, lineHeight: 1.42, fontWeight: 730 } }, title)), /* @__PURE__ */ React.createElement("button", { onClick: () => setOpen((v) => !v), "aria-label": open ? "\u6298\u53E0" : "\u5C55\u5F00", style: {
      width: 30,
      height: 30,
      borderRadius: 10,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(250,252,254,.74)",
      color: T.navyLight,
      cursor: "pointer",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: open ? "chevronDown" : "chevronRight", size: 13 }))), open && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyMid, fontSize: 12.9, lineHeight: 1.68, fontWeight: 460, ...bodyStyle } }, children), action && /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end", gap: 8, flexWrap: "wrap" } }, action)));
  };
  var AgentChoice = ({ children, active, multiple = false, onClick }) => /* @__PURE__ */ React.createElement("button", { onClick, style: {
    minHeight: 34,
    borderRadius: 999,
    border: `1px solid ${active ? "rgba(14,14,44,.16)" : T.hairlineSoft}`,
    background: active ? "rgba(14,14,44,.92)" : "rgba(255,255,255,.78)",
    color: active ? T.white : T.navyMid,
    cursor: "pointer",
    display: "inline-flex",
    alignItems: "center",
    gap: 8,
    padding: "0 12px 0 10px",
    fontSize: 12.4,
    lineHeight: 1,
    fontWeight: active ? 690 : 560,
    boxShadow: active ? "0 10px 20px rgba(14,14,44,.12)" : "0 6px 14px rgba(14,14,44,.035)",
    transition: `transform .22s ${T.spring}, background .2s ${T.ease}, color .2s ${T.ease}, box-shadow .22s ${T.spring}`
  } }, /* @__PURE__ */ React.createElement("span", { style: {
    width: 15,
    height: 15,
    borderRadius: multiple ? 5 : "50%",
    border: `1.4px solid ${active ? "rgba(255,255,255,.76)" : "rgba(14,14,44,.18)"}`,
    background: active ? T.primary : "rgba(255,255,255,.58)",
    color: active ? T.navy : "transparent",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0
  } }, active && /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 9, stroke: 2.6 })), children);
  var AgentParseFlow = ({
    messages = ["\u89E3\u6790\u4E2D", "\u6B63\u5728\u5206\u6790\u4F60\u7684\u5185\u5BB9", "\u6B63\u5728\u6574\u7406\u7ED3\u8BBA"],
    conclusion = "\u5DF2\u7ECF\u5B8C\u6210\u89E3\u6790",
    steps = [],
    active = true,
    showThinking = true,
    settled,
    initialOpen = false,
    resetKey,
    style
  }) => {
    const controlled = typeof settled === "boolean";
    const [phase, setPhase] = React.useState(showThinking ? 0 : settled ? 2 : 1);
    const [open, setOpen] = React.useState(initialOpen);
    const [messageIndex, setMessageIndex] = React.useState(0);
    React.useEffect(() => {
      if (!active) return void 0;
      if (controlled) {
        setPhase(showThinking ? 0 : settled ? 2 : 1);
        setMessageIndex(settled ? Math.max(0, messages.length - 1) : 0);
        const timers2 = [];
        if (showThinking && !settled) {
          timers2.push(window.setTimeout(() => setPhase(1), 720));
        }
        if (!settled && messages.length > 1) {
          const msgTimer = window.setInterval(() => {
            setMessageIndex((i) => (i + 1) % messages.length);
          }, 920);
          timers2.push(msgTimer);
        }
        return () => timers2.forEach((timer) => {
          if (typeof timer === "number") window.clearTimeout(timer);
          else window.clearInterval(timer);
        });
      }
      setPhase(showThinking ? 0 : 1);
      setMessageIndex(0);
      const timers = [];
      if (showThinking) {
        timers.push(window.setTimeout(() => setPhase(1), 720));
      }
      if (messages.length > 1) {
        const msgTimer = window.setInterval(() => {
          setMessageIndex((i) => (i + 1) % messages.length);
        }, 920);
        timers.push(msgTimer);
      }
      timers.push(window.setTimeout(() => {
        setPhase(2);
        setMessageIndex(messages.length - 1);
      }, showThinking ? 720 + 920 * Math.max(1, Math.min(messages.length, 3)) : 920 * Math.max(1, Math.min(messages.length, 3))));
      return () => timers.forEach((timer) => {
        if (typeof timer === "number") window.clearTimeout(timer);
        else window.clearInterval(timer);
      });
    }, [active, showThinking, messages.length, resetKey, controlled, settled]);
    if (!active) return null;
    const currentMessage = phase === 0 ? null : phase === 1 ? messages[messageIndex] : conclusion;
    const detailSteps = steps.length ? steps : [
      { label: "\u7406\u89E3\u8F93\u5165", text: "\u8BFB\u53D6\u7528\u6237\u521A\u521A\u63D0\u4F9B\u7684\u76EE\u6807\u3001\u7D20\u6750\u548C\u4E0A\u4E0B\u6587\u3002", note: "\u5148\u9501\u5B9A\u5185\u5BB9\u7C7B\u578B\uFF0C\u518D\u5224\u65AD\u9700\u8981\u7684\u4E0B\u4E00\u6B65\u3002" },
      { label: "\u5339\u914D\u89C4\u5219", text: "\u5BF9\u7167\u5F53\u524D\u9875\u9762\u7684\u4EFB\u52A1\u9636\u6BB5\uFF0C\u5224\u65AD\u4E0B\u4E00\u6B65\u5E94\u8BE5\u751F\u6210\u4EC0\u4E48\u3002", note: "\u907F\u514D\u628A\u5DF2\u77E5\u4FE1\u606F\u518D\u95EE\u4E00\u904D\u3002" },
      { label: "\u6574\u7406\u8F93\u51FA", text: "\u628A\u53EF\u6267\u884C\u7ED3\u8BBA\u538B\u7F29\u6210\u4E00\u6761\u56DE\u590D\uFF0C\u5E76\u51C6\u5907\u540E\u7EED\u5361\u7247\u5185\u5BB9\u3002", note: "\u8BA9\u56DE\u590D\u548C\u4E0B\u4E00\u5F20\u5361\u4E4B\u95F4\u7684\u8854\u63A5\u66F4\u987A\u3002" }
    ];
    return /* @__PURE__ */ React.createElement("div", { style: {
      width: AGENT_CARD_WIDTH,
      display: "grid",
      gap: 8,
      padding: "2px 0",
      ...style
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "flex-start", gap: 7, color: T.navyLight } }, phase === 0 ? /* @__PURE__ */ React.createElement("span", { style: {
      width: 8,
      height: 8,
      borderRadius: "50%",
      background: T.iris,
      marginTop: 6,
      animation: "agentDotPulse 0.9s ease-in-out 2",
      boxShadow: "0 0 0 0 rgba(75,77,237,.18)"
    } }) : null, /* @__PURE__ */ React.createElement("div", { style: { minWidth: 0, flex: 1 } }, phase >= 1 && /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 5, minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: {
      color: T.navyLight,
      fontSize: 12.2,
      lineHeight: 1.5,
      fontWeight: 560,
      whiteSpace: "nowrap",
      overflow: "hidden",
      textOverflow: "ellipsis"
    } }, currentMessage), /* @__PURE__ */ React.createElement("button", { onClick: () => setOpen((v) => !v), "aria-label": open ? "\u6298\u53E0" : "\u5C55\u5F00", style: {
      border: "none",
      background: "transparent",
      padding: 0,
      width: 16,
      height: 16,
      color: T.navyLight,
      cursor: "pointer",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0,
      opacity: phase >= 2 ? 0.88 : 0.42
    } }, /* @__PURE__ */ React.createElement(Icon, { name: open ? "chevronDown" : "chevronRight", size: 11 }))), open && phase >= 2 && /* @__PURE__ */ React.createElement("div", { style: {
      marginTop: 9,
      paddingLeft: 12,
      borderLeft: `1px solid ${T.hairlineSoft}`,
      display: "grid",
      gap: 8
    } }, detailSteps.map((step, index) => /* @__PURE__ */ React.createElement("div", { key: `${step.label}-${index}`, style: { display: "grid", gap: 2, color: T.navyLight, fontSize: 12.1, lineHeight: 1.58, fontWeight: 520 } }, /* @__PURE__ */ React.createElement("span", null, index + 1, " ", step.label, "\uFF1A", step.text), step.note && /* @__PURE__ */ React.createElement("span", { style: { opacity: 0.72 } }, step.note))), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, opacity: 0.62, fontSize: 11.8, lineHeight: 1.55 } }, "\u5DF2\u4FDD\u7559\u8FD9\u4E00\u6B65\u7684\u5224\u65AD\uFF0C\u540E\u7EED\u751F\u6210\u4F1A\u7EE7\u7EED\u6CBF\u7528\u3002")))));
  };
  var AgentStepSequence = ({
    parseMessages = ["\u6B63\u5728\u67E5\u770B", "\u89E3\u6790\u4E2D", "\u6B63\u5728\u7EC4\u7EC7\u56DE\u590D"],
    parseConclusion,
    parseSteps = [],
    parseOpen = false,
    reply,
    card,
    children,
    showOnion = true,
    showParse = true,
    onionMs = 980,
    parseMs = 1320,
    cardDelayMs = 520,
    onComplete,
    resetKey,
    style
  }) => {
    const hasReply = reply !== void 0 && reply !== null;
    const cardNode = card || children;
    const firstPhase = showOnion ? 0 : showParse ? 1 : 2;
    const [phase, setPhase] = React.useState(firstPhase);
    React.useEffect(() => {
      setPhase(firstPhase);
      const timers = [];
      let elapsed = 0;
      if (showOnion) {
        elapsed += onionMs;
        timers.push(window.setTimeout(() => setPhase(showParse ? 1 : 2), elapsed));
      }
      if (showParse) {
        elapsed += parseMs;
        timers.push(window.setTimeout(() => setPhase(2), elapsed));
      }
      if (cardNode) {
        elapsed += cardDelayMs;
        timers.push(window.setTimeout(() => setPhase(3), elapsed));
      }
      if (onComplete) {
        timers.push(window.setTimeout(() => onComplete(), elapsed + 40));
      }
      return () => timers.forEach(window.clearTimeout);
    }, [resetKey, showOnion, showParse, onionMs, parseMs, cardDelayMs, firstPhase, !!cardNode, onComplete]);
    return /* @__PURE__ */ React.createElement("div", { style: { width: AGENT_CARD_WIDTH, display: "grid", gap: 12, ...style } }, phase === 0 && /* @__PURE__ */ React.createElement(NoriThinkingOnion, null), phase >= 1 && showParse && /* @__PURE__ */ React.createElement(
      AgentParseFlow,
      {
        showThinking: false,
        settled: phase >= 2,
        resetKey,
        messages: parseMessages,
        conclusion: phase >= 3 ? parseConclusion || parseMessages[parseMessages.length - 1] || "\u5DF2\u7ECF\u5B8C\u6210\u89E3\u6790" : parseMessages[parseMessages.length - 1] || "\u5DF2\u7ECF\u5B8C\u6210\u89E3\u6790",
        steps: parseSteps,
        initialOpen: parseOpen
      }
    ), phase >= 2 && hasReply && /* @__PURE__ */ React.createElement(AgentReply, null, reply), phase >= 3 && cardNode && /* @__PURE__ */ React.createElement("div", { style: { width: AGENT_CARD_WIDTH, display: "grid", gap: 12, animation: `messageReveal .84s ${T.ease} both` } }, cardNode));
  };
  var isNearScrollBottom = (node, threshold = 92) => {
    if (!node) return true;
    return node.scrollHeight - node.scrollTop - node.clientHeight < threshold;
  };
  var scrollNodeToBottom = (node, behavior = "auto") => {
    if (!node) return;
    node.scrollTo({ top: node.scrollHeight, behavior });
  };
  var Step1KeyInfo = ({ onComplete, onSkip }) => {
    const [audience, setAudience] = React.useState(null);
    const [style, setStyle] = React.useState(null);
    const [length, setLength] = React.useState(null);
    const ready = audience && style && length;
    const Question = ({ q, options, value, onPick, hint }) => /* @__PURE__ */ React.createElement("div", { style: { marginBottom: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, marginBottom: 10 } }, /* @__PURE__ */ React.createElement("span", { style: { fontSize: 13.5, fontWeight: 600, color: T.navy } }, q), hint && /* @__PURE__ */ React.createElement("span", { style: { fontSize: 11.5, color: T.navyLight } }, hint)), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexWrap: "wrap", gap: 6 } }, options.map((o) => {
      const active = value === o.id;
      return /* @__PURE__ */ React.createElement("button", { key: o.id, onClick: () => onPick(o.id), style: {
        padding: "8px 14px",
        borderRadius: 99,
        border: `1px solid ${active ? T.navy : T.hairline}`,
        background: active ? T.navy : T.white,
        color: active ? T.white : T.navy,
        fontSize: 12.5,
        fontWeight: 500,
        cursor: "pointer",
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        boxShadow: active ? "0 9px 22px rgba(14,14,44,.11)" : "0 5px 14px rgba(14,14,44,.035)",
        transition: `transform .24s ${T.spring}, background .22s ${T.ease}, color .22s ${T.ease}, box-shadow .24s ${T.spring}`
      } }, o.emoji && /* @__PURE__ */ React.createElement("span", { style: { fontSize: 13 } }, o.emoji), o.label);
    })));
    return /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 16 } }, "\u597D\u4E3B\u610F\uFF01\u300C", /* @__PURE__ */ React.createElement("b", null, "\u731B\u7537\u559C\u6B22\u7684\u7C89\u8272\u690D\u7269"), "\u300D\u8FD9\u4E2A\u89D2\u5EA6\u53CD\u5DEE\u611F\u5F88\u6709\u6897\u3002\u5728\u5F00\u59CB\u524D\uFF0C \u6211\u60F3\u8DDF\u4F60\u786E\u8BA4\u51E0\u4E2A\u5173\u952E\u4FE1\u606F\uFF0C\u8FD9\u6837\u751F\u6210\u7684\u5185\u5BB9\u4F1A\u66F4\u7CBE\u51C6 \u2014\u2014"), /* @__PURE__ */ React.createElement("div", { style: {
      background: "rgba(255,255,255,.84)",
      border: `1px solid ${T.hairlineSoft}`,
      borderRadius: 18,
      padding: "18px 20px",
      boxShadow: "0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.82)",
      backdropFilter: "blur(18px) saturate(1.12)"
    } }, /* @__PURE__ */ React.createElement(
      Question,
      {
        q: "\u76EE\u6807\u8BFB\u8005\u662F\u8C01\uFF1F",
        hint: "\u9009\u4E00\u4E2A\u6700\u8D34\u8FD1\u7684\u753B\u50CF",
        value: audience,
        onPick: setAudience,
        options: [
          { id: "novice", label: "\u690D\u7269\u65B0\u624B", emoji: "\u{1F331}" },
          { id: "cat-people", label: "\u5BA0\u7269 / \u5BA4\u5185\u6D3E", emoji: "\u{1F408}" },
          { id: "gym-bro", label: "\u5065\u8EAB\u786C\u6C49", emoji: "\u{1F4AA}" },
          { id: "pro", label: "\u56ED\u827A\u8001\u624B", emoji: "\u{1FAB4}" },
          { id: "all", label: "\u6CDB\u7528\u6237" }
        ]
      }
    ), /* @__PURE__ */ React.createElement(
      Question,
      {
        q: "\u4F60\u60F3\u505A\u6210\u4EC0\u4E48\u98CE\u683C\uFF1F",
        value: style,
        onPick: setStyle,
        options: [
          { id: "edu", label: "\u786C\u6838\u79D1\u666E" },
          { id: "meme", label: "\u53CD\u5DEE\u6897 / \u6574\u6D3B" },
          { id: "visual", label: "\u989C\u503C\u5411 / \u7F8E\u56FE" },
          { id: "guide", label: "\u5B9E\u7528\u517B\u62A4" }
        ]
      }
    ), /* @__PURE__ */ React.createElement(
      Question,
      {
        q: "\u671F\u671B\u957F\u5EA6\uFF1F",
        value: length,
        onPick: setLength,
        options: [
          { id: "s", label: "\u77ED\u5E73\u5FEB \xB7 6 \u56FE\u4EE5\u5185" },
          { id: "m", label: "\u6807\u51C6 \xB7 8\u201310 \u56FE" },
          { id: "l", label: "\u6DF1\u5EA6 \xB7 \u957F\u6587 + \u56FE" }
        ]
      }
    ), /* @__PURE__ */ React.createElement("div", { style: {
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      marginTop: 6,
      paddingTop: 14,
      borderTop: `1px solid ${T.hairlineSoft}`
    } }, /* @__PURE__ */ React.createElement("button", { onClick: onSkip, style: {
      background: "transparent",
      border: "none",
      cursor: "pointer",
      color: T.navyLight,
      fontSize: 12.5,
      fontWeight: 500,
      display: "inline-flex",
      alignItems: "center",
      gap: 5,
      padding: "6px 4px"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "skip", size: 12 }), " \u8DF3\u8FC7\u8FD9\u6B65"), /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: () => onComplete({ audience, style, length }),
        disabled: !ready,
        style: {
          height: 38,
          padding: "0 18px",
          borderRadius: 10,
          border: "none",
          background: ready ? T.navy : T.surface,
          color: ready ? T.primary : T.navyLight,
          fontSize: 13,
          fontWeight: 600,
          cursor: ready ? "pointer" : "not-allowed",
          display: "inline-flex",
          alignItems: "center",
          gap: 6,
          boxShadow: ready ? T.shadowSm : "none",
          transition: `transform .24s ${T.spring}, box-shadow .24s ${T.spring}, background .22s ${T.ease}, color .22s ${T.ease}`
        }
      },
      /* @__PURE__ */ React.createElement(Icon, { name: "sparkles", size: 13 }),
      " \u5F00\u59CB\u751F\u6210"
    ))));
  };
  var HotCard = ({ post }) => {
    return /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          background: "rgba(255,255,255,.86)",
          border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 16,
          overflow: "hidden",
          cursor: "pointer",
          transition: `transform .3s ${T.spring}, box-shadow .3s ${T.spring}`,
          display: "flex",
          flexDirection: "column"
        },
        onMouseEnter: (e) => {
          e.currentTarget.style.transform = "translateY(-2px)";
          e.currentTarget.style.boxShadow = T.shadowMd;
        },
        onMouseLeave: (e) => {
          e.currentTarget.style.transform = "translateY(0)";
          e.currentTarget.style.boxShadow = "none";
        }
      },
      /* @__PURE__ */ React.createElement("div", { style: {
        aspectRatio: "3 / 4",
        background: post.bg,
        position: "relative",
        overflow: "hidden",
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
      } }, post.visual, /* @__PURE__ */ React.createElement("div", { style: {
        position: "absolute",
        top: 8,
        left: 8,
        padding: "3px 7px",
        borderRadius: 99,
        background: "rgba(14,14,44,.7)",
        color: T.white,
        fontSize: 10,
        fontWeight: 600,
        letterSpacing: "0.04em",
        display: "inline-flex",
        alignItems: "center",
        gap: 4,
        backdropFilter: "blur(4px)"
      } }, /* @__PURE__ */ React.createElement(Icon, { name: "trending", size: 9 }), " ", post.platform), /* @__PURE__ */ React.createElement("div", { style: {
        position: "absolute",
        top: 8,
        right: 8,
        padding: "3px 7px",
        borderRadius: 4,
        background: T.primary,
        color: T.navy,
        fontSize: 10,
        fontWeight: 700
      } }, post.hotScore)),
      /* @__PURE__ */ React.createElement("div", { style: { padding: "12px 12px 12px" } }, /* @__PURE__ */ React.createElement("div", { style: {
        fontSize: 12.5,
        fontWeight: 600,
        color: T.navy,
        lineHeight: 1.45,
        marginBottom: 8,
        display: "-webkit-box",
        WebkitLineClamp: 2,
        WebkitBoxOrient: "vertical",
        overflow: "hidden"
      } }, post.title), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10, fontSize: 11, color: T.navyLight } }, /* @__PURE__ */ React.createElement("span", { style: { display: "inline-flex", alignItems: "center", gap: 3 } }, /* @__PURE__ */ React.createElement(Icon, { name: "heart", size: 11 }), " ", post.likes), /* @__PURE__ */ React.createElement("span", { style: { display: "inline-flex", alignItems: "center", gap: 3 } }, /* @__PURE__ */ React.createElement(Icon, { name: "bookmark", size: 11 }), " ", post.saves), /* @__PURE__ */ React.createElement("span", { style: { marginLeft: "auto", fontFamily: T.fontMono, fontSize: 10 } }, post.time)))
    );
  };
  var FlowerVisual = ({ palette }) => /* @__PURE__ */ React.createElement("svg", { viewBox: "0 0 100 130", width: "100%", height: "100%", style: { display: "block" }, preserveAspectRatio: "xMidYMid slice" }, /* @__PURE__ */ React.createElement("rect", { width: "100", height: "130", fill: palette[0] }), /* @__PURE__ */ React.createElement("path", { d: "M10 110 Q 5 70, 30 60 Q 55 50, 50 100 Q 45 130, 20 125 Z", fill: palette[1], opacity: ".85" }), [
    [40, 30, 18, palette[2]],
    [62, 45, 14, palette[3]],
    [55, 70, 16, palette[2]],
    [78, 28, 10, palette[3]],
    [30, 55, 11, palette[3]]
  ].map(([cx, cy, r, c], i) => /* @__PURE__ */ React.createElement("g", { key: i }, [0, 72, 144, 216, 288].map((a) => {
    const rad = a * Math.PI / 180;
    return /* @__PURE__ */ React.createElement("ellipse", { key: a, cx: cx + Math.cos(rad) * r * 0.55, cy: cy + Math.sin(rad) * r * 0.55, rx: r * 0.6, ry: r * 0.45, fill: c, opacity: 0.85, transform: `rotate(${a} ${cx} ${cy})` });
  }), /* @__PURE__ */ React.createElement("circle", { cx, cy, r: r * 0.25, fill: palette[4] }))));
  var Step2HotPosts = ({ onSelectAngle }) => {
    const posts = [
      {
        title: "\u6DF1\u84DD\u5E55\u5E03\u4E0B\u7684\u7C89\u8776\u5170\uFF0C\u8C01\u61C2\u8FD9\u79CD\u53CD\u5DEE\u611F",
        platform: "\u5C0F\u7EA2\u4E66",
        hotScore: "HOT 9.2",
        likes: "5.6w",
        saves: "2.6w",
        time: "2 \u5929\u524D",
        bg: "#1a3a5c",
        visual: /* @__PURE__ */ React.createElement(FlowerVisual, { palette: ["#1a3a5c", "#2c5a3c", "#f5b8c8", "#e896b0", "#fdf5f5"] })
      },
      {
        title: "\u786C\u6C49\u517B\u82B1\u6307\u5317 \xB7 8 \u79CD\u7C89\u5F97\u76F4\u7537\u90FD\u7231\u7684\u690D\u7269",
        platform: "\u5C0F\u7EA2\u4E66",
        hotScore: "HOT 8.8",
        likes: "4.2w",
        saves: "1.9w",
        time: "5 \u5929\u524D",
        bg: "#2a1a2e",
        visual: /* @__PURE__ */ React.createElement(FlowerVisual, { palette: ["#2a1a2e", "#3c5a4c", "#fab1c4", "#f78bb0", T.peachTint] })
      },
      {
        title: "\u4E0D\u517B\u4ED9\u4EBA\u638C\u540E\uFF0C\u6211\u5BB6\u7C89\u8272\u690D\u7269\u6536\u85CF Top 6",
        platform: "\u5C0F\u7EA2\u4E66",
        hotScore: "HOT 8.5",
        likes: "3.8w",
        saves: "1.5w",
        time: "1 \u5468\u524D",
        bg: "#fdf0ee",
        visual: /* @__PURE__ */ React.createElement(FlowerVisual, { palette: ["#fdf0ee", "#9bbfa8", "#e8a0bc", "#d987a8", "#fff"] })
      },
      {
        title: "\u9633\u53F0\u6539\u9020 | \u628A\u7C89\u7EA2\u4ED9\u5883\u642C\u56DE\u5BB6 \xA5300 \u641E\u5B9A",
        platform: "\u5C0F\u7EA2\u4E66",
        hotScore: "HOT 7.9",
        likes: "3.1w",
        saves: "1.2w",
        time: "2 \u5468\u524D",
        bg: "#3a2c4a",
        visual: /* @__PURE__ */ React.createElement(FlowerVisual, { palette: ["#3a2c4a", "#5c7a5c", "#f0a8c4", "#dc8aa8", "#fff"] })
      }
    ];
    const [openConclusion, setOpenConclusion] = React.useState(false);
    const [phase, setPhase] = React.useState(0);
    React.useEffect(() => {
      const timers = [
        setTimeout(() => setPhase(1), 1e3),
        setTimeout(() => setPhase(2), 2600),
        setTimeout(() => setPhase(3), 4300)
      ];
      return () => timers.forEach(clearTimeout);
    }, []);
    return /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 14 } }, "\u6536\u5230\uFF0C\u5F00\u59CB\u52A8\u4E86 \u2728 \u6211\u5148\u53BB\u5C0F\u7EA2\u4E66 / \u6296\u97F3\u4E0A\u6252\u4E86\u4E00\u5708 ", /* @__PURE__ */ React.createElement("b", null, "\u7C89\u8272\u690D\u7269"), " \u76F8\u5173\u7206\u6B3E\uFF0C \u8FD9\u4E2A\u8BDD\u9898\u6709\u771F\u5B9E\u7684\u6D41\u91CF\u76D8\u5B50\uFF0C\u8FD1 30 \u5929\u7206\u6B3E 200+ \u7BC7\uFF0C\u6536\u85CF\u8BC4\u8BBA\u8868\u73B0\u6301\u7EED\u8D70\u9AD8\uFF0C", /* @__PURE__ */ React.createElement("span", { style: { color: T.success, fontWeight: 600 } }, "\u300C\u53EF\u6253\u9020\u4E3A\u7206\u6B3E\u300D\u8BCA\u65AD\u901A\u8FC7"), "\u3002"), /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 14, color: T.navyMid } }, "\u4E0B\u9762\u662F 4 \u7BC7\u53EF\u53C2\u8003\u7684\u7206\u6B3E\uFF0C\u5DF2\u6309\u9009\u9898\u8D34\u5408\u5EA6\u6392\u5E8F \u2014\u2014"), phase === 0 && /* @__PURE__ */ React.createElement(TypingDots, null)), phase >= 1 && /* @__PURE__ */ React.createElement("div", { style: { marginLeft: 38, marginTop: -6, animation: "fadeIn .28s ease" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginBottom: 14 } }, posts.map((p, i) => /* @__PURE__ */ React.createElement(HotCard, { key: i, post: p }))), /* @__PURE__ */ React.createElement("button", { style: {
      fontSize: 12,
      color: T.navyMid,
      background: "transparent",
      border: "none",
      cursor: "pointer",
      padding: "4px 0",
      fontWeight: 500,
      display: "inline-flex",
      alignItems: "center",
      gap: 4
    } }, "\u67E5\u770B\u5176\u4F59 21 \u7BC7\u7206\u6B3E ", /* @__PURE__ */ React.createElement(Icon, { name: "chevronRight", size: 11 }))), phase >= 2 && /* @__PURE__ */ React.createElement(NoriSays, { style: { marginTop: 22 } }, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 14 } }, "\u6211\u628A\u8FD9\u4E9B\u7206\u6B3E\u7684\u5171\u540C\u7ED3\u6784\u62C6\u7ED9\u4F60\u770B \u2014\u2014"), /* @__PURE__ */ React.createElement("div", { style: {
      background: "rgba(255,255,255,.86)",
      border: `1px solid ${T.hairlineSoft}`,
      borderRadius: 16,
      padding: "4px 0",
      overflow: "hidden",
      boxShadow: "0 10px 24px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)"
    } }, [
      { label: "\u6807\u9898\u516C\u5F0F", body: "\u300C\u53CD\u5DEE\u8BCD + \u5177\u4F53\u690D\u7269 + \u60C5\u7EEA/\u6001\u5EA6\u300D \u4F8B\u5982\u300C\u731B\u7537 / \u76F4\u7537 + \u7C89\u8272\u690D\u7269 + \u8C01\u61C2\u8FD9\u79CD\u53CD\u5DEE\u611F\u300D", icon: "edit" },
      { label: "\u5C01\u9762\u53C2\u8003", body: "\u6DF1\u8272\u80CC\u666F +  \u5355\u682A\u690D\u7269\u7279\u5199 + \u6781\u7B80\u7559\u767D\uFF1B\u51B7\u6696\u53CD\u5DEE\u662F\u5173\u952E\uFF0C\u907F\u514D\u751C\u817B", icon: "image" },
      { label: "\u5185\u6587\u957F\u5EA6", body: "8 \u5F20\u56FE / 600\u2013800 \u5B57\u3002\u300C\u4EBA\u8BBE\u94A9\u5B50 \u2192 6 \u79CD\u690D\u7269 \u2192 \u517B\u62A4 Tips \u2192 \u4E92\u52A8\u7ED3\u5C3E\u300D", icon: "document" },
      { label: "\u4E92\u52A8\u94A9\u5B50", body: "\u7ED3\u5C3E\u629B 1 \u4E2A\u5177\u4F53\u95EE\u9898\uFF1A\u300C\u4F60\u5BB6\u6709\u51E0\u76C6\uFF1F\u300D\u300C\u731B\u7537\u80FD hold \u51E0\u79CD\uFF1F\u300D", icon: "chat" }
    ].map((row, i, arr) => /* @__PURE__ */ React.createElement("div", { key: i, style: {
      display: "flex",
      alignItems: "flex-start",
      gap: 14,
      padding: "14px 18px",
      borderBottom: i < arr.length - 1 ? `1px solid ${T.hairlineSoft}` : "none"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      width: 28,
      height: 28,
      borderRadius: 8,
      background: T.irisTint,
      color: T.iris,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0,
      marginTop: 1
    } }, /* @__PURE__ */ React.createElement(Icon, { name: row.icon, size: 14 })), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12, fontWeight: 700, letterSpacing: "0.04em", color: T.navy, marginBottom: 4, textTransform: "uppercase" } }, row.label), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13, color: T.navyMid, lineHeight: 1.6 } }, row.body)))))), phase >= 3 && /* @__PURE__ */ React.createElement(NoriSays, { style: { marginTop: 22 } }, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 14 } }, "\u7EFC\u5408\u4E0A\u9762\u7684\u62C6\u89E3\uFF0C\u6211\u7ED9\u4F60\u7684\u9009\u9898\u7ED3\u8BBA\u662F \u2014\u2014", /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 12.5 } }, "\uFF08\u70B9\u51FB\u540E\u8FDB\u5165\u5C01\u9762\u9009\u62E9\uFF09")), /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: () => onSelectAngle(),
        style: {
          width: "100%",
          textAlign: "left",
          background: "rgba(255,255,255,.86)",
          border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 16,
          padding: "14px 18px",
          display: "flex",
          alignItems: "center",
          gap: 14,
          cursor: "pointer",
          transition: `transform .3s ${T.spring}, box-shadow .3s ${T.spring}, border .22s ${T.ease}`,
          boxShadow: "0 10px 24px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)"
        },
        onMouseEnter: (e) => {
          e.currentTarget.style.borderColor = "rgba(75,77,237,.32)";
          e.currentTarget.style.boxShadow = T.shadowSm;
        },
        onMouseLeave: (e) => {
          e.currentTarget.style.borderColor = T.hairlineSoft;
          e.currentTarget.style.boxShadow = "0 10px 24px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)";
        }
      },
      /* @__PURE__ */ React.createElement("div", { style: {
        width: 44,
        height: 44,
        borderRadius: 10,
        background: T.primary,
        color: T.navy,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0
      } }, /* @__PURE__ */ React.createElement(Icon, { name: "target", size: 22 })),
      /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 14, fontWeight: 700, color: T.navy, marginBottom: 2 } }, "\u9009\u9898\u7ED3\u8BBA \xB7 \u53CD\u5DEE\u4EBA\u8BBE + 6 \u79CD\u7C89\u8272\u690D\u7269\u79CD\u8349"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12, color: T.navyLight } }, "\u5C0F\u7EA2\u4E66\u56FE\u6587 \xB7 8 \u5F20\u56FE \xB7 \u9AD8\u6536\u85CF\u65B9\u5411 \xB7 Nori \u63A8\u8350")),
      /* @__PURE__ */ React.createElement("div", { style: {
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        padding: "6px 12px",
        borderRadius: 8,
        background: T.surface,
        color: T.navy,
        fontSize: 12,
        fontWeight: 600
      } }, /* @__PURE__ */ React.createElement(Icon, { name: "expand", size: 12 }), " \u5728 Canvas \u67E5\u770B")
    )));
  };
  var SourceRow = ({ source, idx }) => {
    return /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "10px 14px",
          borderRadius: 10,
          cursor: "pointer",
          transition: "background .12s"
        },
        onMouseEnter: (e) => e.currentTarget.style.background = T.surface,
        onMouseLeave: (e) => e.currentTarget.style.background = "transparent"
      },
      /* @__PURE__ */ React.createElement("div", { style: {
        width: 24,
        height: 24,
        borderRadius: 6,
        background: source.tint,
        color: source.color,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0
      } }, /* @__PURE__ */ React.createElement(Icon, { name: source.icon, size: 12 })),
      /* @__PURE__ */ React.createElement("div", { style: { flex: 1, minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12.5, fontWeight: 500, color: T.navy, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, source.title), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 10.5, color: T.navyLight, fontFamily: T.fontMono } }, source.host, " \xB7 ", source.kind)),
      /* @__PURE__ */ React.createElement(Icon, { name: "link", size: 12, color: T.navyLight })
    );
  };
  var Step3Research = ({ selectedAsset, onSelectAsset }) => {
    const [imgsExpanded, setImgsExpanded] = React.useState(false);
    const [phase, setPhase] = React.useState(0);
    const sources = [
      { title: "\u300A\u89C2\u8D4F\u690D\u7269\u8272\u7D20\u5206\u5E03\u4E0E\u82B1\u8272\u7A33\u5B9A\u6027\u7814\u7A76\u300B", host: "cnki.net", kind: "PDF \xB7 \u8BBA\u6587", icon: "book", tint: T.irisTint, color: T.iris },
      { title: "\u7C89\u638C\u3001\u59EC\u79CB\u4E3D\u3001\u82B1\u53F6\u51B7\u6C34\u82B1\u517B\u62A4\u8981\u70B9", host: "huayuan.com", kind: "\u79D1\u666E\u6587\u7AE0", icon: "document", tint: "#fff8e0", color: "#c89b00" },
      { title: "Pink Plants Care Guide 2025", host: "gardenista.com", kind: "\u82F1\u6587 Guide", icon: "globe", tint: T.successTint, color: T.success },
      { title: "\u3010\u7C89\u8272\u690D\u7269 Top10\u3011\u5B8C\u6574\u76D8\u70B9", host: "bilibili.com", kind: "\u89C6\u9891 \xB7 7:32", icon: "play", tint: "#ffe5ec", color: "#ff4488" }
    ];
    const Img = ({ asset, featured }) => /* @__PURE__ */ React.createElement(
      "div",
      {
        style: {
          borderRadius: 10,
          overflow: "hidden",
          background: asset.palette[0],
          aspectRatio: "1 / 1.25",
          cursor: "pointer",
          transition: "transform .15s",
          position: "relative",
          outline: selectedAsset?.id === asset.id ? `2px solid ${T.primary}` : "none",
          boxShadow: selectedAsset?.id === asset.id ? "0 0 0 5px rgba(214,255,0,.14)" : "none"
        },
        onClick: () => onSelectAsset && onSelectAsset(asset),
        onMouseEnter: (e) => e.currentTarget.style.transform = "scale(1.02)",
        onMouseLeave: (e) => e.currentTarget.style.transform = "scale(1)"
      },
      /* @__PURE__ */ React.createElement(FlowerVisual, { palette: asset.palette }),
      /* @__PURE__ */ React.createElement("div", { style: {
        position: "absolute",
        top: 6,
        right: 6,
        width: 22,
        height: 22,
        borderRadius: 6,
        background: selectedAsset?.id === asset.id ? T.primary : "rgba(0,0,0,.5)",
        color: selectedAsset?.id === asset.id ? T.navy : T.white,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        backdropFilter: "blur(4px)",
        opacity: selectedAsset?.id === asset.id ? 1 : 0,
        transition: "opacity .15s, background .15s"
      } }, /* @__PURE__ */ React.createElement(Icon, { name: selectedAsset?.id === asset.id ? "check" : "expand", size: 11 })),
      featured && /* @__PURE__ */ React.createElement("div", { style: {
        position: "absolute",
        top: 6,
        left: 6,
        fontSize: 9,
        fontWeight: 700,
        letterSpacing: "0.04em",
        color: T.navy,
        background: T.primary,
        padding: "2px 6px",
        borderRadius: 4
      } }, "\u2605 TOP ", featured),
      selectedAsset?.id === asset.id && /* @__PURE__ */ React.createElement("div", { style: {
        position: "absolute",
        left: 8,
        right: 8,
        bottom: 8,
        padding: "7px 9px",
        borderRadius: 8,
        background: "rgba(255,255,255,.78)",
        color: T.navy,
        fontSize: 10.5,
        fontWeight: 700,
        backdropFilter: "blur(8px)"
      } }, "\u5DF2\u7528\u4E8E\u53F3\u4FA7\u9884\u89C8")
    );
    const assets = [
      { id: "asset-1", label: "\u5E55\u5E03\u5149\u5F71", shape: "ribbon", rotate: -4, palette: ["#1a3a5c", "#2c5a3c", "#f5b8c8", "#e896b0", "#fdf5f5"] },
      { id: "asset-2", label: "\u591C\u8272\u82B1\u5F71", shape: "petal", rotate: 3, palette: ["#2a1a2e", "#3c5a4c", "#fab1c4", "#f78bb0", T.peachTint] },
      { id: "asset-3", label: "\u5976\u6CB9\u6E05\u6668", shape: "bloom", rotate: -2, palette: ["#fdf0ee", "#9bbfa8", "#e8a0bc", "#d987a8", "#fff"] },
      { id: "asset-4", label: "\u7D2B\u8C03\u53CD\u5DEE", shape: "ribbon", rotate: 4, palette: ["#3a2c4a", "#5c7a5c", "#f0a8c4", "#dc8aa8", "#fff"] },
      { id: "asset-5", label: "\u6D77\u76D0\u6DF1\u84DD", shape: "petal", rotate: -3, palette: ["#0e2a3a", "#3c4a3c", "#ffb8c8", "#ff8aa8", "#fff"] },
      { id: "asset-6", label: "\u8393\u679C\u665A\u98CE", shape: "bloom", rotate: 4, palette: ["#2c1a3a", "#5c3c5c", "#f8a8c0", "#e890b0", "#fff"] },
      { id: "asset-7", label: "\u96FE\u7C89\u767D\u663C", shape: "ribbon", rotate: -2, palette: ["#fce5ec", "#a8c8a8", "#dc8aa8", "#b86890", "#fff"] },
      { id: "asset-8", label: "\u68EE\u6797\u5E55\u5899", shape: "petal", rotate: 3, palette: ["#1a2a3a", "#5c7a4c", "#f0c0d0", "#e090b0", "#fff"] },
      { id: "asset-9", label: "\u9152\u7EA2\u573A\u666F", shape: "bloom", rotate: -4, palette: ["#3a1a2a", "#4c5a4c", "#ffa0c0", "#d088a8", "#fff"] },
      { id: "asset-10", label: "\u67D4\u7C89\u7559\u767D", shape: "ribbon", rotate: 2, palette: ["#fdf5f5", "#88aa88", "#e890a8", "#b87090", "#fff"] },
      { id: "asset-11", label: "\u96FE\u84DD\u6697\u6D8C", shape: "petal", rotate: -3, palette: ["#22334a", "#4a6a4a", "#fcb4cc", "#e088a8", "#fff"] },
      { id: "asset-12", label: "\u66AE\u8272\u82B1\u623F", shape: "bloom", rotate: 3, palette: ["#2a2a3c", "#5a7a5a", "#f8a0c0", "#cc7898", "#fff"] }
    ];
    React.useEffect(() => {
      if (!selectedAsset && phase >= 2 && onSelectAsset) onSelectAsset(assets[0]);
    }, [phase, selectedAsset, onSelectAsset]);
    React.useEffect(() => {
      const timers = [
        setTimeout(() => setPhase(1), 1100),
        setTimeout(() => setPhase(2), 2800),
        setTimeout(() => setPhase(3), 4500)
      ];
      return () => timers.forEach(clearTimeout);
    }, []);
    return /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 14 } }, "\u7B56\u7565\u5B9A\u4E86\uFF0C\u6211\u5F00\u59CB\u4E3A\u4F60\u8C03\u7814\u7D20\u6750\u3002\u5148\u6252\u4E86\u4E00\u5708\u5B66\u672F\u8BBA\u6587 + \u79D1\u666E\u6587\u7AE0 + \u89C6\u9891 \u2014\u2014"), phase === 0 && /* @__PURE__ */ React.createElement(TypingDots, null), phase >= 1 && /* @__PURE__ */ React.createElement("div", { style: {
      background: "rgba(255,255,255,.86)",
      border: `1px solid ${T.hairlineSoft}`,
      borderRadius: 16,
      padding: 6,
      overflow: "hidden",
      animation: `fadeIn .32s ${T.spring}`,
      boxShadow: "0 10px 24px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)"
    } }, sources.map((s, i) => /* @__PURE__ */ React.createElement(SourceRow, { key: i, source: s, idx: i }))), phase >= 1 && /* @__PURE__ */ React.createElement("button", { style: {
      marginTop: 8,
      fontSize: 12,
      color: T.navyMid,
      background: "transparent",
      border: "none",
      cursor: "pointer",
      fontWeight: 500,
      display: "inline-flex",
      alignItems: "center",
      gap: 4,
      padding: "4px 0"
    } }, "\u67E5\u770B\u5176\u4F59 5 \u4E2A\u6765\u6E90 ", /* @__PURE__ */ React.createElement(Icon, { name: "chevronDown", size: 11 }))), phase >= 2 && /* @__PURE__ */ React.createElement(NoriSays, { style: { marginTop: 22 } }, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 12 } }, "\u518D\u6252\u4E86\u4E00\u4E9B\u7C89\u8272\u690D\u7269\u7684\u56FE\u7247\u7D20\u6750 \u2014\u2014 \u9AD8\u4EAE\u7684\u8FD9 4 \u5F20\u662F\u6211\u89C9\u5F97\u5C01\u9762 / \u4E3B\u56FE\u6700\u80FD\u7528\u7684\uFF1A"), /* @__PURE__ */ React.createElement("div", { style: {
      display: "grid",
      gridTemplateColumns: "repeat(4, 1fr)",
      gap: 8,
      animation: "fadeIn .28s ease"
    } }, assets.slice(0, 4).map((asset, i) => /* @__PURE__ */ React.createElement(Img, { key: asset.id, asset, featured: i + 1 }))), imgsExpanded && /* @__PURE__ */ React.createElement("div", { style: {
      display: "grid",
      gridTemplateColumns: "repeat(4, 1fr)",
      gap: 8,
      marginTop: 8,
      animation: "fadeIn .3s ease"
    } }, assets.slice(4).map((asset) => /* @__PURE__ */ React.createElement(Img, { key: asset.id, asset }))), /* @__PURE__ */ React.createElement("button", { onClick: () => setImgsExpanded((v) => !v), style: {
      marginTop: 12,
      fontSize: 12,
      color: T.navyMid,
      background: "transparent",
      border: "none",
      cursor: "pointer",
      fontWeight: 500,
      display: "inline-flex",
      alignItems: "center",
      gap: 4,
      padding: "4px 0"
    } }, imgsExpanded ? "\u6536\u8D77" : `\u67E5\u770B\u5176\u4F59 ${assets.length - 4} \u5F20\u56FE\u7247`, /* @__PURE__ */ React.createElement(Icon, { name: imgsExpanded ? "chevronDown" : "chevronRight", size: 11 })), phase >= 3 && /* @__PURE__ */ React.createElement("div", { style: {
      marginTop: 14,
      display: "inline-flex",
      alignItems: "center",
      gap: 6,
      padding: "6px 12px",
      borderRadius: 99,
      background: T.successTint,
      color: T.success,
      fontSize: 12,
      fontWeight: 600,
      animation: "fadeIn .26s ease"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 12 }), " \u7D20\u6750\u641C\u96C6\u5B8C\u6210 \xB7 9 \u7BC7\u8D44\u6599 + 12 \u5F20\u56FE")));
  };
  var Step4Generate = ({ onAllDone, onRevealCanvas }) => {
    const tasks = [
      { id: "t1", label: "\u751F\u6210\u6807\u9898\u4E0E\u6B63\u6587\u4E2D", sub: "\u53CD\u5DEE\u94A9\u5B50 + 6 \u79CD\u690D\u7269 + \u517B\u62A4 Tips" },
      { id: "t2", label: "\u751F\u6210\u56FE\u7247\u5361\u7247\u4E2D", sub: "8 \u5F20\u56FE \xB7 \u5C01\u9762 + \u5185\u9875 + \u4E92\u52A8\u9875" },
      { id: "t3", label: "\u6392\u7248\u4F18\u5316\u4E2D", sub: "\u5C0F\u7EA2\u4E66\u56FE\u6587\u683C\u5F0F \xB7 emoji \u4E0E\u6392\u7248" },
      { id: "t4", label: "\u4E00\u81F4\u6027\u6821\u5BF9\u4E2D", sub: "\u672F\u8BED \xB7 \u98CE\u683C \xB7 \u6807\u70B9\u7EDF\u4E00" }
    ];
    const [done, setDone] = React.useState({});
    const [current, setCurrent] = React.useState(0);
    const [allDone, setAllDone] = React.useState(false);
    React.useEffect(() => {
      if (current >= tasks.length) {
        setAllDone(true);
        const t2 = setTimeout(() => onAllDone && onAllDone(), 700);
        return () => clearTimeout(t2);
      }
      const t = setTimeout(() => {
        setDone((d) => ({ ...d, [tasks[current].id]: true }));
        setCurrent((c) => c + 1);
      }, 1400);
      return () => clearTimeout(t);
    }, [current]);
    return /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 14 } }, "\u6240\u6709\u51C6\u5907\u5C31\u7EEA\uFF0C\u5F00\u59CB\u751F\u6210\u5185\u5BB9\u4E86 \u2014\u2014 \u4F60\u53EF\u4EE5\u5728\u53F3\u8FB9 Canvas \u5B9E\u65F6\u9884\u89C8\uFF1A"), /* @__PURE__ */ React.createElement("div", { style: {
      background: "rgba(255,255,255,.86)",
      border: `1px solid ${T.hairlineSoft}`,
      borderRadius: 16,
      padding: "12px 16px",
      overflow: "hidden",
      boxShadow: "0 10px 24px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)"
    } }, tasks.map((t, i) => {
      const isDone = done[t.id];
      const isActive = current === i && !isDone;
      return /* @__PURE__ */ React.createElement("div", { key: t.id, style: {
        display: "flex",
        alignItems: "center",
        gap: 12,
        padding: "10px 0",
        borderBottom: i < tasks.length - 1 ? `1px solid ${T.hairlineSoft}` : "none"
      } }, /* @__PURE__ */ React.createElement("div", { style: {
        width: 22,
        height: 22,
        borderRadius: 6,
        border: `1.5px solid ${isDone ? T.success : T.navySoft}`,
        background: isDone ? T.success : T.white,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0,
        position: "relative",
        animation: isDone ? "checkPop .35s ease" : "none"
      } }, isDone && /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 12, color: T.white, stroke: 2.5 }), isActive && /* @__PURE__ */ React.createElement("div", { style: {
        position: "absolute",
        inset: -3,
        border: `2px solid ${T.iris}`,
        borderTopColor: "transparent",
        borderRadius: 8,
        animation: "spin 0.9s linear infinite"
      } })), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement("div", { style: {
        fontSize: 13,
        fontWeight: 600,
        color: isDone ? T.navyLight : T.navy,
        textDecoration: isDone ? "line-through" : "none"
      } }, t.label), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11, color: T.navyLight, marginTop: 1 } }, t.sub)), isActive && /* @__PURE__ */ React.createElement("span", { style: { fontSize: 11, color: T.iris, fontWeight: 600, animation: "pulse 1.4s infinite" } }, "\u8FDB\u884C\u4E2D\u2026"), isDone && /* @__PURE__ */ React.createElement("span", { style: { fontSize: 11, color: T.success, fontWeight: 600 } }, "\u5B8C\u6210"));
    })), allDone && /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: () => onRevealCanvas && onRevealCanvas(),
        style: {
          marginTop: 14,
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "12px 16px",
          borderRadius: 12,
          background: `linear-gradient(90deg, ${T.primary} 0%, #edff7a 42%, ${T.successTint} 72%, #f8ffcc 100%)`,
          backgroundSize: "220% 100%",
          color: T.navy,
          fontWeight: 600,
          fontSize: 13.5,
          animation: `doneButtonReveal 1.35s ${T.spring} both, doneButtonGlow 1.4s ease-in-out .12s 2`,
          position: "relative",
          overflow: "hidden",
          width: "100%",
          border: "none",
          cursor: "pointer",
          justifyContent: "space-between",
          textAlign: "left",
          boxShadow: "0 12px 30px rgba(214,255,0,.22)",
          transition: `transform .28s ${T.spring}, box-shadow .28s ${T.spring}`
        }
      },
      /* @__PURE__ */ React.createElement("span", { style: {
        position: "absolute",
        inset: 0,
        background: "linear-gradient(110deg, transparent 0%, rgba(255,255,255,.72) 48%, transparent 62%)",
        transform: "translateX(-120%)",
        animation: `doneButtonSweep 1.1s ${T.spring} .16s both`,
        pointerEvents: "none"
      } }),
      /* @__PURE__ */ React.createElement("span", null, "\u5168\u90E8\u5B8C\u6210\uFF01\u5185\u5BB9\u5DF2\u5C31\u7EEA\uFF0C\u53BB Canvas \u770B\u770B\u5427"),
      /* @__PURE__ */ React.createElement("span", { style: {
        width: 30,
        height: 30,
        borderRadius: "50%",
        background: "rgba(14,14,44,.08)",
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        flexShrink: 0
      } }, /* @__PURE__ */ React.createElement(Icon, { name: "chevronRight", size: 14, color: T.navy }))
    ));
  };
  window.Bubble = Bubble;
  window.NoriSays = NoriSays;
  window.TypingDots = TypingDots;
  window.Avatar = Avatar;
  window.Step1KeyInfo = Step1KeyInfo;
  window.Step2HotPosts = Step2HotPosts;
  window.Step3Research = Step3Research;
  window.Step4Generate = Step4Generate;
  window.FlowerVisual = FlowerVisual;
  var PhoneFrame = ({ children }) => /* @__PURE__ */ React.createElement("div", { style: {
    position: "relative",
    width: "min(356px, 100%)",
    height: 704,
    margin: "0 auto",
    filter: "drop-shadow(0 30px 58px rgba(14,14,44,.18))"
  } }, /* @__PURE__ */ React.createElement("div", { style: {
    position: "absolute",
    inset: 0,
    borderRadius: 55,
    background: "linear-gradient(145deg, #fbfbfc, #d9dce2)",
    boxShadow: "inset 0 0 0 1px rgba(14,14,44,.12), inset 0 0 0 3px rgba(255,255,255,.72)"
  } }), /* @__PURE__ */ React.createElement("span", { style: {
    position: "absolute",
    left: -5,
    top: 164,
    width: 4,
    height: 46,
    borderRadius: "4px 0 0 4px",
    background: "linear-gradient(180deg, #d5d8df, #f8f8fa)",
    boxShadow: "0 98px 0 #e4e6eb, 0 157px 0 #e4e6eb"
  } }), /* @__PURE__ */ React.createElement("span", { style: {
    position: "absolute",
    right: -46,
    top: 315,
    width: 44,
    height: 44,
    borderRadius: "50%",
    background: "linear-gradient(145deg, #f5f6f8, #dfe2e7)",
    border: "1px solid rgba(14,14,44,.08)",
    boxShadow: "0 9px 18px rgba(14,14,44,.10), inset 0 1px 0 rgba(255,255,255,.8)"
  } }), /* @__PURE__ */ React.createElement("div", { style: {
    position: "absolute",
    inset: 8,
    borderRadius: 49,
    background: "#050507",
    boxShadow: "inset 0 0 0 1px rgba(255,255,255,.10)"
  } }), /* @__PURE__ */ React.createElement("div", { style: {
    position: "absolute",
    left: "50%",
    top: 18,
    width: 122,
    height: 34,
    transform: "translateX(-50%)",
    borderRadius: "0 0 19px 19px",
    background: "#050507",
    zIndex: 5
  } }), /* @__PURE__ */ React.createElement("div", { style: {
    position: "absolute",
    left: 17,
    right: 17,
    top: 17,
    bottom: 17,
    borderRadius: 39,
    overflow: "hidden",
    background: "#fff"
  } }, children));
  var CanvasDocumentEditor = ({ data, onSetData }) => /* @__PURE__ */ React.createElement("article", { style: {
    width: "min(720px, 100%)",
    minHeight: "calc(100vh - 188px)",
    background: "rgba(255,255,255,.82)",
    border: `1px solid ${T.hairlineSoft}`,
    borderRadius: 16,
    boxShadow: "0 18px 44px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.84)",
    padding: "50px min(7vw, 62px) 58px",
    color: T.navy
  } }, /* @__PURE__ */ React.createElement(
    EditableText,
    {
      tag: "h1",
      onChange: (v) => onSetData({ ...data, title: v }),
      style: { fontSize: 26, lineHeight: 1.28, fontWeight: 680, letterSpacing: 0, margin: "0 0 18px", color: T.navy }
    },
    data.title
  ), /* @__PURE__ */ React.createElement(
    EditableText,
    {
      tag: "h2",
      onChange: (v) => onSetData({ ...data, hook: v }),
      style: { fontSize: 17, lineHeight: 1.58, fontWeight: 620, margin: "0 0 14px", color: T.navy }
    },
    data.hook
  ), /* @__PURE__ */ React.createElement(
    EditableText,
    {
      tag: "p",
      onChange: (v) => onSetData({ ...data, intro: v }),
      style: { fontSize: 14.6, lineHeight: 1.86, margin: "0 0 26px", color: T.navyMid }
    },
    data.intro
  ), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 18 } }, data.items.map((it, i) => /* @__PURE__ */ React.createElement("section", { key: i }, /* @__PURE__ */ React.createElement(EditableText, { tag: "h3", onChange: (v) => {
    const items = [...data.items];
    items[i] = { ...it, name: v };
    onSetData({ ...data, items });
  }, style: { fontSize: 15.8, fontWeight: 650, lineHeight: 1.55, margin: "0 0 5px", color: T.navy } }, i + 1, ". ", it.name), /* @__PURE__ */ React.createElement(EditableText, { tag: "p", onChange: (v) => {
    const items = [...data.items];
    items[i] = { ...it, desc: v };
    onSetData({ ...data, items });
  }, style: { fontSize: 14.2, lineHeight: 1.86, color: T.navyMid, margin: 0 } }, it.desc)))), /* @__PURE__ */ React.createElement(
    EditableText,
    {
      tag: "p",
      onChange: (v) => onSetData({ ...data, cta: v }),
      style: { margin: "28px 0 0", fontSize: 14.8, fontWeight: 600, lineHeight: 1.82, color: T.navy }
    },
    data.cta
  ), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 22, color: T.navyLight, fontSize: 12.5, lineHeight: 1.7 } }, data.tags.map((tag) => `#${tag}`).join("  ")));
  var TextSelectionMenu = ({ pos, onAction, onClose }) => {
    if (!pos) return null;
    const actions = [
      { id: "rewrite", label: "\u6539\u5199", icon: "edit" },
      { id: "expand", label: "\u6269\u5C55", icon: "plus" },
      { id: "simplify", label: "\u7B80\u5316", icon: "minus" },
      { id: "tone", label: "\u8C03\u6574\u8BED\u6C14", icon: "sliders" }
    ];
    return /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      top: pos.y,
      left: pos.x,
      transform: "translate(-50%, -100%)",
      background: T.navy,
      color: T.white,
      borderRadius: 10,
      padding: 4,
      display: "flex",
      gap: 2,
      boxShadow: T.shadowLg,
      zIndex: 50,
      animation: "fadeIn .15s ease"
    } }, actions.map((a) => /* @__PURE__ */ React.createElement(
      "button",
      {
        key: a.id,
        onClick: () => onAction(a.id),
        style: {
          padding: "6px 10px",
          borderRadius: 6,
          background: "transparent",
          color: T.white,
          border: "none",
          cursor: "pointer",
          fontSize: 12,
          fontWeight: 500,
          display: "inline-flex",
          alignItems: "center",
          gap: 5
        },
        onMouseEnter: (e) => e.currentTarget.style.background = "rgba(255,255,255,.12)",
        onMouseLeave: (e) => e.currentTarget.style.background = "transparent"
      },
      /* @__PURE__ */ React.createElement(Icon, { name: a.icon, size: 12 }),
      " ",
      a.label
    )));
  };
  var EditableText = ({ tag = "p", children, onChange, style }) => {
    const ref = React.useRef(null);
    return React.createElement(tag, {
      ref,
      contentEditable: true,
      suppressContentEditableWarning: true,
      onBlur: (e) => onChange && onChange(e.currentTarget.innerText),
      style: { outline: "none", cursor: "text", ...style },
      spellCheck: false
    }, children);
  };
  var PostPreview = ({ data, onSetData, onSelectText, selectedAsset }) => {
    const handleMouseUp = (e) => {
      const sel = window.getSelection();
      if (!sel || sel.isCollapsed || !sel.toString().trim()) {
        onSelectText(null);
        return;
      }
      const range = sel.getRangeAt(0);
      const r = range.getBoundingClientRect();
      const container = e.currentTarget.getBoundingClientRect();
      onSelectText({ x: r.left - container.left + r.width / 2, y: r.top - container.top - 6 });
    };
    const coverPalette = selectedAsset?.palette || ["#1a3a5c", "#2c5a3c", "#f5b8c8", "#e896b0", "#fdf5f5"];
    const coverShape = selectedAsset?.shape || "petal";
    const coverRotate = selectedAsset?.rotate || 0;
    const coverLabel = selectedAsset?.label || "\u7CBE\u9009\u7D20\u6750";
    const clipPaths = {
      petal: "polygon(12% 16%, 34% 9%, 46% 0%, 60% 12%, 81% 8%, 100% 22%, 93% 44%, 100% 71%, 82% 88%, 61% 84%, 44% 100%, 22% 92%, 0% 74%, 7% 48%, 0% 24%)",
      ribbon: "polygon(6% 7%, 44% 0%, 64% 9%, 100% 4%, 90% 38%, 100% 65%, 83% 100%, 46% 92%, 26% 100%, 0% 81%, 9% 48%, 0% 17%)",
      bloom: "polygon(11% 0%, 38% 8%, 58% 0%, 74% 15%, 100% 17%, 94% 50%, 100% 80%, 76% 100%, 49% 93%, 30% 100%, 0% 82%, 8% 51%, 0% 18%)"
    };
    return /* @__PURE__ */ React.createElement("div", { onMouseUp: handleMouseUp, style: {
      width: "100%",
      height: "100%",
      background: T.white,
      overflowY: "auto",
      overflowX: "hidden",
      position: "relative",
      WebkitOverflowScrolling: "touch"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      position: "sticky",
      top: 0,
      zIndex: 4,
      height: 30,
      padding: "0 18px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      fontSize: 12,
      fontWeight: 700,
      color: "#111",
      background: "rgba(255,255,255,.94)",
      backdropFilter: "blur(10px)"
    } }, /* @__PURE__ */ React.createElement("span", null, "9:41"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 6, color: "rgba(14,14,44,.72)" } }, /* @__PURE__ */ React.createElement("span", { style: { width: 14, height: 9, borderRadius: 3, border: "1.8px solid currentColor", position: "relative", display: "inline-block" } }, /* @__PURE__ */ React.createElement("span", { style: { position: "absolute", inset: 1.5, borderRadius: 1.5, background: "currentColor" } })), /* @__PURE__ */ React.createElement("span", { style: { width: 14, height: 10, display: "inline-flex", alignItems: "flex-end", gap: 1 } }, [4, 6, 8, 10].map((h, i) => /* @__PURE__ */ React.createElement("span", { key: i, style: { width: 2, height: h, borderRadius: 2, background: "currentColor", display: "inline-block" } }))))), /* @__PURE__ */ React.createElement("div", { style: {
      aspectRatio: "3 / 4",
      background: "#1a3a5c",
      position: "relative",
      overflow: "hidden"
    } }, /* @__PURE__ */ React.createElement(FlowerVisual, { palette: coverPalette }), /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      right: 18,
      top: 18,
      width: 110,
      transform: `rotate(${coverRotate}deg)`
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      aspectRatio: "0.82 / 1",
      clipPath: clipPaths[coverShape],
      overflow: "hidden",
      boxShadow: "0 18px 34px rgba(14,14,44,.24)",
      border: "1px solid rgba(255,255,255,.28)"
    } }, /* @__PURE__ */ React.createElement(FlowerVisual, { palette: coverPalette })), /* @__PURE__ */ React.createElement("div", { style: {
      marginTop: 8,
      display: "inline-flex",
      alignItems: "center",
      gap: 5,
      padding: "5px 8px",
      borderRadius: 999,
      background: "rgba(255,255,255,.16)",
      color: T.white,
      backdropFilter: "blur(10px)",
      fontSize: 9.5,
      fontWeight: 700,
      letterSpacing: "0.05em",
      textTransform: "uppercase"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "image", size: 10, color: "currentColor" }), coverLabel)), /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      inset: 0,
      padding: 22,
      display: "flex",
      flexDirection: "column",
      justifyContent: "flex-end",
      background: "linear-gradient(to top, rgba(0,0,0,.55), transparent 50%)"
    } }, /* @__PURE__ */ React.createElement(
      EditableText,
      {
        tag: "div",
        onChange: (v) => onSetData({ ...data, title: v }),
        style: {
          color: T.white,
          fontSize: 26,
          fontWeight: 700,
          lineHeight: 1.2,
          letterSpacing: "-0.01em",
          textShadow: "0 2px 8px rgba(0,0,0,.3)"
        }
      },
      data.title
    ), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 10, display: "flex", alignItems: "center", gap: 6 } }, data.tags.map((t, i) => /* @__PURE__ */ React.createElement("span", { key: i, style: {
      fontSize: 10.5,
      fontWeight: 600,
      color: T.white,
      background: "rgba(255,255,255,.15)",
      padding: "3px 8px",
      borderRadius: 99,
      backdropFilter: "blur(6px)",
      border: "1px solid rgba(255,255,255,.2)"
    } }, "#", t))))), /* @__PURE__ */ React.createElement("div", { style: { padding: "18px 20px 30px" } }, /* @__PURE__ */ React.createElement(
      EditableText,
      {
        tag: "h3",
        onChange: (v) => onSetData({ ...data, hook: v }),
        style: { fontSize: 16, fontWeight: 700, color: T.navy, marginBottom: 10, lineHeight: 1.4 }
      },
      data.hook
    ), /* @__PURE__ */ React.createElement(
      EditableText,
      {
        tag: "p",
        onChange: (v) => onSetData({ ...data, intro: v }),
        style: { fontSize: 13.5, color: T.navyMid, lineHeight: 1.75, marginBottom: 16 }
      },
      data.intro
    ), data.items.map((it, i) => /* @__PURE__ */ React.createElement("div", { key: i, style: { marginBottom: 14 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, marginBottom: 4 } }, /* @__PURE__ */ React.createElement("span", { style: {
      width: 22,
      height: 22,
      borderRadius: 6,
      background: T.primary,
      color: T.navy,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: 11,
      fontWeight: 700,
      fontFamily: T.fontMono
    } }, "0", i + 1), /* @__PURE__ */ React.createElement(EditableText, { tag: "span", onChange: (v) => {
      const items = [...data.items];
      items[i] = { ...it, name: v };
      onSetData({ ...data, items });
    }, style: { fontSize: 14, fontWeight: 700, color: T.navy } }, it.name)), /* @__PURE__ */ React.createElement(EditableText, { tag: "p", onChange: (v) => {
      const items = [...data.items];
      items[i] = { ...it, desc: v };
      onSetData({ ...data, items });
    }, style: { fontSize: 12.5, color: T.navyMid, lineHeight: 1.7, paddingLeft: 30 } }, it.desc))), /* @__PURE__ */ React.createElement("div", { style: {
      marginTop: 18,
      padding: "12px 14px",
      borderRadius: 10,
      background: T.peachTint,
      color: T.navy,
      fontSize: 13,
      fontWeight: 600,
      lineHeight: 1.6
    } }, /* @__PURE__ */ React.createElement(EditableText, { tag: "div", onChange: (v) => onSetData({ ...data, cta: v }) }, data.cta)), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 16, fontSize: 11.5, color: T.navyLight, fontFamily: T.fontMono } }, "\u4E0A\u6D77 \xB7 8 \u5F20\u56FE \xB7 \u9884\u4F30\u9605\u8BFB 1 \u5206\u949F")));
  };
  var SimplePhonePreview = ({ data, selectedAsset }) => {
    const previewAsset = selectedAsset || GENERATED_IMAGES[0];
    const coverPalette = previewAsset?.palette || GENERATION_COVER_OPTIONS[0].palette;
    return /* @__PURE__ */ React.createElement(PhoneFrame, null, /* @__PURE__ */ React.createElement("div", { style: {
      height: "100%",
      background: "#fbfbfd",
      overflow: "auto",
      color: T.navy
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      height: 34,
      padding: "0 18px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      fontSize: 11,
      fontWeight: 650,
      color: "rgba(14,14,44,.76)",
      borderBottom: `1px solid ${T.hairlineSoft}`
    } }, /* @__PURE__ */ React.createElement("span", null, "\u9884\u89C8"), /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight } }, "\u4F4E\u4FDD\u771F")), /* @__PURE__ */ React.createElement("div", { style: { padding: 14 } }, /* @__PURE__ */ React.createElement("div", { style: { aspectRatio: "3 / 4", borderRadius: 18, overflow: "hidden", background: coverPalette[0], boxShadow: "0 10px 28px rgba(14,14,44,.10)" } }, /* @__PURE__ */ React.createElement(GenerationImageVisual, { item: previewAsset })), /* @__PURE__ */ React.createElement("h2", { style: { margin: "14px 0 8px", fontSize: 17, lineHeight: 1.42, fontWeight: 680, color: T.navy } }, generatedPostCopy.title), /* @__PURE__ */ React.createElement("p", { style: { margin: 0, fontSize: 13.2, lineHeight: 1.75, color: T.navyMid } }, generatedPostCopy.body[0]), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 12, display: "flex", flexWrap: "wrap", gap: 6 } }, generatedPostCopy.tags.slice(0, 4).map((tag) => /* @__PURE__ */ React.createElement("span", { key: tag, style: {
      height: 24,
      padding: "0 8px",
      borderRadius: 999,
      background: T.surface,
      color: T.navyMid,
      display: "inline-flex",
      alignItems: "center",
      fontSize: 10.5,
      fontWeight: 600
    } }, tag))), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 14, paddingTop: 12, borderTop: `1px solid ${T.hairlineSoft}`, color: T.navyLight, fontSize: 11.5 } }, "\u624B\u673A\u7AEF\u5927\u81F4\u6392\u5E03\uFF0C\u4EC5\u7528\u4E8E\u786E\u8BA4\u5C01\u9762\u3001\u6807\u9898\u548C\u6B63\u6587\u987A\u5E8F\u3002"))));
  };
  var CanvasMiniButton = ({ icon, label, active, onClick, children }) => {
    const [hov, setHov] = React.useState(false);
    return /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick,
        onMouseEnter: () => setHov(true),
        onMouseLeave: () => setHov(false),
        title: label,
        style: {
          position: "relative",
          width: 42,
          height: 42,
          borderRadius: 14,
          border: active ? `1px solid rgba(75,77,237,.28)` : `1px solid ${T.hairlineSoft}`,
          background: active ? T.navy : hov ? "rgba(14,14,44,.06)" : "rgba(255,255,255,.82)",
          color: active ? T.white : T.navyMid,
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          cursor: "pointer",
          boxShadow: active ? "0 10px 22px rgba(14,14,44,.14)" : "0 6px 16px rgba(14,14,44,.045)",
          transition: `background .2s ${T.ease}, color .2s ${T.ease}, transform .22s ${T.spring}`
        }
      },
      children || /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 18, stroke: 1.8 }),
      hov && /* @__PURE__ */ React.createElement("span", { style: {
        position: "absolute",
        left: 52,
        top: "50%",
        transform: "translateY(-50%)",
        height: 32,
        padding: "0 12px",
        borderRadius: 12,
        background: T.navy,
        color: T.white,
        display: "inline-flex",
        alignItems: "center",
        whiteSpace: "nowrap",
        fontSize: 12.5,
        fontWeight: 650,
        boxShadow: "0 14px 30px rgba(14,14,44,.18)",
        zIndex: 8,
        pointerEvents: "none"
      } }, label)
    );
  };
  var CanvasFloatingTextToolbar = ({ rect, onClose }) => {
    if (!rect) return null;
    return /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      left: rect.left,
      top: rect.top,
      transform: "translate(-50%, -118%)",
      zIndex: 35,
      display: "flex",
      alignItems: "center",
      gap: 4,
      padding: 4,
      borderRadius: 12,
      background: "rgba(255,255,255,.96)",
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: "0 12px 28px rgba(14,14,44,.12)"
    } }, ["B", "I", "L", "A"].map((item, index) => /* @__PURE__ */ React.createElement("button", { key: item, style: {
      width: 26,
      height: 26,
      borderRadius: 8,
      border: "none",
      background: index === 0 ? "rgba(14,14,44,.06)" : "transparent",
      color: T.navy,
      fontSize: 11.5,
      fontWeight: 700,
      cursor: "pointer"
    } }, item)), /* @__PURE__ */ React.createElement("button", { onClick: onClose, style: {
      width: 26,
      height: 26,
      borderRadius: 8,
      border: "none",
      background: "transparent",
      color: T.navyLight,
      cursor: "pointer"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 11 })));
  };
  var ImageQuickMenu = ({ menu, onClose, onPick }) => {
    if (!menu) return null;
    const actions = [
      { id: "upscale", label: "\u653E\u5927", icon: "expand" },
      { id: "remove-bg", label: "\u53BB\u80CC\u666F", icon: "user" },
      { id: "erase", label: "\u6A61\u76AE\u5DE5\u5177", icon: "minus" },
      { id: "text", label: "\u7F16\u8F91\u6587\u5B57", icon: "edit" },
      { id: "download", label: "\u4E0B\u8F7D", icon: "download" }
    ];
    return /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("div", { onClick: onClose, style: { position: "fixed", inset: 0, zIndex: 70 } }), /* @__PURE__ */ React.createElement("div", { style: {
      position: "fixed",
      left: menu.x,
      top: menu.y,
      width: 180,
      padding: 6,
      borderRadius: 14,
      background: "rgba(255,255,255,.96)",
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: T.shadowLg,
      zIndex: 71,
      backdropFilter: "blur(18px) saturate(1.16)"
    } }, actions.map((action) => /* @__PURE__ */ React.createElement(
      "button",
      {
        key: action.id,
        onClick: () => onPick(action),
        style: {
          width: "100%",
          height: 38,
          border: "none",
          borderRadius: 10,
          background: "transparent",
          color: T.navy,
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          gap: 10,
          padding: "0 10px",
          fontSize: 13,
          fontWeight: 600,
          textAlign: "left"
        },
        onMouseEnter: (e) => e.currentTarget.style.background = T.surface,
        onMouseLeave: (e) => e.currentTarget.style.background = "transparent"
      },
      /* @__PURE__ */ React.createElement(Icon, { name: action.icon, size: 15 }),
      action.label
    ))));
  };
  var ImageCanvasEditor = ({ image, onAction, initialPrompt = "", onOpenInspiration }) => {
    const [activeTool, setActiveTool] = React.useState("upload");
    const [menu, setMenu] = React.useState(null);
    const [prompt, setPrompt] = React.useState(initialPrompt);
    const [notes, setNotes] = React.useState([]);
    const [pendingRefs, setPendingRefs] = React.useState([]);
    const [canvasMenu, setCanvasMenu] = React.useState(null);
    const [canvasText, setCanvasText] = React.useState({ open: false, value: "\u5728\u6B64\u8F93\u5165\u6587\u672C", x: 50, y: 52, selected: false });
    const [dragState, setDragState] = React.useState(null);
    const [toolTip, setToolTip] = React.useState(null);
    const filePickerRef = React.useRef(null);
    const chatFileRef = React.useRef(null);
    const selected = image || GENERATED_IMAGES[0];
    const palette = selected.palette || GENERATION_COVER_OPTIONS[0].palette;
    const paletteTools = [
      { id: "upload", label: "\u672C\u5730\u4E0A\u4F20", icon: "upload" },
      { id: "asset", label: "\u5BFC\u5165\u8D44\u4EA7", icon: "folder" },
      { id: "board", label: "\u6DFB\u52A0\u753B\u677F", icon: "grid" },
      { id: "text", label: "\u6DFB\u52A0\u6587\u672C", icon: "edit" }
    ];
    const submitPrompt = () => {
      const clean = prompt.trim();
      if (!clean) return;
      setNotes((v) => [...v, { id: Date.now(), text: clean }]);
      setPrompt("");
    };
    React.useEffect(() => {
      if (!initialPrompt) return;
      setPrompt(initialPrompt);
    }, [initialPrompt]);
    React.useEffect(() => {
      if (!dragState) return void 0;
      const move = (event) => {
        setCanvasText((v) => ({
          ...v,
          x: Math.max(8, Math.min(92, dragState.startX + (event.clientX - dragState.pointerX) / Math.max(1, dragState.width) * 100)),
          y: Math.max(10, Math.min(88, dragState.startY + (event.clientY - dragState.pointerY) / Math.max(1, dragState.height) * 100))
        }));
      };
      const up = () => setDragState(null);
      window.addEventListener("mousemove", move);
      window.addEventListener("mouseup", up);
      return () => {
        window.removeEventListener("mousemove", move);
        window.removeEventListener("mouseup", up);
      };
    }, [dragState]);
    const pickAction = (action) => {
      setMenu(null);
      setNotes((v) => [...v, { id: Date.now(), text: `\u5DF2\u9009\u62E9\uFF1A${action.label}` }]);
      onAction && onAction(action);
    };
    const openToolMenu = (toolId, event) => {
      setActiveTool(toolId);
      const rect = event?.currentTarget?.getBoundingClientRect?.();
      if (toolId === "upload") {
        filePickerRef.current?.click();
        return;
      }
      if (toolId === "asset") {
        setCanvasMenu({ kind: "asset", left: rect ? rect.right + 12 : 92, top: rect ? rect.top : 88 });
        return;
      }
      if (toolId === "board") {
        setCanvasMenu({ kind: "board", left: rect ? rect.right + 12 : 92, top: rect ? rect.top : 154 });
        return;
      }
      if (toolId === "text") {
        setCanvasMenu(null);
        setCanvasText({ open: true, value: canvasText.value || "\u5728\u6B64\u8F93\u5165\u6587\u672C", x: canvasText.x || 50, y: canvasText.y || 52, selected: true });
        setNotes((v) => [...v, { id: Date.now(), text: "\u5DF2\u6DFB\u52A0\u6587\u672C\u6846" }]);
      }
    };
    return /* @__PURE__ */ React.createElement("div", { style: {
      width: "100%",
      minHeight: "100%",
      display: "flex",
      flexDirection: "column",
      position: "relative"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      flex: 1,
      minHeight: 0,
      padding: "72px 24px 104px",
      display: "grid",
      gridTemplateColumns: "76px minmax(320px, 1fr)",
      gap: 20,
      alignItems: "center"
    } }, /* @__PURE__ */ React.createElement(
      "input",
      {
        ref: filePickerRef,
        type: "file",
        accept: "image/*",
        style: { display: "none" },
        onChange: (e) => {
          const file = e.target.files?.[0];
          if (file) setNotes((v) => [...v, { id: Date.now(), text: `\u5DF2\u4E0A\u4F20\uFF1A${file.name}` }]);
          e.target.value = "";
        }
      }
    ), /* @__PURE__ */ React.createElement(
      "input",
      {
        ref: chatFileRef,
        type: "file",
        accept: "image/*",
        multiple: true,
        style: { display: "none" },
        onChange: (e) => {
          const files = Array.from(e.target.files || []).map((file) => ({
            file,
            preview: file.type?.startsWith("image/") ? URL.createObjectURL(file) : null
          }));
          if (files.length) {
            setPendingRefs((list) => [...list, ...files]);
            setNotes((v) => [...v, { id: Date.now(), text: `\u5DF2\u6DFB\u52A0 ${files.length} \u5F20\u53C2\u8003\u56FE` }]);
          }
          e.target.value = "";
        }
      }
    ), /* @__PURE__ */ React.createElement("div", { style: {
      alignSelf: "center",
      justifySelf: "center",
      display: "grid",
      gap: 9,
      padding: 7,
      borderRadius: 20,
      background: "rgba(255,255,255,.90)",
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: "0 16px 36px rgba(14,14,44,.08)"
    } }, paletteTools.map((tool) => /* @__PURE__ */ React.createElement(
      CanvasMiniButton,
      {
        key: tool.id,
        label: tool.label,
        icon: tool.icon,
        active: activeTool === tool.id,
        onClick: (event) => openToolMenu(tool.id, event)
      },
      tool.text ? /* @__PURE__ */ React.createElement("span", { style: { fontSize: tool.text === "T" ? 22 : 20, fontWeight: 650, lineHeight: 1 } }, tool.text) : null
    ))), /* @__PURE__ */ React.createElement("div", { style: {
      height: "min(68vh, 640px)",
      minHeight: 420,
      borderRadius: 0,
      background: "transparent",
      border: "none",
      boxShadow: "none",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      overflow: "hidden"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      inset: 22,
      backgroundImage: `linear-gradient(${T.hairlineSoft} 1px, transparent 1px), linear-gradient(90deg, ${T.hairlineSoft} 1px, transparent 1px)`,
      backgroundSize: "34px 34px",
      opacity: activeTool === "grid" ? 1 : 0.34,
      pointerEvents: "none"
    } }), /* @__PURE__ */ React.createElement(
      "button",
      {
        onContextMenu: (e) => {
          e.preventDefault();
          setMenu({ x: Math.min(e.clientX, window.innerWidth - 196), y: Math.min(e.clientY, window.innerHeight - 230) });
        },
        onClick: () => setNotes((v) => [...v, { id: Date.now(), text: `\u6B63\u5728\u7F16\u8F91\uFF1A${selected.title}` }]),
        style: {
          width: "min(380px, 62%)",
          maxHeight: "86%",
          aspectRatio: "3 / 4",
          borderRadius: 0,
          border: "none",
          background: palette[0],
          overflow: "hidden",
          position: "relative",
          cursor: "default",
          boxShadow: "0 26px 60px rgba(14,14,44,.16)",
          padding: 0
        }
      },
      /* @__PURE__ */ React.createElement(GenerationImageVisual, { item: selected }),
      /* @__PURE__ */ React.createElement("div", { style: {
        position: "absolute",
        left: 20,
        right: 20,
        bottom: 22,
        color: T.white,
        textAlign: "left",
        textShadow: "0 10px 28px rgba(14,14,44,.35)"
      } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 28, lineHeight: 1.1, fontWeight: 760, letterSpacing: 0 } }, selected.title), /* @__PURE__ */ React.createElement("div", { style: {
        marginTop: 8,
        display: "inline-flex",
        height: 28,
        padding: "0 10px",
        borderRadius: 999,
        alignItems: "center",
        background: "rgba(255,255,255,.66)",
        color: T.navyMid,
        fontSize: 11.5,
        fontWeight: 650
      } }, selected.sub))
    ), canvasMenu?.kind === "asset" && /* @__PURE__ */ React.createElement("div", { style: { position: "fixed", left: canvasMenu.left, top: canvasMenu.top, width: 196, borderRadius: 16, background: "rgba(255,255,255,.96)", border: `1px solid ${T.hairlineSoft}`, boxShadow: T.shadowLg, padding: 10, zIndex: 88 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 7 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 13.5, fontWeight: 700, padding: "2px 4px" } }, "\u5BFC\u5165\u8D44\u4EA7"), /* @__PURE__ */ React.createElement("button", { style: { height: 34, borderRadius: 11, border: `1px solid ${T.hairlineSoft}`, background: "rgba(250,252,254,.88)", cursor: "pointer", display: "flex", alignItems: "center", gap: 7, padding: "0 10px", color: T.navy, fontSize: 13 } }, /* @__PURE__ */ React.createElement(Icon, { name: "image", size: 14 }), "\u5BFC\u5165\u56FE\u7247"), /* @__PURE__ */ React.createElement("button", { style: { height: 34, borderRadius: 11, border: `1px solid ${T.hairlineSoft}`, background: "rgba(250,252,254,.88)", cursor: "pointer", display: "flex", alignItems: "center", gap: 7, padding: "0 10px", color: T.navy, fontSize: 13 } }, /* @__PURE__ */ React.createElement(Icon, { name: "video", size: 14 }), "\u5BFC\u5165\u89C6\u9891"))), canvasMenu?.kind === "board" && /* @__PURE__ */ React.createElement("div", { style: { position: "fixed", left: canvasMenu.left, top: canvasMenu.top, width: 224, borderRadius: 16, background: "rgba(255,255,255,.96)", border: `1px solid ${T.hairlineSoft}`, boxShadow: T.shadowLg, padding: 10, zIndex: 88 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 7 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 13.5, fontWeight: 700, padding: "2px 4px" } }, "\u753B\u677F\u5927\u5C0F"), ["16:9 1920 \xD7 1080", "4:3 1536 \xD7 1024", "1:1 1024 \xD7 1024", "3:4 1024 \xD7 1536", "9:16 1080 \xD7 1920"].map((item) => /* @__PURE__ */ React.createElement("button", { key: item, style: { height: 32, borderRadius: 11, border: `1px solid ${T.hairlineSoft}`, background: "rgba(250,252,254,.88)", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 10px", color: T.navy, fontSize: 13 } }, /* @__PURE__ */ React.createElement("span", { style: { fontWeight: 650 } }, item.split(" ")[0]), /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 11.5 } }, item.split(" ").slice(1).join(" ")))), /* @__PURE__ */ React.createElement("button", { style: { height: 32, borderRadius: 11, border: "none", background: "transparent", color: T.navy, cursor: "pointer", display: "flex", alignItems: "center", gap: 7, padding: "0 4px", fontSize: 13 } }, /* @__PURE__ */ React.createElement(Icon, { name: "plus", size: 14 }), "\u65B0\u589E\u9884\u8BBE\u5C3A\u5BF8"))), canvasText.open && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(
      CanvasFloatingTextToolbar,
      {
        rect: { left: `${canvasText.x}%`, top: `${canvasText.y}%` },
        onClose: () => setCanvasText((v) => ({ ...v, selected: false }))
      }
    ), /* @__PURE__ */ React.createElement(
      "input",
      {
        autoFocus: true,
        value: canvasText.value,
        onMouseDown: (e) => {
          const bounds = e.currentTarget.parentElement?.getBoundingClientRect();
          if (bounds) setDragState({ pointerX: e.clientX, pointerY: e.clientY, startX: canvasText.x, startY: canvasText.y, width: bounds.width, height: bounds.height });
          setCanvasText((v) => ({ ...v, selected: true }));
        },
        onClick: () => setCanvasText((v) => ({ ...v, selected: true })),
        onChange: (e) => setCanvasText((v) => ({ ...v, value: e.target.value })),
        style: {
          position: "absolute",
          left: `${canvasText.x}%`,
          top: `${canvasText.y}%`,
          transform: "translate(-50%, -50%)",
          width: 212,
          border: `1.5px solid ${canvasText.selected ? "rgba(75,77,237,.38)" : "rgba(14,14,44,.12)"}`,
          background: "rgba(255,255,255,.86)",
          color: T.navy,
          fontSize: 15,
          fontFamily: T.fontSans,
          padding: "7px 9px",
          outline: "none",
          cursor: dragState ? "grabbing" : "grab",
          boxShadow: "0 10px 24px rgba(14,14,44,.09)"
        }
      }
    )), /* @__PURE__ */ React.createElement(ImageQuickMenu, { menu, onClose: () => setMenu(null), onPick: pickAction }))), /* @__PURE__ */ React.createElement("div", { style: {
      position: "absolute",
      left: "50%",
      bottom: 18,
      transform: "translateX(-50%)",
      width: "min(720px, calc(100% - 56px))",
      borderRadius: 18,
      background: "rgba(255,255,255,.92)",
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: "0 18px 42px rgba(14,14,44,.10), inset 0 1px 0 rgba(255,255,255,.86)",
      backdropFilter: "blur(18px) saturate(1.16)",
      padding: "10px 10px 10px 14px",
      display: "flex",
      alignItems: "flex-end",
      gap: 10
    } }, /* @__PURE__ */ React.createElement("button", { onClick: () => chatFileRef.current?.click(), style: { ...iconBtnStyle(), flexShrink: 0 } }, /* @__PURE__ */ React.createElement(Icon, { name: "plus", size: 14 })), /* @__PURE__ */ React.createElement(
      "textarea",
      {
        value: prompt,
        onChange: (e) => setPrompt(e.target.value),
        onKeyDown: (e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            submitPrompt();
          }
        },
        placeholder: "\u63CF\u8FF0\u4F60\u60F3\u600E\u4E48\u6539\u8FD9\u5F20\u56FE\uFF0C\u6BD4\u5982\uFF1A\u8BA9\u6807\u9898\u66F4\u6E05\u695A\uFF0C\u80CC\u666F\u66F4\u5E72\u51C0\u2026",
        rows: 1,
        style: {
          flex: 1,
          minHeight: 28,
          maxHeight: 96,
          resize: "none",
          border: "none",
          outline: "none",
          background: "transparent",
          color: T.navy,
          fontFamily: T.fontSans,
          fontSize: 13.5,
          lineHeight: 1.6
        }
      }
    ), /* @__PURE__ */ React.createElement("button", { onClick: submitPrompt, disabled: !prompt.trim(), style: {
      width: 34,
      height: 34,
      borderRadius: "50%",
      border: "none",
      background: prompt.trim() ? T.navy : T.surface,
      color: prompt.trim() ? T.white : T.navyLight,
      cursor: prompt.trim() ? "pointer" : "not-allowed",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "arrowUp", size: 15 }))));
  };
  var Canvas = ({ open, expanded, setExpanded, onClose, onTransform, onPublish, mode, setMode, selectedAsset, selectedImage, width = 540, toolbarCollapsed, setToolbarCollapsed, imagePrompt = "", onOpenInspiration }) => {
    const [data, setData] = React.useState({
      title: "\u4E0A\u6D77\u8FD9 5 \u5BB6\u996D\u5E97\uFF0C\u7B2C\u4E00\u6B21\u53BB\u7167\u7740\u70B9\u5C31\u5F88\u7A33",
      tags: ["\u4E0A\u6D77\u996D\u5E97\u63A8\u8350", "\u4E0A\u6D77\u7F8E\u98DF", "\u5468\u672B\u7EA6\u996D"],
      hook: "\u7B2C\u4E00\u6B21\u53BB\u522B\u4E71\u70B9\uFF0C\u5148\u770B\u8FD9\u4EFD\u4E0D\u8E29\u96F7\u83DC\u5355\u3002",
      intro: "\u6211\u628A\u6700\u8FD1\u6536\u85CF\u7387\u9AD8\u7684\u4E0A\u6D77\u996D\u5E97\u5185\u5BB9\u62C6\u4E86\u4E00\u904D\uFF0C\u771F\u6B63\u6709\u7528\u7684\u4E0D\u662F\u6C1B\u56F4\u8BCD\uFF0C\u800C\u662F\u70B9\u4EC0\u4E48\u3001\u4EC0\u4E48\u65F6\u5019\u53BB\u3001\u9002\u5408\u548C\u8C01\u53BB\u3002",
      items: [
        { name: "\u5148\u770B\u62DB\u724C\u83DC", desc: "\u6BCF\u5BB6\u53EA\u4FDD\u7559 2-3 \u4E2A\u7B2C\u4E00\u6B21\u53BB\u6700\u7A33\u7684\u83DC\uFF0C\u4E0D\u505A\u5927\u800C\u5168\u6E05\u5355\u3002" },
        { name: "\u5199\u6E05\u9002\u5408\u8C01", desc: "\u4E0B\u73ED\u7EA6\u996D\u3001\u670B\u53CB\u5C40\u3001\u60C5\u4FA3\u5C0F\u805A\u5206\u5F00\u8BB2\uFF0C\u7528\u6237\u66F4\u5BB9\u6613\u5224\u65AD\u3002" },
        { name: "\u8865\u4E00\u53E5\u907F\u5751", desc: "\u6392\u961F\u65F6\u95F4\u3001\u53E3\u5473\u504F\u751C\u504F\u54B8\u3001\u4EBA\u5747\u4EF7\u683C\u90FD\u6BD4\u7A7A\u6CDB\u5938\u5956\u66F4\u6709\u7528\u3002" },
        { name: "\u7ED9\u5230\u53D1\u5E03\u65F6\u95F4", desc: "\u996D\u70B9\u524D\u540E\u66F4\u9002\u5408\u63A8\u9001\uFF0C\u6807\u9898\u91CC\u4FDD\u7559\u5730\u70B9\u548C\u573A\u666F\u5173\u952E\u8BCD\u3002" }
      ],
      cta: "\u4ECA\u5929 18:40 \u53D1\uFF0C\u996D\u70B9\u524D\u9002\u5408\u63A8\u7ED9\u6B63\u5728\u627E\u7EA6\u996D\u5730\u70B9\u7684\u4EBA\u3002"
    });
    const [textMenu, setTextMenu] = React.useState(null);
    const handleTextAction = (act) => {
      setTextMenu(null);
      window.getSelection().removeAllRanges();
      if (window.__noriOnTextAction) window.__noriOnTextAction(act);
    };
    if (!open) return null;
    return /* @__PURE__ */ React.createElement("aside", { style: {
      width: expanded ? "100%" : width,
      flexShrink: 0,
      height: "100%",
      background: "linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)",
      borderLeft: `1px solid ${T.hairlineSoft}`,
      display: "flex",
      flexDirection: "column",
      animation: `slideInRight .46s ${T.spring}`,
      position: expanded ? "absolute" : "relative",
      right: 0,
      top: 0,
      zIndex: 20,
      boxShadow: expanded ? "none" : "-18px 0 48px rgba(14,14,44,.055)"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      flex: 1,
      overflow: mode === "image" ? "hidden" : "auto",
      padding: mode === "image" ? 0 : "84px 42px 34px",
      position: "relative",
      background: mode === "image" ? "linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)" : mode === "preview" ? "#f6f7f8" : "linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      maxWidth: mode === "image" ? "none" : mode === "preview" ? 560 : 860,
      margin: "0 auto",
      minHeight: "100%",
      display: "flex",
      alignItems: mode === "preview" ? "center" : mode === "image" ? "stretch" : "flex-start",
      justifyContent: "center"
    } }, mode === "image" ? /* @__PURE__ */ React.createElement(ImageCanvasEditor, { image: selectedImage, initialPrompt: imagePrompt, onOpenInspiration, onAction: () => {
    } }) : mode === "preview" ? /* @__PURE__ */ React.createElement(SimplePhonePreview, { data, selectedAsset }) : /* @__PURE__ */ React.createElement(CanvasDocumentEditor, { data, onSetData: setData })), mode !== "image" && /* @__PURE__ */ React.createElement(TextSelectionMenu, { pos: textMenu, onAction: handleTextAction, onClose: () => setTextMenu(null) })), mode !== "image" && /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: onClose,
        style: {
          position: "absolute",
          left: 18,
          top: 18,
          zIndex: 44,
          width: 38,
          height: 38,
          borderRadius: 14,
          border: `1px solid ${T.hairlineSoft}`,
          background: "rgba(255,255,255,.90)",
          color: T.navy,
          cursor: "pointer",
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          boxShadow: "0 12px 28px rgba(14,14,44,.08)"
        }
      },
      /* @__PURE__ */ React.createElement(Icon, { name: "chevronLeft", size: 15 })
    ), mode === "image" && /* @__PURE__ */ React.createElement("button", { onClick: onClose, style: {
      position: "absolute",
      left: 18,
      top: 18,
      zIndex: 44,
      width: 78,
      height: 40,
      borderRadius: 14,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.90)",
      color: T.navy,
      cursor: "pointer",
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      gap: 7,
      fontSize: 13,
      fontWeight: 680,
      boxShadow: "0 12px 28px rgba(14,14,44,.08)"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "arrowLeft", size: 15 }), "\u9000\u51FA"));
  };
  window.Canvas = Canvas;
  window.PostPreview = PostPreview;
  var ComposerAttachmentPreview = ({ files = [], onRemove }) => {
    if (!files.length) return null;
    return /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 10 } }, files.map((file, index) => {
      const isImage = file.type?.startsWith("image/");
      return /* @__PURE__ */ React.createElement("div", { key: `${file.name}-${index}`, style: {
        width: isImage ? 58 : 132,
        height: 58,
        borderRadius: 14,
        border: `1px solid ${T.hairlineSoft}`,
        background: isImage ? T.surface : "rgba(250,252,254,.86)",
        overflow: "hidden",
        position: "relative",
        boxShadow: "0 8px 18px rgba(14,14,44,.045)"
      } }, isImage ? /* @__PURE__ */ React.createElement("img", { src: file.preview || file.url, alt: "", style: { width: "100%", height: "100%", objectFit: "cover", display: "block" } }) : /* @__PURE__ */ React.createElement("div", { style: { height: "100%", display: "grid", gridTemplateColumns: "34px minmax(0, 1fr)", gap: 7, alignItems: "center", padding: 9 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 32, height: 32, borderRadius: 11, background: T.irisTint, color: T.iris, display: "inline-flex", alignItems: "center", justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: file.type?.startsWith("video/") ? "video" : "document", size: 15 })), /* @__PURE__ */ React.createElement("span", { style: { minWidth: 0, color: T.navyMid, fontSize: 11.5, lineHeight: 1.35, fontWeight: 650, overflow: "hidden", textOverflow: "ellipsis", display: "-webkit-box", WebkitLineClamp: 2, WebkitBoxOrient: "vertical" } }, file.name)), /* @__PURE__ */ React.createElement("button", { onClick: () => onRemove?.(index), style: {
        position: "absolute",
        right: -5,
        top: -5,
        width: 21,
        height: 21,
        borderRadius: "50%",
        border: `1px solid ${T.hairlineSoft}`,
        background: "rgba(255,255,255,.92)",
        color: T.navyMid,
        cursor: "pointer",
        display: "inline-flex",
        alignItems: "center",
        justifyContent: "center",
        boxShadow: "0 6px 14px rgba(14,14,44,.10)"
      } }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 9 })));
    }));
  };
  var ChatComposer = ({ onSend, placeholder = "\u7EE7\u7EED\u8FFD\u95EE Nori\uFF0C\u6216\u63CF\u8FF0\u4F60\u7684\u60F3\u6CD5\u2026", initialValue = "", autoFocusKey, onAttach, canSendExtra = false, attachmentCount = 0, attachmentFiles = [], onRemoveAttachment }) => {
    const [text, setText] = React.useState(initialValue);
    const [focused, setFocused] = React.useState(false);
    const inputRef = React.useRef(null);
    const canSend = Boolean(text.trim()) || canSendExtra;
    React.useEffect(() => {
      if (!initialValue) return;
      setText(initialValue);
      window.setTimeout(() => inputRef.current?.focus(), 80);
    }, [initialValue, autoFocusKey]);
    return /* @__PURE__ */ React.createElement("div", { style: {
      background: "rgba(255,255,255,.86)",
      borderRadius: 18,
      border: `1px solid ${focused ? "rgba(75,77,237,.20)" : T.hairlineSoft}`,
      boxShadow: focused ? `0 0 0 5px rgba(75,77,237,.07), ${T.shadowMd}` : "0 8px 20px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)",
      padding: "16px 17px 12px",
      transition: `border .28s ${T.ease}, box-shadow .36s ${T.spring}`,
      backdropFilter: "blur(22px) saturate(1.18)"
    } }, /* @__PURE__ */ React.createElement(ComposerAttachmentPreview, { files: attachmentFiles, onRemove: onRemoveAttachment }), /* @__PURE__ */ React.createElement(
      "textarea",
      {
        ref: inputRef,
        value: text,
        onChange: (e) => setText(e.target.value),
        onFocus: () => setFocused(true),
        onBlur: () => setFocused(false),
        onKeyDown: (e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            if (canSend) {
              onSend(text.trim());
              setText("");
            }
          }
        },
        placeholder,
        rows: 1,
        style: {
          width: "100%",
          border: "none",
          outline: "none",
          resize: "none",
          background: "transparent",
          fontSize: 14,
          lineHeight: 1.55,
          color: T.navy,
          fontFamily: T.fontSans,
          minHeight: 46,
          maxHeight: 148
        }
      }
    ), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", marginTop: 4 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 4 } }, /* @__PURE__ */ React.createElement(ToolPill, { icon: "paperclip", label: "\u9644\u4EF6", onClick: onAttach }), attachmentCount > 0 && /* @__PURE__ */ React.createElement("span", { style: {
      height: 32,
      padding: "0 10px",
      borderRadius: 999,
      background: "rgba(224,250,244,.88)",
      border: "1px solid rgba(49,208,170,.16)",
      color: T.success,
      display: "inline-flex",
      alignItems: "center",
      fontSize: 12,
      fontWeight: 700
    } }, attachmentCount, " \u4E2A\u6587\u4EF6")), /* @__PURE__ */ React.createElement(
      "button",
      {
        onClick: () => {
          if (canSend) {
            onSend(text.trim());
            setText("");
          }
        },
        disabled: !canSend,
        style: {
          width: 32,
          height: 32,
          borderRadius: "50%",
          border: "none",
          cursor: canSend ? "pointer" : "not-allowed",
          background: canSend ? T.navy : T.surface,
          color: canSend ? T.white : T.navyLight,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          transition: `transform .24s ${T.spring}, background .22s ${T.ease}, color .22s ${T.ease}`
        }
      },
      /* @__PURE__ */ React.createElement(Icon, { name: "arrowUp", size: 15, stroke: 2 })
    )));
  };
  var TransformMenu = ({ open, onClose, onPick, anchorRect }) => {
    if (!open || !anchorRect) return null;
    const opts = [
      { id: "gzh", label: "\u516C\u4F17\u53F7\u957F\u6587", sub: "\u6DF1\u5EA6\u957F\u6587 \xB7 1500\u20133000 \u5B57", icon: "document", tint: "#fff8e0", accent: "#c89b00" },
      { id: "dy", label: "\u6296\u97F3\u77ED\u89C6\u9891", sub: "60s \u53E3\u64AD\u811A\u672C + \u5206\u955C", icon: "video", tint: "#e8e8fd", accent: T.iris },
      { id: "wxsph", label: "\u5FAE\u4FE1\u89C6\u9891\u53F7", sub: "90s \u6A2A\u5C4F \xB7 \u9002\u5408\u79D1\u666E", icon: "play", tint: "#e0faf4", accent: T.success },
      { id: "bili", label: "B \u7AD9\u89C6\u9891", sub: "5 \u5206\u949F\u4EE5\u4E0A \xB7 \u957F\u5185\u5BB9", icon: "bilibili", tint: "#ffe5ec", accent: "#ff4488" }
    ];
    const menuWidth = 320;
    const menuHeight = 286;
    const viewportWidth = typeof window !== "undefined" ? window.innerWidth : 1440;
    const viewportHeight = typeof window !== "undefined" ? window.innerHeight : 900;
    const left = Math.max(16, Math.min(anchorRect.right + 12, viewportWidth - menuWidth - 16));
    const top = Math.max(16, Math.min(anchorRect.top - 28, viewportHeight - menuHeight - 16));
    return /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("div", { onClick: onClose, style: { position: "fixed", inset: 0, zIndex: 100 } }), /* @__PURE__ */ React.createElement("div", { style: {
      position: "fixed",
      top,
      left,
      background: T.white,
      borderRadius: 14,
      boxShadow: T.shadowXl,
      border: `1px solid ${T.hairline}`,
      padding: 8,
      width: 320,
      zIndex: 101,
      animation: "fadeIn .18s ease"
    } }, /* @__PURE__ */ React.createElement("div", { style: { padding: "6px 10px 8px", fontSize: 11, fontWeight: 700, letterSpacing: "0.08em", textTransform: "uppercase", color: T.navyLight } }, "\u8F6C\u5316\u4E3A"), opts.map((o) => /* @__PURE__ */ React.createElement(
      "button",
      {
        key: o.id,
        onClick: () => onPick(o),
        style: {
          width: "100%",
          display: "flex",
          alignItems: "center",
          gap: 12,
          padding: "10px 10px",
          borderRadius: 8,
          background: "transparent",
          border: "none",
          cursor: "pointer",
          textAlign: "left"
        },
        onMouseEnter: (e) => e.currentTarget.style.background = T.surface,
        onMouseLeave: (e) => e.currentTarget.style.background = "transparent"
      },
      /* @__PURE__ */ React.createElement("div", { style: {
        width: 32,
        height: 32,
        borderRadius: 8,
        background: o.tint,
        color: o.accent,
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
      } }, /* @__PURE__ */ React.createElement(Icon, { name: o.icon, size: 16 })),
      /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13, fontWeight: 600, color: T.navy } }, o.label), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11, color: T.navyLight } }, o.sub)),
      /* @__PURE__ */ React.createElement(Icon, { name: "chevronRight", size: 12, color: T.navyLight })
    ))));
  };
  var PublishLinkAccount = ({ onLinked }) => {
    const [linking, setLinking] = React.useState(false);
    const [linked, setLinked] = React.useState(false);
    const trigger = () => {
      setLinking(true);
      setTimeout(() => {
        setLinking(false);
        setLinked(true);
        setTimeout(() => onLinked(), 800);
      }, 1600);
    };
    return /* @__PURE__ */ React.createElement(NoriSays, null, !linked ? /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 12 } }, "\u53D1\u5E03\u524D\u9700\u8981\u5148\u94FE\u63A5\u4F60\u7684\u5C0F\u7EA2\u4E66\u8D26\u53F7\u3002", /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 12.5 } }, "(\u53EA\u6709\u7B2C\u4E00\u6B21\u9700\u8981\uFF0C\u4E4B\u540E\u4F1A\u81EA\u52A8\u94FE\u63A5)")), /* @__PURE__ */ React.createElement("div", { style: {
      background: T.white,
      border: `1px solid ${T.hairline}`,
      borderRadius: 12,
      padding: "14px 16px",
      display: "flex",
      alignItems: "center",
      gap: 12
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      width: 36,
      height: 36,
      borderRadius: 10,
      background: "#ffe5ec",
      color: "#ff4488",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      fontWeight: 800,
      fontSize: 16
    } }, "\u7EA2"), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13, fontWeight: 600, color: T.navy } }, "\u5C0F\u7EA2\u4E66"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11.5, color: T.navyLight } }, linking ? "\u6B63\u5728\u8DF3\u8F6C\u6388\u6743\u2026" : "\u672A\u94FE\u63A5")), /* @__PURE__ */ React.createElement("button", { onClick: trigger, disabled: linking, style: {
      height: 34,
      padding: "0 14px",
      borderRadius: 8,
      border: "none",
      cursor: linking ? "wait" : "pointer",
      background: T.navy,
      color: T.primary,
      fontSize: 12.5,
      fontWeight: 600,
      display: "inline-flex",
      alignItems: "center",
      gap: 6
    } }, linking ? /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("span", { style: { width: 12, height: 12, border: `2px solid ${T.primary}`, borderTopColor: "transparent", borderRadius: "50%", animation: "spin .9s linear infinite", display: "inline-block" } }), " \u6388\u6743\u4E2D") : /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Icon, { name: "link", size: 12 }), " \u94FE\u63A5\u8D26\u53F7")))) : /* @__PURE__ */ React.createElement("div", { style: {
      background: T.white,
      border: `1px solid ${T.hairline}`,
      borderRadius: 12,
      padding: "14px 16px",
      display: "flex",
      alignItems: "center",
      gap: 12,
      animation: "fadeIn .3s"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      width: 36,
      height: 36,
      borderRadius: 10,
      background: T.successTint,
      color: T.success,
      display: "flex",
      alignItems: "center",
      justifyContent: "center"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 18, stroke: 2.4 })), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13, fontWeight: 600, color: T.navy } }, "\u5DF2\u94FE\u63A5 \xB7 \u5C0F\u7EA2\u4E66 @luna_writes"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11.5, color: T.navyLight } }, "\u4E0B\u6B21\u53EF\u4EE5\u76F4\u63A5\u53D1\u5E03"))));
  };
  var PublishDraftSaved = () => /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("div", { style: {
    background: `linear-gradient(135deg, ${T.primaryTint}, ${T.peachTint})`,
    border: `1px solid ${T.hairline}`,
    borderRadius: 14,
    padding: "16px 18px",
    display: "flex",
    alignItems: "center",
    gap: 14
  } }, /* @__PURE__ */ React.createElement("div", { style: {
    width: 40,
    height: 40,
    borderRadius: 12,
    background: T.primary,
    color: T.navy,
    display: "flex",
    alignItems: "center",
    justifyContent: "center"
  } }, /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 20, stroke: 2.6 })), /* @__PURE__ */ React.createElement("div", { style: { flex: 1 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 14, fontWeight: 700, color: T.navy } }, "\u5DF2\u5B58\u5165\u4F60\u7684\u8349\u7A3F\u7BB1"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11.5, color: T.navyMid, marginTop: 2 } }, "\u5C0F\u7EA2\u4E66 App \xB7 \u8349\u7A3F\u7BB1 \xB7 1 \u7BC7\u5F85\u5BA1")), /* @__PURE__ */ React.createElement("button", { style: {
    height: 36,
    padding: "0 14px",
    borderRadius: 10,
    background: T.navy,
    color: T.white,
    border: "none",
    cursor: "pointer",
    fontSize: 12.5,
    fontWeight: 600,
    display: "inline-flex",
    alignItems: "center",
    gap: 6
  } }, "\u53BB\u786E\u8BA4 ", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 12 }))));
  var TransformLaunched = ({ target }) => /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", null, "\u597D\uFF0C\u5F00\u59CB\u628A\u5F53\u524D\u5185\u5BB9\u8F6C\u5316\u4E3A ", /* @__PURE__ */ React.createElement("b", null, target.label), "\u3002", /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 12.5 } }, " (", target.sub, ")")), /* @__PURE__ */ React.createElement("div", { style: {
    marginTop: 10,
    padding: "10px 14px",
    borderRadius: 10,
    background: T.surface,
    color: T.navyMid,
    fontSize: 12.5,
    display: "flex",
    alignItems: "center",
    gap: 8
  } }, /* @__PURE__ */ React.createElement("span", { style: {
    width: 14,
    height: 14,
    borderRadius: "50%",
    border: `2px solid ${T.iris}`,
    borderTopColor: "transparent",
    animation: "spin 1s linear infinite"
  } }), "\u6B63\u5728\u91CD\u7EC4\u7ED3\u6784\u4E0E\u8282\u594F \xB7 \u9002\u914D ", target.label, " \u5E73\u53F0\u7279\u6027\u2026"));
  var GENERATION_TOPIC_OPTIONS = [
    {
      id: "shanghai-first-list",
      title: "\u4E0A\u6D77\u996D\u5E97\u7B2C\u4E00\u6B21\u53BB\u600E\u4E48\u70B9",
      desc: "\u9002\u5408\u505A\u6210\u9AD8\u6536\u85CF\u56FE\u6587\uFF0C\u76F4\u63A5\u89E3\u51B3\u300C\u70B9\u4EC0\u4E48\u4E0D\u8E29\u96F7\u300D\u7684\u95EE\u9898\u3002",
      score: "\u6536\u85CF\u6F5C\u529B 94"
    },
    {
      id: "city-dinner-map",
      title: "\u4E0A\u6D77\u4E0B\u73ED\u540E\u5C0F\u9986\u5730\u56FE",
      desc: "\u66F4\u6709\u57CE\u5E02\u751F\u6D3B\u611F\uFF0C\u9002\u5408\u505A\u7CFB\u5217\u5316\u996D\u5E97\u63A8\u8350\u3002",
      score: "\u6DA8\u7C89\u6F5C\u529B 88"
    },
    {
      id: "budget-date",
      title: "\u4EBA\u5747 80 \u7684\u7EA6\u996D\u4E0D\u8E29\u96F7",
      desc: "\u4EF7\u683C\u951A\u70B9\u6E05\u695A\uFF0C\u5BB9\u6613\u5438\u5F15\u60C5\u4FA3\u3001\u670B\u53CB\u5C40\u548C\u5468\u672B\u805A\u9910\u4EBA\u7FA4\u3002",
      score: "\u4F20\u64AD\u6F5C\u529B 84"
    }
  ];
  var GENERATION_COVER_OPTIONS = [
    { id: "cover-a", label: "A", title: "\u62DB\u724C\u83DC\u8FD1\u666F", palette: ["#F7F9FC", "#D6FF00", "#4B4DED", "#31D0AA", "#0e0e2c"], note: "\u9002\u5408\u6536\u85CF\u578B\u5185\u5BB9", image: "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=900&q=82" },
    { id: "cover-b", label: "B", title: "\u5E97\u5185\u70DF\u706B\u6C14", palette: ["#F3DBDA", "#FAFCFE", "#8C8CA1", "#31D0AA", "#0e0e2c"], note: "\u66F4\u50CF\u771F\u5B9E\u63A2\u5E97", image: "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=900&q=82" },
    { id: "cover-c", label: "C", title: "\u57CE\u5E02\u996D\u70B9\u611F", palette: ["#0e0e2c", "#D6FF00", "#EFEFFD", "#F3DBDA", "#ffffff"], note: "\u70B9\u51FB\u7387\u4F18\u5148", image: "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=900&q=82" }
  ];
  var GENERATED_IMAGES = [
    { id: "img-1", title: "\u5C01\u9762", sub: "\u4E0A\u6D77\u996D\u5E97\u63A8\u8350", palette: ["#F7F9FC", "#D6FF00", "#4B4DED", "#31D0AA", "#0e0e2c"], image: "https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=900&q=82" },
    { id: "img-2", title: "\u7B2C 2 \u56FE", sub: "\u9002\u5408\u8C01\u53BB", palette: ["#EFEFFD", "#ffffff", "#4B4DED", "#D6FF00", "#0e0e2c"], image: "https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=900&q=82" },
    { id: "img-3", title: "\u7B2C 3 \u56FE", sub: "\u5FC5\u70B9\u83DC\u5355", palette: ["#E0FAF4", "#ffffff", "#31D0AA", "#4B4DED", "#0e0e2c"], image: "https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=82" },
    { id: "img-4", title: "\u7B2C 4 \u56FE", sub: "\u907F\u5751\u63D0\u9192", palette: ["#FDF5F5", "#F3DBDA", "#8C8CA1", "#D6FF00", "#0e0e2c"], image: "https://images.unsplash.com/photo-1551218808-94e220e084d2?auto=format&fit=crop&w=900&q=82" },
    { id: "img-5", title: "\u7B2C 5 \u56FE", sub: "\u8DEF\u7EBF\u4E0E\u65F6\u95F4", palette: ["#FAFCFE", "#ECF1F4", "#0e0e2c", "#D6FF00", "#31D0AA"], image: "https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?auto=format&fit=crop&w=900&q=82" }
  ];
  var generatedPostCopy = {
    title: "\u4E0A\u6D77\u8FD9 5 \u5BB6\u996D\u5E97\uFF0C\u7B2C\u4E00\u6B21\u53BB\u7167\u7740\u70B9\u5C31\u5F88\u7A33",
    body: [
      "\u6211\u628A\u6700\u8FD1\u6536\u85CF\u7387\u9AD8\u7684\u4E0A\u6D77\u996D\u5E97\u5185\u5BB9\u62C6\u4E86\u4E00\u904D\uFF0C\u53D1\u73B0\u5927\u5BB6\u6700\u60F3\u8981\u7684\u4E0D\u662F\u6C1B\u56F4\u8BCD\uFF0C\u800C\u662F\uFF1A\u7B2C\u4E00\u6B21\u53BB\u5230\u5E95\u70B9\u4EC0\u4E48\u3001\u4EC0\u4E48\u65F6\u5019\u53BB\u3001\u9002\u5408\u548C\u8C01\u53BB\u3002",
      "\u8FD9\u7248\u9002\u5408\u4E0B\u73ED\u7EA6\u996D\u3001\u5468\u672B\u670B\u53CB\u5C40\u548C\u6765\u4E0A\u6D77\u77ED\u6682\u505C\u7559\u7684\u4EBA\u3002\u6BCF\u5BB6\u90FD\u7528\u300C\u62DB\u724C\u83DC + \u9002\u5408\u573A\u666F + \u907F\u5751\u63D0\u9192\u300D\u6765\u5199\uFF0C\u8BFB\u5B8C\u53EF\u4EE5\u76F4\u63A5\u6536\u85CF\u3002",
      "\u5148\u770B\u83DC\u54C1\u7A33\u5B9A\u5EA6\uFF0C\u518D\u770B\u6392\u961F\u6210\u672C\uFF0C\u6700\u540E\u770B\u62CD\u7167\u6C1B\u56F4\u3002\u522B\u53EA\u4E3A\u4E86\u7F51\u7EA2\u611F\u53BB\uFF0C\u771F\u6B63\u503C\u5F97\u63A8\u8350\u7684\u662F\u5403\u5B8C\u8FD8\u613F\u610F\u4E8C\u5237\u3002"
    ],
    tags: ["#\u4E0A\u6D77\u996D\u5E97\u63A8\u8350", "#\u4E0A\u6D77\u7F8E\u98DF", "#\u5468\u672B\u7EA6\u996D", "#\u5C0F\u7EA2\u4E66\u63A2\u5E97", "#\u4E0D\u8E29\u96F7\u83DC\u5355"],
    publishTime: "\u4ECA\u5929 18:40"
  };
  var GenerationImageVisual = ({ item, overlay = true }) => {
    const palette = item?.palette || GENERATION_COVER_OPTIONS[0].palette;
    return /* @__PURE__ */ React.createElement("div", { style: { width: "100%", height: "100%", position: "relative", background: palette[0], overflow: "hidden" } }, item?.image ? /* @__PURE__ */ React.createElement("img", { src: item.image, alt: "", style: { width: "100%", height: "100%", objectFit: "cover", display: "block", filter: "saturate(.94) contrast(.98)" } }) : /* @__PURE__ */ React.createElement(FlowerVisual, { palette }), overlay && /* @__PURE__ */ React.createElement("div", { style: { position: "absolute", inset: 0, background: "linear-gradient(180deg, rgba(14,14,44,0) 42%, rgba(14,14,44,.34) 100%)" } }));
  };
  var TopicChoiceStep = ({ selected, onSelect, onAiDecide }) => /* @__PURE__ */ React.createElement(
    AgentCardShell,
    {
      label: "Agent \u9009\u9898\u65B9\u5411",
      icon: "target",
      title: "\u6211\u5148\u7ED9\u4F60 3 \u4E2A\u9009\u9898\u65B9\u5411\uFF0C\u9009\u4E00\u4E2A\u7EE7\u7EED\uFF1B\u4E5F\u53EF\u4EE5\u8BA9\u6211\u76F4\u63A5\u51B3\u5B9A\u3002",
      action: /* @__PURE__ */ React.createElement("button", { onClick: onAiDecide, style: { ...pillButtonStyle(false), height: 38, borderRadius: 13, fontSize: 13 } }, /* @__PURE__ */ React.createElement(Icon, { name: "sparkles", size: 14 }), "AI \u5E2E\u6211\u51B3\u5B9A")
    },
    /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10 } }, GENERATION_TOPIC_OPTIONS.map((option) => {
      const active = selected?.id === option.id;
      return /* @__PURE__ */ React.createElement(
        "button",
        {
          key: option.id,
          onClick: () => onSelect(option),
          style: {
            width: "100%",
            border: `1px solid ${active ? "rgba(75,77,237,.24)" : T.hairlineSoft}`,
            background: active ? "rgba(239,239,253,.72)" : "rgba(255,255,255,.82)",
            borderRadius: 16,
            padding: 15,
            cursor: "pointer",
            textAlign: "left",
            boxShadow: active ? "0 12px 26px rgba(75,77,237,.08)" : "0 8px 20px rgba(14,14,44,.04)"
          }
        },
        /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 12, alignItems: "flex-start" } }, /* @__PURE__ */ React.createElement("div", { style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 15, fontWeight: 700, lineHeight: 1.4 } }, option.title), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 6, color: T.navyMid, fontSize: 12.8, lineHeight: 1.62 } }, option.desc)), /* @__PURE__ */ React.createElement("span", { style: { flexShrink: 0, height: 26, padding: "0 9px", borderRadius: 999, background: active ? T.white : "rgba(250,252,254,.88)", color: active ? T.iris : T.navyLight, fontSize: 11.5, fontWeight: 650, display: "inline-flex", alignItems: "center" } }, option.score))
      );
    }))
  );
  var IntentClarificationStep = ({ onConfirm, onSkip }) => {
    const [form, setForm] = React.useState({
      location: "",
      price: "\u4EBA\u5747 80-120",
      platform: "\u5C0F\u7EA2\u4E66"
    });
    const Field = ({ label, hint, children }) => /* @__PURE__ */ React.createElement("label", { style: { display: "grid", gap: 7 } }, /* @__PURE__ */ React.createElement("span", { style: { display: "flex", justifyContent: "space-between", gap: 10, alignItems: "baseline" } }, /* @__PURE__ */ React.createElement("span", { style: { color: T.navy, fontSize: 13.2, fontWeight: 700 } }, label), /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 11.5 } }, hint)), children);
    const inputStyle = {
      width: "100%",
      height: 38,
      borderRadius: 13,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(250,252,254,.82)",
      outline: "none",
      padding: "0 11px",
      color: T.navy,
      fontSize: 13,
      fontFamily: T.fontSans
    };
    return /* @__PURE__ */ React.createElement(
      AgentCardShell,
      {
        label: "Agent \u610F\u56FE\u6F84\u6E05",
        icon: "chat",
        title: "\u6211\u53EA\u8865\u95EE\u7F3A\u5931\u7684\u4FE1\u606F",
        action: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("button", { onClick: onSkip, style: { ...pillButtonStyle(false), height: 36, borderRadius: 12, fontSize: 12.5 } }, "\u8DF3\u8FC7\uFF0C\u5148\u751F\u6210"), /* @__PURE__ */ React.createElement("button", { onClick: () => onConfirm(form), style: { ...pillButtonStyle(true), height: 36, borderRadius: 12, fontSize: 12.5 } }, "\u786E\u8BA4\u7EE7\u7EED", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 13 })))
      },
      /* @__PURE__ */ React.createElement("p", { style: { margin: "0 0 12px", color: T.navyMid, fontSize: 13.1, lineHeight: 1.66 } }, "\u5DF2\u77E5\u9053\u4F60\u8981\u505A\u4E0A\u6D77\u996D\u5E97\u63A8\u8350\uFF0C\u6240\u4EE5\u8FD9\u91CC\u53EA\u5C55\u793A\u7F3A\u5931\u9879\u3002"),
      /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 13 } }, /* @__PURE__ */ React.createElement(Field, { label: "\u5E97\u94FA\u5177\u4F53\u4F4D\u7F6E", hint: "\u7F3A\u5931\u9879" }, /* @__PURE__ */ React.createElement("input", { value: form.location, onChange: (e) => setForm((v) => ({ ...v, location: e.target.value })), placeholder: "\u4F8B\u5982\uFF1A\u9759\u5B89\u5BFA / \u6B66\u5EB7\u8DEF / \u4EBA\u6C11\u5E7F\u573A\u9644\u8FD1", style: inputStyle })), /* @__PURE__ */ React.createElement(Field, { label: "\u9884\u7B97\u4E0E\u573A\u666F", hint: "\u53EF\u8C03\u6574" }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexWrap: "wrap", gap: 7 } }, ["\u4EBA\u5747 80-120", "\u670B\u53CB\u805A\u9910", "\u7EA6\u4F1A\u665A\u9910", "\u4E0B\u73ED\u5FEB\u5403"].map((option) => /* @__PURE__ */ React.createElement("button", { key: option, onClick: () => setForm((v) => ({ ...v, price: option })), style: { ...pillButtonStyle(form.price === option), height: 32, borderRadius: 999, fontSize: 12, padding: "0 11px", fontWeight: 650 } }, option)))), /* @__PURE__ */ React.createElement(Field, { label: "\u9996\u53D1\u5E73\u53F0", hint: "\u5DF2\u63A8\u65AD\uFF0C\u53EF\u6539" }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexWrap: "wrap", gap: 7 } }, ["\u5C0F\u7EA2\u4E66", "\u6296\u97F3", "\u516C\u4F17\u53F7", "\u89C6\u9891\u53F7"].map((option) => /* @__PURE__ */ React.createElement("button", { key: option, onClick: () => setForm((v) => ({ ...v, platform: option })), style: { ...pillButtonStyle(form.platform === option), height: 32, borderRadius: 999, fontSize: 12, padding: "0 11px", fontWeight: 650 } }, option)))))
    );
  };
  var GenerationResearchStep = ({ onOpenDocument, onContinue }) => {
    const sources = [
      { title: "\u5C0F\u7EA2\u4E66\u4E0A\u6D77\u996D\u5E97\u6536\u85CF\u578B\u6807\u9898\u8D8B\u52BF", url: "https://www.xiaohongshu.com", meta: "\u6536\u85CF\u5411 \xB7 \u6807\u9898\u516C\u5F0F" },
      { title: "\u5927\u4F17\u70B9\u8BC4\u9759\u5B89 / \u9EC4\u6D66\u70ED\u95E8\u9910\u5385\u8BC4\u4EF7\u6458\u8981", url: "https://www.dianping.com", meta: "\u8BC4\u4EF7\u75DB\u70B9 \xB7 \u4EBA\u5747\u533A\u95F4" },
      { title: "Nori \u7206\u6B3E\u7D20\u6750\u5E93\uFF1A\u57CE\u5E02\u63A2\u5E97 42 \u6761", url: "#", meta: "\u77E5\u8BC6\u5E93 \xB7 \u5185\u90E8\u6C89\u6DC0" }
    ];
    return /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(
      AgentCardShell,
      {
        label: "Agent Research \u6587\u6863",
        icon: "search",
        title: "\u4E0A\u6D77\u996D\u5E97\u63A8\u8350\u7814\u7A76\u7ED3\u679C\u4E0E\u5185\u5BB9\u7B56\u7565",
        action: /* @__PURE__ */ React.createElement("button", { onClick: onContinue, style: { ...pillButtonStyle(true), height: 38, borderRadius: 13, fontSize: 13 } }, "\u8FDB\u5165\u5185\u5BB9\u5236\u4F5C", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 14 }))
      },
      /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center" } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 11.5, fontWeight: 700 } }, "\u5185\u5BB9\u6587\u6863"), /* @__PURE__ */ React.createElement("button", { onClick: onOpenDocument, style: { ...pillButtonStyle(false), height: 34, borderRadius: 12, fontSize: 12.5 } }, "Canvas \u67E5\u770B", /* @__PURE__ */ React.createElement(Icon, { name: "expand", size: 13 }))),
      /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 12 } }, [
        ["\u7814\u7A76\u7ED3\u679C", "\u6536\u85CF\u7387\u66F4\u9AD8\u7684\u5185\u5BB9\u901A\u5E38\u5148\u56DE\u7B54\u201C\u7B2C\u4E00\u6B21\u53BB\u600E\u4E48\u70B9\u201D\uFF0C\u518D\u8865\u4F4D\u7F6E\u3001\u4EF7\u683C\u548C\u9002\u5408\u573A\u666F\u3002"],
        ["\u5185\u5BB9\u7B56\u7565", "\u5207\u5165\u89D2\u5EA6\u653E\u5728\u201C\u7B2C\u4E00\u6B21\u53BB\u7167\u7740\u70B9\u201D\uFF0C\u56FE\u7247\u8D1F\u8D23\u5EFA\u7ACB\u98DF\u6B32\u548C\u771F\u5B9E\u611F\uFF0C\u6B63\u6587\u8D1F\u8D23\u964D\u4F4E\u51B3\u7B56\u6210\u672C\u3002"],
        ["\u7D20\u6750\u4F7F\u7528", "\u4F18\u5148\u4F7F\u7528\u83DC\u54C1\u8FD1\u666F\u3001\u9910\u684C\u73AF\u5883\u548C\u83DC\u5355\u5C40\u90E8\uFF0C\u4E0D\u505A\u8FC7\u5EA6\u7CBE\u4FEE\uFF0C\u4FDD\u7559\u771F\u5B9E\u5230\u5E97\u611F\u3002"]
      ].map(([label, text]) => /* @__PURE__ */ React.createElement("div", { key: label, style: { display: "grid", gap: 4 } }, /* @__PURE__ */ React.createElement("span", { style: { color: T.navy, fontSize: 12.8, fontWeight: 700 } }, label), /* @__PURE__ */ React.createElement("span", { style: { color: T.navyMid, fontSize: 13, lineHeight: 1.72, fontWeight: 460 } }, text)))),
      /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, sources.map((source) => /* @__PURE__ */ React.createElement("a", { key: source.title, href: source.url, target: "_blank", style: { textDecoration: "none", display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center", padding: "9px 10px", borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: "rgba(250,252,254,.72)", color: T.navyMid } }, /* @__PURE__ */ React.createElement("span", { style: { minWidth: 0, fontSize: 12.6, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" } }, source.title), /* @__PURE__ */ React.createElement("span", { style: { flexShrink: 0, color: T.navyLight, fontSize: 11.2 } }, source.meta)))),
      /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "repeat(5, minmax(0, 1fr))", gap: 9 } }, GENERATED_IMAGES.map((img, index) => /* @__PURE__ */ React.createElement("a", { key: img.id, href: img.image, target: "_blank", style: { textDecoration: "none", color: T.navyMid, minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { aspectRatio: "1 / 1", overflow: "hidden", borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: img.palette[0] } }, /* @__PURE__ */ React.createElement(GenerationImageVisual, { item: img, overlay: false })), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 5, fontSize: 10.8, color: T.navyLight, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, "\u7D20\u6750 ", index + 1))))
    ));
  };
  var FinalOutputStep = ({ onPreview, onTransform, onPublish, onEditImage }) => {
    const [title, setTitle] = React.useState(generatedPostCopy.title);
    const [body, setBody] = React.useState(generatedPostCopy.body.join("\n\n"));
    const [tags, setTags] = React.useState(generatedPostCopy.tags);
    return /* @__PURE__ */ React.createElement(
      AgentCardShell,
      {
        label: "Agent \u8F93\u51FA",
        icon: "document",
        title: "",
        style: { gap: 14 }
      },
      /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 12 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "repeat(5, minmax(0, 1fr))", gap: 10 } }, GENERATED_IMAGES.map((img, index) => /* @__PURE__ */ React.createElement(
        "button",
        {
          key: img.id,
          onClick: () => onEditImage?.(img),
          style: {
            minWidth: 0,
            border: "none",
            background: "transparent",
            padding: 0,
            cursor: "pointer",
            textAlign: "left"
          }
        },
        /* @__PURE__ */ React.createElement("div", { style: { aspectRatio: "3 / 4", borderRadius: 0, overflow: "hidden", background: img.palette[0], position: "relative" } }, /* @__PURE__ */ React.createElement(GenerationImageVisual, { item: img }), /* @__PURE__ */ React.createElement("span", { style: {
          position: "absolute",
          right: 8,
          top: 8,
          width: 22,
          height: 22,
          borderRadius: 8,
          background: "rgba(255,255,255,.76)",
          color: T.navyMid,
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 10.5,
          fontWeight: 760
        } }, index + 1)),
        /* @__PURE__ */ React.createElement("div", { style: { marginTop: 6, color: T.navy, fontSize: 11.8, fontWeight: 700 } }, img.title)
      )))), /* @__PURE__ */ React.createElement("div", { style: {
        paddingTop: 10,
        borderTop: `1px solid ${T.hairlineSoft}`,
        display: "grid",
        gap: 10
      } }, /* @__PURE__ */ React.createElement(
        "input",
        {
          value: title,
          onChange: (e) => setTitle(e.target.value),
          style: {
            width: "100%",
            border: "none",
            background: "transparent",
            outline: "none",
            color: T.navy,
            fontSize: 17,
            fontWeight: 760,
            lineHeight: 1.42,
            fontFamily: T.fontSans,
            padding: 0
          }
        }
      ), /* @__PURE__ */ React.createElement(
        "textarea",
        {
          value: body,
          onChange: (e) => setBody(e.target.value),
          rows: 7,
          style: {
            width: "100%",
            margin: 0,
            border: "none",
            background: "transparent",
            color: T.navyMid,
            fontSize: 13.5,
            lineHeight: 1.82,
            fontFamily: T.fontSans,
            resize: "vertical",
            outline: "none",
            padding: 0
          }
        }
      ))),
      /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 7, flexWrap: "wrap", marginTop: 8 } }, tags.map((tag, index) => /* @__PURE__ */ React.createElement(
        "input",
        {
          key: `${tag}-${index}`,
          value: tag,
          onChange: (e) => setTags((list) => list.map((item, i) => i === index ? e.target.value : item)),
          style: {
            width: `${Math.max(84, tag.length * 13)}px`,
            height: 28,
            padding: "0 10px",
            borderRadius: 999,
            background: "rgba(255,255,255,.78)",
            border: `1px solid ${T.hairlineSoft}`,
            color: T.navyMid,
            display: "inline-flex",
            alignItems: "center",
            fontSize: 12,
            fontWeight: 620,
            outline: "none",
            fontFamily: T.fontSans
          }
        }
      ))),
      /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, flexWrap: "wrap", marginTop: 16 } }, /* @__PURE__ */ React.createElement("button", { onClick: onPreview, style: { ...pillButtonStyle(false), height: 36, borderRadius: 12, fontSize: 12.5 } }, /* @__PURE__ */ React.createElement(Icon, { name: "eye", size: 14 }), "\u9884\u89C8\u6A21\u5F0F"), /* @__PURE__ */ React.createElement("button", { onClick: (e) => onTransform?.(e.currentTarget.getBoundingClientRect()), style: { ...pillButtonStyle(false), height: 36, borderRadius: 12, fontSize: 12.5, background: "rgba(255,255,255,.78)", color: T.navyMid, border: `1px solid ${T.hairlineSoft}` } }, /* @__PURE__ */ React.createElement(Icon, { name: "transform", size: 14 }), "\u8F6C\u6362"), /* @__PURE__ */ React.createElement("button", { onClick: onPublish, style: { ...pillButtonStyle(true), height: 36, borderRadius: 12, fontSize: 12.5, background: T.navy, color: T.white, border: "1px solid rgba(14,14,44,.12)", boxShadow: "0 12px 24px rgba(14,14,44,.14)" } }, /* @__PURE__ */ React.createElement(Icon, { name: "send", size: 14 }), "\u53D1\u5E03")),
      /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexDirection: "column", alignItems: "flex-start", gap: 8 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.success, fontSize: 13.2, fontWeight: 680, marginTop: 8 } }, "\u63A8\u8350\u53D1\u5E03\u65F6\u95F4\uFF1A", generatedPostCopy.publishTime))
    );
  };
  var GenerationPage = ({ initialPrompt, assetDraft, skillDraft, onboardingDraft, inspirationDraft, onBackHome, onNewChat, onOpenAssets, onOpenInsights, onOpenMine, onOpenHomeInspiration }) => {
    const isAssetReview = !!assetDraft;
    const isSkillStart = !!skillDraft;
    const isFreshChat = !initialPrompt && !isAssetReview && !isSkillStart && !onboardingDraft;
    const [stage, setStage] = React.useState(isFreshChat ? 0 : 1);
    const [selectedTopic, setSelectedTopic] = React.useState(null);
    const [selectedCover, setSelectedCover] = React.useState(null);
    const [selectedImage, setSelectedImage] = React.useState(null);
    const [imagesDone, setImagesDone] = React.useState(false);
    const [clarification, setClarification] = React.useState(null);
    const [canvasOpen, setCanvasOpen] = React.useState(false);
    const [canvasExpanded, setCanvasExpanded] = React.useState(true);
    const [mode, setMode] = React.useState("edit");
    const [canvasWidth, setCanvasWidth] = React.useState(760);
    const [toolbarCollapsed, setToolbarCollapsed] = React.useState(false);
    const [navCollapsed, setNavCollapsed] = React.useState(false);
    const [transformOpen, setTransformOpen] = React.useState(false);
    const [transformAnchor, setTransformAnchor] = React.useState(null);
    const [followUps, setFollowUps] = React.useState([]);
    const [imagePrompt, setImagePrompt] = React.useState(inspirationDraft?.prompt || "");
    const scrollRef = React.useRef(null);
    const contentRef = React.useRef(null);
    const bottomAnchorRef = React.useRef(null);
    const scrollJobRef = React.useRef(null);
    const shouldFollowScrollRef = React.useRef(true);
    const selectedCanvasAsset = selectedCover ? {
      palette: selectedCover.palette,
      shape: selectedCover.id === "cover-b" ? "ribbon" : selectedCover.id === "cover-c" ? "bloom" : "petal",
      rotate: selectedCover.id === "cover-c" ? -3 : selectedCover.id === "cover-b" ? 4 : 0,
      label: selectedCover.title
    } : null;
    const sessions = [
      "\u4E0A\u6D77\u996D\u5E97\u63A8\u8350 \xB7 \u5F53\u524D",
      "\u4E0B\u73ED\u540E\u5C0F\u9986\u5730\u56FE",
      "\u4EBA\u5747 80 \u7EA6\u996D\u6E05\u5355",
      "\u4EA7\u54C1\u6D4B\u8BC4 \xB7 AI \u89C6\u9891\u5DE5\u5177\u6A2A\u8BC4"
    ];
    const scrollToLatest = React.useCallback((behavior = "auto", force = false) => {
      const node = scrollRef.current;
      if (!node) return;
      if (!force && !shouldFollowScrollRef.current && !isNearScrollBottom(node)) return;
      if (scrollJobRef.current) window.cancelAnimationFrame(scrollJobRef.current);
      scrollJobRef.current = window.requestAnimationFrame(() => {
        scrollNodeToBottom(node, behavior);
        shouldFollowScrollRef.current = isNearScrollBottom(node, 140);
      });
    }, []);
    React.useEffect(() => {
      shouldFollowScrollRef.current = true;
      scrollToLatest("auto", true);
      const t1 = window.setTimeout(() => scrollToLatest("auto", true), 80);
      const t2 = window.setTimeout(() => scrollToLatest("auto", true), 260);
      return () => {
        window.clearTimeout(t1);
        window.clearTimeout(t2);
      };
    }, [stage, followUps.length, selectedTopic, scrollToLatest]);
    React.useEffect(() => {
      const node = scrollRef.current;
      if (!node) return void 0;
      const onScroll = () => {
        shouldFollowScrollRef.current = isNearScrollBottom(node, 140);
      };
      node.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
      return () => node.removeEventListener("scroll", onScroll);
    }, []);
    React.useEffect(() => {
      if (!scrollRef.current || !contentRef.current) return void 0;
      const observer = new MutationObserver(() => scrollToLatest("auto"));
      const resizeObserver = new ResizeObserver(() => scrollToLatest("auto"));
      observer.observe(contentRef.current, { childList: true, subtree: true, characterData: true });
      resizeObserver.observe(contentRef.current);
      return () => {
        observer.disconnect();
        resizeObserver.disconnect();
      };
    }, [scrollToLatest]);
    const startFromUserPrompt = React.useCallback((text) => {
      if (!text.trim()) return;
      setFollowUps((f) => [...f, { kind: "msg", payload: text.trim(), id: Date.now() }]);
      setStage(1);
    }, []);
    const pickTopic = (topic, ai = false) => {
      setSelectedTopic(topic);
      setClarification(null);
      setFollowUps((f) => [...f, { kind: "msg", payload: ai ? `AI \u5E2E\u6211\u51B3\u5B9A\uFF1A${topic.title}` : `\u9009\u62E9\u9009\u9898\uFF1A${topic.title}`, id: Date.now() }]);
      window.setTimeout(() => setStage(2), 280);
    };
    const advanceGenerationStage = React.useCallback((nextStage) => {
      setStage((current) => current < nextStage ? nextStage : current);
    }, []);
    const onTransformPick = (target) => {
      setTransformOpen(false);
      setTransformAnchor(null);
      setFollowUps((f) => [...f, { kind: "transform", payload: target, id: Date.now() }]);
    };
    const onPublish = () => {
      setFollowUps((f) => [...f, { kind: "link", id: Date.now() }]);
    };
    const onLinked = () => {
      setFollowUps((f) => [...f, { kind: "draft", id: Date.now() + 1 }]);
    };
    const openEditor = () => {
      setMode("text");
      setCanvasExpanded(true);
      setCanvasOpen(true);
    };
    const openPreviewCanvas = () => {
      setMode("preview");
      setCanvasExpanded(false);
      setCanvasWidth(520);
      setCanvasOpen(true);
    };
    const openImageEditor = (image) => {
      setSelectedImage(image);
      setMode("image");
      setCanvasExpanded(true);
      setCanvasOpen(true);
    };
    React.useEffect(() => {
      if (!inspirationDraft?.prompt) return;
      setImagePrompt(inspirationDraft.prompt);
      openImageEditor(GENERATED_IMAGES[0]);
    }, [inspirationDraft?.prompt]);
    return /* @__PURE__ */ React.createElement("div", { style: { display: "flex", height: "100%", width: "100%", background: "linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)", position: "relative", overflow: "hidden" } }, /* @__PURE__ */ React.createElement(
      Sidebar,
      {
        active: "home",
        onNew: onNewChat || (() => {
        }),
        onNavigate: (id) => {
          if (id === "home") onBackHome();
          if (id === "library" && onOpenAssets) onOpenAssets();
          if (id === "insights" && onOpenInsights) onOpenInsights();
          if (id === "mine" && onOpenMine) onOpenMine();
        },
        sessions,
        collapsed: navCollapsed,
        onToggle: () => setNavCollapsed((v) => !v)
      }
    ), /* @__PURE__ */ React.createElement("main", { style: {
      flex: 1,
      display: "flex",
      flexDirection: "column",
      minWidth: 0,
      position: "relative"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      height: 56,
      padding: "0 24px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      borderBottom: `1px solid ${T.hairlineSoft}`,
      background: "rgba(250,252,254,.76)",
      backdropFilter: "blur(18px) saturate(1.16)",
      flexShrink: 0
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 12, minWidth: 0 } }, /* @__PURE__ */ React.createElement("button", { onClick: onBackHome, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "home", size: 16, color: T.navyMid })), /* @__PURE__ */ React.createElement("div", { style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13, fontWeight: 600, color: T.navy, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, onboardingDraft?.topic || selectedTopic?.title || "\u4E0A\u6D77\u996D\u5E97\u63A8\u8350\u56FE\u6587"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 10.5, color: T.navyLight, fontFamily: T.fontMono } }, "Chat \u751F\u6210 \xB7 \u7F16\u8F91\u65F6\u8FDB\u5165 Canvas"))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } })), /* @__PURE__ */ React.createElement("div", { ref: scrollRef, style: { flex: 1, minHeight: 0, overflowY: "auto", padding: "28px 0 24px" } }, /* @__PURE__ */ React.createElement("div", { ref: contentRef, style: {
      maxWidth: 780,
      margin: "0 auto",
      padding: "0 24px",
      display: "flex",
      flexDirection: "column",
      gap: 24
    } }, stage === 0 ? /* @__PURE__ */ React.createElement(
      AgentCardShell,
      {
        label: "Agent \u5F00\u573A",
        icon: "chat",
        title: isSkillStart ? `\u5DF2\u8F7D\u5165\u300C${skillDraft.title}\u300DSkill` : "\u6211\u662F Nori\uFF0C\u53EF\u4EE5\u5E2E\u4F60\u628A\u5185\u5BB9\u4E00\u6B65\u6B65\u505A\u51FA\u6765"
      },
      /* @__PURE__ */ React.createElement("p", { style: { margin: 0 } }, "\u6211\u4F1A\u6309\u9009\u9898\u3001\u610F\u56FE\u6F84\u6E05\u3001\u4EFB\u52A1\u89C4\u5212\u3001Research\u3001\u5185\u5BB9\u5236\u4F5C\u3001Review \u548C Output \u7684\u987A\u5E8F\uFF0C\u5728 chat \u91CC\u9010\u6B65\u751F\u6210\u5E76\u4FDD\u7559\u5386\u53F2\u3002")
    ) : /* @__PURE__ */ React.createElement(Bubble, { from: "user" }, initialPrompt || onboardingDraft?.topic || followUps.find((f) => f.kind === "msg")?.payload || "\u6211\u60F3\u505A\u4E00\u7BC7\u4E0A\u6D77\u996D\u5E97\u63A8\u8350\u56FE\u6587"), stage >= 1 && /* @__PURE__ */ React.createElement(
      TopicChoiceStep,
      {
        selected: selectedTopic,
        onSelect: (topic) => pickTopic(topic),
        onAiDecide: () => pickTopic(GENERATION_TOPIC_OPTIONS[0], true)
      }
    ), selectedTopic && stage >= 2 && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(Bubble, { from: "user" }, "\u9009\u62E9\u9009\u9898\uFF1A", selectedTopic.title), /* @__PURE__ */ React.createElement(
      AgentStepSequence,
      {
        resetKey: `topic-${selectedTopic.id}`,
        parseMessages: ["\u6B63\u5728\u89E3\u6790\u4F60\u9009\u62E9\u7684\u9009\u9898", "\u89E3\u6790\u4E2D", "\u6B63\u5728\u5339\u914D\u4E0A\u6D77\u996D\u5E97\u63A8\u8350\u5185\u5BB9\u7ED3\u6784"],
        reply: "\u6211\u5148\u62C6\u4E00\u4E0B\u8FD9\u4E2A\u9009\u9898\uFF1A\u5B83\u9002\u5408\u505A\u6210\u6536\u85CF\u578B\u4E0A\u6D77\u996D\u5E97\u63A8\u8350\uFF0C\u6838\u5FC3\u662F\u5148\u964D\u4F4E\u7B2C\u4E00\u6B21\u5230\u5E97\u7684\u51B3\u7B56\u6210\u672C\uFF0C\u518D\u7528\u771F\u5B9E\u56FE\u7247\u5EFA\u7ACB\u98DF\u6B32\u548C\u4FE1\u4EFB\u3002",
        onComplete: () => advanceGenerationStage(3)
      }
    )), stage >= 3 && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(
      IntentClarificationStep,
      {
        onConfirm: (form) => {
          setClarification(form);
          setStage(4);
        },
        onSkip: () => setStage(4)
      }
    ), stage > 3 && /* @__PURE__ */ React.createElement(Bubble, { from: "user" }, clarification ? `\u8865\u5145\u4FE1\u606F\uFF1A${[clarification.location || "\u4F4D\u7F6E\u7A0D\u540E\u8865\u5145", clarification.price, clarification.platform].filter(Boolean).join(" / ")}` : "\u8DF3\u8FC7\u8865\u5145\u4FE1\u606F\uFF0C\u5148\u8FDB\u5165\u4EFB\u52A1\u89C4\u5212")), stage >= 4 && /* @__PURE__ */ React.createElement(
      AgentStepSequence,
      {
        resetKey: "generation-planning",
        parseMessages: ["\u6B63\u5728\u751F\u6210\u4EFB\u52A1\u89C4\u5212", "\u89E3\u6790\u4E2D", "\u6B63\u5728\u62C6\u89E3\u6267\u884C\u6B65\u9AA4"],
        reply: "\u4E0B\u9762\u662F\u4EFB\u52A1\u89C4\u5212\u3002\u6211\u4F1A\u5148\u628A\u68C0\u7D22\u3001\u7206\u6B3E\u62C6\u89E3\u3001\u7D20\u6750\u6C89\u6DC0\u548C\u5185\u5BB9\u5236\u4F5C\u5206\u5F00\u8DD1\uFF0C\u4FDD\u8BC1\u540E\u9762\u7684\u56FE\u6587\u4E0D\u662F\u51ED\u7A7A\u751F\u6210\u3002",
        onComplete: () => advanceGenerationStage(5)
      }
    ), stage >= 5 && /* @__PURE__ */ React.createElement(
      GenerationResearchStep,
      {
        onOpenDocument: openEditor,
        onContinue: () => setStage(6)
      }
    ), stage >= 6 && /* @__PURE__ */ React.createElement(
      AgentStepSequence,
      {
        resetKey: "generation-making",
        parseMessages: ["\u6B63\u5728\u5236\u4F5C\u5185\u5BB9", "\u751F\u6210\u4E2D", "\u6B63\u5728\u6574\u5408\u56FE\u7247\u3001\u6B63\u6587\u548C\u6807\u7B7E"],
        reply: "\u5F00\u59CB\u5236\u4F5C\u5185\u5BB9\u3002\u6211\u4F1A\u628A\u5C01\u9762\u3001\u6B63\u6587\u56FE\u3001\u6807\u9898\u3001\u6B63\u6587\u3001\u6807\u7B7E\u548C\u53D1\u5E03\u65F6\u95F4\u653E\u5728\u540C\u4E00\u4EFD\u53EF\u7F16\u8F91\u7ED3\u679C\u91CC\u3002",
        onComplete: () => advanceGenerationStage(7)
      }
    ), stage >= 7 && /* @__PURE__ */ React.createElement(
      FinalOutputStep,
      {
        onPreview: openPreviewCanvas,
        onTransform: (rect) => {
          setTransformAnchor(rect);
          setTransformOpen(true);
        },
        onPublish,
        onEditImage: openImageEditor
      }
    ), followUps.map((f) => {
      if (f.kind === "transform") return /* @__PURE__ */ React.createElement(TransformLaunched, { key: f.id, target: f.payload });
      if (f.kind === "link") return /* @__PURE__ */ React.createElement(PublishLinkAccount, { key: f.id, onLinked });
      if (f.kind === "draft") return /* @__PURE__ */ React.createElement(PublishDraftSaved, { key: f.id });
      return null;
    }), /* @__PURE__ */ React.createElement("div", { ref: bottomAnchorRef, style: { height: 1 } }))), /* @__PURE__ */ React.createElement("div", { style: {
      padding: "12px 24px 18px",
      background: "linear-gradient(to top, rgba(250,252,254,.98) 62%, rgba(250,252,254,0))",
      flexShrink: 0
    } }, /* @__PURE__ */ React.createElement("div", { style: { maxWidth: 780, margin: "0 auto" } }, onboardingDraft && /* @__PURE__ */ React.createElement("div", { style: {
      marginBottom: 10,
      padding: "9px 11px",
      borderRadius: 13,
      background: "rgba(255,255,255,.78)",
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: "0 8px 18px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.86)",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: 12,
      flexWrap: "wrap"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "inline-flex", alignItems: "center", gap: 8, minWidth: 0 } }, /* @__PURE__ */ React.createElement("span", { style: {
      width: 24,
      height: 24,
      borderRadius: 9,
      background: T.successTint,
      color: T.success,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 13, stroke: 2.2 })), /* @__PURE__ */ React.createElement("span", { style: { fontSize: 12.5, color: T.navyMid, fontWeight: 580, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, "\u8D26\u53F7\u89C4\u5212\u5DF2\u542F\u7528 \xB7 \u6765\u81EA\u8D26\u53F7\u5B9A\u4F4D \xB7 ", onboardingDraft.positioning))), /* @__PURE__ */ React.createElement(
      ChatComposer,
      {
        placeholder: stage === 0 ? "\u544A\u8BC9 Nori\uFF1A\u4F60\u60F3\u505A\u4EC0\u4E48\u5185\u5BB9\uFF1F" : "\u7EE7\u7EED\u8FFD\u95EE Nori\uFF0C\u6216\u63CF\u8FF0\u4F60\u7684\u4FEE\u6539\u60F3\u6CD5\u2026",
        initialValue: stage === 0 ? skillDraft ? skillDraft.prompt : onboardingDraft?.topic || "" : "",
        autoFocusKey: skillDraft?.id || onboardingDraft?.topic,
        onSend: (t) => {
          if (stage === 0) startFromUserPrompt(t);
          else setFollowUps((f) => [...f, { kind: "msg", payload: t, id: Date.now() }]);
        }
      }
    )))), /* @__PURE__ */ React.createElement(
      Canvas,
      {
        open: canvasOpen,
        expanded: canvasExpanded,
        setExpanded: setCanvasExpanded,
        onClose: () => setCanvasOpen(false),
        onTransform: (rect) => {
          setTransformAnchor(rect);
          setTransformOpen(true);
        },
        onPublish,
        mode,
        setMode,
        selectedAsset: selectedCanvasAsset,
        selectedImage,
        imagePrompt,
        onOpenInspiration: onOpenHomeInspiration,
        width: canvasWidth,
        toolbarCollapsed,
        setToolbarCollapsed
      }
    ), /* @__PURE__ */ React.createElement(
      TransformMenu,
      {
        open: transformOpen,
        anchorRect: transformAnchor,
        onClose: () => {
          setTransformOpen(false);
          setTransformAnchor(null);
        },
        onPick: onTransformPick
      }
    ));
  };
  window.GenerationPage = GenerationPage;
  window.ToolPill = window.ToolPill;
  var PlanningOption = ({ icon, title, desc, active, onClick }) => /* @__PURE__ */ React.createElement(
    "button",
    {
      onClick,
      style: {
        border: `1px solid ${active ? "rgba(75,77,237,.22)" : T.hairlineSoft}`,
        background: active ? "rgba(239,239,253,.76)" : "rgba(255,255,255,.76)",
        borderRadius: 16,
        padding: "13px 14px",
        cursor: "pointer",
        textAlign: "left",
        display: "flex",
        alignItems: "flex-start",
        gap: 11,
        boxShadow: active ? "0 10px 24px rgba(75,77,237,.07), inset 0 1px 0 rgba(255,255,255,.86)" : "0 8px 20px rgba(14,14,44,.035)",
        transition: `transform .28s ${T.spring}, box-shadow .28s ${T.spring}, border .24s ${T.ease}, background .24s ${T.ease}`
      },
      onMouseEnter: (e) => e.currentTarget.style.transform = "translateY(-2px)",
      onMouseLeave: (e) => e.currentTarget.style.transform = "translateY(0)"
    },
    /* @__PURE__ */ React.createElement("span", { style: {
      width: 34,
      height: 34,
      borderRadius: 12,
      background: active ? T.white : T.surfaceWh,
      color: active ? T.iris : T.navyMid,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      flexShrink: 0,
      boxShadow: "inset 0 1px 0 rgba(255,255,255,.8)"
    } }, /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 16 })),
    /* @__PURE__ */ React.createElement("span", null, /* @__PURE__ */ React.createElement("span", { style: { display: "block", fontSize: 13.5, fontWeight: 720, color: T.navy } }, title), /* @__PURE__ */ React.createElement("span", { style: { display: "block", marginTop: 4, fontSize: 11.8, lineHeight: 1.45, color: T.navyLight } }, desc))
  );
  var PlanningStepper = ({ steps, step, isMobile }) => /* @__PURE__ */ React.createElement("div", { style: {
    display: "inline-flex",
    alignItems: "center",
    gap: isMobile ? 6 : 8,
    maxWidth: "100%",
    overflowX: "auto",
    padding: isMobile ? "5px" : "6px",
    borderRadius: 999,
    background: "rgba(255,255,255,.86)",
    border: `1px solid ${T.hairlineSoft}`,
    boxShadow: "0 10px 26px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.86)"
  } }, steps.map((s, i) => {
    const done = step > s.id;
    const active = step === s.id;
    return /* @__PURE__ */ React.createElement(React.Fragment, { key: s.id }, /* @__PURE__ */ React.createElement("div", { style: {
      display: "inline-flex",
      alignItems: "center",
      gap: 8,
      height: 34,
      padding: "0 10px",
      borderRadius: 999,
      color: active ? T.navy : done ? T.navyMid : T.navySoft,
      fontSize: isMobile ? 12 : 12.5,
      fontWeight: active ? 760 : 680,
      whiteSpace: "nowrap"
    } }, /* @__PURE__ */ React.createElement("span", { style: {
      width: 24,
      height: 24,
      borderRadius: "50%",
      background: done ? T.success : active ? T.navy : "rgba(14,14,44,.055)",
      color: done ? T.white : active ? T.primary : T.navySoft,
      display: "inline-flex",
      alignItems: "center",
      justifyContent: "center",
      fontSize: 11,
      fontFamily: T.fontMono,
      fontWeight: 800,
      flexShrink: 0,
      boxShadow: active ? "0 8px 18px rgba(14,14,44,.14)" : "none"
    } }, done ? "\u2713" : s.id), s.label), i < steps.length - 1 && /* @__PURE__ */ React.createElement("span", { style: { width: 22, height: 1, background: "rgba(14,14,44,.10)", flexShrink: 0 } }));
  }));
  var PlanningCompactProgress = ({ steps, step, isMobile }) => /* @__PURE__ */ React.createElement("div", { style: {
    display: "inline-flex",
    alignItems: "center",
    gap: isMobile ? 8 : 12,
    minWidth: 0
  } }, /* @__PURE__ */ React.createElement("div", { style: { display: "inline-flex", alignItems: "center", gap: isMobile ? 5 : 7 } }, steps.map((s) => {
    const active = step === s.id;
    const done = step > s.id;
    return /* @__PURE__ */ React.createElement(
      "span",
      {
        key: s.id,
        "aria-label": `${s.label}${active ? "\uFF0C\u5F53\u524D\u6B65\u9AA4" : ""}`,
        style: {
          width: active ? 34 : 14,
          height: 7,
          borderRadius: 999,
          background: active || done ? T.navy : "rgba(14,14,44,.12)",
          opacity: active ? 1 : done ? 0.9 : 0.72,
          transition: `width .28s ${T.spring}, background .2s ${T.ease}, opacity .2s ${T.ease}`,
          flexShrink: 0
        }
      }
    );
  })), /* @__PURE__ */ React.createElement("span", { style: {
    color: T.navyLight,
    fontSize: isMobile ? 12.5 : 14,
    fontWeight: 560,
    whiteSpace: "nowrap",
    fontFamily: T.fontMono
  } }, "\u7B2C ", step, " / ", steps.length, " \u6B65"));
  var AttachmentChip = ({ attachment, onRemove }) => {
    const icon = attachment.type === "link" ? "link" : attachment.type === "image" ? "image" : "document";
    return /* @__PURE__ */ React.createElement("span", { style: {
      maxWidth: "100%",
      height: 34,
      padding: "0 9px 0 10px",
      borderRadius: 12,
      background: "rgba(255,255,255,.86)",
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: "0 6px 14px rgba(14,14,44,.035), inset 0 1px 0 rgba(255,255,255,.86)",
      display: "inline-flex",
      alignItems: "center",
      gap: 8,
      color: T.navyMid,
      fontSize: 12.5,
      fontWeight: 620
    } }, /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 14, color: attachment.type === "image" ? T.iris : T.navyMid }), /* @__PURE__ */ React.createElement("span", { style: { minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" } }, attachment.label), /* @__PURE__ */ React.createElement("button", { onClick: onRemove, style: { border: "none", background: "transparent", color: T.navyLight, cursor: "pointer", padding: 0, display: "inline-flex" } }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 12 })));
  };
  var InputMethodModal = ({ type, onClose, onConfirm }) => {
    const [value, setValue] = React.useState(type === "link" ? "https://example.com/meituan/shop/\u6696\u80C3\u5C0F\u9986" : type === "text" ? "\u6211\u5728\u793E\u533A\u9644\u8FD1\u5F00\u4E86\u4E00\u5BB6\u5BB6\u5E38\u5C0F\u9986\uFF0C\u60F3\u505A\u5C0F\u7EA2\u4E66\u5F15\u6D41\u5230\u5E97\u3002" : "");
    const fileRef = React.useRef(null);
    const title = type === "link" ? "\u7C98\u8D34\u7F51\u5740" : type === "image" ? "\u4E0A\u4F20\u56FE\u7247" : "\u76F4\u63A5\u63CF\u8FF0";
    const hint = type === "link" ? "\u53EF\u4EE5\u662F\u5E97\u94FA\u3001\u8D26\u53F7\u3001\u6587\u7AE0\u6216\u7ADE\u54C1\u94FE\u63A5" : type === "image" ? "\u9009\u62E9\u4EA7\u54C1\u56FE\u3001\u83DC\u5355\u622A\u56FE\u6216\u8D26\u53F7\u622A\u56FE" : "\u7528\u4E00\u53E5\u8BDD\u8BF4\u6E05\u695A\u4F60\u662F\u505A\u4EC0\u4E48\u7684";
    const confirm = () => {
      const clean = value.trim();
      if (!clean) return;
      onConfirm({
        type,
        label: type === "link" ? clean.replace(/^https?:\/\//, "") : clean,
        value: clean
      });
    };
    return /* @__PURE__ */ React.createElement("div", { style: { position: "fixed", inset: 0, zIndex: 1200, background: "rgba(14,14,44,.22)", display: "flex", alignItems: "center", justifyContent: "center", padding: 18 } }, /* @__PURE__ */ React.createElement("div", { style: {
      width: "min(460px, 100%)",
      borderRadius: 24,
      background: T.white,
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: "0 36px 90px rgba(14,14,44,.22)",
      padding: 20,
      animation: `fadeInScale .32s ${T.spring} both`
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 14, alignItems: "flex-start", marginBottom: 16 } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("h3", { style: { margin: 0, fontSize: 18, fontWeight: 760, color: T.navy, letterSpacing: 0 } }, title), /* @__PURE__ */ React.createElement("p", { style: { margin: "6px 0 0", fontSize: 12.5, color: T.navyLight, lineHeight: 1.55 } }, hint)), /* @__PURE__ */ React.createElement("button", { onClick: onClose, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 13 }))), type === "image" ? /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement(
      "input",
      {
        ref: fileRef,
        type: "file",
        accept: "image/*",
        style: { display: "none" },
        onChange: (e) => {
          const file = e.target.files?.[0];
          if (file) setValue(file.name);
        }
      }
    ), /* @__PURE__ */ React.createElement("button", { onClick: () => fileRef.current?.click(), style: {
      width: "100%",
      height: 118,
      borderRadius: 18,
      border: "1.5px dashed rgba(14,14,44,.14)",
      background: "rgba(250,252,254,.88)",
      color: T.navyMid,
      cursor: "pointer",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      gap: 9,
      fontSize: 13,
      fontWeight: 650
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "upload", size: 22 }), value || "\u9009\u62E9\u672C\u5730\u56FE\u7247")) : /* @__PURE__ */ React.createElement(
      "textarea",
      {
        value,
        onChange: (e) => setValue(e.target.value),
        rows: type === "text" ? 5 : 3,
        style: {
          width: "100%",
          border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 16,
          background: "rgba(250,252,254,.86)",
          padding: "12px 13px",
          resize: "vertical",
          outline: "none",
          color: T.navy,
          fontSize: 13.5,
          lineHeight: 1.62,
          fontFamily: T.fontSans
        }
      }
    ), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 16 } }, /* @__PURE__ */ React.createElement("button", { onClick: onClose, style: { height: 38, padding: "0 14px", border: "none", background: "transparent", color: T.navyLight, cursor: "pointer", fontSize: 13, fontWeight: 650 } }, "\u53D6\u6D88"), /* @__PURE__ */ React.createElement("button", { onClick: confirm, disabled: !value.trim(), style: {
      height: 38,
      padding: "0 16px",
      borderRadius: 13,
      border: "none",
      background: value.trim() ? T.navy : T.surface,
      color: value.trim() ? T.white : T.navyLight,
      cursor: value.trim() ? "pointer" : "not-allowed",
      fontSize: 13,
      fontWeight: 720
    } }, "\u786E\u8BA4"))));
  };
  var PlanningComposerMulti = ({ attachments, text, setText, onRemoveAttachment, onSend }) => /* @__PURE__ */ React.createElement("div", { style: {
    borderRadius: 20,
    border: `1px solid ${T.hairlineSoft}`,
    background: "rgba(255,255,255,.86)",
    boxShadow: "0 14px 32px rgba(14,14,44,.05), inset 0 1px 0 rgba(255,255,255,.86)",
    padding: 12
  } }, attachments.length > 0 && /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexWrap: "wrap", gap: 8, marginBottom: 10, maxWidth: "100%" } }, attachments.map((att, index) => /* @__PURE__ */ React.createElement(AttachmentChip, { key: `${att.type}-${att.label}-${index}`, attachment: att, onRemove: () => onRemoveAttachment(index) }))), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "minmax(0, 1fr) 38px", gap: 9, alignItems: "end" } }, /* @__PURE__ */ React.createElement(
    "textarea",
    {
      value: text,
      onChange: (e) => setText(e.target.value),
      rows: 2,
      placeholder: attachments.length ? "\u53EF\u4EE5\u7EE7\u7EED\u8865\u5145\u4E00\u53E5\u8BF4\u660E..." : "\u5148\u9009\u62E9\u4E00\u79CD\u8F93\u5165\u65B9\u5F0F\uFF0C\u6216\u76F4\u63A5\u8865\u5145\u4F60\u7684\u60F3\u6CD5",
      style: {
        width: "100%",
        border: "none",
        outline: "none",
        resize: "none",
        background: "transparent",
        color: T.navy,
        minHeight: 48,
        fontSize: 13.5,
        lineHeight: 1.6,
        fontFamily: T.fontSans
      }
    }
  ), /* @__PURE__ */ React.createElement("button", { onClick: onSend, disabled: !attachments.length && !text.trim(), style: {
    width: 38,
    height: 38,
    borderRadius: "50%",
    border: "none",
    background: attachments.length || text.trim() ? T.navy : "rgba(14,14,44,.075)",
    color: attachments.length || text.trim() ? T.white : T.navyLight,
    cursor: attachments.length || text.trim() ? "pointer" : "not-allowed",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center"
  } }, /* @__PURE__ */ React.createElement(Icon, { name: "arrowUp", size: 15, stroke: 2 }))));
  var InlineEditableCard = ({ title, value, onChange, rows = 4 }) => /* @__PURE__ */ React.createElement(PlanningPanel, { title }, /* @__PURE__ */ React.createElement(
    "textarea",
    {
      value,
      onChange: (e) => onChange(e.target.value),
      rows,
      style: {
        width: "100%",
        border: "none",
        borderRadius: 14,
        background: "rgba(250,252,254,.76)",
        padding: 12,
        resize: "vertical",
        outline: "none",
        color: T.navyMid,
        fontSize: 13,
        lineHeight: 1.68,
        fontFamily: T.fontSans,
        boxShadow: `inset 0 0 0 1px ${T.hairlineSoft}`
      }
    }
  ));
  var EditableListPanel = ({ title, items, onChange, muted }) => /* @__PURE__ */ React.createElement(PlanningPanel, { title, muted }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, items.map((text, index) => /* @__PURE__ */ React.createElement(
    "input",
    {
      key: `${title}-${index}`,
      value: text,
      onChange: (e) => onChange(items.map((item, i) => i === index ? e.target.value : item)),
      style: {
        width: "100%",
        minHeight: 36,
        border: `1px solid ${T.hairlineSoft}`,
        borderRadius: 12,
        background: "rgba(250,252,254,.72)",
        color: T.navyMid,
        padding: "0 10px",
        outline: "none",
        fontSize: 12.8,
        fontFamily: T.fontSans
      }
    }
  ))));
  var MiniOnionBurst = ({ active }) => {
    if (!active) return null;
    return /* @__PURE__ */ React.createElement("div", { "aria-hidden": "true", style: { position: "absolute", top: 38, right: 56, width: 1, height: 1, pointerEvents: "none", zIndex: 3 } }, ONION_BURST_ASSETS.map((src, i) => /* @__PURE__ */ React.createElement("img", { key: src, src, alt: "", style: {
      position: "absolute",
      width: 34,
      height: 34,
      objectFit: "contain",
      "--x": `${[-74, 58, 82, -86, 18][i]}px`,
      "--y": `${[-48, -62, 24, 22, -88][i]}px`,
      "--r": `${[-16, 18, 12, -9, 7][i]}deg`,
      animation: `onionPop 1.25s ${i * 38}ms ${T.spring} both`,
      filter: "drop-shadow(0 10px 18px rgba(14,14,44,.12))"
    } })));
  };
  var PlanningChoice = ({ children, active, onClick }) => /* @__PURE__ */ React.createElement(
    "button",
    {
      onClick,
      style: {
        minHeight: 32,
        padding: "0 12px",
        borderRadius: 999,
        border: `1px solid ${active ? "rgba(75,77,237,.16)" : T.hairlineSoft}`,
        background: active ? T.navy : "rgba(255,255,255,.78)",
        color: active ? T.white : T.navyMid,
        fontSize: 12.2,
        fontWeight: active ? 680 : 560,
        cursor: "pointer",
        boxShadow: active ? "0 10px 20px rgba(14,14,44,.12)" : "0 6px 14px rgba(14,14,44,.035)",
        transition: `transform .24s ${T.spring}, box-shadow .24s ${T.spring}, background .2s ${T.ease}, color .2s ${T.ease}`
      },
      onMouseEnter: (e) => e.currentTarget.style.transform = "translateY(-1px)",
      onMouseLeave: (e) => e.currentTarget.style.transform = "translateY(0)"
    },
    children
  );
  var PlanningChoiceGroup = ({ title, hint, options, selected, onToggle, allowMultiple = false }) => /* @__PURE__ */ React.createElement(
    AgentCardShell,
    {
      label: `Agent ${allowMultiple ? "\u591A\u9009" : "\u5355\u9009"}`,
      icon: allowMultiple ? "layers" : "target",
      title,
      bodyStyle: { color: T.navyMid, fontSize: 13.2, lineHeight: 1.68 }
    },
    /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10 } }, hint && /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 12.1, lineHeight: 1.5 } }, hint), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexWrap: "wrap", gap: 8 } }, options.map((option) => {
      const active = allowMultiple ? selected.includes(option) : selected === option;
      return /* @__PURE__ */ React.createElement(AgentChoice, { key: option, active, multiple: allowMultiple, onClick: () => onToggle(option) }, option);
    })))
  );
  var PlanningReveal = ({ show = true, delay = 0, children, style }) => {
    if (!show) return null;
    return /* @__PURE__ */ React.createElement("div", { style: {
      animation: `planningReveal 1.18s ${delay}ms ${T.ease} both`,
      overflow: "hidden",
      willChange: "opacity, transform, clip-path, filter",
      ...style
    } }, children);
  };
  var PLANNING_CHAT_INSET = 36;
  var PlanningPanel = ({ title, children, action, muted, style }) => /* @__PURE__ */ React.createElement("section", { style: {
    width: `calc(100% - ${PLANNING_CHAT_INSET}px)`,
    marginLeft: PLANNING_CHAT_INSET,
    border: `1px solid ${T.hairlineSoft}`,
    background: muted ? "rgba(250,252,254,.68)" : "rgba(255,255,255,.82)",
    borderRadius: 20,
    padding: 18,
    boxShadow: "0 14px 34px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.84)",
    backdropFilter: "blur(18px) saturate(1.14)",
    ...style
  } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginBottom: 14 } }, /* @__PURE__ */ React.createElement("h3", { style: { margin: 0, fontSize: 15.5, fontWeight: 730, color: T.navy, letterSpacing: 0 } }, title), action), children);
  var EditableMiniField = ({ label, value, onChange, multiline }) => /* @__PURE__ */ React.createElement("label", { style: { display: "block" } }, /* @__PURE__ */ React.createElement("span", { style: { display: "block", marginBottom: 6, fontSize: 11.5, color: T.navyLight, fontWeight: 620 } }, label), multiline ? /* @__PURE__ */ React.createElement(
    "textarea",
    {
      value,
      onChange: (e) => onChange(e.target.value),
      rows: 3,
      style: {
        width: "100%",
        border: `1px solid ${T.hairlineSoft}`,
        borderRadius: 13,
        background: "rgba(255,255,255,.72)",
        padding: "10px 11px",
        resize: "vertical",
        outline: "none",
        color: T.navy,
        fontSize: 13,
        lineHeight: 1.55,
        fontFamily: T.fontSans
      }
    }
  ) : /* @__PURE__ */ React.createElement(
    "input",
    {
      value,
      onChange: (e) => onChange(e.target.value),
      style: {
        width: "100%",
        height: 38,
        border: `1px solid ${T.hairlineSoft}`,
        borderRadius: 13,
        background: "rgba(255,255,255,.72)",
        padding: "0 11px",
        outline: "none",
        color: T.navy,
        fontSize: 13,
        fontFamily: T.fontSans
      }
    }
  ));
  var AccountPlanningPage = ({ onBackHome, onNewChat, onOpenAssets, onOpenSkills, onOpenInsights, onComplete }) => {
    const { isCompact, isTablet, isMobile } = useViewport();
    const [navCollapsed, setNavCollapsed] = React.useState(false);
    const [step, setStep] = React.useState(1);
    const [method, setMethod] = React.useState(null);
    const [modalType, setModalType] = React.useState(null);
    const [attachment, setAttachment] = React.useState(null);
    const [rawInput, setRawInput] = React.useState("");
    const [sentIntro, setSentIntro] = React.useState(false);
    const [goal, setGoal] = React.useState(null);
    const [platform, setPlatform] = React.useState(null);
    const [confirmed, setConfirmed] = React.useState({});
    const [copied, setCopied] = React.useState("");
    const [reportBurst, setReportBurst] = React.useState(false);
    const [reportVariant, setReportVariant] = React.useState(0);
    const [diagnosisText, setDiagnosisText] = React.useState({
      position: "\u505A\u9644\u8FD1\u4EBA\u613F\u610F\u6536\u85CF\u7684\u70DF\u706B\u6C14\u5C0F\u9986\u8D26\u53F7\u3002\u4F60\u7684\u4F18\u52BF\u4E0D\u662F\u5927\u54C1\u724C\u611F\uFF0C\u800C\u662F\u7A33\u5B9A\u3001\u771F\u5B9E\u3001\u79BB\u7528\u6237\u5F88\u8FD1\u3002\u5185\u5BB9\u8981\u8BA9\u4EBA\u89C9\u5F97\u4E0B\u73ED\u5C31\u80FD\u53BB\u3002",
      audience: "23-38 \u5C81\u9644\u8FD1\u4E0A\u73ED\u65CF\u3001\u60C5\u4FA3\u548C\u5468\u672B\u7EA6\u996D\u4EBA\u7FA4\uFF0C\u5173\u5FC3\u5473\u9053\u7A33\u5B9A\u3001\u4EF7\u683C\u8212\u670D\u3001\u8DDD\u79BB\u65B9\u4FBF\u3002",
      directions: "\u62DB\u724C\u83DC\u6545\u4E8B\uFF1A\u8BA9\u7528\u6237\u8BB0\u4F4F\u4F60\u548C\u522B\u7684\u5E97\u4E0D\u4E00\u6837\u7684\u5730\u65B9\u3002\n\u771F\u5B9E\u5230\u5E97\u573A\u666F\uFF1A\u964D\u4F4E\u7B2C\u4E00\u6B21\u5230\u5E97\u7684\u5FC3\u7406\u6210\u672C\u3002\n\u672C\u5730\u751F\u6D3B\u653B\u7565\uFF1A\u628A\u9910\u5385\u5185\u5BB9\u53D8\u6210\u53EF\u6536\u85CF\u7684\u4FE1\u606F\u3002",
      benchmarks: "@\u672C\u5730\u5403\u559D\u6307\u5357\uFF1A\u6807\u9898\u6E05\u695A\uFF0C\u9002\u5408\u5B66\u4E60\u9009\u9898\u5305\u88C5\u3002\n@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0\uFF1A\u64C5\u957F\u628A\u5C0F\u5E97\u65E5\u5E38\u62CD\u5F97\u6709\u4EBA\u60C5\u5473\u3002\n@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240\uFF1A\u5348\u9910\u573A\u666F\u5207\u5F97\u7EC6\uFF0C\u5BB9\u6613\u5F15\u6D41\u5230\u5E97\u3002",
      selling: "\u7A33\u5B9A\u5BB6\u5E38\u5473 + \u5E97\u4E3B\u771F\u5B9E\u611F + \u79BB\u9644\u8FD1\u4EBA\u751F\u6D3B\u5F88\u8FD1\u3002"
    });
    const [persona, setPersona] = React.useState({
      name: "\u5DF7\u53E3\u6696\u80C3\u5C0F\u9986",
      bio: "\u6BCF\u5929\u8BA4\u771F\u505A\u4E00\u7897\u6709\u70DF\u706B\u6C14\u7684\u5BB6\u5E38\u996D",
      keywords: "\u4EB2\u5207\u3001\u4F1A\u8BB2\u6545\u4E8B\u3001\u61C2\u672C\u5730\u751F\u6D3B",
      tone: "\u50CF\u719F\u4EBA\u63A8\u8350\u4E00\u6837\u81EA\u7136\uFF0C\u5C11\u4E00\u70B9\u5E7F\u544A\u611F\uFF0C\u591A\u4E00\u70B9\u771F\u5B9E\u4F53\u9A8C",
      cover: "\u6696\u8272\u81EA\u7136\u5149\u3001\u5E97\u5185\u7EC6\u8282\u3001\u83DC\u54C1\u8FD1\u666F\uFF0C\u6807\u9898\u7559\u767D\u6E05\u695A"
    });
    const [pillars, setPillars] = React.useState(["\u62DB\u724C\u83DC\u80CC\u540E\u7684\u6545\u4E8B", "\u9644\u8FD1\u4E0A\u73ED\u65CF\u5348\u9910\u9009\u62E9", "\u8001\u677F\u7684\u4E00\u5929", "\u771F\u5B9E\u987E\u5BA2\u53CD\u9988"]);
    const [calendar, setCalendar] = React.useState([
      { day: "\u5468\u4E00", type: "\u63A2\u5E97\u56FE\u6587", topic: "\u7B2C\u4E00\u6B21\u6765\u5E97\u91CC\uFF0C\u5148\u70B9\u8FD9 3 \u9053\u62DB\u724C\u83DC", ref: "@\u672C\u5730\u5403\u559D\u6307\u5357" },
      { day: "\u5468\u4E8C", type: "\u77ED\u89C6\u9891", topic: "\u540E\u53A8\u5907\u83DC 30 \u79D2\uFF0C\u770B\u770B\u4E00\u7897\u996D\u600E\u4E48\u88AB\u8BA4\u771F\u505A\u597D", ref: "@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0" },
      { day: "\u5468\u4E09", type: "\u56FE\u6587", topic: "\u9644\u8FD1\u4E0A\u73ED\u65CF\u5348\u9910\u4E0D\u8E29\u96F7\u83DC\u5355", ref: "@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240" },
      { day: "\u5468\u56DB", type: "\u957F\u6587", topic: "\u4E00\u5BB6\u5C0F\u5E97\u600E\u4E48\u628A\u56DE\u5934\u5BA2\u7559\u4F4F", ref: "@\u4E3B\u7406\u4EBA\u624B\u8BB0" },
      { day: "\u5468\u4E94", type: "\u77ED\u89C6\u9891", topic: "\u987E\u5BA2\u6700\u5E38\u95EE\u7684 5 \u4E2A\u95EE\u9898", ref: "@\u771F\u5B9E\u63A2\u5E97" },
      { day: "\u5468\u516D", type: "\u56FE\u6587", topic: "\u5468\u672B\u5E26\u670B\u53CB\u6765\u5403\uFF0C\u600E\u4E48\u70B9\u66F4\u5212\u7B97", ref: "@\u672C\u5730\u751F\u6D3B\u5BB6" },
      { day: "\u5468\u65E5", type: "\u590D\u76D8", topic: "\u8FD9\u5468\u6700\u53D7\u6B22\u8FCE\u7684\u4E00\u9053\u83DC", ref: "@\u5C0F\u5E97\u7ECF\u8425\u7B14\u8BB0" }
    ]);
    React.useEffect(() => {
      if (step === 3) {
        setReportBurst(false);
        const raf = window.requestAnimationFrame(() => setReportBurst(true));
        const timer = window.setTimeout(() => setReportBurst(false), 1500);
        return () => {
          window.cancelAnimationFrame(raf);
          window.clearTimeout(timer);
        };
      }
      return void 0;
    }, [step, reportVariant]);
    const defaultDiagnosisText = {
      position: "\u505A\u9644\u8FD1\u4EBA\u613F\u610F\u6536\u85CF\u7684\u70DF\u706B\u6C14\u5C0F\u9986\u8D26\u53F7\u3002\u4F60\u7684\u4F18\u52BF\u4E0D\u662F\u5927\u54C1\u724C\u611F\uFF0C\u800C\u662F\u7A33\u5B9A\u3001\u771F\u5B9E\u3001\u79BB\u7528\u6237\u5F88\u8FD1\u3002\u5185\u5BB9\u8981\u8BA9\u4EBA\u89C9\u5F97\u4E0B\u73ED\u5C31\u80FD\u53BB\u3002",
      audience: "23-38 \u5C81\u9644\u8FD1\u4E0A\u73ED\u65CF\u3001\u60C5\u4FA3\u548C\u5468\u672B\u7EA6\u996D\u4EBA\u7FA4\uFF0C\u5173\u5FC3\u5473\u9053\u7A33\u5B9A\u3001\u4EF7\u683C\u8212\u670D\u3001\u8DDD\u79BB\u65B9\u4FBF\u3002",
      directions: "\u62DB\u724C\u83DC\u6545\u4E8B\uFF1A\u8BA9\u7528\u6237\u8BB0\u4F4F\u4F60\u548C\u522B\u7684\u5E97\u4E0D\u4E00\u6837\u7684\u5730\u65B9\u3002\n\u771F\u5B9E\u5230\u5E97\u573A\u666F\uFF1A\u964D\u4F4E\u7B2C\u4E00\u6B21\u5230\u5E97\u7684\u5FC3\u7406\u6210\u672C\u3002\n\u672C\u5730\u751F\u6D3B\u653B\u7565\uFF1A\u628A\u9910\u5385\u5185\u5BB9\u53D8\u6210\u53EF\u6536\u85CF\u7684\u4FE1\u606F\u3002",
      benchmarks: "@\u672C\u5730\u5403\u559D\u6307\u5357\uFF1A\u6807\u9898\u6E05\u695A\uFF0C\u9002\u5408\u5B66\u4E60\u9009\u9898\u5305\u88C5\u3002\n@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0\uFF1A\u64C5\u957F\u628A\u5C0F\u5E97\u65E5\u5E38\u62CD\u5F97\u6709\u4EBA\u60C5\u5473\u3002\n@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240\uFF1A\u5348\u9910\u573A\u666F\u5207\u5F97\u7EC6\uFF0C\u5BB9\u6613\u5F15\u6D41\u5230\u5E97\u3002",
      selling: "\u7A33\u5B9A\u5BB6\u5E38\u5473 + \u5E97\u4E3B\u771F\u5B9E\u611F + \u79BB\u9644\u8FD1\u4EBA\u751F\u6D3B\u5F88\u8FD1\u3002"
    };
    const canAdvanceStep1 = sentIntro && goal && platform;
    const steps = [
      { id: 1, label: "\u5165\u53E3\u4FE1\u606F" },
      { id: 2, label: "\u8D26\u53F7\u8BCA\u65AD" },
      { id: 3, label: "IP \u753B\u50CF" },
      { id: 4, label: "\u5185\u5BB9\u65E5\u5386" },
      { id: 5, label: "\u5F00\u59CB\u5236\u4F5C" }
    ];
    const diagnosis = {
      position: "\u505A\u9644\u8FD1\u4EBA\u613F\u610F\u6536\u85CF\u7684\u70DF\u706B\u6C14\u5C0F\u9986\u8D26\u53F7",
      reason: "\u4F60\u7684\u4F18\u52BF\u4E0D\u662F\u5927\u54C1\u724C\u611F\uFF0C\u800C\u662F\u7A33\u5B9A\u3001\u771F\u5B9E\u3001\u79BB\u7528\u6237\u5F88\u8FD1\u3002\u5185\u5BB9\u8981\u8BA9\u4EBA\u89C9\u5F97\u4E0B\u73ED\u5C31\u80FD\u53BB\u3002",
      audience: "23-38 \u5C81\u9644\u8FD1\u4E0A\u73ED\u65CF\u3001\u60C5\u4FA3\u548C\u5468\u672B\u7EA6\u996D\u4EBA\u7FA4\uFF0C\u5173\u5FC3\u5473\u9053\u7A33\u5B9A\u3001\u4EF7\u683C\u8212\u670D\u3001\u8DDD\u79BB\u65B9\u4FBF\u3002",
      directions: [
        ["\u62DB\u724C\u83DC\u6545\u4E8B", "\u8BA9\u7528\u6237\u8BB0\u4F4F\u4F60\u548C\u522B\u7684\u5E97\u4E0D\u4E00\u6837\u7684\u5730\u65B9\u3002"],
        ["\u771F\u5B9E\u5230\u5E97\u573A\u666F", "\u964D\u4F4E\u7B2C\u4E00\u6B21\u5230\u5E97\u7684\u5FC3\u7406\u6210\u672C\u3002"],
        ["\u672C\u5730\u751F\u6D3B\u653B\u7565", "\u628A\u9910\u5385\u5185\u5BB9\u53D8\u6210\u53EF\u6536\u85CF\u7684\u4FE1\u606F\u3002"]
      ],
      benchmarks: [
        ["@\u672C\u5730\u5403\u559D\u6307\u5357", "\u6807\u9898\u6E05\u695A\uFF0C\u9002\u5408\u5B66\u4E60\u9009\u9898\u5305\u88C5\u3002"],
        ["@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0", "\u64C5\u957F\u628A\u5C0F\u5E97\u65E5\u5E38\u62CD\u5F97\u6709\u4EBA\u60C5\u5473\u3002"],
        ["@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240", "\u5348\u9910\u573A\u666F\u5207\u5F97\u7EC6\uFF0C\u5BB9\u6613\u5F15\u6D41\u5230\u5E97\u3002"]
      ],
      selling: "\u7A33\u5B9A\u5BB6\u5E38\u5473 + \u5E97\u4E3B\u771F\u5B9E\u611F + \u79BB\u9644\u8FD1\u4EBA\u751F\u6D3B\u5F88\u8FD1\u3002"
    };
    const reportSets = [
      {
        names: ["\u5DF7\u53E3\u6696\u80C3\u5C0F\u9986", "\u9644\u8FD1\u4EBA\u7684\u5BB6\u5E38\u996D", "\u4E0B\u73ED\u6765\u5403\u4E00\u53E3"],
        keywords: ["\u4EB2\u5207\u4F46\u4E0D\u6CB9\u817B", "\u61C2\u672C\u5730\u751F\u6D3B", "\u771F\u5B9E\u4E3B\u7406\u4EBA", "\u7A33\u5B9A\u597D\u5403"],
        phrases: ["\u4ECA\u5929\u8FD9\u7897\u996D\uFF0C\u9002\u5408\u4E0B\u73ED\u540E\u6765\u4E00\u53E3\u3002", "\u7B2C\u4E00\u6B21\u6765\u4E0D\u77E5\u9053\u70B9\u4EC0\u4E48\uFF0C\u5148\u770B\u8FD9\u4E00\u7BC7\u3002", "\u4E0D\u662F\u7F51\u7EA2\u5E97\uFF0C\u4F46\u60F3\u628A\u6BCF\u987F\u996D\u8BA4\u771F\u505A\u597D\u3002"],
        bio: "\u6BCF\u5929\u8BA4\u771F\u505A\u4E00\u7897\u6709\u70DF\u706B\u6C14\u7684\u5BB6\u5E38\u996D\uFF0C\u7ED9\u9644\u8FD1\u4EBA\u4E00\u4E2A\u4E0D\u7528\u7EA0\u7ED3\u7684\u5403\u996D\u9009\u62E9\u3002",
        pillars: ["\u62DB\u724C\u83DC\u6545\u4E8B", "\u5348\u9910\u4E0D\u8E29\u96F7", "\u8001\u677F\u7684\u4E00\u5929", "\u771F\u5B9E\u987E\u5BA2\u53CD\u9988", "\u5468\u672B\u670B\u53CB\u5C40\u83DC\u5355"],
        bloggers: ["@\u672C\u5730\u5403\u559D\u6307\u5357", "@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0", "@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240"],
        covers: ["\u6696\u8272\u81EA\u7136\u5149 + \u83DC\u54C1\u8FD1\u666F + \u5927\u7559\u767D\u6807\u9898", "\u5E97\u95E8\u53E3/\u9910\u684C/\u540E\u53A8\u7EC6\u8282\u4E09\u56FE\u62FC\u8D34", "\u4EBA\u7269\u624B\u90E8\u5165\u955C\uFF0C\u5F31\u5316\u6446\u62CD\u611F"]
      },
      {
        names: ["\u4ECA\u5929\u5403\u6696\u80C3\u996D", "\u793E\u533A\u996D\u70B9\u7814\u7A76\u6240", "\u5C0F\u9986\u8BA4\u771F\u996D"],
        keywords: ["\u9760\u8C31\u63A8\u8350", "\u90BB\u91CC\u611F", "\u4EF7\u683C\u53CB\u597D", "\u4E0B\u73ED\u6CBB\u6108"],
        phrases: ["\u8FD9\u4E0D\u662F\u63A2\u5E97\u5E7F\u544A\uFF0C\u662F\u9644\u8FD1\u4EBA\u771F\u7684\u4F1A\u590D\u5403\u7684\u83DC\u5355\u3002", "\u5982\u679C\u4F60\u53EA\u6709 30 \u5206\u949F\u5403\u5348\u996D\uFF0C\u53EF\u4EE5\u8FD9\u4E48\u70B9\u3002", "\u5C0F\u5E97\u6700\u52A8\u4EBA\u7684\u5730\u65B9\uFF0C\u662F\u6BCF\u5929\u90FD\u7A33\u5B9A\u3002"],
        bio: "\u8BB0\u5F55\u4E00\u5BB6\u793E\u533A\u5C0F\u9986\u7684\u65E5\u5E38\u83DC\u5355\u3001\u771F\u5B9E\u5BA2\u4EBA\u548C\u8BA9\u4EBA\u5B89\u5FC3\u7684\u5BB6\u5E38\u5473\u3002",
        pillars: ["30 \u5206\u949F\u5348\u9910\u65B9\u6848", "\u590D\u5403\u83DC\u5355", "\u5C0F\u5E97\u5E55\u540E", "\u672C\u5468\u65B0\u54C1", "\u9644\u8FD1\u751F\u6D3B\u8DEF\u7EBF"],
        bloggers: ["@\u901A\u52E4\u5348\u9910\u5730\u56FE", "@\u5C0F\u5E97\u89C2\u5BDF\u5458", "@\u9644\u8FD1\u751F\u6D3B\u624B\u518C"],
        covers: ["\u6D45\u8272\u684C\u9762 + \u4FEF\u62CD\u5957\u9910 + \u624B\u5199\u611F\u6807\u9898", "\u8001\u677F\u51FA\u955C + \u83DC\u54C1\u7279\u5199 + \u771F\u5B9E\u73AF\u5883", "\u4F4E\u9971\u548C\u6696\u8272\uFF0C\u5F3A\u8C03\u5E72\u51C0\u548C\u53EF\u4FE1"]
      }
    ];
    const report = reportSets[reportVariant % reportSets.length];
    const setCalendarItem = (index, patch) => {
      setCalendar((items) => items.map((item, i) => i === index ? { ...item, ...patch } : item));
    };
    const firstTopic = calendar[0]?.topic || "\u7B2C\u4E00\u6B21\u6765\u5E97\u91CC\uFF0C\u5148\u70B9\u8FD9 3 \u9053\u62DB\u724C\u83DC";
    const complete = () => onComplete({
      topic: `\u5C0F\u7EA2\u4E66\u56FE\u6587\uFF1A${firstTopic}`,
      platform: platform || "\u5C0F\u7EA2\u4E66",
      positioning: diagnosis.position,
      persona,
      pillars
    });
    const memory = /* @__PURE__ */ React.createElement("section", { style: {
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.82)",
      borderRadius: 22,
      padding: 16,
      boxShadow: "0 16px 38px rgba(14,14,44,.052), inset 0 1px 0 rgba(255,255,255,.86)"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 } }, /* @__PURE__ */ React.createElement("h3", { style: { margin: 0, fontSize: 14.5, fontWeight: 760, color: T.navy } }, "IP Memory"), /* @__PURE__ */ React.createElement("span", { style: { fontSize: 10.5, color: T.navyLight, fontFamily: T.fontMono } }, Math.min(5, [sentIntro, goal, platform, method, step >= 2].filter(Boolean).length), "/5")), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 9 } }, [
      ["\u8D5B\u9053", "\u672C\u5730\u751F\u6D3B / \u5C0F\u9910\u996E", sentIntro],
      ["\u76EE\u6807", goal || "\u5F85\u9009\u62E9", !!goal],
      ["\u5E73\u53F0", platform || "\u5F85\u9009\u62E9", !!platform],
      ["\u4EA7\u54C1", methods.length ? "\u5BB6\u5E38\u83DC\u3001\u5348\u9910\u3001\u9644\u8FD1\u5230\u5E97" : "\u5F85\u8BC6\u522B", methods.length > 0],
      ["\u5B9A\u4F4D", step >= 2 ? diagnosis.position : "\u5F85\u8BCA\u65AD", step >= 2]
    ].map(([k, v, done]) => /* @__PURE__ */ React.createElement("div", { key: k, style: {
      padding: "10px 10px",
      borderRadius: 13,
      background: done ? "rgba(224,250,244,.62)" : "rgba(246,248,251,.72)",
      border: `1px solid ${done ? "rgba(49,208,170,.20)" : T.hairlineSoft}`,
      animation: done ? `memoryReady .48s ${T.spring} both` : "none"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8, marginBottom: 4 } }, /* @__PURE__ */ React.createElement("span", { style: { color: done ? T.success : T.navyLight, fontSize: 11.5, fontWeight: 720 } }, k), /* @__PURE__ */ React.createElement("span", { style: { width: 18, height: 18, borderRadius: "50%", background: done ? T.success : "rgba(14,14,44,.06)", color: T.white, display: "inline-flex", alignItems: "center", justifyContent: "center" } }, done && /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 10, stroke: 2.4 }))), /* @__PURE__ */ React.createElement("div", { style: { color: done ? T.navy : T.navyLight, fontSize: 12.2, fontWeight: done ? 650 : 520, lineHeight: 1.45 } }, v)))));
    const copyText = (text) => {
      setCopied(text);
      navigator.clipboard?.writeText(text).catch(() => {
      });
      window.setTimeout(() => setCopied(""), 1100);
    };
    return /* @__PURE__ */ React.createElement("div", { style: { display: "flex", height: "100%", width: "100%", background: "linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)", overflow: "hidden" } }, !isTablet && /* @__PURE__ */ React.createElement(
      Sidebar,
      {
        active: "home",
        onNew: onNewChat,
        onNavigate: (id) => {
          if (id === "home") onBackHome();
          if (id === "library") onOpenAssets && onOpenAssets();
          if (id === "skills") onOpenSkills && onOpenSkills();
          if (id === "insights") onOpenInsights && onOpenInsights();
        },
        sessions: ["\u8D26\u53F7\u89C4\u5212 \xB7 \u5F53\u524D", "\u4E0A\u6D77\u5496\u5561\u9986 City Walk Top 10", "\u4EA7\u54C1\u6D4B\u8BC4 \xB7 AI \u89C6\u9891\u5DE5\u5177\u6A2A\u8BC4"],
        collapsed: navCollapsed,
        onToggle: () => setNavCollapsed((v) => !v)
      }
    ), /* @__PURE__ */ React.createElement("main", { style: { flex: 1, overflow: "auto", position: "relative", background: "linear-gradient(180deg, #FFFFFF 0%, #FBFCFE 54%, #F7F9FC 100%)" } }, /* @__PURE__ */ React.createElement("div", { style: {
      position: "sticky",
      top: 0,
      zIndex: 8,
      height: isMobile ? "auto" : 58,
      padding: isMobile ? "12px 16px" : "0 24px",
      display: "flex",
      alignItems: isMobile ? "stretch" : "center",
      justifyContent: "space-between",
      gap: 14,
      borderBottom: `1px solid ${T.hairlineSoft}`,
      background: "rgba(250,252,254,.78)",
      backdropFilter: "blur(18px) saturate(1.16)",
      flexDirection: isMobile ? "column" : "row"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 12, minWidth: 0 } }, /* @__PURE__ */ React.createElement("button", { onClick: onBackHome, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "home", size: 15, color: T.navyMid })), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13.5, fontWeight: 720, color: T.navy } }, "\u8D26\u53F7\u89C4\u5212"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11, color: T.navyLight } }, "\u7528\u6700\u5C11\u7684\u4FE1\u606F\uFF0C\u5EFA\u7ACB\u53EF\u6267\u884C\u7684\u8D26\u53F7\u7CFB\u7EDF"))), isMobile ? nav : /* @__PURE__ */ React.createElement("div", { style: { width: isCompact ? 520 : 610 } }, nav)), /* @__PURE__ */ React.createElement("div", { style: {
      maxWidth: isMobile ? "100%" : 1180,
      margin: "0 auto",
      padding: isMobile ? "22px 18px 42px" : "34px 42px 58px",
      display: "grid",
      gridTemplateColumns: isMobile ? "1fr" : isCompact ? "minmax(0, 1fr) 260px" : "170px minmax(0, 1fr) 292px",
      gap: isMobile ? 18 : 22,
      alignItems: "start"
    } }, !isMobile && /* @__PURE__ */ React.createElement("div", { style: { position: "sticky", top: 88 } }, nav), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 18 } }, isMobile && memory, step === 1 && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 8, fontSize: 15, fontWeight: 680 } }, "\u5148\u7ED9\u6211\u4E00\u70B9\u7EBF\u7D22\u5C31\u884C\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13 } }, "\u53EF\u4EE5\u8D34\u94FE\u63A5\u3001\u4F20\u622A\u56FE\uFF0C\u6216\u8005\u76F4\u63A5\u8BF4\u4F60\u662F\u505A\u4EC0\u4E48\u7684\u3002\u6211\u4F1A\u628A\u540E\u9762\u7684\u95EE\u9898\u538B\u5230 3 \u8F6E\u4EE5\u5185\u3002")), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u9009\u62E9\u8F93\u5165\u65B9\u5F0F" }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "repeat(3, minmax(0, 1fr))", gap: 10 } }, /* @__PURE__ */ React.createElement(PlanningOption, { icon: "link", title: "\u7C98\u8D34\u94FE\u63A5", desc: "\u5E97\u94FA / \u8D26\u53F7 / \u6587\u7AE0", active: method === "link", onClick: () => {
      setMethod("link");
      setRawInput("https://example.com/meituan/shop/\u6696\u80C3\u5C0F\u9986");
    } }), /* @__PURE__ */ React.createElement(PlanningOption, { icon: "image", title: "\u4E0A\u4F20\u56FE\u7247", desc: "\u4EA7\u54C1\u56FE / \u622A\u56FE", active: method === "image", onClick: () => {
      setMethod("image");
      setRawInput("\u5DF2\u6A21\u62DF\u4E0A\u4F20\uFF1A\u5E97\u94FA\u83DC\u5355\u622A\u56FE.png");
    } }), /* @__PURE__ */ React.createElement(PlanningOption, { icon: "chat", title: "\u76F4\u63A5\u63CF\u8FF0", desc: "\u6211\u662F\u505A\u4EC0\u4E48\u7684", active: method === "text", onClick: () => {
      setMethod("text");
      setRawInput("\u6211\u5728\u793E\u533A\u9644\u8FD1\u5F00\u4E86\u4E00\u5BB6\u5BB6\u5E38\u5C0F\u9986\uFF0C\u60F3\u505A\u5C0F\u7EA2\u4E66\u5F15\u6D41\u5230\u5E97\u3002");
    } })), /* @__PURE__ */ React.createElement(
      "textarea",
      {
        value: rawInput,
        onChange: (e) => setRawInput(e.target.value),
        placeholder: "\u628A\u94FE\u63A5\u3001\u622A\u56FE\u8BF4\u660E\u6216\u4E00\u53E5\u63CF\u8FF0\u653E\u5728\u8FD9\u91CC",
        rows: 3,
        style: {
          marginTop: 12,
          width: "100%",
          border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 15,
          background: "rgba(250,252,254,.72)",
          padding: "12px 13px",
          resize: "vertical",
          outline: "none",
          color: T.navy,
          fontSize: 13,
          lineHeight: 1.55,
          fontFamily: T.fontSans
        }
      }
    )), method && /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 12 } }, "\u6536\u5230\uFF01\u6211\u770B\u5230\u4F60\u662F\u505A\u672C\u5730\u5C0F\u9910\u996E\u7684\uFF0C\u4E3B\u6253\u5BB6\u5E38\u83DC\u548C\u9644\u8FD1\u5230\u5E97\u3002\u4F60\u60F3\u901A\u8FC7\u793E\u5A92\u4E3B\u8981\u505A\u4EC0\u4E48\uFF1F"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, flexWrap: "wrap" } }, ["\u5F15\u6D41\u5230\u5E97", "\u54C1\u724C\u66DD\u5149", "\u7EBF\u4E0A\u5356\u8D27"].map((v) => /* @__PURE__ */ React.createElement(PlanningChoice, { key: v, active: goal === v, onClick: () => setGoal(v) }, v)))), goal && /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 12 } }, "\u660E\u767D\u3002\u4F60\u5E0C\u671B\u5148\u5728\u54EA\u4E2A\u5E73\u53F0\u505A\uFF1F"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, flexWrap: "wrap" } }, ["\u5C0F\u7EA2\u4E66", "\u6296\u97F3", "\u90FD\u60F3\u8BD5\u8BD5"].map((v) => /* @__PURE__ */ React.createElement(PlanningChoice, { key: v, active: platform === v, onClick: () => setPlatform(v) }, v)))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(2), disabled: !canAdvanceStep1, style: {
      height: 40,
      padding: "0 18px",
      borderRadius: 13,
      border: "none",
      background: canAdvanceStep1 ? T.navy : T.surface,
      color: canAdvanceStep1 ? T.white : T.navyLight,
      cursor: canAdvanceStep1 ? "pointer" : "not-allowed",
      fontSize: 13,
      fontWeight: 700,
      boxShadow: canAdvanceStep1 ? "0 12px 24px rgba(14,14,44,.14)" : "none"
    } }, "\u8FDB\u5165\u8D26\u53F7\u8BCA\u65AD"))), step === 2 && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 4, fontSize: 15, fontWeight: 680 } }, "\u6211\u5148\u628A\u8D26\u53F7\u5B9A\u4F4D\u62C6\u51FA\u6765\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13 } }, "\u4E0B\u9762\u6BCF\u4E00\u9879\u90FD\u53EF\u4EE5\u786E\u8BA4\u6216\u8C03\u6574\uFF1B\u73B0\u5728\u5148\u7528\u6700\u5BB9\u6613\u6267\u884C\u7684\u7248\u672C\u3002")), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u63A8\u8350\u8D26\u53F7\u5B9A\u4F4D" }, /* @__PURE__ */ React.createElement("h2", { style: { margin: 0, fontSize: isMobile ? 20 : 23, lineHeight: 1.22, color: T.navy, fontWeight: 760 } }, diagnosis.position), /* @__PURE__ */ React.createElement("p", { style: { margin: "10px 0 0", color: T.navyMid, fontSize: 13, lineHeight: 1.65 } }, diagnosis.reason)), [
      ["\u76EE\u6807\u53D7\u4F17\u753B\u50CF", diagnosis.audience],
      ["\u5DEE\u5F02\u5316\u5356\u70B9", diagnosis.selling]
    ].map(([title, body]) => /* @__PURE__ */ React.createElement(PlanningPanel, { key: title, title, action: /* @__PURE__ */ React.createElement(PlanningChoice, { active: confirmed[title], onClick: () => setConfirmed((c) => ({ ...c, [title]: !c[title] })) }, confirmed[title] ? "\u5DF2\u786E\u8BA4" : "\u786E\u8BA4") }, /* @__PURE__ */ React.createElement("p", { style: { margin: 0, color: T.navyMid, fontSize: 13, lineHeight: 1.65 } }, body))), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u5185\u5BB9\u65B9\u5411\u5EFA\u8BAE" }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10 } }, diagnosis.directions.map(([title, body]) => /* @__PURE__ */ React.createElement("div", { key: title, style: { padding: 13, borderRadius: 14, background: "rgba(250,252,254,.72)", border: `1px solid ${T.hairlineSoft}` } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13.5, fontWeight: 720, color: T.navy } }, title), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 4, fontSize: 12.5, color: T.navyMid, lineHeight: 1.55 } }, body))))), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u5BF9\u6807\u8D26\u53F7\u63A8\u8350" }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 9 } }, diagnosis.benchmarks.map(([name, body]) => /* @__PURE__ */ React.createElement("div", { key: name, style: { display: "flex", gap: 10, alignItems: "center" } }, /* @__PURE__ */ React.createElement("span", { style: { width: 34, height: 34, borderRadius: "50%", background: T.irisTint, color: T.iris, display: "inline-flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 800 } }, name.slice(1, 2)), /* @__PURE__ */ React.createElement("span", { style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("span", { style: { display: "block", fontSize: 13, fontWeight: 700, color: T.navy } }, name), /* @__PURE__ */ React.createElement("span", { style: { display: "block", fontSize: 12, color: T.navyLight } }, body)))))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(4), style: { border: "none", background: "transparent", color: T.navyLight, cursor: "pointer", fontSize: 12.5, fontWeight: 600 } }, "\u8DF3\u8FC7\uFF0C\u76F4\u63A5\u751F\u6210"), /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(3), style: { height: 40, padding: "0 18px", borderRadius: 13, border: "none", background: T.navy, color: T.white, cursor: "pointer", fontSize: 13, fontWeight: 700, boxShadow: "0 12px 24px rgba(14,14,44,.14)" } }, "\u770B\u8D77\u6765\u4E0D\u9519\uFF0C\u7EE7\u7EED"))), step === 3 && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 4, fontSize: 15, fontWeight: 680 } }, "\u5B9A\u4F4D\u53EF\u4EE5\u843D\u6210\u4E00\u4E2A\u53EF\u6267\u884C\u7684 IP \u7CFB\u7EDF\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13 } }, "\u8FD9\u4E9B\u5185\u5BB9\u90FD\u53EF\u4EE5\u6539\uFF0C\u786E\u8BA4\u540E\u4F1A\u7528\u4E8E\u540E\u7EED\u5185\u5BB9\u751F\u6210\u3002")), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u4EBA\u8BBE\u5361\u7247" }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "1fr 1fr", gap: 12 } }, /* @__PURE__ */ React.createElement(EditableMiniField, { label: "\u8D26\u53F7\u540D\u5EFA\u8BAE", value: persona.name, onChange: (v) => setPersona((p) => ({ ...p, name: v })) }), /* @__PURE__ */ React.createElement(EditableMiniField, { label: "\u4EBA\u8BBE\u5173\u952E\u8BCD", value: persona.keywords, onChange: (v) => setPersona((p) => ({ ...p, keywords: v })) }), /* @__PURE__ */ React.createElement("div", { style: { gridColumn: isMobile ? "auto" : "span 2" } }, /* @__PURE__ */ React.createElement(EditableMiniField, { label: "\u7B7E\u540D\u5EFA\u8BAE", value: persona.bio, onChange: (v) => setPersona((p) => ({ ...p, bio: v })) })))), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u5185\u5BB9\u98CE\u683C" }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 12 } }, /* @__PURE__ */ React.createElement(EditableMiniField, { label: "\u8BED\u6C14\u8C03\u6027 / \u5E38\u7528\u53E5\u5F0F", multiline: true, value: persona.tone, onChange: (v) => setPersona((p) => ({ ...p, tone: v })) }), /* @__PURE__ */ React.createElement(EditableMiniField, { label: "\u5C01\u9762\u98CE\u683C\u65B9\u5411", multiline: true, value: persona.cover, onChange: (v) => setPersona((p) => ({ ...p, cover: v })) }))), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u5185\u5BB9\u652F\u67F1" }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, pillars.map((pillar, index) => /* @__PURE__ */ React.createElement("div", { key: index, style: { display: "flex", gap: 8 } }, /* @__PURE__ */ React.createElement("input", { value: pillar, onChange: (e) => setPillars((list) => list.map((p, i) => i === index ? e.target.value : p)), style: { flex: 1, height: 36, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: "rgba(255,255,255,.72)", padding: "0 11px", outline: "none", color: T.navy, fontSize: 13 } }), /* @__PURE__ */ React.createElement("button", { onClick: () => setPillars((list) => list.filter((_, i) => i !== index)), style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 12 })))), /* @__PURE__ */ React.createElement("button", { onClick: () => setPillars((list) => [...list, "\u65B0\u7684\u56FA\u5B9A\u9009\u9898\u65B9\u5411"]), style: { height: 34, borderRadius: 12, border: `1px dashed ${T.hairline}`, background: "rgba(255,255,255,.58)", color: T.navyMid, cursor: "pointer", fontSize: 12.5, fontWeight: 620 } }, "\u65B0\u589E\u5185\u5BB9\u652F\u67F1"))), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u6211\u7684 IP \u7CFB\u7EDF\u9884\u89C8" }, /* @__PURE__ */ React.createElement("div", { style: { padding: 18, borderRadius: 18, background: "linear-gradient(135deg, rgba(239,239,253,.76), rgba(224,250,244,.66))", border: "1px solid rgba(255,255,255,.72)" } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 20, fontWeight: 780, color: T.navy } }, persona.name), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 6, color: T.navyMid, fontSize: 13 } }, persona.bio), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 12, display: "flex", gap: 7, flexWrap: "wrap" } }, persona.keywords.split(/[、,，]/).filter(Boolean).map((k) => /* @__PURE__ */ React.createElement("span", { key: k, style: { padding: "5px 9px", borderRadius: 999, background: "rgba(255,255,255,.66)", color: T.navyMid, fontSize: 11.5, fontWeight: 650 } }, k))))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(4), style: { height: 40, padding: "0 18px", borderRadius: 13, border: "none", background: T.navy, color: T.white, cursor: "pointer", fontSize: 13, fontWeight: 700, boxShadow: "0 12px 24px rgba(14,14,44,.14)" } }, "\u786E\u8BA4\u753B\u50CF"))), step === 4 && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 4, fontSize: 15, fontWeight: 680 } }, "\u6211\u5148\u6392\u51FA\u672A\u6765\u4E00\u5468\u7684\u5185\u5BB9\u5EFA\u8BAE\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13 } }, "V1 \u5148\u4E0D\u53D1\u5E03\uFF0C\u53EA\u628A\u8BA1\u5212\u548C\u7B2C\u4E00\u7BC7\u5236\u4F5C\u5165\u53E3\u51C6\u5907\u597D\u3002")), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u4E00\u5468\u5185\u5BB9\u89C4\u5212" }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10 } }, calendar.map((item, index) => /* @__PURE__ */ React.createElement("div", { key: `${item.day}-${index}`, style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "64px 86px minmax(0, 1fr) 34px", gap: 8, alignItems: "center", padding: 10, borderRadius: 14, background: index === 0 ? "rgba(239,239,253,.58)" : "rgba(250,252,254,.72)", border: `1px solid ${index === 0 ? "rgba(75,77,237,.14)" : T.hairlineSoft}` } }, /* @__PURE__ */ React.createElement("input", { value: item.day, onChange: (e) => setCalendarItem(index, { day: e.target.value }), style: { border: "none", background: "transparent", color: T.navy, fontSize: 12.5, fontWeight: 720, outline: "none" } }), /* @__PURE__ */ React.createElement("input", { value: item.type, onChange: (e) => setCalendarItem(index, { type: e.target.value }), style: { border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.62)", borderRadius: 10, height: 32, padding: "0 9px", color: T.navyMid, fontSize: 12, outline: "none" } }), /* @__PURE__ */ React.createElement("input", { value: item.topic, onChange: (e) => setCalendarItem(index, { topic: e.target.value }), style: { border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.62)", borderRadius: 10, height: 32, padding: "0 9px", color: T.navy, fontSize: 12.5, outline: "none" } }), /* @__PURE__ */ React.createElement("button", { onClick: () => setCalendar((list) => list.filter((_, i) => i !== index)), style: { ...iconBtnStyle(), width: 32, height: 32 } }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 11 })), /* @__PURE__ */ React.createElement("div", { style: { gridColumn: isMobile ? "auto" : "3 / 4", color: T.navyLight, fontSize: 11.5 } }, "\u53C2\u8003\uFF1A", item.ref))), /* @__PURE__ */ React.createElement("button", { onClick: () => setCalendar((list) => [...list, { day: "\u65B0\u589E", type: "\u56FE\u6587", topic: "\u65B0\u7684\u5185\u5BB9\u9009\u9898", ref: "@\u53C2\u8003\u8D26\u53F7" }]), style: { height: 36, borderRadius: 13, border: `1px dashed ${T.hairline}`, background: "rgba(255,255,255,.58)", color: T.navyMid, cursor: "pointer", fontSize: 12.5, fontWeight: 650 } }, "\u65B0\u589E\u4E00\u5929"))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end" } }, /* @__PURE__ */ React.createElement("button", { onClick: complete, style: { height: 42, padding: "0 20px", borderRadius: 14, border: "none", background: T.navy, color: T.white, cursor: "pointer", fontSize: 13.2, fontWeight: 740, boxShadow: "0 14px 28px rgba(14,14,44,.16)" } }, "\u5F00\u59CB\u5236\u4F5C\u7B2C\u4E00\u7BC7")))), !isMobile && /* @__PURE__ */ React.createElement("div", { style: { position: "sticky", top: 88 } }, memory))));
  };
  window.AccountPlanningPage = AccountPlanningPage;
  var AccountPlanningPagePolished = ({ onBackHome, onNewChat, onOpenAssets, onOpenSkills, onOpenInsights, onComplete }) => {
    const { isCompact, isTablet, isMobile } = useViewport();
    const [navCollapsed, setNavCollapsed] = React.useState(false);
    const [step, setStep] = React.useState(1);
    const [modalType, setModalType] = React.useState(null);
    const [method, setMethod] = React.useState(null);
    const [methods2, setMethods] = React.useState([]);
    const [attachment, setAttachment] = React.useState(null);
    const [attachments, setAttachments] = React.useState([]);
    const [rawInput, setRawInput] = React.useState("");
    const [sentIntro, setSentIntro] = React.useState(false);
    const [goal, setGoal] = React.useState(null);
    const [platform, setPlatform] = React.useState(null);
    const [confirmed, setConfirmed] = React.useState({});
    const [copied, setCopied] = React.useState("");
    const [reportVariant, setReportVariant] = React.useState(0);
    const [reportBurst, setReportBurst] = React.useState(false);
    const [weekStart, setWeekStart] = React.useState("2026-05-18");
    const [showWeekPicker, setShowWeekPicker] = React.useState(false);
    const [diagnosisText, setDiagnosisText] = React.useState({
      position: "\u505A\u9644\u8FD1\u4EBA\u613F\u610F\u6536\u85CF\u7684\u70DF\u706B\u6C14\u5C0F\u9986\u8D26\u53F7\u3002\u4F60\u7684\u4F18\u52BF\u4E0D\u662F\u5927\u54C1\u724C\u611F\uFF0C\u800C\u662F\u7A33\u5B9A\u3001\u771F\u5B9E\u3001\u79BB\u7528\u6237\u5F88\u8FD1\u3002\u5185\u5BB9\u8981\u8BA9\u4EBA\u89C9\u5F97\u4E0B\u73ED\u5C31\u80FD\u53BB\u3002",
      audience: "23-38 \u5C81\u9644\u8FD1\u4E0A\u73ED\u65CF\u3001\u60C5\u4FA3\u548C\u5468\u672B\u7EA6\u996D\u4EBA\u7FA4\uFF0C\u5173\u5FC3\u5473\u9053\u7A33\u5B9A\u3001\u4EF7\u683C\u8212\u670D\u3001\u8DDD\u79BB\u65B9\u4FBF\u3002",
      directions: "\u62DB\u724C\u83DC\u6545\u4E8B\uFF1A\u8BA9\u7528\u6237\u8BB0\u4F4F\u4F60\u548C\u522B\u7684\u5E97\u4E0D\u4E00\u6837\u7684\u5730\u65B9\u3002\n\u771F\u5B9E\u5230\u5E97\u573A\u666F\uFF1A\u964D\u4F4E\u7B2C\u4E00\u6B21\u5230\u5E97\u7684\u5FC3\u7406\u6210\u672C\u3002\n\u672C\u5730\u751F\u6D3B\u653B\u7565\uFF1A\u628A\u9910\u5385\u5185\u5BB9\u53D8\u6210\u53EF\u6536\u85CF\u7684\u4FE1\u606F\u3002",
      benchmarks: "@\u672C\u5730\u5403\u559D\u6307\u5357\uFF1A\u6807\u9898\u6E05\u695A\uFF0C\u9002\u5408\u5B66\u4E60\u9009\u9898\u5305\u88C5\u3002\n@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0\uFF1A\u64C5\u957F\u628A\u5C0F\u5E97\u65E5\u5E38\u62CD\u5F97\u6709\u4EBA\u60C5\u5473\u3002\n@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240\uFF1A\u5348\u9910\u573A\u666F\u5207\u5F97\u7EC6\uFF0C\u5BB9\u6613\u5F15\u6D41\u5230\u5E97\u3002",
      selling: "\u7A33\u5B9A\u5BB6\u5E38\u5473 + \u5E97\u4E3B\u771F\u5B9E\u611F + \u79BB\u9644\u8FD1\u4EBA\u751F\u6D3B\u5F88\u8FD1\u3002"
    });
    const [calendar, setCalendar] = React.useState([
      { day: "\u5468\u4E00", type: "\u63A2\u5E97\u56FE\u6587", topic: "\u7B2C\u4E00\u6B21\u6765\u5E97\u91CC\uFF0C\u5148\u70B9\u8FD9 3 \u9053\u62DB\u724C\u83DC", ref: "@\u672C\u5730\u5403\u559D\u6307\u5357" },
      { day: "\u5468\u4E8C", type: "\u77ED\u89C6\u9891", topic: "\u540E\u53A8\u5907\u83DC 30 \u79D2\uFF0C\u770B\u770B\u4E00\u7897\u996D\u600E\u4E48\u88AB\u8BA4\u771F\u505A\u597D", ref: "@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0" },
      { day: "\u5468\u4E09", type: "\u56FE\u6587", topic: "\u9644\u8FD1\u4E0A\u73ED\u65CF\u5348\u9910\u4E0D\u8E29\u96F7\u83DC\u5355", ref: "@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240" },
      { day: "\u5468\u56DB", type: "\u957F\u6587", topic: "\u4E00\u5BB6\u5C0F\u5E97\u600E\u4E48\u628A\u56DE\u5934\u5BA2\u7559\u4F4F", ref: "@\u4E3B\u7406\u4EBA\u624B\u8BB0" },
      { day: "\u5468\u4E94", type: "\u77ED\u89C6\u9891", topic: "\u987E\u5BA2\u6700\u5E38\u95EE\u7684 5 \u4E2A\u95EE\u9898", ref: "@\u771F\u5B9E\u63A2\u5E97" },
      { day: "\u5468\u516D", type: "\u56FE\u6587", topic: "\u5468\u672B\u5E26\u670B\u53CB\u6765\u5403\uFF0C\u600E\u4E48\u70B9\u66F4\u5212\u7B97", ref: "@\u672C\u5730\u751F\u6D3B\u5BB6" },
      { day: "\u5468\u65E5", type: "\u590D\u76D8", topic: "\u8FD9\u5468\u6700\u53D7\u6B22\u8FCE\u7684\u4E00\u9053\u83DC", ref: "@\u5C0F\u5E97\u7ECF\u8425\u7B14\u8BB0" }
    ]);
    const [reportDraft, setReportDraft] = React.useState(null);
    const steps = [
      { id: 1, label: "\u5165\u53E3\u4FE1\u606F" },
      { id: 2, label: "\u8D26\u53F7\u8BCA\u65AD" },
      { id: 3, label: "IP \u753B\u50CF" },
      { id: 4, label: "\u5185\u5BB9\u65E5\u5386" },
      { id: 5, label: "\u5F00\u59CB\u5236\u4F5C" }
    ];
    const defaultDiagnosis = {
      position: "\u505A\u9644\u8FD1\u4EBA\u613F\u610F\u6536\u85CF\u7684\u70DF\u706B\u6C14\u5C0F\u9986\u8D26\u53F7\u3002\u4F60\u7684\u4F18\u52BF\u4E0D\u662F\u5927\u54C1\u724C\u611F\uFF0C\u800C\u662F\u7A33\u5B9A\u3001\u771F\u5B9E\u3001\u79BB\u7528\u6237\u5F88\u8FD1\u3002\u5185\u5BB9\u8981\u8BA9\u4EBA\u89C9\u5F97\u4E0B\u73ED\u5C31\u80FD\u53BB\u3002",
      audience: "23-38 \u5C81\u9644\u8FD1\u4E0A\u73ED\u65CF\u3001\u60C5\u4FA3\u548C\u5468\u672B\u7EA6\u996D\u4EBA\u7FA4\uFF0C\u5173\u5FC3\u5473\u9053\u7A33\u5B9A\u3001\u4EF7\u683C\u8212\u670D\u3001\u8DDD\u79BB\u65B9\u4FBF\u3002",
      directions: "\u62DB\u724C\u83DC\u6545\u4E8B\uFF1A\u8BA9\u7528\u6237\u8BB0\u4F4F\u4F60\u548C\u522B\u7684\u5E97\u4E0D\u4E00\u6837\u7684\u5730\u65B9\u3002\n\u771F\u5B9E\u5230\u5E97\u573A\u666F\uFF1A\u964D\u4F4E\u7B2C\u4E00\u6B21\u5230\u5E97\u7684\u5FC3\u7406\u6210\u672C\u3002\n\u672C\u5730\u751F\u6D3B\u653B\u7565\uFF1A\u628A\u9910\u5385\u5185\u5BB9\u53D8\u6210\u53EF\u6536\u85CF\u7684\u4FE1\u606F\u3002",
      benchmarks: "@\u672C\u5730\u5403\u559D\u6307\u5357\uFF1A\u6807\u9898\u6E05\u695A\uFF0C\u9002\u5408\u5B66\u4E60\u9009\u9898\u5305\u88C5\u3002\n@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0\uFF1A\u64C5\u957F\u628A\u5C0F\u5E97\u65E5\u5E38\u62CD\u5F97\u6709\u4EBA\u60C5\u5473\u3002\n@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240\uFF1A\u5348\u9910\u573A\u666F\u5207\u5F97\u7EC6\uFF0C\u5BB9\u6613\u5F15\u6D41\u5230\u5E97\u3002",
      selling: "\u7A33\u5B9A\u5BB6\u5E38\u5473 + \u5E97\u4E3B\u771F\u5B9E\u611F + \u79BB\u9644\u8FD1\u4EBA\u751F\u6D3B\u5F88\u8FD1\u3002"
    };
    const reports = [
      {
        names: ["\u5DF7\u53E3\u6696\u80C3\u5C0F\u9986", "\u9644\u8FD1\u4EBA\u7684\u5BB6\u5E38\u996D", "\u4E0B\u73ED\u6765\u5403\u4E00\u53E3"],
        keywords: ["\u4EB2\u5207\u4F46\u4E0D\u6CB9\u817B", "\u61C2\u672C\u5730\u751F\u6D3B", "\u771F\u5B9E\u4E3B\u7406\u4EBA", "\u7A33\u5B9A\u597D\u5403"],
        phrases: ["\u4ECA\u5929\u8FD9\u7897\u996D\uFF0C\u9002\u5408\u4E0B\u73ED\u540E\u6765\u4E00\u53E3\u3002", "\u7B2C\u4E00\u6B21\u6765\u4E0D\u77E5\u9053\u70B9\u4EC0\u4E48\uFF0C\u5148\u770B\u8FD9\u4E00\u7BC7\u3002", "\u4E0D\u662F\u7F51\u7EA2\u5E97\uFF0C\u4F46\u60F3\u628A\u6BCF\u987F\u996D\u8BA4\u771F\u505A\u597D\u3002"],
        bio: "\u6BCF\u5929\u8BA4\u771F\u505A\u4E00\u7897\u6709\u70DF\u706B\u6C14\u7684\u5BB6\u5E38\u996D\uFF0C\u7ED9\u9644\u8FD1\u4EBA\u4E00\u4E2A\u4E0D\u7528\u7EA0\u7ED3\u7684\u5403\u996D\u9009\u62E9\u3002",
        pillars: ["\u62DB\u724C\u83DC\u6545\u4E8B", "\u5348\u9910\u4E0D\u8E29\u96F7", "\u8001\u677F\u7684\u4E00\u5929", "\u771F\u5B9E\u987E\u5BA2\u53CD\u9988", "\u5468\u672B\u670B\u53CB\u5C40\u83DC\u5355"],
        bloggers: ["@\u672C\u5730\u5403\u559D\u6307\u5357", "@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0", "@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240"],
        covers: ["\u6696\u8272\u81EA\u7136\u5149 + \u83DC\u54C1\u8FD1\u666F + \u5927\u7559\u767D\u6807\u9898", "\u5E97\u95E8\u53E3/\u9910\u684C/\u540E\u53A8\u7EC6\u8282\u4E09\u56FE\u62FC\u8D34", "\u4EBA\u7269\u624B\u90E8\u5165\u955C\uFF0C\u5F31\u5316\u6446\u62CD\u611F"]
      },
      {
        names: ["\u4ECA\u5929\u5403\u6696\u80C3\u996D", "\u793E\u533A\u996D\u70B9\u7814\u7A76\u6240", "\u5C0F\u9986\u8BA4\u771F\u996D"],
        keywords: ["\u9760\u8C31\u63A8\u8350", "\u90BB\u91CC\u611F", "\u4EF7\u683C\u53CB\u597D", "\u4E0B\u73ED\u6CBB\u6108"],
        phrases: ["\u8FD9\u4E0D\u662F\u63A2\u5E97\u5E7F\u544A\uFF0C\u662F\u9644\u8FD1\u4EBA\u771F\u7684\u4F1A\u590D\u5403\u7684\u83DC\u5355\u3002", "\u5982\u679C\u4F60\u53EA\u6709 30 \u5206\u949F\u5403\u5348\u996D\uFF0C\u53EF\u4EE5\u8FD9\u4E48\u70B9\u3002", "\u5C0F\u5E97\u6700\u52A8\u4EBA\u7684\u5730\u65B9\uFF0C\u662F\u6BCF\u5929\u90FD\u7A33\u5B9A\u3002"],
        bio: "\u8BB0\u5F55\u4E00\u5BB6\u793E\u533A\u5C0F\u9986\u7684\u65E5\u5E38\u83DC\u5355\u3001\u771F\u5B9E\u5BA2\u4EBA\u548C\u8BA9\u4EBA\u5B89\u5FC3\u7684\u5BB6\u5E38\u5473\u3002",
        pillars: ["30 \u5206\u949F\u5348\u9910\u65B9\u6848", "\u590D\u5403\u83DC\u5355", "\u5C0F\u5E97\u5E55\u540E", "\u672C\u5468\u65B0\u54C1", "\u9644\u8FD1\u751F\u6D3B\u8DEF\u7EBF"],
        bloggers: ["@\u901A\u52E4\u5348\u9910\u5730\u56FE", "@\u5C0F\u5E97\u89C2\u5BDF\u5458", "@\u9644\u8FD1\u751F\u6D3B\u624B\u518C"],
        covers: ["\u6D45\u8272\u684C\u9762 + \u4FEF\u62CD\u5957\u9910 + \u624B\u5199\u611F\u6807\u9898", "\u8001\u677F\u51FA\u955C + \u83DC\u54C1\u7279\u5199 + \u771F\u5B9E\u73AF\u5883", "\u4F4E\u9971\u548C\u6696\u8272\uFF0C\u5F3A\u8C03\u5E72\u51C0\u548C\u53EF\u4FE1"]
      }
    ];
    const report = reports[reportVariant % reports.length];
    React.useEffect(() => {
      const next = reports[reportVariant % reports.length];
      setReportDraft({
        names: [...next.names],
        keywords: [...next.keywords],
        phrases: [...next.phrases],
        bio: next.bio,
        pillars: [...next.pillars],
        bloggers: [...next.bloggers],
        covers: [...next.covers]
      });
    }, [reportVariant]);
    const activeReport = reportDraft || report;
    React.useEffect(() => {
      if (step !== 3) return void 0;
      setReportBurst(false);
      const raf = window.requestAnimationFrame(() => setReportBurst(true));
      const timer = window.setTimeout(() => setReportBurst(false), 1500);
      return () => {
        window.cancelAnimationFrame(raf);
        window.clearTimeout(timer);
      };
    }, [step, reportVariant]);
    const canAdvanceStep1 = sentIntro && goal && platform;
    const firstTopic = calendar[0]?.topic || "\u7B2C\u4E00\u6B21\u6765\u5E97\u91CC\uFF0C\u5148\u70B9\u8FD9 3 \u9053\u62DB\u724C\u83DC";
    const copyText = (text) => {
      setCopied(text);
      navigator.clipboard?.writeText(text).catch(() => {
      });
      window.setTimeout(() => setCopied(""), 1100);
    };
    const confirmAttachment = (att) => {
      setAttachment(att);
      setAttachments((list) => [...list, att]);
      setMethod(att.type);
      setMethods((list) => list.includes(att.type) ? list : [...list, att.type]);
      setModalType(null);
    };
    const sendIntro = () => {
      if (!attachments.length && !rawInput.trim()) return;
      setSentIntro(true);
    };
    const complete = () => onComplete({
      topic: `\u5C0F\u7EA2\u4E66\u56FE\u6587\uFF1A${firstTopic}`,
      platform: platform || "\u5C0F\u7EA2\u4E66",
      positioning: "\u505A\u9644\u8FD1\u4EBA\u613F\u610F\u6536\u85CF\u7684\u70DF\u706B\u6C14\u5C0F\u9986\u8D26\u53F7",
      persona: {
        name: activeReport.names[0],
        bio: activeReport.bio,
        keywords: activeReport.keywords.join("\u3001"),
        tone: activeReport.phrases.join(" / "),
        cover: activeReport.covers[0]
      },
      pillars: activeReport.pillars
    });
    const memory = /* @__PURE__ */ React.createElement("section", { style: {
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.84)",
      borderRadius: 22,
      padding: 16,
      boxShadow: "0 16px 38px rgba(14,14,44,.052), inset 0 1px 0 rgba(255,255,255,.86)"
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 } }, /* @__PURE__ */ React.createElement("h3", { style: { margin: 0, fontSize: 14.5, fontWeight: 760, color: T.navy } }, "IP Memory"), /* @__PURE__ */ React.createElement("span", { style: { fontSize: 10.5, color: T.navyLight, fontFamily: T.fontMono } }, Math.min(5, [sentIntro, goal, platform, method, step >= 2].filter(Boolean).length), "/5")), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 9 } }, [
      ["\u8D5B\u9053", "\u672C\u5730\u751F\u6D3B / \u5C0F\u9910\u996E", sentIntro],
      ["\u76EE\u6807", goal || "\u5F85\u9009\u62E9", !!goal],
      ["\u5E73\u53F0", platform || "\u5F85\u9009\u62E9", !!platform],
      ["\u4EA7\u54C1", method ? "\u5BB6\u5E38\u83DC\u3001\u5348\u9910\u3001\u9644\u8FD1\u5230\u5E97" : "\u5F85\u8BC6\u522B", !!method],
      ["\u5B9A\u4F4D", step >= 2 ? "\u70DF\u706B\u6C14\u5C0F\u9986\u8D26\u53F7" : "\u5F85\u8BCA\u65AD", step >= 2]
    ].map(([k, v, done]) => /* @__PURE__ */ React.createElement("div", { key: k, style: { padding: "10px 10px", borderRadius: 13, background: done ? "rgba(224,250,244,.62)" : "rgba(246,248,251,.72)", border: `1px solid ${done ? "rgba(49,208,170,.20)" : T.hairlineSoft}`, animation: done ? `memoryReady .48s ${T.spring} both` : "none" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "space-between", gap: 8, marginBottom: 4 } }, /* @__PURE__ */ React.createElement("span", { style: { color: done ? T.success : T.navyLight, fontSize: 11.5, fontWeight: 720 } }, k), /* @__PURE__ */ React.createElement("span", { style: { width: 18, height: 18, borderRadius: "50%", background: done ? T.success : "rgba(14,14,44,.06)", color: T.white, display: "inline-flex", alignItems: "center", justifyContent: "center" } }, done && /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 10, stroke: 2.4 }))), /* @__PURE__ */ React.createElement("div", { style: { color: done ? T.navy : T.navyLight, fontSize: 12.2, fontWeight: done ? 650 : 520, lineHeight: 1.45 } }, v)))));
    return /* @__PURE__ */ React.createElement("div", { style: { display: "flex", height: "100%", width: "100%", background: "linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)", overflow: "hidden" } }, !isTablet && /* @__PURE__ */ React.createElement(
      Sidebar,
      {
        active: "home",
        onNew: onNewChat,
        onNavigate: (id) => {
          if (id === "home") onBackHome();
          if (id === "library") onOpenAssets && onOpenAssets();
          if (id === "skills") onOpenSkills && onOpenSkills();
          if (id === "insights") onOpenInsights && onOpenInsights();
        },
        sessions: ["\u8D26\u53F7\u89C4\u5212 \xB7 \u5F53\u524D", "\u4E0A\u6D77\u5496\u5561\u9986 City Walk Top 10", "\u4EA7\u54C1\u6D4B\u8BC4 \xB7 AI \u89C6\u9891\u5DE5\u5177\u6A2A\u8BC4"],
        collapsed: navCollapsed,
        onToggle: () => setNavCollapsed((v) => !v)
      }
    ), /* @__PURE__ */ React.createElement("main", { style: { flex: 1, overflow: "auto", position: "relative", background: "linear-gradient(180deg, #FFFFFF 0%, #FBFCFE 54%, #F7F9FC 100%)" } }, /* @__PURE__ */ React.createElement("div", { style: { position: "sticky", top: 0, zIndex: 8, minHeight: isMobile ? "auto" : 66, padding: isMobile ? "12px 16px" : "0 24px", display: "flex", alignItems: isMobile ? "stretch" : "center", justifyContent: "space-between", gap: 14, borderBottom: `1px solid ${T.hairlineSoft}`, background: "rgba(250,252,254,.84)", backdropFilter: "blur(18px) saturate(1.16)", flexDirection: isMobile ? "column" : "row" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 12, minWidth: 0 } }, /* @__PURE__ */ React.createElement("button", { onClick: onBackHome, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "home", size: 15, color: T.navyMid })), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13.5, fontWeight: 720, color: T.navy } }, "\u8D26\u53F7\u89C4\u5212"), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11, color: T.navyLight } }, "\u7528\u6700\u5C11\u7684\u4FE1\u606F\uFF0C\u5EFA\u7ACB\u53EF\u6267\u884C\u7684\u8D26\u53F7\u7CFB\u7EDF"))), /* @__PURE__ */ React.createElement(PlanningStepper, { steps, step, isMobile })), /* @__PURE__ */ React.createElement("div", { style: { maxWidth: isMobile ? "100%" : 1160, margin: "0 auto", padding: isMobile ? "22px 18px 42px" : "34px 42px 58px", display: "grid", gridTemplateColumns: isMobile ? "1fr" : isCompact ? "minmax(0, 1fr) 260px" : "minmax(0, 1fr) 292px", gap: isMobile ? 18 : 24, alignItems: "start" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 18, minWidth: 0 } }, isMobile && memory, step === 1 && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 8, fontSize: 15, fontWeight: 680 } }, "\u5148\u7ED9\u6211\u4E00\u70B9\u7EBF\u7D22\u5C31\u884C\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13 } }, "\u53EF\u4EE5\u8D34\u94FE\u63A5\u3001\u4F20\u622A\u56FE\uFF0C\u6216\u8005\u76F4\u63A5\u8BF4\u4F60\u662F\u505A\u4EC0\u4E48\u7684\u3002\u6211\u4F1A\u628A\u540E\u9762\u7684\u95EE\u9898\u538B\u5230 3 \u8F6E\u4EE5\u5185\u3002")), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u9009\u62E9\u8F93\u5165\u65B9\u5F0F" }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "repeat(3, minmax(0, 1fr))", gap: 10, marginBottom: 12 } }, /* @__PURE__ */ React.createElement(PlanningOption, { icon: "link", title: "\u7C98\u8D34\u94FE\u63A5", desc: "\u5E97\u94FA / \u8D26\u53F7 / \u6587\u7AE0", active: methods2.includes("link"), onClick: () => setModalType("link") }), /* @__PURE__ */ React.createElement(PlanningOption, { icon: "image", title: "\u4E0A\u4F20\u56FE\u7247", desc: "\u4EA7\u54C1\u56FE / \u622A\u56FE", active: methods2.includes("image"), onClick: () => setModalType("image") }), /* @__PURE__ */ React.createElement(PlanningOption, { icon: "chat", title: "\u76F4\u63A5\u63CF\u8FF0", desc: "\u6211\u662F\u505A\u4EC0\u4E48\u7684", active: methods2.includes("text"), onClick: () => setModalType("text") })), /* @__PURE__ */ React.createElement(
      PlanningComposerMulti,
      {
        attachments,
        text: rawInput,
        setText: setRawInput,
        onRemoveAttachment: (index) => {
          setAttachments((list) => {
            const next = list.filter((_, i) => i !== index);
            setMethods([...new Set(next.map((item) => item.type))]);
            setMethod(next[next.length - 1]?.type || null);
            setAttachment(next[next.length - 1] || null);
            return next;
          });
        },
        onSend: sendIntro
      }
    )), sentIntro && /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 12 } }, "\u6536\u5230\uFF01\u6211\u770B\u5230\u4F60\u662F\u505A\u672C\u5730\u5C0F\u9910\u996E\u7684\uFF0C\u4E3B\u6253\u5BB6\u5E38\u83DC\u548C\u9644\u8FD1\u5230\u5E97\u3002\u4F60\u60F3\u901A\u8FC7\u793E\u5A92\u4E3B\u8981\u505A\u4EC0\u4E48\uFF1F"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, flexWrap: "wrap" } }, ["\u5F15\u6D41\u5230\u5E97", "\u54C1\u724C\u66DD\u5149", "\u7EBF\u4E0A\u5356\u8D27"].map((v) => /* @__PURE__ */ React.createElement(PlanningChoice, { key: v, active: goal === v, onClick: () => setGoal(v) }, v)))), goal && /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 12 } }, "\u660E\u767D\u3002\u4F60\u5E0C\u671B\u5148\u5728\u54EA\u4E2A\u5E73\u53F0\u505A\uFF1F"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, flexWrap: "wrap" } }, ["\u5C0F\u7EA2\u4E66", "\u6296\u97F3", "\u90FD\u60F3\u8BD5\u8BD5"].map((v) => /* @__PURE__ */ React.createElement(PlanningChoice, { key: v, active: platform === v, onClick: () => setPlatform(v) }, v)))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(2), disabled: !canAdvanceStep1, style: { height: 40, padding: "0 18px", borderRadius: 13, border: "none", background: canAdvanceStep1 ? T.navy : T.surface, color: canAdvanceStep1 ? T.white : T.navyLight, cursor: canAdvanceStep1 ? "pointer" : "not-allowed", fontSize: 13, fontWeight: 700, boxShadow: canAdvanceStep1 ? "0 12px 24px rgba(14,14,44,.14)" : "none" } }, "\u8FDB\u5165\u8D26\u53F7\u8BCA\u65AD"))), step === 2 && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 4, fontSize: 15, fontWeight: 680 } }, "\u6211\u5148\u628A\u8D26\u53F7\u5B9A\u4F4D\u62C6\u51FA\u6765\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13 } }, "\u6BCF\u4E2A\u677F\u5757\u90FD\u53EF\u4EE5\u76F4\u63A5\u7F16\u8F91\uFF0C\u6539\u5B8C\u4F1A\u81EA\u52A8\u4FDD\u7559\u5728\u8FD9\u4EFD\u8D26\u53F7\u89C4\u5212\u91CC\u3002")), /* @__PURE__ */ React.createElement(InlineEditableCard, { title: "\u63A8\u8350\u8D26\u53F7\u5B9A\u4F4D", rows: 4, value: diagnosisText.position, onChange: (v) => setDiagnosisText((d) => ({ ...d, position: v })) }), /* @__PURE__ */ React.createElement(InlineEditableCard, { title: "\u76EE\u6807\u53D7\u4F17\u753B\u50CF", rows: 3, value: diagnosisText.audience, onChange: (v) => setDiagnosisText((d) => ({ ...d, audience: v })) }), /* @__PURE__ */ React.createElement(InlineEditableCard, { title: "\u5185\u5BB9\u65B9\u5411\u5EFA\u8BAE", rows: 5, value: diagnosisText.directions, onChange: (v) => setDiagnosisText((d) => ({ ...d, directions: v })) }), /* @__PURE__ */ React.createElement(InlineEditableCard, { title: "\u5BF9\u6807\u8D26\u53F7\u63A8\u8350", rows: 5, value: diagnosisText.benchmarks, onChange: (v) => setDiagnosisText((d) => ({ ...d, benchmarks: v })) }), /* @__PURE__ */ React.createElement(InlineEditableCard, { title: "\u5DEE\u5F02\u5316\u5356\u70B9", rows: 3, value: diagnosisText.selling, onChange: (v) => setDiagnosisText((d) => ({ ...d, selling: v })) }), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(4), style: { border: "none", background: "transparent", color: T.navyLight, cursor: "pointer", fontSize: 12.5, fontWeight: 600 } }, "\u8DF3\u8FC7\uFF0C\u76F4\u63A5\u751F\u6210"), /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(3), style: { height: 40, padding: "0 18px", borderRadius: 13, border: "none", background: T.navy, color: T.white, cursor: "pointer", fontSize: 13, fontWeight: 700, boxShadow: "0 12px 24px rgba(14,14,44,.14)" } }, "\u770B\u8D77\u6765\u4E0D\u9519\uFF0C\u7EE7\u7EED"))), step === 3 && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 4, fontSize: 15, fontWeight: 680 } }, "\u6211\u628A\u5B9A\u4F4D\u6574\u7406\u6210\u4E00\u4EFD\u53EF\u6267\u884C\u7684 IP \u753B\u50CF\u62A5\u544A\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13 } }, "\u540E\u9762\u505A\u5185\u5BB9\u65F6\uFF0C\u8FD9\u4E9B\u4F1A\u6210\u4E3A Nori \u9ED8\u8BA4\u8BB0\u4F4F\u7684\u8D26\u53F7\u89C4\u5219\u3002")), /* @__PURE__ */ React.createElement("section", { style: { position: "relative", borderRadius: 24, border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.88)", boxShadow: "0 18px 42px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.88)", padding: isMobile ? 18 : 22, overflow: "hidden" } }, /* @__PURE__ */ React.createElement(MiniOnionBurst, { active: reportBurst }), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 14, marginBottom: 18 } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 11.5, color: T.navyLight, fontWeight: 720, letterSpacing: "0.08em", textTransform: "uppercase", marginBottom: 6 } }, "IP System Report"), /* @__PURE__ */ React.createElement("h2", { style: { margin: 0, color: T.navy, fontSize: isMobile ? 22 : 28, lineHeight: 1.16, fontWeight: 780 } }, "\u6211\u7684 IP \u7CFB\u7EDF")), /* @__PURE__ */ React.createElement("span", { style: { height: 30, padding: "0 10px", borderRadius: 999, background: T.successTint, color: T.success, fontSize: 11.5, fontWeight: 720, display: "inline-flex", alignItems: "center", gap: 5 } }, /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 12 }), " \u5DF2\u751F\u6210")), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "1fr 1fr", gap: 14 } }, /* @__PURE__ */ React.createElement(EditableListPanel, { title: "\u8D26\u53F7\u540D\u5EFA\u8BAE", items: activeReport.names, onChange: (items) => setReportDraft((r) => ({ ...activeReport, ...r, names: items })) }), /* @__PURE__ */ React.createElement(EditableListPanel, { title: "\u4EBA\u8BBE\u5173\u952E\u8BCD", items: activeReport.keywords, onChange: (items) => setReportDraft((r) => ({ ...activeReport, ...r, keywords: items })) }), /* @__PURE__ */ React.createElement(EditableListPanel, { title: "\u5E38\u7528\u53E5\u5F0F", items: activeReport.phrases, onChange: (items) => setReportDraft((r) => ({ ...activeReport, ...r, phrases: items })), muted: true }), /* @__PURE__ */ React.createElement(EditableListPanel, { title: "\u8D26\u53F7\u4E3B\u8981\u5185\u5BB9\u652F\u67F1", items: activeReport.pillars, onChange: (items) => setReportDraft((r) => ({ ...activeReport, ...r, pillars: items })) }), /* @__PURE__ */ React.createElement(EditableListPanel, { title: "\u5BF9\u6807\u535A\u4E3B", items: activeReport.bloggers, onChange: (items) => setReportDraft((r) => ({ ...activeReport, ...r, bloggers: items })) }), /* @__PURE__ */ React.createElement(EditableListPanel, { title: "\u63A8\u8350\u5C01\u9762\u56FE\u7247", items: activeReport.covers, onChange: (items) => setReportDraft((r) => ({ ...activeReport, ...r, covers: items })), muted: true }), /* @__PURE__ */ React.createElement("div", { style: { gridColumn: isMobile ? "auto" : "span 2" } }, /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u7B7E\u540D" }, /* @__PURE__ */ React.createElement(
      "textarea",
      {
        value: activeReport.bio,
        onChange: (e) => setReportDraft((r) => ({ ...activeReport, ...r, bio: e.target.value })),
        rows: 3,
        style: {
          width: "100%",
          border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 12,
          background: "rgba(250,252,254,.72)",
          color: T.navyMid,
          padding: 10,
          outline: "none",
          resize: "vertical",
          fontSize: 12.8,
          lineHeight: 1.55,
          fontFamily: T.fontSans
        }
      }
    )))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 14 } }, [
      ["heart", "\u559C\u6B22"],
      ["download", "\u4E0B\u8F7D"],
      ["copy", copied === "ip-system" ? "\u5DF2\u590D\u5236" : "\u590D\u5236"]
    ].map(([icon, label]) => /* @__PURE__ */ React.createElement(
      "button",
      {
        key: icon,
        title: label,
        "aria-label": label,
        onClick: () => {
          if (icon === "copy") {
            copyText([...activeReport.names, activeReport.bio, ...activeReport.keywords, ...activeReport.phrases, ...activeReport.pillars, ...activeReport.bloggers, ...activeReport.covers].join("\n"));
            setCopied("ip-system");
          }
        },
        style: {
          width: 34,
          height: 34,
          borderRadius: 12,
          border: `1px solid ${T.hairlineSoft}`,
          background: "rgba(255,255,255,.78)",
          color: T.navyMid,
          cursor: "pointer",
          display: "inline-flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 6,
          fontSize: 12,
          fontWeight: 650
        }
      },
      /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 13 })
    )))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end", gap: 10, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setReportVariant((v) => v + 1), style: { height: 40, padding: "0 15px", borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.78)", color: T.navyMid, cursor: "pointer", fontSize: 13, fontWeight: 700, display: "inline-flex", alignItems: "center", gap: 6 } }, /* @__PURE__ */ React.createElement(Icon, { name: "refresh", size: 13 }), " \u91CD\u65B0\u751F\u6210"), /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(4), style: { height: 40, padding: "0 18px", borderRadius: 13, border: "none", background: T.navy, color: T.white, cursor: "pointer", fontSize: 13, fontWeight: 700, boxShadow: "0 12px 24px rgba(14,14,44,.14)" } }, "\u786E\u8BA4"))), step === 4 && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 4, fontSize: 15, fontWeight: 680 } }, "\u6211\u5148\u6392\u51FA\u672A\u6765\u4E00\u5468\u7684\u5185\u5BB9\u5EFA\u8BAE\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13 } }, "V1 \u5148\u4E0D\u53D1\u5E03\uFF0C\u53EA\u628A\u8BA1\u5212\u548C\u7B2C\u4E00\u7BC7\u5236\u4F5C\u5165\u53E3\u51C6\u5907\u597D\u3002")), /* @__PURE__ */ React.createElement(
      PlanningPanel,
      {
        title: "\u4E00\u5468\u5185\u5BB9\u89C4\u5212",
        action: /* @__PURE__ */ React.createElement("div", { style: { position: "relative" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setShowWeekPicker((v) => !v), style: { height: 32, padding: "0 11px", borderRadius: 12, border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.78)", color: T.navyMid, cursor: "pointer", display: "inline-flex", alignItems: "center", gap: 6, fontSize: 12, fontWeight: 650 } }, /* @__PURE__ */ React.createElement(Icon, { name: "calendar", size: 13 }), "\u9009\u62E9\u5468"), showWeekPicker && /* @__PURE__ */ React.createElement(
          "input",
          {
            type: "date",
            value: weekStart,
            onChange: (e) => {
              setWeekStart(e.target.value);
              setShowWeekPicker(false);
            },
            style: {
              position: "absolute",
              right: 0,
              top: 38,
              zIndex: 10,
              height: 36,
              border: `1px solid ${T.hairlineSoft}`,
              borderRadius: 12,
              background: T.white,
              padding: "0 9px",
              color: T.navyMid,
              boxShadow: T.shadowMd,
              fontFamily: T.fontSans
            }
          }
        ))
      },
      /* @__PURE__ */ React.createElement("div", { style: { margin: "-2px 0 12px", color: T.navyLight, fontSize: 12.2 } }, "\u89C4\u5212\u5468\u8D77\u59CB\u65E5\uFF1A", weekStart),
      /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10 } }, calendar.map((item, index) => /* @__PURE__ */ React.createElement("div", { key: `${item.day}-${index}`, style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "64px 86px minmax(0, 1fr) 34px", gap: 8, alignItems: "center", padding: 10, borderRadius: 14, background: index === 0 ? "rgba(239,239,253,.58)" : "rgba(250,252,254,.72)", border: `1px solid ${index === 0 ? "rgba(75,77,237,.14)" : T.hairlineSoft}` } }, /* @__PURE__ */ React.createElement("input", { value: item.day, onChange: (e) => setCalendar((list) => list.map((row, i) => i === index ? { ...row, day: e.target.value } : row)), style: { border: "none", background: "transparent", color: T.navy, fontSize: 12.5, fontWeight: 720, outline: "none" } }), /* @__PURE__ */ React.createElement("input", { value: item.type, onChange: (e) => setCalendar((list) => list.map((row, i) => i === index ? { ...row, type: e.target.value } : row)), style: { border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.62)", borderRadius: 10, height: 32, padding: "0 9px", color: T.navyMid, fontSize: 12, outline: "none" } }), /* @__PURE__ */ React.createElement("textarea", { value: item.topic, rows: isMobile ? 2 : 1, onChange: (e) => setCalendar((list) => list.map((row, i) => i === index ? { ...row, topic: e.target.value } : row)), style: { border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.62)", borderRadius: 10, minHeight: 32, padding: "7px 9px", color: T.navy, fontSize: 12.5, outline: "none", resize: "vertical", fontFamily: T.fontSans, lineHeight: 1.45 } }), /* @__PURE__ */ React.createElement("button", { onClick: () => setCalendar((list) => list.filter((_, i) => i !== index)), style: { ...iconBtnStyle(), width: 32, height: 32 } }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 11 })), /* @__PURE__ */ React.createElement(
        "input",
        {
          value: item.ref,
          onChange: (e) => setCalendar((list) => list.map((row, i) => i === index ? { ...row, ref: e.target.value } : row)),
          "aria-label": "\u53C2\u8003\u8D26\u53F7",
          style: {
            gridColumn: isMobile ? "auto" : "3 / 4",
            border: "none",
            background: "transparent",
            color: T.navyLight,
            fontSize: 11.5,
            outline: "none",
            fontFamily: T.fontSans
          }
        }
      ))), /* @__PURE__ */ React.createElement("button", { onClick: () => setCalendar((list) => [...list, { day: "\u65B0\u589E", type: "\u56FE\u6587", topic: "\u65B0\u7684\u5185\u5BB9\u9009\u9898", ref: "@\u53C2\u8003\u8D26\u53F7" }]), style: { height: 36, borderRadius: 13, border: `1px dashed ${T.hairline}`, background: "rgba(255,255,255,.58)", color: T.navyMid, cursor: "pointer", fontSize: 12.5, fontWeight: 650 } }, "\u65B0\u589E\u4E00\u5929"))
    ), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end" } }, /* @__PURE__ */ React.createElement("button", { onClick: complete, style: { height: 42, padding: "0 20px", borderRadius: 14, border: "none", background: T.navy, color: T.white, cursor: "pointer", fontSize: 13.2, fontWeight: 740, boxShadow: "0 14px 28px rgba(14,14,44,.16)" } }, "\u5F00\u59CB\u5236\u4F5C\u7B2C\u4E00\u7BC7")))), !isMobile && /* @__PURE__ */ React.createElement("div", { style: { position: "sticky", top: 92 } }, memory))), modalType && /* @__PURE__ */ React.createElement(InputMethodModal, { type: modalType, onClose: () => setModalType(null), onConfirm: confirmAttachment }));
  };
  window.AccountPlanningPagePolished = AccountPlanningPagePolished;
  var PLAN_STORAGE_KEY = "nori-account-plan-draft-v2";
  var buildPlanExportText = (state) => {
    const planPersona = state.persona || {};
    const personaName = planPersona.name || planPersona.names?.[0] || "\u5DF7\u53E3\u6696\u80C3\u5C0F\u9986";
    const personaKeywords = Array.isArray(planPersona.keywords) ? planPersona.keywords.join("\u3001") : planPersona.keywords;
    const personaTone = Array.isArray(planPersona.phrases) ? planPersona.phrases.join(" / ") : planPersona.tone;
    const personaCover = Array.isArray(planPersona.covers) ? planPersona.covers[0] : planPersona.cover;
    const lines = [
      "\u300A\u8D26\u53F7\u5B9A\u4F4D + \u8FD0\u8425\u8BA1\u5212 + \u5185\u5BB9\u6392\u671F\u300B",
      "",
      `\u8D26\u53F7\u5B9A\u4F4D\uFF1A${state.diagnosisText.position}`,
      `\u76EE\u6807\u53D7\u4F17\uFF1A${state.diagnosisText.audience}`,
      `\u5185\u5BB9\u65B9\u5411\uFF1A${state.diagnosisText.directions.replace(/\n/g, " / ")}`,
      `\u5BF9\u6807\u8D26\u53F7\uFF1A${state.diagnosisText.benchmarks.replace(/\n/g, " / ")}`,
      `\u5DEE\u5F02\u5316\u5356\u70B9\uFF1A${state.diagnosisText.selling}`,
      "",
      `\u4EBA\u8BBE\uFF1A${personaName}`,
      `\u7B7E\u540D\uFF1A${planPersona.bio}`,
      `\u5173\u952E\u8BCD\uFF1A${personaKeywords}`,
      `\u8BED\u6C14\uFF1A${personaTone}`,
      `\u5C01\u9762\uFF1A${personaCover}`,
      "",
      `\u9009\u9898\u5E93\uFF1A${state.pillars.join(" / ")}`,
      `\u53D1\u5E03\u8282\u594F\uFF1A${state.calendar.map((item) => `${item.day} ${item.type} ${item.topic}`).join(" | ")}`,
      `\u6570\u636E\u76EE\u6807\uFF1A7 \u5929\u5185\u9A8C\u8BC1 1 \u5957\u7A33\u5B9A\u9009\u9898\u7ED3\u6784\uFF0C\u6536\u85CF\u7387 / \u5B8C\u8BFB\u7387 / \u70B9\u51FB\u7387\u4FDD\u6301\u53EF\u6301\u7EED\u63D0\u5347`
    ];
    return lines.join("\n");
  };
  var PlanningChatDivider = ({ label }) => /* @__PURE__ */ React.createElement("div", { style: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    margin: "4px 0",
    color: T.navyLight,
    fontSize: 11.5,
    fontWeight: 650
  } }, /* @__PURE__ */ React.createElement("span", { style: { height: 1, flex: 1, background: T.hairlineSoft } }), /* @__PURE__ */ React.createElement("span", null, label), /* @__PURE__ */ React.createElement("span", { style: { height: 1, flex: 1, background: T.hairlineSoft } }));
  var PlanningUserSummary = ({ children }) => /* @__PURE__ */ React.createElement(Bubble, { from: "user", style: { margin: "2px 0" } }, /* @__PURE__ */ React.createElement("div", { style: { whiteSpace: "pre-wrap" } }, children));
  var PlanningPlainReply = ({ children, style }) => /* @__PURE__ */ React.createElement(AgentReply, { style }, children);
  var PlanningStartPanel = ({ quickLink, setQuickLink, onUploadImage, onUploadDoc, onPasteLink }) => /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10 } }, /* @__PURE__ */ React.createElement("div", { style: {
    minWidth: 0,
    height: 46,
    borderRadius: 16,
    border: `1px solid ${T.hairlineSoft}`,
    background: "rgba(250,252,254,.76)",
    display: "flex",
    alignItems: "center",
    padding: "0 14px",
    boxShadow: "inset 0 1px 0 rgba(255,255,255,.84)"
  } }, /* @__PURE__ */ React.createElement(Icon, { name: "link", size: 14, color: T.navyLight }), /* @__PURE__ */ React.createElement(
    "input",
    {
      value: quickLink,
      onChange: (e) => setQuickLink(e.target.value),
      placeholder: "\u7C98\u8D34\u7F8E\u56E2 / \u5927\u4F17\u70B9\u8BC4 / \u5C0F\u7EA2\u4E66\u5E97\u94FA\u94FE\u63A5",
      style: {
        flex: 1,
        minWidth: 0,
        border: "none",
        outline: "none",
        background: "transparent",
        color: T.navy,
        fontSize: 13.5,
        lineHeight: 1.5,
        marginLeft: 10,
        fontFamily: T.fontSans
      }
    }
  )), /* @__PURE__ */ React.createElement("div", { style: {
    display: "grid",
    gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
    gap: 10
  } }, /* @__PURE__ */ React.createElement("button", { onClick: onUploadImage, style: { ...pillButtonStyle(false), height: 38, borderRadius: 13, justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "upload", size: 14 }), "\u4E0A\u4F20\u56FE\u7247"), /* @__PURE__ */ React.createElement("button", { onClick: onUploadDoc, style: { ...pillButtonStyle(false), height: 38, borderRadius: 13, justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "document", size: 14 }), "\u4E0A\u4F20\u6587\u6863"), /* @__PURE__ */ React.createElement("button", { onClick: onPasteLink, style: { ...pillButtonStyle(false), height: 38, borderRadius: 13, justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "link", size: 14 }), "\u7C98\u8D34\u94FE\u63A5")));
  var PlanningUploadedAssetStrip = ({ attachments, onAddMore, onConfirm }) => {
    const [open, setOpen] = React.useState(false);
    const fallback = [
      { type: "link", label: "\u7F8E\u56E2\u5E97\u94FA\u94FE\u63A5", value: "\u4E0A\u6D77\u6696\u80C3\u5C0F\u9986 \xB7 \u5E97\u94FA\u4E3B\u9875", thumb: PLANNING_ASSET_THUMBS[2] },
      { type: "image", label: "\u83DC\u5355\u4E0E\u73AF\u5883\u56FE\u7247", value: "4 \u5F20", thumb: PLANNING_ASSET_THUMBS[0] },
      { type: "file", label: "\u7528\u6237\u8BC4\u4EF7\u6458\u8981", value: "32 \u6761\u8BC4\u8BBA", thumb: PLANNING_ASSET_THUMBS[3] }
    ];
    const assets = (attachments.length ? attachments : fallback).map((item, index) => ({
      ...item,
      thumb: item.thumb || (item.preview && item.type === "image" ? item.preview : PLANNING_ASSET_THUMBS[index % PLANNING_ASSET_THUMBS.length])
    }));
    const shown = open ? assets : assets.slice(0, 4);
    const iconFor = (type) => type === "link" ? "link" : type === "image" ? "image" : type === "video" ? "video" : "file";
    return /* @__PURE__ */ React.createElement(
      AgentCardShell,
      {
        label: "Agent \u8D44\u4EA7\u8BC6\u522B",
        icon: "folder",
        title: "\u5DF2\u8BFB\u5230\u7684\u8D44\u6599",
        action: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("button", { onClick: onAddMore, style: { ...pillButtonStyle(false), height: 34, borderRadius: 12, fontSize: 12.4 } }, /* @__PURE__ */ React.createElement(Icon, { name: "plus", size: 13 }), "\u6DFB\u52A0\u66F4\u591A"), onConfirm && /* @__PURE__ */ React.createElement("button", { onClick: onConfirm, style: { ...planningActionButtonStyle("primary"), height: 34, borderRadius: 12, fontSize: 12.4 } }, "\u786E\u8BA4\uFF0C\u4E0B\u4E00\u6B65", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 13 }))),
        style: { padding: 13 },
        bodyStyle: { fontSize: 12.6 }
      },
      /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(112px, 1fr))", gap: 8 } }, shown.map((item, index) => /* @__PURE__ */ React.createElement("div", { key: `${item.type}-${index}`, style: {
        minWidth: 0,
        borderRadius: 14,
        border: `1px solid ${T.hairlineSoft}`,
        background: "rgba(250,252,254,.76)",
        padding: 7,
        display: "grid",
        gridTemplateColumns: "34px minmax(0, 1fr)",
        gap: 8,
        alignItems: "center"
      } }, /* @__PURE__ */ React.createElement("span", { style: { width: 34, height: 34, borderRadius: 10, overflow: "hidden", background: T.surface, color: T.navyLight, display: "inline-flex", alignItems: "center", justifyContent: "center", position: "relative" } }, item.thumb ? /* @__PURE__ */ React.createElement("img", { src: item.thumb, alt: "", style: { width: "100%", height: "100%", objectFit: "cover", display: "block" } }) : /* @__PURE__ */ React.createElement(Icon, { name: iconFor(item.type), size: 14 })), /* @__PURE__ */ React.createElement("span", { style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("span", { style: { display: "block", color: T.navy, fontSize: 11.8, lineHeight: 1.35, fontWeight: 680, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, item.label || item.value || item.type), /* @__PURE__ */ React.createElement("span", { style: { display: "block", marginTop: 2, color: T.navyLight, fontSize: 10.8, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, item.value || (item.type === "image" ? "\u56FE\u7247\u7D20\u6750" : item.type === "link" ? "\u94FE\u63A5\u7EBF\u7D22" : "\u6587\u6863\u8D44\u6599")))))), assets.length > 4 && /* @__PURE__ */ React.createElement("button", { onClick: () => setOpen((v) => !v), style: { border: "none", background: "transparent", color: T.navyLight, cursor: "pointer", justifySelf: "start", fontSize: 12, fontWeight: 650, padding: 0 } }, open ? "\u6536\u8D77\u8D44\u6599" : `\u5C55\u5F00\u5168\u90E8 ${assets.length} \u4E2A\u8D44\u6599`))
    );
  };
  var PlanningResearchFlow = ({ bullets, conclusion, isMobile, onComplete, showThinking = true }) => {
    React.useEffect(() => {
      const timers = [window.setTimeout(() => onComplete?.(), 1200)];
      return () => timers.forEach(window.clearTimeout);
    }, [bullets, onComplete]);
    return null;
  };
  var PlanningBenchmarkList = ({ accounts }) => /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, accounts.map((item, index) => /* @__PURE__ */ React.createElement("div", { key: `${item.name}-${index}`, style: {
    display: "grid",
    gridTemplateColumns: "40px minmax(0, 1fr) auto",
    gap: 10,
    alignItems: "center",
    borderRadius: 16,
    padding: 10,
    border: `1px solid ${T.hairlineSoft}`,
    background: "rgba(250,252,254,.76)"
  } }, /* @__PURE__ */ React.createElement("img", { src: item.photo, alt: "", style: { width: 40, height: 40, borderRadius: 14, objectFit: "cover" } }), /* @__PURE__ */ React.createElement("div", { style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 12.8, fontWeight: 700, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, item.name), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 3, color: T.navyLight, fontSize: 11.5, lineHeight: 1.45 } }, item.platform)), /* @__PURE__ */ React.createElement("div", { style: {
    padding: "5px 8px",
    borderRadius: 999,
    background: "rgba(224,250,244,.88)",
    color: T.success,
    fontSize: 11.2,
    fontWeight: 700,
    whiteSpace: "nowrap"
  } }, "\u76F8\u4F3C\u5EA6 ", item.similarity))));
  var planningActionButtonStyle = (variant = "secondary") => ({
    ...pillButtonStyle(variant === "primary"),
    height: 38,
    padding: "0 15px",
    borderRadius: 13,
    fontSize: 13,
    fontWeight: 720
  });
  var PLANNING_BENCHMARK_PHOTOS = [
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=900&q=80",
    "https://images.unsplash.com/photo-1498654896293-37aacf113fd9?auto=format&fit=crop&w=900&q=80"
  ];
  var PLANNING_ASSET_THUMBS = [
    "./src/inspiration-skill-card.png",
    "./src/onion-burst-real.png",
    "./src/insight-avatar-reference.png",
    "./src/onion-burst-collage.png"
  ];
  var PLANNING_STRATEGY_IMAGES = [
    "https://images.unsplash.com/photo-1528712306091-ed0763094c98?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1400&q=80"
  ];
  var PlanningSkeletonMerge = ({ diagnosisText, setDiagnosisText, audienceTags, setAudienceTags, appearanceTags, setAppearanceTags, marketTags, setMarketTags, pillars = [], setPillars = () => {
  }, isMobile, action }) => {
    const accounts = [
      { name: "@\u672C\u5730\u5403\u559D\u6307\u5357", platform: "\u5C0F\u7EA2\u4E66", similarity: "86%", photo: PLANNING_BENCHMARK_PHOTOS[0] },
      { name: "@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0", platform: "\u6296\u97F3", similarity: "79%", photo: PLANNING_BENCHMARK_PHOTOS[1] },
      { name: "@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240", platform: "\u5C0F\u7EA2\u4E66", similarity: "74%", photo: PLANNING_BENCHMARK_PHOTOS[2] }
    ];
    return /* @__PURE__ */ React.createElement(AgentCardShell, { label: "Agent \u8D26\u53F7\u5B9A\u4F4D\u786E\u8BA4", icon: "target", title: "\u8D26\u53F7\u5B9A\u4F4D / \u5BF9\u6807\u8D26\u53F7", style: { padding: 16 }, action }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 14 } }, [
      ["\u4F60\u7684\u89C2\u4F17\u662F\uFF1A", "23-38 \u5C81\u9644\u8FD1\u4E0A\u73ED\u65CF\u3001\u60C5\u4FA3\u548C\u5468\u672B\u7EA6\u996D\u4EBA\u7FA4\u3002\u4ED6\u4EEC\u5173\u5FC3\u5473\u9053\u7A33\u5B9A\u3001\u4EF7\u683C\u8212\u670D\u3001\u79BB\u81EA\u5DF1\u8FD1\uFF0C\u6700\u597D\u8BFB\u5B8C\u5C31\u77E5\u9053\u7B2C\u4E00\u6B21\u600E\u4E48\u70B9\u3002"],
      ["\u4F60\u7684\u8D5B\u9053\u662F\uFF1A", "\u4E0A\u6D77\u672C\u5730\u751F\u6D3B\u91CC\u7684\u793E\u533A\u996D\u5E97\u63A8\u8350\uFF0C\u4E0D\u505A\u6CDB\u63A2\u5E97\uFF0C\u91CD\u70B9\u5207\u300C\u9644\u8FD1\u4EBA\u771F\u5B9E\u590D\u5403\u300D\u548C\u300C\u4E0B\u73ED\u540E\u4E0D\u7EA0\u7ED3\u7684\u4E00\u987F\u996D\u300D\u3002"],
      ["\u4F60\u7684\u4EBA\u8BBE\u662F\uFF1A", "\u4EB2\u5207\u3001\u771F\u5B9E\u4E3B\u7406\u4EBA\u3001\u61C2\u672C\u5730\u751F\u6D3B\u3002\u8BF4\u8BDD\u50CF\u719F\u4EBA\u63A8\u8350\uFF0C\u4E0D\u5938\u5F20\u79CD\u8349\uFF0C\u4E5F\u4E0D\u505A\u8FC7\u5EA6\u7CBE\u4FEE\u3002"],
      ["\u4F60\u7684\u5185\u5BB9\u4EF7\u503C\u662F\uFF1A", "\u5E2E\u7528\u6237\u964D\u4F4E\u5230\u5E97\u51B3\u7B56\u6210\u672C\uFF1A\u70B9\u4EC0\u4E48\u3001\u4EC0\u4E48\u65F6\u5019\u53BB\u3001\u9002\u5408\u8C01\u53BB\u3001\u6709\u54EA\u4E9B\u907F\u5751\u4FE1\u606F\u3002"],
      ["\u4F60\u7684\u98CE\u683C\u662F\uFF1A", "\u53E3\u8BED\u5316\u3001\u8F7B\u677E\u3001\u5E72\u51C0\u3002\u5C01\u9762\u7528\u771F\u5B9E\u83DC\u54C1\u548C\u5E97\u5185\u7EC6\u8282\uFF0C\u6B63\u6587\u7528\u6E05\u6670\u5C0F\u6807\u9898\u3002"],
      ["\u4F60\u7684\u5185\u5BB9\u5927\u7EB2\u662F\uFF1A", pillars.join(" / ")],
      ["\u4F60\u7684\u8D26\u53F7\u5B9A\u4F4D\u662F\uFF1A", `${diagnosisText.position} ${diagnosisText.selling}`]
    ].map(([label, value]) => /* @__PURE__ */ React.createElement("section", { key: label, style: { display: "grid", gap: 5 } }, /* @__PURE__ */ React.createElement("h4", { style: { margin: 0, color: T.navy, fontSize: 14.2, lineHeight: 1.42, fontWeight: 700 } }, label), /* @__PURE__ */ React.createElement("p", { style: { margin: 0, color: T.navyMid, fontSize: 13.1, lineHeight: 1.68 } }, value))), /* @__PURE__ */ React.createElement("section", null, /* @__PURE__ */ React.createElement("h4", { style: { margin: "0 0 8px", color: T.navy, fontSize: 14.2, fontWeight: 700 } }, "\u4F60\u7684\u5BF9\u6807\u535A\u4E3B\u662F\uFF1A"), /* @__PURE__ */ React.createElement(PlanningBenchmarkList, { accounts })), /* @__PURE__ */ React.createElement("section", { style: { display: "grid", gap: 8 } }, /* @__PURE__ */ React.createElement("h4", { style: { margin: 0, color: T.navy, fontSize: 14.2, lineHeight: 1.42, fontWeight: 700 } }, "\u54C1\u724C\u8D44\u4EA7\u6C89\u6DC0"), /* @__PURE__ */ React.createElement("div", { style: {
      borderRadius: 16,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(250,252,254,.72)",
      padding: isMobile ? 12 : 14,
      display: "grid",
      gridTemplateColumns: isMobile ? "1fr" : "repeat(2, minmax(0, 1fr))",
      gap: 10
    } }, [
      ["\u5E97\u94FA\u540D", "\u5DF7\u53E3\u6696\u80C3\u5C0F\u9986\uFF0C\u53EF\u4F5C\u4E3A\u8D26\u53F7\u4E3B\u540D\u6216\u7CFB\u5217\u680F\u76EE\u540D\u3002"],
      ["Logo \u7EBF\u7D22", "\u6696\u8272\u5C0F\u7897\u56FE\u5F62\u9002\u5408\u505A\u5934\u50CF\u3001\u5C01\u9762\u89D2\u6807\u548C\u6C34\u5370\u3002"],
      ["\u89C6\u89C9\u98CE\u683C", "\u771F\u5B9E\u83DC\u54C1\u8FD1\u666F\u3001\u6696\u8272\u81EA\u7136\u5149\u3001\u5E72\u51C0\u5C0F\u6807\u9898\u3002"],
      ["\u8BED\u6C14\u8D44\u4EA7", "\u719F\u4EBA\u63A8\u8350\u3001\u4E0D\u5938\u5F20\uFF0C\u5148\u7ED9\u70B9\u5355\u7ED3\u8BBA\u518D\u8865\u7406\u7531\u3002"]
    ].map(([label, value]) => /* @__PURE__ */ React.createElement("div", { key: label, style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 11.4, lineHeight: 1.35, fontWeight: 680, marginBottom: 4 } }, label), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyMid, fontSize: 12.6, lineHeight: 1.58, fontWeight: 480 } }, value)))))));
  };
  var PlanningStrategyDocModal = ({ strategy, onClose }) => {
    if (!strategy) return null;
    return /* @__PURE__ */ React.createElement("div", { style: { position: "fixed", inset: 0, zIndex: 1e3, background: "rgba(8,8,18,.46)", display: "flex", alignItems: "center", justifyContent: "center", padding: 24 } }, /* @__PURE__ */ React.createElement("div", { style: { width: "min(920px, 100%)", maxHeight: "86vh", overflow: "hidden", borderRadius: 26, background: T.white, border: `1px solid ${T.hairlineSoft}`, boxShadow: "0 44px 110px rgba(14,14,44,.24)" } }, /* @__PURE__ */ React.createElement("div", { style: { height: 64, padding: "0 22px", borderBottom: `1px solid ${T.hairlineSoft}`, display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 12 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 38, height: 38, borderRadius: 14, background: T.irisTint, color: T.iris, display: "inline-flex", alignItems: "center", justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "document", size: 18 })), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 16, fontWeight: 740 } }, strategy.name, " \xB7 \u5B8C\u6574\u8FD0\u8425\u8BA1\u5212"), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 3, color: T.navyLight, fontSize: 12.2 } }, "\u521A\u521A\u751F\u6210 \xB7 \u53EF\u7528\u4E8E\u540E\u7EED\u521B\u4F5C"))), /* @__PURE__ */ React.createElement("button", { onClick: onClose, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 15, color: T.navyMid }))), /* @__PURE__ */ React.createElement("div", { style: { overflowY: "auto", maxHeight: "calc(86vh - 64px)", padding: "34px min(9vw, 86px) 48px" } }, /* @__PURE__ */ React.createElement("h1", { style: { margin: 0, color: T.navy, fontSize: 34, lineHeight: 1.18, fontWeight: 740 } }, strategy.name, " \u5B8C\u6574\u8FD0\u8425\u8BA1\u5212"), [
      ["1. \u8D26\u53F7\u5B9A\u4F4D", strategy.position],
      ["2. \u4EBA\u8BBE\u5173\u952E\u8BCD", strategy.keyword],
      ["3. \u5185\u5BB9\u652F\u67F1", strategy.pillar],
      ["4. \u7B7E\u540D", strategy.bio],
      ["5. \u53D1\u5E03\u8282\u594F", "\u7B2C\u4E00\u5468\u5148\u7528\u300C\u771F\u5B9E\u573A\u666F + \u53EF\u6536\u85CF\u6E05\u5355\u300D\u9A8C\u8BC1\u70B9\u51FB\u548C\u6536\u85CF\uFF0C\u56FE\u6587\u4E0E\u77ED\u89C6\u9891\u4EA4\u66FF\u3002"],
      ["6. \u6570\u636E\u76EE\u6807", "7 \u5929\u5185\u9A8C\u8BC1 1 \u5957\u7A33\u5B9A\u6807\u9898\u7ED3\u6784\uFF0C\u91CD\u70B9\u770B\u6536\u85CF\u3001\u8BC4\u8BBA\u548C\u51C0\u6DA8\u7C89\u3002"]
    ].map(([title, body]) => /* @__PURE__ */ React.createElement("section", { key: title, style: { marginTop: 30 } }, /* @__PURE__ */ React.createElement("h2", { style: { margin: "0 0 12px", color: T.navy, fontSize: 22, fontWeight: 740 } }, title), /* @__PURE__ */ React.createElement("p", { style: { margin: 0, color: T.navyMid, fontSize: 15, lineHeight: 1.9 } }, body))))));
  };
  var PlanningStrategyCards = ({ isMobile, activeReport, pillars, onOpenDoc, onConfirm }) => {
    const [expandedId, setExpandedId] = React.useState("warm");
    const [selectedId, setSelectedId] = React.useState("warm");
    const [checkedId, setCheckedId] = React.useState(null);
    const strategies = [
      {
        id: "warm",
        name: activeReport.names?.[0] || "\u5DF7\u53E3\u6696\u80C3\u5C0F\u9986",
        keyword: activeReport.keywords?.[0] || "\u771F\u5B9E\u4E3B\u7406\u4EBA",
        pillar: pillars?.[0] || "\u62DB\u724C\u83DC\u6545\u4E8B",
        bio: activeReport.bio || "\u6BCF\u5929\u8BA4\u771F\u505A\u4E00\u7897\u6709\u70DF\u706B\u6C14\u7684\u5BB6\u5E38\u996D\u3002",
        position: "\u505A\u9644\u8FD1\u4EBA\u613F\u610F\u6536\u85CF\u7684\u70DF\u706B\u6C14\u5C0F\u9986\u8D26\u53F7\uFF0C\u5148\u5EFA\u7ACB\u4FE1\u4EFB\uFF0C\u518D\u5F15\u5BFC\u5230\u5E97\u3002",
        recommended: true,
        image: PLANNING_STRATEGY_IMAGES[0],
        why: "\u6700\u8D34\u8FD1\u4F60\u73B0\u6709\u7D20\u6750\u548C\u95E8\u5E97\u6C14\u8D28\uFF0C\u7B2C\u4E00\u5468\u9A8C\u8BC1\u6210\u672C\u6700\u4F4E\u3002"
      },
      {
        id: "city",
        name: "\u9644\u8FD1\u5348\u9910\u7814\u7A76\u6240",
        keyword: "\u6548\u7387\u53CB\u597D",
        pillar: "30 \u5206\u949F\u5348\u9910\u65B9\u6848",
        bio: "\u5E2E\u9644\u8FD1\u4E0A\u73ED\u65CF\u5FEB\u901F\u627E\u5230\u4E00\u987F\u4E0D\u8E29\u96F7\u7684\u996D\u3002",
        position: "\u7528\u7EC6\u5206\u573A\u666F\u5207\u5165\u672C\u5730\u5348\u9910\u9700\u6C42\uFF0C\u4E3B\u6253\u6536\u85CF\u548C\u641C\u7D22\u3002",
        image: PLANNING_STRATEGY_IMAGES[1],
        why: "\u9002\u5408\u505A\u641C\u7D22\u6D41\u91CF\u548C\u83DC\u5355\u5408\u96C6\uFF0C\u5185\u5BB9\u66F4\u5DE5\u5177\u5316\u3002"
      },
      {
        id: "owner",
        name: "\u4E3B\u7406\u4EBA\u8BA4\u771F\u996D",
        keyword: "\u4E3B\u7406\u4EBA\u89C6\u89D2",
        pillar: "\u8001\u677F\u7684\u4E00\u5929",
        bio: "\u628A\u5C0F\u5E97\u65E5\u5E38\u8BB2\u7ED9\u771F\u6B63\u4F1A\u590D\u5403\u7684\u4EBA\u542C\u3002",
        position: "\u63D0\u9AD8\u4EBA\u7269\u8BB0\u5FC6\u70B9\uFF0C\u8BA9\u7528\u6237\u5148\u8BB0\u4F4F\u4EBA\uFF0C\u518D\u8BB0\u4F4F\u83DC\u3002",
        image: PLANNING_STRATEGY_IMAGES[2],
        why: "\u9002\u5408\u4E3B\u7406\u4EBA\u613F\u610F\u7A33\u5B9A\u51FA\u955C\u65F6\u4F7F\u7528\uFF0C\u4FE1\u4EFB\u611F\u66F4\u5F3A\u3002"
      }
    ];
    return /* @__PURE__ */ React.createElement(
      AgentCardShell,
      {
        label: "Agent \u8FD0\u8425\u8BA1\u5212",
        icon: "layers",
        title: "\u4E09\u5957\u53EF\u6267\u884C\u8FD0\u8425\u8BA1\u5212",
        action: /* @__PURE__ */ React.createElement("button", { onClick: () => onConfirm?.(), style: { ...planningActionButtonStyle("primary") } }, "\u786E\u8BA4\u8FD0\u8425\u8BA1\u5212\uFF0C\u6392\u671F", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 14 }))
      },
      /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 11 } }, strategies.map((item, index) => {
        const expanded = isMobile || expandedId === item.id;
        const selected = selectedId === item.id;
        const checked = checkedId === item.id;
        return /* @__PURE__ */ React.createElement("div", { key: item.id, style: {
          padding: 0,
          overflow: "hidden",
          borderRadius: 18,
          background: expanded ? "rgba(255,255,255,.90)" : "rgba(255,255,255,.74)",
          border: expanded ? "1px solid rgba(14,14,44,.14)" : `1px solid ${T.hairlineSoft}`,
          boxShadow: expanded ? "0 22px 54px rgba(14,14,44,.11), inset 0 1px 0 rgba(255,255,255,.90)" : "0 8px 18px rgba(14,14,44,.035), inset 0 1px 0 rgba(255,255,255,.80)",
          cursor: expanded ? "default" : "pointer",
          transition: `box-shadow .32s ${T.spring}, border .24s ${T.ease}, background .24s ${T.ease}`
        } }, /* @__PURE__ */ React.createElement("div", { onClick: () => {
          setExpandedId(item.id);
          setSelectedId(item.id);
        }, style: {
          display: "grid",
          gridTemplateColumns: isMobile ? "1fr" : expanded ? "minmax(0, 1.05fr) minmax(230px, .55fr)" : "56px minmax(0, 1fr) auto",
          gap: expanded ? 0 : 13,
          alignItems: "stretch",
          minHeight: expanded ? 216 : 74
        } }, expanded ? /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("div", { style: { padding: isMobile ? 18 : item.recommended ? 22 : 19, display: "flex", flexDirection: "column", justifyContent: "space-between", gap: 18, background: item.recommended ? "linear-gradient(135deg, rgba(255,255,255,.92), rgba(245,255,224,.34))" : "transparent" } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap", marginBottom: 13 } }, item.recommended && /* @__PURE__ */ React.createElement("span", { style: { height: 28, padding: "0 11px", borderRadius: 999, background: T.primary, color: T.navy, fontSize: 12, fontWeight: 800, boxShadow: "0 10px 22px rgba(214,255,0,.22)" } }, "Nori \u63A8\u8350"), /* @__PURE__ */ React.createElement("span", { style: { height: 27, padding: "0 10px", borderRadius: 999, background: "rgba(250,252,254,.82)", border: `1px solid ${T.hairlineSoft}`, color: T.navyLight, fontSize: 11.8, fontWeight: 680 } }, "\u8FD0\u8425\u8BA1\u5212 ", index + 1)), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: isMobile ? 22 : item.recommended ? 28 : 25, lineHeight: 1.16, fontWeight: item.recommended ? 800 : 760, letterSpacing: 0 } }, item.name), /* @__PURE__ */ React.createElement("p", { style: { margin: "11px 0 0", color: T.navyMid, fontSize: 13.6, lineHeight: 1.66, maxWidth: 560 } }, item.position)), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "repeat(3, minmax(0, 1fr))", gap: 9 } }, [
          ["\u8D26\u53F7\u540D", item.name],
          ["\u4EBA\u8BBE\u5173\u952E\u8BCD", item.keyword],
          ["\u5185\u5BB9\u652F\u67F1", item.pillar],
          ["\u7B7E\u540D", item.bio]
        ].map(([label, value], detailIndex) => /* @__PURE__ */ React.createElement("div", { key: label, style: { gridColumn: detailIndex === 3 && !isMobile ? "span 3" : "auto", borderRadius: 14, background: "rgba(250,252,254,.72)", border: `1px solid ${T.hairlineSoft}`, padding: "10px 11px" } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 11.2, fontWeight: 680, marginBottom: 4 } }, label), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 12.7, lineHeight: 1.48, fontWeight: 640 } }, value)))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center", flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 12.2, lineHeight: 1.5 } }, "\u63A8\u8350\u539F\u56E0\uFF1A", item.why), /* @__PURE__ */ React.createElement("button", { onClick: (e) => {
          e.stopPropagation();
          onOpenDoc(item);
        }, style: { ...planningActionButtonStyle("secondary"), height: 36, borderRadius: 13, fontSize: 12.6, justifyContent: "center" } }, "\u67E5\u770B\u5B8C\u6574\u8FD0\u8425\u8BA1\u5212"))), /* @__PURE__ */ React.createElement("div", { style: { minHeight: isMobile ? 168 : "auto", background: `linear-gradient(90deg, rgba(14,14,44,.10), rgba(14,14,44,.34)), url(${item.image}) center / cover`, position: "relative" } }, /* @__PURE__ */ React.createElement("div", { style: { position: "absolute", inset: 0, background: "linear-gradient(180deg, rgba(255,255,255,0), rgba(14,14,44,.18))" } }), /* @__PURE__ */ React.createElement(
          "button",
          {
            onClick: (e) => {
              e.stopPropagation();
              setCheckedId(item.id);
              setSelectedId(item.id);
            },
            style: {
              position: "absolute",
              right: 16,
              top: 16,
              height: 34,
              minWidth: 34,
              padding: checked ? "0 11px" : 0,
              borderRadius: 999,
              border: checked ? "1px solid rgba(49,208,170,.24)" : "1px solid rgba(14,14,44,.12)",
              background: checked ? T.success : "rgba(255,255,255,.78)",
              color: checked ? T.white : T.navyLight,
              display: "inline-flex",
              alignItems: "center",
              justifyContent: "center",
              gap: 6,
              boxShadow: checked ? "0 14px 30px rgba(49,208,170,.22)" : "0 12px 28px rgba(14,14,44,.18)",
              cursor: "pointer",
              fontSize: 12,
              fontWeight: 780,
              transition: `transform .24s ${T.spring}, background .2s ${T.ease}, box-shadow .24s ${T.spring}, color .2s ${T.ease}`
            }
          },
          /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 15, stroke: 2.2 }),
          checked && "\u5DF2\u9009\u62E9"
        ))) : /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("div", { style: { margin: 12, width: 50, height: 50, borderRadius: 16, background: `url(${item.image}) center / cover`, border: `1px solid ${T.hairlineSoft}`, boxShadow: "0 8px 18px rgba(14,14,44,.06)", filter: item.recommended ? "saturate(1.06)" : "saturate(.92) brightness(.98)" } }), /* @__PURE__ */ React.createElement("div", { style: { padding: "12px 0", minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, alignItems: "center", marginBottom: 5 } }, /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 11.8, fontWeight: 650 } }, "\u8FD0\u8425\u8BA1\u5212 ", index + 1), /* @__PURE__ */ React.createElement("span", { style: { color: T.navySoft, fontSize: 11 } }, "\u70B9\u51FB\u5C55\u5F00")), /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 15, lineHeight: 1.35, fontWeight: 700, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" } }, item.name)), /* @__PURE__ */ React.createElement("button", { onClick: (e) => {
          e.stopPropagation();
          setExpandedId(item.id);
          setSelectedId(item.id);
        }, style: { margin: "18px 14px 18px 0", height: 34, padding: "0 12px", borderRadius: 12, border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.72)", color: T.navyMid, cursor: "pointer", display: "inline-flex", alignItems: "center", gap: 6, fontSize: 12.2, fontWeight: 650, boxShadow: "none" } }, "\u5C55\u5F00", /* @__PURE__ */ React.createElement(Icon, { name: "chevronRight", size: 12 })))));
      }))
    );
  };
  var PlanningCalendarPreviewCard = ({ calendar = [], onView, onGenerate }) => /* @__PURE__ */ React.createElement(
    AgentCardShell,
    {
      label: "Agent \u5185\u5BB9\u65E5\u5386",
      icon: "calendar",
      title: "\u7B2C\u4E00\u5468\u5185\u5BB9\u6392\u671F\u5DF2\u751F\u6210",
      style: { padding: 14 },
      bodyStyle: { fontSize: 12.8 },
      action: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement("button", { onClick: onView, style: { ...planningActionButtonStyle("secondary"), height: 34, borderRadius: 12, fontSize: 12.5 } }, "\u67E5\u770B", /* @__PURE__ */ React.createElement(Icon, { name: "expand", size: 13 })), /* @__PURE__ */ React.createElement("button", { onClick: onGenerate, style: { ...planningActionButtonStyle("primary"), height: 34, borderRadius: 12, fontSize: 12.5 } }, "\u76F4\u63A5\u751F\u6210", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 13 })))
    },
    /* @__PURE__ */ React.createElement("div", { style: {
      minHeight: 82,
      borderRadius: 14,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(250,252,254,.72)",
      display: "grid",
      gridTemplateColumns: "repeat(5, minmax(0, 1fr))",
      gap: 6,
      padding: 8
    } }, ["\u5468\u4E00", "\u5468\u4E8C", "\u5468\u4E09", "\u5468\u56DB", "\u5468\u4E94"].map((day, index) => {
      const item = calendar.find((row) => row.day === day) || calendar[index] || {};
      const topic = item.topic || "\u5185\u5BB9\u9009\u9898";
      return /* @__PURE__ */ React.createElement("div", { key: day, style: {
        borderRadius: 10,
        background: index === 0 ? T.irisTint : "rgba(255,255,255,.74)",
        border: `1px solid ${index === 0 ? "rgba(75,77,237,.12)" : T.hairlineSoft}`,
        display: "grid",
        gap: 5,
        alignContent: "start",
        padding: "8px 8px 7px",
        color: index === 0 ? T.iris : T.navyLight
      } }, /* @__PURE__ */ React.createElement("span", { style: { fontSize: 11.1, lineHeight: 1, fontWeight: 760 } }, day), /* @__PURE__ */ React.createElement("span", { style: {
        color: T.navyMid,
        fontSize: 10.8,
        lineHeight: 1.34,
        fontWeight: 560,
        display: "-webkit-box",
        WebkitLineClamp: 2,
        WebkitBoxOrient: "vertical",
        overflow: "hidden"
      } }, topic));
    }))
  );
  var PlanningCalendarModal = ({ open, onClose, children, onGenerate }) => {
    if (!open) return null;
    return /* @__PURE__ */ React.createElement("div", { style: {
      position: "fixed",
      inset: 0,
      zIndex: 1200,
      background: "rgba(8,8,18,.34)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: 24
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      width: "min(1180px, calc(100vw - 48px))",
      maxHeight: "88vh",
      overflow: "hidden",
      borderRadius: 24,
      border: `1px solid ${T.hairlineSoft}`,
      background: T.white,
      boxShadow: "0 34px 90px rgba(14,14,44,.22)",
      display: "flex",
      flexDirection: "column"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      height: 58,
      padding: "0 18px",
      borderBottom: `1px solid ${T.hairlineSoft}`,
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: 12,
      flexShrink: 0
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10, color: T.navy, fontSize: 15, fontWeight: 730 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 30, height: 30, borderRadius: 11, background: T.irisTint, color: T.iris, display: "inline-flex", alignItems: "center", justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "calendar", size: 15 })), "\u7B2C\u4E00\u5468\u5185\u5BB9\u65E5\u5386"), /* @__PURE__ */ React.createElement("button", { onClick: onClose, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 14, color: T.navyMid }))), /* @__PURE__ */ React.createElement("div", { style: { overflow: "auto", padding: 16 } }, children), /* @__PURE__ */ React.createElement("div", { style: { padding: "0 16px 16px", display: "flex", justifyContent: "flex-end", flexShrink: 0 } }, /* @__PURE__ */ React.createElement("button", { onClick: onGenerate, style: { ...planningActionButtonStyle("primary") } }, "\u5F00\u59CB\u751F\u6210\u7B2C\u4E00\u7BC7", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 14 })))));
  };
  var PlanningCalendarBoard = ({ calendar, setCalendar, weekStart, setWeekStart, isMobile, wide = false }) => {
    const [activeEvent, setActiveEvent] = React.useState(null);
    const [draggingId, setDraggingId] = React.useState(null);
    const times = ["09:00", "11:30", "14:00", "16:30", "20:00"];
    const dayDates = ["05/18", "05/19", "05/20", "05/21", "05/22", "05/23", "05/24"];
    const days = ["\u5468\u4E00", "\u5468\u4E8C", "\u5468\u4E09", "\u5468\u56DB", "\u5468\u4E94", "\u5468\u516D", "\u5468\u65E5"];
    const tones = [
      { bg: "rgba(239,239,253,.76)", border: "rgba(75,77,237,.16)", fg: T.iris },
      { bg: "rgba(224,250,244,.76)", border: "rgba(49,208,170,.16)", fg: T.success },
      { bg: "rgba(245,255,224,.86)", border: "rgba(214,255,0,.28)", fg: "#6e8400" },
      { bg: "rgba(253,245,245,.86)", border: "rgba(243,219,218,.95)", fg: T.navyMid }
    ];
    const events = calendar.map((item, index) => {
      const dayIndex = Math.max(0, days.indexOf(item.day));
      const timeIndex = Math.max(0, times.indexOf(item.time || times[index % times.length]));
      return {
        ...item,
        id: item.id || `calendar-${index}`,
        date: dayDates[dayIndex] || dayDates[index] || "05/25",
        time: item.time || times[index % times.length],
        dayIndex,
        timeIndex,
        top: 72 + timeIndex * 84,
        tone: tones[index % tones.length]
      };
    });
    const addCalendarItem = () => {
      const id = `calendar-new-${Date.now()}`;
      setCalendar((list) => [{ id, day: "\u5468\u4E00", time: "11:30", type: "\u56FE\u6587", topic: "\u65B0\u589E\u5185\u5BB9\u9009\u9898\uFF0C\u70B9\u51FB\u540E\u53EF\u4FEE\u6539", ref: "@\u53C2\u8003\u8D26\u53F7" }, ...list]);
      setActiveEvent(id);
    };
    const moveEventToDay = (eventId, nextDay) => {
      setCalendar((list) => list.map((row, index) => (row.id || `calendar-${index}`) === eventId ? { ...row, id: eventId, day: nextDay } : { ...row, id: row.id || `calendar-${index}` }));
    };
    if (isMobile) {
      return /* @__PURE__ */ React.createElement(AgentCardShell, { label: "Agent \u5185\u5BB9\u65E5\u5386", icon: "calendar", title: "\u7B2C\u4E00\u5468\u5185\u5BB9\u6392\u671F", style: { padding: 16, width: wide ? "100%" : AGENT_CARD_WIDTH } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8, marginBottom: 12 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 17, fontWeight: 730 } }, "2026 \u5E74 5 \u6708"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 8, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("input", { type: "date", value: weekStart, onChange: (e) => setWeekStart(e.target.value), style: { height: 38, borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: T.white, color: T.navyMid, padding: "0 10px", fontFamily: T.fontSans, fontSize: 12.5 } }), /* @__PURE__ */ React.createElement("button", { onClick: addCalendarItem, style: { ...pillButtonStyle(true), height: 38, borderRadius: 13, fontSize: 13 } }, /* @__PURE__ */ React.createElement(Icon, { name: "plus", size: 14 }), "\u65B0\u589E\u5185\u5BB9"))), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 9 } }, events.map((item, index) => /* @__PURE__ */ React.createElement("div", { key: `${item.day}-${index}`, onClick: () => setActiveEvent(activeEvent === index ? null : index), style: { borderRadius: 16, border: `1px solid ${item.tone.border}`, background: item.tone.bg, padding: 12, cursor: "pointer" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 8, alignItems: "center" } }, /* @__PURE__ */ React.createElement("div", { style: { color: item.tone.fg, fontSize: 11.8, fontWeight: 760 } }, item.day, " \xB7 ", item.type), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 11.2, fontFamily: T.fontMono } }, item.time)), /* @__PURE__ */ React.createElement("textarea", { value: item.topic, rows: 2, onChange: (e) => setCalendar((list) => list.map((row, i) => i === index ? { ...row, topic: e.target.value } : row)), style: { marginTop: 7, width: "100%", border: "none", background: "transparent", color: T.navy, fontSize: 13, outline: "none", resize: "vertical", fontFamily: T.fontSans, lineHeight: 1.52 } }), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 11.2 } }, "\u53C2\u8003\uFF1A", item.ref)))));
    }
    return /* @__PURE__ */ React.createElement(AgentCardShell, { label: "Agent \u5185\u5BB9\u65E5\u5386", icon: "calendar", title: "\u7B2C\u4E00\u5468\u5185\u5BB9\u6392\u671F", style: { padding: 0, overflow: "hidden", width: wide ? "100%" : AGENT_CARD_WIDTH }, bodyStyle: { fontSize: 13 } }, /* @__PURE__ */ React.createElement("div", { style: { height: 60, padding: "0 18px", borderBottom: `1px solid ${T.hairlineSoft}`, display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 18, fontWeight: 740 } }, "2026 \u5E74 5 \u6708"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 10 } }, /* @__PURE__ */ React.createElement("input", { type: "date", value: weekStart, onChange: (e) => setWeekStart(e.target.value), style: { height: 38, borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: T.white, color: T.navyMid, padding: "0 10px", fontFamily: T.fontSans, fontSize: 12.5 } }), /* @__PURE__ */ React.createElement("button", { onClick: addCalendarItem, style: { ...pillButtonStyle(true), height: 38, borderRadius: 13 } }, /* @__PURE__ */ React.createElement(Icon, { name: "plus", size: 15 }), "\u65B0\u589E\u5185\u5BB9"))), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: wide ? "68px repeat(7, minmax(105px, 1fr))" : "74px repeat(7, minmax(130px, 1fr))", minHeight: wide ? 492 : 518, overflowX: "auto" } }, /* @__PURE__ */ React.createElement("div", { style: { borderRight: `1px solid ${T.hairlineSoft}`, background: "rgba(250,252,254,.58)" } }, /* @__PURE__ */ React.createElement("div", { style: { height: 70, borderBottom: `1px solid ${T.hairlineSoft}` } }), times.map((time) => /* @__PURE__ */ React.createElement("div", { key: time, style: { height: 84, borderBottom: `1px solid ${T.hairlineSoft}`, padding: "14px 12px", color: T.navyLight, fontSize: 12, fontFamily: T.fontMono } }, time))), days.map((day, index) => /* @__PURE__ */ React.createElement(
      "div",
      {
        key: day,
        onDragOver: (e) => e.preventDefault(),
        onDrop: (e) => {
          e.preventDefault();
          const eventId = e.dataTransfer.getData("text/plain") || draggingId;
          if (eventId) moveEventToDay(eventId, day);
          setDraggingId(null);
        },
        style: { minWidth: 130, borderRight: index === days.length - 1 ? "none" : `1px solid ${T.hairlineSoft}`, position: "relative", background: draggingId ? "rgba(250,252,254,.42)" : "transparent" }
      },
      /* @__PURE__ */ React.createElement("div", { style: { height: 70, borderBottom: `1px solid ${T.hairlineSoft}`, display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "column", background: index === 3 ? "rgba(239,239,253,.28)" : "transparent" } }, /* @__PURE__ */ React.createElement("div", { style: { color: index === 3 ? T.iris : T.navy, fontSize: 13.5, fontWeight: 740 } }, day), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 4, color: T.navyLight, fontSize: 11.2, fontFamily: T.fontMono } }, dayDates[index])),
      times.map((time) => /* @__PURE__ */ React.createElement("div", { key: time, style: { height: 84, borderBottom: `1px solid ${T.hairlineSoft}`, background: index === 3 ? "rgba(239,239,253,.12)" : "transparent" } })),
      events.filter((event) => event.day === day).map((event) => /* @__PURE__ */ React.createElement(
        "div",
        {
          key: event.id,
          draggable: true,
          onDragStart: (e) => {
            setDraggingId(event.id);
            e.dataTransfer.setData("text/plain", event.id);
            e.dataTransfer.effectAllowed = "move";
          },
          onDragEnd: () => setDraggingId(null),
          onClick: () => setActiveEvent(activeEvent === event.id ? null : event.id),
          style: {
            position: "absolute",
            top: event.top,
            left: 12,
            right: 12,
            borderRadius: 17,
            border: `1px solid ${event.tone.border}`,
            background: event.tone.bg,
            padding: 12,
            boxShadow: activeEvent === event.id ? "0 18px 34px rgba(14,14,44,.10)" : "0 14px 28px rgba(14,14,44,.055)",
            cursor: "grab",
            zIndex: activeEvent === event.id ? 4 : 2,
            opacity: draggingId === event.id ? 0.58 : 1
          }
        },
        /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 8, marginBottom: 7 } }, /* @__PURE__ */ React.createElement("span", { style: { color: event.tone.fg, fontSize: 11.8, fontWeight: 780 } }, event.type), /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 11.2, fontFamily: T.fontMono } }, event.time)),
        /* @__PURE__ */ React.createElement("textarea", { value: event.topic, rows: 3, onChange: (e) => setCalendar((list) => list.map((row, i) => (row.id || `calendar-${i}`) === event.id ? { ...row, id: event.id, topic: e.target.value } : row)), style: { width: "100%", border: "none", background: "transparent", color: T.navy, fontSize: 13, lineHeight: 1.48, fontWeight: 650, resize: "vertical", outline: "none", fontFamily: T.fontSans } }),
        /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 11.2, lineHeight: 1.4 } }, event.ref),
        activeEvent === event.id && null
      ))
    ))));
  };
  var loadPlanDraft = () => {
    try {
      const raw = window.localStorage?.getItem(PLAN_STORAGE_KEY);
      if (!raw) return null;
      return JSON.parse(raw);
    } catch {
      return null;
    }
  };
  var clearPlanDraftStorage = () => {
    try {
      window.localStorage?.removeItem(PLAN_STORAGE_KEY);
    } catch {
    }
  };
  var AccountPlanningPagePolishedV2 = ({ onBackHome, onNewChat, onOpenAssets, onOpenSkills, onOpenInsights, onComplete }) => {
    const { isMobile } = useViewport();
    const savedDraft = null;
    const [step, setStep] = React.useState(1);
    const [modalType, setModalType] = React.useState(null);
    const [attachments, setAttachments] = React.useState([]);
    const [rawInput, setRawInput] = React.useState("");
    const [sentIntro, setSentIntro] = React.useState(false);
    const [goalSelections, setGoalSelections] = React.useState([]);
    const [platformSelections, setPlatformSelections] = React.useState([]);
    const [diagnosisText, setDiagnosisText] = React.useState({
      position: "\u505A\u9644\u8FD1\u4EBA\u613F\u610F\u6536\u85CF\u7684\u70DF\u706B\u6C14\u5C0F\u9986\u8D26\u53F7\u3002\u4F60\u7684\u4F18\u52BF\u4E0D\u662F\u5927\u54C1\u724C\u611F\uFF0C\u800C\u662F\u7A33\u5B9A\u3001\u771F\u5B9E\u3001\u79BB\u7528\u6237\u5F88\u8FD1\u3002\u5185\u5BB9\u8981\u8BA9\u4EBA\u89C9\u5F97\u4E0B\u73ED\u5C31\u80FD\u53BB\u3002",
      audience: "23-38 \u5C81\u9644\u8FD1\u4E0A\u73ED\u65CF\u3001\u60C5\u4FA3\u548C\u5468\u672B\u7EA6\u996D\u4EBA\u7FA4\uFF0C\u5173\u5FC3\u5473\u9053\u7A33\u5B9A\u3001\u4EF7\u683C\u8212\u670D\u3001\u8DDD\u79BB\u65B9\u4FBF\u3002",
      directions: "\u62DB\u724C\u83DC\u6545\u4E8B\uFF1A\u8BA9\u7528\u6237\u8BB0\u4F4F\u4F60\u548C\u522B\u7684\u5E97\u4E0D\u4E00\u6837\u7684\u5730\u65B9\u3002\n\u771F\u5B9E\u5230\u5E97\u573A\u666F\uFF1A\u964D\u4F4E\u7B2C\u4E00\u6B21\u5230\u5E97\u7684\u5FC3\u7406\u6210\u672C\u3002\n\u672C\u5730\u751F\u6D3B\u653B\u7565\uFF1A\u628A\u9910\u5385\u5185\u5BB9\u53D8\u6210\u53EF\u6536\u85CF\u7684\u4FE1\u606F\u3002",
      benchmarks: "@\u672C\u5730\u5403\u559D\u6307\u5357\uFF1A\u6807\u9898\u6E05\u695A\uFF0C\u9002\u5408\u5B66\u4E60\u9009\u9898\u5305\u88C5\u3002\n@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0\uFF1A\u64C5\u957F\u628A\u5C0F\u5E97\u65E5\u5E38\u62CD\u5F97\u6709\u4EBA\u60C5\u5473\u3002\n@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240\uFF1A\u5348\u9910\u573A\u666F\u5207\u5F97\u7EC6\uFF0C\u5BB9\u6613\u5F15\u6D41\u5230\u5E97\u3002",
      selling: "\u7A33\u5B9A\u5BB6\u5E38\u5473 + \u5E97\u4E3B\u771F\u5B9E\u611F + \u79BB\u9644\u8FD1\u4EBA\u751F\u6D3B\u5F88\u8FD1\u3002"
    });
    const [persona, setPersona] = React.useState({
      name: "\u5DF7\u53E3\u6696\u80C3\u5C0F\u9986",
      bio: "\u6BCF\u5929\u8BA4\u771F\u505A\u4E00\u7897\u6709\u70DF\u706B\u6C14\u7684\u5BB6\u5E38\u996D\uFF0C\u7ED9\u9644\u8FD1\u4EBA\u4E00\u4E2A\u4E0D\u7528\u7EA0\u7ED3\u7684\u5403\u996D\u9009\u62E9\u3002",
      keywords: "\u4EB2\u5207\u4F46\u4E0D\u6CB9\u817B\u3001\u61C2\u672C\u5730\u751F\u6D3B\u3001\u771F\u5B9E\u4E3B\u7406\u4EBA\u3001\u7A33\u5B9A\u597D\u5403",
      tone: "\u4ECA\u5929\u8FD9\u7897\u996D\uFF0C\u9002\u5408\u4E0B\u73ED\u540E\u6765\u4E00\u53E3\u3002 / \u7B2C\u4E00\u6B21\u6765\u4E0D\u77E5\u9053\u70B9\u4EC0\u4E48\uFF0C\u5148\u770B\u8FD9\u4E00\u7BC7\u3002",
      cover: "\u6696\u8272\u81EA\u7136\u5149 + \u83DC\u54C1\u8FD1\u666F + \u5927\u7559\u767D\u6807\u9898"
    });
    const [pillars, setPillars] = React.useState(["\u62DB\u724C\u83DC\u6545\u4E8B", "\u5348\u9910\u4E0D\u8E29\u96F7", "\u8001\u677F\u7684\u4E00\u5929", "\u771F\u5B9E\u987E\u5BA2\u53CD\u9988", "\u5468\u672B\u670B\u53CB\u5C40\u83DC\u5355"]);
    const [calendar, setCalendar] = React.useState([
      { day: "\u5468\u4E00", type: "\u63A2\u5E97\u56FE\u6587", topic: "\u7B2C\u4E00\u6B21\u6765\u5E97\u91CC\uFF0C\u5148\u70B9\u8FD9 3 \u9053\u62DB\u724C\u83DC", ref: "@\u672C\u5730\u5403\u559D\u6307\u5357" },
      { day: "\u5468\u4E8C", type: "\u77ED\u89C6\u9891", topic: "\u540E\u53A8\u5907\u83DC 30 \u79D2\uFF0C\u770B\u770B\u4E00\u7897\u996D\u600E\u4E48\u88AB\u8BA4\u771F\u505A\u597D", ref: "@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0" },
      { day: "\u5468\u4E09", type: "\u56FE\u6587", topic: "\u9644\u8FD1\u4E0A\u73ED\u65CF\u5348\u9910\u4E0D\u8E29\u96F7\u83DC\u5355", ref: "@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240" },
      { day: "\u5468\u56DB", type: "\u957F\u6587", topic: "\u4E00\u5BB6\u5C0F\u5E97\u600E\u4E48\u628A\u56DE\u5934\u5BA2\u7559\u4F4F", ref: "@\u4E3B\u7406\u4EBA\u624B\u8BB0" },
      { day: "\u5468\u4E94", type: "\u77ED\u89C6\u9891", topic: "\u987E\u5BA2\u6700\u5E38\u95EE\u7684 5 \u4E2A\u95EE\u9898", ref: "@\u771F\u5B9E\u63A2\u5E97" },
      { day: "\u5468\u516D", type: "\u56FE\u6587", topic: "\u5468\u672B\u5E26\u670B\u53CB\u6765\u5403\uFF0C\u600E\u4E48\u70B9\u66F4\u5212\u7B97", ref: "@\u672C\u5730\u751F\u6D3B\u5BB6" },
      { day: "\u5468\u65E5", type: "\u590D\u76D8", topic: "\u8FD9\u5468\u6700\u53D7\u6B22\u8FCE\u7684\u4E00\u9053\u83DC", ref: "@\u5C0F\u5E97\u7ECF\u8425\u7B14\u8BB0" }
    ]);
    const [weekStart, setWeekStart] = React.useState("2026-05-18");
    const [showWeekPicker, setShowWeekPicker] = React.useState(false);
    const [reportVariant, setReportVariant] = React.useState(0);
    const [copied, setCopied] = React.useState("");
    const [liked, setLiked] = React.useState(false);
    const [toast, setToast] = React.useState("");
    const [stage, setStage] = React.useState(0);
    const [followUps, setFollowUps] = React.useState([]);
    const [activePreviewSection, setActivePreviewSection] = React.useState("\u5B9A\u4F4D");
    const [strategyDoc, setStrategyDoc] = React.useState(null);
    const [pendingFiles, setPendingFiles] = React.useState([]);
    const [quickLink, setQuickLink] = React.useState("");
    const [analysisComplete, setAnalysisComplete] = React.useState(false);
    const [calendarModalOpen, setCalendarModalOpen] = React.useState(false);
    const [assetConfirmed, setAssetConfirmed] = React.useState(false);
    const fileInputRef = React.useRef(null);
    const scrollRef = React.useRef(null);
    const contentRef = React.useRef(null);
    const endRef = React.useRef(null);
    const revealTimersRef = React.useRef([]);
    const shouldFollowScrollRef = React.useRef(true);
    const chatMaxWidth = step >= 2 ? 760 : 720;
    const analysisBullets = [
      { label: "\u8C03\u7814\u540C\u8D5B\u9053\u5934\u90E8\u8D26\u53F7", text: "\u6211\u5148\u770B\u4E86\u672C\u5730\u996D\u5E97\u3001\u63A2\u5E97\u548C\u793E\u533A\u5348\u9910\u8D26\u53F7\u7684\u5C01\u9762\u3001\u6807\u9898\u548C\u8BC4\u8BBA\u533A\u9AD8\u9891\u95EE\u9898\u3002" },
      { label: "\u63D0\u53D6\u7528\u6237\u75DB\u70B9", text: "\u7528\u6237\u6700\u6015\u7F51\u7EA2\u5E97\u8E29\u96F7\u3001\u6392\u961F\u4E45\u3001\u4EF7\u683C\u4E0D\u900F\u660E\uFF0C\u6240\u4EE5\u5185\u5BB9\u5FC5\u987B\u5148\u7ED9\u53EF\u6267\u884C\u5EFA\u8BAE\u3002" },
      { label: "\u5BFB\u627E\u5DEE\u5F02\u5316\u673A\u4F1A", text: "\u4F60\u7684\u673A\u4F1A\u4E0D\u662F\u6CDB\u63A2\u5E97\uFF0C\u800C\u662F\u628A\u300C\u9644\u8FD1\u4EBA\u771F\u5B9E\u590D\u5403\u300D\u548C\u300C\u4E3B\u7406\u4EBA\u8BA4\u771F\u996D\u300D\u8BB2\u7A33\u5B9A\u3002" }
    ];
    const steps = [
      { id: 1, label: "\u8F93\u5165\u7EBF\u7D22" },
      { id: 2, label: "\u8D26\u53F7\u5B9A\u4F4D" },
      { id: 3, label: "\u8FD0\u8425\u8BA1\u5212" },
      { id: 4, label: "\u5185\u5BB9\u6392\u671F" }
    ];
    const reports = [
      {
        names: ["\u5DF7\u53E3\u6696\u80C3\u5C0F\u9986", "\u9644\u8FD1\u4EBA\u7684\u5BB6\u5E38\u996D", "\u4E0B\u73ED\u6765\u5403\u4E00\u53E3"],
        keywords: ["\u4EB2\u5207\u4F46\u4E0D\u6CB9\u817B", "\u61C2\u672C\u5730\u751F\u6D3B", "\u771F\u5B9E\u4E3B\u7406\u4EBA", "\u7A33\u5B9A\u597D\u5403"],
        phrases: ["\u4ECA\u5929\u8FD9\u7897\u996D\uFF0C\u9002\u5408\u4E0B\u73ED\u540E\u6765\u4E00\u53E3\u3002", "\u7B2C\u4E00\u6B21\u6765\u4E0D\u77E5\u9053\u70B9\u4EC0\u4E48\uFF0C\u5148\u770B\u8FD9\u4E00\u7BC7\u3002", "\u4E0D\u662F\u7F51\u7EA2\u5E97\uFF0C\u4F46\u60F3\u628A\u6BCF\u987F\u996D\u8BA4\u771F\u505A\u597D\u3002"],
        bio: "\u6BCF\u5929\u8BA4\u771F\u505A\u4E00\u7897\u6709\u70DF\u706B\u6C14\u7684\u5BB6\u5E38\u996D\uFF0C\u7ED9\u9644\u8FD1\u4EBA\u4E00\u4E2A\u4E0D\u7528\u7EA0\u7ED3\u7684\u5403\u996D\u9009\u62E9\u3002",
        pillars: ["\u62DB\u724C\u83DC\u6545\u4E8B", "\u5348\u9910\u4E0D\u8E29\u96F7", "\u8001\u677F\u7684\u4E00\u5929", "\u771F\u5B9E\u987E\u5BA2\u53CD\u9988", "\u5468\u672B\u670B\u53CB\u5C40\u83DC\u5355"],
        bloggers: ["@\u672C\u5730\u5403\u559D\u6307\u5357", "@\u8857\u89D2\u5C0F\u5E97\u65E5\u8BB0", "@\u57CE\u5E02\u5348\u9910\u7814\u7A76\u6240"],
        covers: ["\u6696\u8272\u81EA\u7136\u5149 + \u83DC\u54C1\u8FD1\u666F + \u5927\u7559\u767D\u6807\u9898", "\u5E97\u95E8\u53E3 / \u9910\u684C / \u540E\u53A8\u7EC6\u8282\u4E09\u56FE\u62FC\u8D34", "\u4EBA\u7269\u624B\u90E8\u5165\u955C\uFF0C\u5F31\u5316\u6446\u62CD\u611F"]
      },
      {
        names: ["\u4ECA\u5929\u5403\u6696\u80C3\u996D", "\u793E\u533A\u996D\u70B9\u7814\u7A76\u6240", "\u5C0F\u9986\u8BA4\u771F\u996D"],
        keywords: ["\u9760\u8C31\u63A8\u8350", "\u90BB\u91CC\u611F", "\u4EF7\u683C\u53CB\u597D", "\u4E0B\u73ED\u6CBB\u6108"],
        phrases: ["\u8FD9\u4E0D\u662F\u63A2\u5E97\u5E7F\u544A\uFF0C\u662F\u9644\u8FD1\u4EBA\u771F\u7684\u4F1A\u590D\u5403\u7684\u83DC\u5355\u3002", "\u5982\u679C\u4F60\u53EA\u6709 30 \u5206\u949F\u5403\u5348\u996D\uFF0C\u53EF\u4EE5\u8FD9\u4E48\u70B9\u3002", "\u5C0F\u5E97\u6700\u52A8\u4EBA\u7684\u5730\u65B9\uFF0C\u662F\u6BCF\u5929\u90FD\u7A33\u5B9A\u3002"],
        bio: "\u8BB0\u5F55\u4E00\u5BB6\u793E\u533A\u5C0F\u9986\u7684\u65E5\u5E38\u83DC\u5355\u3001\u771F\u5B9E\u5BA2\u4EBA\u548C\u8BA9\u4EBA\u5B89\u5FC3\u7684\u5BB6\u5E38\u5473\u3002",
        pillars: ["30 \u5206\u949F\u5348\u9910\u65B9\u6848", "\u590D\u5403\u83DC\u5355", "\u5C0F\u5E97\u5E55\u540E", "\u672C\u5468\u65B0\u54C1", "\u9644\u8FD1\u751F\u6D3B\u8DEF\u7EBF"],
        bloggers: ["@\u901A\u52E4\u5348\u9910\u5730\u56FE", "@\u5C0F\u5E97\u89C2\u5BDF\u5458", "@\u9644\u8FD1\u751F\u6D3B\u624B\u518C"],
        covers: ["\u6D45\u8272\u684C\u9762 + \u4FEF\u62CD\u5957\u9910 + \u624B\u5199\u611F\u6807\u9898", "\u8001\u677F\u51FA\u955C + \u83DC\u54C1\u7279\u5199 + \u771F\u5B9E\u73AF\u5883", "\u4F4E\u9971\u548C\u6696\u8272\uFF0C\u5F3A\u8C03\u5E72\u51C0\u548C\u53EF\u4FE1"]
      }
    ];
    const report = reports[reportVariant % reports.length];
    const reportDraft = React.useMemo(() => ({
      names: [...report.names],
      keywords: [...report.keywords],
      phrases: [...report.phrases],
      bio: report.bio,
      pillars: [...report.pillars],
      bloggers: [...report.bloggers],
      covers: [...report.covers]
    }), [reportVariant]);
    const [activeReport, setActiveReport] = React.useState(reportDraft);
    const [audienceTags, setAudienceTags] = React.useState(["25-38 \u5C81", "\u9644\u8FD1\u4E0A\u73ED\u65CF", "\u60C5\u4FA3\u7EA6\u996D", "\u5468\u672B\u805A\u9910"]);
    const [appearanceTags, setAppearanceTags] = React.useState(["\u771F\u5B9E\u4E3B\u7406\u4EBA", "\u540E\u53A8\u65E5\u5E38", "\u83DC\u54C1\u8FD1\u666F"]);
    const [marketTags, setMarketTags] = React.useState(["\u672C\u5730\u751F\u6D3B", "\u793E\u533A\u5468\u8FB9", "\u5C0F\u7EA2\u4E66\u641C\u7D22"]);
    React.useEffect(() => {
      revealTimersRef.current.forEach(window.clearTimeout);
      setStage(0);
      if (step === 2) setAnalysisComplete(false);
      const timers = [
        window.setTimeout(() => setStage(1), 180),
        window.setTimeout(() => setStage(2), 520),
        window.setTimeout(() => setStage(3), 900)
      ];
      revealTimersRef.current = timers;
      return () => timers.forEach(window.clearTimeout);
    }, [step]);
    const scrollToBottom = React.useCallback((behavior = "smooth", force = false) => {
      const node = scrollRef.current;
      if (!node) return;
      if (!force && !shouldFollowScrollRef.current && !isNearScrollBottom(node)) return;
      window.requestAnimationFrame(() => {
        scrollNodeToBottom(node, behavior);
        shouldFollowScrollRef.current = isNearScrollBottom(node, 140);
      });
    }, []);
    React.useEffect(() => {
      shouldFollowScrollRef.current = true;
      const t = window.setTimeout(() => scrollToBottom("smooth", true), 80);
      return () => window.clearTimeout(t);
    }, [step, sentIntro, goalSelections.length, platformSelections.length, followUps.length, attachments.length, scrollToBottom]);
    React.useEffect(() => {
      const node = scrollRef.current;
      if (!node || !contentRef.current) return void 0;
      const onScroll = () => {
        shouldFollowScrollRef.current = isNearScrollBottom(node, 140);
      };
      node.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
      const observer = new MutationObserver(() => {
        scrollToBottom("auto");
      });
      const resizeObserver = new ResizeObserver(() => {
        scrollToBottom("auto");
      });
      observer.observe(contentRef.current, { childList: true, subtree: true, characterData: true });
      resizeObserver.observe(contentRef.current);
      return () => {
        node.removeEventListener("scroll", onScroll);
        observer.disconnect();
        resizeObserver.disconnect();
      };
    }, [scrollToBottom]);
    const canAdvanceStep1 = sentIntro && goalSelections.length > 0 && platformSelections.length > 0;
    const isReadyToDeliver = step >= 4;
    const persistDraft = (nextStep = step) => {
      const payload = {
        step: nextStep,
        attachments,
        rawInput,
        sentIntro,
        goalSelections,
        platformSelections,
        diagnosisText,
        activeReport,
        pillars,
        calendar,
        weekStart,
        reportVariant,
        followUps,
        quickLink
      };
      window.localStorage?.setItem(PLAN_STORAGE_KEY, JSON.stringify(payload));
      setToast("\u5DF2\u6682\u5B58");
      window.setTimeout(() => setToast(""), 1200);
      onBackHome();
    };
    const copyPlan = (text) => {
      setCopied(text);
      navigator.clipboard?.writeText(text).catch(() => {
      });
      window.setTimeout(() => setCopied(""), 1200);
    };
    const downloadPlan = () => {
      const blob = new Blob([buildPlanExportText({
        diagnosisText,
        persona: activeReport || persona,
        pillars,
        calendar
      })], { type: "text/markdown;charset=utf-8" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "nori-account-plan.md";
      a.click();
      URL.revokeObjectURL(url);
      setToast("\u5DF2\u4E0B\u8F7D\u6587\u6863");
      window.setTimeout(() => setToast(""), 1200);
    };
    const completePlan = () => {
      const finalPersona = activeReport || persona;
      onComplete({
        topic: `\u5C0F\u7EA2\u4E66\u56FE\u6587\uFF1A${calendar[0]?.topic || "\u8D26\u53F7\u89C4\u5212"}`,
        platform: platformSelections[0] || "\u5C0F\u7EA2\u4E66",
        positioning: diagnosisText.position,
        persona: {
          name: finalPersona.names ? finalPersona.names[0] : finalPersona.name,
          bio: finalPersona.bio,
          keywords: finalPersona.keywords?.join ? finalPersona.keywords.join("\u3001") : finalPersona.keywords,
          tone: finalPersona.phrases ? finalPersona.phrases.join(" / ") : finalPersona.tone,
          cover: finalPersona.covers ? finalPersona.covers[0] : finalPersona.cover
        },
        pillars
      });
      clearPlanDraftStorage();
    };
    const startFirstContent = () => {
      const finalPersona = activeReport || persona;
      onComplete({
        topic: `\u5C0F\u7EA2\u4E66\u56FE\u6587\uFF1A${calendar[0]?.topic || "\u8D26\u53F7\u89C4\u5212"}`,
        platform: platformSelections[0] || "\u5C0F\u7EA2\u4E66",
        positioning: diagnosisText.position,
        persona: {
          name: finalPersona.names ? finalPersona.names[0] : finalPersona.name,
          bio: finalPersona.bio,
          keywords: finalPersona.keywords?.join ? finalPersona.keywords.join("\u3001") : finalPersona.keywords,
          tone: finalPersona.phrases ? finalPersona.phrases.join(" / ") : finalPersona.tone,
          cover: finalPersona.covers ? finalPersona.covers[0] : finalPersona.cover
        },
        pillars,
        calendar
      });
      clearPlanDraftStorage();
    };
    const toggleMulti = (value, setter) => {
      setter((prev) => prev.includes(value) ? prev.filter((item) => item !== value) : [...prev, value]);
    };
    const restartRevealSequence = React.useCallback(() => {
      revealTimersRef.current.forEach(window.clearTimeout);
      setStage(0);
      const timers = [
        window.setTimeout(() => setStage(1), 220),
        window.setTimeout(() => setStage(2), 680),
        window.setTimeout(() => setStage(3), 1180)
      ];
      revealTimersRef.current = timers;
    }, []);
    const contentProfiles = [
      { title: "\u8D26\u53F7\u5B9A\u4F4D", value: diagnosisText.position },
      { title: "\u76EE\u6807\u53D7\u4F17", value: diagnosisText.audience },
      { title: "\u5185\u5BB9\u65B9\u5411", value: diagnosisText.directions },
      { title: "\u5BF9\u6807\u8D26\u53F7", value: diagnosisText.benchmarks },
      { title: "\u5DEE\u5F02\u5316\u5356\u70B9", value: diagnosisText.selling }
    ];
    const sendPlanningMessage = (text) => {
      const quickLinkText = !sentIntro && /^https?:\/\//i.test(quickLink.trim()) ? quickLink.trim() : "";
      if (!text.trim() && pendingFiles.length === 0 && !quickLinkText) return;
      const now = Date.now();
      const selectedFiles = pendingFiles.map((item) => item.file || item);
      const fileAttachments = selectedFiles.map((file) => ({
        type: file.type?.startsWith("image/") ? "image" : file.type?.startsWith("video/") ? "video" : "file",
        label: file.name,
        value: `${file.name} \xB7 ${Math.max(1, Math.round(file.size / 1024))}KB`,
        preview: file.type?.startsWith("image/") ? URL.createObjectURL(file) : null
      }));
      if (fileAttachments.length) {
        setAttachments((list) => [...list, ...fileAttachments]);
        pendingFiles.forEach((item) => item.preview && URL.revokeObjectURL(item.preview));
        setPendingFiles([]);
      }
      const linkAttachment = quickLinkText ? { type: "link", label: "\u5E97\u94FA\u94FE\u63A5", value: quickLinkText, thumb: PLANNING_ASSET_THUMBS[2] } : null;
      if (linkAttachment) {
        setAttachments((list) => list.some((item) => item.value === quickLinkText) ? list : [...list, linkAttachment]);
      }
      const userText = text.trim() || quickLinkText || `\u5DF2\u4E0A\u4F20 ${fileAttachments.length} \u4E2A\u6587\u4EF6`;
      if (!sentIntro) {
        setRawInput(userText);
        setAssetConfirmed(false);
        setSentIntro(true);
        restartRevealSequence();
        return;
      }
      setFollowUps((list) => [
        ...list,
        { id: now, from: "user", text: fileAttachments.length ? `${userText}
${fileAttachments.map((item) => item.label).join("\u3001")}` : userText },
        { id: now + 1, from: "nori", text: step < 5 ? "\u6536\u5230\uFF0C\u6211\u4F1A\u628A\u8FD9\u6761\u8865\u5145\u8FDB\u8D26\u53F7\u89C4\u5212\u91CC\u3002\u4F60\u4E5F\u53EF\u4EE5\u7EE7\u7EED\u53D1\u94FE\u63A5\u3001\u622A\u56FE\u6216\u76F4\u63A5\u63CF\u8FF0\u3002" : "\u6536\u5230\uFF0C\u6211\u4F1A\u6309\u8FD9\u4E2A\u65B9\u5411\u66F4\u65B0\u53F3\u4FA7\u6587\u6863\u9884\u89C8\u91CC\u7684\u5185\u5BB9\u3002" }
      ]);
    };
    const pasteQuickLink = () => {
      const link = quickLink.trim() || "https://www.meituan.com/shop/\u4E0A\u6D77\u6696\u80C3\u5C0F\u9986";
      setQuickLink(link);
      setRawInput(link);
      setAttachments((list) => list.some((item) => item.value === link) ? list : [...list, { type: "link", label: "\u7F8E\u56E2\u5E97\u94FA\u94FE\u63A5", value: link, thumb: PLANNING_ASSET_THUMBS[2] }]);
    };
    return /* @__PURE__ */ React.createElement("div", { style: {
      height: "100%",
      minHeight: 0,
      width: "100%",
      display: "flex",
      flexDirection: "column",
      background: "linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)",
      color: T.navy,
      overflow: "hidden",
      fontFamily: T.fontSans
    } }, /* @__PURE__ */ React.createElement("header", { style: {
      height: isMobile ? "auto" : 56,
      padding: isMobile ? "12px 16px" : "0 24px",
      display: "flex",
      alignItems: isMobile ? "stretch" : "center",
      justifyContent: "space-between",
      gap: 14,
      flexDirection: isMobile ? "column" : "row",
      borderBottom: `1px solid ${T.hairlineSoft}`,
      background: "rgba(250,252,254,.78)",
      backdropFilter: "blur(18px) saturate(1.16)",
      flexShrink: 0
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 12, minWidth: 0 } }, /* @__PURE__ */ React.createElement("button", { onClick: onBackHome, style: iconBtnStyle() }, /* @__PURE__ */ React.createElement(Icon, { name: "arrowLeft", size: 16, color: T.navyMid })), /* @__PURE__ */ React.createElement("div", { style: { minWidth: 0 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13.5, fontWeight: 670, color: T.navy } }, "\u8D26\u53F7\u89C4\u5212"))), /* @__PURE__ */ React.createElement("div", null)), /* @__PURE__ */ React.createElement("div", { style: { flex: 1, minHeight: 0, display: "flex", overflow: "hidden" } }, /* @__PURE__ */ React.createElement("main", { style: { flex: 1, minWidth: 0, display: "flex", flexDirection: "column" } }, /* @__PURE__ */ React.createElement("div", { ref: scrollRef, style: { flex: 1, minHeight: 0, overflowY: "auto", padding: isMobile ? "22px 0 20px" : "28px 0 24px" } }, /* @__PURE__ */ React.createElement("div", { ref: contentRef, style: {
      maxWidth: chatMaxWidth,
      margin: "0 auto",
      padding: isMobile ? "0 16px" : "0 30px",
      display: "flex",
      flexDirection: "column",
      gap: 22
    } }, toast && /* @__PURE__ */ React.createElement("div", { style: {
      alignSelf: "flex-start",
      display: "inline-flex",
      alignItems: "center",
      gap: 8,
      padding: "9px 13px",
      borderRadius: 999,
      background: "rgba(255,255,255,.82)",
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: "0 10px 26px rgba(14,14,44,.06)",
      color: T.navyMid,
      fontSize: 12.5,
      fontWeight: 650
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 13 }), " ", toast), /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 0 }, /* @__PURE__ */ React.createElement(PlanningPlainReply, null, /* @__PURE__ */ React.createElement("p", { style: { margin: "0 0 8px", color: T.navy, fontSize: 14.1, lineHeight: 1.62, fontWeight: 650 } }, "\u6211\u662F Nori\uFF0C\u53EF\u4EE5\u5E2E\u4F60\u4EA4\u4ED8\u4E00\u4EFD\u300C\u8D26\u53F7\u5B9A\u4F4D + \u8FD0\u8425\u8BA1\u5212 + \u5185\u5BB9\u6392\u671F\u300D\u3002"), /* @__PURE__ */ React.createElement("p", { style: { margin: 0 } }, "\u4F60\u53EF\u4EE5\u53D1\u4E3B\u9875\u94FE\u63A5\u3001\u7ADE\u54C1\u94FE\u63A5\u3001\u622A\u56FE\u3001\u83DC\u5355 / \u4EA7\u54C1\u6587\u4EF6\uFF0C\u4E5F\u53EF\u4EE5\u76F4\u63A5\u7528\u4E00\u53E5\u8BDD\u63CF\u8FF0\u4F60\u60F3\u505A\u4EC0\u4E48\u3002"))), !sentIntro && /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 120 }, /* @__PURE__ */ React.createElement(
      PlanningStartPanel,
      {
        quickLink,
        setQuickLink,
        onUploadImage: () => fileInputRef.current?.click(),
        onUploadDoc: () => fileInputRef.current?.click(),
        onPasteLink: pasteQuickLink
      }
    )), attachments.length > 0 && !sentIntro && /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 200 }, /* @__PURE__ */ React.createElement(PlanningUploadedAssetStrip, { attachments, onAddMore: () => fileInputRef.current?.click() })), sentIntro && /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 80 }, /* @__PURE__ */ React.createElement(Bubble, { from: "user" }, rawInput || attachments.map((item) => item.label || item.value || item.type).join("\u3001") || "\u6211\u5DF2\u7ECF\u63D0\u4F9B\u4E86\u4E00\u4E9B\u8D26\u53F7\u7EBF\u7D22")), sentIntro && step === 1 && /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 100 }, /* @__PURE__ */ React.createElement(
      AgentStepSequence,
      {
        resetKey: "planning-intro-response",
        parseMessages: ["\u6B63\u5728\u67E5\u770B\u4F60\u63D0\u4F9B\u7684\u8D44\u6599", "\u89E3\u6790\u4E2D", "\u6B63\u5728\u63D0\u70BC\u5E97\u94FA\u7EBF\u7D22"],
        reply: /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 14.1, fontWeight: 650 } }, "\u6211\u5148\u770B\u5230\u4E86\u4F60\u7684\u5E97\u94FA\u94FE\u63A5\u3001\u56FE\u7247\u548C\u8BC4\u4EF7\uFF0C\u8FD9\u4E9B\u5DF2\u7ECF\u8DB3\u591F\u8BA9\u6211\u5F00\u59CB\u5224\u65AD\u4F60\u9002\u5408\u4EC0\u4E48\u6837\u7684\u8D26\u53F7\u3002"), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyMid, fontSize: 12.9, lineHeight: 1.72 } }, "\u6211\u4F1A\u5148\u505A\u7ADE\u54C1\u4E0E\u884C\u4E1A\u5206\u6790\uFF0C\u518D\u7ED9\u4F60\u8D26\u53F7\u5B9A\u4F4D\uFF0C\u907F\u514D\u548C\u540C\u8D5B\u9053\u7684\u5185\u5BB9\u957F\u5F97\u592A\u50CF\u3002\u6211\u9700\u8981\u5148\u77E5\u9053\u4E24\u4E2A\u95EE\u9898\u3002")),
        card: /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(PlanningUploadedAssetStrip, { attachments, onAddMore: () => fileInputRef.current?.click(), onConfirm: () => setAssetConfirmed(true) }), assetConfirmed && /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(PlanningPlainReply, null, "\u4E86\u89E3\u4E86\u4F60\u7684\u54C1\u724C / \u4E2A\u4EBA\u8D44\u4EA7\uFF0C\u8FD8\u6709\u4E24\u4E2A\u95EE\u9898\u9700\u8981\u63D0\u524D\u786E\u8BA4\u3002"), /* @__PURE__ */ React.createElement(
          AgentCardShell,
          {
            label: "Agent \u504F\u597D\u786E\u8BA4",
            icon: "target",
            title: "\u5148\u628A\u4E24\u4E2A\u5173\u952E\u95EE\u9898\u8BF4\u6E05\u695A",
            action: /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(2), disabled: !canAdvanceStep1, style: { ...planningActionButtonStyle(canAdvanceStep1 ? "primary" : "secondary"), opacity: canAdvanceStep1 ? 1 : 0.56, cursor: canAdvanceStep1 ? "pointer" : "not-allowed" } }, "\u4E0B\u4E00\u6B65", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 14 }))
          },
          /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 16 } }, /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 13.6, fontWeight: 700, marginBottom: 8 } }, "\u6700\u60F3\u7528\u793E\u5A92\u8D26\u53F7\u505A\u4EC0\u4E48\uFF1F"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexWrap: "wrap", gap: 8 } }, ["\u5F15\u6D41\u5230\u5E97", "\u54C1\u724C\u66DD\u5149", "\u7EBF\u4E0A\u5356\u8D27", "\u79EF\u7D2F\u53E3\u7891"].map((option) => /* @__PURE__ */ React.createElement(AgentChoice, { key: option, active: goalSelections.includes(option), multiple: true, onClick: () => toggleMulti(option, setGoalSelections) }, option)))), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navy, fontSize: 13.6, fontWeight: 700, marginBottom: 8 } }, "\u6700\u60F3\u5728\u54EA\u4E2A\u5E73\u53F0\u505A\uFF1F"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", flexWrap: "wrap", gap: 8 } }, ["\u5C0F\u7EA2\u4E66", "\u6296\u97F3", "\u89C6\u9891\u53F7", "\u516C\u4F17\u53F7"].map((option) => /* @__PURE__ */ React.createElement(AgentChoice, { key: option, active: platformSelections.includes(option), multiple: true, onClick: () => toggleMulti(option, setPlatformSelections) }, option)))))
        )))
      }
    )), step >= 2 && /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 100 }, /* @__PURE__ */ React.createElement(PlanningUserSummary, null, `\u76EE\u6807\uFF1A${goalSelections.join("\u3001") || "\u5F85\u786E\u8BA4"}
\u5E73\u53F0\uFF1A${platformSelections.join("\u3001") || "\u5F85\u786E\u8BA4"}`)), step >= 2 && !analysisComplete && /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 200 }, /* @__PURE__ */ React.createElement(
      AgentStepSequence,
      {
        resetKey: "planning-position-analysis",
        parseMessages: ["\u6B63\u5728\u5BF9\u7167\u540C\u8D5B\u9053\u8D26\u53F7", "\u89E3\u6790\u4E2D", "\u6B63\u5728\u63D0\u70BC\u5DEE\u5F02\u5316\u673A\u4F1A"],
        reply: "\u6211\u6B63\u5728\u7ED3\u5408\u4F60\u7684\u8D44\u6599\u4E0E\u540C\u8D5B\u9053\u5185\u5BB9\u505A\u5BF9\u7167\uFF0C\u5148\u627E\u51FA\u7528\u6237\u771F\u6B63\u4F1A\u6536\u85CF\u3001\u4F1A\u5230\u5E97\u7684\u7406\u7531\uFF0C\u518D\u786E\u5B9A\u5B9A\u4F4D\u3002",
        card: /* @__PURE__ */ React.createElement(
          PlanningResearchFlow,
          {
            bullets: analysisBullets,
            conclusion: "\u5EFA\u8BAE\u628A\u5185\u5BB9\u5B9A\u4F4D\u5728\u300C\u9644\u8FD1\u4EBA\u771F\u5B9E\u590D\u5403 + \u4E3B\u7406\u4EBA\u8BA4\u771F\u996D\u300D\uFF0C\u5148\u5EFA\u7ACB\u4FE1\u4EFB\uFF0C\u518D\u653E\u5927\u5230\u5230\u5E97\u51B3\u7B56\u3002",
            isMobile,
            onComplete: () => setAnalysisComplete(true),
            showThinking: false
          }
        )
      }
    )), step >= 2 && analysisComplete && /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 120 }, /* @__PURE__ */ React.createElement(PlanningPlainReply, null, "\u4E0B\u9762\u662F\u6211\u6574\u7406\u51FA\u7684\u8D26\u53F7\u5B9A\u4F4D\u3002\u5B83\u4F1A\u540C\u6B65\u5230\u300C\u6211\u7684 \xB7 \u8D26\u53F7\u5B9A\u4F4D\u300D\uFF0C\u5E76\u7528\u4E8E\u540E\u7EED\u751F\u6210\u5185\u5BB9\u3002"), /* @__PURE__ */ React.createElement(
      PlanningSkeletonMerge,
      {
        diagnosisText,
        setDiagnosisText,
        audienceTags,
        setAudienceTags,
        appearanceTags,
        setAppearanceTags,
        marketTags,
        setMarketTags,
        pillars,
        setPillars,
        isMobile,
        action: /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(3), style: { ...planningActionButtonStyle("primary") } }, "\u7EE7\u7EED\u751F\u6210\u8FD0\u8425\u8BA1\u5212", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 14 }))
      }
    )), step >= 3 && /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 120 }, /* @__PURE__ */ React.createElement(
      AgentStepSequence,
      {
        resetKey: "planning-strategy",
        parseMessages: ["\u6B63\u5728\u751F\u6210\u4F60\u7684\u8FD0\u8425\u8BA1\u5212", "\u89E3\u6790\u4E2D", "\u6B63\u5728\u6BD4\u8F83\u4E09\u5957\u8D26\u53F7\u6253\u6CD5"],
        parseConclusion: "\u5DF2\u751F\u6210\u4E09\u5957\u8FD0\u8425\u8BA1\u5212",
        reply: "\u8FD9\u662F\u4F60\u7684\u8FD0\u8425\u8BA1\u5212\uFF0C\u6211\u66F4\u63A8\u8350\u7B2C\u4E00\u5957\u54E6\u3002",
        card: /* @__PURE__ */ React.createElement(
          PlanningStrategyCards,
          {
            isMobile,
            activeReport,
            pillars,
            onOpenDoc: setStrategyDoc,
            onConfirm: () => setStep(4)
          }
        )
      }
    )), step >= 4 && /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 120 }, /* @__PURE__ */ React.createElement(
      AgentStepSequence,
      {
        resetKey: "planning-calendar",
        parseMessages: ["\u6B63\u5728\u751F\u6210\u4F60\u7684\u5185\u5BB9\u65E5\u5386", "\u89E3\u6790\u4E2D", "\u6B63\u5728\u6574\u7406\u4E00\u5468\u6392\u671F"],
        parseConclusion: "\u6B63\u5728\u6574\u7406\u4E00\u5468\u6392\u671F",
        reply: "\u8FD9\u662F\u4F60\u7B2C\u4E00\u5468\u7684\u5185\u5BB9\u6392\u671F\u3002\u8FD9\u4EFD\u5185\u5BB9\u6392\u671F\u4F1A\u540C\u6B65\u5230\u300C\u6211\u7684 \xB7 \u5185\u5BB9\u65E5\u5386\u300D\uFF0C\u786E\u8BA4\u540E\u53EF\u4EE5\u76F4\u63A5\u5F00\u59CB\u751F\u6210\u7B2C\u4E00\u7BC7\u3002",
        card: /* @__PURE__ */ React.createElement(
          PlanningCalendarPreviewCard,
          {
            calendar,
            onView: () => setCalendarModalOpen(true),
            onGenerate: startFirstContent
          }
        )
      }
    )), followUps.map((item) => item.from === "user" ? /* @__PURE__ */ React.createElement(PlanningReveal, { key: item.id, show: true, delay: 60 }, /* @__PURE__ */ React.createElement(Bubble, { from: "user" }, item.text)) : /* @__PURE__ */ React.createElement(PlanningReveal, { key: item.id, show: true, delay: 140 }, /* @__PURE__ */ React.createElement(PlanningPlainReply, null, item.text))), /* @__PURE__ */ React.createElement("div", { ref: endRef, style: { height: 1 } }))), /* @__PURE__ */ React.createElement(
      PlanningCalendarModal,
      {
        open: calendarModalOpen,
        onClose: () => setCalendarModalOpen(false),
        onGenerate: startFirstContent
      },
      /* @__PURE__ */ React.createElement(
        PlanningCalendarBoard,
        {
          calendar,
          setCalendar,
          weekStart,
          setWeekStart,
          isMobile,
          wide: true
        }
      )
    ), /* @__PURE__ */ React.createElement("div", { style: {
      padding: isMobile ? "8px 16px 14px" : "8px 24px 16px",
      background: "linear-gradient(to top, rgba(250,252,254,.98) 62%, rgba(250,252,254,0))",
      flexShrink: 0
    } }, /* @__PURE__ */ React.createElement("div", { style: { maxWidth: chatMaxWidth, margin: "0 auto", padding: isMobile ? 0 : "0 30px" } }, /* @__PURE__ */ React.createElement(
      "input",
      {
        ref: fileInputRef,
        type: "file",
        multiple: true,
        accept: "image/*,video/*,.pdf,.doc,.docx,.txt,.md,.csv",
        onChange: (e) => {
          const files = Array.from(e.target.files || []).map((file) => ({
            file,
            preview: file.type?.startsWith("image/") ? URL.createObjectURL(file) : null
          }));
          setPendingFiles((list) => [...list, ...files]);
          e.target.value = "";
        },
        style: { display: "none" }
      }
    ), /* @__PURE__ */ React.createElement(
      ChatComposer,
      {
        placeholder: "\u7EE7\u7EED\u8DDF Nori \u8BF4\uFF1A\u8865\u5145\u8D44\u6599\u3001\u4FEE\u6539\u5B9A\u4F4D\u3001\u8C03\u6574\u65E5\u5386...",
        onSend: sendPlanningMessage,
        onAttach: () => fileInputRef.current?.click(),
        canSendExtra: pendingFiles.length > 0,
        attachmentCount: pendingFiles.length,
        attachmentFiles: pendingFiles.map((item) => ({ name: item.file?.name || item.name, type: item.file?.type || item.type, preview: item.preview })),
        onRemoveAttachment: (index) => setPendingFiles((list) => {
          const next = list.filter((_, i) => i !== index);
          const removed = list[index];
          if (removed?.preview) URL.revokeObjectURL(removed.preview);
          return next;
        })
      }
    ), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 9, textAlign: "center", color: T.navyLight, fontSize: 11.5, lineHeight: 1.45 } }, "Nori is AI and can make mistakes. Please double-check responses.")))), false), modalType && /* @__PURE__ */ React.createElement(InputMethodModal, { type: modalType, onClose: () => setModalType(null), onConfirm: (att) => {
      setAttachments((list) => [...list, att]);
      if (att.type === "text") setRawInput(att.value);
      setModalType(null);
      setSentIntro(true);
    } }), /* @__PURE__ */ React.createElement(PlanningStrategyDocModal, { strategy: strategyDoc, onClose: () => setStrategyDoc(null) }));
    return /* @__PURE__ */ React.createElement("div", { style: {
      height: "100%",
      minHeight: 0,
      width: "100%",
      display: "flex",
      flexDirection: "column",
      background: "linear-gradient(180deg, #FCFDFE 0%, #F4F7FA 100%)",
      color: T.navy,
      overflow: "hidden"
    } }, /* @__PURE__ */ React.createElement("header", { style: {
      position: "sticky",
      top: 0,
      zIndex: 8,
      display: "block",
      gap: 14,
      padding: isMobile ? "14px 16px 10px" : "18px 24px 12px",
      background: "rgba(252,253,254,.82)",
      backdropFilter: "blur(16px) saturate(1.12)"
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      maxWidth: 1120,
      margin: "0 auto",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: 14
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: isMobile ? 12 : 22, minWidth: 0 } }, /* @__PURE__ */ React.createElement("button", { onClick: onBackHome, style: {
      border: "none",
      background: "transparent",
      color: T.navyMid,
      cursor: "pointer",
      display: "inline-flex",
      alignItems: "center",
      gap: 8,
      fontSize: 13.5,
      fontWeight: 650,
      padding: "6px 2px",
      flexShrink: 0
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "arrowLeft", size: 16 }), "\u9000\u51FA"), /* @__PURE__ */ React.createElement(PlanningCompactProgress, { steps, step, isMobile })), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, flexShrink: 0 } }, /* @__PURE__ */ React.createElement("button", { onClick: () => persistDraft(step), style: {
      height: 34,
      padding: "0 13px",
      borderRadius: 12,
      border: `1px solid ${T.hairlineSoft}`,
      background: "rgba(255,255,255,.78)",
      color: T.navyMid,
      cursor: "pointer",
      fontSize: 12.5,
      fontWeight: 650
    } }, "\u6682\u65F6\u4FDD\u5B58"), !isMobile && /* @__PURE__ */ React.createElement("div", { style: { fontSize: 12.5, color: T.navyLight, fontFamily: T.fontMono } }, "\u7B2C ", step, " / ", steps.length, " \u6B65")))), /* @__PURE__ */ React.createElement("main", { style: {
      flex: 1,
      minHeight: 0,
      overflowY: "auto",
      overflowX: "hidden",
      WebkitOverflowScrolling: "touch",
      padding: isMobile ? "4px 16px 34px" : "6px 24px 40px"
    }, ref: scrollRef }, /* @__PURE__ */ React.createElement("div", { style: { maxWidth: 1120, margin: "0 auto" } }, toast && /* @__PURE__ */ React.createElement("div", { style: {
      position: "sticky",
      top: 12,
      zIndex: 5,
      marginBottom: 12,
      display: "inline-flex",
      alignItems: "center",
      gap: 8,
      padding: "10px 14px",
      borderRadius: 999,
      background: "rgba(255,255,255,.82)",
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: "0 10px 26px rgba(14,14,44,.06)",
      color: T.navyMid,
      fontSize: 12.5,
      fontWeight: 650
    } }, /* @__PURE__ */ React.createElement(Icon, { name: "check", size: 13 }), " ", toast), step >= 1 && /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 18 } }, /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 0 }, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 8, fontSize: 16, fontWeight: 680 } }, "\u5148\u804A\u804A\uFF0C\u4F60\u624B\u4E0A\u6709\u70B9\u4EC0\u4E48\uFF1F"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13.5 } }, "\u4E09\u79CD\u65B9\u5F0F\u53EF\u4EE5\u540C\u65F6\u4F7F\u7528\uFF0C\u7ED9\u7684\u4FE1\u606F\u8D8A\u5168\uFF0CNori \u8BFB\u5F97\u8D8A\u51C6\u3002"))), /* @__PURE__ */ React.createElement(PlanningReveal, { show: stage >= 1, delay: 0 }, /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u8F93\u5165\u65B9\u5F0F", style: { padding: isMobile ? 16 : 20 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "repeat(3, minmax(0, 1fr))", gap: 10, marginBottom: 12 } }, /* @__PURE__ */ React.createElement(PlanningOption, { icon: "link", title: "\u7C98\u8D34\u94FE\u63A5", desc: "\u5E97\u94FA / \u4E3B\u9875 / \u6587\u7AE0", active: attachments.some((item) => item.type === "link"), onClick: () => setModalType("link") }), /* @__PURE__ */ React.createElement(PlanningOption, { icon: "image", title: "\u4E0A\u4F20\u56FE\u7247", desc: "\u4EA7\u54C1\u56FE / \u622A\u56FE", active: attachments.some((item) => item.type === "image"), onClick: () => setModalType("image") }), /* @__PURE__ */ React.createElement(PlanningOption, { icon: "chat", title: "\u76F4\u63A5\u63CF\u8FF0", desc: "\u6211\u662F\u505A\u4EC0\u4E48\u7684", active: attachments.some((item) => item.type === "text"), onClick: () => setModalType("text") })), /* @__PURE__ */ React.createElement(
      PlanningComposerMulti,
      {
        attachments,
        text: rawInput,
        setText: setRawInput,
        onRemoveAttachment: (index) => setAttachments((list) => list.filter((_, i) => i !== index)),
        onSend: () => setSentIntro(true)
      }
    ))), /* @__PURE__ */ React.createElement(PlanningReveal, { show: stage >= 2 && sentIntro, delay: 0 }, /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u5148\u628A\u4E24\u4E2A\u5173\u952E\u95EE\u9898\u8BF4\u6E05\u695A", style: { padding: isMobile ? 16 : 20 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 18 } }, /* @__PURE__ */ React.createElement(
      PlanningChoiceGroup,
      {
        title: "\u6700\u60F3\u7528\u793E\u5A92\u8D26\u53F7\u505A\u4EC0\u4E48\uFF1F",
        hint: "\u53EF\u591A\u9009",
        options: ["\u5F15\u6D41\u5230\u5E97", "\u54C1\u724C\u66DD\u5149", "\u7EBF\u4E0A\u5356\u8D27", "\u79EF\u7D2F\u53E3\u7891"],
        selected: goalSelections,
        onToggle: (value) => toggleMulti(value, setGoalSelections),
        allowMultiple: true
      }
    ), /* @__PURE__ */ React.createElement(
      PlanningChoiceGroup,
      {
        title: "\u6700\u60F3\u5728\u54EA\u4E2A\u5E73\u53F0\u505A\uFF1F",
        hint: "\u53EF\u591A\u9009",
        options: ["\u5C0F\u7EA2\u4E66", "\u6296\u97F3", "\u89C6\u9891\u53F7", "\u516C\u4F17\u53F7"],
        selected: platformSelections,
        onToggle: (value) => toggleMulti(value, setPlatformSelections),
        allowMultiple: true
      }
    )))), step === 1 && /* @__PURE__ */ React.createElement(PlanningReveal, { show: stage >= 3 && sentIntro, delay: 0 }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "flex-end", gap: 10, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: onBackHome, style: { height: 40, padding: "0 14px", borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.78)", color: T.navyMid, cursor: "pointer", fontSize: 13, fontWeight: 650 } }, "\u9000\u51FA"), /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(2), disabled: !canAdvanceStep1, style: { height: 40, padding: "0 18px", borderRadius: 13, border: "none", background: canAdvanceStep1 ? T.navy : T.surface, color: canAdvanceStep1 ? T.white : T.navyLight, cursor: canAdvanceStep1 ? "pointer" : "not-allowed", fontSize: 13, fontWeight: 700, boxShadow: canAdvanceStep1 ? "0 12px 24px rgba(14,14,44,.14)" : "none" } }, "\u8FDB\u5165\u8D26\u53F7\u8BCA\u65AD")))), step >= 2 && /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 18 } }, /* @__PURE__ */ React.createElement(PlanningUserSummary, null, `\u6211\u63D0\u4F9B\u4E86 ${attachments.length || rawInput ? "\u8D26\u53F7\u7EBF\u7D22" : "\u57FA\u7840\u4FE1\u606F"}\u3002
\u76EE\u6807\uFF1A${goalSelections.join("\u3001") || "\u5F85\u786E\u8BA4"}
\u5E73\u53F0\uFF1A${platformSelections.join("\u3001") || "\u5F85\u786E\u8BA4"}`), /* @__PURE__ */ React.createElement(PlanningChatDivider, { label: "\u8D26\u53F7\u8BCA\u65AD" }), /* @__PURE__ */ React.createElement(PlanningReveal, { show: true, delay: 0 }, /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 8, fontSize: 16, fontWeight: 680 } }, "\u8BFB\u5B8C\u4E86\uFF0C\u8FD9\u662F\u6211\u770B\u5230\u7684\u4F60\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13.5 } }, "\u6BCF\u4E00\u9879\u90FD\u53EF\u4EE5\u76F4\u63A5\u7F16\u8F91\uFF0C\u6539\u5B8C Nori \u81EA\u52A8\u8BB0\u4F4F\u3002"))), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "repeat(2, minmax(0, 1fr))", gap: 14 } }, contentProfiles.map((item, index) => /* @__PURE__ */ React.createElement(
      PlanningReveal,
      {
        key: item.title,
        show: stage >= Math.min(index + 1, 3),
        delay: index * 80,
        style: { gridColumn: index === 4 && !isMobile ? "span 2" : "auto" }
      },
      /* @__PURE__ */ React.createElement(PlanningPanel, { title: item.title, style: { padding: 18 } }, /* @__PURE__ */ React.createElement(
        "textarea",
        {
          value: item.value,
          onChange: (e) => setDiagnosisText((prev) => ({ ...prev, [Object.keys(diagnosisText)[index]]: e.target.value })),
          rows: index < 2 ? 4 : 5,
          style: {
            width: "100%",
            border: `1px solid ${T.hairlineSoft}`,
            borderRadius: 14,
            background: "rgba(250,252,254,.76)",
            padding: 12,
            resize: "vertical",
            outline: "none",
            color: T.navyMid,
            fontSize: 13,
            lineHeight: 1.72,
            fontFamily: T.fontSans,
            boxShadow: `inset 0 0 0 1px ${T.hairlineSoft}`
          }
        }
      ))
    ))), step === 2 && /* @__PURE__ */ React.createElement(PlanningReveal, { show: stage >= 3, delay: 180 }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 10, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(1), style: { border: "none", background: "transparent", color: T.navyLight, cursor: "pointer", fontSize: 12.8, fontWeight: 650 } }, "\u8FD4\u56DE\u4E0A\u4E00\u6B65"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(3), style: { height: 40, padding: "0 18px", borderRadius: 13, border: "none", background: T.navy, color: T.white, cursor: "pointer", fontSize: 13, fontWeight: 700, boxShadow: "0 12px 24px rgba(14,14,44,.14)" } }, "\u770B\u8D77\u6765\u4E0D\u9519\uFF0C\u7EE7\u7EED"))))), step >= 3 && /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 18 } }, /* @__PURE__ */ React.createElement(PlanningUserSummary, null, "\u770B\u8D77\u6765\u4E0D\u9519\uFF0C\u7EE7\u7EED\u751F\u6210\u8D26\u53F7\u5B9A\u4F4D\u3002"), /* @__PURE__ */ React.createElement(PlanningChatDivider, { label: "\u8D26\u53F7\u5B9A\u4F4D" }), /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 8, fontSize: 16, fontWeight: 680 } }, "\u8FD9\u662F\u4F60\u7684\u8D26\u53F7\u5B9A\u4F4D\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13.5 } }, "\u6BCF\u4E00\u9879\u90FD\u53EF\u4EE5\u76F4\u63A5\u7F16\u8F91\uFF0C\u786E\u8BA4\u540E Nori \u4F1A\u6309\u8FD9\u5957\u89C4\u5219\u751F\u6210\u3002")), /* @__PURE__ */ React.createElement(PlanningPanel, { style: { padding: isMobile ? 16 : 20, position: "relative", overflow: "hidden" } }, /* @__PURE__ */ React.createElement(MiniOnionBurst, { active: true }), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "minmax(0, 1.15fr) minmax(280px, .75fr)", gap: 16, alignItems: "start" } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 12 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 14 } }, /* @__PURE__ */ React.createElement("div", { style: { width: 54, height: 54, borderRadius: 18, background: T.irisTint, display: "inline-flex", alignItems: "center", justifyContent: "center", color: T.iris } }, /* @__PURE__ */ React.createElement(Icon, { name: "sparkles", size: 22 })), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 12.5, fontWeight: 650 } }, "\u521B\u4F5C\u8005 \xB7 Holly"), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 4, color: T.navy, fontSize: 21, fontWeight: 720 } }, "\u7406\u6027\u89E3\u8BFB \xB7 \u514B\u5236\u6292\u60C5 \xB7 \u5148\u7ED3\u8BBA\u518D\u5C55\u5F00"))), /* @__PURE__ */ React.createElement("div", { style: { color: T.navyMid, fontSize: 13.5, lineHeight: 1.72 } }, "\u628A\u590D\u6742\u5DE5\u5177\u8BB2\u6210\u666E\u901A\u4EBA\u80FD\u7ACB\u523B\u4E0A\u624B\u7684\u751F\u6D3B\u65B9\u6CD5\u3002")), /* @__PURE__ */ React.createElement("div", { style: { borderRadius: 18, border: `1px solid ${T.hairlineSoft}`, background: "rgba(250,252,254,.72)", padding: 16 } }, /* @__PURE__ */ React.createElement("div", { style: { color: T.navyLight, fontSize: 12, fontWeight: 680, marginBottom: 8 } }, "\u8D26\u53F7\u5B9A\u4F4D\u8BB0\u5FC6"), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 12, color: T.navyMid, fontSize: 13, lineHeight: 1.68 } }, "\u518D\u53D1\u5E03 2 \u6761\uFF0CNori \u5C31\u80FD\u628A\u4F60\u7684\u9996\u6BB5\u94A9\u5B50\u504F\u597D\u6C89\u6DC0\u6210\u89C4\u5219\u3002")))), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "repeat(2, minmax(0, 1fr))", gap: 14 } }, /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u8D26\u53F7\u540D\u5EFA\u8BAE", style: { padding: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, (activeReport.names || []).map((item, index) => /* @__PURE__ */ React.createElement("input", { key: index, value: item, onChange: (e) => setActiveReport((prev) => ({ ...prev, names: prev.names.map((row, i) => i === index ? e.target.value : row) })), style: { width: "100%", minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: "rgba(250,252,254,.72)", color: T.navyMid, padding: "0 10px", outline: "none", fontSize: 13 } })))), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u4EBA\u8BBE\u5173\u952E\u8BCD", style: { padding: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, (activeReport.keywords || []).map((item, index) => /* @__PURE__ */ React.createElement("input", { key: index, value: item, onChange: (e) => setActiveReport((prev) => ({ ...prev, keywords: prev.keywords.map((row, i) => i === index ? e.target.value : row) })), style: { width: "100%", minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: "rgba(250,252,254,.72)", color: T.navyMid, padding: "0 10px", outline: "none", fontSize: 13 } })))), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u5E38\u7528\u53E5\u5F0F", style: { padding: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, (activeReport.phrases || []).map((item, index) => /* @__PURE__ */ React.createElement("input", { key: index, value: item, onChange: (e) => setActiveReport((prev) => ({ ...prev, phrases: prev.phrases.map((row, i) => i === index ? e.target.value : row) })), style: { width: "100%", minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: "rgba(250,252,254,.72)", color: T.navyMid, padding: "0 10px", outline: "none", fontSize: 13 } })))), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u8D26\u53F7\u4E3B\u8981\u5185\u5BB9\u652F\u67F1", style: { padding: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, (pillars || []).map((item, index) => /* @__PURE__ */ React.createElement("input", { key: index, value: item, onChange: (e) => setPillars((list) => list.map((row, i) => i === index ? e.target.value : row)), style: { width: "100%", minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: "rgba(250,252,254,.72)", color: T.navyMid, padding: "0 10px", outline: "none", fontSize: 13 } })))), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u5BF9\u6807\u535A\u4E3B", style: { padding: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, (activeReport.bloggers || []).map((item, index) => /* @__PURE__ */ React.createElement("input", { key: index, value: item, onChange: (e) => setActiveReport((prev) => ({ ...prev, bloggers: prev.bloggers.map((row, i) => i === index ? e.target.value : row) })), style: { width: "100%", minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: "rgba(250,252,254,.72)", color: T.navyMid, padding: "0 10px", outline: "none", fontSize: 13 } })))), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u63A8\u8350\u5C01\u9762\u56FE\u7247", style: { padding: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 8 } }, (activeReport.covers || []).map((item, index) => /* @__PURE__ */ React.createElement("input", { key: index, value: item, onChange: (e) => setActiveReport((prev) => ({ ...prev, covers: prev.covers.map((row, i) => i === index ? e.target.value : row) })), style: { width: "100%", minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: "rgba(250,252,254,.72)", color: T.navyMid, padding: "0 10px", outline: "none", fontSize: 13 } })))), /* @__PURE__ */ React.createElement("div", { style: { gridColumn: isMobile ? "auto" : "span 2" } }, /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u7B7E\u540D", style: { padding: 18 } }, /* @__PURE__ */ React.createElement(
      "textarea",
      {
        value: activeReport.bio,
        onChange: (e) => setActiveReport((prev) => ({ ...prev, bio: e.target.value })),
        rows: 3,
        style: { width: "100%", border: `1px solid ${T.hairlineSoft}`, borderRadius: 14, background: "rgba(250,252,254,.76)", color: T.navyMid, padding: 12, outline: "none", resize: "vertical", fontSize: 13, lineHeight: 1.7, fontFamily: T.fontSans }
      }
    )))), step === 3 && /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 10, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(2), style: { border: "none", background: "transparent", color: T.navyLight, cursor: "pointer", fontSize: 12.8, fontWeight: 650 } }, "\u8FD4\u56DE\u4E0A\u4E00\u6B65"), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", gap: 10, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(4), style: { height: 40, padding: "0 18px", borderRadius: 13, border: "none", background: T.navy, color: T.white, cursor: "pointer", fontSize: 13, fontWeight: 700, boxShadow: "0 12px 24px rgba(14,14,44,.14)" } }, "\u786E\u8BA4\u753B\u50CF")))), step >= 4 && /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 18 } }, /* @__PURE__ */ React.createElement(PlanningUserSummary, null, "\u786E\u8BA4\u8FD0\u8425\u8BA1\u5212\uFF0C\u7EE7\u7EED\u6392\u5185\u5BB9\u6392\u671F\u3002"), /* @__PURE__ */ React.createElement(PlanningChatDivider, { label: "\u5185\u5BB9\u6392\u671F" }), /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 8, fontSize: 16, fontWeight: 680 } }, "\u5148\u9009\u4E00\u6BB5\u65F6\u95F4\uFF0C\u6211\u628A\u4E00\u5468\u5185\u5BB9\u6392\u671F\u653E\u8FDB\u53BB\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13.5 } }, "\u9ED8\u8BA4\u4E00\u5468 7 \u7BC7\uFF0C\u6309\u5185\u5BB9\u652F\u67F1\u8F6E\u8F6C\uFF0C\u53F3\u4E0A\u89D2\u53EF\u5355\u72EC\u6539\u65F6\u95F4\u3002")), /* @__PURE__ */ React.createElement(
      PlanningPanel,
      {
        title: "\u4E00\u5468\u5185\u5BB9\u6392\u671F",
        action: /* @__PURE__ */ React.createElement("div", { style: { position: "relative" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setShowWeekPicker((v) => !v), style: { height: 32, padding: "0 11px", borderRadius: 12, border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.78)", color: T.navyMid, cursor: "pointer", display: "inline-flex", alignItems: "center", gap: 6, fontSize: 12, fontWeight: 650 } }, /* @__PURE__ */ React.createElement(Icon, { name: "calendar", size: 13 }), "\u9009\u62E9\u5468"), showWeekPicker && /* @__PURE__ */ React.createElement(
          "input",
          {
            type: "date",
            value: weekStart,
            onChange: (e) => {
              setWeekStart(e.target.value);
              setShowWeekPicker(false);
            },
            style: {
              position: "absolute",
              right: 0,
              top: 38,
              zIndex: 10,
              height: 36,
              border: `1px solid ${T.hairlineSoft}`,
              borderRadius: 12,
              background: T.white,
              padding: "0 9px",
              color: T.navyMid,
              boxShadow: T.shadowMd,
              fontFamily: T.fontSans
            }
          }
        )),
        style: { padding: 18 }
      },
      /* @__PURE__ */ React.createElement("div", { style: { margin: "-2px 0 14px", color: T.navyLight, fontSize: 12.5 } }, "\u89C4\u5212\u5468\u8D77\u59CB\u65E5\uFF1A", weekStart),
      /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 10 } }, calendar.map((item, index) => /* @__PURE__ */ React.createElement("div", { key: `${item.day}-${index}`, style: {
        borderRadius: 18,
        background: index === 0 ? "rgba(239,239,253,.56)" : "rgba(250,252,254,.76)",
        border: `1px solid ${index === 0 ? "rgba(75,77,237,.14)" : T.hairlineSoft}`,
        padding: 14
      } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 12, alignItems: "center", marginBottom: 10 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("span", { style: { height: 24, padding: "0 9px", borderRadius: 999, background: T.white, color: T.navy, display: "inline-flex", alignItems: "center", fontSize: 12.5, fontWeight: 720 } }, item.day), /* @__PURE__ */ React.createElement("span", { style: { color: T.navyLight, fontSize: 12.2 } }, item.type)), /* @__PURE__ */ React.createElement("button", { onClick: () => setCalendar((list) => list.filter((_, i) => i !== index)), style: { ...iconBtnStyle(), width: 32, height: 32 } }, /* @__PURE__ */ React.createElement(Icon, { name: "close", size: 11 }))), /* @__PURE__ */ React.createElement(
        "textarea",
        {
          value: item.topic,
          rows: 2,
          onChange: (e) => setCalendar((list) => list.map((row, i) => i === index ? { ...row, topic: e.target.value } : row)),
          style: {
            width: "100%",
            border: `1px solid ${T.hairlineSoft}`,
            background: "rgba(255,255,255,.7)",
            borderRadius: 14,
            minHeight: 54,
            padding: "10px 11px",
            color: T.navy,
            fontSize: 13,
            outline: "none",
            resize: "vertical",
            fontFamily: T.fontSans,
            lineHeight: 1.58
          }
        }
      ), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 10, color: T.navyLight, fontSize: 11.8 } }, "\u53C2\u8003\uFF1A", item.ref))), /* @__PURE__ */ React.createElement("button", { onClick: () => setCalendar((list) => [...list, { day: "\u65B0\u589E", type: "\u56FE\u6587", topic: "\u65B0\u7684\u5185\u5BB9\u9009\u9898", ref: "@\u53C2\u8003\u8D26\u53F7" }]), style: { height: 38, borderRadius: 13, border: `1px dashed ${T.hairline}`, background: "rgba(255,255,255,.58)", color: T.navyMid, cursor: "pointer", fontSize: 12.5, fontWeight: 650 } }, "\u65B0\u589E\u4E00\u5929"))
    ), step === 4 && /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 10, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(3), style: { border: "none", background: "transparent", color: T.navyLight, cursor: "pointer", fontSize: 12.8, fontWeight: 650 } }, "\u8FD4\u56DE\u4E0A\u4E00\u6B65"), /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(5), style: { height: 40, padding: "0 18px", borderRadius: 13, border: "none", background: T.navy, color: T.white, cursor: "pointer", fontSize: 13, fontWeight: 700, boxShadow: "0 12px 24px rgba(14,14,44,.14)" } }, "\u751F\u6210\u6700\u7EC8\u4EA4\u4ED8"))), step >= 5 && /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gap: 18 } }, /* @__PURE__ */ React.createElement(PlanningUserSummary, null, "\u751F\u6210\u6700\u7EC8\u4EA4\u4ED8\u3002"), /* @__PURE__ */ React.createElement(PlanningChatDivider, { label: "\u6700\u7EC8\u4EA4\u4ED8" }), /* @__PURE__ */ React.createElement(NoriSays, null, /* @__PURE__ */ React.createElement("p", { style: { marginBottom: 8, fontSize: 16, fontWeight: 680 } }, "\u4EA4\u4ED8\u597D\u4E86\uFF0C\u8FD9\u662F\u4F60\u53EF\u4EE5\u76F4\u63A5\u5E26\u8D70\u7684\u7248\u672C\u3002"), /* @__PURE__ */ React.createElement("p", { style: { color: T.navyMid, fontSize: 13.5 } }, "\u300A\u8D26\u53F7\u5B9A\u4F4D + \u8FD0\u8425\u8BA1\u5212 + \u5185\u5BB9\u6392\u671F\u300B1 \u4EFD\uFF0C\u542B\u5B9A\u4F4D\u3001\u4EBA\u8BBE\u3001\u5BF9\u6807\u3001\u9009\u9898\u5E93\u3001\u53D1\u5E03\u8282\u594F\u3001\u6570\u636E\u76EE\u6807\u3002")), /* @__PURE__ */ React.createElement(PlanningPanel, { title: "\u6700\u7EC8\u4EA4\u4ED8", style: { padding: 18 } }, /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "minmax(0, 1.08fr) 280px", gap: 14 } }, /* @__PURE__ */ React.createElement("div", { style: { borderRadius: 18, border: `1px solid ${T.hairlineSoft}`, background: "rgba(250,252,254,.76)", padding: 16 } }, /* @__PURE__ */ React.createElement("div", { style: { fontSize: 19, fontWeight: 740, color: T.navy } }, "\u300A\u8D26\u53F7\u5B9A\u4F4D + \u8FD0\u8425\u8BA1\u5212 + \u5185\u5BB9\u6392\u671F\u300B"), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 8, color: T.navyMid, fontSize: 13.5, lineHeight: 1.7 } }, "1 \u4EFD\uFF0C\u542B\u5B9A\u4F4D\u3001\u4EBA\u8BBE\u3001\u5BF9\u6807\u3001\u9009\u9898\u5E93\u3001\u53D1\u5E03\u8282\u594F\u3001\u6570\u636E\u76EE\u6807\u3002"), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 14, display: "flex", flexWrap: "wrap", gap: 8 } }, ["\u5B9A\u4F4D", "\u4EBA\u8BBE", "\u5BF9\u6807", "\u9009\u9898\u5E93", "\u53D1\u5E03\u8282\u594F", "\u6570\u636E\u76EE\u6807"].map((tag) => /* @__PURE__ */ React.createElement("span", { key: tag, style: { height: 32, padding: "0 11px", borderRadius: 999, background: "rgba(255,255,255,.78)", border: `1px solid ${T.hairlineSoft}`, color: T.navyMid, display: "inline-flex", alignItems: "center", fontSize: 12.2, fontWeight: 650 } }, tag))), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 14, color: T.navyLight, fontSize: 12.2, lineHeight: 1.64 } }, "\u8FD9\u4EFD\u6587\u6863\u4F1A\u540C\u6B65\u5230 Nori \u540E\u7EED\u521B\u4F5C\u91CC\u3002")), /* @__PURE__ */ React.createElement("div", { style: { borderRadius: 18, border: `1px solid ${T.hairlineSoft}`, background: "rgba(255,255,255,.72)", padding: 16, display: "grid", gap: 8, alignContent: "start" } }, /* @__PURE__ */ React.createElement("button", { onClick: downloadPlan, style: { ...pillButtonStyle(true), justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "download", size: 15 }), "\u4E0B\u8F7D\u6587\u6863"), /* @__PURE__ */ React.createElement("button", { onClick: () => setLiked((v) => !v), style: { ...pillButtonStyle(false), justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "heart", size: 15 }), liked ? "\u5DF2\u70B9\u8D5E" : "\u70B9\u8D5E"), /* @__PURE__ */ React.createElement("button", { onClick: () => copyPlan(buildPlanExportText({ diagnosisText, persona: activeReport || persona, pillars, calendar })), style: { ...pillButtonStyle(false), justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: copied ? "check" : "copy", size: 15 }), copied ? "\u5DF2\u590D\u5236" : "\u590D\u5236"), /* @__PURE__ */ React.createElement("button", { onClick: completePlan, style: { ...pillButtonStyle(false), justifyContent: "center" } }, /* @__PURE__ */ React.createElement(Icon, { name: "sparkles", size: 15 }), "\u5B8C\u6210\u5E76\u5F00\u59CB\u5236\u4F5C")))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", justifyContent: "space-between", gap: 10, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: () => setStep(4), style: { border: "none", background: "transparent", color: T.navyLight, cursor: "pointer", fontSize: 12.8, fontWeight: 650 } }, "\u8FD4\u56DE\u4E0A\u4E00\u6B65"), /* @__PURE__ */ React.createElement("button", { onClick: completePlan, style: { height: 40, padding: "0 18px", borderRadius: 13, border: "none", background: T.navy, color: T.white, cursor: "pointer", fontSize: 13, fontWeight: 700, boxShadow: "0 12px 24px rgba(14,14,44,.14)" } }, "\u5B8C\u6210\u4EA4\u4ED8"))), /* @__PURE__ */ React.createElement("div", { ref: endRef, style: { height: 1 } }))), modalType && /* @__PURE__ */ React.createElement(InputMethodModal, { type: modalType, onClose: () => setModalType(null), onConfirm: (att) => {
      setAttachments((list) => [...list, att]);
      if (att.type === "text") setRawInput(att.value);
      setModalType(null);
      setSentIntro(true);
    } }));
  };
  window.AccountPlanningPagePolishedV2 = AccountPlanningPagePolishedV2;
  window.AccountPlanningPagePolished = AccountPlanningPagePolishedV2;
  var WelcomeIntroOverlay = ({ open, leaving, onStartPlan, onTry }) => {
    const { isMobile } = useViewport();
    if (!open) return null;
    return /* @__PURE__ */ React.createElement("div", { style: {
      position: "fixed",
      inset: 0,
      zIndex: 999,
      background: "rgba(8,8,13,.56)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      padding: 22,
      opacity: leaving ? 0 : 1,
      transform: leaving ? "scale(1.015)" : "scale(1)",
      transition: `opacity .46s ${T.ease}, transform .46s ${T.spring}`
    } }, /* @__PURE__ */ React.createElement("div", { style: {
      width: "min(620px, 100%)",
      borderRadius: 28,
      background: T.white,
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: "0 42px 110px rgba(14,14,44,.24), 0 8px 24px rgba(14,14,44,.08)",
      padding: isMobile ? "24px 22px 22px" : "32px 34px 30px",
      color: T.navy,
      animation: `welcomeRise .72s ${T.spring} both`
    } }, /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", gap: 13, marginBottom: 24 } }, /* @__PURE__ */ React.createElement(NoriLogo, { size: 38 }), /* @__PURE__ */ React.createElement("div", null, /* @__PURE__ */ React.createElement("div", { style: { fontFamily: T.fontSerif, fontSize: 34, lineHeight: 0.96, fontStyle: "italic", fontWeight: 700, letterSpacing: 0 } }, "Nori"), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 7, color: T.navyLight, fontSize: 12.2, lineHeight: 1.45 } }, "\u61C2\u4F60\uFF0C\u4F1A\u8FDB\u5316\u7684\u81EA\u5A92\u4F53\u8D26\u53F7\u4EE3\u7406"))), /* @__PURE__ */ React.createElement("h1", { style: { margin: 0, fontSize: isMobile ? 25 : 32, lineHeight: 1.18, letterSpacing: 0, fontWeight: 760 } }, "\u4ECE\u4E00\u4E2A\u6A21\u7CCA\u60F3\u6CD5\uFF0C\u957F\u6210\u4E00\u4E2A\u80FD\u6301\u7EED\u8FD0\u8425\u7684\u8D26\u53F7\u3002"), /* @__PURE__ */ React.createElement("p", { style: { margin: "14px 0 22px", color: T.navyMid, fontSize: 14, lineHeight: 1.76, maxWidth: 520, fontWeight: 430 } }, "Nori \u4F1A\u5E2E\u4F60\u5B8C\u6210\u8D26\u53F7\u5B9A\u4F4D\u3001\u8FD0\u8425\u8BA1\u5212\u548C\u5185\u5BB9\u6392\u671F\uFF0C\u5E76\u628A\u7B2C\u4E00\u7BC7\u5185\u5BB9\u76F4\u63A5\u5E26\u8FDB\u5DE5\u4F5C\u53F0\u3002"), /* @__PURE__ */ React.createElement("div", { style: { display: "grid", gridTemplateColumns: isMobile ? "1fr" : "repeat(3, minmax(0, 1fr))", gap: 10, marginBottom: 24 } }, [
      ["target", "\u8D26\u53F7\u5B9A\u4F4D", "\u628A\u8D5B\u9053\u3001\u76EE\u6807\u548C\u5E73\u53F0\u8BF4\u6E05\u695A"],
      ["sparkles", "\u8FD0\u8425\u8BA1\u5212", "\u5F62\u6210\u53EF\u590D\u7528\u7684\u4EBA\u8BBE\u548C\u5185\u5BB9\u652F\u67F1"],
      ["document", "\u5185\u5BB9\u6392\u671F", "\u81EA\u52A8\u6392\u51FA\u4E00\u5468\u9009\u9898\u5EFA\u8BAE"]
    ].map(([icon, title, desc]) => /* @__PURE__ */ React.createElement("div", { key: title, style: { borderRadius: 17, background: "rgba(246,248,251,.76)", border: `1px solid ${T.hairlineSoft}`, padding: 14 } }, /* @__PURE__ */ React.createElement("span", { style: { width: 32, height: 32, borderRadius: 12, background: T.white, color: T.iris, display: "inline-flex", alignItems: "center", justifyContent: "center", marginBottom: 12, boxShadow: "inset 0 1px 0 rgba(255,255,255,.86)" } }, /* @__PURE__ */ React.createElement(Icon, { name: icon, size: 15 })), /* @__PURE__ */ React.createElement("div", { style: { fontSize: 13.2, fontWeight: 740, color: T.navy } }, title), /* @__PURE__ */ React.createElement("div", { style: { marginTop: 5, fontSize: 11.8, lineHeight: 1.52, color: T.navyLight } }, desc)))), /* @__PURE__ */ React.createElement("div", { style: { display: "flex", alignItems: "center", justifyContent: "flex-end", gap: 12, flexWrap: "wrap" } }, /* @__PURE__ */ React.createElement("button", { onClick: onTry, style: { height: 42, padding: "0 12px", border: "none", background: "transparent", color: T.navyLight, cursor: "pointer", fontSize: 13, fontWeight: 650 } }, "\u8DF3\u8FC7\uFF0C\u7A0D\u540E\u518D\u505A"), /* @__PURE__ */ React.createElement("button", { onClick: onStartPlan, style: {
      height: 44,
      padding: "0 18px",
      borderRadius: 14,
      border: "none",
      background: T.navy,
      color: T.white,
      cursor: "pointer",
      fontSize: 13.5,
      fontWeight: 760,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      gap: 8,
      boxShadow: "0 14px 30px rgba(14,14,44,.18)"
    } }, "\u5F00\u59CB\u8D26\u53F7\u89C4\u5212", /* @__PURE__ */ React.createElement(Icon, { name: "arrowRight", size: 14 })))));
  };
  window.WelcomeIntroOverlay = WelcomeIntroOverlay;
  var GlobalPolish = () => /* @__PURE__ */ React.createElement("style", null, `
    * { -webkit-tap-highlight-color: transparent; }
    button, a, textarea { font: inherit; }
    button:active { transform: scale(.985); }
    ::selection { background: rgba(214,255,0,.42); color: ${T.navy}; }
    @keyframes templateTicker {
      0% { opacity: 0; transform: translateY(10px); filter: blur(2px); }
      13% { opacity: 1; transform: translateY(0); filter: blur(0); }
      78% { opacity: 1; transform: translateY(0); filter: blur(0); }
      100% { opacity: 0; transform: translateY(-10px); filter: blur(2px); }
    }
    .noriWord {
      position: relative;
      overflow: visible;
      transition: transform .34s ${T.spring}, filter .34s ${T.ease};
    }
    .noriWord:hover { transform: translateY(-1px) scale(1.01); filter: drop-shadow(0 10px 18px rgba(14,14,44,.07)); }
    .noriWord::after {
      content: "";
      position: absolute;
      inset: -10px -14px;
      background: linear-gradient(110deg, transparent 0%, rgba(255,255,255,0) 38%, rgba(214,255,0,.36) 48%, rgba(255,255,255,.72) 52%, rgba(75,77,237,.18) 58%, transparent 68%);
      transform: translateX(-105%) skewX(-12deg);
      opacity: 0;
      pointer-events: none;
      mix-blend-mode: screen;
    }
    .noriWordSpark::after { animation: noriShimmer .92s ${T.spring} both; }
    .noriWordSpark { animation: noriLetterPulse .92s ${T.spring} both; }
    @keyframes noriShimmer {
      0% { opacity: 0; transform: translateX(-105%) skewX(-12deg); }
      28% { opacity: .7; }
      100% { opacity: 0; transform: translateX(105%) skewX(-12deg); }
    }
    @keyframes noriLetterPulse {
      0% { transform: scale(1); filter: drop-shadow(0 0 0 rgba(214,255,0,0)); }
      34% { transform: translateY(-1px) scale(1.018); filter: drop-shadow(0 0 12px rgba(214,255,0,.22)); }
      62% { transform: translateY(0) scale(.995); }
      100% { transform: scale(1); filter: drop-shadow(0 0 0 rgba(214,255,0,0)); }
    }
    @keyframes onionPop {
      0% { opacity: 0; transform: translate(-50%, -50%) translate(0, 0) rotate(0deg) scale(.16); filter: blur(4px) drop-shadow(0 0 0 rgba(14,14,44,0)); }
      38% { opacity: .92; filter: blur(0) drop-shadow(0 12px 18px rgba(14,14,44,.10)); }
      76% { opacity: .92; }
      100% { opacity: 0; transform: translate(-50%, -50%) translate(var(--x, 0), var(--y, 0)) rotate(var(--r, 0deg)) scale(.72); filter: blur(2px) drop-shadow(0 12px 18px rgba(14,14,44,.06)); }
    }
    @keyframes sparkPop {
      0% { opacity: 0; transform: translate(0, 0) scale(.2); }
      28% { opacity: 1; }
      100% { opacity: 0; transform: translate(var(--spark-x, 0), var(--spark-y, 0)) scale(1.35); }
    }
    @keyframes accountIconSpin {
      0% { transform: rotate(0deg) scale(1); }
      48% { transform: rotate(18deg) scale(1.06); }
      100% { transform: rotate(0deg) scale(1); }
    }
    @keyframes welcomeRise {
      0% { opacity: 0; transform: translateY(18px) scale(.985); filter: blur(5px); }
      100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }
    @keyframes userMessageReveal {
      0% { opacity: 0; transform: translateY(7px) scale(.996); }
      100% { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }
    @keyframes messageReveal {
      0% { opacity: 0; transform: translateY(10px) scale(.996); clip-path: inset(0 0 88% 0 round 18px); }
      22% { opacity: .22; clip-path: inset(0 0 70% 0 round 18px); }
      48% { opacity: .58; clip-path: inset(0 0 38% 0 round 18px); }
      74% { opacity: .88; clip-path: inset(0 0 12% 0 round 18px); }
      100% { opacity: 1; transform: translateY(0) scale(1); clip-path: inset(0 0 0 0 round 18px); }
    }
    @keyframes memoryReady {
      0% { opacity: .54; transform: translateY(4px); }
      58% { opacity: 1; transform: translateY(-1px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    @keyframes planningReveal {
      0% { opacity: 0; transform: translateY(12px); clip-path: inset(0 0 94% 0 round 20px); }
      22% { opacity: .20; clip-path: inset(0 0 76% 0 round 20px); }
      52% { opacity: .56; clip-path: inset(0 0 40% 0 round 20px); }
      78% { opacity: .88; clip-path: inset(0 0 12% 0 round 20px); }
      100% { opacity: 1; transform: translateY(0); clip-path: inset(0 0 0 0 round 20px); }
    }
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
      background: rgba(14,14,44,.13);
      border: 3px solid transparent;
      border-radius: 999px;
      background-clip: content-box;
    }
    ::-webkit-scrollbar-thumb:hover { background: rgba(14,14,44,.22); background-clip: content-box; }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: .001ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: .001ms !important;
        scroll-behavior: auto !important;
      }
    }
  `);
  var App = () => {
    const [page, setPage] = React.useState("home");
    const [prompt, setPrompt] = React.useState("");
    const [assetDraft, setAssetDraft] = React.useState(null);
    const [skillDraft, setSkillDraft] = React.useState(null);
    const [accountPlanDraft, setAccountPlanDraft] = React.useState(null);
    const [showIntro, setShowIntro] = React.useState(true);
    const [introLeaving, setIntroLeaving] = React.useState(false);
    const [recentProject, setRecentProject] = React.useState(null);
    const [insightInitialTab, setInsightInitialTab] = React.useState("review");
    const [homeFocusKey, setHomeFocusKey] = React.useState(0);
    const [inspirationDraft, setInspirationDraft] = React.useState(null);
    const goGen = (p) => {
      const clean = p || "";
      setPrompt(clean);
      setInspirationDraft(null);
      setAssetDraft(null);
      setSkillDraft(null);
      setAccountPlanDraft(null);
      if (clean.trim()) {
        setRecentProject({
          title: clean.replace(/^\[[^\]]+\]\s*/, "").slice(0, 34),
          summary: clean.length > 34 ? `${clean.slice(0, 54)}...` : "\u6765\u81EA\u9996\u9875\u5BF9\u8BDD\u6846\u7684\u7B2C\u4E00\u8F6E\u521B\u4F5C",
          date: "\u4ECA\u5929",
          prompt: clean
        });
      }
      setPage("gen");
    };
    const startFreshAccountPlan = ({ hideIntroImmediately = false } = {}) => {
      clearPlanDraftStorage();
      setAccountPlanDraft(null);
      if (hideIntroImmediately) {
        setShowIntro(false);
        setIntroLeaving(false);
      }
      setPage("accountPlan");
    };
    const withPolish = (node) => /* @__PURE__ */ React.createElement(React.Fragment, null, /* @__PURE__ */ React.createElement(GlobalPolish, null), node, /* @__PURE__ */ React.createElement(
      WelcomeIntroOverlay,
      {
        open: showIntro,
        leaving: introLeaving,
        onTry: () => {
          setIntroLeaving(true);
          window.setTimeout(() => {
            setShowIntro(false);
            setIntroLeaving(false);
          }, 460);
        },
        onStartPlan: () => {
          setIntroLeaving(true);
          window.setTimeout(() => {
            setShowIntro(false);
            setIntroLeaving(false);
            startFreshAccountPlan();
          }, 460);
        }
      }
    ));
    if (page === "home") return withPolish(
      /* @__PURE__ */ React.createElement(
        HomePage,
        {
          onSubmit: goGen,
          onOpenAssets: () => setPage("assets"),
          onOpenInsights: () => {
            setInsightInitialTab("review");
            setPage("insights");
          },
          onOpenMine: () => setPage("mine"),
          onAccountPlan: () => startFreshAccountPlan({ hideIntroImmediately: true }),
          accountPlanDraft,
          recentProject,
          onOpenInspiration: (draft) => {
            setPage("gen");
            setInspirationDraft({
              item: draft?.item || null,
              prompt: draft?.prompt || "\u53C2\u8003\u9996\u9875\u7075\u611F\u53D1\u73B0\u91CC\u7684\u5185\u5BB9\uFF0C\u628A\u8FD9\u5F20\u56FE\u6539\u6210\u66F4\u50CF\u4E0A\u6D77\u996D\u5E97\u63A2\u5E97\u5C01\u9762\u7684\u6837\u5F0F\u3002"
            });
          },
          focusInspirationKey: homeFocusKey,
          onOpenProject: () => {
            if (!recentProject) return;
            setPrompt(recentProject.prompt);
            setAssetDraft(null);
            setSkillDraft(null);
            setAccountPlanDraft(null);
            setPage("gen");
          }
        }
      )
    );
    if (page === "accountPlan") {
      return withPolish(
        /* @__PURE__ */ React.createElement(
          AccountPlanningPagePolishedV2,
          {
            onBackHome: () => setPage("home"),
            onOpenAssets: () => setPage("assets"),
            onOpenInsights: () => {
              setInsightInitialTab("review");
              setPage("insights");
            },
            onNewChat: () => {
              setPrompt("");
              setAssetDraft(null);
              setSkillDraft(null);
              setAccountPlanDraft(null);
              setPage("gen");
            },
            onComplete: (draft) => {
              setPrompt("");
              setAssetDraft(null);
              setSkillDraft(null);
              setAccountPlanDraft(draft);
              setPage("gen");
            }
          }
        )
      );
    }
    if (page === "assets") {
      return withPolish(
        /* @__PURE__ */ React.createElement(
          AssetsPage,
          {
            onBackHome: () => setPage("home"),
            onOpenInsights: () => {
              setInsightInitialTab("review");
              setPage("insights");
            },
            onOpenMine: () => setPage("mine"),
            onNewChat: () => {
              setPrompt("");
              setAssetDraft(null);
              setSkillDraft(null);
              setAccountPlanDraft(null);
              setPage("gen");
            },
            onOpenAsset: (asset) => {
              setPrompt(`\u7EE7\u7EED\u7F16\u8F91\u5185\u5BB9\u8D44\u4EA7\uFF1A${asset.title}`);
              setAssetDraft(asset);
              setSkillDraft(null);
              setAccountPlanDraft(null);
              setPage("gen");
            }
          }
        )
      );
    }
    if (page === "mine") {
      return withPolish(
        /* @__PURE__ */ React.createElement(
          MinePage,
          {
            onBackHome: () => setPage("home"),
            onOpenAssets: () => setPage("assets"),
            onOpenInsights: () => {
              setInsightInitialTab("review");
              setPage("insights");
            },
            onNewChat: () => {
              setPrompt("");
              setAssetDraft(null);
              setSkillDraft(null);
              setAccountPlanDraft(null);
              setPage("gen");
            }
          }
        )
      );
    }
    if (page === "insights") {
      return withPolish(
        /* @__PURE__ */ React.createElement(
          InsightsPage,
          {
            onBackHome: () => setPage("home"),
            onOpenAssets: () => setPage("assets"),
            onOpenMine: () => setPage("mine"),
            initialTab: insightInitialTab,
            onNewChat: () => {
              setPrompt("");
              setAssetDraft(null);
              setSkillDraft(null);
              setAccountPlanDraft(null);
              setPage("gen");
            }
          }
        )
      );
    }
    return withPolish(
      /* @__PURE__ */ React.createElement(
        GenerationPage,
        {
          initialPrompt: prompt,
          assetDraft,
          skillDraft,
          onboardingDraft: accountPlanDraft,
          inspirationDraft,
          onBackHome: () => setPage("home"),
          onOpenAssets: () => setPage("assets"),
          onOpenInsights: () => {
            setInsightInitialTab("review");
            setPage("insights");
          },
          onOpenMine: () => setPage("mine"),
          onOpenHomeInspiration: () => {
            setHomeFocusKey((v) => v + 1);
            setPage("home");
          },
          onNewChat: () => {
            setPrompt("");
            setAssetDraft(null);
            setSkillDraft(null);
            setAccountPlanDraft(null);
            setPage("gen");
          }
        }
      )
    );
  };
  ReactDOM.createRoot(document.getElementById("root")).render(/* @__PURE__ */ React.createElement(App, null));
})();
