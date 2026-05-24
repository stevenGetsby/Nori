function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/* ─── Nori Tokens — derived from Design System ─── */
const T = {
  // Brand
  primary: '#D6FF00',
  // Fuschia
  primaryHov: '#b8e000',
  primaryTint: '#f5ffe0',
  iris: '#4B4DED',
  irisHov: '#3537c7',
  irisTint: '#EFEFFD',
  peach: '#F3DBDA',
  peachTint: '#fdf5f5',
  // Onyx scale
  navy: '#0e0e2c',
  navyMid: '#4a4a68',
  navyLight: '#8c8ca1',
  navySoft: '#c4c4d4',
  // Surfaces
  surface: '#ECF1F4',
  // Dorian
  surfaceWh: '#fafcfe',
  // Cloud
  white: '#ffffff',
  hairline: 'rgba(14,14,44,.08)',
  hairlineSoft: 'rgba(14,14,44,.05)',
  // Semantic
  success: '#31D0AA',
  successTint: '#e0faf4',
  warn: '#fb8c00',
  error: '#e53935',
  // Shadows
  shadowXs: '0 1px 2px rgba(14,14,44,.04), 0 1px 4px rgba(14,14,44,.03)',
  shadowSm: '0 2px 6px rgba(14,14,44,.06), 0 1px 2px rgba(14,14,44,.04)',
  shadowMd: '0 4px 12px rgba(14,14,44,.08), 0 1px 3px rgba(14,14,44,.05)',
  shadowLg: '0 8px 24px rgba(14,14,44,.10), 0 2px 6px rgba(14,14,44,.06)',
  shadowXl: '0 16px 48px rgba(14,14,44,.12), 0 4px 12px rgba(14,14,44,.07)',
  shadowBtn: '0 2px 6px rgba(14,14,44,.06), 0 1px 2px rgba(14,14,44,.04), inset 0 -1px 0 rgba(14,14,44,.12)',
  // Type
  fontSans: "'Source Han Sans CN', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif",
  fontSerif: "'Fraunces', Georgia, serif",
  fontMono: "'DM Mono', 'Monaco', monospace"
};
window.T = T;
/* ─── Icon set: outlined, 1.6 stroke, currentColor ─── */
const Icon = ({
  name,
  size = 18,
  color = 'currentColor',
  stroke = 1.6,
  style
}) => {
  const props = {
    width: size,
    height: size,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: color,
    strokeWidth: stroke,
    strokeLinecap: 'round',
    strokeLinejoin: 'round',
    style
  };
  const paths = {
    attach: /*#__PURE__*/React.createElement("path", {
      d: "M21 12.5l-8.5 8.5a5.5 5.5 0 0 1-7.8-7.8l9-9a3.7 3.7 0 0 1 5.2 5.2l-8.5 8.5a1.8 1.8 0 0 1-2.6-2.6L15.5 8"
    }),
    globe: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "12",
      r: "9"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"
    })),
    send: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M22 2L11 13"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M22 2l-7 20-4-9-9-4 20-7Z"
    })),
    arrowRight: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M5 12h14"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M13 5l7 7-7 7"
    })),
    arrowUp: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M12 19V5"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M5 12l7-7 7 7"
    })),
    chevronDown: /*#__PURE__*/React.createElement("path", {
      d: "M6 9l6 6 6-6"
    }),
    chevronLeft: /*#__PURE__*/React.createElement("path", {
      d: "M15 6l-6 6 6 6"
    }),
    chevronRight: /*#__PURE__*/React.createElement("path", {
      d: "M9 6l6 6-6 6"
    }),
    plus: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M12 5v14"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M5 12h14"
    })),
    close: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M18 6L6 18"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M6 6l12 12"
    })),
    check: /*#__PURE__*/React.createElement("path", {
      d: "M5 12.5l5 5 9-12"
    }),
    sparkle: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"
    })),
    star: /*#__PURE__*/React.createElement("path", {
      d: "M12 3l2.8 6.2 6.7.6-5.1 4.5 1.6 6.7L12 17.5 5.9 21l1.6-6.7L2.4 9.8l6.7-.6L12 3z"
    }),
    heart: /*#__PURE__*/React.createElement("path", {
      d: "M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"
    }),
    bookmark: /*#__PURE__*/React.createElement("path", {
      d: "M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"
    }),
    eye: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "12",
      r: "3"
    })),
    edit: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M18.5 2.5a2.1 2.1 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
    })),
    image: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("rect", {
      x: "3",
      y: "3",
      width: "18",
      height: "18",
      rx: "2"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "8.5",
      cy: "8.5",
      r: "1.5"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M21 15l-5-5L5 21"
    })),
    file: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M14 2v6h6"
    })),
    search: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
      cx: "11",
      cy: "11",
      r: "7"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M21 21l-4.3-4.3"
    })),
    chat: /*#__PURE__*/React.createElement("path", {
      d: "M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
    }),
    library: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"
    })),
    home: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M3 9.5l9-7 9 7V20a2 2 0 0 1-2 2h-4v-7H9v7H5a2 2 0 0 1-2-2z"
    })),
    splitView: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("rect", {
      x: "3",
      y: "5",
      width: "18",
      height: "14",
      rx: "4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M11.5 5v14"
    })),
    grid: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("rect", {
      x: "3",
      y: "3",
      width: "7",
      height: "7"
    }), /*#__PURE__*/React.createElement("rect", {
      x: "14",
      y: "3",
      width: "7",
      height: "7"
    }), /*#__PURE__*/React.createElement("rect", {
      x: "3",
      y: "14",
      width: "7",
      height: "7"
    }), /*#__PURE__*/React.createElement("rect", {
      x: "14",
      y: "14",
      width: "7",
      height: "7"
    })),
    expand: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M15 3h6v6"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M9 21H3v-6"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M21 3l-7 7"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M3 21l7-7"
    })),
    collapse: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M4 14h6v6"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M20 10h-6V4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M14 10l7-7"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M3 21l7-7"
    })),
    download: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M7 10l5 5 5-5"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M12 15V3"
    })),
    upload: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M17 8l-5-5-5 5"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M12 3v12"
    })),
    sync: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M21 12a9 9 0 0 1-15 6.7L3 16"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M3 12a9 9 0 0 1 15-6.7L21 8"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M21 3v5h-5"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M3 21v-5h5"
    })),
    transform: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M16 3l4 4-4 4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M20 7H4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M8 21l-4-4 4-4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M4 17h16"
    })),
    phone: /*#__PURE__*/React.createElement("rect", {
      x: "6",
      y: "2",
      width: "12",
      height: "20",
      rx: "2"
    }),
    pen: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M12 19l7-7 3 3-7 7-3-3z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M2 2l7.6 7.6"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "11",
      cy: "11",
      r: "2"
    })),
    sliders: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("line", {
      x1: "4",
      y1: "21",
      x2: "4",
      y2: "14"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "4",
      y1: "10",
      x2: "4",
      y2: "3"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "12",
      y1: "21",
      x2: "12",
      y2: "12"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "12",
      y1: "8",
      x2: "12",
      y2: "3"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "20",
      y1: "21",
      x2: "20",
      y2: "16"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "20",
      y1: "12",
      x2: "20",
      y2: "3"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "1",
      y1: "14",
      x2: "7",
      y2: "14"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "9",
      y1: "8",
      x2: "15",
      y2: "8"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "17",
      y1: "16",
      x2: "23",
      y2: "16"
    })),
    user: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "8",
      r: "4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M4 21a8 8 0 0 1 16 0"
    })),
    play: /*#__PURE__*/React.createElement("path", {
      d: "M5 3l14 9-14 9V3z"
    }),
    paperPlane: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M22 2L11 13"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M22 2l-7 20-4-9-9-4 20-7Z"
    })),
    document: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("rect", {
      x: "4",
      y: "3",
      width: "16",
      height: "18",
      rx: "2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M8 8h8M8 12h8M8 16h5"
    })),
    video: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("rect", {
      x: "2",
      y: "6",
      width: "14",
      height: "12",
      rx: "2"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M22 8l-6 4 6 4z"
    })),
    bilibili: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("rect", {
      x: "3",
      y: "6",
      width: "18",
      height: "14",
      rx: "3"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "9",
      cy: "13",
      r: ".8",
      fill: "currentColor"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "15",
      cy: "13",
      r: ".8",
      fill: "currentColor"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M8 4l3 2M16 4l-3 2"
    })),
    minus: /*#__PURE__*/React.createElement("path", {
      d: "M5 12h14"
    }),
    sparkles: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M12 3l1.8 4.2L18 9l-4.2 1.8L12 15l-1.8-4.2L6 9l4.2-1.8z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M19 14l.9 2.1L22 17l-2.1.9L19 20l-.9-2.1L16 17l2.1-.9z"
    })),
    quote: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M3 14h6v7H3z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M14 14h6v7h-6z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M3 14V9a4 4 0 0 1 4-4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M14 14V9a4 4 0 0 1 4-4"
    })),
    book: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M4 4h7a3 3 0 0 1 3 3v14a2 2 0 0 0-2-2H4z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M20 4h-7a3 3 0 0 0-3 3v14a2 2 0 0 1 2-2h8z"
    })),
    paperclip: /*#__PURE__*/React.createElement("path", {
      d: "M21 12.5l-8.5 8.5a5.5 5.5 0 0 1-7.8-7.8l9-9a3.7 3.7 0 0 1 5.2 5.2l-8.5 8.5a1.8 1.8 0 0 1-2.6-2.6L15.5 8"
    }),
    settings: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "12",
      r: "3"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"
    })),
    bell: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M13.7 21a2 2 0 0 1-3.4 0"
    })),
    refresh: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M3 12a9 9 0 0 1 15-6.7L21 8M21 3v5h-5"
    })),
    skip: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M5 4l10 8-10 8z"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "19",
      y1: "5",
      x2: "19",
      y2: "19"
    })),
    palette: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "12",
      r: "9"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "7",
      cy: "10",
      r: "1.3",
      fill: "currentColor"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "7",
      r: "1.3",
      fill: "currentColor"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "17",
      cy: "10",
      r: "1.3",
      fill: "currentColor"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "16",
      cy: "15",
      r: "1.3",
      fill: "currentColor"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M12 21a3 3 0 0 1-3-3 2 2 0 0 1 2-2h2a2 2 0 0 0 2-2"
    })),
    target: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "12",
      r: "9"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "12",
      r: "5"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "12",
      r: "1.5",
      fill: "currentColor"
    })),
    lightbulb: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M9 18h6"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M10 22h4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M15.5 14a5 5 0 1 0-7 0c.6.6 1 1.4 1 2.3V18h5v-1.7c0-.9.4-1.7 1-2.3z"
    })),
    chart: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M3 3v18h18"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M7 14l3-3 4 4 5-6"
    })),
    trending: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M22 7l-9 9-5-5-7 7"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M16 7h6v6"
    })),
    layers: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M12 2L2 7l10 5 10-5-10-5z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M2 17l10 5 10-5"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M2 12l10 5 10-5"
    })),
    list: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("line", {
      x1: "8",
      y1: "6",
      x2: "21",
      y2: "6"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "8",
      y1: "12",
      x2: "21",
      y2: "12"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "8",
      y1: "18",
      x2: "21",
      y2: "18"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "3",
      y1: "6",
      x2: "3.01",
      y2: "6"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "3",
      y1: "12",
      x2: "3.01",
      y2: "12"
    }), /*#__PURE__*/React.createElement("line", {
      x1: "3",
      y1: "18",
      x2: "3.01",
      y2: "18"
    })),
    moreH: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
      cx: "5",
      cy: "12",
      r: "1.2",
      fill: "currentColor"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "12",
      r: "1.2",
      fill: "currentColor"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "19",
      cy: "12",
      r: "1.2",
      fill: "currentColor"
    })),
    moreV: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "5",
      r: "1.2",
      fill: "currentColor"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "12",
      r: "1.2",
      fill: "currentColor"
    }), /*#__PURE__*/React.createElement("circle", {
      cx: "12",
      cy: "19",
      r: "1.2",
      fill: "currentColor"
    })),
    link: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"
    })),
    folder: /*#__PURE__*/React.createElement("path", {
      d: "M3 7a2 2 0 0 1 2-2h4l2 3h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"
    }),
    flag: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M4 22V4"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M4 4h13l-2 4 2 4H4"
    })),
    headphone: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("path", {
      d: "M3 18v-6a9 9 0 0 1 18 0v6"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3z"
    }), /*#__PURE__*/React.createElement("path", {
      d: "M3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"
    })),
    /* brand glyphs */
    xhs: /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("rect", {
      x: "3",
      y: "3",
      width: "18",
      height: "18",
      rx: "4"
    })),
    nori: null // logo handled separately
  };
  return /*#__PURE__*/React.createElement("svg", props, paths[name]);
};

/* Brand logo — onion silhouette based on the provided reference mark. */
const NoriLogo = ({
  size = 28,
  dark = true
}) => {
  const fg = dark ? T.navy : '#fff';
  const bg = T.primary;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      width: size,
      height: size,
      borderRadius: size * 0.32,
      background: bg,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: size * 0.72,
    height: size * 0.72,
    viewBox: "0 0 64 64",
    fill: "none",
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M31.8 5.5L36.4 13.3L41 5.8C44 12.2 49.9 17.8 54.2 26.6C59.1 36.6 56.8 48.8 48.2 56C43.6 59.9 38 62 32 62C26 62 20.4 59.9 15.8 56C7.2 48.8 4.9 36.6 9.8 26.6C14.2 17.7 19.8 12 22.8 5.7C24.6 9 25.8 11.8 26.6 15.1C27.9 10.6 29.4 7.7 31.8 5.5Z",
    fill: fg
  }), /*#__PURE__*/React.createElement("path", {
    d: "M31.5 14.5C26.6 19.7 23.4 26.3 22 33.4C20.6 40.2 21.2 47.3 24 53.6",
    stroke: bg,
    strokeWidth: "3.2",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M22 12.8C16.7 19.5 13.8 27.2 13 35.3C12.4 41.4 13.7 47.6 17 53.2",
    stroke: bg,
    strokeWidth: "2.6",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M41.8 12.8C47.1 19.5 50 27.2 50.8 35.3C51.4 41.4 50.1 47.6 46.8 53.2",
    stroke: bg,
    strokeWidth: "2.6",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M32.2 22.2C27.8 28.1 25.9 34.5 26.5 41.7C27 47 28.7 51.7 32 56.4",
    stroke: bg,
    strokeWidth: "3.2",
    strokeLinecap: "round"
  }), /*#__PURE__*/React.createElement("path", {
    d: "M27.8 58.4C28.8 60.2 30.4 61.2 32 61.4C33.6 61.2 35.2 60.2 36.2 58.4",
    stroke: bg,
    strokeWidth: "2.6",
    strokeLinecap: "round"
  })));
};
window.Icon = Icon;
window.NoriLogo = NoriLogo;
/* ─── Home Page ─── */

const useViewport = () => {
  const [width, setWidth] = React.useState(() => window.innerWidth);
  React.useEffect(() => {
    const onResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);
  return {
    width,
    isCompact: width < 1180,
    isTablet: width < 980,
    isMobile: width < 760
  };
};
const PlatformLogo = ({
  kind,
  size = 20
}) => {
  const base = {
    width: size,
    height: size,
    borderRadius: size * 0.32,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    flexShrink: 0
  };
  if (kind === 'xhs') {
    return /*#__PURE__*/React.createElement("span", {
      style: {
        ...base,
        background: '#ff2442',
        color: '#fff',
        fontSize: size * 0.36,
        fontWeight: 800,
        letterSpacing: 0,
        boxShadow: 'inset 0 1px 0 rgba(255,255,255,.24)'
      }
    }, "RED");
  }
  if (kind === 'dy') {
    return /*#__PURE__*/React.createElement("span", {
      style: {
        ...base,
        background: '#111',
        padding: 0
      }
    }, /*#__PURE__*/React.createElement("img", {
      src: "/Users/holly/Downloads/vecteezy_tiktok-png-icon_16716450.png",
      alt: "Douyin",
      style: {
        width: '100%',
        height: '100%',
        objectFit: 'cover'
      }
    }));
  }
  if (kind === 'bili') {
    return /*#__PURE__*/React.createElement("span", {
      style: {
        ...base,
        background: '#ffffff',
        color: '#fb7299',
        border: '1px solid rgba(251,114,153,.18)',
        boxShadow: '0 2px 8px rgba(251,114,153,.12)'
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "bilibili",
      size: size * 0.76,
      color: "currentColor"
    }));
  }
  return /*#__PURE__*/React.createElement("span", {
    style: {
      ...base,
      background: T.success,
      color: '#fff',
      fontSize: size * 0.52,
      fontWeight: 800
    }
  }, "\u5FAE");
};
const Sidebar = ({
  active,
  onNew,
  onNavigate = () => {},
  sessions = [],
  collapsed = false,
  onToggle = () => {}
}) => {
  return /*#__PURE__*/React.createElement("aside", {
    style: {
      width: collapsed ? 82 : 244,
      flexShrink: 0,
      background: 'linear-gradient(180deg, rgba(250,252,254,.98), rgba(246,249,252,.94))',
      display: 'flex',
      flexDirection: 'column',
      padding: collapsed ? '16px 12px' : '20px 16px',
      height: '100%',
      borderRight: `1px solid ${T.hairlineSoft}`,
      boxShadow: '12px 0 34px rgba(14,14,44,.035)',
      transition: 'width .24s cubic-bezier(.2,.8,.2,1), padding .24s cubic-bezier(.2,.8,.2,1)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      justifyContent: collapsed ? 'center' : 'flex-start',
      padding: collapsed ? '4px 2px 20px' : '4px 10px 20px'
    }
  }, !collapsed && /*#__PURE__*/React.createElement(NoriLogo, {
    size: 28
  }), !collapsed && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 18,
      fontWeight: 700,
      letterSpacing: '-0.02em'
    }
  }, "Nori"), /*#__PURE__*/React.createElement("button", {
    onClick: onToggle,
    "aria-label": collapsed ? '展开导航栏' : '收起导航栏',
    style: {
      marginLeft: collapsed ? 0 : 'auto',
      width: 40,
      height: 40,
      borderRadius: 14,
      border: `1px solid ${T.hairline}`,
      background: 'rgba(255,255,255,.82)',
      color: T.navyLight,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      cursor: 'pointer',
      boxShadow: collapsed ? T.shadowSm : 'inset 0 1px 0 rgba(255,255,255,.72)',
      transition: 'transform .16s cubic-bezier(.2,.8,.2,1), box-shadow .16s cubic-bezier(.2,.8,.2,1), background .16s'
    },
    onMouseEnter: e => {
      e.currentTarget.style.transform = 'translateY(-1px)';
      e.currentTarget.style.boxShadow = T.shadowSm;
    },
    onMouseLeave: e => {
      e.currentTarget.style.transform = 'translateY(0)';
      e.currentTarget.style.boxShadow = collapsed ? T.shadowSm : 'inset 0 1px 0 rgba(255,255,255,.72)';
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "splitView",
    size: 18,
    color: "currentColor"
  }))), /*#__PURE__*/React.createElement("button", {
    onClick: () => onNew && onNew(),
    style: {
      height: collapsed ? 48 : 40,
      borderRadius: collapsed ? 16 : 10,
      border: `1px solid ${T.hairline}`,
      background: T.white,
      color: T.navy,
      display: 'flex',
      alignItems: 'center',
      justifyContent: collapsed ? 'center' : 'space-between',
      padding: collapsed ? 0 : '0 14px',
      fontSize: 13,
      fontWeight: 500,
      cursor: 'pointer',
      marginBottom: 18,
      boxShadow: collapsed ? T.shadowSm : T.shadowXs,
      transition: 'all .15s'
    },
    onMouseEnter: e => e.currentTarget.style.background = T.surface,
    onMouseLeave: e => e.currentTarget.style.background = T.white
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "edit",
    size: collapsed ? 18 : 15,
    color: T.navyMid
  }), !collapsed && /*#__PURE__*/React.createElement("span", null, "\u65B0\u5EFA\u5BF9\u8BDD")), !collapsed && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 10,
      fontFamily: T.fontMono,
      color: T.navyLight,
      background: T.surface,
      padding: '2px 5px',
      borderRadius: 3
    }
  }, "\u2318K")), /*#__PURE__*/React.createElement("nav", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 1
    }
  }, [{
    id: 'home',
    label: '首页',
    icon: 'home'
  }, {
    id: 'library',
    label: '我的内容库',
    icon: 'library'
  }, {
    id: 'skills',
    label: 'Skill 广场',
    icon: 'sparkles'
  }, {
    id: 'insights',
    label: '账号洞察',
    icon: 'chart'
  }].map(item => /*#__PURE__*/React.createElement("a", {
    key: item.id,
    href: "#",
    onClick: e => {
      e.preventDefault();
      onNavigate(item.id);
    },
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: collapsed ? 0 : 10,
      justifyContent: collapsed ? 'center' : 'flex-start',
      padding: collapsed ? '0' : '8px 10px',
      height: collapsed ? 48 : 'auto',
      borderRadius: collapsed ? 16 : 8,
      fontSize: 13,
      fontWeight: active === item.id ? 600 : 500,
      color: active === item.id ? T.navy : T.navyMid,
      background: active === item.id ? T.surface : 'transparent',
      textDecoration: 'none',
      transition: 'all .12s',
      marginBottom: collapsed ? 8 : 0,
      boxShadow: collapsed && active === item.id ? 'inset 0 1px 0 rgba(255,255,255,.65)' : 'none'
    },
    onMouseEnter: e => {
      if (active !== item.id) e.currentTarget.style.background = 'rgba(14,14,44,.03)';
    },
    onMouseLeave: e => {
      if (active !== item.id) e.currentTarget.style.background = 'transparent';
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: item.icon,
    size: collapsed ? 18 : 16,
    color: active === item.id ? T.navy : T.navyLight
  }), !collapsed && item.label))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 24,
      flex: 1,
      overflow: 'hidden',
      display: 'flex',
      flexDirection: 'column'
    }
  }, !collapsed && /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 10,
      fontWeight: 600,
      letterSpacing: '0.1em',
      textTransform: 'uppercase',
      color: T.navyLight,
      padding: '0 10px 8px'
    }
  }, "\u6700\u8FD1\u521B\u4F5C"), !collapsed && /*#__PURE__*/React.createElement("div", {
    style: {
      overflowY: 'auto',
      display: 'flex',
      flexDirection: 'column',
      gap: 1
    }
  }, sessions.map((s, i) => /*#__PURE__*/React.createElement("a", {
    key: i,
    href: "#",
    style: {
      padding: collapsed ? '9px 0' : '7px 10px',
      borderRadius: 6,
      fontSize: 12.5,
      color: T.navyMid,
      fontWeight: 450,
      textDecoration: 'none',
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      transition: 'background .12s',
      textAlign: collapsed ? 'center' : 'left'
    },
    onMouseEnter: e => e.currentTarget.style.background = 'rgba(14,14,44,.03)',
    onMouseLeave: e => e.currentTarget.style.background = 'transparent'
  }, collapsed ? `${i + 1}` : s)))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      justifyContent: collapsed ? 'center' : 'flex-start',
      padding: collapsed ? '8px 0' : '10px',
      borderRadius: collapsed ? 16 : 10,
      marginTop: 12,
      cursor: 'pointer',
      transition: 'background .12s'
    },
    onMouseEnter: e => e.currentTarget.style.background = T.surface,
    onMouseLeave: e => e.currentTarget.style.background = 'transparent'
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: collapsed ? 42 : 30,
      height: collapsed ? 42 : 30,
      borderRadius: '50%',
      background: `linear-gradient(135deg, ${T.iris}, ${T.peach})`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: T.white,
      fontSize: collapsed ? 13 : 12,
      fontWeight: 700,
      boxShadow: collapsed ? T.shadowSm : 'none'
    }
  }, "L"), !collapsed && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      minWidth: 0,
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12.5,
      fontWeight: 600,
      color: T.navy
    }
  }, "Luna"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 10.5,
      color: T.navyLight
    }
  }, "Pro \xB7 87 / 200 \u6B21")), !collapsed && /*#__PURE__*/React.createElement(Icon, {
    name: "moreH",
    size: 14,
    color: T.navyLight
  })));
};
const HeroHeadline = ({
  compact,
  mobile
}) => {
  const [bursting, setBursting] = React.useState(false);
  const timerRef = React.useRef(null);
  const headlineSize = mobile ? 27 : compact ? 35 : 42;
  const serifSize = mobile ? 31 : compact ? 39 : 46;
  const particles = [{
    type: 'platform',
    kind: 'dy',
    x: '-190px',
    y: '-70px',
    mx: '-98px',
    my: '-58px',
    r: '-8deg',
    delay: 40,
    size: 24
  }, {
    type: 'platform',
    kind: 'xhs',
    x: '188px',
    y: '-78px',
    mx: '94px',
    my: '-64px',
    r: '8deg',
    delay: 150,
    size: 24
  }, {
    type: 'platform',
    kind: 'bili',
    x: '220px',
    y: '52px',
    mx: '102px',
    my: '44px',
    r: '-7deg',
    delay: 250,
    size: 24
  }, {
    type: 'icon',
    icon: 'sparkles',
    color: T.primary,
    x: '-110px',
    y: '-104px',
    mx: '-54px',
    my: '-94px',
    r: '-16deg',
    delay: 0,
    size: 13
  }, {
    type: 'icon',
    icon: 'star',
    color: T.iris,
    x: '84px',
    y: '-110px',
    mx: '42px',
    my: '-102px',
    r: '12deg',
    delay: 90,
    size: 12
  }, {
    type: 'icon',
    icon: 'sparkle',
    color: T.peach,
    x: '-218px',
    y: '64px',
    mx: '-112px',
    my: '58px',
    r: '18deg',
    delay: 185,
    size: 12
  }, {
    type: 'icon',
    icon: 'sparkle',
    color: T.success,
    x: '296px',
    y: '-12px',
    mx: '118px',
    my: '-8px',
    r: '14deg',
    delay: 290,
    size: 12
  }, {
    type: 'onion',
    x: '-42px',
    y: '90px',
    mx: '-18px',
    my: '82px',
    r: '10deg',
    delay: 340,
    size: 19
  }];
  const triggerBurst = React.useCallback(() => {
    window.clearTimeout(timerRef.current);
    setBursting(false);
    requestAnimationFrame(() => {
      setBursting(true);
      timerRef.current = window.setTimeout(() => setBursting(false), 1850);
    });
  }, []);
  React.useEffect(() => () => window.clearTimeout(timerRef.current), []);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      width: '100%',
      marginBottom: mobile ? 20 : 28
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: '50%',
      top: mobile ? '44%' : '48%',
      width: mobile ? 260 : 520,
      height: mobile ? 150 : 260,
      borderRadius: '50%',
      background: `radial-gradient(circle, rgba(214,255,0,.17), rgba(243,217,218,.13) 42%, rgba(75,77,237,.10) 66%, transparent 72%)`,
      opacity: bursting ? .78 : .48,
      transform: 'translate3d(-50%, -50%, 0)',
      filter: 'blur(18px)',
      pointerEvents: 'none',
      animation: bursting ? 'heroHalo 1.5s ease-out' : 'none'
    }
  }), particles.map((item, index) => {
    const endX = mobile ? item.mx : item.x;
    const endY = mobile ? item.my : item.y;
    return /*#__PURE__*/React.createElement("div", {
      key: `${item.type}-${index}`,
      style: {
        '--burst-x': endX,
        '--burst-y': endY,
        '--burst-end-x': endX,
        '--burst-end-y': endY,
        '--burst-r': item.r,
        position: 'absolute',
        left: '50%',
        top: '48%',
        zIndex: 4,
        opacity: 0,
        pointerEvents: 'none',
        animation: bursting ? `heroSpark .92s ${item.delay}ms cubic-bezier(.18,.86,.28,1) forwards` : 'none'
      }
    }, item.type === 'platform' ? /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: mobile ? '6px' : '7px',
        borderRadius: 999,
        background: 'rgba(255,255,255,.74)',
        border: '1px solid rgba(255,255,255,.78)',
        boxShadow: '0 12px 34px rgba(14,14,44,.10), inset 0 1px 0 rgba(255,255,255,.72)',
        backdropFilter: 'blur(18px) saturate(1.4)'
      }
    }, /*#__PURE__*/React.createElement(PlatformLogo, {
      kind: item.kind,
      size: mobile ? 20 : item.size
    })) : item.type === 'onion' ? /*#__PURE__*/React.createElement("div", {
      style: {
        padding: 4,
        borderRadius: 12,
        background: 'rgba(255,255,255,.66)',
        border: '1px solid rgba(255,255,255,.74)',
        boxShadow: T.shadowSm,
        backdropFilter: 'blur(14px)'
      }
    }, /*#__PURE__*/React.createElement(NoriLogo, {
      size: item.size
    })) : /*#__PURE__*/React.createElement("span", {
      style: {
        width: item.size + 16,
        height: item.size + 16,
        borderRadius: 999,
        background: 'rgba(255,255,255,.68)',
        border: '1px solid rgba(255,255,255,.76)',
        boxShadow: T.shadowSm,
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: item.color,
        backdropFilter: 'blur(14px)'
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: item.icon,
      size: item.size,
      color: item.color
    })));
  }), /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: triggerBurst,
    "aria-label": "Play Nori slogan animation",
    style: {
      position: 'relative',
      zIndex: 2,
      width: '100%',
      border: 'none',
      background: 'transparent',
      padding: mobile ? '6px 0 2px' : '8px 0 4px',
      cursor: 'pointer',
      textAlign: 'center',
      WebkitTapHighlightColor: 'transparent'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 8,
      padding: mobile ? '6px 10px' : '7px 12px',
      marginBottom: mobile ? 16 : 20,
      borderRadius: 999,
      background: 'rgba(255,255,255,.66)',
      border: '1px solid rgba(255,255,255,.78)',
      boxShadow: '0 10px 28px rgba(14,14,44,.07), inset 0 1px 0 rgba(255,255,255,.7)',
      backdropFilter: 'blur(20px) saturate(1.35)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 7,
      height: 7,
      borderRadius: '50%',
      background: bursting ? T.success : T.primary,
      boxShadow: bursting ? `0 0 0 6px rgba(49,208,170,.13)` : `0 0 0 6px rgba(214,255,0,.14)`,
      transition: 'background .28s ease, box-shadow .28s ease'
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 10.5,
      fontWeight: 650,
      letterSpacing: 0,
      textTransform: 'uppercase',
      color: T.navyMid
    }
  }, "Nori creative OS")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      gap: mobile ? 2 : 6,
      maxWidth: mobile ? 324 : 720,
      margin: '0 auto',
      fontSize: headlineSize,
      lineHeight: mobile ? 1.08 : 1.01,
      letterSpacing: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: mobile ? 9 : 12,
      flexWrap: 'wrap',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: T.fontSans,
      fontWeight: 560,
      color: 'rgba(14,14,44,.72)',
      textShadow: bursting ? '0 0 14px rgba(214,255,0,.34), 0 0 32px rgba(214,255,0,.16)' : 'none',
      animation: bursting ? 'sloganSoftGlow .9s ease-out 2' : 'none',
      transition: 'color .34s ease, text-shadow .34s ease'
    }
  }, "From one"), /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'relative',
      fontFamily: T.fontSerif,
      fontSize: serifSize,
      fontWeight: 520,
      fontStyle: 'italic',
      color: T.navy,
      textShadow: bursting ? '0 0 22px rgba(75,77,237,.34)' : '0 18px 42px rgba(14,14,44,.08)',
      animation: bursting ? 'sloganSoftGlow .9s ease-out 2' : 'none',
      transition: 'color .34s ease, text-shadow .34s ease'
    }
  }, "idea", /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      right: mobile ? -8 : -11,
      top: mobile ? 0 : 2,
      color: bursting ? T.peach : T.peach,
      opacity: bursting ? 1 : .7,
      animation: bursting ? 'heroGlint .48s ease-out 2' : 'pulse 2.4s ease-in-out infinite'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "sparkles",
    size: mobile ? 10 : 12,
    color: "currentColor"
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'baseline',
      gap: mobile ? 9 : 12,
      flexWrap: 'wrap',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: T.fontSans,
      fontWeight: 520,
      color: T.iris,
      textShadow: bursting ? '0 0 18px rgba(75,77,237,.38), 0 0 38px rgba(75,77,237,.18)' : '0 10px 30px rgba(75,77,237,.08)',
      animation: bursting ? 'sloganSoftGlow .9s ease-out 2' : 'none',
      transition: 'color .34s ease, text-shadow .34s ease'
    }
  }, "to content"), /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'relative',
      fontFamily: T.fontSerif,
      fontSize: serifSize,
      fontWeight: 560,
      color: T.navy,
      textShadow: bursting ? '0 0 22px rgba(49,208,170,.34)' : 'none',
      animation: bursting ? 'sloganSoftGlow .9s ease-out 2' : 'none',
      transition: 'color .34s ease, text-shadow .34s ease'
    }
  }, "everywhere", /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      left: '8%',
      right: '5%',
      bottom: mobile ? 2 : 4,
      height: mobile ? 8 : 10,
      borderRadius: 999,
      background: bursting ? `linear-gradient(90deg, rgba(214,255,0,.36), rgba(49,208,170,.20), rgba(75,77,237,.20))` : `linear-gradient(90deg, rgba(243,217,218,.34), rgba(214,255,0,.16), rgba(75,77,237,.12))`,
      filter: 'blur(8px)',
      zIndex: -1,
      transition: 'background .34s ease'
    }
  }))))));
};
const FormatTag = ({
  label,
  sub,
  onCancel
}) => /*#__PURE__*/React.createElement("div", {
  style: {
    display: 'inline-flex',
    alignItems: 'center',
    gap: 6,
    padding: '4px 6px 4px 10px',
    borderRadius: 999,
    background: T.irisTint,
    color: T.iris,
    fontSize: 12,
    fontWeight: 600,
    marginBottom: 10
  }
}, label, sub ? ` · ${sub}` : '', /*#__PURE__*/React.createElement("button", {
  onClick: onCancel,
  style: {
    width: 18,
    height: 18,
    borderRadius: '50%',
    border: 'none',
    cursor: 'pointer',
    background: 'rgba(75,77,237,.15)',
    color: T.iris,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center'
  }
}, /*#__PURE__*/React.createElement(Icon, {
  name: "close",
  size: 10,
  stroke: 2.4
})));
const HomeComposer = ({
  value,
  onChange,
  onSubmit,
  format,
  onClearFormat,
  compact,
  mobile
}) => {
  const [focused, setFocused] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      background: 'linear-gradient(180deg, rgba(255,255,255,.94), rgba(255,255,255,.88))',
      borderRadius: mobile ? 22 : 28,
      border: `1px solid ${focused ? 'rgba(75,77,237,.24)' : 'rgba(14,14,44,.06)'}`,
      boxShadow: focused ? `0 0 0 4px rgba(75,77,237,.10), 0 32px 80px rgba(14,14,44,.10), ${T.shadowLg}` : '0 28px 80px rgba(14,14,44,.08), 0 6px 18px rgba(14,14,44,.04)',
      padding: mobile ? '16px 16px 12px' : compact ? '18px 18px 14px' : '20px 22px 14px',
      transition: 'border .18s, box-shadow .18s, transform .18s',
      backdropFilter: 'blur(20px)',
      overflow: 'hidden',
      animation: focused ? 'prismBorder 2.8s ease-in-out infinite' : 'none'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      background: 'radial-gradient(circle at 14% 12%, rgba(214,255,0,.12), transparent 30%), radial-gradient(circle at 88% 14%, rgba(75,77,237,.08), transparent 22%)',
      pointerEvents: 'none'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      zIndex: 1
    }
  }, format && /*#__PURE__*/React.createElement(FormatTag, {
    label: format.label,
    sub: format.sub,
    onCancel: onClearFormat
  }), /*#__PURE__*/React.createElement("textarea", {
    value: value,
    onChange: e => onChange(e.target.value),
    onFocus: () => setFocused(true),
    onBlur: () => setFocused(false),
    onKeyDown: e => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (value.trim()) onSubmit();
      }
    },
    placeholder: "Share one idea. Nori turns it into content everywhere...",
    rows: mobile ? 3 : 2,
    style: {
      width: '100%',
      border: 'none',
      outline: 'none',
      background: 'transparent',
      resize: 'none',
      fontSize: mobile ? 16 : 17,
      fontWeight: 450,
      lineHeight: 1.55,
      color: T.navy,
      fontFamily: T.fontSans,
      minHeight: mobile ? 84 : 74,
      maxHeight: 180
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: mobile ? 'stretch' : 'center',
      justifyContent: 'space-between',
      gap: 10,
      marginTop: 4,
      flexDirection: mobile ? 'column' : 'row'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 6,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement(ToolPill, {
    icon: "paperclip",
    label: "Attach"
  }), /*#__PURE__*/React.createElement(ToolPill, {
    icon: "globe",
    label: "Search",
    active: true
  }), /*#__PURE__*/React.createElement(ToolPill, {
    icon: "sparkles",
    label: "Refine"
  })), /*#__PURE__*/React.createElement("button", {
    onClick: () => value.trim() && onSubmit(),
    disabled: !value.trim(),
    style: {
      width: mobile ? '100%' : 42,
      height: 42,
      borderRadius: mobile ? 999 : '50%',
      border: 'none',
      cursor: value.trim() ? 'pointer' : 'not-allowed',
      background: value.trim() ? T.navy : 'rgba(14,14,44,.08)',
      color: value.trim() ? T.white : T.navyLight,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: 8,
      boxShadow: value.trim() ? '0 10px 24px rgba(14,14,44,.18)' : 'none',
      transition: 'all .15s'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "paperPlane",
    size: 15,
    stroke: 2
  }), mobile && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      fontWeight: 600
    }
  }, "Start crafting")))));
};
const FormatPicker = ({
  format,
  onPick,
  compact,
  mobile
}) => {
  const [openCat, setOpenCat] = React.useState(null);
  const cats = [{
    key: 'xhs',
    icon: 'image',
    label: '小红书图文'
  }, {
    key: 'wechat',
    icon: 'document',
    label: '公众号长文'
  }, {
    key: 'video',
    icon: 'video',
    label: '抖音短视频'
  }];
  const subs = {
    xhs: ['爆款种草', '攻略干货', '生活记录', '产品测评'],
    wechat: ['深度长文', '观点专栏', '人物访谈', '行业分析'],
    video: ['科普视频', '产品宣传', '漫剧', '口播']
  };
  const current = openCat ? cats.find(c => c.key === openCat) : null;
  return /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: 8,
      justifyContent: mobile ? 'center' : 'flex-start'
    }
  }, cats.map(c => {
    const isOpen = openCat === c.key;
    const isPicked = format && format.cat === c.key;
    return /*#__PURE__*/React.createElement("button", {
      key: c.key,
      onClick: () => setOpenCat(isOpen ? null : c.key),
      style: {
        minHeight: 36,
        padding: compact ? '0 12px' : '0 14px',
        borderRadius: 99,
        border: `1px solid ${isOpen || isPicked ? 'rgba(14,14,44,.44)' : T.hairline}`,
        background: isOpen || isPicked ? T.navy : 'rgba(255,255,255,.88)',
        color: isOpen || isPicked ? T.white : T.navyMid,
        fontSize: 13,
        fontWeight: 520,
        cursor: 'pointer',
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        transition: 'all .15s',
        backdropFilter: 'blur(10px)'
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: c.icon,
      size: 14
    }), c.label);
  })), current && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 10,
      display: 'flex',
      flexWrap: 'wrap',
      gap: 8,
      animation: 'fadeIn .2s ease',
      justifyContent: mobile ? 'center' : 'flex-start'
    }
  }, subs[current.key].map((s, i) => /*#__PURE__*/React.createElement("button", {
    key: i,
    onClick: () => {
      onPick({
        cat: current.key,
        label: current.label,
        sub: s
      });
      setOpenCat(null);
    },
    style: {
      background: 'rgba(255,255,255,.9)',
      border: `1px solid ${T.hairline}`,
      borderRadius: 14,
      padding: '10px 14px',
      textAlign: 'left',
      cursor: 'pointer',
      display: 'flex',
      flexDirection: 'column',
      gap: 2,
      minWidth: mobile ? 136 : 148,
      transition: 'all .15s',
      boxShadow: T.shadowXs
    },
    onMouseEnter: e => {
      e.currentTarget.style.borderColor = 'rgba(75,77,237,.4)';
      e.currentTarget.style.transform = 'translateY(-1px)';
    },
    onMouseLeave: e => {
      e.currentTarget.style.borderColor = T.hairline;
      e.currentTarget.style.transform = 'translateY(0)';
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: T.navy
    }
  }, s), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 11,
      color: T.navyLight
    }
  }, current.label, " \xB7 ", s)))));
};
const ToolPill = ({
  icon,
  label,
  active
}) => {
  const [hov, setHov] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    onMouseEnter: () => setHov(true),
    onMouseLeave: () => setHov(false),
    style: {
      height: 30,
      padding: '0 10px',
      borderRadius: 99,
      background: active ? T.irisTint : hov ? T.surface : 'transparent',
      border: `1px solid ${active ? 'transparent' : hov ? 'transparent' : T.hairline}`,
      color: active ? T.iris : T.navyMid,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 5,
      fontSize: 12,
      fontWeight: 500,
      cursor: 'pointer',
      transition: 'all .12s'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: icon,
    size: 13
  }), label);
};
const InspirationPhoto = ({
  src,
  shape,
  rotate = 0,
  height
}) => {
  const clipPaths = {
    petal: 'polygon(12% 16%, 34% 9%, 46% 0%, 60% 12%, 81% 8%, 100% 22%, 93% 44%, 100% 71%, 82% 88%, 61% 84%, 44% 100%, 22% 92%, 0% 74%, 7% 48%, 0% 24%)',
    ribbon: 'polygon(6% 7%, 44% 0%, 64% 9%, 100% 4%, 90% 38%, 100% 65%, 83% 100%, 46% 92%, 26% 100%, 0% 81%, 9% 48%, 0% 17%)',
    bloom: 'polygon(11% 0%, 38% 8%, 58% 0%, 74% 15%, 100% 17%, 94% 50%, 100% 80%, 76% 100%, 49% 93%, 30% 100%, 0% 82%, 8% 51%, 0% 18%)'
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%',
      height,
      transform: `rotate(${rotate}deg)`,
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%',
      height: '100%',
      clipPath: clipPaths[shape] || clipPaths.petal,
      overflow: 'hidden',
      boxShadow: '0 20px 36px rgba(14,14,44,.12)'
    }
  }, /*#__PURE__*/React.createElement("img", {
    src: src,
    alt: "",
    style: {
      width: '100%',
      height: '100%',
      objectFit: 'cover'
    }
  })));
};
const QuickStart = ({
  onPick,
  compact,
  mobile
}) => {
  const shelves = [[{
    title: '阳台植物的情绪版改造',
    desc: '从一个小阳台出发，延展成封面、图文和短视频脚本。',
    tint: '#fcf6f6',
    accent: '#aa2e3d',
    tag: 'Balcony Reset',
    platform: 'dy',
    photo: 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=900&q=80',
    shape: 'ribbon',
    rotate: -5
  }, {
    title: '当家居博主爱上拼豆后',
    desc: '把手作过程变成更有记忆点的生活方式内容。',
    tint: '#f8fbf3',
    accent: '#736e00',
    tag: 'Craft Loop',
    platform: 'xhs',
    photo: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80',
    shape: 'petal',
    rotate: 4
  }, {
    title: '深夜食堂里的治愈系主厨',
    desc: '从一碗热汤，做出一整套有人情味的社媒叙事。',
    tint: '#f7f6ff',
    accent: '#4950a5',
    tag: 'Warm Series',
    platform: 'bili',
    photo: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80',
    shape: 'bloom',
    rotate: -3
  }, {
    title: '职场人的知识 IP 变现路径',
    desc: '把五年经验整理成会传播、可连载的知识内容。',
    tint: '#f5f8fc',
    accent: '#21489e',
    tag: 'Pro Story',
    platform: 'dy',
    photo: 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=900&q=80',
    shape: 'petal',
    rotate: 3
  }], [{
    title: '猫咪日常也能拍出栏目感',
    desc: '把碎片化生活切成固定栏目，轻松做持续更新。',
    tint: '#fcf8f3',
    accent: '#8e4e00',
    tag: 'Soft Habit',
    platform: 'xhs',
    photo: 'https://images.unsplash.com/photo-1519052537078-e6302a4968d4?auto=format&fit=crop&w=900&q=80',
    shape: 'bloom',
    rotate: -4
  }, {
    title: 'City Walk 变成城市策展笔记',
    desc: '不是打卡清单，而是有审美和路线逻辑的内容包。',
    tint: '#fcf6fb',
    accent: '#7e3d79',
    tag: 'Urban Edit',
    platform: 'bili',
    photo: 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80',
    shape: 'ribbon',
    rotate: 5
  }, {
    title: '咖啡入门 12 个名词',
    desc: '做成对新手友好的知识卡片和短内容矩阵。',
    tint: '#fbf8f2',
    accent: '#8d6d38',
    tag: 'Starter Pack',
    platform: 'dy',
    photo: 'https://images.unsplash.com/photo-1442512595331-e89e73853f31?auto=format&fit=crop&w=900&q=80',
    shape: 'petal',
    rotate: -3
  }, {
    title: '极简通勤穿搭一周 OOTD',
    desc: '让日常穿搭更像连载内容，而不是单条记录。',
    tint: '#f5f7fd',
    accent: '#4868a5',
    tag: 'Week Format',
    platform: 'xhs',
    photo: 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=900&q=80',
    shape: 'bloom',
    rotate: 2
  }], [{
    title: '租房避雷指南 v2',
    desc: '把经验帖升级成更有结构、更有分享欲的攻略。',
    tint: '#f6f7fd',
    accent: '#4c5eb3',
    tag: 'Field Notes',
    platform: 'bili',
    photo: 'https://images.unsplash.com/photo-1460317442991-0ec209397118?auto=format&fit=crop&w=900&q=80',
    shape: 'petal',
    rotate: -4
  }, {
    title: 'AI 视频工具横评',
    desc: '从工具参数转成更适合传播的体验型结论。',
    tint: '#f6fbf6',
    accent: '#48762d',
    tag: 'Tool Review',
    platform: 'dy',
    photo: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80',
    shape: 'bloom',
    rotate: 4
  }, {
    title: '品牌主理人的幕后手帐',
    desc: '把产品思考、开会片段和灵感卡片织成系列。',
    tint: '#fcf7f3',
    accent: '#9a5426',
    tag: 'Behind Scene',
    platform: 'xhs',
    photo: 'https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=900&q=80',
    shape: 'ribbon',
    rotate: -2
  }, {
    title: '健身猛男为什么爱粉色植物',
    desc: '反差感、观点感和视觉记忆点一次给足。',
    tint: '#fafbf2',
    accent: '#7d5a00',
    tag: 'Contrast Hook',
    platform: 'bili',
    photo: 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80',
    shape: 'petal',
    rotate: 3
  }]];
  const [shelfIndex, setShelfIndex] = React.useState(0);
  const [animateKey, setAnimateKey] = React.useState(0);
  const items = shelves[shelfIndex];
  const layout = mobile ? '1fr' : compact ? 'repeat(2, minmax(0, 1fr))' : 'repeat(4, minmax(0, 1fr))';
  const refreshShelf = () => {
    setShelfIndex(prev => (prev + 1) % shelves.length);
    setAnimateKey(prev => prev + 1);
  };
  return /*#__PURE__*/React.createElement("section", {
    style: {
      padding: mobile ? '6px 0 6px' : '10px 0 4px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: mobile ? 'flex-start' : 'center',
      justifyContent: 'space-between',
      gap: 14,
      flexWrap: 'wrap',
      marginBottom: 18
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      color: T.navyLight,
      marginBottom: 6,
      letterSpacing: '0.08em',
      textTransform: 'uppercase'
    }
  }, "\u5FEB\u901F\u5F00\u59CB"), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: mobile ? 22 : 28,
      fontWeight: 450,
      lineHeight: 1.08,
      letterSpacing: '-0.04em',
      color: T.navy
    }
  }, "Quick Start")), /*#__PURE__*/React.createElement("button", {
    onClick: refreshShelf,
    style: {
      height: 44,
      padding: '0 16px',
      borderRadius: 999,
      border: `1px solid ${T.hairline}`,
      background: 'rgba(255,255,255,.9)',
      color: T.navy,
      fontSize: 14,
      fontWeight: 520,
      cursor: 'pointer',
      display: 'inline-flex',
      alignItems: 'center',
      gap: 8,
      boxShadow: T.shadowSm
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "refresh",
    size: 14
  }), "\u6362\u4E00\u6362")), /*#__PURE__*/React.createElement("div", {
    key: animateKey,
    style: {
      display: 'grid',
      gridTemplateColumns: layout,
      gap: mobile ? 12 : 14,
      alignItems: 'start'
    }
  }, items.map((it, i) => /*#__PURE__*/React.createElement("button", {
    key: `${it.title}-${animateKey}`,
    onClick: () => onPick(it.title),
    style: {
      background: 'transparent',
      border: 'none',
      padding: 0,
      textAlign: 'left',
      cursor: 'pointer',
      animation: `fadeInScale .42s ${i * 60}ms both`
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      borderRadius: mobile ? 20 : 22,
      overflow: 'hidden',
      background: `linear-gradient(180deg, rgba(255,255,255,.96) 0%, ${it.tint} 100%)`,
      border: '1px solid rgba(14,14,44,.05)',
      boxShadow: '0 10px 26px rgba(14,14,44,.06)',
      transition: 'transform .28s cubic-bezier(.2,.8,.2,1), box-shadow .28s cubic-bezier(.2,.8,.2,1)'
    },
    onMouseEnter: e => {
      e.currentTarget.style.transform = 'translateY(-5px) scale(1.005)';
      e.currentTarget.style.boxShadow = '0 18px 34px rgba(14,14,44,.08)';
    },
    onMouseLeave: e => {
      e.currentTarget.style.transform = 'translateY(0) scale(1)';
      e.currentTarget.style.boxShadow = '0 10px 26px rgba(14,14,44,.06)';
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      minHeight: mobile ? 196 : compact ? 202 : 210,
      padding: mobile ? 13 : 14,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      justifyContent: 'space-between',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '7px',
      borderRadius: 999,
      background: 'rgba(255,255,255,.74)',
      backdropFilter: 'blur(8px)'
    }
  }, /*#__PURE__*/React.createElement(PlatformLogo, {
    kind: it.platform,
    size: 18
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      width: 32,
      height: 32,
      borderRadius: 999,
      background: 'rgba(255,255,255,.42)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: T.navy,
      boxShadow: 'inset 0 1px 0 rgba(255,255,255,.35)'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "sparkles",
    size: 13,
    color: "currentColor"
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: mobile ? '4px 4px 0' : '8px 8px 0'
    }
  }, /*#__PURE__*/React.createElement(InspirationPhoto, {
    src: it.photo,
    shape: it.shape,
    rotate: it.rotate,
    height: mobile ? 82 : compact ? 90 : 96
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '0 15px 14px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 10.5,
      fontWeight: 700,
      letterSpacing: '0.12em',
      color: 'rgba(14,14,44,.52)',
      textTransform: 'uppercase',
      marginBottom: 7
    }
  }, it.tag), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 14.5,
      fontWeight: 600,
      color: '#111',
      lineHeight: 1.28,
      marginBottom: 7,
      letterSpacing: '-0.01em'
    }
  }, it.title), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12.5,
      color: 'rgba(14,14,44,.78)',
      lineHeight: 1.54,
      minHeight: mobile ? 'auto' : 42
    }
  }, it.desc), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'flex-end',
      marginTop: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      height: 32,
      padding: '0 12px',
      borderRadius: 999,
      border: '1px solid rgba(14,14,44,.10)',
      background: 'rgba(255,255,255,.82)',
      color: T.navy,
      fontSize: 12,
      fontWeight: 600,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      boxShadow: T.shadowXs
    }
  }, "\u8FDB\u5165", /*#__PURE__*/React.createElement(Icon, {
    name: "arrowRight",
    size: 12
  }))))))))));
};
const SkillSquare = ({
  compact,
  mobile
}) => {
  const skills = [{
    name: '小红书爆款图文',
    author: '@Nori',
    uses: '12.4w',
    tint: '#f6eddc',
    accent: '#bd8e42',
    icon: 'image',
    desc: '标题、封面、内文一体生成，适合做种草和反差感主题。',
    cta: '立即套用'
  }, {
    name: '公众号深度长文',
    author: '@Lina',
    uses: '8.6w',
    tint: '#edf1ff',
    accent: '#5f70d6',
    icon: 'document',
    desc: '更适合观点梳理、深度分析和可读性更强的长文结构。',
    cta: '查看模版'
  }, {
    name: '抖音口播脚本',
    author: '@Theo',
    uses: '6.2w',
    tint: '#efe9ff',
    accent: '#8369da',
    icon: 'video',
    desc: '把观点拆成节奏点、转场和 hook，适配短视频传播。',
    cta: '生成脚本'
  }, {
    name: '封面拆解师',
    author: '@Yuki',
    uses: '3.7w',
    tint: '#e8f4eb',
    accent: '#5f9d73',
    icon: 'palette',
    desc: '从视觉构图、标题布局和色彩关系拆出可复用规律。',
    cta: '打开分析'
  }];
  if (mobile) {
    return /*#__PURE__*/React.createElement("section", {
      style: {
        background: 'rgba(255,255,255,.72)',
        border: `1px solid ${T.hairline}`,
        borderRadius: 24,
        padding: '18px 16px 18px',
        boxShadow: '0 18px 42px rgba(14,14,44,.05)'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        marginBottom: 16
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 12,
        color: T.navyLight,
        marginBottom: 6,
        letterSpacing: '0.08em',
        textTransform: 'uppercase'
      }
    }, "Skill Gallery"), /*#__PURE__*/React.createElement("h3", {
      style: {
        fontSize: 22,
        fontWeight: 450,
        letterSpacing: '-0.04em',
        color: T.navy,
        lineHeight: 1.08
      }
    }, "Browse reusable creative systems")), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'grid',
        gap: 12
      }
    }, skills.map((s, i) => /*#__PURE__*/React.createElement("div", {
      key: i,
      style: {
        background: 'rgba(255,255,255,.88)',
        border: `1px solid ${T.hairline}`,
        borderRadius: 20,
        padding: 14
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        height: 160,
        borderRadius: 18,
        background: `linear-gradient(160deg, rgba(255,255,255,.8), rgba(255,255,255,.2)), ${s.tint}`,
        padding: 16,
        marginBottom: 12,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        width: 38,
        height: 38,
        borderRadius: 12,
        background: 'rgba(255,255,255,.66)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: s.accent
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: s.icon,
      size: 18
    })), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        padding: '6px 10px',
        borderRadius: 999,
        background: 'rgba(255,255,255,.6)',
        color: s.accent,
        fontSize: 11,
        fontWeight: 600,
        alignSelf: 'flex-start'
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "sparkles",
      size: 10,
      color: s.accent
    }), s.uses)), /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 16,
        fontWeight: 600,
        color: T.navy,
        marginBottom: 6
      }
    }, s.name), /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 12.5,
        color: T.navyMid,
        lineHeight: 1.58,
        marginBottom: 10
      }
    }, s.desc), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 11.5,
        color: T.navyLight
      }
    }, s.author), /*#__PURE__*/React.createElement("button", {
      style: {
        border: `1px solid ${T.hairline}`,
        background: T.white,
        borderRadius: 999,
        height: 32,
        padding: '0 12px',
        fontSize: 12,
        fontWeight: 600,
        color: T.navy,
        cursor: 'pointer'
      }
    }, s.cta))))));
  }
  return /*#__PURE__*/React.createElement("section", {
    style: {
      background: 'rgba(255,255,255,.72)',
      border: `1px solid ${T.hairline}`,
      borderRadius: 30,
      padding: compact ? '22px 20px 24px' : '24px 24px 26px',
      boxShadow: '0 18px 42px rgba(14,14,44,.05), inset 0 1px 0 rgba(255,255,255,.7)',
      backdropFilter: 'blur(18px)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: 18,
      gap: 14,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      color: T.navyLight,
      marginBottom: 6,
      letterSpacing: '0.08em',
      textTransform: 'uppercase'
    }
  }, "Skill Gallery"), /*#__PURE__*/React.createElement("h3", {
    style: {
      fontSize: compact ? 24 : 28,
      fontWeight: 450,
      lineHeight: 1.08,
      letterSpacing: '-0.04em',
      color: T.navy
    }
  }, "Browse reusable creative systems")), /*#__PURE__*/React.createElement("a", {
    href: "#",
    style: {
      height: 44,
      padding: '0 16px',
      borderRadius: 999,
      border: `1px solid ${T.hairline}`,
      background: 'rgba(255,255,255,.9)',
      color: T.navy,
      textDecoration: 'none',
      fontSize: 14,
      fontWeight: 520,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 8,
      boxShadow: T.shadowSm
    }
  }, "Browse the skill gallery", /*#__PURE__*/React.createElement(Icon, {
    name: "arrowRight",
    size: 14
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: compact ? 'repeat(2, minmax(0, 1fr))' : '1.35fr repeat(3, minmax(0, 1fr))',
      gap: 18,
      alignItems: 'start'
    }
  }, skills.map((s, i) => {
    const featured = !compact && i === 0;
    return /*#__PURE__*/React.createElement("div", {
      key: i,
      style: {
        gridColumn: featured ? 'span 1' : 'span 1'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        background: 'transparent',
        borderRadius: 24,
        transition: 'transform .28s cubic-bezier(.2,.8,.2,1)',
        cursor: 'pointer'
      },
      onMouseEnter: e => e.currentTarget.style.transform = 'translateY(-4px)',
      onMouseLeave: e => e.currentTarget.style.transform = 'translateY(0)'
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        height: featured ? 280 : compact ? 220 : 250,
        borderRadius: 24,
        background: `linear-gradient(160deg, rgba(255,255,255,.82), rgba(255,255,255,.18)), ${s.tint}`,
        border: `1px solid rgba(14,14,44,.06)`,
        boxShadow: '0 8px 22px rgba(14,14,44,.05)',
        overflow: 'hidden',
        padding: 18,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'space-between',
        gap: 10
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        width: 40,
        height: 40,
        borderRadius: 14,
        background: 'rgba(255,255,255,.66)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: s.accent
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: s.icon,
      size: 18
    })), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        padding: '7px 10px',
        borderRadius: 999,
        background: 'rgba(255,255,255,.58)',
        color: s.accent,
        fontSize: 11,
        fontWeight: 600
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "sparkles",
      size: 10,
      color: s.accent
    }), s.uses)), /*#__PURE__*/React.createElement("div", {
      style: {
        alignSelf: featured ? 'stretch' : 'center',
        height: featured ? 132 : 104,
        borderRadius: 20,
        background: 'rgba(255,255,255,.42)',
        boxShadow: 'inset 0 0 0 1px rgba(255,255,255,.3)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: s.accent
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: featured ? 'layers' : i % 2 === 0 ? 'document' : 'palette',
      size: featured ? 42 : 34
    }))), /*#__PURE__*/React.createElement("div", {
      style: {
        padding: '14px 6px 0'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: 10,
        marginBottom: 8
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: featured ? 18 : 16,
        fontWeight: 600,
        color: T.navy,
        lineHeight: 1.2
      }
    }, s.name), !featured && /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 11.5,
        color: T.navyLight
      }
    }, s.author)), /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: featured ? 13.5 : 12.5,
        color: T.navyMid,
        lineHeight: 1.58,
        marginBottom: 12
      }
    }, s.desc), /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        gap: 10
      }
    }, featured ? /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 12,
        color: T.navyLight
      }
    }, s.author) : /*#__PURE__*/React.createElement("span", null), /*#__PURE__*/React.createElement("button", {
      style: {
        border: `1px solid ${T.hairline}`,
        background: T.white,
        borderRadius: 999,
        height: 34,
        padding: '0 12px',
        fontSize: 12,
        fontWeight: 600,
        color: T.navy,
        cursor: 'pointer',
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6
      }
    }, s.cta, /*#__PURE__*/React.createElement(Icon, {
      name: "arrowRight",
      size: 12
    }))))));
  })));
};
const HomePage = ({
  onSubmit,
  onOpenAssets,
  onOpenSkills,
  onOpenInsights
}) => {
  const {
    isCompact,
    isTablet,
    isMobile
  } = useViewport();
  const [text, setText] = React.useState('');
  const [format, setFormat] = React.useState(null);
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const submit = () => {
    if (text.trim()) {
      onSubmit(format ? `[${format.label} · ${format.sub}] ${text.trim()}` : text.trim());
    }
  };
  const sessions = ['猛男喜欢的粉色植物 · 小红书图文', '上海咖啡馆 City Walk Top 10', '租房避雷指南 v2', '产品测评 · AI 视频工具横评', '极简通勤穿搭一周 OOTD', '咖啡入门 12 个名词', '我和我的猫 · 7 个瞬间'];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      height: '100%',
      width: '100%',
      background: 'linear-gradient(180deg, #f8fbfd 0%, #ffffff 100%)',
      padding: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flex: 1,
      background: 'transparent',
      borderRadius: 0,
      boxShadow: 'none',
      overflow: 'hidden'
    }
  }, !isTablet && /*#__PURE__*/React.createElement(Sidebar, {
    active: "home",
    onNew: () => {
      setNavCollapsed(true);
      onSubmit('');
    },
    onNavigate: id => {
      if (id === 'home') return;
      if (id === 'library') onOpenAssets && onOpenAssets();
      if (id === 'skills') onOpenSkills && onOpenSkills();
      if (id === 'insights') onOpenInsights && onOpenInsights();
    },
    sessions: sessions,
    collapsed: navCollapsed,
    onToggle: () => setNavCollapsed(v => !v)
  }), /*#__PURE__*/React.createElement("main", {
    style: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      overflow: 'auto',
      position: 'relative',
      background: 'linear-gradient(180deg, #ffffff 0%, #fcfdff 46%, #fafcfe 100%)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      background: 'radial-gradient(circle at 49% 17%, rgba(214,255,0,.18), transparent 14%), radial-gradient(circle at 66% 18%, rgba(75,77,237,.075), transparent 19%), radial-gradient(circle at 36% 23%, rgba(243,217,218,.22), transparent 18%), radial-gradient(circle at 76% 54%, rgba(49,208,170,.055), transparent 21%)',
      pointerEvents: 'none'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      right: isMobile ? -50 : isTablet ? -34 : 72,
      top: isMobile ? 92 : 96,
      width: isMobile ? 112 : 148,
      height: isMobile ? 112 : 148,
      borderRadius: 46,
      opacity: isMobile ? .035 : .045,
      transform: 'rotate(-12deg)',
      pointerEvents: 'none',
      filter: 'blur(.1px)'
    }
  }, /*#__PURE__*/React.createElement("svg", {
    width: "100%",
    height: "100%",
    viewBox: "0 0 64 64",
    fill: "none",
    "aria-hidden": "true"
  }, /*#__PURE__*/React.createElement("path", {
    d: "M31.8 5.5L36.4 13.3L41 5.8C44 12.2 49.9 17.8 54.2 26.6C59.1 36.6 56.8 48.8 48.2 56C43.6 59.9 38 62 32 62C26 62 20.4 59.9 15.8 56C7.2 48.8 4.9 36.6 9.8 26.6C14.2 17.7 19.8 12 22.8 5.7C24.6 9 25.8 11.8 26.6 15.1C27.9 10.6 29.4 7.7 31.8 5.5Z",
    fill: T.navy
  }), /*#__PURE__*/React.createElement("path", {
    d: "M31.5 14.5C26.6 19.7 23.4 26.3 22 33.4C20.6 40.2 21.2 47.3 24 53.6M22 12.8C16.7 19.5 13.8 27.2 13 35.3C12.4 41.4 13.7 47.6 17 53.2M41.8 12.8C47.1 19.5 50 27.2 50.8 35.3C51.4 41.4 50.1 47.6 46.8 53.2",
    stroke: "#fff",
    strokeWidth: "2.4",
    strokeLinecap: "round"
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      height: isMobile ? 58 : 54,
      padding: isMobile ? '0 18px' : '0 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      flexShrink: 0,
      position: 'relative',
      zIndex: 1
    }
  }, isTablet ? /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement(NoriLogo, {
    size: 26
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 15,
      fontWeight: 700,
      color: T.navy
    }
  }, "Nori"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: T.navyLight
    }
  }, "creative system"))) : /*#__PURE__*/React.createElement("div", {
    "aria-hidden": "true",
    style: {
      width: 38,
      height: 38
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 4
    }
  }, /*#__PURE__*/React.createElement("button", {
    style: iconBtnStyle()
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "bell",
    size: 15,
    color: T.navyLight
  })), /*#__PURE__*/React.createElement("button", {
    style: iconBtnStyle()
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "settings",
    size: 15,
    color: T.navyLight
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      maxWidth: isMobile ? '100%' : 1120,
      width: '100%',
      margin: '0 auto',
      padding: isMobile ? '6px 18px 28px' : isTablet ? '18px 28px 42px' : '24px 36px 46px',
      gap: isMobile ? 28 : 34,
      position: 'relative',
      zIndex: 1
    }
  }, /*#__PURE__*/React.createElement("section", {
    style: {
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: isMobile ? '14px 0 0' : '18px 0 0'
    }
  }, /*#__PURE__*/React.createElement(HeroHeadline, {
    compact: isCompact,
    mobile: isMobile
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      width: '100%',
      maxWidth: 880
    }
  }, /*#__PURE__*/React.createElement(HomeComposer, {
    value: text,
    onChange: setText,
    onSubmit: submit,
    format: format,
    onClearFormat: () => setFormat(null),
    compact: isCompact,
    mobile: isMobile
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 14
    }
  }, /*#__PURE__*/React.createElement(FormatPicker, {
    format: format,
    onPick: setFormat,
    compact: isCompact,
    mobile: isMobile
  })))), /*#__PURE__*/React.createElement("section", null, /*#__PURE__*/React.createElement(QuickStart, {
    onPick: t => onSubmit(`帮我做一篇 ${t}`),
    compact: isCompact,
    mobile: isMobile
  }))))));
};
const iconBtnStyle = () => ({
  width: 40,
  height: 40,
  borderRadius: 14,
  border: `1px solid ${T.hairlineSoft}`,
  background: 'rgba(255,255,255,.88)',
  cursor: 'pointer',
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  transition: 'transform .18s cubic-bezier(.2,.8,.2,1), box-shadow .18s cubic-bezier(.2,.8,.2,1), background .18s cubic-bezier(.2,.8,.2,1)',
  boxShadow: '0 8px 18px rgba(14,14,44,.05), inset 0 1px 0 rgba(255,255,255,.72)'
});
window.HomePage = HomePage;
window.Sidebar = Sidebar;
window.iconBtnStyle = iconBtnStyle;

/* ─── Assets Page: saved content library ─── */

const ASSET_ITEMS = [{
  id: 'pink-plants',
  title: '深蓝幕布下的粉蝶兰，谁懂这种反差感？',
  platform: '小红书',
  type: '图文',
  time: '今天 21:18',
  status: '已生成',
  height: 214,
  palette: ['#103f5f', '#1d6f58', '#f4a8bf', '#de7fa3', '#fff8fb'],
  tags: ['粉色植物', '室内绿植']
}, {
  id: 'coffee-walk',
  title: '上海咖啡馆 City Walk Top 10 路线',
  platform: '小红书',
  type: '视频',
  time: '昨天 18:42',
  status: '草稿',
  height: 258,
  palette: ['#d9d0bd', '#7c6b58', '#f3e7d7', '#a47758', '#fffaf2'],
  tags: ['城市漫步', '咖啡馆']
}, {
  id: 'rental-guide',
  title: '租房避雷指南：看房前必须问清楚的 18 件事',
  platform: '公众号',
  type: '纯文字',
  time: '5 月 5 日',
  status: '已发布',
  height: 184,
  palette: ['#f7f9fc', '#d7e0eb', '#4b4ded', '#31d0aa', '#0e0e2c'],
  tags: ['生活经验', '清单']
}, {
  id: 'ai-video-tools',
  title: 'AI 视频工具横评：从脚本到成片的真实体验',
  platform: 'B站',
  type: '视频',
  time: '5 月 4 日',
  status: '已生成',
  height: 244,
  palette: ['#20284a', '#5c66a8', '#f3dbda', '#d6ff00', '#ffffff'],
  tags: ['AI工具', '测评']
}, {
  id: 'ootd',
  title: '极简通勤穿搭一周 OOTD',
  platform: '短视频',
  type: '视频',
  time: '5 月 3 日',
  status: '草稿',
  height: 268,
  palette: ['#e8ebee', '#1d2330', '#b8c2cb', '#f3dbda', '#ffffff'],
  tags: ['穿搭', '通勤']
}, {
  id: 'coffee-terms',
  title: '咖啡入门 12 个名词，一次讲清楚',
  platform: '公众号',
  type: '纯文字',
  time: '5 月 2 日',
  status: '已生成',
  height: 178,
  palette: ['#fffaf2', '#efe1cc', '#8a6545', '#31d0aa', '#0e0e2c'],
  tags: ['知识科普', '咖啡']
}, {
  id: 'cat-moments',
  title: '我和我的猫：7 个适合发图文的生活瞬间',
  platform: '小红书',
  type: '图文',
  time: '4 月 29 日',
  status: '已发布',
  height: 222,
  palette: ['#fdf5f5', '#95a5a6', '#f0b5c8', '#4b4ded', '#ffffff'],
  tags: ['生活记录', '宠物']
}, {
  id: 'product-manager',
  title: '2026 年 AI 产品经理必备能力地图',
  platform: '公众号',
  type: '图文',
  time: '4 月 26 日',
  status: '已生成',
  height: 202,
  palette: ['#ecf1f4', '#c8d8e6', '#4b4ded', '#d6ff00', '#0e0e2c'],
  tags: ['职场', 'AI']
}, {
  id: 'launch-copy',
  title: '新品发布文案：从预热到转化的 5 个版本',
  platform: '小红书',
  type: '纯文字',
  time: '4 月 22 日',
  status: '草稿',
  height: 188,
  palette: ['#ffffff', '#efeefd', '#4b4ded', '#f3dbda', '#0e0e2c'],
  tags: ['营销文案', '发布']
}];
const AssetVisual = ({
  item
}) => {
  if (item.type === '纯文字') {
    return /*#__PURE__*/React.createElement("div", {
      style: {
        height: item.height,
        padding: 15,
        background: `linear-gradient(145deg, ${item.palette[0]}, ${item.palette[1]})`,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        width: 30,
        height: 30,
        borderRadius: 10,
        background: 'rgba(255,255,255,.82)',
        color: item.palette[2],
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: 'inset 0 1px 0 rgba(255,255,255,.72)'
      }
    }, /*#__PURE__*/React.createElement(Icon, {
      name: "document",
      size: 13
    })), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 9.8,
        fontFamily: T.fontMono,
        color: T.navyLight,
        marginBottom: 7
      }
    }, item.platform, " \xB7 TEXT"), /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 16.5,
        lineHeight: 1.24,
        fontWeight: 740,
        color: T.navy,
        letterSpacing: 0
      }
    }, item.title)));
  }
  return /*#__PURE__*/React.createElement("div", {
    style: {
      height: item.height,
      position: 'relative',
      overflow: 'hidden',
      background: item.palette[0]
    }
  }, /*#__PURE__*/React.createElement(FlowerVisual, {
    palette: item.palette
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      background: item.type === '视频' ? 'linear-gradient(180deg, rgba(0,0,0,.02), rgba(0,0,0,.44))' : 'linear-gradient(180deg, rgba(255,255,255,.04), rgba(0,0,0,.32))'
    }
  }), item.type === '视频' && /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: 12,
      top: 12,
      width: 32,
      height: 32,
      borderRadius: '50%',
      background: 'rgba(255,255,255,.86)',
      color: T.navy,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      boxShadow: '0 10px 22px rgba(14,14,44,.14)',
      backdropFilter: 'blur(10px)'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "play",
    size: 12
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: 13,
      right: 13,
      bottom: 13,
      color: T.white
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 5,
      flexWrap: 'wrap',
      marginBottom: 7
    }
  }, item.tags.slice(0, 2).map(tag => /*#__PURE__*/React.createElement("span", {
    key: tag,
    style: {
      height: 19,
      padding: '0 6px',
      borderRadius: 999,
      background: 'rgba(255,255,255,.18)',
      border: '1px solid rgba(255,255,255,.22)',
      display: 'inline-flex',
      alignItems: 'center',
      fontSize: 9,
      fontWeight: 700,
      backdropFilter: 'blur(10px)'
    }
  }, "#", tag))), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 16.5,
      lineHeight: 1.18,
      fontWeight: 760,
      letterSpacing: 0,
      textShadow: '0 2px 10px rgba(0,0,0,.24)'
    }
  }, item.title)));
};
const FilterChip = ({
  active,
  children,
  onClick,
  count
}) => /*#__PURE__*/React.createElement("button", {
  onClick: onClick,
  style: {
    height: 34,
    padding: '0 12px',
    borderRadius: 12,
    border: `1px solid ${active ? 'rgba(75,77,237,.16)' : T.hairlineSoft}`,
    background: active ? T.irisTint : 'rgba(255,255,255,.76)',
    color: active ? T.iris : T.navyMid,
    boxShadow: active ? 'inset 0 1px 0 rgba(255,255,255,.78)' : 'none',
    cursor: 'pointer',
    fontSize: 12.5,
    fontWeight: 700,
    display: 'inline-flex',
    alignItems: 'center',
    gap: 7,
    transition: 'transform .16s cubic-bezier(.2,.8,.2,1), background .16s, box-shadow .16s'
  },
  onMouseEnter: e => {
    e.currentTarget.style.transform = 'translateY(-1px)';
    e.currentTarget.style.boxShadow = active ? T.shadowSm : T.shadowXs;
  },
  onMouseLeave: e => {
    e.currentTarget.style.transform = 'translateY(0)';
    e.currentTarget.style.boxShadow = active ? 'inset 0 1px 0 rgba(255,255,255,.78)' : 'none';
  }
}, children, typeof count === 'number' && /*#__PURE__*/React.createElement("span", {
  style: {
    minWidth: 20,
    height: 20,
    padding: '0 6px',
    borderRadius: 999,
    background: active ? 'rgba(75,77,237,.12)' : T.surface,
    color: active ? T.iris : T.navyLight,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 10.5,
    fontFamily: T.fontMono
  }
}, count));
const AssetCard = ({
  item,
  index,
  onOpen
}) => {
  const [menuOpen, setMenuOpen] = React.useState(false);
  return /*#__PURE__*/React.createElement("article", {
    onClick: () => onOpen(item),
    style: {
      breakInside: 'avoid',
      marginBottom: 14,
      borderRadius: 16,
      overflow: 'hidden',
      background: T.white,
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: '0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)',
      cursor: 'pointer',
      position: 'relative',
      animation: `fadeInScale .44s ${index * 48}ms cubic-bezier(.2,.8,.2,1) both`,
      transition: 'transform .2s cubic-bezier(.2,.8,.2,1), box-shadow .2s cubic-bezier(.2,.8,.2,1)'
    },
    onMouseEnter: e => {
      e.currentTarget.style.transform = 'translateY(-3px)';
      e.currentTarget.style.boxShadow = '0 16px 38px rgba(14,14,44,.095), inset 0 1px 0 rgba(255,255,255,.76)';
    },
    onMouseLeave: e => {
      e.currentTarget.style.transform = 'translateY(0)';
      e.currentTarget.style.boxShadow = '0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)';
    }
  }, /*#__PURE__*/React.createElement(AssetVisual, {
    item: item
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '10px 11px 11px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12.4,
      lineHeight: 1.38,
      fontWeight: 690,
      color: T.navy,
      letterSpacing: 0,
      display: '-webkit-box',
      WebkitLineClamp: 2,
      WebkitBoxOrient: 'vertical',
      overflow: 'hidden'
    }
  }, item.title), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8,
      display: 'flex',
      alignItems: 'center',
      gap: 5,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      height: 20,
      padding: '0 6px',
      borderRadius: 999,
      background: T.primaryTint,
      color: T.navy,
      display: 'inline-flex',
      alignItems: 'center',
      fontSize: 9.5,
      fontWeight: 700
    }
  }, item.platform), /*#__PURE__*/React.createElement("span", {
    style: {
      height: 20,
      padding: '0 6px',
      borderRadius: 999,
      background: item.type === '视频' ? T.peachTint : item.type === '图文' ? T.successTint : T.surface,
      color: item.type === '视频' ? '#a35a62' : item.type === '图文' ? '#168b73' : T.navyMid,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 4,
      fontSize: 9.5,
      fontWeight: 700
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: item.type === '视频' ? 'video' : item.type === '图文' ? 'image' : 'document',
    size: 9
  }), item.type))), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: e => {
      e.stopPropagation();
      setMenuOpen(v => !v);
    },
    style: {
      width: 26,
      height: 26,
      borderRadius: 9,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(250,252,254,.88)',
      color: T.navyLight,
      cursor: 'pointer',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "moreH",
    size: 13
  })), menuOpen && /*#__PURE__*/React.createElement("div", {
    onClick: e => e.stopPropagation(),
    style: {
      position: 'absolute',
      right: 0,
      top: 34,
      zIndex: 8,
      width: 126,
      padding: 5,
      borderRadius: 13,
      background: 'rgba(255,255,255,.96)',
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: T.shadowLg,
      backdropFilter: 'blur(18px)',
      animation: 'fadeIn .16s ease both'
    }
  }, [{
    label: 'Extend',
    icon: 'sparkles'
  }, {
    label: '下载',
    icon: 'download'
  }, {
    label: '删除',
    icon: 'close',
    danger: true
  }].map(action => /*#__PURE__*/React.createElement("button", {
    key: action.label,
    style: {
      width: '100%',
      height: 31,
      borderRadius: 9,
      border: 'none',
      background: 'transparent',
      color: action.danger ? T.error : T.navyMid,
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: 7,
      padding: '0 8px',
      fontSize: 12,
      fontWeight: 650
    },
    onMouseEnter: e => e.currentTarget.style.background = action.danger ? 'rgba(229,57,53,.08)' : T.surface,
    onMouseLeave: e => e.currentTarget.style.background = 'transparent'
  }, /*#__PURE__*/React.createElement(Icon, {
    name: action.icon,
    size: 12
  }), action.label))))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 9,
      paddingTop: 9,
      borderTop: `1px solid ${T.hairlineSoft}`,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      color: T.navyLight,
      fontSize: 10.2
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 4
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "check",
    size: 10
  }), item.status), /*#__PURE__*/React.createElement("span", {
    style: {
      fontFamily: T.fontMono
    }
  }, item.time))));
};
const AssetsPage = ({
  onOpenAsset,
  onBackHome,
  onOpenSkills,
  onOpenInsights,
  onNewChat
}) => {
  const {
    width,
    isTablet,
    isMobile
  } = useViewport();
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [query, setQuery] = React.useState('');
  const [platform, setPlatform] = React.useState('全部');
  const [type, setType] = React.useState('全部');
  const [sort, setSort] = React.useState('最新');
  const [view, setView] = React.useState('grid');
  const columnCount = view === 'list' ? 1 : isMobile ? 1 : isTablet ? 2 : Math.min(6, Math.max(4, Math.floor((width - (navCollapsed ? 132 : 292)) / 214)));
  const sessions = ASSET_ITEMS.slice(0, 6).map(item => item.title);
  const filtered = ASSET_ITEMS.filter(item => platform === '全部' || item.platform === platform).filter(item => type === '全部' || item.type === type).filter(item => !query.trim() || `${item.title} ${item.platform} ${item.type} ${item.tags.join(' ')}`.toLowerCase().includes(query.trim().toLowerCase()));
  const sorted = sort === '最早' ? [...filtered].reverse() : filtered;
  const platforms = ['全部', '小红书', '公众号', 'B站', '短视频'];
  const types = ['全部', '图文', '视频', '纯文字'];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      width: '100%',
      height: '100%',
      background: T.surfaceWh,
      overflow: 'hidden'
    }
  }, !isTablet && /*#__PURE__*/React.createElement(Sidebar, {
    active: "library",
    onNew: onNewChat,
    onNavigate: id => {
      if (id === 'home') onBackHome();
      if (id === 'skills') onOpenSkills && onOpenSkills();
      if (id === 'insights') onOpenInsights && onOpenInsights();
    },
    sessions: sessions,
    collapsed: navCollapsed,
    onToggle: () => setNavCollapsed(v => !v)
  }), /*#__PURE__*/React.createElement("main", {
    style: {
      flex: 1,
      minWidth: 0,
      overflow: 'auto',
      background: 'linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)',
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      background: 'radial-gradient(circle at 18% 12%, rgba(214,255,0,.16), transparent 18%), radial-gradient(circle at 86% 10%, rgba(75,77,237,.08), transparent 22%), radial-gradient(circle at 64% 72%, rgba(49,208,170,.07), transparent 22%)',
      pointerEvents: 'none'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      zIndex: 1,
      maxWidth: 1640,
      margin: '0 auto',
      padding: isMobile ? '18px 18px 36px' : '28px 30px 50px'
    }
  }, isTablet && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: 18
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement(NoriLogo, {
    size: 28
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 15,
      fontWeight: 760,
      color: T.navy
    }
  }, "\u6211\u7684\u5185\u5BB9\u5E93"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: T.navyLight
    }
  }, "\u81EA\u52A8\u4FDD\u5B58\u7684\u521B\u4F5C\u8D44\u4EA7"))), /*#__PURE__*/React.createElement("button", {
    onClick: onBackHome,
    style: iconBtnStyle()
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "home",
    size: 16,
    color: T.navyMid
  }))), /*#__PURE__*/React.createElement("header", {
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      justifyContent: 'space-between',
      gap: 22,
      marginBottom: 24,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      fontWeight: 800,
      letterSpacing: '0.08em',
      textTransform: 'uppercase',
      color: T.navyLight,
      marginBottom: 8
    }
  }, "Assets"), /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: 0,
      fontSize: isMobile ? 28 : 38,
      lineHeight: 1.08,
      letterSpacing: 0,
      color: T.navy,
      fontWeight: 760
    }
  }, "\u6211\u7684\u5185\u5BB9\u5E93"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '10px 0 0',
      fontSize: 13.5,
      lineHeight: 1.6,
      color: T.navyMid
    }
  }, "\u751F\u6210\u8FC7\u7684\u56FE\u6587\u3001\u89C6\u9891\u548C\u6587\u6848\u4F1A\u81EA\u52A8\u4FDD\u5B58\uFF0C\u968F\u65F6\u67E5\u770B\u3001\u7F16\u8F91\u3001\u91CD\u65B0\u53D1\u5E03\u6216\u8F6C\u6362\u5F62\u6001\u3002")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      flexWrap: 'wrap',
      justifyContent: isMobile ? 'flex-start' : 'flex-end',
      width: isMobile ? '100%' : 'auto'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: 46,
      minWidth: isMobile ? '100%' : 300,
      borderRadius: 16,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.82)',
      boxShadow: '0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.78)',
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      padding: '0 14px',
      backdropFilter: 'blur(18px)'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "search",
    size: 17,
    color: T.navyLight
  }), /*#__PURE__*/React.createElement("input", {
    value: query,
    onChange: e => setQuery(e.target.value),
    placeholder: "\u641C\u7D22\u5185\u5BB9\u8D44\u4EA7...",
    style: {
      flex: 1,
      border: 'none',
      outline: 'none',
      background: 'transparent',
      color: T.navy,
      fontSize: 14,
      fontFamily: T.fontSans
    }
  })), /*#__PURE__*/React.createElement("button", {
    onClick: () => setSort(s => s === '最新' ? '最早' : '最新'),
    style: {
      height: 46,
      padding: '0 16px',
      borderRadius: 16,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.82)',
      boxShadow: '0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.78)',
      color: T.navy,
      cursor: 'pointer',
      display: 'inline-flex',
      alignItems: 'center',
      gap: 9,
      fontSize: 13.5,
      fontWeight: 740
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "list",
    size: 16,
    color: T.navyMid
  }), sort), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 46,
      padding: 4,
      borderRadius: 16,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.82)',
      boxShadow: '0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.78)',
      display: 'inline-flex',
      gap: 4
    }
  }, [{
    id: 'grid',
    icon: 'grid'
  }, {
    id: 'list',
    icon: 'list'
  }].map(v => /*#__PURE__*/React.createElement("button", {
    key: v.id,
    onClick: () => setView(v.id),
    style: {
      width: 38,
      height: 38,
      borderRadius: 12,
      border: 'none',
      background: view === v.id ? T.navy : 'transparent',
      color: view === v.id ? T.white : T.navyLight,
      cursor: 'pointer',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      transition: 'background .16s, color .16s'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: v.icon,
    size: 16
  })))))), /*#__PURE__*/React.createElement("section", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 12,
      flexWrap: 'wrap',
      paddingBottom: 18,
      borderBottom: `1px solid ${T.hairlineSoft}`,
      marginBottom: 24
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      flexWrap: 'wrap'
    }
  }, platforms.map(p => /*#__PURE__*/React.createElement(FilterChip, {
    key: p,
    active: platform === p,
    onClick: () => setPlatform(p),
    count: p === '全部' ? ASSET_ITEMS.length : ASSET_ITEMS.filter(item => item.platform === p).length
  }, p))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      flexWrap: 'wrap'
    }
  }, types.map(t => /*#__PURE__*/React.createElement(FilterChip, {
    key: t,
    active: type === t,
    onClick: () => setType(t)
  }, t)))), /*#__PURE__*/React.createElement("section", {
    style: {
      columnCount,
      columnGap: 14,
      maxWidth: view === 'list' ? 880 : 'none'
    }
  }, sorted.map((item, index) => /*#__PURE__*/React.createElement(AssetCard, {
    key: item.id,
    item: item,
    index: index,
    onOpen: onOpenAsset
  }))), sorted.length === 0 && /*#__PURE__*/React.createElement("div", {
    style: {
      minHeight: 280,
      borderRadius: 22,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.72)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: T.navyLight,
      fontSize: 13.5,
      boxShadow: T.shadowXs
    }
  }, "\u6CA1\u6709\u627E\u5230\u5339\u914D\u7684\u5185\u5BB9\u8D44\u4EA7"))));
};
window.AssetsPage = AssetsPage;

/* ─── Skill Plaza ─── */

const SKILL_ITEMS = [{
  id: 'xhs-viral-note',
  owner: 'community',
  title: '小红书爆款图文拆解器',
  type: '小红书图文',
  uses: '12.8k',
  height: 278,
  accent: T.iris,
  tint: T.irisTint,
  palette: ['#efeefd', '#4b4ded', '#d6ff00', '#f3dbda', '#0e0e2c'],
  desc: '把一个普通选题拆成标题钩子、封面结构、正文节奏和评论区引导，适合生活方式、测评和知识类图文。',
  prompt: '使用「小红书爆款图文拆解器」：请基于我接下来输入的主题，生成小红书图文内容。请包含标题备选、封面文案、正文结构、标签和评论区互动问题。主题：',
  result: ['3 组标题方向', '封面视觉脚本', '正文 6 段结构', '发布标签']
}, {
  id: 'longform-editorial',
  owner: 'community',
  title: '公众号长文编辑台',
  type: '公众号长文',
  uses: '8.4k',
  height: 326,
  accent: T.success,
  tint: T.successTint,
  palette: ['#e0faf4', '#31d0aa', '#0e0e2c', '#d6ff00', '#ffffff'],
  desc: '将零散观点整理成有开头、有论证、有案例、有结尾的公众号长文，适合行业观点、产品思考和深度复盘。',
  prompt: '使用「公众号长文编辑台」：请把我输入的主题扩展为公众号长文。请先给文章大纲，再写完整正文，并加入小标题、案例和结尾行动建议。主题：',
  result: ['文章大纲', '完整长文', '小标题优化', '结尾 CTA']
}, {
  id: 'short-video-script',
  owner: 'community',
  title: '短视频 60 秒口播脚本',
  type: '短视频',
  uses: '15.2k',
  height: 296,
  accent: '#a35a62',
  tint: T.peachTint,
  palette: ['#fdf5f5', '#f3dbda', '#0e0e2c', '#4b4ded', '#ffffff'],
  desc: '将观点压缩成 60 秒短视频脚本，自动拆分前三秒钩子、口播、转场和结尾关注理由。',
  prompt: '使用「短视频 60 秒口播脚本」：请基于主题生成 60 秒短视频脚本，包含前三秒钩子、分镜、口播稿、字幕重点和结尾关注引导。主题：',
  result: ['口播稿', '分镜节奏', '字幕重点', '封面标题']
}, {
  id: 'product-review',
  owner: 'community',
  title: '产品测评对比模板',
  type: '小红书图文',
  uses: '6.9k',
  height: 248,
  accent: T.navy,
  tint: T.surface,
  palette: ['#ecf1f4', '#c4c4d4', '#4b4ded', '#d6ff00', '#0e0e2c'],
  desc: '把多个产品整理成维度清晰的横评卡片，自动生成优缺点、适合人群和购买建议。',
  prompt: '使用「产品测评对比模板」：请根据我输入的产品或工具，生成横评内容，包含对比维度、优缺点、适合人群、结论和推荐排序。产品：',
  result: ['对比维度', '优缺点', '推荐排序', '购买建议']
}, {
  id: 'personal-brand',
  owner: 'mine',
  title: '个人 IP 日常内容系统',
  type: '小红书图文',
  uses: '1.1k',
  height: 310,
  accent: T.iris,
  tint: T.irisTint,
  palette: ['#fafcfe', '#efeefd', '#4b4ded', '#f3dbda', '#0e0e2c'],
  desc: '从日常经历里提炼观点，生成适合个人品牌的图文内容，适合创作者、咨询师和独立工作者。',
  prompt: '使用「个人 IP 日常内容系统」：请把我输入的一段日常经历提炼成个人品牌内容，包含观点、故事、反思、标题和互动问题。经历：',
  result: ['故事钩子', '个人观点', '标题组', '互动问题']
}, {
  id: 'launch-campaign',
  owner: 'mine',
  title: '新品发布节奏规划',
  type: '公众号长文',
  uses: '860',
  height: 270,
  accent: T.success,
  tint: T.successTint,
  palette: ['#e0faf4', '#31d0aa', '#f3dbda', '#d6ff00', '#0e0e2c'],
  desc: '为新品发布自动规划预热、发布、复盘三个阶段的内容节奏和每条内容的主信息。',
  prompt: '使用「新品发布节奏规划」：请基于我的新品信息，设计一套发布内容节奏，包含预热、发布、复盘阶段，每阶段给出内容主题和文案方向。新品：',
  result: ['发布节奏', '内容主题', '文案方向', '复盘指标']
}, {
  id: 'knowledge-card',
  owner: 'community',
  title: '知识卡片系列生成器',
  type: '小红书图文',
  uses: '9.7k',
  height: 286,
  accent: T.primary,
  tint: T.primaryTint,
  palette: ['#f5ffe0', '#d6ff00', '#0e0e2c', '#4b4ded', '#ffffff'],
  desc: '把一个知识点拆成 6-9 张卡片，每张卡片都有标题、重点句和视觉建议。',
  prompt: '使用「知识卡片系列生成器」：请把我输入的知识主题拆成一组图文卡片，包含每张卡片标题、重点句、视觉建议和结尾总结。主题：',
  result: ['卡片大纲', '重点句', '视觉建议', '总结页']
}, {
  id: 'case-study',
  owner: 'community',
  title: '案例复盘长文框架',
  type: '公众号长文',
  uses: '5.3k',
  height: 336,
  accent: T.navy,
  tint: T.surface,
  palette: ['#f8fbfd', '#ecf1f4', '#0e0e2c', '#31d0aa', '#4b4ded'],
  desc: '把项目经历整理成背景、动作、结果、复盘、可复用经验的完整案例文章。',
  prompt: '使用「案例复盘长文框架」：请把我的项目经历整理成案例复盘文章，包含背景、目标、关键动作、结果数据、失败点和可复用经验。项目：',
  result: ['案例结构', '复盘问题', '结果表达', '经验提炼']
}];
const SkillArtwork = ({
  skill
}) => /*#__PURE__*/React.createElement("div", {
  style: {
    height: skill.height,
    position: 'relative',
    overflow: 'hidden',
    background: `linear-gradient(145deg, ${skill.palette[0]}, ${skill.palette[1]})`
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    position: 'absolute',
    inset: 0,
    background: 'radial-gradient(circle at 26% 20%, rgba(255,255,255,.72), transparent 24%), radial-gradient(circle at 80% 14%, rgba(255,255,255,.34), transparent 22%), radial-gradient(circle at 72% 78%, rgba(14,14,44,.10), transparent 30%)'
  }
}), /*#__PURE__*/React.createElement("div", {
  style: {
    position: 'absolute',
    left: 18,
    top: 18,
    width: 42,
    height: 42,
    borderRadius: 15,
    background: 'rgba(255,255,255,.78)',
    color: skill.accent,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: '0 14px 30px rgba(14,14,44,.10), inset 0 1px 0 rgba(255,255,255,.7)',
    backdropFilter: 'blur(14px)'
  }
}, /*#__PURE__*/React.createElement(Icon, {
  name: skill.type === '短视频' ? 'video' : skill.type === '公众号长文' ? 'document' : 'image',
  size: 18
})), /*#__PURE__*/React.createElement("div", {
  style: {
    position: 'absolute',
    right: -28,
    top: 40,
    width: 130,
    height: 130,
    borderRadius: 42,
    transform: 'rotate(14deg)',
    background: `linear-gradient(135deg, ${skill.palette[2]}, ${skill.palette[3]})`,
    opacity: .92,
    boxShadow: '0 24px 52px rgba(14,14,44,.16)'
  }
}), /*#__PURE__*/React.createElement("div", {
  style: {
    position: 'absolute',
    left: 18,
    right: 18,
    bottom: 18
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    display: 'inline-flex',
    height: 25,
    alignItems: 'center',
    padding: '0 9px',
    borderRadius: 999,
    background: 'rgba(255,255,255,.64)',
    color: T.navyMid,
    fontSize: 10.5,
    fontWeight: 800,
    backdropFilter: 'blur(10px)',
    marginBottom: 10
  }
}, skill.type), /*#__PURE__*/React.createElement("div", {
  style: {
    fontSize: 21,
    lineHeight: 1.14,
    fontWeight: 780,
    color: T.navy,
    letterSpacing: 0
  }
}, skill.title)));
const SkillCard = ({
  skill,
  index,
  onOpen
}) => /*#__PURE__*/React.createElement("article", {
  onClick: () => onOpen(skill),
  style: {
    breakInside: 'avoid',
    marginBottom: 16,
    borderRadius: 18,
    overflow: 'hidden',
    background: T.white,
    border: `1px solid ${T.hairlineSoft}`,
    boxShadow: '0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)',
    cursor: 'pointer',
    animation: `fadeInScale .44s ${index * 48}ms cubic-bezier(.2,.8,.2,1) both`,
    transition: 'transform .2s cubic-bezier(.2,.8,.2,1), box-shadow .2s cubic-bezier(.2,.8,.2,1)'
  },
  onMouseEnter: e => {
    e.currentTarget.style.transform = 'translateY(-3px)';
    e.currentTarget.style.boxShadow = '0 16px 38px rgba(14,14,44,.095), inset 0 1px 0 rgba(255,255,255,.76)';
  },
  onMouseLeave: e => {
    e.currentTarget.style.transform = 'translateY(0)';
    e.currentTarget.style.boxShadow = '0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)';
  }
}, /*#__PURE__*/React.createElement(SkillArtwork, {
  skill: skill
}), /*#__PURE__*/React.createElement("div", {
  style: {
    padding: '12px 13px 13px'
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    fontSize: 13.2,
    lineHeight: 1.38,
    fontWeight: 700,
    color: T.navy,
    letterSpacing: 0,
    display: '-webkit-box',
    WebkitLineClamp: 2,
    WebkitBoxOrient: 'vertical',
    overflow: 'hidden'
  }
}, skill.title), /*#__PURE__*/React.createElement("div", {
  style: {
    marginTop: 11,
    paddingTop: 10,
    borderTop: `1px solid ${T.hairlineSoft}`,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  }
}, /*#__PURE__*/React.createElement("span", {
  style: {
    fontSize: 10.8,
    color: T.navyLight,
    fontFamily: T.fontMono
  }
}, skill.uses, " uses"), /*#__PURE__*/React.createElement("span", {
  style: {
    height: 22,
    padding: '0 8px',
    borderRadius: 999,
    background: skill.tint,
    color: skill.accent === T.primary ? T.navy : skill.accent,
    display: 'inline-flex',
    alignItems: 'center',
    gap: 5,
    fontSize: 10,
    fontWeight: 760
  }
}, /*#__PURE__*/React.createElement(Icon, {
  name: "sparkles",
  size: 10
}), "Skill"))));
const SkillDetail = ({
  skill,
  onBack,
  onUse
}) => /*#__PURE__*/React.createElement("div", {
  style: {
    maxWidth: 980,
    margin: '0 auto',
    animation: 'fadeInScale .28s ease both'
  }
}, /*#__PURE__*/React.createElement("button", {
  onClick: onBack,
  style: {
    height: 38,
    padding: '0 13px',
    borderRadius: 13,
    border: `1px solid ${T.hairlineSoft}`,
    background: 'rgba(255,255,255,.84)',
    color: T.navyMid,
    cursor: 'pointer',
    display: 'inline-flex',
    alignItems: 'center',
    gap: 7,
    fontSize: 12.5,
    fontWeight: 700,
    boxShadow: T.shadowXs,
    marginBottom: 18
  }
}, /*#__PURE__*/React.createElement(Icon, {
  name: "chevronLeft",
  size: 14
}), "\u8FD4\u56DE Skill \u5E7F\u573A"), /*#__PURE__*/React.createElement("section", {
  style: {
    display: 'grid',
    gridTemplateColumns: 'minmax(0, .95fr) minmax(320px, 1.05fr)',
    gap: 24,
    alignItems: 'stretch'
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    borderRadius: 26,
    overflow: 'hidden',
    border: `1px solid ${T.hairlineSoft}`,
    boxShadow: T.shadowLg,
    background: T.white
  }
}, /*#__PURE__*/React.createElement(SkillArtwork, {
  skill: {
    ...skill,
    height: 520
  }
})), /*#__PURE__*/React.createElement("div", {
  style: {
    borderRadius: 26,
    border: `1px solid ${T.hairlineSoft}`,
    background: 'rgba(255,255,255,.84)',
    boxShadow: '0 18px 44px rgba(14,14,44,.08), inset 0 1px 0 rgba(255,255,255,.78)',
    padding: 28,
    display: 'flex',
    flexDirection: 'column'
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    display: 'flex',
    alignItems: 'center',
    gap: 8,
    marginBottom: 18,
    flexWrap: 'wrap'
  }
}, /*#__PURE__*/React.createElement("span", {
  style: {
    height: 28,
    padding: '0 10px',
    borderRadius: 999,
    background: skill.tint,
    color: skill.accent === T.primary ? T.navy : skill.accent,
    display: 'inline-flex',
    alignItems: 'center',
    fontSize: 11.5,
    fontWeight: 780
  }
}, skill.type), /*#__PURE__*/React.createElement("span", {
  style: {
    height: 28,
    padding: '0 10px',
    borderRadius: 999,
    background: T.surface,
    color: T.navyLight,
    display: 'inline-flex',
    alignItems: 'center',
    gap: 6,
    fontSize: 11.5,
    fontFamily: T.fontMono
  }
}, /*#__PURE__*/React.createElement(Icon, {
  name: "sparkles",
  size: 11
}), skill.uses, " uses")), /*#__PURE__*/React.createElement("h1", {
  style: {
    margin: 0,
    fontSize: 38,
    lineHeight: 1.08,
    fontWeight: 780,
    letterSpacing: 0,
    color: T.navy
  }
}, skill.title), /*#__PURE__*/React.createElement("p", {
  style: {
    margin: '18px 0 24px',
    color: T.navyMid,
    fontSize: 14.5,
    lineHeight: 1.8
  }
}, skill.desc), /*#__PURE__*/React.createElement("div", {
  style: {
    display: 'grid',
    gap: 10,
    marginBottom: 24
  }
}, skill.result.map((item, i) => /*#__PURE__*/React.createElement("div", {
  key: item,
  style: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    minHeight: 42,
    padding: '8px 12px',
    borderRadius: 14,
    background: 'rgba(250,252,254,.82)',
    border: `1px solid ${T.hairlineSoft}`
  }
}, /*#__PURE__*/React.createElement("span", {
  style: {
    width: 24,
    height: 24,
    borderRadius: 9,
    background: i === 0 ? T.primary : skill.tint,
    color: i === 0 ? T.navy : skill.accent,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 10.5,
    fontFamily: T.fontMono,
    fontWeight: 800
  }
}, String(i + 1).padStart(2, '0')), /*#__PURE__*/React.createElement("span", {
  style: {
    fontSize: 13,
    fontWeight: 680,
    color: T.navy
  }
}, item)))), /*#__PURE__*/React.createElement("div", {
  style: {
    marginTop: 'auto',
    padding: 16,
    borderRadius: 18,
    background: `linear-gradient(135deg, ${T.primaryTint}, ${skill.tint})`,
    border: `1px solid ${T.hairlineSoft}`
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    fontSize: 12,
    color: T.navyMid,
    lineHeight: 1.65,
    marginBottom: 14
  }
}, "\u4F7F\u7528\u540E\u4F1A\u81EA\u52A8\u628A Skill \u6A21\u677F\u586B\u5165\u751F\u6210\u9875\u8F93\u5165\u6846\uFF0C\u5E76\u7B49\u5F85\u4F60\u8865\u5145\u5177\u4F53\u4E3B\u9898\u3002"), /*#__PURE__*/React.createElement("button", {
  onClick: () => onUse(skill),
  style: {
    width: '100%',
    height: 48,
    borderRadius: 16,
    border: 'none',
    background: T.navy,
    color: T.primary,
    cursor: 'pointer',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    fontSize: 14,
    fontWeight: 780,
    boxShadow: '0 14px 28px rgba(14,14,44,.18)'
  }
}, /*#__PURE__*/React.createElement(Icon, {
  name: "sparkles",
  size: 16
}), "\u4F7F\u7528 Skill")))));
const SkillsPage = ({
  onBackHome,
  onOpenAssets,
  onOpenInsights,
  onNewChat,
  onUseSkill
}) => {
  const {
    width,
    isTablet,
    isMobile
  } = useViewport();
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [scope, setScope] = React.useState('community');
  const [type, setType] = React.useState('全部');
  const [selected, setSelected] = React.useState(null);
  const sessions = SKILL_ITEMS.slice(0, 6).map(item => item.title);
  const types = ['全部', '小红书图文', '公众号长文', '短视频'];
  const filtered = SKILL_ITEMS.filter(skill => skill.owner === scope).filter(skill => type === '全部' || skill.type === type);
  const columnCount = isMobile ? 1 : isTablet ? 2 : Math.min(5, Math.max(3, Math.floor((width - (navCollapsed ? 150 : 310)) / 258)));
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      width: '100%',
      height: '100%',
      background: T.surfaceWh,
      overflow: 'hidden'
    }
  }, !isTablet && /*#__PURE__*/React.createElement(Sidebar, {
    active: "skills",
    onNew: onNewChat,
    onNavigate: id => {
      if (id === 'home') onBackHome();
      if (id === 'library') onOpenAssets();
      if (id === 'skills') setSelected(null);
      if (id === 'insights') onOpenInsights && onOpenInsights();
    },
    sessions: sessions,
    collapsed: navCollapsed,
    onToggle: () => setNavCollapsed(v => !v)
  }), /*#__PURE__*/React.createElement("main", {
    style: {
      flex: 1,
      minWidth: 0,
      overflow: 'auto',
      background: 'linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)',
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      background: 'radial-gradient(circle at 48% 8%, rgba(214,255,0,.18), transparent 18%), radial-gradient(circle at 76% 12%, rgba(75,77,237,.075), transparent 22%), radial-gradient(circle at 23% 65%, rgba(243,217,218,.20), transparent 22%)',
      pointerEvents: 'none'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      zIndex: 1,
      maxWidth: 1640,
      margin: '0 auto',
      padding: isMobile ? '18px 18px 36px' : '28px 30px 50px'
    }
  }, selected ? /*#__PURE__*/React.createElement(SkillDetail, {
    skill: selected,
    onBack: () => setSelected(null),
    onUse: onUseSkill
  }) : /*#__PURE__*/React.createElement(React.Fragment, null, isTablet && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: 18
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement(NoriLogo, {
    size: 28
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 15,
      fontWeight: 760,
      color: T.navy
    }
  }, "Skill \u5E7F\u573A"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: T.navyLight
    }
  }, "\u53EF\u590D\u7528\u521B\u4F5C\u7CFB\u7EDF"))), /*#__PURE__*/React.createElement("button", {
    onClick: onBackHome,
    style: iconBtnStyle()
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "home",
    size: 16,
    color: T.navyMid
  }))), /*#__PURE__*/React.createElement("header", {
    style: {
      display: 'flex',
      alignItems: 'flex-end',
      justifyContent: 'space-between',
      gap: 20,
      marginBottom: 24,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      fontWeight: 800,
      letterSpacing: '0.08em',
      textTransform: 'uppercase',
      color: T.navyLight,
      marginBottom: 8
    }
  }, "Skill Plaza"), /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: 0,
      fontSize: isMobile ? 28 : 38,
      lineHeight: 1.08,
      letterSpacing: 0,
      color: T.navy,
      fontWeight: 760
    }
  }, "Skill \u5E7F\u573A"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '10px 0 0',
      fontSize: 13.5,
      lineHeight: 1.6,
      color: T.navyMid
    }
  }, "\u9009\u62E9\u4E00\u4E2A\u53EF\u590D\u7528\u7684\u521B\u4F5C\u7CFB\u7EDF\uFF0C\u8BA9 Nori \u6309\u6307\u5B9A\u7ED3\u6784\u5F00\u59CB\u751F\u6210\u3002")), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 46,
      padding: 4,
      borderRadius: 17,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.82)',
      boxShadow: '0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.78)',
      display: 'inline-flex',
      gap: 4
    }
  }, [{
    id: 'community',
    label: '社区'
  }, {
    id: 'mine',
    label: '我的'
  }].map(tab => /*#__PURE__*/React.createElement("button", {
    key: tab.id,
    onClick: () => {
      setScope(tab.id);
      setType('全部');
    },
    style: {
      height: 38,
      padding: '0 18px',
      borderRadius: 13,
      border: 'none',
      background: scope === tab.id ? T.navy : 'transparent',
      color: scope === tab.id ? T.white : T.navyMid,
      cursor: 'pointer',
      fontSize: 13,
      fontWeight: 760,
      transition: 'background .16s, color .16s'
    }
  }, tab.label)))), /*#__PURE__*/React.createElement("section", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      flexWrap: 'wrap',
      paddingBottom: 18,
      borderBottom: `1px solid ${T.hairlineSoft}`,
      marginBottom: 24
    }
  }, types.map(t => /*#__PURE__*/React.createElement(FilterChip, {
    key: t,
    active: type === t,
    onClick: () => setType(t),
    count: t === '全部' ? filtered.length : SKILL_ITEMS.filter(skill => skill.owner === scope && skill.type === t).length
  }, t))), /*#__PURE__*/React.createElement("section", {
    style: {
      columnCount,
      columnGap: 16
    }
  }, filtered.map((skill, index) => /*#__PURE__*/React.createElement(SkillCard, {
    key: skill.id,
    skill: skill,
    index: index,
    onOpen: setSelected
  })))))));
};
window.SkillsPage = SkillsPage;

/* ─── Insights Page ─── */

const INSIGHT_CONTENTS = [{
  id: 'c1',
  title: '深蓝幕布下的粉蝶兰，谁懂这种反差感？',
  type: '图文',
  platform: '小红书',
  date: '今天',
  exposure: '12.8w',
  likes: '8.0w',
  saves: '2.6w',
  comments: '1.1k',
  fans: '+234'
}, {
  id: 'c2',
  title: '咖啡入门 12 个名词，一次讲清楚',
  type: '纯文字',
  platform: '公众号',
  date: '昨天',
  exposure: '9.6w',
  likes: '5.2w',
  saves: '1.9w',
  comments: '384',
  fans: '+112'
}, {
  id: 'c3',
  title: '极简通勤穿搭一周 OOTD',
  type: '视频',
  platform: '抖音',
  date: '3 天前',
  exposure: '15.4w',
  likes: '7.4w',
  saves: '3.1w',
  comments: '912',
  fans: '+426'
}, {
  id: 'c4',
  title: '产品测评对比模板',
  type: '图文',
  platform: '小红书',
  date: '5 天前',
  exposure: '7.2w',
  likes: '4.1w',
  saves: '1.5w',
  comments: '228',
  fans: '+90'
}, {
  id: 'c5',
  title: '租房避雷指南',
  type: '纯文字',
  platform: '公众号',
  date: '1 周前',
  exposure: '5.8w',
  likes: '2.6w',
  saves: '1.3w',
  comments: '174',
  fans: '+58'
}, {
  id: 'c6',
  title: 'AI 视频工具横评',
  type: '视频',
  platform: '视频号',
  date: '2 周前',
  exposure: '18.1w',
  likes: '9.4w',
  saves: '3.5w',
  comments: '1.4k',
  fans: '+702'
}];
const RadarBar = ({
  label,
  value,
  max = 100,
  tint = T.iris
}) => /*#__PURE__*/React.createElement("div", {
  style: {
    display: 'grid',
    gridTemplateColumns: '82px minmax(0, 1fr) 42px',
    gap: 10,
    alignItems: 'center'
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    fontSize: 12,
    color: T.navyMid,
    fontWeight: 680
  }
}, label), /*#__PURE__*/React.createElement("div", {
  style: {
    height: 8,
    borderRadius: 999,
    background: 'rgba(14,14,44,.06)',
    overflow: 'hidden'
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    width: `${Math.min(100, value / max * 100)}%`,
    height: '100%',
    borderRadius: 999,
    background: `linear-gradient(90deg, ${tint}, rgba(214,255,0,.86))`,
    boxShadow: `0 0 18px ${tint}55`
  }
})), /*#__PURE__*/React.createElement("div", {
  style: {
    fontSize: 11.5,
    color: T.navyLight,
    fontFamily: T.fontMono,
    textAlign: 'right'
  }
}, value));
const FloatTag = ({
  children,
  style,
  drift = 'up',
  tint = T.white,
  depth = 1
}) => /*#__PURE__*/React.createElement("div", {
  style: {
    position: 'absolute',
    zIndex: depth,
    animation: drift === 'up' ? 'floatDrift 5.4s ease-in-out infinite' : 'floatDriftReverse 5.8s ease-in-out infinite',
    ...style
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    borderRadius: 999,
    padding: '8px 12px',
    background: `linear-gradient(180deg, ${tint}, rgba(255,255,255,.68))`,
    border: '1px solid rgba(255,255,255,.62)',
    boxShadow: '0 16px 36px rgba(14,14,44,.09), inset 0 1px 0 rgba(255,255,255,.9)',
    backdropFilter: 'blur(18px) saturate(1.3)',
    WebkitBackdropFilter: 'blur(18px) saturate(1.3)',
    color: T.navy,
    fontSize: 11.5,
    fontWeight: 780,
    whiteSpace: 'nowrap',
    animation: 'tagGlow 4.8s ease-in-out infinite'
  }
}, children));
const MetricTile = ({
  label,
  value,
  sub,
  accent = T.iris
}) => /*#__PURE__*/React.createElement("div", {
  style: {
    borderRadius: 20,
    padding: 16,
    background: 'linear-gradient(180deg, rgba(255,255,255,.82), rgba(250,252,254,.68))',
    border: '1px solid rgba(255,255,255,.62)',
    boxShadow: '0 14px 30px rgba(14,14,44,.07), inset 0 1px 0 rgba(255,255,255,.86)',
    backdropFilter: 'blur(18px)'
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 8
  }
}, /*#__PURE__*/React.createElement("span", {
  style: {
    fontSize: 11.5,
    color: T.navyLight,
    fontWeight: 720
  }
}, label), /*#__PURE__*/React.createElement("span", {
  style: {
    width: 8,
    height: 8,
    borderRadius: '50%',
    background: accent,
    boxShadow: `0 0 0 5px ${accent}20`
  }
})), /*#__PURE__*/React.createElement("div", {
  style: {
    marginTop: 10,
    fontSize: 25,
    lineHeight: 1,
    fontWeight: 820,
    color: T.navy,
    letterSpacing: '-0.035em'
  }
}, value), /*#__PURE__*/React.createElement("div", {
  style: {
    marginTop: 6,
    fontSize: 11.5,
    color: T.navyLight
  }
}, sub));
const MiniLineChart = ({
  tint = T.iris
}) => /*#__PURE__*/React.createElement("svg", {
  viewBox: "0 0 520 170",
  width: "100%",
  height: "170",
  style: {
    display: 'block'
  },
  preserveAspectRatio: "none"
}, /*#__PURE__*/React.createElement("defs", null, /*#__PURE__*/React.createElement("linearGradient", {
  id: "insightLineFill",
  x1: "0",
  x2: "0",
  y1: "0",
  y2: "1"
}, /*#__PURE__*/React.createElement("stop", {
  offset: "0%",
  stopColor: tint,
  stopOpacity: ".22"
}), /*#__PURE__*/React.createElement("stop", {
  offset: "100%",
  stopColor: tint,
  stopOpacity: "0"
})), /*#__PURE__*/React.createElement("linearGradient", {
  id: "insightLineStroke",
  x1: "0",
  x2: "1",
  y1: "0",
  y2: "0"
}, /*#__PURE__*/React.createElement("stop", {
  offset: "0%",
  stopColor: T.success
}), /*#__PURE__*/React.createElement("stop", {
  offset: "55%",
  stopColor: tint
}), /*#__PURE__*/React.createElement("stop", {
  offset: "100%",
  stopColor: T.primary
}))), [36, 70, 104, 138].map(y => /*#__PURE__*/React.createElement("line", {
  key: y,
  x1: "0",
  x2: "520",
  y1: y,
  y2: y,
  stroke: "rgba(14,14,44,.06)",
  strokeWidth: "1"
})), /*#__PURE__*/React.createElement("path", {
  d: "M0 124 C42 112 52 72 96 82 C142 92 150 46 194 54 C250 64 254 110 306 94 C356 80 366 30 416 42 C458 52 470 24 520 34 L520 170 L0 170 Z",
  fill: "url(#insightLineFill)"
}), /*#__PURE__*/React.createElement("path", {
  d: "M0 124 C42 112 52 72 96 82 C142 92 150 46 194 54 C250 64 254 110 306 94 C356 80 366 30 416 42 C458 52 470 24 520 34",
  fill: "none",
  stroke: "url(#insightLineStroke)",
  strokeWidth: "5",
  strokeLinecap: "round"
}), [96, 194, 306, 416, 520].map((x, i) => /*#__PURE__*/React.createElement("circle", {
  key: x,
  cx: x,
  cy: [82, 54, 94, 42, 34][i],
  r: "5.5",
  fill: "#fff",
  stroke: tint,
  strokeWidth: "3"
})));
const Avatar3D = ({
  waving,
  onClick,
  compact = false
}) => {
  const scale = compact ? .78 : 1;
  const petalStyle = (x, y, rot, bg, delay) => ({
    position: 'absolute',
    left: '50%',
    top: 88,
    width: 126,
    height: 158,
    borderRadius: '58% 58% 48% 48%',
    background: bg,
    boxShadow: 'inset 0 18px 28px rgba(255,255,255,.22), inset 0 -18px 30px rgba(121,54,88,.18), 0 22px 40px rgba(160,80,110,.13)',
    transform: `translate(${x}px, ${y}px) rotate(${rot}deg)`,
    transformOrigin: '50% 78%',
    animation: `petalBreath 5.6s ${delay}s ease-in-out infinite`
  });
  return /*#__PURE__*/React.createElement("button", {
    onClick: onClick,
    style: {
      position: 'relative',
      width: compact ? 300 : 380,
      height: compact ? 430 : 520,
      border: 'none',
      background: 'transparent',
      cursor: 'pointer',
      padding: 0,
      display: 'block',
      margin: '0 auto',
      transform: `scale(${scale})`,
      transformOrigin: '50% 50%'
    },
    "aria-label": "IP \u5934\u50CF\uFF0C\u70B9\u51FB\u62DB\u624B"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: '50%',
      bottom: 34,
      width: 248,
      height: 54,
      transform: 'translateX(-50%)',
      borderRadius: '50%',
      background: 'radial-gradient(ellipse, rgba(14,14,44,.18), rgba(14,14,44,.05) 55%, transparent 72%)',
      filter: 'blur(8px)'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: '50%',
      top: 42,
      width: 310,
      height: 330,
      transform: 'translateX(-50%)',
      borderRadius: '50%',
      background: 'radial-gradient(circle, rgba(255,130,170,.24), rgba(214,255,0,.11) 42%, rgba(75,77,237,.08) 58%, transparent 72%)',
      filter: 'blur(20px)',
      animation: 'avatarAura 5.6s ease-in-out infinite'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: petalStyle(-64, 18, -55, 'linear-gradient(145deg, #f05f93, #d7477b 62%, #b8396f)', 0)
  }), /*#__PURE__*/React.createElement("div", {
    style: petalStyle(26, 18, 55, 'linear-gradient(145deg, #ff7aa8, #dd4d82 64%, #bd3c70)', .22)
  }), /*#__PURE__*/React.createElement("div", {
    style: petalStyle(-22, -26, 0, 'linear-gradient(160deg, #ef5f95, #d64c82 64%, #b83870)', .4)
  }), /*#__PURE__*/React.createElement("div", {
    style: petalStyle(-78, 116, -118, 'linear-gradient(145deg, #ff89b2, #e15a8a 64%, #bd4277)', .64)
  }), /*#__PURE__*/React.createElement("div", {
    style: petalStyle(42, 116, 118, 'linear-gradient(145deg, #ff89b2, #e15a8a 64%, #bd4277)', .86)
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: '50%',
      top: 146,
      width: 142,
      height: 132,
      transform: `translateX(-50%) ${waving ? 'rotate(-4deg) translateY(-3px)' : ''}`,
      transition: 'transform .34s cubic-bezier(.2,.8,.2,1)',
      borderRadius: '48% 48% 45% 45%',
      background: 'linear-gradient(180deg, #e4a378 0%, #c9825a 100%)',
      boxShadow: 'inset 0 18px 24px rgba(255,226,200,.22), inset 0 -14px 20px rgba(107,56,34,.14), 0 18px 34px rgba(120,62,48,.13)',
      zIndex: 4
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: '50%',
      top: 136,
      width: 150,
      height: 82,
      transform: `translateX(-50%) ${waving ? 'rotate(-3deg)' : ''}`,
      transition: 'transform .34s cubic-bezier(.2,.8,.2,1)',
      borderRadius: '70px 70px 38px 38px',
      background: 'linear-gradient(180deg, #8a4d2e, #5e321e)',
      clipPath: 'polygon(0 36%, 18% 13%, 48% 0, 80% 13%, 100% 36%, 88% 58%, 54% 36%, 42% 78%, 20% 60%)',
      boxShadow: 'inset 0 10px 18px rgba(255,192,126,.2)',
      zIndex: 6
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: 138,
      top: 204,
      width: 34,
      height: 24,
      borderRadius: '50%',
      background: '#2e2630',
      transform: 'rotate(-12deg)',
      zIndex: 7
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      right: 138,
      top: 204,
      width: 34,
      height: 24,
      borderRadius: '50%',
      background: '#2e2630',
      transform: 'rotate(12deg)',
      zIndex: 7
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: 133,
      top: 199,
      width: 42,
      height: 12,
      borderRadius: '50%',
      borderTop: '5px solid #4b2d22',
      transform: 'rotate(12deg)',
      zIndex: 8
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      right: 133,
      top: 199,
      width: 42,
      height: 12,
      borderRadius: '50%',
      borderTop: '5px solid #4b2d22',
      transform: 'rotate(-12deg)',
      zIndex: 8
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: '50%',
      top: 244,
      width: 22,
      height: 12,
      transform: 'translateX(-50%)',
      borderBottom: '3px solid #4d2d24',
      borderRadius: '50%',
      zIndex: 8
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: '50%',
      top: 278,
      width: 94,
      height: 82,
      transform: 'translateX(-50%)',
      borderRadius: '34px 34px 18px 18px',
      background: 'linear-gradient(180deg, #d4c3ff, #9e8df2)',
      boxShadow: '0 18px 28px rgba(75,77,237,.12)',
      zIndex: 3
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: 88,
      top: 288,
      width: 74,
      height: 18,
      borderRadius: 999,
      background: 'linear-gradient(90deg, #5a7949, #8fb276)',
      transform: `rotate(${waving ? -30 : -14}deg) translateY(${waving ? -15 : 0}px)`,
      transformOrigin: '100% 50%',
      transition: 'transform .32s cubic-bezier(.2,.8,.2,1)',
      zIndex: 2
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      right: 86,
      top: 290,
      width: 82,
      height: 18,
      borderRadius: 999,
      background: 'linear-gradient(90deg, #8fb276, #5a7949)',
      transform: `rotate(${waving ? -48 : 16}deg) translateY(${waving ? -24 : 0}px)`,
      transformOrigin: '0 50%',
      transition: 'transform .32s cubic-bezier(.2,.8,.2,1)',
      zIndex: 2
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: '50%',
      bottom: 52,
      width: 158,
      height: 34,
      transform: 'translateX(-50%)',
      borderRadius: '50%',
      background: 'linear-gradient(180deg, #e6699b, #bc4779)',
      boxShadow: '0 16px 28px rgba(161,80,112,.18), inset 0 1px 0 rgba(255,255,255,.28)',
      zIndex: 1
    }
  }));
};
const InsightsPage = ({
  onBackHome,
  onOpenAssets,
  onOpenSkills,
  onNewChat
}) => {
  const {
    isTablet,
    isMobile
  } = useViewport();
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [mode, setMode] = React.useState('profile');
  const [selectedContent, setSelectedContent] = React.useState(INSIGHT_CONTENTS[0]);
  const [search, setSearch] = React.useState('');
  const [wave, setWave] = React.useState(false);
  const [hotTab, setHotTab] = React.useState('内容趋势');
  const sessions = INSIGHT_CONTENTS.slice(0, 6).map(item => item.title);
  const filteredContents = INSIGHT_CONTENTS.filter(item => !search.trim() || `${item.title} ${item.type} ${item.platform}`.toLowerCase().includes(search.trim().toLowerCase()));
  const hotCards = [{
    title: '粉色植物 / 猛男养花',
    trend: '+18%',
    sub: '最近 7 天互动上升',
    accent: T.iris
  }, {
    title: '咖啡入门 / 知识科普',
    trend: '+12%',
    sub: '长文阅读更稳定',
    accent: T.success
  }, {
    title: '通勤穿搭 / OOTD',
    trend: '+24%',
    sub: '视频化转化更高',
    accent: T.primary
  }, {
    title: 'AI 工具评测',
    trend: '+31%',
    sub: '评论区提问明显增多',
    accent: T.peach
  }];
  const trendRows = [{
    label: '曝光',
    value: 86,
    tint: T.iris
  }, {
    label: '点赞',
    value: 74,
    tint: T.success
  }, {
    label: '收藏',
    value: 62,
    tint: T.primary
  }, {
    label: '评论',
    value: 39,
    tint: T.peach
  }, {
    label: '涨粉',
    value: 55,
    tint: T.navy
  }];
  const titleToggles = [{
    label: '我的IP人设',
    value: 'profile'
  }, {
    label: '数据看板',
    value: 'dashboard'
  }];
  const dashboardOpen = mode === 'dashboard';
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      width: '100%',
      height: '100%',
      background: T.surfaceWh,
      overflow: 'hidden'
    }
  }, !isTablet && /*#__PURE__*/React.createElement(Sidebar, {
    active: "insights",
    onNew: onNewChat,
    onNavigate: id => {
      if (id === 'home') onBackHome();
      if (id === 'library') onOpenAssets();
      if (id === 'skills') onOpenSkills && onOpenSkills();
      if (id === 'insights') return;
    },
    sessions: sessions,
    collapsed: navCollapsed,
    onToggle: () => setNavCollapsed(v => !v)
  }), /*#__PURE__*/React.createElement("main", {
    style: {
      flex: 1,
      minWidth: 0,
      overflow: 'auto',
      background: 'linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)',
      position: 'relative'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      background: 'radial-gradient(circle at 18% 9%, rgba(214,255,0,.14), transparent 18%), radial-gradient(circle at 80% 10%, rgba(75,77,237,.08), transparent 20%), radial-gradient(circle at 58% 82%, rgba(49,208,170,.08), transparent 25%)',
      pointerEvents: 'none'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      zIndex: 1,
      maxWidth: 1680,
      margin: '0 auto',
      padding: isMobile ? '16px 14px 36px' : '26px 30px 52px'
    }
  }, isTablet && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement(NoriLogo, {
    size: 28
  }), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 15,
      fontWeight: 760,
      color: T.navy
    }
  }, "\u8D26\u53F7\u6D1E\u5BDF"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: T.navyLight
    }
  }, "IP / \u6570\u636E / \u70ED\u70B9"))), /*#__PURE__*/React.createElement("button", {
    onClick: onBackHome,
    style: iconBtnStyle()
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "home",
    size: 16,
    color: T.navyMid
  }))), /*#__PURE__*/React.createElement("section", {
    style: {
      position: 'relative',
      minHeight: isMobile ? 760 : 'calc(100vh - 72px)',
      borderRadius: isMobile ? 26 : 34,
      overflow: 'hidden',
      border: '1px solid rgba(255,255,255,.72)',
      background: 'linear-gradient(180deg, rgba(255,255,255,.88), rgba(246,249,252,.72))',
      boxShadow: '0 26px 70px rgba(14,14,44,.10), inset 0 1px 0 rgba(255,255,255,.94)',
      marginBottom: 24
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      background: 'radial-gradient(circle at 50% 18%, rgba(214,255,0,.18), transparent 20%), radial-gradient(circle at 62% 36%, rgba(75,77,237,.12), transparent 22%), radial-gradient(circle at 40% 60%, rgba(243,219,218,.32), transparent 24%)',
      pointerEvents: 'none'
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: '50%',
      bottom: isMobile ? 110 : 74,
      width: dashboardOpen && !isMobile ? 430 : 620,
      height: dashboardOpen && !isMobile ? 92 : 124,
      transform: dashboardOpen && !isMobile ? 'translateX(-78%) rotateX(66deg)' : 'translateX(-50%) rotateX(66deg)',
      borderRadius: '50%',
      background: 'radial-gradient(ellipse, rgba(255,255,255,.82), rgba(214,255,0,.12) 44%, rgba(75,77,237,.06) 66%, transparent 72%)',
      border: '1px solid rgba(255,255,255,.52)',
      boxShadow: '0 36px 70px rgba(14,14,44,.08)',
      transition: 'transform .46s cubic-bezier(.2,.8,.2,1), width .46s cubic-bezier(.2,.8,.2,1)'
    }
  }), [0, 1, 2].map(i => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      position: 'absolute',
      left: `${18 + i * 24}%`,
      top: `${18 + i * 12}%`,
      width: 6,
      height: 6,
      borderRadius: '50%',
      background: i === 1 ? T.iris : T.primary,
      opacity: .34,
      boxShadow: `0 0 26px ${i === 1 ? T.iris : T.primary}`,
      animation: `${i % 2 ? 'floatDriftReverse' : 'floatDrift'} ${6 + i}s ease-in-out infinite`
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      zIndex: 2,
      minHeight: 'inherit',
      display: 'grid',
      gridTemplateRows: 'auto minmax(0, 1fr)',
      padding: isMobile ? '18px 16px 24px' : '24px 26px 30px'
    }
  }, /*#__PURE__*/React.createElement("header", {
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      justifyContent: 'space-between',
      gap: 18,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: 520
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 8,
      height: 30,
      padding: '0 11px',
      borderRadius: 999,
      background: 'rgba(255,255,255,.72)',
      border: '1px solid rgba(255,255,255,.68)',
      boxShadow: T.shadowXs,
      color: T.navyMid,
      fontSize: 11.5,
      fontWeight: 780,
      marginBottom: 12
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "sparkles",
    size: 12,
    color: T.iris
  }), "Insight Center"), /*#__PURE__*/React.createElement("h1", {
    style: {
      margin: 0,
      fontSize: isMobile ? 30 : 42,
      lineHeight: 1.04,
      letterSpacing: '-0.045em',
      color: T.navy,
      fontWeight: 780
    }
  }, "\u8D26\u53F7\u6D1E\u5BDF"), /*#__PURE__*/React.createElement("p", {
    style: {
      margin: '10px 0 0',
      maxWidth: 560,
      fontSize: 13.5,
      lineHeight: 1.72,
      color: T.navyMid
    }
  }, "\u7528\u6237 IP \u753B\u50CF\u3001\u5185\u5BB9\u6570\u636E\u8D8B\u52BF\u548C\u957F\u671F\u70ED\u70B9\u8FFD\u8E2A\u90FD\u5728\u8FD9\u4E2A\u7A7A\u95F4\u91CC\u6C89\u6DC0\u3002")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'inline-flex',
      gap: 4,
      padding: 4,
      borderRadius: 18,
      border: '1px solid rgba(255,255,255,.68)',
      background: 'rgba(255,255,255,.66)',
      boxShadow: '0 14px 30px rgba(14,14,44,.07), inset 0 1px 0 rgba(255,255,255,.86)',
      backdropFilter: 'blur(18px)'
    }
  }, titleToggles.map(item => /*#__PURE__*/React.createElement("button", {
    key: item.value,
    onClick: () => setMode(item.value),
    style: {
      height: 38,
      padding: '0 16px',
      borderRadius: 14,
      border: 'none',
      background: mode === item.value ? T.navy : 'transparent',
      color: mode === item.value ? T.white : T.navyMid,
      cursor: 'pointer',
      fontSize: 13,
      fontWeight: 780,
      boxShadow: mode === item.value ? '0 10px 24px rgba(14,14,44,.16)' : 'none',
      transition: 'background .18s, color .18s, box-shadow .18s'
    }
  }, item.label)))), /*#__PURE__*/React.createElement("div", {
    className: dashboardOpen ? 'insightStageGrid insightStageGridDashboard' : 'insightStageGrid',
    style: {
      position: 'relative',
      minHeight: isMobile ? 640 : 620,
      display: 'grid',
      gridTemplateColumns: isMobile ? '1fr' : undefined,
      gap: dashboardOpen && !isMobile ? 20 : 0,
      alignItems: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      minHeight: isMobile ? 520 : 610,
      display: 'flex',
      alignItems: 'center',
      justifyContent: dashboardOpen && !isMobile ? 'flex-start' : 'center',
      transform: dashboardOpen && !isMobile ? 'translateX(8px) scale(.9)' : 'translateX(0) scale(1)',
      transition: 'transform .46s cubic-bezier(.2,.8,.2,1)'
    }
  }, /*#__PURE__*/React.createElement(Avatar3D, {
    waving: wave,
    compact: dashboardOpen && !isMobile,
    onClick: () => setWave(v => !v)
  }), !dashboardOpen && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(FloatTag, {
    drift: "up",
    depth: 6,
    tint: T.white,
    style: {
      top: isMobile ? 42 : 74,
      left: isMobile ? 6 : '13%',
      animationDelay: '.1s'
    }
  }, "\u7C89\u4E1D\u6570 2.3k"), /*#__PURE__*/React.createElement(FloatTag, {
    drift: "down",
    depth: 6,
    tint: T.primaryTint,
    style: {
      top: isMobile ? 18 : 42,
      right: isMobile ? 0 : '17%',
      animationDelay: '.44s'
    }
  }, "\u6574\u4F53\u70B9\u8D5E\u91CF 8w"), /*#__PURE__*/React.createElement(FloatTag, {
    drift: "up",
    depth: 6,
    tint: T.surfaceWh,
    style: {
      top: isMobile ? 118 : 168,
      left: isMobile ? -12 : '7%',
      animationDelay: '.9s'
    }
  }, "\u77E9\u9635\uFF1A\u5C0F\u7EA2\u4E66 / \u6296\u97F3 / \u89C6\u9891\u53F7"), /*#__PURE__*/React.createElement(FloatTag, {
    drift: "down",
    depth: 6,
    tint: T.surfaceWh,
    style: {
      top: isMobile ? 190 : 236,
      right: isMobile ? -16 : '8%',
      animationDelay: '1.2s'
    }
  }, "\u690D\u7269\u7C7B\u578B\u535A\u4E3B"), /*#__PURE__*/React.createElement(FloatTag, {
    drift: "up",
    depth: 6,
    tint: T.successTint,
    style: {
      bottom: isMobile ? 168 : 188,
      left: isMobile ? 8 : '18%',
      animationDelay: '1.55s'
    }
  }, "\u79D1\u666E"), /*#__PURE__*/React.createElement(FloatTag, {
    drift: "down",
    depth: 6,
    tint: T.irisTint,
    style: {
      bottom: isMobile ? 132 : 154,
      right: isMobile ? 20 : '22%',
      animationDelay: '1.9s'
    }
  }, "\u62BD\u8C61"), /*#__PURE__*/React.createElement(FloatTag, {
    drift: "up",
    depth: 7,
    tint: T.peachTint,
    style: {
      top: isMobile ? 90 : 112,
      left: isMobile ? '54%' : '56%',
      animationDelay: '1.08s'
    }
  }, "\u771F\u4EBA\u51FA\u955C"), /*#__PURE__*/React.createElement(FloatTag, {
    drift: "down",
    depth: 7,
    tint: T.white,
    style: {
      bottom: isMobile ? 84 : 110,
      left: isMobile ? '46%' : '55%',
      animationDelay: '.72s'
    }
  }, "\u89C6\u9891\u4E3A\u4E3B")), dashboardOpen && !isMobile && /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(FloatTag, {
    drift: "up",
    tint: T.white,
    style: {
      top: 94,
      left: 14,
      animationDelay: '.2s'
    }
  }, "IP \u5C0F\u7ED3"), /*#__PURE__*/React.createElement(FloatTag, {
    drift: "down",
    tint: T.irisTint,
    style: {
      bottom: 158,
      left: 22,
      animationDelay: '.8s'
    }
  }, "\u690D\u7269 / \u79D1\u666E"))), dashboardOpen && /*#__PURE__*/React.createElement("div", {
    style: {
      alignSelf: 'center',
      borderRadius: 30,
      border: '1px solid rgba(255,255,255,.7)',
      background: 'linear-gradient(180deg, rgba(255,255,255,.72), rgba(250,252,254,.52))',
      boxShadow: '0 22px 54px rgba(14,14,44,.10), inset 0 1px 0 rgba(255,255,255,.9)',
      backdropFilter: 'blur(24px) saturate(1.28)',
      WebkitBackdropFilter: 'blur(24px) saturate(1.28)',
      padding: isMobile ? 16 : 20,
      display: 'grid',
      gap: 16,
      animation: 'fadeInScale .36s cubic-bezier(.2,.8,.2,1) both'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      justifyContent: 'space-between',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11.5,
      color: T.navyLight,
      fontWeight: 820,
      letterSpacing: '0.08em',
      textTransform: 'uppercase'
    }
  }, "\u6570\u636E\u770B\u677F"), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 6,
      fontSize: 20,
      lineHeight: 1.18,
      fontWeight: 800,
      color: T.navy,
      letterSpacing: '-0.025em'
    }
  }, "\u8D26\u53F7\u7EA7\u8D8B\u52BF\u548C\u5355\u6761\u5185\u5BB9\u6307\u6807")), /*#__PURE__*/React.createElement("span", {
    style: {
      height: 30,
      padding: '0 10px',
      borderRadius: 999,
      background: T.successTint,
      color: '#168b73',
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      fontSize: 11.5,
      fontWeight: 780
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "trending",
    size: 12
  }), "7\u65E5\u4E0A\u5347")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: isMobile ? 'repeat(2, minmax(0, 1fr))' : 'repeat(4, minmax(0, 1fr))',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement(MetricTile, {
    label: "\u66DD\u5149",
    value: "86w",
    sub: "+18.4%",
    accent: T.iris
  }), /*#__PURE__*/React.createElement(MetricTile, {
    label: "\u70B9\u8D5E",
    value: "8w",
    sub: "+9.7%",
    accent: T.success
  }), /*#__PURE__*/React.createElement(MetricTile, {
    label: "\u6536\u85CF",
    value: "2.8w",
    sub: "+12.1%",
    accent: T.primary
  }), /*#__PURE__*/React.createElement(MetricTile, {
    label: "\u6DA8\u7C89",
    value: "+1,246",
    sub: "+22.6%",
    accent: T.peach
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 24,
      background: 'rgba(255,255,255,.58)',
      border: '1px solid rgba(255,255,255,.62)',
      boxShadow: 'inset 0 1px 0 rgba(255,255,255,.86)',
      padding: '16px 16px 12px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13,
      fontWeight: 780,
      color: T.navy
    }
  }, "\u8D26\u53F7\u8D8B\u52BF"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 11.5,
      color: T.navyLight,
      fontFamily: T.fontMono
    }
  }, "May 01 - May 07")), /*#__PURE__*/React.createElement(MiniLineChart, null)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: isMobile ? '1fr' : 'minmax(0, .9fr) minmax(0, 1.1fr)',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 22,
      background: 'rgba(255,255,255,.58)',
      border: '1px solid rgba(255,255,255,.62)',
      padding: 16,
      display: 'grid',
      gap: 11
    }
  }, trendRows.map(row => /*#__PURE__*/React.createElement(RadarBar, _extends({
    key: row.label
  }, row)))), /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 22,
      background: 'rgba(255,255,255,.58)',
      border: '1px solid rgba(255,255,255,.62)',
      padding: 14,
      display: 'grid',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 780,
      color: T.navy,
      marginBottom: 2
    }
  }, "\u5355\u6761\u5185\u5BB9\u6307\u6807"), filteredContents.slice(0, 3).map((item, i) => /*#__PURE__*/React.createElement("div", {
    key: item.id,
    style: {
      borderRadius: 16,
      padding: '10px 12px',
      background: i === 0 ? 'rgba(239,239,253,.78)' : 'rgba(250,252,254,.72)',
      border: `1px solid ${T.hairlineSoft}`,
      display: 'grid',
      gap: 6
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12.5,
      fontWeight: 760,
      color: T.navy,
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }
  }, item.title), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10,
      flexWrap: 'wrap',
      fontSize: 11.5,
      color: T.navyLight
    }
  }, /*#__PURE__*/React.createElement("span", null, "\u66DD\u5149 ", item.exposure), /*#__PURE__*/React.createElement("span", null, "\u70B9\u8D5E ", item.likes), /*#__PURE__*/React.createElement("span", null, "\u6536\u85CF ", item.saves), /*#__PURE__*/React.createElement("span", null, "\u8BC4\u8BBA ", item.comments)))))))))), /*#__PURE__*/React.createElement("section", {
    style: {
      display: 'grid',
      gap: 22,
      paddingBottom: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 30,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.84)',
      boxShadow: '0 18px 44px rgba(14,14,44,.08), inset 0 1px 0 rgba(255,255,255,.78)',
      padding: 22
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 10,
      flexWrap: 'wrap',
      marginBottom: 16
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      fontWeight: 800,
      letterSpacing: '0.08em',
      textTransform: 'uppercase',
      color: T.navyLight
    }
  }, "\u590D\u76D8\u6C47\u62A5"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13.5,
      color: T.navyMid,
      marginTop: 6
    }
  }, "\u70B9\u51FB\u4E00\u6761\u5185\u5BB9\uFF0C\u67E5\u770B Agent \u590D\u76D8\u5206\u6790\u3002")), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'relative',
      minWidth: isMobile ? '100%' : 260,
      flex: isMobile ? '1 1 100%' : '0 1 260px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: 40,
      borderRadius: 14,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.86)',
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      padding: '0 12px',
      boxShadow: T.shadowXs
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "search",
    size: 15,
    color: T.navyLight
  }), /*#__PURE__*/React.createElement("input", {
    value: search,
    onChange: e => setSearch(e.target.value),
    placeholder: "\u641C\u7D22\u590D\u76D8\u5185\u5BB9...",
    style: {
      flex: 1,
      border: 'none',
      outline: 'none',
      background: 'transparent',
      fontSize: 13,
      color: T.navy
    }
  })))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: isMobile ? '1fr' : '360px minmax(0, 1fr)',
      gap: 14,
      minHeight: 460
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 22,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.84)',
      padding: 10,
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 6
    }
  }, filteredContents.map(item => /*#__PURE__*/React.createElement("button", {
    key: item.id,
    onClick: () => setSelectedContent(item),
    style: {
      textAlign: 'left',
      border: 'none',
      cursor: 'pointer',
      borderRadius: 14,
      padding: '12px 12px',
      background: selectedContent.id === item.id ? T.irisTint : 'transparent',
      transition: 'background .16s'
    },
    onMouseEnter: e => {
      if (selectedContent.id !== item.id) e.currentTarget.style.background = T.surface;
    },
    onMouseLeave: e => {
      if (selectedContent.id !== item.id) e.currentTarget.style.background = 'transparent';
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13.2,
      fontWeight: 740,
      color: T.navy,
      lineHeight: 1.4
    }
  }, item.title), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 10.5,
      color: T.navyLight,
      fontFamily: T.fontMono
    }
  }, item.date)), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8,
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      fontSize: 11.5,
      color: T.navyLight
    }
  }, /*#__PURE__*/React.createElement("span", null, item.platform), /*#__PURE__*/React.createElement("span", null, "\xB7"), /*#__PURE__*/React.createElement("span", null, item.type), /*#__PURE__*/React.createElement("span", null, "\xB7"), /*#__PURE__*/React.createElement("span", null, "\u66DD\u5149 ", item.exposure)))))), /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 22,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.84)',
      padding: 18,
      display: 'flex',
      flexDirection: 'column',
      gap: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 8,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      color: T.navyLight,
      letterSpacing: '0.08em',
      textTransform: 'uppercase',
      fontWeight: 800
    }
  }, "Agent \u590D\u76D8\u6C47\u62A5"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 18,
      fontWeight: 780,
      color: T.navy,
      marginTop: 6
    }
  }, selectedContent.title)), /*#__PURE__*/React.createElement("button", {
    style: {
      height: 34,
      padding: '0 12px',
      borderRadius: 12,
      border: 'none',
      background: T.navy,
      color: T.white,
      cursor: 'pointer',
      fontSize: 12,
      fontWeight: 760,
      position: 'relative'
    }
  }, "\u590D\u76D8\u65E5\u62A5\u8BA2\u9605", /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      top: -36,
      right: 0,
      opacity: 0,
      pointerEvents: 'none',
      padding: '8px 10px',
      borderRadius: 10,
      background: T.navy,
      color: T.white,
      fontSize: 11,
      whiteSpace: 'nowrap',
      boxShadow: T.shadowLg,
      transform: 'translateY(4px)',
      transition: 'opacity .16s, transform .16s'
    },
    className: "subHint"
  }, "\u53EF\u6536\u5230\u6BCF\u65E5\u590D\u76D8\u62A5\u544A\uFF08\u53EF\u9009\u4EA7\u54C1\u5185\u901A\u77E5 / \u5FAE\u4FE1 / \u98DE\u4E66\u8FDB\u884C\u63A8\u9001\uFF09"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gap: 10
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 16,
      background: T.surfaceWh,
      border: `1px solid ${T.hairlineSoft}`,
      padding: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 780,
      color: T.navy,
      marginBottom: 8
    }
  }, "\u8FD9\u6761\u5185\u5BB9\u8868\u73B0\u600E\u4E48\u6837"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13.5,
      lineHeight: 1.78,
      color: T.navyMid
    }
  }, "\u8FD9\u6761\u5185\u5BB9\u7684\u6536\u85CF\u548C\u6DA8\u7C89\u6548\u7387\u660E\u663E\u9AD8\u4E8E\u5E73\u5747\u503C\uFF0C\u8BF4\u660E\u6807\u9898\u5207\u5165\u70B9\u548C\u5C01\u9762\u53CD\u5DEE\u611F\u6293\u4EBA\u3002\u8BC4\u8BBA\u6570\u4E0D\u7B97\u7206\u53D1\uFF0C\u4F46\u8BF4\u660E\u7528\u6237\u4E3B\u8981\u4EE5\u201C\u4FDD\u5B58\u53C2\u8003\u201D\u4E3A\u4E3B\u3002")), /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 16,
      background: T.surfaceWh,
      border: `1px solid ${T.hairlineSoft}`,
      padding: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 780,
      color: T.navy,
      marginBottom: 8
    }
  }, "\u4E3A\u4EC0\u4E48\u597D / \u4E3A\u4EC0\u4E48\u4E0D\u597D"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13.5,
      lineHeight: 1.78,
      color: T.navyMid
    }
  }, "\u597D\u5728\u89C6\u89C9\u51B2\u51FB\u8DB3\u591F\uFF0C\u4FE1\u606F\u5BC6\u5EA6\u9002\u4E2D\uFF0C\u4E14\u5207\u4E2D\u201C\u76F4\u7537\u517B\u82B1\u201D\u7684\u53CD\u5DEE\u70B9\u3002\u4E0D\u8DB3\u662F\u7ED3\u5C3E\u4E92\u52A8\u7565\u5F31\uFF0C\u8BC4\u8BBA\u533A\u5E26\u52A8\u8FD8\u53EF\u4EE5\u66F4\u660E\u786E\u3002")), /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 16,
      background: T.surfaceWh,
      border: `1px solid ${T.hairlineSoft}`,
      padding: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 780,
      color: T.navy,
      marginBottom: 8
    }
  }, "\u4E0B\u4E00\u6B65\u5EFA\u8BAE"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13.5,
      lineHeight: 1.78,
      color: T.navyMid
    }
  }, "\u540E\u7EED\u53EF\u4EE5\u628A\u8FD9\u7C7B\u5185\u5BB9\u7EE7\u7EED\u505A\u6210\u7CFB\u5217\u5C01\u9762\u6A21\u677F\uFF0C\u7EDF\u4E00\u89C6\u89C9\u9524\uFF1B\u540C\u65F6\u5728\u7ED3\u5C3E\u52A0\u4E0A\u201C\u8BA9\u7528\u6237\u8BC4\u8BBA\u81EA\u5BB6\u54C1\u79CD\u201D\u7684\u63D0\u95EE\uFF0C\u5F3A\u5316\u4E92\u52A8\u3002")))))), /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 30,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.84)',
      boxShadow: '0 18px 44px rgba(14,14,44,.08), inset 0 1px 0 rgba(255,255,255,.78)',
      padding: 22
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 10,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      fontWeight: 800,
      letterSpacing: '0.08em',
      textTransform: 'uppercase',
      color: T.navyLight
    }
  }, "\u9886\u57DF\u70ED\u70B9\u957F\u671F\u8DDF\u8E2A + \u63A8\u9001\u6C47\u62A5"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13.5,
      color: T.navyMid,
      marginTop: 6
    }
  }, "\u4ED8\u8D39\u89E3\u9501\u540E\u53EF\u957F\u671F\u76D1\u6D4B\u67D0\u4E00\u9886\u57DF\u5185\u5BB9\u8D8B\u52BF\u3001\u6D41\u91CF\u8D8B\u52BF\u4E0E\u65B0\u9C9C\u9009\u9898\u8D44\u8BAF\u3002")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'inline-flex',
      gap: 4,
      padding: 4,
      borderRadius: 16,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.82)',
      boxShadow: T.shadowXs
    }
  }, ['内容趋势', '流量趋势', '新鲜选题资讯'].map(t => /*#__PURE__*/React.createElement("button", {
    key: t,
    onClick: () => setHotTab(t),
    style: {
      height: 36,
      padding: '0 14px',
      borderRadius: 12,
      border: 'none',
      background: hotTab === t ? T.navy : 'transparent',
      color: hotTab === t ? T.white : T.navyMid,
      cursor: 'pointer',
      fontSize: 12.5,
      fontWeight: 760
    }
  }, t)))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 16,
      display: 'grid',
      gridTemplateColumns: isMobile ? '1fr' : 'repeat(4, minmax(0, 1fr))',
      gap: 12
    }
  }, hotCards.map(card => /*#__PURE__*/React.createElement("div", {
    key: card.title,
    style: {
      borderRadius: 18,
      padding: 16,
      background: 'linear-gradient(180deg, #fff, #f8fbfd)',
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: T.shadowXs,
      minHeight: 128
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12.5,
      fontWeight: 780,
      color: T.navy
    }
  }, card.title), /*#__PURE__*/React.createElement("span", {
    style: {
      color: card.accent,
      fontSize: 13,
      fontWeight: 780
    }
  }, card.trend)), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8,
      fontSize: 12.5,
      lineHeight: 1.7,
      color: T.navyMid
    }
  }, card.sub), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 12,
      display: 'flex',
      alignItems: 'center',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 8,
      height: 8,
      borderRadius: '50%',
      background: card.accent,
      boxShadow: `0 0 0 5px ${card.accent}18`
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 11.5,
      color: T.navyLight
    }
  }, "\u53D1\u73B0\u6F5C\u5728\u673A\u4F1A\u65F6\u4E3B\u52A8\u6807\u6CE8\u63A8\u8350"))))))))), /*#__PURE__*/React.createElement("style", null, `
        @keyframes petalBreath {
          0%, 100% { scale: 1; filter: saturate(1); }
          50% { scale: 1.025; filter: saturate(1.08); }
        }
        @keyframes avatarAura {
          0%, 100% { opacity: .56; transform: translateX(-50%) scale(.96); }
          50% { opacity: .78; transform: translateX(-50%) scale(1.04); }
        }
        .insightStageGrid {
          grid-template-columns: 1fr;
          transition: grid-template-columns .46s cubic-bezier(.2,.8,.2,1);
        }
        .insightStageGridDashboard {
          grid-template-columns: minmax(300px, .72fr) minmax(520px, 1.28fr);
        }
        @media (max-width: 760px) {
          .insightStageGrid,
          .insightStageGridDashboard {
            grid-template-columns: 1fr;
          }
        }
        .subHint { opacity: 0; transform: translateY(4px); }
        button:hover .subHint { opacity: 1; transform: translateY(0); }
      `));
};
window.InsightsPage = InsightsPage;
/* ─── Generation Chat Steps ─── */

/* ── Common atoms ── */

const Avatar = ({
  kind = 'nori'
}) => {
  if (kind === 'user') {
    return /*#__PURE__*/React.createElement("div", {
      style: {
        width: 28,
        height: 28,
        borderRadius: '50%',
        flexShrink: 0,
        background: `linear-gradient(135deg, ${T.iris}, ${T.peach})`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: T.white,
        fontSize: 11.5,
        fontWeight: 700
      }
    }, "L");
  }
  return /*#__PURE__*/React.createElement(NoriLogo, {
    size: 28
  });
};
const Bubble = ({
  from = 'nori',
  children,
  style
}) => {
  const isUser = from === 'user';
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10,
      alignItems: 'flex-start',
      flexDirection: isUser ? 'row-reverse' : 'row',
      animation: 'fadeIn .32s ease both',
      ...style
    }
  }, /*#__PURE__*/React.createElement(Avatar, {
    kind: isUser ? 'user' : 'nori'
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: '92%',
      padding: isUser ? '10px 14px' : 0,
      borderRadius: isUser ? 14 : 0,
      background: isUser ? T.navy : 'transparent',
      color: isUser ? T.white : T.navy,
      fontSize: 14,
      lineHeight: 1.65,
      fontWeight: 450,
      flex: isUser ? '0 1 auto' : '1 1 auto'
    }
  }, children));
};
const NoriSays = ({
  children,
  style
}) => /*#__PURE__*/React.createElement(Bubble, {
  from: "nori",
  style: style
}, /*#__PURE__*/React.createElement("div", {
  style: {
    paddingTop: 4,
    fontSize: 14,
    lineHeight: 1.7,
    color: T.navy,
    fontWeight: 450
  }
}, children));
const TypingDots = () => /*#__PURE__*/React.createElement("div", {
  style: {
    display: 'inline-flex',
    gap: 3,
    padding: '4px 0'
  }
}, [0, 1, 2].map(i => /*#__PURE__*/React.createElement("span", {
  key: i,
  style: {
    width: 5,
    height: 5,
    borderRadius: '50%',
    background: T.navyLight,
    animation: `pulse 1.2s ${i * 0.15}s infinite`
  }
})));

/* ── Step 1: 关键信息确认 ── */
const Step1KeyInfo = ({
  onComplete,
  onSkip
}) => {
  const [audience, setAudience] = React.useState(null);
  const [style, setStyle] = React.useState(null);
  const [length, setLength] = React.useState(null);
  const ready = audience && style && length;
  const Question = ({
    q,
    options,
    value,
    onPick,
    hint
  }) => /*#__PURE__*/React.createElement("div", {
    style: {
      marginBottom: 18
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      marginBottom: 10
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 13.5,
      fontWeight: 600,
      color: T.navy
    }
  }, q), hint && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 11.5,
      color: T.navyLight
    }
  }, hint)), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexWrap: 'wrap',
      gap: 8
    }
  }, options.map(o => {
    const active = value === o.id;
    return /*#__PURE__*/React.createElement("button", {
      key: o.id,
      onClick: () => onPick(o.id),
      style: {
        padding: '8px 14px',
        borderRadius: 99,
        border: `1px solid ${active ? T.navy : T.hairline}`,
        background: active ? T.navy : T.white,
        color: active ? T.white : T.navy,
        fontSize: 12.5,
        fontWeight: 500,
        cursor: 'pointer',
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        transition: 'all .12s'
      }
    }, o.emoji && /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 13
      }
    }, o.emoji), o.label);
  })));
  return /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 16
    }
  }, "\u597D\u4E3B\u610F\uFF01\u300C", /*#__PURE__*/React.createElement("b", null, "\u731B\u7537\u559C\u6B22\u7684\u7C89\u8272\u690D\u7269"), "\u300D\u8FD9\u4E2A\u89D2\u5EA6\u53CD\u5DEE\u611F\u5F88\u6709\u6897\u3002\u5728\u5F00\u59CB\u524D\uFF0C \u6211\u60F3\u8DDF\u4F60\u786E\u8BA4\u51E0\u4E2A\u5173\u952E\u4FE1\u606F\uFF0C\u8FD9\u6837\u751F\u6210\u7684\u5185\u5BB9\u4F1A\u66F4\u7CBE\u51C6 \u2014\u2014"), /*#__PURE__*/React.createElement("div", {
    style: {
      background: T.white,
      border: `1px solid ${T.hairline}`,
      borderRadius: 14,
      padding: '18px 20px',
      boxShadow: T.shadowXs
    }
  }, /*#__PURE__*/React.createElement(Question, {
    q: "\u76EE\u6807\u8BFB\u8005\u662F\u8C01\uFF1F",
    hint: "\u9009\u4E00\u4E2A\u6700\u8D34\u8FD1\u7684\u753B\u50CF",
    value: audience,
    onPick: setAudience,
    options: [{
      id: 'novice',
      label: '植物新手',
      emoji: '🌱'
    }, {
      id: 'cat-people',
      label: '宠物 / 室内派',
      emoji: '🐈'
    }, {
      id: 'gym-bro',
      label: '健身硬汉',
      emoji: '💪'
    }, {
      id: 'pro',
      label: '园艺老手',
      emoji: '🪴'
    }, {
      id: 'all',
      label: '泛用户'
    }]
  }), /*#__PURE__*/React.createElement(Question, {
    q: "\u4F60\u60F3\u505A\u6210\u4EC0\u4E48\u98CE\u683C\uFF1F",
    value: style,
    onPick: setStyle,
    options: [{
      id: 'edu',
      label: '硬核科普'
    }, {
      id: 'meme',
      label: '反差梗 / 整活'
    }, {
      id: 'visual',
      label: '颜值向 / 美图'
    }, {
      id: 'guide',
      label: '实用养护'
    }]
  }), /*#__PURE__*/React.createElement(Question, {
    q: "\u671F\u671B\u957F\u5EA6\uFF1F",
    value: length,
    onPick: setLength,
    options: [{
      id: 's',
      label: '短平快 · 6 图以内'
    }, {
      id: 'm',
      label: '标准 · 8–10 图'
    }, {
      id: 'l',
      label: '深度 · 长文 + 图'
    }]
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginTop: 6,
      paddingTop: 14,
      borderTop: `1px solid ${T.hairlineSoft}`
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: onSkip,
    style: {
      background: 'transparent',
      border: 'none',
      cursor: 'pointer',
      color: T.navyLight,
      fontSize: 12.5,
      fontWeight: 500,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 5,
      padding: '6px 4px'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "skip",
    size: 12
  }), " \u8DF3\u8FC7\u8FD9\u6B65"), /*#__PURE__*/React.createElement("button", {
    onClick: () => onComplete({
      audience,
      style,
      length
    }),
    disabled: !ready,
    style: {
      height: 38,
      padding: '0 18px',
      borderRadius: 10,
      border: 'none',
      background: ready ? T.navy : T.surface,
      color: ready ? T.primary : T.navyLight,
      fontSize: 13,
      fontWeight: 600,
      cursor: ready ? 'pointer' : 'not-allowed',
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      boxShadow: ready ? T.shadowSm : 'none',
      transition: 'all .15s'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "sparkles",
    size: 13
  }), " \u5F00\u59CB\u751F\u6210"))));
};

/* ── Step 2: 拆解爆款 + 选题方案 ── */

const HotCard = ({
  post
}) => {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: T.white,
      border: `1px solid ${T.hairline}`,
      borderRadius: 14,
      overflow: 'hidden',
      cursor: 'pointer',
      transition: 'all .15s',
      display: 'flex',
      flexDirection: 'column'
    },
    onMouseEnter: e => {
      e.currentTarget.style.transform = 'translateY(-2px)';
      e.currentTarget.style.boxShadow = T.shadowMd;
    },
    onMouseLeave: e => {
      e.currentTarget.style.transform = 'translateY(0)';
      e.currentTarget.style.boxShadow = 'none';
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      aspectRatio: '3 / 4',
      background: post.bg,
      position: 'relative',
      overflow: 'hidden',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, post.visual, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: 8,
      left: 8,
      padding: '3px 7px',
      borderRadius: 99,
      background: 'rgba(14,14,44,.7)',
      color: T.white,
      fontSize: 10,
      fontWeight: 600,
      letterSpacing: '0.04em',
      display: 'inline-flex',
      alignItems: 'center',
      gap: 4,
      backdropFilter: 'blur(4px)'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "trending",
    size: 9
  }), " ", post.platform), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: 8,
      right: 8,
      padding: '3px 7px',
      borderRadius: 4,
      background: T.primary,
      color: T.navy,
      fontSize: 10,
      fontWeight: 700
    }
  }, post.hotScore)), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '12px 12px 12px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12.5,
      fontWeight: 600,
      color: T.navy,
      lineHeight: 1.45,
      marginBottom: 8,
      display: '-webkit-box',
      WebkitLineClamp: 2,
      WebkitBoxOrient: 'vertical',
      overflow: 'hidden'
    }
  }, post.title), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      fontSize: 11,
      color: T.navyLight
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 3
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "heart",
    size: 11
  }), " ", post.likes), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 3
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "bookmark",
    size: 11
  }), " ", post.saves), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: 'auto',
      fontFamily: T.fontMono,
      fontSize: 10
    }
  }, post.time))));
};

/* placeholder visuals for the four hot posts */
const FlowerVisual = ({
  palette
}) => /*#__PURE__*/React.createElement("svg", {
  viewBox: "0 0 100 130",
  width: "100%",
  height: "100%",
  style: {
    display: 'block'
  },
  preserveAspectRatio: "xMidYMid slice"
}, /*#__PURE__*/React.createElement("rect", {
  width: "100",
  height: "130",
  fill: palette[0]
}), /*#__PURE__*/React.createElement("path", {
  d: "M10 110 Q 5 70, 30 60 Q 55 50, 50 100 Q 45 130, 20 125 Z",
  fill: palette[1],
  opacity: ".85"
}), [[40, 30, 18, palette[2]], [62, 45, 14, palette[3]], [55, 70, 16, palette[2]], [78, 28, 10, palette[3]], [30, 55, 11, palette[3]]].map(([cx, cy, r, c], i) => /*#__PURE__*/React.createElement("g", {
  key: i
}, [0, 72, 144, 216, 288].map(a => {
  const rad = a * Math.PI / 180;
  return /*#__PURE__*/React.createElement("ellipse", {
    key: a,
    cx: cx + Math.cos(rad) * r * 0.55,
    cy: cy + Math.sin(rad) * r * 0.55,
    rx: r * 0.6,
    ry: r * 0.45,
    fill: c,
    opacity: 0.85,
    transform: `rotate(${a} ${cx} ${cy})`
  });
}), /*#__PURE__*/React.createElement("circle", {
  cx: cx,
  cy: cy,
  r: r * 0.25,
  fill: palette[4]
}))));
const Step2HotPosts = ({
  onSelectAngle
}) => {
  const posts = [{
    title: '深蓝幕布下的粉蝶兰，谁懂这种反差感',
    platform: '小红书',
    hotScore: 'HOT 9.2',
    likes: '5.6w',
    saves: '2.6w',
    time: '2 天前',
    bg: '#1a3a5c',
    visual: /*#__PURE__*/React.createElement(FlowerVisual, {
      palette: ['#1a3a5c', '#2c5a3c', '#f5b8c8', '#e896b0', '#fdf5f5']
    })
  }, {
    title: '硬汉养花指北 · 8 种粉得直男都爱的植物',
    platform: '小红书',
    hotScore: 'HOT 8.8',
    likes: '4.2w',
    saves: '1.9w',
    time: '5 天前',
    bg: '#2a1a2e',
    visual: /*#__PURE__*/React.createElement(FlowerVisual, {
      palette: ['#2a1a2e', '#3c5a4c', '#fab1c4', '#f78bb0', T.peachTint]
    })
  }, {
    title: '不养仙人掌后，我家粉色植物收藏 Top 6',
    platform: '小红书',
    hotScore: 'HOT 8.5',
    likes: '3.8w',
    saves: '1.5w',
    time: '1 周前',
    bg: '#fdf0ee',
    visual: /*#__PURE__*/React.createElement(FlowerVisual, {
      palette: ['#fdf0ee', '#9bbfa8', '#e8a0bc', '#d987a8', '#fff']
    })
  }, {
    title: '阳台改造 | 把粉红仙境搬回家 ¥300 搞定',
    platform: '小红书',
    hotScore: 'HOT 7.9',
    likes: '3.1w',
    saves: '1.2w',
    time: '2 周前',
    bg: '#3a2c4a',
    visual: /*#__PURE__*/React.createElement(FlowerVisual, {
      palette: ['#3a2c4a', '#5c7a5c', '#f0a8c4', '#dc8aa8', '#fff']
    })
  }];
  const [openConclusion, setOpenConclusion] = React.useState(false);
  const [phase, setPhase] = React.useState(0);
  React.useEffect(() => {
    const timers = [setTimeout(() => setPhase(1), 1000), setTimeout(() => setPhase(2), 2600), setTimeout(() => setPhase(3), 4300)];
    return () => timers.forEach(clearTimeout);
  }, []);
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 14
    }
  }, "\u6536\u5230\uFF0C\u5F00\u59CB\u52A8\u4E86 \u2728 \u6211\u5148\u53BB\u5C0F\u7EA2\u4E66 / \u6296\u97F3\u4E0A\u6252\u4E86\u4E00\u5708 ", /*#__PURE__*/React.createElement("b", null, "\u7C89\u8272\u690D\u7269"), " \u76F8\u5173\u7206\u6B3E\uFF0C \u8FD9\u4E2A\u8BDD\u9898\u6709\u771F\u5B9E\u7684\u6D41\u91CF\u76D8\u5B50 \u2014\u2014 \u8FD1 30 \u5929\u7206\u6B3E 200+ \u7BC7\uFF0C\u5E73\u5747\u4E92\u52A8\u7387 5.8%\uFF0C", /*#__PURE__*/React.createElement("span", {
    style: {
      color: T.success,
      fontWeight: 600
    }
  }, "\u300C\u53EF\u6253\u9020\u4E3A\u7206\u6B3E\u300D\u8BCA\u65AD\u901A\u8FC7"), "\u3002"), /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 14,
      color: T.navyMid
    }
  }, "\u4E0B\u9762\u662F 4 \u7BC7\u53EF\u53C2\u8003\u7684\u7206\u6B3E\uFF0C\u5DF2\u6309\u9009\u9898\u8D34\u5408\u5EA6\u6392\u5E8F \u2014\u2014"), phase === 0 && /*#__PURE__*/React.createElement(TypingDots, null)), phase >= 1 && /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: 38,
      marginTop: -6,
      animation: 'fadeIn .28s ease'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(4, 1fr)',
      gap: 12,
      marginBottom: 14
    }
  }, posts.map((p, i) => /*#__PURE__*/React.createElement(HotCard, {
    key: i,
    post: p
  }))), /*#__PURE__*/React.createElement("button", {
    style: {
      fontSize: 12,
      color: T.navyMid,
      background: 'transparent',
      border: 'none',
      cursor: 'pointer',
      padding: '4px 0',
      fontWeight: 500,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 4
    }
  }, "\u67E5\u770B\u5176\u4F59 21 \u7BC7\u7206\u6B3E ", /*#__PURE__*/React.createElement(Icon, {
    name: "chevronRight",
    size: 11
  }))), phase >= 2 && /*#__PURE__*/React.createElement(NoriSays, {
    style: {
      marginTop: 22
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 14
    }
  }, "\u6211\u628A\u8FD9\u4E9B\u7206\u6B3E\u7684\u5171\u540C\u7ED3\u6784\u62C6\u7ED9\u4F60\u770B \u2014\u2014"), /*#__PURE__*/React.createElement("div", {
    style: {
      background: T.white,
      border: `1px solid ${T.hairline}`,
      borderRadius: 14,
      padding: '4px 0',
      overflow: 'hidden'
    }
  }, [{
    label: '标题公式',
    body: '「反差词 + 具体植物 + 情绪/态度」 例如「猛男 / 直男 + 粉色植物 + 谁懂这种反差感」',
    icon: 'edit'
  }, {
    label: '封面参考',
    body: '深色背景 +  单株植物特写 + 极简留白；冷暖反差是关键，避免甜腻',
    icon: 'image'
  }, {
    label: '内文长度',
    body: '8 张图 / 600–800 字。「人设钩子 → 6 种植物 → 养护 Tips → 互动结尾」',
    icon: 'document'
  }, {
    label: '互动钩子',
    body: '结尾抛 1 个具体问题：「你家有几盆？」「猛男能 hold 几种？」',
    icon: 'chat'
  }].map((row, i, arr) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      display: 'flex',
      alignItems: 'flex-start',
      gap: 14,
      padding: '14px 18px',
      borderBottom: i < arr.length - 1 ? `1px solid ${T.hairlineSoft}` : 'none'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 28,
      height: 28,
      borderRadius: 8,
      background: T.irisTint,
      color: T.iris,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0,
      marginTop: 1
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: row.icon,
    size: 14
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      fontWeight: 700,
      letterSpacing: '0.04em',
      color: T.navy,
      marginBottom: 4,
      textTransform: 'uppercase'
    }
  }, row.label), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      color: T.navyMid,
      lineHeight: 1.6
    }
  }, row.body)))))), phase >= 3 && /*#__PURE__*/React.createElement(NoriSays, {
    style: {
      marginTop: 22
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 14
    }
  }, "\u7EFC\u5408\u4E0A\u9762\u7684\u62C6\u89E3\uFF0C\u6211\u7ED9\u4F60\u7684\u9009\u9898\u7ED3\u8BBA\u662F \u2014\u2014", /*#__PURE__*/React.createElement("span", {
    style: {
      color: T.navyLight,
      fontSize: 12.5
    }
  }, "\uFF08\u70B9\u51FB\u5C55\u5F00\u53F3\u8FB9 Canvas \u67E5\u770B\u5B8C\u6574\u7B56\u7565\uFF09")), /*#__PURE__*/React.createElement("button", {
    onClick: () => onSelectAngle(),
    style: {
      width: '100%',
      textAlign: 'left',
      background: T.white,
      border: `1px solid ${T.hairline}`,
      borderRadius: 14,
      padding: '14px 18px',
      display: 'flex',
      alignItems: 'center',
      gap: 14,
      cursor: 'pointer',
      transition: 'all .15s'
    },
    onMouseEnter: e => {
      e.currentTarget.style.borderColor = 'rgba(75,77,237,.32)';
      e.currentTarget.style.boxShadow = T.shadowSm;
    },
    onMouseLeave: e => {
      e.currentTarget.style.borderColor = T.hairline;
      e.currentTarget.style.boxShadow = 'none';
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 44,
      height: 44,
      borderRadius: 10,
      background: T.primary,
      color: T.navy,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "target",
    size: 22
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 14,
      fontWeight: 700,
      color: T.navy,
      marginBottom: 2
    }
  }, "\u9009\u9898\u7ED3\u8BBA \xB7 \u53CD\u5DEE\u4EBA\u8BBE + 6 \u79CD\u7C89\u8272\u690D\u7269\u79CD\u8349"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      color: T.navyLight
    }
  }, "\u5C0F\u7EA2\u4E66\u56FE\u6587 \xB7 8 \u5F20\u56FE \xB7 \u9884\u4F30\u7206\u6B3E\u7387 72% \xB7 Nori \u63A8\u8350")), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      padding: '6px 12px',
      borderRadius: 8,
      background: T.surface,
      color: T.navy,
      fontSize: 12,
      fontWeight: 600
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "expand",
    size: 12
  }), " \u5728 Canvas \u67E5\u770B"))));
};

/* ── Step 3: 素材调研 ── */

const SourceRow = ({
  source,
  idx
}) => {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      padding: '10px 14px',
      borderRadius: 10,
      cursor: 'pointer',
      transition: 'background .12s'
    },
    onMouseEnter: e => e.currentTarget.style.background = T.surface,
    onMouseLeave: e => e.currentTarget.style.background = 'transparent'
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 24,
      height: 24,
      borderRadius: 6,
      background: source.tint,
      color: source.color,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: source.icon,
    size: 12
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12.5,
      fontWeight: 500,
      color: T.navy,
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }
  }, source.title), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 10.5,
      color: T.navyLight,
      fontFamily: T.fontMono
    }
  }, source.host, " \xB7 ", source.kind)), /*#__PURE__*/React.createElement(Icon, {
    name: "link",
    size: 12,
    color: T.navyLight
  }));
};
const Step3Research = ({
  selectedAsset,
  onSelectAsset
}) => {
  const [imgsExpanded, setImgsExpanded] = React.useState(false);
  const [phase, setPhase] = React.useState(0);
  const sources = [{
    title: '《观赏植物色素分布与花色稳定性研究》',
    host: 'cnki.net',
    kind: 'PDF · 论文',
    icon: 'book',
    tint: T.irisTint,
    color: T.iris
  }, {
    title: '粉掌、姬秋丽、花叶冷水花养护要点',
    host: 'huayuan.com',
    kind: '科普文章',
    icon: 'document',
    tint: '#fff8e0',
    color: '#c89b00'
  }, {
    title: 'Pink Plants Care Guide 2025',
    host: 'gardenista.com',
    kind: '英文 Guide',
    icon: 'globe',
    tint: T.successTint,
    color: T.success
  }, {
    title: '【粉色植物 Top10】完整盘点',
    host: 'bilibili.com',
    kind: '视频 · 7:32',
    icon: 'play',
    tint: '#ffe5ec',
    color: '#ff4488'
  }];

  /* image grid: 4 highlighted + 8 hidden */
  const Img = ({
    asset,
    featured
  }) => /*#__PURE__*/React.createElement("div", {
    style: {
      borderRadius: 10,
      overflow: 'hidden',
      background: asset.palette[0],
      aspectRatio: '1 / 1.25',
      cursor: 'pointer',
      transition: 'transform .15s',
      position: 'relative',
      outline: selectedAsset?.id === asset.id ? `2px solid ${T.primary}` : 'none',
      boxShadow: selectedAsset?.id === asset.id ? '0 0 0 5px rgba(214,255,0,.14)' : 'none'
    },
    onClick: () => onSelectAsset && onSelectAsset(asset),
    onMouseEnter: e => e.currentTarget.style.transform = 'scale(1.02)',
    onMouseLeave: e => e.currentTarget.style.transform = 'scale(1)'
  }, /*#__PURE__*/React.createElement(FlowerVisual, {
    palette: asset.palette
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: 6,
      right: 6,
      width: 22,
      height: 22,
      borderRadius: 6,
      background: selectedAsset?.id === asset.id ? T.primary : 'rgba(0,0,0,.5)',
      color: selectedAsset?.id === asset.id ? T.navy : T.white,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backdropFilter: 'blur(4px)',
      opacity: selectedAsset?.id === asset.id ? 1 : 0,
      transition: 'opacity .15s, background .15s'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: selectedAsset?.id === asset.id ? 'check' : 'expand',
    size: 11
  })), featured && /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: 6,
      left: 6,
      fontSize: 9,
      fontWeight: 700,
      letterSpacing: '0.04em',
      color: T.navy,
      background: T.primary,
      padding: '2px 6px',
      borderRadius: 4
    }
  }, "\u2605 TOP ", featured), selectedAsset?.id === asset.id && /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      left: 8,
      right: 8,
      bottom: 8,
      padding: '7px 9px',
      borderRadius: 8,
      background: 'rgba(255,255,255,.78)',
      color: T.navy,
      fontSize: 10.5,
      fontWeight: 700,
      backdropFilter: 'blur(8px)'
    }
  }, "\u5DF2\u7528\u4E8E\u53F3\u4FA7\u9884\u89C8"));
  const assets = [{
    id: 'asset-1',
    label: '幕布光影',
    shape: 'ribbon',
    rotate: -4,
    palette: ['#1a3a5c', '#2c5a3c', '#f5b8c8', '#e896b0', '#fdf5f5']
  }, {
    id: 'asset-2',
    label: '夜色花影',
    shape: 'petal',
    rotate: 3,
    palette: ['#2a1a2e', '#3c5a4c', '#fab1c4', '#f78bb0', T.peachTint]
  }, {
    id: 'asset-3',
    label: '奶油清晨',
    shape: 'bloom',
    rotate: -2,
    palette: ['#fdf0ee', '#9bbfa8', '#e8a0bc', '#d987a8', '#fff']
  }, {
    id: 'asset-4',
    label: '紫调反差',
    shape: 'ribbon',
    rotate: 4,
    palette: ['#3a2c4a', '#5c7a5c', '#f0a8c4', '#dc8aa8', '#fff']
  }, {
    id: 'asset-5',
    label: '海盐深蓝',
    shape: 'petal',
    rotate: -3,
    palette: ['#0e2a3a', '#3c4a3c', '#ffb8c8', '#ff8aa8', '#fff']
  }, {
    id: 'asset-6',
    label: '莓果晚风',
    shape: 'bloom',
    rotate: 4,
    palette: ['#2c1a3a', '#5c3c5c', '#f8a8c0', '#e890b0', '#fff']
  }, {
    id: 'asset-7',
    label: '雾粉白昼',
    shape: 'ribbon',
    rotate: -2,
    palette: ['#fce5ec', '#a8c8a8', '#dc8aa8', '#b86890', '#fff']
  }, {
    id: 'asset-8',
    label: '森林幕墙',
    shape: 'petal',
    rotate: 3,
    palette: ['#1a2a3a', '#5c7a4c', '#f0c0d0', '#e090b0', '#fff']
  }, {
    id: 'asset-9',
    label: '酒红场景',
    shape: 'bloom',
    rotate: -4,
    palette: ['#3a1a2a', '#4c5a4c', '#ffa0c0', '#d088a8', '#fff']
  }, {
    id: 'asset-10',
    label: '柔粉留白',
    shape: 'ribbon',
    rotate: 2,
    palette: ['#fdf5f5', '#88aa88', '#e890a8', '#b87090', '#fff']
  }, {
    id: 'asset-11',
    label: '雾蓝暗涌',
    shape: 'petal',
    rotate: -3,
    palette: ['#22334a', '#4a6a4a', '#fcb4cc', '#e088a8', '#fff']
  }, {
    id: 'asset-12',
    label: '暮色花房',
    shape: 'bloom',
    rotate: 3,
    palette: ['#2a2a3c', '#5a7a5a', '#f8a0c0', '#cc7898', '#fff']
  }];
  React.useEffect(() => {
    if (!selectedAsset && phase >= 2 && onSelectAsset) onSelectAsset(assets[0]);
  }, [phase, selectedAsset, onSelectAsset]);
  React.useEffect(() => {
    const timers = [setTimeout(() => setPhase(1), 1100), setTimeout(() => setPhase(2), 2800), setTimeout(() => setPhase(3), 4500)];
    return () => timers.forEach(clearTimeout);
  }, []);
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 14
    }
  }, "\u7B56\u7565\u5B9A\u4E86\uFF0C\u6211\u5F00\u59CB\u4E3A\u4F60\u8C03\u7814\u7D20\u6750\u3002\u5148\u6252\u4E86\u4E00\u5708\u5B66\u672F\u8BBA\u6587 + \u79D1\u666E\u6587\u7AE0 + \u89C6\u9891 \u2014\u2014"), phase === 0 && /*#__PURE__*/React.createElement(TypingDots, null), phase >= 1 && /*#__PURE__*/React.createElement("div", {
    style: {
      background: T.white,
      border: `1px solid ${T.hairline}`,
      borderRadius: 14,
      padding: 6,
      overflow: 'hidden',
      animation: 'fadeIn .28s ease'
    }
  }, sources.map((s, i) => /*#__PURE__*/React.createElement(SourceRow, {
    key: i,
    source: s,
    idx: i
  }))), phase >= 1 && /*#__PURE__*/React.createElement("button", {
    style: {
      marginTop: 8,
      fontSize: 12,
      color: T.navyMid,
      background: 'transparent',
      border: 'none',
      cursor: 'pointer',
      fontWeight: 500,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 4,
      padding: '4px 0'
    }
  }, "\u67E5\u770B\u5176\u4F59 5 \u4E2A\u6765\u6E90 ", /*#__PURE__*/React.createElement(Icon, {
    name: "chevronDown",
    size: 11
  }))), phase >= 2 && /*#__PURE__*/React.createElement(NoriSays, {
    style: {
      marginTop: 22
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 12
    }
  }, "\u518D\u6252\u4E86\u4E00\u4E9B\u7C89\u8272\u690D\u7269\u7684\u56FE\u7247\u7D20\u6750 \u2014\u2014 \u9AD8\u4EAE\u7684\u8FD9 4 \u5F20\u662F\u6211\u89C9\u5F97\u5C01\u9762 / \u4E3B\u56FE\u6700\u80FD\u7528\u7684\uFF1A"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(4, 1fr)',
      gap: 8,
      animation: 'fadeIn .28s ease'
    }
  }, assets.slice(0, 4).map((asset, i) => /*#__PURE__*/React.createElement(Img, {
    key: asset.id,
    asset: asset,
    featured: i + 1
  }))), imgsExpanded && /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'grid',
      gridTemplateColumns: 'repeat(4, 1fr)',
      gap: 8,
      marginTop: 8,
      animation: 'fadeIn .3s ease'
    }
  }, assets.slice(4).map(asset => /*#__PURE__*/React.createElement(Img, {
    key: asset.id,
    asset: asset
  }))), /*#__PURE__*/React.createElement("button", {
    onClick: () => setImgsExpanded(v => !v),
    style: {
      marginTop: 12,
      fontSize: 12,
      color: T.navyMid,
      background: 'transparent',
      border: 'none',
      cursor: 'pointer',
      fontWeight: 500,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 4,
      padding: '4px 0'
    }
  }, imgsExpanded ? '收起' : `查看其余 ${assets.length - 4} 张图片`, /*#__PURE__*/React.createElement(Icon, {
    name: imgsExpanded ? 'chevronDown' : 'chevronRight',
    size: 11
  })), phase >= 3 && /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 14,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      padding: '6px 12px',
      borderRadius: 99,
      background: T.successTint,
      color: T.success,
      fontSize: 12,
      fontWeight: 600,
      animation: 'fadeIn .26s ease'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "check",
    size: 12
  }), " \u7D20\u6750\u641C\u96C6\u5B8C\u6210 \xB7 9 \u7BC7\u8D44\u6599 + 12 \u5F20\u56FE")));
};

/* ── Step 4: 内容生成 TODO 列表 ── */

const Step4Generate = ({
  onAllDone,
  onRevealCanvas
}) => {
  const tasks = [{
    id: 't1',
    label: '生成标题与正文中',
    sub: '反差钩子 + 6 种植物 + 养护 Tips'
  }, {
    id: 't2',
    label: '生成图片卡片中',
    sub: '8 张图 · 封面 + 内页 + 互动页'
  }, {
    id: 't3',
    label: '排版优化中',
    sub: '小红书图文格式 · emoji 与排版'
  }, {
    id: 't4',
    label: '一致性校对中',
    sub: '术语 · 风格 · 标点统一'
  }];
  const [done, setDone] = React.useState({});
  const [current, setCurrent] = React.useState(0);
  const [allDone, setAllDone] = React.useState(false);
  React.useEffect(() => {
    if (current >= tasks.length) {
      setAllDone(true);
      const t = setTimeout(() => onAllDone && onAllDone(), 700);
      return () => clearTimeout(t);
    }
    const t = setTimeout(() => {
      setDone(d => ({
        ...d,
        [tasks[current].id]: true
      }));
      setCurrent(c => c + 1);
    }, 1400);
    return () => clearTimeout(t);
  }, [current]);
  return /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 14
    }
  }, "\u6240\u6709\u51C6\u5907\u5C31\u7EEA\uFF0C\u5F00\u59CB\u751F\u6210\u5185\u5BB9\u4E86 \u2014\u2014 \u4F60\u53EF\u4EE5\u5728\u53F3\u8FB9 Canvas \u5B9E\u65F6\u9884\u89C8\uFF1A"), /*#__PURE__*/React.createElement("div", {
    style: {
      background: T.white,
      border: `1px solid ${T.hairline}`,
      borderRadius: 14,
      padding: '12px 16px',
      overflow: 'hidden'
    }
  }, tasks.map((t, i) => {
    const isDone = done[t.id];
    const isActive = current === i && !isDone;
    return /*#__PURE__*/React.createElement("div", {
      key: t.id,
      style: {
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        padding: '10px 0',
        borderBottom: i < tasks.length - 1 ? `1px solid ${T.hairlineSoft}` : 'none'
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        width: 22,
        height: 22,
        borderRadius: 6,
        border: `1.5px solid ${isDone ? T.success : T.navySoft}`,
        background: isDone ? T.success : T.white,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexShrink: 0,
        position: 'relative',
        animation: isDone ? 'checkPop .35s ease' : 'none'
      }
    }, isDone && /*#__PURE__*/React.createElement(Icon, {
      name: "check",
      size: 12,
      color: T.white,
      stroke: 2.5
    }), isActive && /*#__PURE__*/React.createElement("div", {
      style: {
        position: 'absolute',
        inset: -3,
        border: `2px solid ${T.iris}`,
        borderTopColor: 'transparent',
        borderRadius: 8,
        animation: 'spin 0.9s linear infinite'
      }
    })), /*#__PURE__*/React.createElement("div", {
      style: {
        flex: 1
      }
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 13,
        fontWeight: 600,
        color: isDone ? T.navyLight : T.navy,
        textDecoration: isDone ? 'line-through' : 'none'
      }
    }, t.label), /*#__PURE__*/React.createElement("div", {
      style: {
        fontSize: 11,
        color: T.navyLight,
        marginTop: 1
      }
    }, t.sub)), isActive && /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 11,
        color: T.iris,
        fontWeight: 600,
        animation: 'pulse 1.4s infinite'
      }
    }, "\u8FDB\u884C\u4E2D\u2026"), isDone && /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 11,
        color: T.success,
        fontWeight: 600
      }
    }, "\u5B8C\u6210"));
  })), allDone && /*#__PURE__*/React.createElement("button", {
    onClick: () => onRevealCanvas && onRevealCanvas(),
    style: {
      marginTop: 14,
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      padding: '12px 16px',
      borderRadius: 12,
      background: `linear-gradient(90deg, ${T.primary} 0%, #edff7a 42%, ${T.successTint} 72%, #f8ffcc 100%)`,
      backgroundSize: '220% 100%',
      color: T.navy,
      fontWeight: 600,
      fontSize: 13.5,
      animation: 'doneButtonReveal 1.35s cubic-bezier(.2,.8,.2,1) both, doneButtonGlow 1.4s ease-in-out .12s 2',
      position: 'relative',
      overflow: 'hidden',
      width: '100%',
      border: 'none',
      cursor: 'pointer',
      justifyContent: 'space-between',
      textAlign: 'left',
      boxShadow: '0 12px 30px rgba(214,255,0,.22)',
      transition: 'transform .18s cubic-bezier(.2,.8,.2,1), box-shadow .18s cubic-bezier(.2,.8,.2,1)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      inset: 0,
      background: 'linear-gradient(110deg, transparent 0%, rgba(255,255,255,.72) 48%, transparent 62%)',
      transform: 'translateX(-120%)',
      animation: 'doneButtonSweep 1.1s cubic-bezier(.2,.8,.2,1) .16s both',
      pointerEvents: 'none'
    }
  }), /*#__PURE__*/React.createElement("span", null, "\u5168\u90E8\u5B8C\u6210\uFF01\u5185\u5BB9\u5DF2\u5C31\u7EEA\uFF0C\u53BB Canvas \u770B\u770B\u5427"), /*#__PURE__*/React.createElement("span", {
    style: {
      width: 30,
      height: 30,
      borderRadius: '50%',
      background: 'rgba(14,14,44,.08)',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "chevronRight",
    size: 14,
    color: T.navy
  }))));
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
/* ─── Canvas: editable preview + toolbar ─── */

const PhoneFrame = ({
  children
}) => /*#__PURE__*/React.createElement("div", {
  style: {
    position: 'relative',
    width: 'min(356px, 100%)',
    height: 704,
    margin: '0 auto',
    filter: 'drop-shadow(0 30px 58px rgba(14,14,44,.18))'
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    position: 'absolute',
    inset: 0,
    borderRadius: 55,
    background: 'linear-gradient(145deg, #fbfbfc, #d9dce2)',
    boxShadow: 'inset 0 0 0 1px rgba(14,14,44,.12), inset 0 0 0 3px rgba(255,255,255,.72)'
  }
}), /*#__PURE__*/React.createElement("span", {
  style: {
    position: 'absolute',
    left: -5,
    top: 164,
    width: 4,
    height: 46,
    borderRadius: '4px 0 0 4px',
    background: 'linear-gradient(180deg, #d5d8df, #f8f8fa)',
    boxShadow: '0 98px 0 #e4e6eb, 0 157px 0 #e4e6eb'
  }
}), /*#__PURE__*/React.createElement("span", {
  style: {
    position: 'absolute',
    right: -46,
    top: 315,
    width: 44,
    height: 44,
    borderRadius: '50%',
    background: 'linear-gradient(145deg, #f5f6f8, #dfe2e7)',
    border: '1px solid rgba(14,14,44,.08)',
    boxShadow: '0 9px 18px rgba(14,14,44,.10), inset 0 1px 0 rgba(255,255,255,.8)'
  }
}), /*#__PURE__*/React.createElement("div", {
  style: {
    position: 'absolute',
    inset: 8,
    borderRadius: 49,
    background: '#050507',
    boxShadow: 'inset 0 0 0 1px rgba(255,255,255,.10)'
  }
}), /*#__PURE__*/React.createElement("div", {
  style: {
    position: 'absolute',
    left: '50%',
    top: 18,
    width: 122,
    height: 34,
    transform: 'translateX(-50%)',
    borderRadius: '0 0 19px 19px',
    background: '#050507',
    zIndex: 5
  }
}), /*#__PURE__*/React.createElement("div", {
  style: {
    position: 'absolute',
    left: 17,
    right: 17,
    top: 17,
    bottom: 17,
    borderRadius: 39,
    overflow: 'hidden',
    background: '#fff'
  }
}, children));
const CanvasDocumentEditor = ({
  data,
  onSetData
}) => /*#__PURE__*/React.createElement("div", {
  style: {
    width: 'min(760px, 100%)',
    minHeight: 'calc(100vh - 190px)',
    background: T.white,
    border: `1px solid ${T.hairline}`,
    borderRadius: 18,
    boxShadow: '0 22px 60px rgba(14,14,44,.08)',
    padding: '42px 54px 56px',
    color: T.navy
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    marginBottom: 34
  }
}, /*#__PURE__*/React.createElement("span", {
  style: {
    width: 34,
    height: 34,
    borderRadius: 12,
    background: T.irisTint,
    color: T.iris,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center'
  }
}, /*#__PURE__*/React.createElement(Icon, {
  name: "edit",
  size: 16
})), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
  style: {
    fontSize: 13,
    fontWeight: 700,
    color: T.navy
  }
}, "\u6587\u6848\u7F16\u8F91"), /*#__PURE__*/React.createElement("div", {
  style: {
    fontSize: 11.5,
    color: T.navyLight
  }
}, "\u50CF\u6587\u6863\u4E00\u6837\u4FEE\u6539\u6807\u9898\u3001\u6B63\u6587\u548C\u7ED3\u6784"))), /*#__PURE__*/React.createElement(EditableText, {
  tag: "h1",
  onChange: v => onSetData({
    ...data,
    title: v
  }),
  style: {
    fontSize: 34,
    lineHeight: 1.18,
    fontWeight: 750,
    letterSpacing: 0,
    margin: '0 0 18px',
    color: T.navy
  }
}, data.title), /*#__PURE__*/React.createElement("div", {
  style: {
    display: 'flex',
    gap: 8,
    flexWrap: 'wrap',
    marginBottom: 28
  }
}, data.tags.map((tag, i) => /*#__PURE__*/React.createElement("span", {
  key: i,
  style: {
    padding: '5px 10px',
    borderRadius: 999,
    background: T.surface,
    color: T.navyMid,
    fontSize: 12,
    fontWeight: 600
  }
}, "#", tag))), /*#__PURE__*/React.createElement(EditableText, {
  tag: "h2",
  onChange: v => onSetData({
    ...data,
    hook: v
  }),
  style: {
    fontSize: 20,
    lineHeight: 1.45,
    fontWeight: 700,
    margin: '0 0 16px',
    color: T.navy
  }
}, data.hook), /*#__PURE__*/React.createElement(EditableText, {
  tag: "p",
  onChange: v => onSetData({
    ...data,
    intro: v
  }),
  style: {
    fontSize: 15.5,
    lineHeight: 1.9,
    margin: '0 0 28px',
    color: T.navyMid
  }
}, data.intro), /*#__PURE__*/React.createElement("div", {
  style: {
    display: 'grid',
    gap: 20
  }
}, data.items.map((it, i) => /*#__PURE__*/React.createElement("div", {
  key: i,
  style: {
    display: 'grid',
    gridTemplateColumns: '44px minmax(0, 1fr)',
    gap: 14
  }
}, /*#__PURE__*/React.createElement("span", {
  style: {
    width: 34,
    height: 34,
    borderRadius: 12,
    background: T.primaryTint,
    color: T.navy,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 12,
    fontFamily: T.fontMono,
    fontWeight: 700
  }
}, String(i + 1).padStart(2, '0')), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement(EditableText, {
  tag: "h3",
  onChange: v => {
    const items = [...data.items];
    items[i] = {
      ...it,
      name: v
    };
    onSetData({
      ...data,
      items
    });
  },
  style: {
    fontSize: 16.5,
    fontWeight: 700,
    lineHeight: 1.5,
    margin: '0 0 4px',
    color: T.navy
  }
}, it.name), /*#__PURE__*/React.createElement(EditableText, {
  tag: "p",
  onChange: v => {
    const items = [...data.items];
    items[i] = {
      ...it,
      desc: v
    };
    onSetData({
      ...data,
      items
    });
  },
  style: {
    fontSize: 14.5,
    lineHeight: 1.85,
    color: T.navyMid,
    margin: 0
  }
}, it.desc))))), /*#__PURE__*/React.createElement("div", {
  style: {
    marginTop: 32,
    padding: '16px 18px',
    borderRadius: 14,
    background: T.peachTint,
    border: `1px solid ${T.hairlineSoft}`
  }
}, /*#__PURE__*/React.createElement(EditableText, {
  tag: "div",
  onChange: v => onSetData({
    ...data,
    cta: v
  }),
  style: {
    fontSize: 15,
    fontWeight: 650,
    lineHeight: 1.75,
    color: T.navy
  }
}, data.cta)));
const CanvasToolbar = ({
  onClose,
  onTransform,
  onPublish,
  mode,
  setMode,
  expanded,
  setExpanded,
  collapsed,
  onToggleCollapse
}) => {
  const Btn = ({
    icon,
    label,
    onClick,
    primary,
    accent,
    active,
    children
  }) => {
    const [hov, setHov] = React.useState(false);
    const bg = primary ? 'linear-gradient(135deg, #5c62ef, #6c6ff2)' : active ? accent === 'green' ? 'rgba(49,208,170,.18)' : 'rgba(75,77,237,.12)' : accent === 'green' ? hov ? 'rgba(49,208,170,.18)' : 'rgba(49,208,170,.10)' : accent === 'purple' ? hov ? 'rgba(75,77,237,.14)' : 'rgba(75,77,237,.08)' : hov ? 'rgba(14,14,44,.09)' : 'rgba(14,14,44,.045)';
    return /*#__PURE__*/React.createElement("button", {
      onClick: onClick,
      onMouseEnter: () => setHov(true),
      onMouseLeave: () => setHov(false),
      style: {
        height: label ? 42 : 40,
        minWidth: label ? 92 : 40,
        padding: label ? '0 15px' : 0,
        borderRadius: label ? 15 : 14,
        border: primary ? 'none' : `1px solid ${active ? 'rgba(49,208,170,.16)' : 'rgba(14,14,44,.075)'}`,
        cursor: 'pointer',
        background: bg,
        color: primary ? T.white : T.navy,
        fontSize: 13,
        fontWeight: 700,
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        justifyContent: 'center',
        transition: 'transform .16s cubic-bezier(.2,.8,.2,1), box-shadow .16s cubic-bezier(.2,.8,.2,1), background .16s cubic-bezier(.2,.8,.2,1)',
        boxShadow: primary ? '0 12px 24px rgba(75,77,237,.22)' : '0 6px 14px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.72)'
      }
    }, icon && /*#__PURE__*/React.createElement(Icon, {
      name: icon,
      size: label ? 16 : 15
    }), label, children);
  };
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '7px 8px',
      background: 'rgba(251,252,255,.88)',
      borderRadius: 19,
      boxShadow: '0 14px 34px rgba(14,14,44,.09), inset 0 1px 0 rgba(255,255,255,.86)',
      gap: 7,
      backdropFilter: 'blur(18px)',
      border: '1px solid rgba(255,255,255,.76)'
    }
  }, /*#__PURE__*/React.createElement(Btn, {
    icon: "transform",
    accent: "purple",
    onClick: e => onTransform && onTransform(e.currentTarget.getBoundingClientRect())
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      width: 1,
      height: 22,
      background: 'rgba(14,14,44,.08)',
      margin: '0 1px'
    }
  }), /*#__PURE__*/React.createElement(Btn, {
    icon: "phone",
    accent: "green",
    active: mode === 'preview',
    onClick: () => setMode('preview')
  }), /*#__PURE__*/React.createElement(Btn, {
    icon: "edit",
    accent: "purple",
    active: mode === 'edit',
    onClick: () => setMode('edit')
  }), /*#__PURE__*/React.createElement(Btn, {
    icon: "send",
    label: "\u53D1\u5E03",
    primary: true,
    onClick: onPublish
  }), /*#__PURE__*/React.createElement(Btn, {
    icon: "download",
    onClick: () => {}
  }), /*#__PURE__*/React.createElement(Btn, {
    icon: expanded ? 'collapse' : 'expand',
    accent: "purple",
    onClick: () => setExpanded(v => !v)
  }), /*#__PURE__*/React.createElement(Btn, {
    icon: collapsed ? 'chevronLeft' : 'chevronRight',
    onClick: onToggleCollapse
  }), /*#__PURE__*/React.createElement(Btn, {
    icon: "close",
    onClick: onClose
  }));
};

/* Floating text-edit menu — appears when text is selected */
const TextSelectionMenu = ({
  pos,
  onAction,
  onClose
}) => {
  if (!pos) return null;
  const actions = [{
    id: 'rewrite',
    label: '改写',
    icon: 'edit'
  }, {
    id: 'expand',
    label: '扩展',
    icon: 'plus'
  }, {
    id: 'simplify',
    label: '简化',
    icon: 'minus'
  }, {
    id: 'tone',
    label: '调整语气',
    icon: 'sliders'
  }];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: pos.y,
      left: pos.x,
      transform: 'translate(-50%, -100%)',
      background: T.navy,
      color: T.white,
      borderRadius: 10,
      padding: 4,
      display: 'flex',
      gap: 2,
      boxShadow: T.shadowLg,
      zIndex: 50,
      animation: 'fadeIn .15s ease'
    }
  }, actions.map(a => /*#__PURE__*/React.createElement("button", {
    key: a.id,
    onClick: () => onAction(a.id),
    style: {
      padding: '6px 10px',
      borderRadius: 6,
      background: 'transparent',
      color: T.white,
      border: 'none',
      cursor: 'pointer',
      fontSize: 12,
      fontWeight: 500,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 5
    },
    onMouseEnter: e => e.currentTarget.style.background = 'rgba(255,255,255,.12)',
    onMouseLeave: e => e.currentTarget.style.background = 'transparent'
  }, /*#__PURE__*/React.createElement(Icon, {
    name: a.icon,
    size: 12
  }), " ", a.label)));
};

/* Editable text */
const EditableText = ({
  tag = 'p',
  children,
  onChange,
  style
}) => {
  const ref = React.useRef(null);
  return React.createElement(tag, {
    ref,
    contentEditable: true,
    suppressContentEditableWarning: true,
    onBlur: e => onChange && onChange(e.currentTarget.innerText),
    style: {
      outline: 'none',
      cursor: 'text',
      ...style
    },
    spellCheck: false
  }, children);
};

/* The mock generated post — small-red-book style */
const PostPreview = ({
  data,
  onSetData,
  onSelectText,
  selectedAsset
}) => {
  const handleMouseUp = e => {
    const sel = window.getSelection();
    if (!sel || sel.isCollapsed || !sel.toString().trim()) {
      onSelectText(null);
      return;
    }
    const range = sel.getRangeAt(0);
    const r = range.getBoundingClientRect();
    const container = e.currentTarget.getBoundingClientRect();
    onSelectText({
      x: r.left - container.left + r.width / 2,
      y: r.top - container.top - 6
    });
  };
  const coverPalette = selectedAsset?.palette || ['#1a3a5c', '#2c5a3c', '#f5b8c8', '#e896b0', '#fdf5f5'];
  const coverShape = selectedAsset?.shape || 'petal';
  const coverRotate = selectedAsset?.rotate || 0;
  const coverLabel = selectedAsset?.label || '精选素材';
  const clipPaths = {
    petal: 'polygon(12% 16%, 34% 9%, 46% 0%, 60% 12%, 81% 8%, 100% 22%, 93% 44%, 100% 71%, 82% 88%, 61% 84%, 44% 100%, 22% 92%, 0% 74%, 7% 48%, 0% 24%)',
    ribbon: 'polygon(6% 7%, 44% 0%, 64% 9%, 100% 4%, 90% 38%, 100% 65%, 83% 100%, 46% 92%, 26% 100%, 0% 81%, 9% 48%, 0% 17%)',
    bloom: 'polygon(11% 0%, 38% 8%, 58% 0%, 74% 15%, 100% 17%, 94% 50%, 100% 80%, 76% 100%, 49% 93%, 30% 100%, 0% 82%, 8% 51%, 0% 18%)'
  };
  return /*#__PURE__*/React.createElement("div", {
    onMouseUp: handleMouseUp,
    style: {
      width: '100%',
      height: '100%',
      background: T.white,
      overflowY: 'auto',
      overflowX: 'hidden',
      position: 'relative',
      WebkitOverflowScrolling: 'touch'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'sticky',
      top: 0,
      zIndex: 4,
      height: 30,
      padding: '0 18px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      fontSize: 12,
      fontWeight: 700,
      color: '#111',
      background: 'rgba(255,255,255,.94)',
      backdropFilter: 'blur(10px)'
    }
  }, /*#__PURE__*/React.createElement("span", null, "9:41"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 6,
      color: 'rgba(14,14,44,.72)'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 14,
      height: 9,
      borderRadius: 3,
      border: '1.8px solid currentColor',
      position: 'relative',
      display: 'inline-block'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      position: 'absolute',
      inset: 1.5,
      borderRadius: 1.5,
      background: 'currentColor'
    }
  })), /*#__PURE__*/React.createElement("span", {
    style: {
      width: 14,
      height: 10,
      display: 'inline-flex',
      alignItems: 'flex-end',
      gap: 1
    }
  }, [4, 6, 8, 10].map((h, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    style: {
      width: 2,
      height: h,
      borderRadius: 2,
      background: 'currentColor',
      display: 'inline-block'
    }
  }))))), /*#__PURE__*/React.createElement("div", {
    style: {
      aspectRatio: '3 / 4',
      background: '#1a3a5c',
      position: 'relative',
      overflow: 'hidden'
    }
  }, data.coverImage && /*#__PURE__*/React.createElement("img", {
    src: data.coverImage,
    alt: data.coverTitle || data.title,
    style: {
      position: 'absolute',
      inset: 0,
      width: '100%',
      height: '100%',
      objectFit: 'cover',
      zIndex: 5
    }
  }), /*#__PURE__*/React.createElement(FlowerVisual, {
    palette: coverPalette
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      right: 18,
      top: 18,
      width: 110,
      transform: `rotate(${coverRotate}deg)`
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      aspectRatio: '0.82 / 1',
      clipPath: clipPaths[coverShape],
      overflow: 'hidden',
      boxShadow: '0 18px 34px rgba(14,14,44,.24)',
      border: '1px solid rgba(255,255,255,.28)'
    }
  }, /*#__PURE__*/React.createElement(FlowerVisual, {
    palette: coverPalette
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 8,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 5,
      padding: '5px 8px',
      borderRadius: 999,
      background: 'rgba(255,255,255,.16)',
      color: T.white,
      backdropFilter: 'blur(10px)',
      fontSize: 9.5,
      fontWeight: 700,
      letterSpacing: '0.05em',
      textTransform: 'uppercase'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "image",
    size: 10,
    color: "currentColor"
  }), coverLabel)), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      inset: 0,
      padding: 22,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'flex-end',
      background: 'linear-gradient(to top, rgba(0,0,0,.55), transparent 50%)'
    }
  }, /*#__PURE__*/React.createElement(EditableText, {
    tag: "div",
    onChange: v => onSetData({
      ...data,
      title: v
    }),
    style: {
      color: T.white,
      fontSize: 26,
      fontWeight: 700,
      lineHeight: 1.2,
      letterSpacing: '-0.01em',
      textShadow: '0 2px 8px rgba(0,0,0,.3)'
    }
  }, data.title), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 10,
      display: 'flex',
      alignItems: 'center',
      gap: 6
    }
  }, data.tags.map((t, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    style: {
      fontSize: 10.5,
      fontWeight: 600,
      color: T.white,
      background: 'rgba(255,255,255,.15)',
      padding: '3px 8px',
      borderRadius: 99,
      backdropFilter: 'blur(6px)',
      border: '1px solid rgba(255,255,255,.2)'
    }
  }, "#", t))))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '18px 20px 30px'
    }
  }, /*#__PURE__*/React.createElement(EditableText, {
    tag: "h3",
    onChange: v => onSetData({
      ...data,
      hook: v
    }),
    style: {
      fontSize: 16,
      fontWeight: 700,
      color: T.navy,
      marginBottom: 10,
      lineHeight: 1.4
    }
  }, data.hook), /*#__PURE__*/React.createElement(EditableText, {
    tag: "p",
    onChange: v => onSetData({
      ...data,
      intro: v
    }),
    style: {
      fontSize: 13.5,
      color: T.navyMid,
      lineHeight: 1.75,
      marginBottom: 16
    }
  }, data.intro), data.items.map((it, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      marginBottom: 14
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8,
      marginBottom: 4
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 22,
      height: 22,
      borderRadius: 6,
      background: T.primary,
      color: T.navy,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 11,
      fontWeight: 700,
      fontFamily: T.fontMono
    }
  }, "0", i + 1), /*#__PURE__*/React.createElement(EditableText, {
    tag: "span",
    onChange: v => {
      const items = [...data.items];
      items[i] = {
        ...it,
        name: v
      };
      onSetData({
        ...data,
        items
      });
    },
    style: {
      fontSize: 14,
      fontWeight: 700,
      color: T.navy
    }
  }, it.name)), /*#__PURE__*/React.createElement(EditableText, {
    tag: "p",
    onChange: v => {
      const items = [...data.items];
      items[i] = {
        ...it,
        desc: v
      };
      onSetData({
        ...data,
        items
      });
    },
    style: {
      fontSize: 12.5,
      color: T.navyMid,
      lineHeight: 1.7,
      paddingLeft: 30
    }
  }, it.desc))), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 18,
      padding: '12px 14px',
      borderRadius: 10,
      background: T.peachTint,
      color: T.navy,
      fontSize: 13,
      fontWeight: 600,
      lineHeight: 1.6
    }
  }, /*#__PURE__*/React.createElement(EditableText, {
    tag: "div",
    onChange: v => onSetData({
      ...data,
      cta: v
    })
  }, data.cta)), /*#__PURE__*/React.createElement("div", {
    style: {
      marginTop: 16,
      fontSize: 11.5,
      color: T.navyLight,
      fontFamily: T.fontMono
    }
  }, data.footer || "\u4E0A\u6D77 \xB7 8 \u5F20\u56FE \xB7 \u9884\u4F30\u9605\u8BFB 1 \u5206\u949F")));
};
const Canvas = ({
  open,
  expanded,
  setExpanded,
  onClose,
  onTransform,
  onPublish,
  mode,
  setMode,
  selectedAsset,
  width = 540,
  toolbarCollapsed,
  setToolbarCollapsed
}) => {
  const [data, setData] = React.useState(() => window.NORI_GENERATED_DEMO?.post || ({
    title: '深蓝幕布下的粉蝶兰\n谁懂这种反差感？',
    tags: ['粉色植物', '猛男养花', '室内绿植'],
    hook: '硬汉的家里，最浪漫的 6 盆粉色植物 🌸',
    intro: '别再以为粉色只属于女孩房间。健身房 + 一盆粉蝶兰 = 顶级反差感。我家这 6 盆，每一盆都被来串门的兄弟问爆。',
    items: [{
      name: '粉蝶兰 Phalaenopsis',
      desc: '花期长达 3 个月，对光线宽容，办公桌 / 茶几都能放。深色背景下的拍照效果尤其惊艳。'
    }, {
      name: '姬秋丽 Graptopetalum',
      desc: '多肉里的颜值天花板。叶片粉嫩，全日照下会更红，懒人也养得活。'
    }, {
      name: '花叶冷水花 Pilea',
      desc: '叶脉粉条纹，散光环境长得最好。喜欢湿度，浴室窗台一绝。'
    }, {
      name: '粉掌 Anthurium',
      desc: '佛焰苞像 wax 质感，热带植物里的颜值担当。每周一次浸盆即可。'
    }],
    cta: '👇 你家有几盆？硬汉能 hold 住几种？评论区比个高低～'
  }));
  const [textMenu, setTextMenu] = React.useState(null);
  const handleTextAction = act => {
    setTextMenu(null);
    window.getSelection().removeAllRanges();
    // Hook into chat: dispatched action would land in chat as a follow-up
    if (window.__noriOnTextAction) window.__noriOnTextAction(act);
  };
  if (!open) return null;
  return /*#__PURE__*/React.createElement("aside", {
    style: {
      width: expanded ? '100%' : width,
      flexShrink: 0,
      height: '100%',
      background: 'linear-gradient(180deg, #f8fafc 0%, #f2f5fa 100%)',
      borderLeft: `1px solid ${T.hairline}`,
      display: 'flex',
      flexDirection: 'column',
      animation: 'slideInRight .35s ease',
      position: expanded ? 'absolute' : 'relative',
      right: 0,
      top: 0,
      zIndex: 20
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      overflow: 'auto',
      padding: '84px 42px 34px',
      position: 'relative',
      background: mode === 'preview' ? '#f6f6f7' : 'linear-gradient(180deg, #f7f9fc 0%, #eff3f8 100%)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: mode === 'preview' ? 560 : 860,
      margin: '0 auto',
      minHeight: '100%',
      display: 'flex',
      alignItems: mode === 'preview' ? 'center' : 'flex-start',
      justifyContent: 'center'
    }
  }, mode === 'preview' ? /*#__PURE__*/React.createElement(PhoneFrame, null, /*#__PURE__*/React.createElement(PostPreview, {
    data: data,
    onSetData: setData,
    onSelectText: setTextMenu,
    selectedAsset: selectedAsset
  })) : /*#__PURE__*/React.createElement(CanvasDocumentEditor, {
    data: data,
    onSetData: setData
  })), /*#__PURE__*/React.createElement(TextSelectionMenu, {
    pos: textMenu,
    onAction: handleTextAction,
    onClose: () => setTextMenu(null)
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: 18,
      left: '50%',
      transform: 'translateX(-50%)',
      zIndex: 30,
      width: 'auto'
    }
  }, toolbarCollapsed ? /*#__PURE__*/React.createElement("button", {
    onClick: () => setToolbarCollapsed(false),
    style: {
      width: 44,
      height: 88,
      borderRadius: 18,
      border: '1px solid rgba(14,14,44,.06)',
      background: 'rgba(251,252,255,.94)',
      color: T.navy,
      cursor: 'pointer',
      boxShadow: '0 18px 38px rgba(14,14,44,.12)'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "chevronLeft",
    size: 16,
    color: T.navy
  })) : /*#__PURE__*/React.createElement(CanvasToolbar, {
    onClose: onClose,
    onTransform: onTransform,
    onPublish: onPublish,
    mode: mode,
    setMode: setMode,
    expanded: expanded,
    setExpanded: setExpanded,
    collapsed: toolbarCollapsed,
    onToggleCollapse: () => setToolbarCollapsed(true)
  })));
};
window.Canvas = Canvas;
window.PostPreview = PostPreview;
/* ─── Generation Page: orchestrates 4 chat steps + Canvas ─── */

const StepperRail = ({
  stage
}) => {
  const steps = [{
    id: 1,
    label: '关键信息'
  }, {
    id: 2,
    label: '爆款拆解'
  }, {
    id: 3,
    label: '素材调研'
  }, {
    id: 4,
    label: '内容生成'
  }];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 6,
      padding: '8px 14px',
      borderRadius: 99,
      background: T.white,
      border: `1px solid ${T.hairline}`,
      boxShadow: T.shadowXs
    }
  }, steps.map((s, i) => {
    const done = stage > s.id;
    const active = stage === s.id;
    return /*#__PURE__*/React.createElement(React.Fragment, {
      key: s.id
    }, /*#__PURE__*/React.createElement("div", {
      style: {
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        opacity: stage >= s.id ? 1 : 0.45
      }
    }, /*#__PURE__*/React.createElement("span", {
      style: {
        width: 18,
        height: 18,
        borderRadius: '50%',
        background: done ? T.success : active ? T.navy : T.surface,
        color: done ? T.white : active ? T.primary : T.navyLight,
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: 10,
        fontWeight: 700,
        fontFamily: T.fontMono
      }
    }, done ? '✓' : s.id), /*#__PURE__*/React.createElement("span", {
      style: {
        fontSize: 12,
        fontWeight: active ? 700 : 500,
        color: active ? T.navy : T.navyMid
      }
    }, s.label)), i < steps.length - 1 && /*#__PURE__*/React.createElement("span", {
      style: {
        width: 14,
        height: 1,
        background: T.hairline
      }
    }));
  }));
};
const ChatComposer = ({
  onSend,
  placeholder = '继续追问 Nori，或描述你的想法…',
  initialValue = '',
  autoFocusKey
}) => {
  const [text, setText] = React.useState(initialValue);
  const [focused, setFocused] = React.useState(false);
  const inputRef = React.useRef(null);
  React.useEffect(() => {
    if (!initialValue) return;
    setText(initialValue);
    window.setTimeout(() => inputRef.current?.focus(), 80);
  }, [initialValue, autoFocusKey]);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      background: T.white,
      borderRadius: 16,
      border: `1px solid ${focused ? 'rgba(75,77,237,.3)' : T.hairline}`,
      boxShadow: focused ? `0 0 0 4px rgba(75,77,237,.1), ${T.shadowSm}` : T.shadowXs,
      padding: '14px 16px 10px',
      transition: 'all .15s'
    }
  }, /*#__PURE__*/React.createElement("textarea", {
    ref: inputRef,
    value: text,
    onChange: e => setText(e.target.value),
    onFocus: () => setFocused(true),
    onBlur: () => setFocused(false),
    onKeyDown: e => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (text.trim()) {
          onSend(text.trim());
          setText('');
        }
      }
    },
    placeholder: placeholder,
    rows: 1,
    style: {
      width: '100%',
      border: 'none',
      outline: 'none',
      resize: 'none',
      background: 'transparent',
      fontSize: 14,
      lineHeight: 1.5,
      color: T.navy,
      fontFamily: T.fontSans,
      minHeight: 24,
      maxHeight: 120
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginTop: 4
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 4
    }
  }, /*#__PURE__*/React.createElement(ToolPill, {
    icon: "paperclip",
    label: "\u9644\u4EF6"
  }), /*#__PURE__*/React.createElement(ToolPill, {
    icon: "globe",
    label: "\u8054\u7F51",
    active: true
  })), /*#__PURE__*/React.createElement("button", {
    onClick: () => {
      if (text.trim()) {
        onSend(text.trim());
        setText('');
      }
    },
    disabled: !text.trim(),
    style: {
      width: 32,
      height: 32,
      borderRadius: '50%',
      border: 'none',
      cursor: text.trim() ? 'pointer' : 'not-allowed',
      background: text.trim() ? T.navy : T.surface,
      color: text.trim() ? T.white : T.navyLight,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      transition: 'all .15s'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "arrowUp",
    size: 15,
    stroke: 2
  }))));
};

/* Transform menu — appears when transform clicked */
const TransformMenu = ({
  open,
  onClose,
  onPick,
  anchorRect
}) => {
  if (!open || !anchorRect) return null;
  const opts = [{
    id: 'gzh',
    label: '公众号长文',
    sub: '深度长文 · 1500–3000 字',
    icon: 'document',
    tint: '#fff8e0',
    accent: '#c89b00'
  }, {
    id: 'dy',
    label: '抖音短视频',
    sub: '60s 口播脚本 + 分镜',
    icon: 'video',
    tint: '#e8e8fd',
    accent: T.iris
  }, {
    id: 'wxsph',
    label: '微信视频号',
    sub: '90s 横屏 · 适合科普',
    icon: 'play',
    tint: '#e0faf4',
    accent: T.success
  }, {
    id: 'bili',
    label: 'B 站视频',
    sub: '5 分钟以上 · 长内容',
    icon: 'bilibili',
    tint: '#ffe5ec',
    accent: '#ff4488'
  }];
  const menuWidth = 320;
  const menuHeight = 286;
  const viewportWidth = typeof window !== 'undefined' ? window.innerWidth : 1440;
  const viewportHeight = typeof window !== 'undefined' ? window.innerHeight : 900;
  const left = Math.max(16, Math.min(anchorRect.left - menuWidth - 14, viewportWidth - menuWidth - 16));
  const top = Math.max(16, Math.min(anchorRect.top - 88, viewportHeight - menuHeight - 16));
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("div", {
    onClick: onClose,
    style: {
      position: 'fixed',
      inset: 0,
      zIndex: 100
    }
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'fixed',
      top,
      left,
      background: T.white,
      borderRadius: 14,
      boxShadow: T.shadowXl,
      border: `1px solid ${T.hairline}`,
      padding: 8,
      width: 320,
      zIndex: 101,
      animation: 'fadeIn .18s ease'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '6px 10px 8px',
      fontSize: 11,
      fontWeight: 700,
      letterSpacing: '0.08em',
      textTransform: 'uppercase',
      color: T.navyLight
    }
  }, "\u8F6C\u5316\u4E3A"), opts.map(o => /*#__PURE__*/React.createElement("button", {
    key: o.id,
    onClick: () => onPick(o),
    style: {
      width: '100%',
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      padding: '10px 10px',
      borderRadius: 8,
      background: 'transparent',
      border: 'none',
      cursor: 'pointer',
      textAlign: 'left'
    },
    onMouseEnter: e => e.currentTarget.style.background = T.surface,
    onMouseLeave: e => e.currentTarget.style.background = 'transparent'
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 32,
      height: 32,
      borderRadius: 8,
      background: o.tint,
      color: o.accent,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: o.icon,
    size: 16
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: T.navy
    }
  }, o.label), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: T.navyLight
    }
  }, o.sub)), /*#__PURE__*/React.createElement(Icon, {
    name: "chevronRight",
    size: 12,
    color: T.navyLight
  })))));
};

/* Publish flow messages — after step 4 */
const PublishLinkAccount = ({
  onLinked
}) => {
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
  return /*#__PURE__*/React.createElement(NoriSays, null, !linked ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 12
    }
  }, "\u53D1\u5E03\u524D\u9700\u8981\u5148\u94FE\u63A5\u4F60\u7684\u5C0F\u7EA2\u4E66\u8D26\u53F7\u3002", /*#__PURE__*/React.createElement("span", {
    style: {
      color: T.navyLight,
      fontSize: 12.5
    }
  }, "(\u53EA\u6709\u7B2C\u4E00\u6B21\u9700\u8981\uFF0C\u4E4B\u540E\u4F1A\u81EA\u52A8\u94FE\u63A5)")), /*#__PURE__*/React.createElement("div", {
    style: {
      background: T.white,
      border: `1px solid ${T.hairline}`,
      borderRadius: 12,
      padding: '14px 16px',
      display: 'flex',
      alignItems: 'center',
      gap: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 36,
      height: 36,
      borderRadius: 10,
      background: '#ffe5ec',
      color: '#ff4488',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontWeight: 800,
      fontSize: 16
    }
  }, "\u7EA2"), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: T.navy
    }
  }, "\u5C0F\u7EA2\u4E66"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11.5,
      color: T.navyLight
    }
  }, linking ? '正在跳转授权…' : '未链接')), /*#__PURE__*/React.createElement("button", {
    onClick: trigger,
    disabled: linking,
    style: {
      height: 34,
      padding: '0 14px',
      borderRadius: 8,
      border: 'none',
      cursor: linking ? 'wait' : 'pointer',
      background: T.navy,
      color: T.primary,
      fontSize: 12.5,
      fontWeight: 600,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6
    }
  }, linking ? /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 12,
      height: 12,
      border: `2px solid ${T.primary}`,
      borderTopColor: 'transparent',
      borderRadius: '50%',
      animation: 'spin .9s linear infinite',
      display: 'inline-block'
    }
  }), " \u6388\u6743\u4E2D") : /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(Icon, {
    name: "link",
    size: 12
  }), " \u94FE\u63A5\u8D26\u53F7")))) : /*#__PURE__*/React.createElement("div", {
    style: {
      background: T.white,
      border: `1px solid ${T.hairline}`,
      borderRadius: 12,
      padding: '14px 16px',
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      animation: 'fadeIn .3s'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 36,
      height: 36,
      borderRadius: 10,
      background: T.successTint,
      color: T.success,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "check",
    size: 18,
    stroke: 2.4
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: T.navy
    }
  }, "\u5DF2\u94FE\u63A5 \xB7 \u5C0F\u7EA2\u4E66 @luna_writes"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11.5,
      color: T.navyLight
    }
  }, "\u4E0B\u6B21\u53EF\u4EE5\u76F4\u63A5\u53D1\u5E03"))));
};
const PublishDraftSaved = () => /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("div", {
  style: {
    background: `linear-gradient(135deg, ${T.primaryTint}, ${T.peachTint})`,
    border: `1px solid ${T.hairline}`,
    borderRadius: 14,
    padding: '16px 18px',
    display: 'flex',
    alignItems: 'center',
    gap: 14
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    width: 40,
    height: 40,
    borderRadius: 12,
    background: T.primary,
    color: T.navy,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center'
  }
}, /*#__PURE__*/React.createElement(Icon, {
  name: "check",
  size: 20,
  stroke: 2.6
})), /*#__PURE__*/React.createElement("div", {
  style: {
    flex: 1
  }
}, /*#__PURE__*/React.createElement("div", {
  style: {
    fontSize: 14,
    fontWeight: 700,
    color: T.navy
  }
}, "\u5DF2\u5B58\u5165\u4F60\u7684\u8349\u7A3F\u7BB1"), /*#__PURE__*/React.createElement("div", {
  style: {
    fontSize: 11.5,
    color: T.navyMid,
    marginTop: 2
  }
}, "\u5C0F\u7EA2\u4E66 App \xB7 \u8349\u7A3F\u7BB1 \xB7 1 \u7BC7\u5F85\u5BA1")), /*#__PURE__*/React.createElement("button", {
  style: {
    height: 36,
    padding: '0 14px',
    borderRadius: 10,
    background: T.navy,
    color: T.white,
    border: 'none',
    cursor: 'pointer',
    fontSize: 12.5,
    fontWeight: 600,
    display: 'inline-flex',
    alignItems: 'center',
    gap: 6
  }
}, "\u53BB\u786E\u8BA4 ", /*#__PURE__*/React.createElement(Icon, {
  name: "arrowRight",
  size: 12
}))));

/* Transform launched — new round of chat */
const TransformLaunched = ({
  target
}) => /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("p", null, "\u597D\uFF0C\u5F00\u59CB\u628A\u5F53\u524D\u5185\u5BB9\u8F6C\u5316\u4E3A ", /*#__PURE__*/React.createElement("b", null, target.label), "\u3002", /*#__PURE__*/React.createElement("span", {
  style: {
    color: T.navyLight,
    fontSize: 12.5
  }
}, " (", target.sub, ")")), /*#__PURE__*/React.createElement("div", {
  style: {
    marginTop: 10,
    padding: '10px 14px',
    borderRadius: 10,
    background: T.surface,
    color: T.navyMid,
    fontSize: 12.5,
    display: 'flex',
    alignItems: 'center',
    gap: 8
  }
}, /*#__PURE__*/React.createElement("span", {
  style: {
    width: 14,
    height: 14,
    borderRadius: '50%',
    border: `2px solid ${T.iris}`,
    borderTopColor: 'transparent',
    animation: 'spin 1s linear infinite'
  }
}), "\u6B63\u5728\u91CD\u7EC4\u7ED3\u6784\u4E0E\u8282\u594F \xB7 \u9002\u914D ", target.label, " \u5E73\u53F0\u7279\u6027\u2026"));

/* Main GenerationPage */
const GenerationPage = ({
  initialPrompt,
  assetDraft,
  skillDraft,
  onBackHome,
  onNewChat,
  onOpenAssets,
  onOpenSkills,
  onOpenInsights
}) => {
  /* stage 1..4 = active step; 5 = canvas open / done */
  const isAssetReview = !!assetDraft;
  const isSkillStart = !!skillDraft;
  const isFreshChat = !initialPrompt && !isAssetReview && !isSkillStart;
  const [stage, setStage] = React.useState(isFreshChat ? 0 : isAssetReview ? 5 : 1);
  const [canvasOpen, setCanvasOpen] = React.useState(isAssetReview);
  const [canvasExpanded, setCanvasExpanded] = React.useState(false);
  const [mode, setMode] = React.useState('preview');
  const [selectedAsset, setSelectedAsset] = React.useState(null);
  const [canvasWidth, setCanvasWidth] = React.useState(560);
  const [toolbarCollapsed, setToolbarCollapsed] = React.useState(false);
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [transformOpen, setTransformOpen] = React.useState(false);
  const [transformAnchor, setTransformAnchor] = React.useState(null);
  const [followUps, setFollowUps] = React.useState([]); // {kind: 'transform' | 'link' | 'draft' | 'msg', payload}
  const [keyInfo, setKeyInfo] = React.useState(null);
  const scrollRef = React.useRef(null);
  const contentRef = React.useRef(null);
  const bottomAnchorRef = React.useRef(null);
  const chatWrapRef = React.useRef(null);
  const dragState = React.useRef(null);
  const scrollJobRef = React.useRef(null);
  const scrollToLatest = React.useCallback((behavior = 'auto') => {
    if (!scrollRef.current) return;
    if (scrollJobRef.current) window.cancelAnimationFrame(scrollJobRef.current);
    scrollJobRef.current = window.requestAnimationFrame(() => {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior
      });
      bottomAnchorRef.current?.scrollIntoView({
        block: 'end',
        behavior
      });
    });
  }, []);

  /* Auto-scroll to bottom when content changes */
  React.useEffect(() => {
    scrollToLatest();
    const t1 = window.setTimeout(() => scrollToLatest(), 80);
    const t2 = window.setTimeout(() => scrollToLatest(), 260);
    return () => {
      window.clearTimeout(t1);
      window.clearTimeout(t2);
    };
  }, [stage, followUps.length, canvasOpen, selectedAsset, canvasWidth, scrollToLatest]);
  React.useEffect(() => {
    if (!scrollRef.current || !contentRef.current) return undefined;
    const observer = new MutationObserver(() => {
      scrollToLatest();
    });
    const resizeObserver = new ResizeObserver(() => {
      scrollToLatest();
    });
    observer.observe(contentRef.current, {
      childList: true,
      subtree: true,
      characterData: true
    });
    resizeObserver.observe(contentRef.current);
    return () => {
      observer.disconnect();
      resizeObserver.disconnect();
    };
  }, [scrollToLatest]);
  const startResize = e => {
    if (!canvasOpen || canvasExpanded) return;
    dragState.current = {
      startX: e.clientX,
      startWidth: canvasWidth
    };
    const onMove = ev => {
      const delta = dragState.current.startX - ev.clientX;
      const next = Math.min(980, Math.max(420, dragState.current.startWidth + delta));
      setCanvasWidth(next);
    };
    const onUp = () => {
      window.removeEventListener('mousemove', onMove);
      window.removeEventListener('mouseup', onUp);
      dragState.current = null;
    };
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
  };
  const sessions = [window.NORI_GENERATED_DEMO?.sessionTitle || '猛男喜欢的粉色植物 · 当前', '上海咖啡馆 City Walk Top 10', '租房避雷指南 v2', '产品测评 · AI 视频工具横评'];

  /* Step 1 done → step 2 starts (auto, with simulated delay) */
  const onStep1Done = info => {
    setKeyInfo(info);
    setStage(1.5);
    setTimeout(() => setStage(2), 700);
  };
  const onStep1Skip = () => {
    setStage(1.5);
    setTimeout(() => setStage(2), 500);
  };

  /* User clicks 选题结论 → opens canvas + advances to step 3 */
  const onSelectAngle = () => {
    setCanvasOpen(true);
    setStage(2.5);
    setTimeout(() => setStage(3), 1200);
  };

  /* When step 3's research finishes, advance to step 4 */
  React.useEffect(() => {
    if (stage === 3) {
      const t = setTimeout(() => setStage(3.5), 4500);
      return () => clearTimeout(t);
    }
    if (stage === 3.5) {
      const t = setTimeout(() => setStage(4), 600);
      return () => clearTimeout(t);
    }
  }, [stage]);
  const onAllDone = () => setStage(5);
  const onTransformPick = target => {
    setTransformOpen(false);
    setTransformAnchor(null);
    setFollowUps(f => [...f, {
      kind: 'transform',
      payload: target,
      id: Date.now()
    }]);
  };
  const onPublish = () => {
    setFollowUps(f => [...f, {
      kind: 'link',
      id: Date.now()
    }]);
  };
  const onLinked = () => {
    setFollowUps(f => [...f, {
      kind: 'draft',
      id: Date.now() + 1
    }]);
  };
  const startFromUserPrompt = React.useCallback(text => {
    if (!text.trim()) return;
    setFollowUps(f => [...f, {
      kind: 'msg',
      payload: text.trim(),
      id: Date.now()
    }]);
    setStage(1);
  }, []);
  const chatTopCondensed = canvasOpen;
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      height: '100%',
      width: '100%',
      background: T.surfaceWh,
      position: 'relative',
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement(Sidebar, {
    active: "home",
    onNew: onNewChat || (() => {}),
    onNavigate: id => {
      if (id === 'home') onBackHome();
      if (id === 'library' && onOpenAssets) onOpenAssets();
      if (id === 'skills' && onOpenSkills) onOpenSkills();
      if (id === 'insights' && onOpenInsights) onOpenInsights();
    },
    sessions: sessions,
    collapsed: navCollapsed,
    onToggle: () => setNavCollapsed(v => !v)
  }), /*#__PURE__*/React.createElement("main", {
    ref: chatWrapRef,
    style: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      minWidth: canvasOpen && !canvasExpanded ? 360 : 0,
      position: 'relative',
      transition: 'min-width .28s cubic-bezier(.2,.8,.2,1)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      height: chatTopCondensed ? 0 : 56,
      padding: chatTopCondensed ? '0 24px' : '0 24px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      borderBottom: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(250,252,254,.8)',
      backdropFilter: 'blur(8px)',
      flexShrink: 0,
      overflow: 'hidden',
      opacity: chatTopCondensed ? 0 : 1,
      transform: chatTopCondensed ? 'translateY(-10px)' : 'translateY(0)',
      transition: 'height .28s cubic-bezier(.2,.8,.2,1), opacity .2s ease, transform .28s cubic-bezier(.2,.8,.2,1)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 12,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("button", {
    onClick: onBackHome,
    style: iconBtnStyle()
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "home",
    size: 16,
    color: T.navyMid
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 600,
      color: T.navy,
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }
  }, window.NORI_GENERATED_DEMO?.chatTitle || "\u731B\u7537\u559C\u6B22\u7684\u7C89\u8272\u690D\u7269\u79D1\u666E\u4E0E\u517B\u62A4\u6307\u5BFC"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 10.5,
      color: T.navyLight,
      fontFamily: T.fontMono
    }
  }, "\u5C0F\u7EA2\u4E66\u56FE\u6587 \xB7 ", new Date().toLocaleDateString('zh-CN'), " \xB7 \u81EA\u52A8\u4FDD\u5B58\u4E2D"))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10
    }
  }, !chatTopCondensed && /*#__PURE__*/React.createElement(StepperRail, {
    stage: Math.min(Math.ceil(stage), 4)
  }), /*#__PURE__*/React.createElement("button", {
    style: iconBtnStyle()
  }, /*#__PURE__*/React.createElement(Icon, {
    name: "moreH",
    size: 16,
    color: T.navyMid
  })))), /*#__PURE__*/React.createElement("div", {
    ref: scrollRef,
    style: {
      flex: 1,
      overflowY: 'auto',
      padding: '24px 0 24px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    ref: contentRef,
    style: {
      maxWidth: canvasOpen ? 640 : 760,
      margin: '0 auto',
      padding: '0 24px',
      display: 'flex',
      flexDirection: 'column',
      gap: 22
    }
  }, isSkillStart && stage === 0 ? /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 2,
      fontSize: 15,
      fontWeight: 600
    }
  }, "\u5DF2\u8F7D\u5165\u300C", skillDraft.title, "\u300DSkill"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: T.navyLight,
      fontSize: 12.5
    }
  }, "\u6211\u5DF2\u7ECF\u628A Skill \u6A21\u677F\u653E\u8FDB\u8F93\u5165\u6846\u4E86\uFF0C\u4F60\u53EF\u4EE5\u8865\u5145\u4E3B\u9898\u3001\u53D7\u4F17\u6216\u8BED\u6C14\u540E\u53D1\u9001\u3002")) : isFreshChat && stage === 0 ? /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("p", {
    style: {
      marginBottom: 2,
      fontSize: 15,
      fontWeight: 600
    }
  }, "\u8BF7\u95EE\u4F60\u60F3\u505A\u4E9B\u4EC0\u4E48\uFF1F"), /*#__PURE__*/React.createElement("p", {
    style: {
      color: T.navyLight,
      fontSize: 12.5
    }
  }, "\u63CF\u8FF0\u4E00\u4E2A\u4E3B\u9898\u3001\u5E73\u53F0\u3001\u98CE\u683C\uFF0CNori \u4F1A\u7EE7\u7EED\u5E2E\u4F60\u62C6\u89E3\u548C\u751F\u6210\u3002")) : isAssetReview ? /*#__PURE__*/React.createElement(Bubble, {
    from: "user"
  }, "\u6253\u5F00\u5185\u5BB9\u8D44\u4EA7\uFF1A", assetDraft.title) : /*#__PURE__*/React.createElement(Bubble, {
    from: "user"
  }, initialPrompt || followUps.find(f => f.kind === 'msg')?.payload || '我想生成一篇有关于猛男喜欢的粉色的植物科普与养护指导'), stage >= 1 && stage < 1.5 && /*#__PURE__*/React.createElement(Step1KeyInfo, {
    onComplete: onStep1Done,
    onSkip: onStep1Skip
  }), stage >= 1.5 && /*#__PURE__*/React.createElement(Bubble, {
    from: "user"
  }, keyInfo ? '目标：植物新手 + 反差梗 / 整活 + 标准 8–10 图' : '直接开始吧～'), stage === 1.5 && /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("span", {
    style: {
      color: T.navyMid
    }
  }, "\u6B63\u5728\u5206\u6790\u7206\u6B3E\u6570\u636E "), /*#__PURE__*/React.createElement(TypingDots, null)), stage >= 2 && /*#__PURE__*/React.createElement(Step2HotPosts, {
    onSelectAngle: onSelectAngle
  }), stage === 2.5 && /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("span", {
    style: {
      color: T.navyMid
    }
  }, "\u9009\u9898\u5DF2\u786E\u8BA4\uFF0C\u5F00\u59CB\u8C03\u7814\u7D20\u6750 "), /*#__PURE__*/React.createElement(TypingDots, null)), stage >= 3 && /*#__PURE__*/React.createElement(Step3Research, {
    selectedAsset: selectedAsset,
    onSelectAsset: setSelectedAsset
  }), stage === 3.5 && /*#__PURE__*/React.createElement(NoriSays, null, /*#__PURE__*/React.createElement("span", {
    style: {
      color: T.navyMid
    }
  }, "\u7D20\u6750\u51C6\u5907\u5B8C\u6BD5\uFF0C\u5F00\u59CB\u7EC4\u88C5 "), /*#__PURE__*/React.createElement(TypingDots, null)), stage >= 4 && /*#__PURE__*/React.createElement(Step4Generate, {
    onAllDone: onAllDone
  }), followUps.map(f => {
    if (f.kind === 'transform') return /*#__PURE__*/React.createElement(TransformLaunched, {
      key: f.id,
      target: f.payload
    });
    if (f.kind === 'link') return /*#__PURE__*/React.createElement(PublishLinkAccount, {
      key: f.id,
      onLinked: onLinked
    });
    if (f.kind === 'draft') return /*#__PURE__*/React.createElement(PublishDraftSaved, {
      key: f.id
    });
    return null;
  }), /*#__PURE__*/React.createElement("div", {
    ref: bottomAnchorRef,
    style: {
      height: 1
    }
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '12px 24px 18px',
      background: 'linear-gradient(to top, rgba(250,252,254,1) 60%, rgba(250,252,254,0))',
      flexShrink: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      maxWidth: canvasOpen ? 640 : 760,
      margin: '0 auto'
    }
  }, /*#__PURE__*/React.createElement(ChatComposer, {
    placeholder: stage === 0 ? '告诉 Nori：你想做什么内容？' : '继续追问 Nori，或描述你的想法…',
    initialValue: stage === 0 && skillDraft ? skillDraft.prompt : '',
    autoFocusKey: skillDraft?.id,
    onSend: t => {
      if (stage === 0) startFromUserPrompt(t);else setFollowUps(f => [...f, {
        kind: 'msg',
        payload: t,
        id: Date.now()
      }]);
    }
  })))), canvasOpen && !canvasExpanded && /*#__PURE__*/React.createElement("div", {
    onMouseDown: startResize,
    style: {
      width: 8,
      cursor: 'col-resize',
      background: 'linear-gradient(180deg, rgba(14,14,44,.02), rgba(14,14,44,.08), rgba(14,14,44,.02))',
      position: 'relative',
      zIndex: 22
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      position: 'absolute',
      top: '50%',
      left: '50%',
      width: 4,
      height: 68,
      transform: 'translate(-50%, -50%)',
      borderRadius: 999,
      background: 'rgba(14,14,44,.18)'
    }
  })), /*#__PURE__*/React.createElement(Canvas, {
    open: canvasOpen,
    expanded: canvasExpanded,
    setExpanded: setCanvasExpanded,
    onClose: () => setCanvasOpen(false),
    onTransform: rect => {
      setTransformAnchor(rect);
      setTransformOpen(true);
    },
    onPublish: onPublish,
    mode: mode,
    setMode: setMode,
    selectedAsset: selectedAsset,
    width: canvasWidth,
    toolbarCollapsed: toolbarCollapsed,
    setToolbarCollapsed: setToolbarCollapsed
  }), /*#__PURE__*/React.createElement(TransformMenu, {
    open: transformOpen,
    anchorRect: transformAnchor,
    onClose: () => {
      setTransformOpen(false);
      setTransformAnchor(null);
    },
    onPick: onTransformPick
  }));
};
window.GenerationPage = GenerationPage;
window.ToolPill = window.ToolPill; // already global from home
/* ─── App root ─── */

const App = () => {
  const demoBoot = window.NORI_GENERATED_DEMO || {};
  const [page, setPage] = React.useState(demoBoot.autostart ? 'gen' : 'home'); // 'home' | 'assets' | 'skills' | 'insights' | 'gen'
  const [prompt, setPrompt] = React.useState(demoBoot.prompt || '');
  const [assetDraft, setAssetDraft] = React.useState(demoBoot.autostart ? demoBoot.assetDraft || null : null);
  const [skillDraft, setSkillDraft] = React.useState(null);
  const goGen = p => {
    setPrompt(p);
    setAssetDraft(null);
    setSkillDraft(null);
    setPage('gen');
  };
  if (page === 'home') return /*#__PURE__*/React.createElement(HomePage, {
    onSubmit: goGen,
    onOpenAssets: () => setPage('assets'),
    onOpenSkills: () => setPage('skills'),
    onOpenInsights: () => setPage('insights')
  });
  if (page === 'assets') {
    return /*#__PURE__*/React.createElement(AssetsPage, {
      onBackHome: () => setPage('home'),
      onOpenSkills: () => setPage('skills'),
      onOpenInsights: () => setPage('insights'),
      onNewChat: () => {
        setPrompt('');
        setAssetDraft(null);
        setSkillDraft(null);
        setPage('gen');
      },
      onOpenAsset: asset => {
        setPrompt(`继续编辑内容资产：${asset.title}`);
        setAssetDraft(asset);
        setSkillDraft(null);
        setPage('gen');
      }
    });
  }
  if (page === 'skills') {
    return /*#__PURE__*/React.createElement(SkillsPage, {
      onBackHome: () => setPage('home'),
      onOpenAssets: () => setPage('assets'),
      onOpenInsights: () => setPage('insights'),
      onNewChat: () => {
        setPrompt('');
        setAssetDraft(null);
        setSkillDraft(null);
        setPage('gen');
      },
      onUseSkill: skill => {
        setPrompt('');
        setAssetDraft(null);
        setSkillDraft(skill);
        setPage('gen');
      }
    });
  }
  if (page === 'insights') {
    return /*#__PURE__*/React.createElement(InsightsPage, {
      onBackHome: () => setPage('home'),
      onOpenAssets: () => setPage('assets'),
      onOpenSkills: () => setPage('skills'),
      onNewChat: () => {
        setPrompt('');
        setAssetDraft(null);
        setSkillDraft(null);
        setPage('gen');
      }
    });
  }
  return /*#__PURE__*/React.createElement(GenerationPage, {
    initialPrompt: prompt,
    assetDraft: assetDraft,
    skillDraft: skillDraft,
    onBackHome: () => setPage('home'),
    onOpenAssets: () => setPage('assets'),
    onOpenSkills: () => setPage('skills'),
    onOpenInsights: () => setPage('insights'),
    onNewChat: () => {
      setPrompt('');
      setAssetDraft(null);
      setSkillDraft(null);
      setPage('gen');
    }
  });
};
ReactDOM.createRoot(document.getElementById('root')).render(/*#__PURE__*/React.createElement(App, null));