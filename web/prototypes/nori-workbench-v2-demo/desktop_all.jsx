/* ─── Nori Tokens — derived from Design System ─── */
const T = {
  // Brand
  primary:    '#D6FF00', // Fuschia
  primaryHov: '#b8e000',
  primaryTint:'#f5ffe0',
  iris:       '#4B4DED',
  irisHov:    '#3537c7',
  irisTint:   '#EFEFFD',
  peach:      '#F3DBDA',
  peachTint:  '#fdf5f5',

  // Onyx scale
  navy:       '#0e0e2c',
  navyMid:    '#4a4a68',
  navyLight:  '#8c8ca1',
  navySoft:   '#c4c4d4',

  // Surfaces
  surface:    '#ECF1F4',  // Dorian
  surfaceWh:  '#fafcfe',  // Cloud
  white:      '#ffffff',
  hairline:   'rgba(14,14,44,.08)',
  hairlineSoft:'rgba(14,14,44,.05)',

  // Semantic
  success:    '#31D0AA',
  successTint:'#e0faf4',
  warn:       '#fb8c00',
  error:      '#e53935',

  // Shadows
  shadowXs:   '0 1px 2px rgba(14,14,44,.035), 0 1px 5px rgba(14,14,44,.025)',
  shadowSm:   '0 5px 14px rgba(14,14,44,.055), 0 1px 2px rgba(14,14,44,.035)',
  shadowMd:   '0 12px 28px rgba(14,14,44,.075), 0 2px 5px rgba(14,14,44,.045)',
  shadowLg:   '0 22px 54px rgba(14,14,44,.095), 0 4px 12px rgba(14,14,44,.055)',
  shadowXl:   '0 34px 80px rgba(14,14,44,.13), 0 8px 22px rgba(14,14,44,.07)',
  shadowBtn:  '0 7px 18px rgba(14,14,44,.08), 0 1px 2px rgba(14,14,44,.04), inset 0 -1px 0 rgba(14,14,44,.10)',

  // Type
  fontSans:   "'Noto Sans SC', -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'Helvetica Neue', sans-serif",
  fontSerif:  "'Fraunces', Georgia, serif",
  fontMono:   "'DM Mono', 'Monaco', monospace",

  // Motion
  spring:      'cubic-bezier(.22, 1, .36, 1)',
  ease:        'cubic-bezier(.25, .1, .25, 1)',
  softSurface: 'rgba(255,255,255,.78)',
};

window.T = T;
const NORI_LOGO_SRC = './src/nori-onion-logo.png';
window.NORI_LOGO_SRC = NORI_LOGO_SRC;
const ONION_BURST_ASSETS = [
  './src/onion-burst-collage.png',
  './src/onion-burst-star.png',
  './src/onion-burst-real.png',
  './src/onion-burst-ring.png',
  './src/onion-burst-ink.png',
];
/* ─── Icon set: outlined, 1.6 stroke, currentColor ─── */
const Icon = ({ name, size = 18, color = 'currentColor', stroke = 1.6, style }) => {
  const props = {
    width: size, height: size, viewBox: '0 0 24 24',
    fill: 'none', stroke: color, strokeWidth: stroke,
    strokeLinecap: 'round', strokeLinejoin: 'round',
    style,
  };
  const paths = {
    attach: <path d="M21 12.5l-8.5 8.5a5.5 5.5 0 0 1-7.8-7.8l9-9a3.7 3.7 0 0 1 5.2 5.2l-8.5 8.5a1.8 1.8 0 0 1-2.6-2.6L15.5 8" />,
    globe: <><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></>,
    send: <><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 20-7Z"/></>,
    arrowRight: <><path d="M5 12h14"/><path d="M13 5l7 7-7 7"/></>,
    arrowUp: <><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></>,
    arrowLeft: <><path d="M19 12H5"/><path d="M11 19l-7-7 7-7"/></>,
    chevronDown: <path d="M6 9l6 6 6-6"/>,
    chevronLeft: <path d="M15 6l-6 6 6 6"/>,
    chevronRight: <path d="M9 6l6 6-6 6"/>,
    plus: <><path d="M12 5v14"/><path d="M5 12h14"/></>,
    close: <><path d="M18 6L6 18"/><path d="M6 6l12 12"/></>,
    check: <path d="M5 12.5l5 5 9-12"/>,
    sparkle: <><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/></>,
    star: <path d="M12 3l2.8 6.2 6.7.6-5.1 4.5 1.6 6.7L12 17.5 5.9 21l1.6-6.7L2.4 9.8l6.7-.6L12 3z"/>,
    heart: <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/>,
    bookmark: <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>,
    eye: <><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></>,
    edit: <><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.1 2.1 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></>,
    image: <><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="M21 15l-5-5L5 21"/></>,
    calendar: <><rect x="3" y="4" width="18" height="18" rx="3"/><path d="M16 2v4M8 2v4M3 10h18"/></>,
    file: <><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></>,
    save: <><path d="M17 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14V7z"/><path d="M7 3v6h8"/><path d="M9 21v-6h6"/></>,
    copy: <><rect x="9" y="9" width="11" height="11" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></>,
    lock: <><rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></>,
    search: <><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></>,
    chat: <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>,
    library: <><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></>,
    home: <><path d="M3 9.5l9-7 9 7V20a2 2 0 0 1-2 2h-4v-7H9v7H5a2 2 0 0 1-2-2z"/></>,
    splitView: <><rect x="3" y="5" width="18" height="14" rx="4"/><path d="M11.5 5v14"/></>,
    grid: <><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></>,
    expand: <><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></>,
    collapse: <><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><path d="M14 10l7-7"/><path d="M3 21l7-7"/></>,
    download: <><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></>,
    upload: <><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8l-5-5-5 5"/><path d="M12 3v12"/></>,
    sync: <><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M3 21v-5h5"/></>,
    transform: <><path d="M16 3l4 4-4 4"/><path d="M20 7H4"/><path d="M8 21l-4-4 4-4"/><path d="M4 17h16"/></>,
    phone: <rect x="6" y="2" width="12" height="20" rx="2"/>,
    pen: <><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="M2 2l7.6 7.6"/><circle cx="11" cy="11" r="2"/></>,
    sliders: <><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></>,
    user: <><circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/></>,
    play: <path d="M5 3l14 9-14 9V3z"/>,
    paperPlane: <><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4 20-7Z"/></>,
    document: <><rect x="4" y="3" width="16" height="18" rx="2"/><path d="M8 8h8M8 12h8M8 16h5"/></>,
    video: <><rect x="2" y="6" width="14" height="12" rx="2"/><path d="M22 8l-6 4 6 4z"/></>,
    bilibili: <><rect x="3" y="6" width="18" height="14" rx="3"/><circle cx="9" cy="13" r=".8" fill="currentColor"/><circle cx="15" cy="13" r=".8" fill="currentColor"/><path d="M8 4l3 2M16 4l-3 2"/></>,
    minus: <path d="M5 12h14"/>,
    sparkles: <><path d="M12 3l1.8 4.2L18 9l-4.2 1.8L12 15l-1.8-4.2L6 9l4.2-1.8z"/><path d="M19 14l.9 2.1L22 17l-2.1.9L19 20l-.9-2.1L16 17l2.1-.9z"/></>,
    quote: <><path d="M3 14h6v7H3z"/><path d="M14 14h6v7h-6z"/><path d="M3 14V9a4 4 0 0 1 4-4"/><path d="M14 14V9a4 4 0 0 1 4-4"/></>,
    book: <><path d="M4 4h7a3 3 0 0 1 3 3v14a2 2 0 0 0-2-2H4z"/><path d="M20 4h-7a3 3 0 0 0-3 3v14a2 2 0 0 1 2-2h8z"/></>,
    paperclip: <path d="M21 12.5l-8.5 8.5a5.5 5.5 0 0 1-7.8-7.8l9-9a3.7 3.7 0 0 1 5.2 5.2l-8.5 8.5a1.8 1.8 0 0 1-2.6-2.6L15.5 8"/>,
    settings: <><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></>,
    bell: <><path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/></>,
    refresh: <><path d="M3 12a9 9 0 0 1 15-6.7L21 8M21 3v5h-5"/></>,
    skip: <><path d="M5 4l10 8-10 8z"/><line x1="19" y1="5" x2="19" y2="19"/></>,
    palette: <><circle cx="12" cy="12" r="9"/><circle cx="7" cy="10" r="1.3" fill="currentColor"/><circle cx="12" cy="7" r="1.3" fill="currentColor"/><circle cx="17" cy="10" r="1.3" fill="currentColor"/><circle cx="16" cy="15" r="1.3" fill="currentColor"/><path d="M12 21a3 3 0 0 1-3-3 2 2 0 0 1 2-2h2a2 2 0 0 0 2-2"/></>,
    target: <><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></>,
    lightbulb: <><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.5 14a5 5 0 1 0-7 0c.6.6 1 1.4 1 2.3V18h5v-1.7c0-.9.4-1.7 1-2.3z"/></>,
    moon: <path d="M21 14.4A7.8 7.8 0 0 1 9.6 3 8.8 8.8 0 1 0 21 14.4z"/>,
    chart: <><path d="M3 3v18h18"/><path d="M7 14l3-3 4 4 5-6"/></>,
    trending: <><path d="M22 7l-9 9-5-5-7 7"/><path d="M16 7h6v6"/></>,
    layers: <><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></>,
    list: <><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></>,
    moreH: <><circle cx="5" cy="12" r="1.2" fill="currentColor"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/><circle cx="19" cy="12" r="1.2" fill="currentColor"/></>,
    moreV: <><circle cx="12" cy="5" r="1.2" fill="currentColor"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/><circle cx="12" cy="19" r="1.2" fill="currentColor"/></>,
    link: <><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></>,
    folder: <path d="M3 7a2 2 0 0 1 2-2h4l2 3h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>,
    flag: <><path d="M4 22V4"/><path d="M4 4h13l-2 4 2 4H4"/></>,
    headphone: <><path d="M3 18v-6a9 9 0 0 1 18 0v6"/><path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3z"/><path d="M3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"/></>,
    /* brand glyphs */
    xhs: <><rect x="3" y="3" width="18" height="18" rx="4"/></>,
    nori: null, // logo handled separately
  };
  return <svg {...props}>{paths[name]}</svg>;
};

/* Brand logo — uses the supplied clean geometric onion mark. */
const NoriLogo = ({ size = 28, dark = true, framed = true }) => {
  return (
    <div style={{
      width: size,
      height: size,
      borderRadius: framed ? size * 0.34 : 0,
      background: framed
        ? (dark ? 'rgba(255,255,255,.82)' : 'rgba(14,14,44,.9)')
        : 'transparent',
      border: framed ? '1px solid rgba(14,14,44,.055)' : 'none',
      boxShadow: framed ? '0 10px 24px rgba(14,14,44,.06), inset 0 1px 0 rgba(255,255,255,.86)' : 'none',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0,
      overflow: 'hidden',
    }}>
      <img
        src={NORI_LOGO_SRC}
        alt="Nori"
        style={{
          width: framed ? '72%' : '100%',
          height: framed ? '72%' : '100%',
          objectFit: 'contain',
          display: 'block',
          filter: dark ? 'none' : 'invert(1)',
        }}
      />
    </div>
  );
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
    isMobile: width < 760,
  };
};

const PlatformLogo = ({ kind, size = 20 }) => {
  const base = {
    width: size,
    height: size,
    borderRadius: size * 0.32,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    overflow: 'hidden',
    flexShrink: 0,
  };
  if (kind === 'xhs') {
    return (
      <span style={{
        ...base,
        background: '#ff2442',
        color: '#fff',
        fontSize: size * 0.36,
        fontWeight: 800,
        letterSpacing: 0,
        boxShadow: 'inset 0 1px 0 rgba(255,255,255,.24)',
      }}>
        RED
      </span>
    );
  }
  if (kind === 'dy') {
    return (
      <span style={{ ...base, background: '#111', padding: 0 }}>
        <img
          src="/Users/holly/Downloads/vecteezy_tiktok-png-icon_16716450.png"
          alt="Douyin"
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </span>
    );
  }
  if (kind === 'bili') {
    return (
      <span style={{
        ...base,
        background: '#ffffff',
        color: '#fb7299',
        border: '1px solid rgba(251,114,153,.18)',
        boxShadow: '0 2px 8px rgba(251,114,153,.12)',
      }}>
        <Icon name="bilibili" size={size * 0.76} color="currentColor" />
      </span>
    );
  }
  return (
    <span style={{ ...base, background: T.success, color: '#fff', fontSize: size * 0.52, fontWeight: 800 }}>
      微
    </span>
  );
};

const GLOBAL_RECENT_SESSIONS = [
  '上海饭店推荐 · 当前',
  '下班后小馆地图',
  '人均 80 约饭清单',
  '产品测评 · AI 视频工具横评',
  '极简通勤穿搭一周 OOTD',
  '咖啡入门 12 个名词',
  '我和我的猫 · 7 个瞬间',
];

const Sidebar = ({ active, onNew, onNavigate = () => {}, sessions = [], collapsed = false, onToggle = () => {} }) => {
  return (
    <aside style={{
      width: collapsed ? 66 : 220,
      flexShrink: 0,
      background: 'linear-gradient(180deg, rgba(250,252,254,.98), rgba(247,249,252,.96))',
      display: 'flex',
      flexDirection: 'column',
      padding: collapsed ? '12px 9px' : '16px 12px',
      height: '100%',
      borderRight: '1px solid rgba(14,14,44,.075)',
      boxShadow: '8px 0 28px rgba(14,14,44,.018)',
      backdropFilter: 'blur(20px) saturate(1.12)',
      transition: `width .42s ${T.spring}, padding .42s ${T.spring}`,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 9, justifyContent: collapsed ? 'center' : 'flex-start', padding: collapsed ? '3px 2px 22px' : '3px 10px 22px' }}>
        {!collapsed && <NoriLogo size={22} framed={false} />}
        {!collapsed && <span style={{ fontSize: 16, fontWeight: 720, letterSpacing: 0, color: T.navy }}>Nori</span>}
        <button
          onClick={onToggle}
          aria-label={collapsed ? '展开导航栏' : '收起导航栏'}
          style={{
            marginLeft: collapsed ? 0 : 'auto',
            width: 30,
            height: 30,
            borderRadius: 11,
            border: `1px solid ${T.hairlineSoft}`,
            background: 'rgba(255,255,255,.70)',
            color: T.navyLight,
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            boxShadow: collapsed ? T.shadowSm : 'inset 0 1px 0 rgba(255,255,255,.78)',
            transition: `transform .28s ${T.spring}, box-shadow .28s ${T.spring}, background .28s ${T.ease}`,
          }}
          onMouseEnter={e => {
            e.currentTarget.style.transform = 'translateY(-1px)';
            e.currentTarget.style.boxShadow = T.shadowSm;
          }}
          onMouseLeave={e => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = collapsed ? T.shadowSm : 'inset 0 1px 0 rgba(255,255,255,.72)';
          }}
        >
          <Icon name="splitView" size={16} color="currentColor" />
        </button>
      </div>

      <button
        onClick={() => onNew && onNew()}
        style={{
          height: collapsed ? 38 : 40,
          borderRadius: collapsed ? 13 : 11,
          border: 'none',
          background: `linear-gradient(135deg, ${T.iris}, #686AF4)`,
          color: T.white,
          display: 'flex',
          alignItems: 'center',
          justifyContent: collapsed ? 'center' : 'space-between',
          padding: collapsed ? 0 : '0 14px',
          fontSize: 13,
          fontWeight: 650,
          cursor: 'pointer',
          marginBottom: 14,
          boxShadow: '0 14px 28px rgba(75,77,237,.18), inset 0 1px 0 rgba(255,255,255,.18)',
          transition: `transform .28s ${T.spring}, background .24s ${T.ease}, box-shadow .28s ${T.spring}`,
        }}
        onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-1px)'; e.currentTarget.style.boxShadow = '0 18px 34px rgba(75,77,237,.24), inset 0 1px 0 rgba(255,255,255,.22)'; }}
        onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 14px 28px rgba(75,77,237,.18), inset 0 1px 0 rgba(255,255,255,.18)'; }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <Icon name="plus" size={collapsed ? 15 : 16} color="currentColor" />
          {!collapsed && <span>新建内容</span>}
        </div>
      </button>

      <nav style={{ display: 'flex', flexDirection: 'column', gap: 5 }}>
        {[
          { id: 'home', label: '创作', icon: 'home' },
          { id: 'library', label: '资产', icon: 'library' },
          { id: 'insights', label: '洞察', icon: 'chart' },
          { id: 'mine', label: '我的', icon: 'user' },
        ].map(item => (
          <a
            key={item.id}
            href="#"
            onClick={e => {
              e.preventDefault();
              onNavigate(item.id);
              if (item.id !== 'home' && !collapsed) onToggle();
            }}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: collapsed ? 0 : 9,
              justifyContent: collapsed ? 'center' : 'flex-start',
              padding: collapsed ? '0' : '0 12px',
              height: collapsed ? 38 : 40,
              borderRadius: collapsed ? 13 : 10,
              fontSize: 13,
              fontWeight: active === item.id ? 680 : 560,
              color: active === item.id ? T.iris : T.navyMid,
              background: active === item.id ? 'rgba(75,77,237,.105)' : 'transparent',
              textDecoration: 'none',
              transition: `background .24s ${T.ease}, color .24s ${T.ease}, transform .28s ${T.spring}, box-shadow .28s ${T.spring}`,
              marginBottom: collapsed ? 7 : 0,
              boxShadow: active === item.id ? 'inset 0 1px 0 rgba(255,255,255,.74)' : 'none',
            }}
            onMouseEnter={e => { if (active !== item.id) e.currentTarget.style.background = 'rgba(14,14,44,.028)'; }}
            onMouseLeave={e => { if (active !== item.id) e.currentTarget.style.background = 'transparent'; }}
          >
            <Icon name={item.icon} size={collapsed ? 15 : 16} color={active === item.id ? T.iris : T.navyMid} />
            {!collapsed && item.label}
          </a>
        ))}
      </nav>

      <div style={{ marginTop: 22, paddingTop: 18, borderTop: `1px solid ${T.hairline}`, flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        {!collapsed && <div style={{ fontSize: 11, fontWeight: 620, letterSpacing: 0, color: T.navyLight, padding: '0 10px 10px' }}>
          最近
        </div>}
        {!collapsed && <div style={{ overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 1 }}>
          {GLOBAL_RECENT_SESSIONS.map((s, i) => (
            <a
              key={i}
              href="#"
              style={{
                padding: collapsed ? '8px 0' : '6px 10px',
                borderRadius: 6,
                fontSize: 11.5,
                color: T.navyLight,
                fontWeight: 450,
                textDecoration: 'none',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                transition: 'background .12s',
                textAlign: collapsed ? 'center' : 'left',
              }}
              onMouseEnter={e => e.currentTarget.style.background = 'rgba(14,14,44,.03)'}
              onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
            >
              {collapsed ? `${i + 1}` : s}
            </a>
          ))}
        </div>}
      </div>

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          justifyContent: collapsed ? 'center' : 'flex-start',
          padding: collapsed ? '8px 0' : '10px',
          borderRadius: collapsed ? 16 : 10,
          marginTop: 12,
          cursor: 'pointer',
          transition: 'background .12s',
        }}
        onMouseEnter={e => e.currentTarget.style.background = T.surface}
        onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
      >
        <div style={{
          width: collapsed ? 36 : 28,
          height: collapsed ? 36 : 28,
          borderRadius: '50%',
          background: `linear-gradient(135deg, ${T.iris}, ${T.peach})`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: T.white,
          fontSize: collapsed ? 12 : 11,
          fontWeight: 700,
          boxShadow: collapsed ? T.shadowSm : 'none',
        }}>L</div>
        {!collapsed && <div style={{ display: 'flex', flexDirection: 'column', minWidth: 0, flex: 1 }}>
          <span style={{ fontSize: 12, fontWeight: 600, color: T.navy }}>Luna</span>
          <span style={{ fontSize: 10, color: T.navyLight }}>Pro · 87 / 200 次</span>
        </div>}
        {!collapsed && <Icon name="moreH" size={14} color={T.navyLight} />}
      </div>
    </aside>
  );
};

const OnionBurst = ({ active, mobile }) => {
  const pieces = [
    { src: ONION_BURST_ASSETS[0], x: -104, y: -70, r: -13, s: .54, d: '0ms' },
    { src: ONION_BURST_ASSETS[1], x: 86, y: -78, r: 14, s: .45, d: '45ms' },
    { src: ONION_BURST_ASSETS[2], x: 116, y: 10, r: 11, s: .47, d: '90ms' },
    { src: ONION_BURST_ASSETS[3], x: -118, y: 18, r: -8, s: .43, d: '120ms' },
    { src: ONION_BURST_ASSETS[4], x: 28, y: -112, r: 6, s: .41, d: '155ms' },
  ];
  if (!active) return null;
  return (
    <div aria-hidden="true" style={{ position: 'absolute', left: '50%', top: '46%', width: 1, height: 1, pointerEvents: 'none', zIndex: 3 }}>
      {pieces.map((piece, i) => (
        <img
          key={`${piece.src}-${i}`}
          src={piece.src}
          alt=""
          style={{
            position: 'absolute',
            width: mobile ? 40 : 54,
            height: mobile ? 40 : 54,
            objectFit: 'contain',
            mixBlendMode: 'multiply',
            '--x': `${mobile ? piece.x * .62 : piece.x}px`,
            '--y': `${mobile ? piece.y * .62 : piece.y}px`,
            '--r': `${piece.r}deg`,
            filter: 'drop-shadow(0 10px 20px rgba(14,14,44,.08))',
            animation: `onionPop 1.45s ${piece.d} ${T.spring} both`,
          }}
        />
      ))}
      {[0, 1, 2, 3, 4, 5].map(i => (
        <span key={i} style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width: i % 2 ? 5 : 4,
          height: i % 2 ? 5 : 4,
          borderRadius: '50%',
          background: i % 3 === 0 ? T.primary : i % 3 === 1 ? T.iris : T.peach,
          '--spark-x': `${mobile ? [-74, 68, 116, -110, 28, -18][i] * .62 : [-74, 68, 116, -110, 28, -18][i]}px`,
          '--spark-y': `${mobile ? [-50, -60, 52, 44, -112, 88][i] * .62 : [-50, -60, 52, 44, -112, 88][i]}px`,
          boxShadow: '0 0 16px currentColor',
          animation: `sparkPop 1.2s ${i * 48}ms ${T.spring} both`,
        }} />
      ))}
    </div>
  );
};

const HeroHeadline = ({ compact, mobile }) => {
  const [burst, setBurst] = React.useState(false);
  const triggerBurst = () => {
    setBurst(false);
    window.requestAnimationFrame(() => setBurst(true));
  };
  React.useEffect(() => {
    if (!burst) return undefined;
    const timer = window.setTimeout(() => setBurst(false), 1700);
    return () => window.clearTimeout(timer);
  }, [burst]);

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      marginBottom: mobile ? 14 : 18,
      textAlign: 'center',
    }}>
      <div style={{
        position: 'absolute',
        left: '50%',
        top: '46%',
        width: mobile ? 170 : 300,
        height: mobile ? 88 : 120,
        borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(214,255,0,.12), rgba(243,217,218,.10) 46%, rgba(75,77,237,.055) 62%, transparent 76%)',
        opacity: .38,
        transform: 'translate3d(-50%, -50%, 0)',
        filter: 'blur(24px)',
        pointerEvents: 'none',
      }} />
      <OnionBurst active={burst} mobile={mobile} />
      <button
        onClick={triggerBurst}
        aria-label="触发 Nori 洋葱闪光"
        className={burst ? 'noriWord noriWordSpark' : 'noriWord'}
        style={{
          position: 'relative',
          zIndex: 4,
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          border: 'none',
          background: 'transparent',
          padding: '0 8px 2px',
          cursor: 'pointer',
          color: T.navy,
          fontFamily: T.fontSerif,
          fontSize: mobile ? 38 : compact ? 54 : 62,
          lineHeight: .92,
          fontWeight: 700,
          fontStyle: 'italic',
          letterSpacing: 0,
        }}
      >
        Nori
      </button>
      <p style={{
        position: 'relative',
        zIndex: 1,
        margin: mobile ? '8px 0 0' : '12px 0 0',
        color: T.navyLight,
        fontSize: mobile ? 12 : 13,
        lineHeight: 1.55,
        fontWeight: 520,
        letterSpacing: 0,
      }}>
        懂你，会进化的自媒体账号代理
      </p>
    </div>
  );
};

const FormatTag = ({ label, sub, onCancel }) => (
  <div style={{
    display: 'inline-flex',
    alignItems: 'center',
    gap: 6,
    padding: '4px 6px 4px 10px',
    borderRadius: 999,
    background: T.irisTint,
    color: T.iris,
    fontSize: 12,
    fontWeight: 600,
    marginBottom: 10,
  }}>
    {label}{sub ? ` · ${sub}` : ''}
    <button onClick={onCancel} style={{
      width: 18,
      height: 18,
      borderRadius: '50%',
      border: 'none',
      cursor: 'pointer',
      background: 'rgba(75,77,237,.15)',
      color: T.iris,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <Icon name="close" size={10} stroke={2.4} />
    </button>
  </div>
);

const HomeComposer = ({ value, onChange, onSubmit, format, onClearFormat, compact, mobile }) => {
  const [focused, setFocused] = React.useState(false);
  const prompts = [
    '让 Nori 生成一组城市探店的小红书图文',
    '让 Nori 打造一个女性成长博主的账号',
    '让 Nori 生成一篇有关于 AI 最新报道的公众号文章',
    '让 Nori 设计一组通勤穿搭选题',
    '让 Nori 拆解一个咖啡品牌的内容增长路径',
    '让 Nori 把灵感变成一周短视频脚本',
  ];
  const [promptIndex, setPromptIndex] = React.useState(0);

  React.useEffect(() => {
    const timer = window.setInterval(() => {
      setPromptIndex(i => (i + 1) % prompts.length);
    }, 2600);
    return () => window.clearInterval(timer);
  }, []);

  return (
    <div style={{
      position: 'relative',
      background: 'linear-gradient(180deg, rgba(255,255,255,.94), rgba(250,252,254,.82))',
      borderRadius: mobile ? 20 : 24,
      border: `1.4px solid ${focused ? 'rgba(75,77,237,.22)' : 'rgba(75,77,237,.11)'}`,
      boxShadow: focused
        ? `0 0 0 4px rgba(75,77,237,.055), 0 20px 46px rgba(14,14,44,.065), 0 16px 42px rgba(49,208,170,.045), inset 0 1px 0 rgba(255,255,255,.95)`
        : '0 16px 42px rgba(14,14,44,.052), 0 12px 36px rgba(49,208,170,.032), inset 0 1px 0 rgba(255,255,255,.9)',
      padding: mobile ? '13px 13px 11px' : compact ? '16px 18px 14px' : '17px 20px 14px',
      transition: `border .28s ${T.ease}, box-shadow .36s ${T.spring}, transform .36s ${T.spring}`,
      backdropFilter: 'blur(26px) saturate(1.2)',
      overflow: 'hidden',
      animation: focused ? 'prismBorder 2.8s ease-in-out infinite' : 'none',
    }}>
      <div style={{
        position: 'absolute',
        inset: 0,
        background: 'radial-gradient(circle at 12% 18%, rgba(214,255,0,.11), transparent 32%), radial-gradient(circle at 92% 12%, rgba(75,77,237,.055), transparent 25%)',
        pointerEvents: 'none',
      }} />

      <div style={{ position: 'relative', zIndex: 1 }}>
        {format && <FormatTag label={format.label} sub={format.sub} onCancel={onClearFormat} />}

        <div style={{ position: 'relative' }}>
          {!value && (
            <div
              key={promptIndex}
              style={{
                position: 'absolute',
                left: 0,
                top: 0,
                right: 0,
                color: T.navyLight,
                fontSize: mobile ? 14 : 15,
                fontWeight: 570,
                lineHeight: 1.55,
                pointerEvents: 'none',
                animation: `templateTicker 2.6s ${T.spring} both`,
                whiteSpace: mobile ? 'normal' : 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
              }}
            >
              {prompts[promptIndex]}
            </div>
          )}
          <textarea
            value={value}
            onChange={e => onChange(e.target.value)}
            onFocus={() => setFocused(true)}
            onBlur={() => setFocused(false)}
            onKeyDown={e => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                if (value.trim()) onSubmit();
              }
            }}
            placeholder=""
            rows={mobile ? 3 : 2}
            style={{
              width: '100%',
              border: 'none',
              outline: 'none',
              background: 'transparent',
              resize: 'none',
              fontSize: mobile ? 14 : 15,
              fontWeight: 570,
              lineHeight: 1.55,
              color: T.navy,
              fontFamily: T.fontSans,
              minHeight: mobile ? 74 : 76,
              maxHeight: 124,
              position: 'relative',
              zIndex: 1,
            }}
          />
        </div>

        <div style={{
          display: 'flex',
          alignItems: mobile ? 'stretch' : 'center',
          justifyContent: 'space-between',
          gap: 10,
          marginTop: mobile ? 2 : 6,
          flexDirection: mobile ? 'column' : 'row',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
            <ToolPill icon="paperclip" label="附件" />
            <ToolPill icon="sparkle" label="优化" />
          </div>

          <button
            onClick={() => value.trim() && onSubmit()}
            disabled={!value.trim()}
            style={{
              width: mobile ? '100%' : 38,
              height: mobile ? 36 : 38,
              borderRadius: mobile ? 999 : '50%',
              border: 'none',
              cursor: value.trim() ? 'pointer' : 'not-allowed',
              background: value.trim() ? T.navy : 'rgba(14,14,44,.075)',
              color: value.trim() ? T.white : T.navyLight,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 8,
              boxShadow: value.trim() ? '0 10px 22px rgba(14,14,44,.16), inset 0 1px 0 rgba(255,255,255,.10)' : 'none',
              transition: `transform .26s ${T.spring}, box-shadow .26s ${T.spring}, background .2s ${T.ease}, color .2s ${T.ease}`,
            }}
            onMouseEnter={e => { if (value.trim()) e.currentTarget.style.transform = 'translateY(-1px) scale(1.02)'; }}
            onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0) scale(1)'; }}
          >
            <Icon name="paperPlane" size={13} stroke={2} />
            {mobile && <span style={{ fontSize: 13, fontWeight: 600 }}>Start crafting</span>}
          </button>
        </div>
      </div>
    </div>
  );
};

const HomeIpModeBar = ({ mobile, onAccountPlan, onViewProfile, planned }) => {
  const [freeMode, setFreeMode] = React.useState(false);
  const isIpMode = planned && !freeMode;
  const icon = isIpMode ? 'check' : freeMode ? 'unlock' : 'lock';
  const title = isIpMode ? '已开启 IP 模式 · 上海小饭店主理人' : freeMode ? '自由模式 · 内容不关联 IP' : '完成账号规划，解锁 IP 模式';
  const desc = isIpMode ? '真实到店 · 菜品稳定 · 先结论再展开' : freeMode ? '' : '按门店气质和经营方式生成';
  return (
    <div style={{
      width: '100%',
      minHeight: mobile ? 52 : 54,
      borderRadius: mobile ? 20 : 22,
      border: planned && !freeMode ? `1px solid rgba(14,14,44,.08)` : `1px dashed rgba(14,14,44,.16)`,
      background: 'rgba(255,255,255,.86)',
      boxShadow: planned && !freeMode ? '0 12px 26px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.9)' : 'inset 0 1px 0 rgba(255,255,255,.9)',
      display: 'flex',
      alignItems: mobile ? 'flex-start' : 'center',
      justifyContent: 'space-between',
      gap: 12,
      padding: mobile ? '13px 14px' : '0 18px',
      marginBottom: 12,
      flexDirection: mobile ? 'column' : 'row',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, minWidth: 0 }}>
        <span style={{
          width: isIpMode || freeMode ? 10 : 28,
          height: isIpMode || freeMode ? 10 : 28,
          borderRadius: isIpMode || freeMode ? '50%' : 10,
          background: isIpMode ? T.success : freeMode ? 'rgba(14,14,44,.18)' : T.irisTint,
          border: isIpMode || freeMode ? 'none' : `1px solid ${T.hairlineSoft}`,
          color: isIpMode ? T.success : freeMode ? T.navyMid : T.iris,
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0,
        }}>
          {!isIpMode && !freeMode && <Icon name={icon === 'unlock' ? 'lock' : icon} size={13} />}
        </span>
        <div style={{ minWidth: 0, color: T.navyMid, fontSize: mobile ? 13 : 14, lineHeight: 1.42 }}>
          <span style={{ color: T.navy, fontWeight: isIpMode ? 640 : 680 }}>{title}</span>
          {desc && <span> · {desc}</span>}
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexShrink: 0 }}>
        {isIpMode && (
          <button
            onClick={onViewProfile}
            style={{
              border: 'none',
              background: 'transparent',
              color: T.navyMid,
              cursor: 'pointer',
              fontSize: 13,
              fontWeight: 660,
              padding: '6px 4px',
            }}
          >
            查看
          </button>
        )}
        {(!isIpMode || freeMode) && (
          <button
            onClick={onAccountPlan}
            style={{
              border: freeMode ? `1px solid ${T.hairlineSoft}` : 'none',
              background: freeMode ? 'rgba(255,255,255,.72)' : T.navy,
              color: freeMode ? T.navy : T.white,
              cursor: 'pointer',
              fontSize: 12.5,
              fontWeight: 700,
              height: 32,
              padding: '0 12px',
              borderRadius: 999,
              display: 'inline-flex',
              alignItems: 'center',
              gap: 6,
              boxShadow: freeMode ? 'none' : '0 10px 20px rgba(14,14,44,.12)',
            }}
          >
            {freeMode ? '开启' : '开始'}
            <Icon name="arrowRight" size={12} />
          </button>
        )}
        {isIpMode && (
          <button
            onClick={() => setFreeMode(true)}
            style={{
              border: 'none',
              background: 'rgba(255,255,255,.72)',
              color: T.navy,
              cursor: 'pointer',
              fontSize: 13,
              fontWeight: 700,
              height: 36,
              padding: '0 14px',
              borderRadius: 999,
              boxShadow: `inset 0 0 0 1px ${T.hairlineSoft}`,
            }}
          >
            关闭
          </button>
        )}
      </div>
    </div>
  );
};

const FormatPicker = ({ format, onPick, compact, mobile }) => {
  const [openCat, setOpenCat] = React.useState(null);
  const cats = [
    { key: 'xhs', icon: 'image', label: '小红书图文' },
    { key: 'wechat', icon: 'document', label: '公众号长文' },
    { key: 'video', icon: 'video', label: '抖音短视频' },
    { key: 'wechatShort', icon: 'video', label: '公众号短视频' },
    { key: 'drama', icon: 'play', label: '漫剧' },
    { key: 'podcast', icon: 'headphone', label: '播客' },
    { key: 'ins', icon: 'image', label: 'Ins post' },
  ];
  const subs = {
    xhs: ['爆款种草', '攻略干货', '生活记录', '产品测评'],
    wechat: ['深度长文', '观点专栏', '人物访谈', '行业分析'],
    video: ['科普视频', '产品宣传', '漫剧', '口播'],
    wechatShort: ['门店短片', '活动预告', '主理人出镜', '菜品展示'],
    drama: ['剧情种草', '人物关系', '反转钩子', '连载脚本'],
    podcast: ['访谈提纲', '单人口播', '播客切片', '节目大纲'],
    ins: ['九宫格', 'Reels 封面', 'Story', 'Carousel'],
  };
  const current = openCat ? cats.find(c => c.key === openCat) : null;

  return (
    <div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, justifyContent: mobile ? 'center' : 'flex-start' }}>
        {cats.map(c => {
          const isOpen = openCat === c.key;
          const isPicked = format && format.cat === c.key;
          return (
            <button
              key={c.key}
              onClick={() => setOpenCat(isOpen ? null : c.key)}
              style={{
                minHeight: 32,
                padding: compact ? '0 10px' : '0 12px',
                borderRadius: 99,
                border: `1px solid ${isOpen || isPicked ? 'rgba(14,14,44,.32)' : T.hairlineSoft}`,
                background: isOpen || isPicked ? T.navy : 'rgba(255,255,255,.72)',
                color: isOpen || isPicked ? T.white : T.navyMid,
                fontSize: 12.5,
                fontWeight: 520,
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
                boxShadow: isOpen || isPicked ? '0 10px 24px rgba(14,14,44,.12)' : '0 6px 16px rgba(14,14,44,.035)',
                transition: `transform .28s ${T.spring}, background .22s ${T.ease}, border .22s ${T.ease}, box-shadow .28s ${T.spring}`,
                backdropFilter: 'blur(14px) saturate(1.18)',
              }}
            >
              <Icon name={c.icon} size={13} />
              {c.label}
            </button>
          );
        })}
      </div>
      {current && (
        <div style={{
          marginTop: 10,
          display: 'flex',
          flexWrap: 'wrap',
          gap: 8,
          animation: `fadeIn .28s ${T.spring}`,
          justifyContent: mobile ? 'center' : 'flex-start',
        }}>
          {subs[current.key].map((s, i) => (
            <button
              key={i}
              onClick={() => { onPick({ cat: current.key, label: current.label, sub: s }); setOpenCat(null); }}
              style={{
                background: 'rgba(255,255,255,.82)',
                border: `1px solid ${T.hairlineSoft}`,
                borderRadius: 16,
                padding: '8px 12px',
                textAlign: 'left',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                gap: 2,
                minWidth: mobile ? 124 : 136,
                transition: `transform .28s ${T.spring}, border .22s ${T.ease}, box-shadow .28s ${T.spring}`,
                boxShadow: '0 8px 18px rgba(14,14,44,.04)',
              }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(75,77,237,.4)'; e.currentTarget.style.transform = 'translateY(-1px)'; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = T.hairlineSoft; e.currentTarget.style.transform = 'translateY(0)'; }}
            >
              <span style={{ fontSize: 12.5, fontWeight: 600, color: T.navy }}>{s}</span>
              <span style={{ fontSize: 10.5, color: T.navyLight }}>{current.label} · {s}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

const ToolPill = ({ icon, label, active, onClick }) => {
  const [hov, setHov] = React.useState(false);
  return (
    <button
      type="button"
      onClick={onClick}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        height: 32,
        padding: '0 12px',
        borderRadius: 99,
        background: active ? 'rgba(239,239,253,.92)' : (hov ? 'rgba(255,255,255,.88)' : 'rgba(255,255,255,.68)'),
        border: `1px solid ${active ? 'rgba(75,77,237,.22)' : 'rgba(14,14,44,.08)'}`,
        color: active ? T.iris : T.navyMid,
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        fontSize: 12.5,
        fontWeight: active ? 690 : 580,
        cursor: 'pointer',
        transform: hov ? 'translateY(-1px)' : 'translateY(0)',
        transition: `transform .24s ${T.spring}, background .24s ${T.ease}, border .24s ${T.ease}, color .24s ${T.ease}`,
      }}
    >
      <Icon name={icon} size={14} />
      {label}
    </button>
  );
};

const InspirationPhoto = ({ src, shape, rotate = 0, height }) => {
  const clipPaths = {
    petal: 'polygon(12% 16%, 34% 9%, 46% 0%, 60% 12%, 81% 8%, 100% 22%, 93% 44%, 100% 71%, 82% 88%, 61% 84%, 44% 100%, 22% 92%, 0% 74%, 7% 48%, 0% 24%)',
    ribbon: 'polygon(6% 7%, 44% 0%, 64% 9%, 100% 4%, 90% 38%, 100% 65%, 83% 100%, 46% 92%, 26% 100%, 0% 81%, 9% 48%, 0% 17%)',
    bloom: 'polygon(11% 0%, 38% 8%, 58% 0%, 74% 15%, 100% 17%, 94% 50%, 100% 80%, 76% 100%, 49% 93%, 30% 100%, 0% 82%, 8% 51%, 0% 18%)',
  };
  return (
    <div style={{
      width: '100%',
      height,
      transform: `rotate(${rotate}deg)`,
      position: 'relative',
    }}>
      <div style={{
        width: '100%',
        height: '100%',
        clipPath: clipPaths[shape] || clipPaths.petal,
        overflow: 'hidden',
        boxShadow: '0 20px 36px rgba(14,14,44,.12)',
      }}>
        <img src={src} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </div>
    </div>
  );
};

const QuickStart = ({ onPick, compact, mobile }) => {
  const shelves = [
    [
      { title: '阳台植物的情绪版改造', desc: '从一个小阳台出发，延展成封面、图文和短视频脚本。', tint: '#fcf6f6', accent: '#aa2e3d', tag: 'Balcony Reset', platform: 'dy', photo: 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?auto=format&fit=crop&w=900&q=80', shape: 'ribbon', rotate: -5 },
      { title: '当家居博主爱上拼豆后', desc: '把手作过程变成更有记忆点的生活方式内容。', tint: '#f8fbf3', accent: '#736e00', tag: 'Craft Loop', platform: 'xhs', photo: 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80', shape: 'petal', rotate: 4 },
      { title: '深夜食堂里的治愈系主厨', desc: '从一碗热汤，做出一整套有人情味的社媒叙事。', tint: '#f7f6ff', accent: '#4950a5', tag: 'Warm Series', platform: 'bili', photo: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80', shape: 'bloom', rotate: -3 },
      { title: '职场人的知识 IP 变现路径', desc: '把五年经验整理成会传播、可连载的知识内容。', tint: '#f5f8fc', accent: '#21489e', tag: 'Pro Story', platform: 'dy', photo: 'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=900&q=80', shape: 'petal', rotate: 3 },
    ],
    [
      { title: '猫咪日常也能拍出栏目感', desc: '把碎片化生活切成固定栏目，轻松做持续更新。', tint: '#fcf8f3', accent: '#8e4e00', tag: 'Soft Habit', platform: 'xhs', photo: 'https://images.unsplash.com/photo-1519052537078-e6302a4968d4?auto=format&fit=crop&w=900&q=80', shape: 'bloom', rotate: -4 },
      { title: 'City Walk 变成城市策展笔记', desc: '不是打卡清单，而是有审美和路线逻辑的内容包。', tint: '#fcf6fb', accent: '#7e3d79', tag: 'Urban Edit', platform: 'bili', photo: 'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80', shape: 'ribbon', rotate: 5 },
      { title: '咖啡入门 12 个名词', desc: '做成对新手友好的知识卡片和短内容矩阵。', tint: '#fbf8f2', accent: '#8d6d38', tag: 'Starter Pack', platform: 'dy', photo: 'https://images.unsplash.com/photo-1442512595331-e89e73853f31?auto=format&fit=crop&w=900&q=80', shape: 'petal', rotate: -3 },
      { title: '极简通勤穿搭一周 OOTD', desc: '让日常穿搭更像连载内容，而不是单条记录。', tint: '#f5f7fd', accent: '#4868a5', tag: 'Week Format', platform: 'xhs', photo: 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?auto=format&fit=crop&w=900&q=80', shape: 'bloom', rotate: 2 },
    ],
    [
      { title: '租房避雷指南 v2', desc: '把经验帖升级成更有结构、更有分享欲的攻略。', tint: '#f6f7fd', accent: '#4c5eb3', tag: 'Field Notes', platform: 'bili', photo: 'https://images.unsplash.com/photo-1460317442991-0ec209397118?auto=format&fit=crop&w=900&q=80', shape: 'petal', rotate: -4 },
      { title: 'AI 视频工具横评', desc: '从工具参数转成更适合传播的体验型结论。', tint: '#f6fbf6', accent: '#48762d', tag: 'Tool Review', platform: 'dy', photo: 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80', shape: 'bloom', rotate: 4 },
      { title: '品牌主理人的幕后手帐', desc: '把产品思考、开会片段和灵感卡片织成系列。', tint: '#fcf7f3', accent: '#9a5426', tag: 'Behind Scene', platform: 'xhs', photo: 'https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=900&q=80', shape: 'ribbon', rotate: -2 },
      { title: '健身猛男为什么爱粉色植物', desc: '反差感、观点感和视觉记忆点一次给足。', tint: '#fafbf2', accent: '#7d5a00', tag: 'Contrast Hook', platform: 'bili', photo: 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80', shape: 'petal', rotate: 3 },
    ],
  ];

  const [shelfIndex, setShelfIndex] = React.useState(0);
  const [animateKey, setAnimateKey] = React.useState(0);
  const items = shelves[shelfIndex];
  const layout = mobile ? '1fr' : compact ? 'repeat(2, minmax(0, 1fr))' : 'repeat(4, minmax(0, 1fr))';

  const refreshShelf = () => {
    setShelfIndex(prev => (prev + 1) % shelves.length);
    setAnimateKey(prev => prev + 1);
  };

  return (
    <section style={{
      padding: mobile ? '6px 0 6px' : '10px 0 4px',
    }}>
      <div style={{
        display: 'flex',
        alignItems: mobile ? 'flex-start' : 'center',
        justifyContent: 'space-between',
        gap: 14,
        flexWrap: 'wrap',
        marginBottom: 18,
      }}>
        <div>
          <div style={{ fontSize: 12, color: T.navyLight, marginBottom: 6, letterSpacing: '0.08em', textTransform: 'uppercase' }}>
            快速开始
          </div>
          <h3 style={{ fontSize: mobile ? 22 : 28, fontWeight: 450, lineHeight: 1.08, letterSpacing: '-0.04em', color: T.navy }}>
            Quick Start
          </h3>
        </div>

        <button
          onClick={refreshShelf}
          style={{
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
            boxShadow: T.shadowSm,
          }}
        >
          <Icon name="refresh" size={14} />
          换一换
        </button>
      </div>

      <div
        key={animateKey}
        style={{
          display: 'grid',
          gridTemplateColumns: layout,
          gap: mobile ? 12 : 14,
          alignItems: 'start',
        }}
      >
        {items.map((it, i) => (
          <button
            key={`${it.title}-${animateKey}`}
            onClick={() => onPick(it.title)}
            style={{
              background: 'transparent',
              border: 'none',
              padding: 0,
              textAlign: 'left',
              cursor: 'pointer',
              animation: `fadeInScale .42s ${i * 60}ms both`,
            }}
          >
            <div
              style={{
                position: 'relative',
                borderRadius: mobile ? 20 : 22,
                overflow: 'hidden',
                background: `linear-gradient(180deg, rgba(255,255,255,.92) 0%, ${it.tint} 100%)`,
                border: '1px solid rgba(14,14,44,.05)',
                boxShadow: '0 9px 24px rgba(14,14,44,.052), inset 0 1px 0 rgba(255,255,255,.82)',
                transition: `transform .42s ${T.spring}, box-shadow .42s ${T.spring}, border-color .26s ${T.ease}`,
              }}
              onMouseEnter={e => {
                e.currentTarget.style.transform = 'translateY(-4px) scale(1.004)';
                e.currentTarget.style.boxShadow = '0 18px 40px rgba(14,14,44,.078), inset 0 1px 0 rgba(255,255,255,.88)';
              }}
              onMouseLeave={e => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)';
                e.currentTarget.style.boxShadow = '0 9px 24px rgba(14,14,44,.052), inset 0 1px 0 rgba(255,255,255,.82)';
              }}
            >
              <div style={{
                minHeight: mobile ? 196 : compact ? 202 : 210,
                padding: mobile ? 13 : 14,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
              }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 10 }}>
                  <span style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '7px',
                    borderRadius: 999,
                    background: 'rgba(255,255,255,.74)',
                    backdropFilter: 'blur(8px)',
                  }}>
                    <PlatformLogo kind={it.platform} size={18} />
                  </span>
                  <div style={{
                    width: 32,
                    height: 32,
                    borderRadius: 999,
                    background: 'rgba(255,255,255,.42)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: T.navy,
                    boxShadow: 'inset 0 1px 0 rgba(255,255,255,.35)',
                  }}>
                    <Icon name="sparkles" size={13} color="currentColor" />
                  </div>
                </div>

                <div style={{
                  padding: mobile ? '4px 4px 0' : '8px 8px 0',
                }}>
                  <InspirationPhoto src={it.photo} shape={it.shape} rotate={it.rotate} height={mobile ? 82 : compact ? 90 : 96} />
                </div>
              </div>

              <div style={{ padding: '0 15px 14px' }}>
                <div style={{
                  fontSize: 10.5,
                  fontWeight: 700,
                  letterSpacing: '0.12em',
                  color: 'rgba(14,14,44,.52)',
                  textTransform: 'uppercase',
                  marginBottom: 7,
                }}>
                  {it.tag}
                </div>
                <div style={{ fontSize: 14.5, fontWeight: 620, color: T.navy, lineHeight: 1.32, marginBottom: 7, letterSpacing: 0 }}>
                  {it.title}
                </div>
                <div style={{ fontSize: 12.5, color: 'rgba(14,14,44,.78)', lineHeight: 1.54, minHeight: mobile ? 'auto' : 42 }}>
                  {it.desc}
                </div>
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 10 }}>
                  <span style={{
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
                    boxShadow: T.shadowXs,
                  }}>
                    进入
                    <Icon name="arrowRight" size={12} />
                  </span>
                </div>
              </div>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
};

const SectionTitle = ({ title, action, mobile }) => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 16,
    marginBottom: mobile ? 12 : 16,
  }}>
    <h2 style={{
      margin: 0,
      color: T.navy,
      fontSize: mobile ? 18 : 21,
      lineHeight: 1.2,
      fontWeight: 720,
      letterSpacing: 0,
    }}>
      {title}
    </h2>
    {action && (
      <button style={{
        border: 'none',
        background: 'transparent',
        color: T.navyLight,
        cursor: 'pointer',
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        fontSize: mobile ? 12.5 : 13.5,
        fontWeight: 520,
        padding: '6px 0',
      }}>
        {action}
        <Icon name="chevronRight" size={13} />
      </button>
    )}
  </div>
);

const RecentProjects = ({ mobile, compact, onNew, recentProject, onOpenProject }) => {
  const ActionCard = ({ icon, title, desc, cta, onClick }) => {
    const [hover, setHover] = React.useState(false);
    return (
      <button
        onClick={onClick}
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        style={{
          minWidth: 0,
          aspectRatio: '1 / 1',
          border: '1px solid rgba(14,14,44,.08)',
          background: 'rgba(255,255,255,.58)',
          borderRadius: 22,
          padding: mobile ? 15 : 16,
          textAlign: 'left',
          cursor: 'pointer',
          boxShadow: hover
            ? '0 18px 38px rgba(14,14,44,.07), inset 0 1px 0 rgba(255,255,255,.86)'
            : '0 10px 24px rgba(14,14,44,.035), inset 0 1px 0 rgba(255,255,255,.78)',
          transform: hover ? 'translateY(-3px)' : 'translateY(0)',
          transition: `transform .34s ${T.spring}, box-shadow .34s ${T.spring}, border .26s ${T.ease}, background .26s ${T.ease}`,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
        }}
      >
        <div style={{
          flex: 1,
          minHeight: 0,
          borderRadius: 18,
          border: '1.4px dashed rgba(14,14,44,.14)',
          background: 'rgba(250,252,254,.68)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: T.navyLight,
          boxShadow: 'inset 0 1px 0 rgba(255,255,255,.82)',
          overflow: 'hidden',
        }}>
          <span style={{
            width: 46,
            height: 46,
            borderRadius: 16,
            background: 'rgba(255,255,255,.72)',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 10px 22px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.86)',
            transformOrigin: '50% 50%',
          }}>
            <Icon name={icon} size={22} stroke={1.55} />
          </span>
        </div>
        <div style={{
          marginTop: 13,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 12,
        }}>
          <div style={{ minWidth: 0 }}>
            <div style={{ fontSize: mobile ? 14.5 : 15.5, fontWeight: 720, color: T.navy, letterSpacing: 0 }}>
              {title}
            </div>
            <div style={{ marginTop: 5, fontSize: 12.2, color: T.navyLight, lineHeight: 1.45 }}>
              {desc}
            </div>
          </div>
          <span style={{
            flexShrink: 0,
            height: 30,
            padding: '0 10px',
            borderRadius: 999,
            background: 'rgba(236,241,244,.74)',
            color: T.navyMid,
            fontSize: 11.5,
            fontWeight: 650,
            display: 'inline-flex',
            alignItems: 'center',
            gap: 5,
          }}>
            {cta}
            <Icon name="arrowRight" size={12} />
          </span>
        </div>
      </button>
    );
  };

  return (
    <section style={{
      width: '100%',
      maxWidth: mobile ? '100%' : compact ? 820 : 960,
      margin: '0 auto',
    }}>
      <SectionTitle title="最近项目" mobile={mobile} />
      <div style={{
        display: 'grid',
        gridTemplateColumns: mobile ? '1fr' : '168px minmax(0, 1fr)',
        gap: mobile ? 14 : 18,
        alignItems: 'stretch',
      }}>
        <ActionCard
          icon="plus"
          title="新建项目"
          desc="直接从一个想法开始生成内容"
          cta="开始"
          onClick={onNew}
        />
        {recentProject ? (
          <button
            onClick={onOpenProject}
            style={{
              minHeight: mobile ? 146 : 168,
              borderRadius: 22,
              border: `1px solid ${T.hairlineSoft}`,
              background: 'rgba(255,255,255,.72)',
              boxShadow: '0 12px 28px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.82)',
              padding: mobile ? 16 : 18,
              textAlign: 'left',
              cursor: 'pointer',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              transition: `transform .32s ${T.spring}, box-shadow .32s ${T.spring}`,
            }}
            onMouseEnter={e => {
              e.currentTarget.style.transform = 'translateY(-3px)';
              e.currentTarget.style.boxShadow = '0 18px 38px rgba(14,14,44,.065), inset 0 1px 0 rgba(255,255,255,.88)';
            }}
            onMouseLeave={e => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 12px 28px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.82)';
            }}
          >
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, marginBottom: 14 }}>
                <span style={{ width: 34, height: 34, borderRadius: 13, background: T.irisTint, color: T.iris, display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Icon name="document" size={15} />
                </span>
                <span style={{ color: T.navyLight, fontSize: 11.5, fontFamily: T.fontMono }}>{recentProject.date}</span>
              </div>
              <div style={{ color: T.navy, fontSize: mobile ? 15 : 16, lineHeight: 1.35, fontWeight: 740, maxWidth: 520 }}>{recentProject.title}</div>
              <div style={{ marginTop: 8, color: T.navyMid, fontSize: 12.2, lineHeight: 1.5 }}>{recentProject.summary}</div>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: T.navyLight, fontSize: 11.5, marginTop: 14 }}>
              <Icon name="chat" size={13} />
              点击继续查看历史对话
            </div>
          </button>
        ) : (
          <div style={{
            minHeight: mobile ? 118 : 168,
            borderRadius: 22,
            border: '1.5px dashed rgba(14,14,44,.13)',
            background: 'rgba(255,255,255,.42)',
            color: T.navyLight,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 10,
            fontSize: 12.5,
            fontWeight: 620,
            boxShadow: 'inset 0 1px 0 rgba(255,255,255,.72)',
          }}>
            <Icon name="folder" size={18} />
            还没有任何项目
          </div>
        )}
      </div>
    </section>
  );
};

const InspirationCard = ({ item, index, onUse }) => {
  const [buttonHover, setButtonHover] = React.useState(false);
  return (
  <article style={{
    breakInside: 'avoid',
    marginBottom: 16,
    borderRadius: 18,
    overflow: 'hidden',
    background: 'rgba(255,255,255,.82)',
    border: `1px solid ${T.hairlineSoft}`,
    boxShadow: '0 9px 22px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.86)',
    animation: `fadeInScale .48s ${(index % 5) * 42}ms ${T.spring} both`,
    transition: `transform .34s ${T.spring}, box-shadow .34s ${T.spring}`,
  }}
  onMouseEnter={e => {
    e.currentTarget.style.transform = 'translateY(-3px)';
    e.currentTarget.style.boxShadow = '0 16px 34px rgba(14,14,44,.065), inset 0 1px 0 rgba(255,255,255,.9)';
  }}
  onMouseLeave={e => {
    e.currentTarget.style.transform = 'translateY(0)';
    e.currentTarget.style.boxShadow = '0 9px 22px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.86)';
  }}
  >
    <div style={{ overflow: 'hidden', borderRadius: '18px 18px 0 0', background: T.surface }}>
      <img
        src={item.image}
        alt=""
        style={{
          width: '100%',
          aspectRatio: item.ratio,
          objectFit: 'cover',
          display: 'block',
          transition: `transform .68s ${T.spring}, filter .4s ${T.ease}`,
        }}
        onMouseEnter={e => {
          e.currentTarget.style.transform = 'scale(1.055)';
          e.currentTarget.style.filter = 'saturate(1.04)';
        }}
        onMouseLeave={e => {
          e.currentTarget.style.transform = 'scale(1)';
          e.currentTarget.style.filter = 'saturate(1)';
        }}
      />
    </div>
    <div style={{ padding: '13px 13px 12px' }}>
      <h3 style={{ margin: 0, color: T.navy, fontSize: 14, lineHeight: 1.32, fontWeight: 700, letterSpacing: 0 }}>
        {item.title}
      </h3>
      <p style={{ margin: '4px 0 12px', color: T.navyMid, fontSize: 11.5, lineHeight: 1.45, fontWeight: 450 }}>
        {item.desc}
      </p>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10 }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: 10, color: T.navyMid, fontSize: 11.5, fontWeight: 600 }}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5 }}>
            <Icon name="star" size={14} color="#f7c600" />
            {item.stars}
          </span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5 }}>
            <Icon name="heart" size={14} color="#ff5f8f" />
            {item.likes}
          </span>
        </div>
        <button
          onClick={() => onUse && onUse(item)}
          onMouseEnter={() => setButtonHover(true)}
          onMouseLeave={() => setButtonHover(false)}
          style={{
          height: 30,
          padding: '0 11px',
          borderRadius: 12,
          border: `1px solid ${buttonHover ? 'rgba(14,14,44,.16)' : T.hairlineSoft}`,
          background: buttonHover ? T.navy : 'rgba(246,248,251,.92)',
          color: buttonHover ? T.white : T.navyMid,
          display: 'inline-flex',
          alignItems: 'center',
          gap: 6,
          cursor: 'pointer',
          fontSize: 11.5,
          fontWeight: 620,
          boxShadow: buttonHover ? '0 10px 20px rgba(14,14,44,.12)' : 'inset 0 1px 0 rgba(255,255,255,.82)',
          transform: buttonHover ? 'translateY(-1px)' : 'translateY(0)',
          transition: `transform .24s ${T.spring}, background .2s ${T.ease}, color .2s ${T.ease}, box-shadow .24s ${T.spring}`,
        }}>
          使用
          <Icon name="arrowRight" size={13} />
        </button>
      </div>
    </div>
  </article>
  );
};

const InspirationDetailView = ({ item, onBack, onUse }) => {
  if (!item) return null;
  const prompt = `参考「${item.title}」的构图：保留真实店铺照片质感，标题放在画面下三分之一，整体更像上海饭店探店封面，少一点模板感。`;
  return (
    <section style={{
      width: '100%',
      maxWidth: 960,
      margin: '0 auto',
      borderRadius: 22,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.86)',
      boxShadow: '0 18px 42px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.86)',
      padding: 16,
      display: 'grid',
      gridTemplateColumns: 'minmax(220px, 320px) minmax(0, 1fr)',
      gap: 18,
    }}>
      <button onClick={onBack} style={{ position: 'absolute', opacity: 0, pointerEvents: 'none' }} />
      <div style={{ borderRadius: 18, overflow: 'hidden', background: T.surface, border: `1px solid ${T.hairlineSoft}` }}>
        <img src={item.image} alt="" style={{ width: '100%', aspectRatio: '1 / 1', objectFit: 'cover', display: 'block' }} />
      </div>
      <div style={{ display: 'grid', gap: 12, alignContent: 'start' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'flex-start' }}>
          <div>
            <div style={{ color: T.navyLight, fontSize: 11.5, fontWeight: 720, marginBottom: 6 }}>{item.category}</div>
            <h3 style={{ margin: 0, color: T.navy, fontSize: 22, lineHeight: 1.22, fontWeight: 760 }}>{item.title}</h3>
          </div>
          <button onClick={onBack} style={iconBtnStyle()}><Icon name="close" size={13} /></button>
        </div>
        <p style={{ margin: 0, color: T.navyMid, fontSize: 13.2, lineHeight: 1.72 }}>{item.desc}。适合提取封面构图、标题节奏和提示词结构。</p>
        <div style={{ display: 'grid', gap: 8 }}>
          {[
            ['标题', item.title],
            ['文案', '把场景说清楚，把决策成本降下来，让用户知道为什么现在就值得收藏。'],
            ['提示词', prompt],
          ].map(([label, value]) => (
            <div key={label} style={{ borderRadius: 14, background: 'rgba(250,252,254,.72)', border: `1px solid ${T.hairlineSoft}`, padding: 11 }}>
              <div style={{ color: T.navyLight, fontSize: 11.5, fontWeight: 700, marginBottom: 5 }}>{label}</div>
              <div style={{ color: T.navy, fontSize: 12.8, lineHeight: 1.62 }}>{value}</div>
            </div>
          ))}
        </div>
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button onClick={() => onUse?.({ item, prompt })} style={{ ...pillButtonStyle(true), height: 38, borderRadius: 13, fontSize: 13 }}>
            直接使用
            <Icon name="arrowRight" size={14} />
          </button>
        </div>
      </div>
    </section>
  );
};

const InspirationDiscovery = ({ mobile, compact, onUseInspiration }) => {
  const [category, setCategory] = React.useState('全部');
  const [search, setSearch] = React.useState('');
  const [usedTitle, setUsedTitle] = React.useState('');
  const [detail, setDetail] = React.useState(null);
  const categories = ['全部', '短视频', '图文', '推送文章', '漫剧', '其他'];
  const images = [
    './src/inspiration-skill-card.png',
    'https://images.unsplash.com/photo-1512290923902-8a9f81dc236c?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1524758631624-e2822e304c36?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1460317442991-0ec209397118?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1519052537078-e6302a4968d4?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1442512595331-e89e73853f31?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=900&q=80',
    'https://images.unsplash.com/photo-1518005020951-eccb494ad742?auto=format&fit=crop&w=900&q=80',
  ];
  const titles = ['美拉德美甲', '女性成长账号封面', 'AI 新闻速递', '城市生活提案', '产品种草模板', '咖啡馆内容策展', '品牌视觉灵感', '治愈系食谱', '主理人幕后手帐', '知识 IP 选题库', '猫咪栏目化日常', '咖啡入门卡片', '运动反差内容', '轻熟穿搭脚本', '建筑空间叙事'];
  const items = images.map((image, i) => ({
    image,
    title: titles[i],
    category: categories[(i % (categories.length - 1)) + 1],
    desc: i === 0 ? '一个有关手美甲如何拍照才好看的 skill' : ['封面、标题、脚本与分发建议一体生成', '适合做成账号长期栏目与内容资产', '从视觉参考提炼可复用的内容模板'][i % 3],
    stars: [500, 820, 640, 320, 980, 760, 440][i % 7],
    likes: [3200, 1860, 2480, 910, 4020, 1650, 2880][i % 7],
    ratio: ['1 / 1.02', '1 / 1.28', '1 / 0.92', '1 / 1.16', '1 / 0.78'][i % 5],
  }));
  const filtered = items.filter(item => category === '全部' || item.category === category)
    .filter(item => !search.trim() || `${item.title} ${item.desc} ${item.category}`.toLowerCase().includes(search.trim().toLowerCase()));

  if (detail) {
    return <InspirationDetailView item={detail} onBack={() => setDetail(null)} onUse={({ item, prompt }) => {
      setUsedTitle(item.title);
      setDetail(null);
      onUseInspiration?.({ item, prompt });
    }} />;
  }

  return (
    <section style={{
      width: '100%',
      maxWidth: mobile ? '100%' : compact ? 820 : 960,
      margin: '0 auto',
    }}>
      <div style={{
        display: 'flex',
        alignItems: mobile ? 'flex-start' : 'center',
        justifyContent: 'space-between',
        gap: 16,
        marginBottom: mobile ? 12 : 16,
        flexDirection: mobile ? 'column' : 'row',
      }}>
        <SectionTitle title="灵感发现" mobile={mobile} />
        <div style={{
          display: 'flex',
          gap: mobile ? 8 : 10,
          overflowX: 'auto',
          paddingBottom: mobile ? 4 : 0,
          maxWidth: '100%',
          alignItems: 'center',
          flexWrap: mobile ? 'wrap' : 'nowrap',
        }}>
          {categories.map((cat, i) => (
            <button key={cat} onClick={() => setCategory(cat)} style={{
              height: mobile ? 32 : 34,
              padding: '0 14px',
              borderRadius: 999,
              border: `1px solid ${category === cat ? 'transparent' : 'rgba(14,14,44,.08)'}`,
              background: category === cat ? T.navy : 'rgba(255,255,255,.72)',
              color: category === cat ? T.white : T.navyMid,
              fontSize: mobile ? 12 : 12.5,
              fontWeight: category === cat ? 700 : 580,
              cursor: 'pointer',
              whiteSpace: 'nowrap',
              boxShadow: category === cat ? '0 10px 20px rgba(14,14,44,.12)' : '0 5px 12px rgba(14,14,44,.03)',
            }}>
              {cat}
            </button>
          ))}
          <label style={{
            height: mobile ? 32 : 34,
            width: mobile ? '100%' : 176,
            borderRadius: 999,
            border: `1px solid ${T.hairlineSoft}`,
            background: 'rgba(255,255,255,.74)',
            display: 'inline-flex',
            alignItems: 'center',
            gap: 7,
            padding: '0 11px',
            color: T.navyLight,
            boxShadow: '0 5px 12px rgba(14,14,44,.03), inset 0 1px 0 rgba(255,255,255,.78)',
          }}>
            <Icon name="search" size={13} />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="搜索灵感"
              style={{ minWidth: 0, flex: 1, border: 'none', outline: 'none', background: 'transparent', color: T.navy, fontSize: 12.5, fontFamily: T.fontSans }}
            />
          </label>
        </div>
      </div>
      {usedTitle && <div style={{ margin: '-4px 0 10px', color: T.success, fontSize: 12, fontWeight: 650 }}>已套用灵感：{usedTitle}</div>}
      <div style={{
        columnCount: mobile ? 1 : compact ? 3 : 4,
        columnGap: mobile ? 14 : 16,
      }}>
        {filtered.map((item, i) => <InspirationCard key={`${item.title}-${i}`} item={item} index={i} onUse={(picked) => setDetail(picked)} />)}
      </div>
    </section>
  );
};

const SkillSquare = ({ compact, mobile }) => {
  const skills = [
    { name: '小红书爆款图文', author: '@Nori', uses: '12.4w', tint: '#f6eddc', accent: '#bd8e42', icon: 'image', desc: '标题、封面、内文一体生成，适合做种草和反差感主题。', cta: '立即套用' },
    { name: '公众号深度长文', author: '@Lina', uses: '8.6w', tint: '#edf1ff', accent: '#5f70d6', icon: 'document', desc: '更适合观点梳理、深度分析和可读性更强的长文结构。', cta: '查看模版' },
    { name: '抖音口播脚本', author: '@Theo', uses: '6.2w', tint: '#efe9ff', accent: '#8369da', icon: 'video', desc: '把观点拆成节奏点、转场和 hook，适配短视频传播。', cta: '生成脚本' },
    { name: '封面拆解师', author: '@Yuki', uses: '3.7w', tint: '#e8f4eb', accent: '#5f9d73', icon: 'palette', desc: '从视觉构图、标题布局和色彩关系拆出可复用规律。', cta: '打开分析' },
  ];

  if (mobile) {
    return (
      <section style={{
        background: 'rgba(255,255,255,.72)',
        border: `1px solid ${T.hairline}`,
        borderRadius: 24,
        padding: '18px 16px 18px',
        boxShadow: '0 18px 42px rgba(14,14,44,.05)',
      }}>
        <div style={{ marginBottom: 16 }}>
          <div style={{ fontSize: 12, color: T.navyLight, marginBottom: 6, letterSpacing: '0.08em', textTransform: 'uppercase' }}>Skill Gallery</div>
          <h3 style={{ fontSize: 22, fontWeight: 450, letterSpacing: '-0.04em', color: T.navy, lineHeight: 1.08 }}>Browse reusable creative systems</h3>
        </div>
        <div style={{ display: 'grid', gap: 12 }}>
          {skills.map((s, i) => (
            <div key={i} style={{ background: 'rgba(255,255,255,.88)', border: `1px solid ${T.hairline}`, borderRadius: 20, padding: 14 }}>
              <div style={{ height: 160, borderRadius: 18, background: `linear-gradient(160deg, rgba(255,255,255,.8), rgba(255,255,255,.2)), ${s.tint}`, padding: 16, marginBottom: 12, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                <div style={{ width: 38, height: 38, borderRadius: 12, background: 'rgba(255,255,255,.66)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: s.accent }}>
                  <Icon name={s.icon} size={18} />
                </div>
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '6px 10px', borderRadius: 999, background: 'rgba(255,255,255,.6)', color: s.accent, fontSize: 11, fontWeight: 600, alignSelf: 'flex-start' }}>
                  <Icon name="sparkles" size={10} color={s.accent} />
                  {s.uses}
                </div>
              </div>
              <div style={{ fontSize: 16, fontWeight: 600, color: T.navy, marginBottom: 6 }}>{s.name}</div>
              <div style={{ fontSize: 12.5, color: T.navyMid, lineHeight: 1.58, marginBottom: 10 }}>{s.desc}</div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <span style={{ fontSize: 11.5, color: T.navyLight }}>{s.author}</span>
                <button style={{ border: `1px solid ${T.hairline}`, background: T.white, borderRadius: 999, height: 32, padding: '0 12px', fontSize: 12, fontWeight: 600, color: T.navy, cursor: 'pointer' }}>{s.cta}</button>
              </div>
            </div>
          ))}
        </div>
      </section>
    );
  }

  return (
    <section style={{
      background: 'rgba(255,255,255,.72)',
      border: `1px solid ${T.hairline}`,
      borderRadius: 30,
      padding: compact ? '22px 20px 24px' : '24px 24px 26px',
      boxShadow: '0 18px 42px rgba(14,14,44,.05), inset 0 1px 0 rgba(255,255,255,.7)',
      backdropFilter: 'blur(18px)',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18, gap: 14, flexWrap: 'wrap' }}>
        <div>
          <div style={{ fontSize: 12, color: T.navyLight, marginBottom: 6, letterSpacing: '0.08em', textTransform: 'uppercase' }}>Skill Gallery</div>
          <h3 style={{ fontSize: compact ? 24 : 28, fontWeight: 450, lineHeight: 1.08, letterSpacing: '-0.04em', color: T.navy }}>
            Browse reusable creative systems
          </h3>
        </div>
        <a href="#" style={{
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
          boxShadow: T.shadowSm,
        }}>
          Browse the skill gallery
          <Icon name="arrowRight" size={14} />
        </a>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: compact ? 'repeat(2, minmax(0, 1fr))' : '1.35fr repeat(3, minmax(0, 1fr))',
        gap: 18,
        alignItems: 'start',
      }}>
        {skills.map((s, i) => {
          const featured = !compact && i === 0;
          return (
            <div key={i} style={{ gridColumn: featured ? 'span 1' : 'span 1' }}>
              <div
                style={{
                  background: 'transparent',
                  borderRadius: 24,
                  transition: 'transform .28s cubic-bezier(.2,.8,.2,1)',
                  cursor: 'pointer',
                }}
                onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-4px)'}
                onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}
              >
                <div style={{
                  height: featured ? 280 : compact ? 220 : 250,
                  borderRadius: 24,
                  background: `linear-gradient(160deg, rgba(255,255,255,.82), rgba(255,255,255,.18)), ${s.tint}`,
                  border: `1px solid rgba(14,14,44,.06)`,
                  boxShadow: '0 8px 22px rgba(14,14,44,.05)',
                  overflow: 'hidden',
                  padding: 18,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 10 }}>
                    <div style={{ width: 40, height: 40, borderRadius: 14, background: 'rgba(255,255,255,.66)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: s.accent }}>
                      <Icon name={s.icon} size={18} />
                    </div>
                    <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, padding: '7px 10px', borderRadius: 999, background: 'rgba(255,255,255,.58)', color: s.accent, fontSize: 11, fontWeight: 600 }}>
                      <Icon name="sparkles" size={10} color={s.accent} />
                      {s.uses}
                    </div>
                  </div>

                  <div style={{
                    alignSelf: featured ? 'stretch' : 'center',
                    height: featured ? 132 : 104,
                    borderRadius: 20,
                    background: 'rgba(255,255,255,.42)',
                    boxShadow: 'inset 0 0 0 1px rgba(255,255,255,.3)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: s.accent,
                  }}>
                    <Icon name={featured ? 'layers' : i % 2 === 0 ? 'document' : 'palette'} size={featured ? 42 : 34} />
                  </div>
                </div>

                <div style={{ padding: '14px 6px 0' }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10, marginBottom: 8 }}>
                    <div style={{ fontSize: featured ? 18 : 16, fontWeight: 600, color: T.navy, lineHeight: 1.2 }}>{s.name}</div>
                    {!featured && <span style={{ fontSize: 11.5, color: T.navyLight }}>{s.author}</span>}
                  </div>
                  <div style={{ fontSize: featured ? 13.5 : 12.5, color: T.navyMid, lineHeight: 1.58, marginBottom: 12 }}>{s.desc}</div>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10 }}>
                    {featured ? <span style={{ fontSize: 12, color: T.navyLight }}>{s.author}</span> : <span />}
                    <button style={{
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
                      gap: 6,
                    }}>
                      {s.cta}
                      <Icon name="arrowRight" size={12} />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

const HomeContentCalendar = ({ mobile, compact, onPick }) => {
  const calendar = [
    { day: '周一', date: '05/18', type: '图文', title: '第一次来店里，先点这 3 道招牌菜' },
    { day: '周二', date: '05/19', type: '短视频', title: '后厨备菜 30 秒，看看一碗饭怎么被认真做好' },
    { day: '周三', date: '05/20', type: '图文', title: '附近上班族午餐不踩雷菜单' },
    { day: '周四', date: '05/21', type: '长文', title: '一家小店怎么把回头客留住' },
    { day: '周五', date: '05/22', type: '短视频', title: '顾客最常问的 5 个问题' },
  ];
  return (
    <section style={{
      width: '100%',
      maxWidth: mobile ? '100%' : compact ? 820 : 960,
      margin: '0 auto',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 14, marginBottom: 16 }}>
        <SectionTitle title="内容日历" mobile={mobile} />
        <button style={{
          border: 'none',
          background: 'transparent',
          color: T.navyLight,
          cursor: 'pointer',
          display: 'inline-flex',
          alignItems: 'center',
          gap: 6,
          fontSize: 13,
          fontWeight: 620,
        }}>
          查看全部
          <Icon name="chevronRight" size={14} />
        </button>
      </div>
      <div style={{
        display: 'grid',
        gridTemplateColumns: mobile ? '1fr' : compact ? 'repeat(2, minmax(0, 1fr))' : 'repeat(5, minmax(0, 1fr))',
        gap: 14,
      }}>
        {calendar.map((item, index) => (
          <button
            key={`${item.day}-${index}`}
            onClick={() => onPick(`[内容日历 · ${item.type}] ${item.title}`)}
            style={{
              minHeight: mobile ? 132 : 158,
              borderRadius: 20,
              border: `1px solid ${index === 0 ? 'rgba(75,77,237,.18)' : T.hairlineSoft}`,
              background: index === 0 ? 'rgba(239,239,253,.60)' : 'rgba(255,255,255,.78)',
              boxShadow: index === 0 ? '0 16px 34px rgba(75,77,237,.08), inset 0 1px 0 rgba(255,255,255,.78)' : '0 10px 26px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.78)',
              padding: 16,
              cursor: 'pointer',
              textAlign: 'left',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              gap: 14,
              transition: `transform .28s ${T.spring}, box-shadow .28s ${T.spring}, border-color .22s ${T.ease}`,
            }}
            onMouseEnter={e => {
              e.currentTarget.style.transform = 'translateY(-3px)';
              e.currentTarget.style.boxShadow = '0 20px 44px rgba(14,14,44,.085), inset 0 1px 0 rgba(255,255,255,.82)';
            }}
            onMouseLeave={e => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = index === 0 ? '0 16px 34px rgba(75,77,237,.08), inset 0 1px 0 rgba(255,255,255,.78)' : '0 10px 26px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.78)';
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: 10, alignItems: 'flex-start' }}>
              <div>
                <div style={{ color: T.navy, fontSize: 14, fontWeight: 680 }}>{item.day}</div>
                <div style={{ marginTop: 4, color: T.navyLight, fontSize: 11.5, fontFamily: T.fontMono }}>{item.date}</div>
              </div>
              <span style={{
                height: 26,
                padding: '0 9px',
                borderRadius: 999,
                background: 'rgba(255,255,255,.78)',
                border: `1px solid ${T.hairlineSoft}`,
                color: index === 0 ? T.iris : T.navyLight,
                display: 'inline-flex',
                alignItems: 'center',
                fontSize: 11.5,
                fontWeight: 650,
              }}>{item.type}</span>
            </div>
            <div>
              <div style={{ color: T.navy, fontSize: 14.5, lineHeight: 1.5, fontWeight: 620 }}>{item.title}</div>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
};

const HomePage = ({ onSubmit, onOpenAssets, onOpenInsights, onOpenMine, onAccountPlan, accountPlanDraft, recentProject, onOpenProject, onOpenInspiration, focusInspirationKey }) => {
  const { isCompact, isTablet, isMobile } = useViewport();
  const [text, setText] = React.useState('');
  const [format, setFormat] = React.useState(null);
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [sleepMode, setSleepMode] = React.useState(false);
  const [sleepHelp, setSleepHelp] = React.useState(false);
  const inspirationRef = React.useRef(null);

  const submit = () => {
    if (text.trim()) {
      onSubmit(format ? `[${format.label} · ${format.sub}] ${text.trim()}` : text.trim());
    }
  };

  const sessions = [
    '猛男喜欢的粉色植物 · 小红书图文',
    '上海饭店推荐 · 小红书图文',
    '下班后小馆地图',
    '产品测评 · AI 视频工具横评',
    '极简通勤穿搭一周 OOTD',
    '咖啡入门 12 个名词',
    '我和我的猫 · 7 个瞬间',
  ];

  React.useEffect(() => {
    if (!focusInspirationKey) return;
    window.setTimeout(() => inspirationRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 120);
  }, [focusInspirationKey]);

  return (
    <div
      onClick={() => {
        if (sleepHelp) setSleepHelp(false);
      }}
      style={{
      display: 'flex',
      height: '100%',
      width: '100%',
      background: 'linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)',
      padding: 0,
    }}>
      <div style={{
        display: 'flex',
        flex: 1,
        background: 'transparent',
        borderRadius: 0,
        boxShadow: 'none',
        overflow: 'hidden',
      }}>
        {!isTablet && (
          <Sidebar
            active="home"
            onNew={() => {
              setNavCollapsed(true);
              onSubmit('');
            }}
            onNavigate={(id) => {
              if (id === 'home') return;
              if (id === 'library') onOpenAssets && onOpenAssets();
              if (id === 'insights') onOpenInsights && onOpenInsights();
              if (id === 'mine') onOpenMine && onOpenMine();
            }}
            sessions={sessions}
            collapsed={navCollapsed}
            onToggle={() => setNavCollapsed(v => !v)}
          />
        )}

        <main style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'auto',
          position: 'relative',
          background: 'linear-gradient(180deg, #FFFFFF 0%, #FBFCFE 52%, #F7F9FC 100%)',
        }}>
          <div style={{
            position: 'absolute',
            inset: 0,
            background: 'radial-gradient(circle at 50% 8%, rgba(214,255,0,.10), transparent 18%), radial-gradient(circle at 68% 18%, rgba(75,77,237,.045), transparent 22%), radial-gradient(circle at 72% 52%, rgba(49,208,170,.035), transparent 24%)',
            pointerEvents: 'none',
          }} />
          <div style={{
            height: isMobile ? 50 : 46,
            padding: isMobile ? '0 16px' : '0 22px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexShrink: 0,
            position: 'relative',
            zIndex: 1,
          }}>
            {isTablet ? (
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <NoriLogo size={26} />
                <div>
                  <div style={{ fontSize: 14, fontWeight: 720, color: T.navy, letterSpacing: 0 }}>Nori</div>
                  <div style={{ fontSize: 10.5, color: T.navyLight }}>creative system</div>
                </div>
              </div>
            ) : (
              <div aria-hidden="true" style={{ width: 38, height: 38 }} />
            )}

            <div style={{ display: 'flex', alignItems: 'center', gap: 8, position: 'relative' }}>
              <button
                onClick={e => {
                  e.stopPropagation();
                  setSleepMode(v => !v);
                  setSleepHelp(v => !v);
                }}
                style={{
                  height: 36,
                  borderRadius: 14,
                  border: `1px solid ${sleepMode ? 'rgba(75,77,237,.18)' : T.hairlineSoft}`,
                  background: sleepMode ? 'rgba(239,239,253,.92)' : 'rgba(255,255,255,.74)',
                  color: sleepMode ? T.iris : T.navyMid,
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 9,
                  padding: isMobile ? '0 10px' : '0 12px',
                  cursor: 'pointer',
                  boxShadow: sleepMode ? '0 10px 24px rgba(75,77,237,.10), inset 0 1px 0 rgba(255,255,255,.78)' : '0 6px 16px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.78)',
                  backdropFilter: 'blur(16px) saturate(1.18)',
                  transition: `background .22s ${T.ease}, border-color .22s ${T.ease}, color .22s ${T.ease}, box-shadow .24s ${T.ease}`,
                }}
                aria-pressed={sleepMode}
                aria-label="睡眠模式"
              >
                <Icon name="moon" size={14} color="currentColor" />
                {!isMobile && <span style={{ fontSize: 12.5, fontWeight: 700 }}>睡眠模式</span>}
                <span style={{
                  width: 30,
                  height: 18,
                  borderRadius: 999,
                  background: sleepMode ? T.iris : 'rgba(14,14,44,.12)',
                  padding: 2,
                  display: 'inline-flex',
                  justifyContent: sleepMode ? 'flex-end' : 'flex-start',
                  flexShrink: 0,
                }}>
                  <span style={{ width: 13, height: 13, borderRadius: '50%', background: T.white, boxShadow: '0 1px 3px rgba(14,14,44,.18)' }} />
                </span>
              </button>
              {sleepHelp && (
                <div
                  onClick={e => e.stopPropagation()}
                  style={{
                  position: 'absolute',
                  right: 78,
                  top: 44,
                  width: isMobile ? 260 : 318,
                  padding: 14,
                  borderRadius: 18,
                  border: `1px solid ${T.hairlineSoft}`,
                  background: 'rgba(255,255,255,.94)',
                  boxShadow: '0 18px 44px rgba(14,14,44,.12), inset 0 1px 0 rgba(255,255,255,.82)',
                  color: T.navyMid,
                  fontSize: 12.8,
                  lineHeight: 1.65,
                  zIndex: 20,
                }}>
                  <div style={{ color: T.navy, fontSize: 13.2, fontWeight: 760, marginBottom: 6 }}>睡眠模式</div>
                  开启后，Nori 会在你休息时持续学习爆款内容、整理可复用 Skill，并在第二天把可用的选题和结构放进创作建议。
                </div>
              )}
              <button style={iconBtnStyle()}><Icon name="bell" size={15} color={T.navyLight} /></button>
              <button style={iconBtnStyle()}><Icon name="settings" size={15} color={T.navyLight} /></button>
            </div>
          </div>

          <div style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-start',
            maxWidth: isMobile ? '100%' : 1220,
            width: '100%',
            margin: '0 auto',
            padding: isMobile ? '14px 18px 36px' : isTablet ? '28px 46px 60px' : '44px 84px 78px',
            gap: isMobile ? 34 : 62,
            position: 'relative',
            zIndex: 1,
          }}>
            <section style={{
              position: 'relative',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              padding: isMobile ? '10px 0 0' : '24px 0 0',
            }}>
              <HeroHeadline compact={isCompact} mobile={isMobile} />

              <div style={{ width: '100%', maxWidth: isMobile ? '100%' : 820 }}>
                <HomeIpModeBar
                  mobile={isMobile}
                  onAccountPlan={onAccountPlan}
                  onViewProfile={onOpenMine}
                  planned={!!accountPlanDraft}
                />
                <HomeComposer
                  value={text}
                  onChange={setText}
                  onSubmit={submit}
                  format={format}
                  onClearFormat={() => setFormat(null)}
                  compact={isCompact}
                  mobile={isMobile}
                />
                <div style={{ marginTop: 14, display: 'flex', justifyContent: 'center' }}>
                  <FormatPicker format={format} onPick={setFormat} compact={isCompact} mobile={isMobile} />
                </div>
              </div>
            </section>

            <HomeContentCalendar mobile={isMobile} compact={isCompact} onPick={onSubmit} />

            <div ref={inspirationRef}>
              <InspirationDiscovery mobile={isMobile} compact={isCompact} onUseInspiration={onOpenInspiration} />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

const iconBtnStyle = () => ({
  width: 34,
  height: 34,
  borderRadius: 12,
  border: `1px solid ${T.hairlineSoft}`,
  background: 'rgba(255,255,255,.74)',
  cursor: 'pointer',
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  transition: `transform .28s ${T.spring}, box-shadow .28s ${T.spring}, background .22s ${T.ease}`,
  boxShadow: '0 6px 16px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.78)',
  backdropFilter: 'blur(16px) saturate(1.18)',
});

window.HomePage = HomePage;
window.Sidebar = Sidebar;
window.iconBtnStyle = iconBtnStyle;

/* ─── Assets Page: saved content library ─── */

const ASSET_ITEMS = [
  {
    id: 'pink-plants',
    title: '深蓝幕布下的粉蝶兰，谁懂这种反差感？',
    platform: '小红书',
    type: '图文',
    time: '今天 21:18',
    status: '已生成',
    height: 214,
    palette: ['#103f5f', '#1d6f58', '#f4a8bf', '#de7fa3', '#fff8fb'],
    tags: ['粉色植物', '室内绿植'],
  },
  {
    id: 'coffee-walk',
    title: '上海咖啡馆 City Walk Top 10 路线',
    platform: '小红书',
    type: '视频',
    time: '昨天 18:42',
    status: '草稿',
    height: 258,
    palette: ['#d9d0bd', '#7c6b58', '#f3e7d7', '#a47758', '#fffaf2'],
    tags: ['城市漫步', '咖啡馆'],
  },
  {
    id: 'rental-guide',
    title: '租房避雷指南：看房前必须问清楚的 18 件事',
    platform: '公众号',
    type: '纯文字',
    time: '5 月 5 日',
    status: '已发布',
    height: 184,
    palette: ['#f7f9fc', '#d7e0eb', '#4b4ded', '#31d0aa', '#0e0e2c'],
    tags: ['生活经验', '清单'],
  },
  {
    id: 'ai-video-tools',
    title: 'AI 视频工具横评：从脚本到成片的真实体验',
    platform: 'B站',
    type: '视频',
    time: '5 月 4 日',
    status: '已生成',
    height: 244,
    palette: ['#20284a', '#5c66a8', '#f3dbda', '#d6ff00', '#ffffff'],
    tags: ['AI工具', '测评'],
  },
  {
    id: 'ootd',
    title: '极简通勤穿搭一周 OOTD',
    platform: '短视频',
    type: '视频',
    time: '5 月 3 日',
    status: '草稿',
    height: 268,
    palette: ['#e8ebee', '#1d2330', '#b8c2cb', '#f3dbda', '#ffffff'],
    tags: ['穿搭', '通勤'],
  },
  {
    id: 'coffee-terms',
    title: '咖啡入门 12 个名词，一次讲清楚',
    platform: '公众号',
    type: '纯文字',
    time: '5 月 2 日',
    status: '已生成',
    height: 178,
    palette: ['#fffaf2', '#efe1cc', '#8a6545', '#31d0aa', '#0e0e2c'],
    tags: ['知识科普', '咖啡'],
  },
  {
    id: 'cat-moments',
    title: '我和我的猫：7 个适合发图文的生活瞬间',
    platform: '小红书',
    type: '图文',
    time: '4 月 29 日',
    status: '已发布',
    height: 222,
    palette: ['#fdf5f5', '#95a5a6', '#f0b5c8', '#4b4ded', '#ffffff'],
    tags: ['生活记录', '宠物'],
  },
  {
    id: 'product-manager',
    title: '2026 年 AI 产品经理必备能力地图',
    platform: '公众号',
    type: '图文',
    time: '4 月 26 日',
    status: '已生成',
    height: 202,
    palette: ['#ecf1f4', '#c8d8e6', '#4b4ded', '#d6ff00', '#0e0e2c'],
    tags: ['职场', 'AI'],
  },
  {
    id: 'launch-copy',
    title: '新品发布文案：从预热到转化的 5 个版本',
    platform: '小红书',
    type: '纯文字',
    time: '4 月 22 日',
    status: '草稿',
    height: 188,
    palette: ['#ffffff', '#efeefd', '#4b4ded', '#f3dbda', '#0e0e2c'],
    tags: ['营销文案', '发布'],
  },
];

const AssetVisual = ({ item }) => {
  if (item.type === '纯文字') {
    return (
      <div style={{
        height: 178,
        padding: 14,
        background: `linear-gradient(145deg, ${item.palette[0]}, ${item.palette[1]})`,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
      }}>
        <div style={{
          width: 30,
          height: 30,
          borderRadius: 10,
          background: 'rgba(255,255,255,.82)',
          color: item.palette[2],
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: 'inset 0 1px 0 rgba(255,255,255,.72)',
        }}>
          <Icon name="document" size={13} />
        </div>
        <div>
          <div style={{ fontSize: 16.5, lineHeight: 1.24, fontWeight: 740, color: T.navy, letterSpacing: 0 }}>{item.title}</div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ height: 178, position: 'relative', overflow: 'hidden', background: item.palette[0] }}>
      <FlowerVisual palette={item.palette} />
      <div style={{
        position: 'absolute',
        inset: 0,
        background: item.type === '视频'
          ? 'linear-gradient(180deg, rgba(0,0,0,.02), rgba(0,0,0,.44))'
          : 'linear-gradient(180deg, rgba(255,255,255,.04), rgba(0,0,0,.32))',
      }} />
      {item.type === '视频' && (
        <div style={{
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
          backdropFilter: 'blur(10px)',
        }}>
          <Icon name="play" size={12} />
        </div>
      )}
      <div style={{
        position: 'absolute',
        left: 13,
        right: 13,
        bottom: 13,
        color: T.white,
      }}>
        <div style={{ fontSize: 16.5, lineHeight: 1.18, fontWeight: 760, letterSpacing: 0, textShadow: '0 2px 10px rgba(0,0,0,.24)' }}>
          {item.title}
        </div>
      </div>
    </div>
  );
};

const assetStatusTone = (status) => {
  if (status === '已发布') return { bg: T.successTint, fg: T.success };
  if (status === '草稿') return { bg: T.irisTint, fg: T.iris };
  return { bg: T.primaryTint, fg: T.navy };
};

const FilterChip = ({ active, children, onClick, count }) => (
  <button
    onClick={onClick}
    style={{
      height: 34,
      padding: '0 12px',
      borderRadius: 12,
      border: `1px solid ${active ? 'rgba(75,77,237,.16)' : T.hairlineSoft}`,
      background: active ? T.irisTint : 'rgba(255,255,255,.76)',
      color: active ? T.iris : T.navyMid,
      boxShadow: active ? '0 7px 18px rgba(75,77,237,.08), inset 0 1px 0 rgba(255,255,255,.78)' : 'none',
      cursor: 'pointer',
      fontSize: 12.5,
      fontWeight: 700,
      display: 'inline-flex',
      alignItems: 'center',
      gap: 7,
      transition: `transform .28s ${T.spring}, background .22s ${T.ease}, box-shadow .28s ${T.spring}, color .22s ${T.ease}`,
    }}
    onMouseEnter={e => {
      e.currentTarget.style.transform = 'translateY(-1px)';
      e.currentTarget.style.boxShadow = active ? T.shadowSm : T.shadowXs;
    }}
    onMouseLeave={e => {
      e.currentTarget.style.transform = 'translateY(0)';
      e.currentTarget.style.boxShadow = active ? 'inset 0 1px 0 rgba(255,255,255,.78)' : 'none';
    }}
  >
    {children}
    {typeof count === 'number' && <span style={{
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
      fontFamily: T.fontMono,
    }}>{count}</span>}
  </button>
);

const AssetCard = ({ item, index, onOpen }) => (
    <article
      onClick={() => onOpen(item)}
      style={{
        breakInside: 'avoid',
        marginBottom: 14,
        borderRadius: 16,
        overflow: 'hidden',
        minHeight: 286,
        background: 'rgba(255,255,255,.86)',
        border: `1px solid ${T.hairlineSoft}`,
        boxShadow: '0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)',
        cursor: 'pointer',
        position: 'relative',
        animation: `fadeInScale .5s ${index * 48}ms ${T.spring} both`,
        transition: `transform .34s ${T.spring}, box-shadow .34s ${T.spring}`,
      }}
      onMouseEnter={e => {
        e.currentTarget.style.transform = 'translateY(-3px)';
        e.currentTarget.style.boxShadow = '0 16px 38px rgba(14,14,44,.095), inset 0 1px 0 rgba(255,255,255,.76)';
      }}
      onMouseLeave={e => {
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = '0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)';
      }}
    >
      <AssetVisual item={item} />
      <div style={{ padding: '10px 12px 11px' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10 }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 7, minWidth: 0 }}>
            <PlatformLogo kind={item.platform === '小红书' ? 'xhs' : item.platform === 'B站' ? 'bili' : item.platform === '短视频' ? 'dy' : 'wechat'} size={19} />
            <span style={{ color: T.navy, fontSize: 13, lineHeight: 1.2, fontWeight: 720, whiteSpace: 'nowrap' }}>{item.platform}</span>
          </div>
          <span style={{
            height: 24,
            padding: '0 9px',
            borderRadius: 999,
            background: assetStatusTone(item.status).bg,
            color: assetStatusTone(item.status).fg,
            fontSize: 11.5,
            fontWeight: 760,
            display: 'inline-flex',
            alignItems: 'center',
            flexShrink: 0,
          }}>{item.status}</span>
        </div>
        <div style={{
          marginTop: 8,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 10,
          color: T.navyLight,
          fontSize: 12.2,
          lineHeight: 1.35,
        }}>
          <span>{item.time}</span>
        </div>
      </div>
    </article>
);

const AssetsPage = ({ onOpenAsset, onBackHome, onOpenInsights, onOpenMine, onNewChat }) => {
  const { width, isTablet, isMobile } = useViewport();
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [query, setQuery] = React.useState('');
  const [platform, setPlatform] = React.useState('全部');
  const [type, setType] = React.useState('全部');
  const [sort, setSort] = React.useState('最新');
  const columnCount = isMobile
    ? 1
    : isTablet
      ? 2
      : Math.min(6, Math.max(4, Math.floor((width - (navCollapsed ? 132 : 292)) / 214)));

  const sessions = ASSET_ITEMS.slice(0, 6).map(item => item.title);
  const filtered = ASSET_ITEMS
    .filter(item => platform === '全部' || item.platform === platform)
    .filter(item => type === '全部' || item.type === type)
    .filter(item => !query.trim() || `${item.title} ${item.platform} ${item.type} ${item.tags.join(' ')}`.toLowerCase().includes(query.trim().toLowerCase()));

  const sorted = sort === '最早' ? [...filtered].reverse() : filtered;
  const platforms = ['全部', '小红书', '公众号', 'B站', '短视频'];
  const types = ['全部', '图文', '视频', '纯文字'];

  return (
    <div style={{ display: 'flex', width: '100%', height: '100%', background: T.surfaceWh, overflow: 'hidden' }}>
      {!isTablet && (
        <Sidebar
          active="library"
          onNew={onNewChat}
          onNavigate={(id) => {
            if (id === 'home') onBackHome();
            if (id === 'insights') onOpenInsights && onOpenInsights();
            if (id === 'mine') onOpenMine && onOpenMine();
          }}
          sessions={sessions}
          collapsed={navCollapsed}
          onToggle={() => setNavCollapsed(v => !v)}
        />
      )}

      <main style={{
        flex: 1,
        minWidth: 0,
        overflow: 'auto',
        background: 'linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)',
        position: 'relative',
      }}>
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(circle at 18% 12%, rgba(214,255,0,.16), transparent 18%), radial-gradient(circle at 86% 10%, rgba(75,77,237,.08), transparent 22%), radial-gradient(circle at 64% 72%, rgba(49,208,170,.07), transparent 22%)',
          pointerEvents: 'none',
        }} />
        <div style={{ position: 'relative', zIndex: 1, maxWidth: 1640, margin: '0 auto', padding: isMobile ? '18px 18px 36px' : '28px 30px 50px' }}>
          {isTablet && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <NoriLogo size={28} />
                <div>
                  <div style={{ fontSize: 15, fontWeight: 760, color: T.navy }}>我的内容库</div>
                  <div style={{ fontSize: 11, color: T.navyLight }}>自动保存的创作资产</div>
                </div>
              </div>
              <button onClick={onBackHome} style={iconBtnStyle()}><Icon name="home" size={16} color={T.navyMid} /></button>
            </div>
          )}

          <header style={{
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'space-between',
            gap: 22,
            marginBottom: 24,
            flexWrap: 'wrap',
          }}>
            <div>
              <div style={{ fontSize: 12, fontWeight: 800, letterSpacing: '0.08em', textTransform: 'uppercase', color: T.navyLight, marginBottom: 8 }}>
                Assets
              </div>
              <h1 style={{ margin: 0, fontSize: isMobile ? 28 : 38, lineHeight: 1.08, letterSpacing: 0, color: T.navy, fontWeight: 760 }}>
                我的内容库
              </h1>
              <p style={{ margin: '10px 0 0', fontSize: 13.5, lineHeight: 1.6, color: T.navyMid }}>
                生成过的图文、视频和文案会自动保存，随时查看、编辑、重新发布或转换形态。
              </p>
            </div>

            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              flexWrap: 'wrap',
              justifyContent: isMobile ? 'flex-start' : 'flex-end',
              width: isMobile ? '100%' : 'auto',
            }}>
              <div style={{
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
                backdropFilter: 'blur(18px)',
              }}>
                <Icon name="search" size={17} color={T.navyLight} />
                <input
                  value={query}
                  onChange={e => setQuery(e.target.value)}
                  placeholder="搜索内容资产..."
                  style={{
                    flex: 1,
                    border: 'none',
                    outline: 'none',
                    background: 'transparent',
                    color: T.navy,
                    fontSize: 14,
                    fontFamily: T.fontSans,
                  }}
                />
              </div>
              <button
                onClick={() => setSort(s => s === '最新' ? '最早' : '最新')}
                style={{
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
                  fontWeight: 740,
                }}
              >
                <Icon name="list" size={16} color={T.navyMid} />
                {sort}
              </button>
            </div>
          </header>

          <section style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: 12,
            flexWrap: 'wrap',
            paddingBottom: 18,
            borderBottom: `1px solid ${T.hairlineSoft}`,
            marginBottom: 24,
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
              {platforms.map(p => (
                <FilterChip
                  key={p}
                  active={platform === p}
                  onClick={() => setPlatform(p)}
                  count={p === '全部' ? ASSET_ITEMS.length : ASSET_ITEMS.filter(item => item.platform === p).length}
                >
                  {p}
                </FilterChip>
              ))}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
              {types.map(t => (
                <FilterChip
                  key={t}
                  active={type === t}
                  onClick={() => setType(t)}
                >
                  {t}
                </FilterChip>
              ))}
            </div>
          </section>

          <section style={{
            columnCount,
            columnGap: 14,
          }}>
            {sorted.map((item, index) => (
              <AssetCard key={item.id} item={item} index={index} onOpen={onOpenAsset} />
            ))}
          </section>

          {sorted.length === 0 && (
            <div style={{
              minHeight: 280,
              borderRadius: 22,
              border: `1px solid ${T.hairlineSoft}`,
              background: 'rgba(255,255,255,.72)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: T.navyLight,
              fontSize: 13.5,
              boxShadow: T.shadowXs,
            }}>
              没有找到匹配的内容资产
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

window.AssetsPage = AssetsPage;

/* ─── Skill Plaza ─── */

const SKILL_ITEMS = [
  {
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
    result: ['3 组标题方向', '封面视觉脚本', '正文 6 段结构', '发布标签'],
  },
  {
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
    result: ['文章大纲', '完整长文', '小标题优化', '结尾 CTA'],
  },
  {
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
    result: ['口播稿', '分镜节奏', '字幕重点', '封面标题'],
  },
  {
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
    result: ['对比维度', '优缺点', '推荐排序', '购买建议'],
  },
  {
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
    result: ['故事钩子', '个人观点', '标题组', '互动问题'],
  },
  {
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
    result: ['发布节奏', '内容主题', '文案方向', '复盘指标'],
  },
  {
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
    result: ['卡片大纲', '重点句', '视觉建议', '总结页'],
  },
  {
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
    result: ['案例结构', '复盘问题', '结果表达', '经验提炼'],
  },
];

const SkillArtwork = ({ skill, compact = false }) => (
  <div style={{
    height: compact ? 'auto' : skill.height,
    aspectRatio: compact ? '1 / 1' : 'auto',
    position: 'relative',
    overflow: 'hidden',
    background: `linear-gradient(145deg, ${skill.palette[0]}, ${skill.palette[1]})`,
    borderRadius: compact ? 18 : 0,
  }}>
    <div style={{
      position: 'absolute',
      inset: 0,
      background: 'radial-gradient(circle at 26% 20%, rgba(255,255,255,.72), transparent 24%), radial-gradient(circle at 80% 14%, rgba(255,255,255,.34), transparent 22%), radial-gradient(circle at 72% 78%, rgba(14,14,44,.10), transparent 30%)',
    }} />
    <div style={{
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
      backdropFilter: 'blur(14px)',
    }}>
      <Icon name={skill.type === '短视频' ? 'video' : skill.type === '公众号长文' ? 'document' : 'image'} size={18} />
    </div>
    <div style={{
      position: 'absolute',
      right: -28,
      top: 40,
      width: 130,
      height: 130,
      borderRadius: 42,
      transform: 'rotate(14deg)',
      background: `linear-gradient(135deg, ${skill.palette[2]}, ${skill.palette[3]})`,
      opacity: .92,
      boxShadow: '0 24px 52px rgba(14,14,44,.16)',
    }} />
    <div style={{
      position: 'absolute',
      left: 18,
      right: 18,
      bottom: 18,
    }}>
      <div style={{
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
        marginBottom: 10,
      }}>{skill.type}</div>
      <div style={{ fontSize: 21, lineHeight: 1.14, fontWeight: 780, color: T.navy, letterSpacing: 0 }}>
        {skill.title}
      </div>
    </div>
  </div>
);
const SkillCard = ({ skill, index, onOpen }) => (
  <article
    onClick={() => onOpen(skill)}
    style={{
      width: '100%',
      borderRadius: 22,
      overflow: 'hidden',
      background: 'rgba(255,255,255,.86)',
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: '0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)',
      cursor: 'pointer',
      animation: `fadeInScale .5s ${index * 48}ms ${T.spring} both`,
      transition: `transform .34s ${T.spring}, box-shadow .34s ${T.spring}, border-color .24s ${T.ease}, background .24s ${T.ease}`,
      display: 'grid',
      gridTemplateColumns: 'minmax(132px, 180px) minmax(0, 1fr)',
      gap: 18,
      padding: 14,
      alignItems: 'stretch',
    }}
    onMouseEnter={e => {
      e.currentTarget.style.transform = 'translateY(-5px) scale(1.006)';
      e.currentTarget.style.boxShadow = '0 24px 58px rgba(14,14,44,.13), inset 0 1px 0 rgba(255,255,255,.78)';
      e.currentTarget.style.borderColor = 'rgba(75,77,237,.18)';
      e.currentTarget.style.background = 'rgba(255,255,255,.94)';
    }}
    onMouseLeave={e => {
      e.currentTarget.style.transform = 'translateY(0) scale(1)';
      e.currentTarget.style.boxShadow = '0 10px 26px rgba(14,14,44,.062), inset 0 1px 0 rgba(255,255,255,.72)';
      e.currentTarget.style.borderColor = T.hairlineSoft;
      e.currentTarget.style.background = 'rgba(255,255,255,.86)';
    }}
  >
    <SkillArtwork skill={skill} compact />
    <div style={{ padding: '4px 8px 4px 0', display: 'flex', flexDirection: 'column', minWidth: 0 }}>
      <div style={{
        fontSize: 18,
        lineHeight: 1.32,
        fontWeight: 740,
        color: T.navy,
        letterSpacing: 0,
      }}>{skill.title}</div>
      <div style={{ marginTop: 9, color: T.navyMid, fontSize: 13.2, lineHeight: 1.68, fontWeight: 450 }}>
        {skill.desc}
      </div>
      <div style={{ marginTop: 14, display: 'flex', gap: 7, flexWrap: 'wrap' }}>
        {skill.result.slice(0, 3).map(item => (
          <span key={item} style={{
            height: 28,
            padding: '0 9px',
            borderRadius: 999,
            background: 'rgba(250,252,254,.78)',
            border: `1px solid ${T.hairlineSoft}`,
            color: T.navyLight,
            display: 'inline-flex',
            alignItems: 'center',
            fontSize: 11.2,
            fontWeight: 640,
          }}>{item}</span>
        ))}
      </div>
      <div style={{ marginTop: 'auto', paddingTop: 15, display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12 }}>
        <span style={{ fontSize: 11.5, color: T.navyLight, fontFamily: T.fontMono }}>{skill.uses} uses</span>
        <span style={{
          height: 30,
          padding: '0 10px',
          borderRadius: 999,
          background: skill.tint,
          color: skill.accent === T.primary ? T.navy : skill.accent,
          display: 'inline-flex',
          alignItems: 'center',
          gap: 5,
          fontSize: 11.2,
          fontWeight: 760,
        }}>
          <Icon name="sparkles" size={10} />
          Skill
        </span>
      </div>
    </div>
  </article>
);

const SkillDetail = ({ skill, onBack, onUse }) => (
  <div style={{ maxWidth: 980, margin: '0 auto', animation: 'fadeInScale .28s ease both' }}>
    <button
      onClick={onBack}
      style={{
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
        marginBottom: 18,
      }}
    >
      <Icon name="chevronLeft" size={14} />
      返回 Skill 广场
    </button>
    <section style={{
      display: 'grid',
      gridTemplateColumns: 'minmax(0, .95fr) minmax(320px, 1.05fr)',
      gap: 24,
      alignItems: 'stretch',
    }}>
      <div style={{
        borderRadius: 26,
        overflow: 'hidden',
        border: `1px solid ${T.hairlineSoft}`,
        boxShadow: T.shadowLg,
        background: T.white,
      }}>
        <SkillArtwork skill={{ ...skill, height: 520 }} />
      </div>
      <div style={{
        borderRadius: 26,
        border: `1px solid ${T.hairlineSoft}`,
        background: 'rgba(255,255,255,.84)',
        boxShadow: '0 18px 44px rgba(14,14,44,.08), inset 0 1px 0 rgba(255,255,255,.78)',
        padding: 28,
        display: 'flex',
        flexDirection: 'column',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 18, flexWrap: 'wrap' }}>
          <span style={{ height: 28, padding: '0 10px', borderRadius: 999, background: skill.tint, color: skill.accent === T.primary ? T.navy : skill.accent, display: 'inline-flex', alignItems: 'center', fontSize: 11.5, fontWeight: 780 }}>{skill.type}</span>
          <span style={{ height: 28, padding: '0 10px', borderRadius: 999, background: T.surface, color: T.navyLight, display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 11.5, fontFamily: T.fontMono }}>
            <Icon name="sparkles" size={11} />
            {skill.uses} uses
          </span>
        </div>
        <h1 style={{ margin: 0, fontSize: 38, lineHeight: 1.08, fontWeight: 780, letterSpacing: 0, color: T.navy }}>
          {skill.title}
        </h1>
        <p style={{ margin: '18px 0 24px', color: T.navyMid, fontSize: 14.5, lineHeight: 1.8 }}>
          {skill.desc}
        </p>
        <div style={{ display: 'grid', gap: 10, marginBottom: 24 }}>
          {skill.result.map((item, i) => (
            <div key={item} style={{
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              minHeight: 42,
              padding: '8px 12px',
              borderRadius: 14,
              background: 'rgba(250,252,254,.82)',
              border: `1px solid ${T.hairlineSoft}`,
            }}>
              <span style={{ width: 24, height: 24, borderRadius: 9, background: i === 0 ? T.primary : skill.tint, color: i === 0 ? T.navy : skill.accent, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: 10.5, fontFamily: T.fontMono, fontWeight: 800 }}>
                {String(i + 1).padStart(2, '0')}
              </span>
              <span style={{ fontSize: 13, fontWeight: 680, color: T.navy }}>{item}</span>
            </div>
          ))}
        </div>
        <div style={{
          marginTop: 'auto',
          padding: 16,
          borderRadius: 18,
          background: `linear-gradient(135deg, ${T.primaryTint}, ${skill.tint})`,
          border: `1px solid ${T.hairlineSoft}`,
        }}>
          <div style={{ fontSize: 12, color: T.navyMid, lineHeight: 1.65, marginBottom: 14 }}>
            使用后会自动把 Skill 模板填入生成页输入框，并等待你补充具体主题。
          </div>
          <button
            onClick={() => onUse(skill)}
            style={{
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
              boxShadow: '0 14px 28px rgba(14,14,44,.18)',
            }}
          >
            <Icon name="sparkles" size={16} />
            使用 Skill
          </button>
        </div>
      </div>
    </section>
  </div>
);

const SkillsPage = ({ onBackHome, onOpenAssets, onOpenInsights, onNewChat, onUseSkill }) => {
  const { width, isTablet, isMobile } = useViewport();
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [scope, setScope] = React.useState('community');
  const [type, setType] = React.useState('全部');
  const [query, setQuery] = React.useState('');
  const [selected, setSelected] = React.useState(null);
  const sessions = SKILL_ITEMS.slice(0, 6).map(item => item.title);
  const types = ['全部', '小红书图文', '公众号长文', '短视频'];
  const filtered = SKILL_ITEMS
    .filter(skill => skill.owner === scope)
    .filter(skill => type === '全部' || skill.type === type)
    .filter(skill => !query.trim() || `${skill.title} ${skill.type} ${skill.desc}`.toLowerCase().includes(query.trim().toLowerCase()));

  return (
    <div style={{ display: 'flex', width: '100%', height: '100%', background: T.surfaceWh, overflow: 'hidden' }}>
      {!isTablet && (
        <Sidebar
          active="skills"
          onNew={onNewChat}
          onNavigate={(id) => {
            if (id === 'home') onBackHome();
            if (id === 'library') onOpenAssets();
            if (id === 'skills') setSelected(null);
            if (id === 'insights') onOpenInsights && onOpenInsights();
          }}
          sessions={sessions}
          collapsed={navCollapsed}
          onToggle={() => setNavCollapsed(v => !v)}
        />
      )}
      <main style={{
        flex: 1,
        minWidth: 0,
        overflow: 'auto',
        background: 'linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)',
        position: 'relative',
      }}>
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(circle at 48% 8%, rgba(214,255,0,.18), transparent 18%), radial-gradient(circle at 76% 12%, rgba(75,77,237,.075), transparent 22%), radial-gradient(circle at 23% 65%, rgba(243,217,218,.20), transparent 22%)',
          pointerEvents: 'none',
        }} />
        <div style={{ position: 'relative', zIndex: 1, maxWidth: 1640, margin: '0 auto', padding: isMobile ? '18px 18px 36px' : '28px 30px 50px' }}>
          {selected ? (
            <SkillDetail skill={selected} onBack={() => setSelected(null)} onUse={onUseSkill} />
          ) : (
            <>
              {isTablet && (
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <NoriLogo size={28} />
                    <div>
                      <div style={{ fontSize: 15, fontWeight: 760, color: T.navy }}>Skill 广场</div>
                      <div style={{ fontSize: 11, color: T.navyLight }}>可复用创作系统</div>
                    </div>
                  </div>
                  <button onClick={onBackHome} style={iconBtnStyle()}><Icon name="home" size={16} color={T.navyMid} /></button>
                </div>
              )}

              <header style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', gap: 20, marginBottom: 24, flexWrap: 'wrap' }}>
                <div>
                  <div style={{ fontSize: 12, fontWeight: 800, letterSpacing: '0.08em', textTransform: 'uppercase', color: T.navyLight, marginBottom: 8 }}>
                    Skill Plaza
                  </div>
                  <h1 style={{ margin: 0, fontSize: isMobile ? 28 : 38, lineHeight: 1.08, letterSpacing: 0, color: T.navy, fontWeight: 760 }}>
                    Skill 广场
                  </h1>
                  <p style={{ margin: '10px 0 0', fontSize: 13.5, lineHeight: 1.6, color: T.navyMid }}>
                    选择一个可复用的创作系统，让 Nori 按指定结构开始生成。
                  </p>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap', justifyContent: isMobile ? 'flex-start' : 'flex-end' }}>
                  <label style={{
                    height: 46,
                    minWidth: isMobile ? '100%' : 260,
                    borderRadius: 17,
                    border: `1px solid ${T.hairlineSoft}`,
                    background: 'rgba(255,255,255,.82)',
                    boxShadow: '0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.78)',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 10,
                    padding: '0 14px',
                    color: T.navyLight,
                  }}>
                    <Icon name="search" size={16} />
                    <input
                      value={query}
                      onChange={e => setQuery(e.target.value)}
                      placeholder="搜索 Skill..."
                      style={{ flex: 1, minWidth: 0, border: 'none', outline: 'none', background: 'transparent', color: T.navy, fontSize: 13.5, fontFamily: T.fontSans }}
                    />
                  </label>
                  <div style={{
                    height: 46,
                    padding: 4,
                    borderRadius: 17,
                    border: `1px solid ${T.hairlineSoft}`,
                    background: 'rgba(255,255,255,.82)',
                    boxShadow: '0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.78)',
                    display: 'inline-flex',
                    gap: 4,
                  }}>
                    {[
                      { id: 'community', label: '社区' },
                      { id: 'mine', label: '我的' },
                    ].map(tab => (
                      <button
                        key={tab.id}
                        onClick={() => { setScope(tab.id); setType('全部'); }}
                        style={{
                          height: 38,
                          padding: '0 18px',
                          borderRadius: 13,
                          border: 'none',
                          background: scope === tab.id ? T.navy : 'transparent',
                          color: scope === tab.id ? T.white : T.navyMid,
                          cursor: 'pointer',
                          fontSize: 13,
                          fontWeight: 760,
                          transition: 'background .16s, color .16s',
                        }}
                      >
                        {tab.label}
                      </button>
                    ))}
                  </div>
                </div>
              </header>

              <section style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap', paddingBottom: 18, borderBottom: `1px solid ${T.hairlineSoft}`, marginBottom: 24 }}>
                {types.map(t => (
                  <FilterChip key={t} active={type === t} onClick={() => setType(t)} count={t === '全部' ? filtered.length : SKILL_ITEMS.filter(skill => skill.owner === scope && skill.type === t).length}>
                    {t}
                  </FilterChip>
                ))}
              </section>

              <section style={{ maxWidth: 1040, margin: '0 auto', display: 'grid', gap: 16 }}>
                {filtered.map((skill, index) => (
                  <SkillCard key={skill.id} skill={skill} index={index} onOpen={setSelected} />
                ))}
              </section>
              {filtered.length === 0 && (
                <div style={{ minHeight: 220, borderRadius: 22, border: `1px dashed ${T.hairline}`, background: 'rgba(255,255,255,.56)', color: T.navyLight, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 13 }}>
                  没有找到匹配的 Skill
                </div>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
};

window.SkillsPage = SkillsPage;

/* ─── Insights Page ─── */

const INSIGHT_CONTENTS = [
  { id: 'c1', title: '上海小饭店第一次去怎么点', platform: 'RED', platformLabel: '小红书', exposure: '42,180', likes: '3,180', saves: '1,820', comments: '248', score: '92', next: '拆成菜单系列' },
  { id: 'c2', title: '下班后 30 分钟能吃到的热饭', platform: 'RED', platformLabel: '小红书', exposure: '31,020', likes: '2,012', saves: '1,130', comments: '162', score: '86', next: '补一版对比图' },
  { id: 'c3', title: '后厨备菜的一天', platform: 'd', platformLabel: '抖音', exposure: '86,540', likes: '5,810', saves: '910', comments: '420', score: '89', next: '剪 30s 口播' },
  { id: 'c4', title: '主理人怎么把一碗饭做稳定', platform: '微', platformLabel: '微信', exposure: '8,600', likes: '320', saves: '410', comments: '38', score: '71', next: '前 20% 重写' },
];

const INSIGHT_OBSERVATIONS = [
  {
    type: '赢点',
    time: '今天 · 09:00',
    title: '这周「第一次去怎么点」跑赢同类 82%',
    body: '封面直接把「不踩雷菜单」写清楚，前 3 秒先给结论，再补招牌菜和适合谁去，最能让附近上班族停下来。',
    action: '延展成「招牌菜 / 人均 / 场景」三条系列',
    platform: '小红书优先',
    accent: T.success,
  },
  {
    type: '待优化',
    time: '今天 · 09:00',
    title: '长文《小饭店怎么留住回头客》完读率偏低',
    body: '前 30% 读完率只有 34%，问题在第 2 小节展开过快。可以在小节前加一段「下班来吃饭」的具象场景。',
    action: '把开头改成真实到店场景，再进入方法论',
    platform: '公众号 / 视频号',
    accent: T.warn,
  },
  {
    type: '机会',
    time: '昨天 · 18:12',
    title: '最新机会：#上海饭店推荐 正在上升',
    body: '近 48h 同类内容收藏评论表现 +62%，推荐本周追一条「午市套餐 / 招牌菜 / 适合谁去」的收藏型笔记。',
    action: '今天先做封面和标题 A/B，明早发布',
    platform: '小红书 + 短视频',
    accent: T.iris,
  },
];

const INSIGHT_HOT_TOPICS = [
  { tag: '#上海饭店推荐', change: '+62%', note: '第一次去怎么点、菜单怎么选、适合谁去，这类内容的收藏率持续抬升。', fit: '强相关', format: '图文对比' },
  { tag: '#午市套餐', change: '+38%', note: '人均友好、通勤方便、出餐快的内容，更容易被附近上班族保存。', fit: '可追', format: '清单笔记' },
  { tag: '#主理人日常', change: '+12%', note: '真实备菜、出餐和店内环境，更容易建立门店信任感。', fit: '长期养号', format: '短视频' },
];

const INSIGHT_ACTIONS = [
  { title: '下一条优先做', value: '第一次去怎么点', note: '沿用高收藏封面语言，标题更直接', accent: T.primary },
  { title: '暂缓投入', value: '纯方法论长文', note: '当前完读偏低，先补到店案例', accent: T.peach },
  { title: '定位可沉淀点', value: '首段钩子模板', note: '再发布 2 条即可沉淀为账号写作规则', accent: T.success },
];

const DEFAULT_ACCOUNT_PLAN_CALENDAR = [
  { day: '周一', type: '探店图文', topic: '第一次来店里，先点这 3 道招牌菜', ref: '@本地吃喝指南' },
  { day: '周二', type: '短视频', topic: '后厨备菜 30 秒，看看一碗饭怎么被认真做好', ref: '@街角小店日记' },
  { day: '周三', type: '图文', topic: '附近上班族午餐不踩雷菜单', ref: '@城市午餐研究所' },
  { day: '周四', type: '长文', topic: '一家小店怎么把回头客留住', ref: '@主理人手记' },
  { day: '周五', type: '短视频', topic: '顾客最常问的 5 个问题', ref: '@真实探店' },
  { day: '周六', type: '图文', topic: '周末带朋友来吃，怎么点更划算', ref: '@本地生活家' },
  { day: '周日', type: '复盘', topic: '这周最受欢迎的一道菜', ref: '@小店经营笔记' },
];

const INSIGHT_PLATFORM_PROFILES = {
  overall: {
    label: '全部平台',
    platform: 'ALL',
    theme: T.iris,
    headline: '上海小饭店账号结果优先看',
    note: '先看涨粉、点赞、收藏和评论；点击率、完读率等作为下一层分析指标。',
    conclusion: '现在适合发布「上海小饭店第一次去怎么点」的收藏型内容：先给结论，再给招牌菜、预算和适合谁去，最容易带来保存和到店意愿。',
    overviewCards: [
      { title: '入口', value: '封面点击率稳定', note: '小红书和视频号都适合继续测封面 A/B', accent: T.iris },
      { title: '留存', value: '完读率可加码', note: '公众号长文适合承接更完整的菜单解释', accent: T.success },
      { title: '增长', value: '净涨粉变好', note: '抖音短视频可以把选店逻辑拆成 30 秒版本', accent: T.primary },
    ],
    metrics: [
      { label: '涨粉', value: '+1,284', delta: '+21%' },
      { label: '点赞', value: '11.9k', delta: '+18%' },
      { label: '收藏', value: '4.8k', delta: '+24%' },
      { label: '评论', value: '928', delta: '+12%' },
    ],
    analysisMetrics: [
      { label: '封面点击率', value: '6.0%', delta: '+0.9%' },
      { label: '完播 / 完读率', value: '50.2%', delta: '+2.4%' },
      { label: '收藏率', value: '2.9%', delta: '+0.5%' },
      { label: '净涨粉', value: '+480', delta: '+21%' },
    ],
    chart: {
      '7d': [15, 19, 22, 26, 31, 34, 38, 41, 47, 51, 57, 64],
      '30d': [18, 22, 27, 30, 35, 39, 44, 49, 54, 58, 65, 74],
      '90d': [20, 24, 28, 34, 38, 43, 48, 53, 59, 66, 73, 82],
    },
    rows: [
      { id: 'a1', title: '上海小饭店第一次去怎么点', platform: 'RED', platformLabel: '小红书', exposure: '42,180', likes: '3,180', saves: '1,820', comments: '248', score: '92', next: '继续做系列封面' },
      { id: 'a2', title: '30 秒看懂人均 80 元怎么吃', platform: 'DY', platformLabel: '抖音', exposure: '86,540', likes: '5,810', saves: '910', comments: '420', score: '89', next: '剪 3 秒钩子' },
      { id: 'a3', title: '一家小饭店怎么把回头客留住', platform: 'WX', platformLabel: '微信公众号', exposure: '12,480', likes: '560', saves: '620', comments: '52', score: '79', next: '补案例截图' },
    ],
  },
  red: {
    label: '小红书',
    platform: 'RED',
    theme: T.iris,
    headline: '小红书账号结果',
    note: '先看涨粉、点赞、收藏和评论，再用点击率、完读率判断要不要换封面或补一版。',
    overviewCards: [
      { title: '封面', value: '点击率先看', note: '先判断封面是不是抓住了人', accent: T.primary },
      { title: '正文', value: '完读率稳定', note: '标题进来的人愿不愿意看完', accent: T.iris },
      { title: '扩散', value: '收藏率优先', note: '是否值得继续做系列', accent: T.success },
    ],
    metrics: [
      { label: '涨粉', value: '+1,284', delta: '+24%' },
      { label: '点赞', value: '11.9k', delta: '+18%' },
      { label: '收藏', value: '4.8k', delta: '+24%' },
      { label: '评论', value: '928', delta: '+12%' },
    ],
    analysisMetrics: [
      { label: '封面点击率', value: '8.2%', delta: '+1.4%' },
      { label: '完播 / 完读率', value: '62.4%', delta: '+3.6%' },
      { label: '收藏率', value: '4.3%', delta: '+0.8%' },
      { label: '净涨粉', value: '+128', delta: '+24%' },
    ],
    chart: {
      '7d': [18, 24, 20, 32, 39, 34, 50, 44, 58, 52, 68, 82],
      '30d': [20, 26, 31, 34, 42, 39, 45, 52, 61, 58, 70, 88],
      '90d': [24, 29, 33, 38, 40, 48, 54, 57, 66, 72, 80, 92],
    },
    rows: [
      { id: 'r1', title: '上海小饭店第一次去怎么点', platform: 'RED', platformLabel: '小红书', exposure: '42,180', likes: '3,180', saves: '1,820', comments: '248', score: '92', next: '拆成菜单系列' },
      { id: 'r2', title: '附近上班族午餐不踩雷', platform: 'RED', platformLabel: '小红书', exposure: '31,020', likes: '2,012', saves: '1,130', comments: '162', score: '86', next: '补一版对比图' },
      { id: 'r3', title: '把一碗饭讲清楚', platform: 'RED', platformLabel: '小红书', exposure: '28,640', likes: '1,820', saves: '980', comments: '144', score: '84', next: '做 3 步教程' },
    ],
  },
  dy: {
    label: '抖音',
    platform: 'DY',
    theme: T.success,
    headline: '抖音账号结果',
    note: '先看涨粉、点赞和评论，再用前 3 秒与完播率判断镜头节奏。',
    overviewCards: [
      { title: '前 3 秒', value: '钩子先立住', note: '有没有留下继续看的理由', accent: T.success },
      { title: '中段', value: '完播最关键', note: '节奏是否足够紧', accent: T.iris },
      { title: '回流', value: '评论带涨粉', note: '有没有形成互动链路', accent: T.primary },
    ],
    metrics: [
      { label: '涨粉', value: '+1,284', delta: '+31%' },
      { label: '点赞', value: '11.9k', delta: '+18%' },
      { label: '收藏', value: '4.8k', delta: '+24%' },
      { label: '评论', value: '928', delta: '+12%' },
    ],
    analysisMetrics: [
      { label: '封面点击率', value: '6.4%', delta: '+0.8%' },
      { label: '完播 / 完读率', value: '38.5%', delta: '+2.4%' },
      { label: '收藏率', value: '2.1%', delta: '+0.4%' },
      { label: '净涨粉', value: '+204', delta: '+31%' },
    ],
    chart: {
      '7d': [14, 18, 16, 22, 26, 24, 32, 40, 38, 44, 52, 60],
      '30d': [18, 21, 24, 28, 30, 36, 38, 45, 49, 54, 60, 71],
      '90d': [16, 19, 23, 27, 31, 35, 39, 42, 46, 52, 59, 68],
    },
    rows: [
      { id: 'd1', title: '把后厨备菜拍成 30 秒', platform: 'DY', platformLabel: '抖音', exposure: '86,540', likes: '5,810', saves: '910', comments: '420', score: '89', next: '剪 30s 口播' },
      { id: 'd2', title: '三分钟看懂菜单怎么点', platform: 'DY', platformLabel: '抖音', exposure: '54,210', likes: '3,260', saves: '760', comments: '198', score: '82', next: '补结尾引导' },
      { id: 'd3', title: '主理人一天的出餐节奏', platform: 'DY', platformLabel: '抖音', exposure: '34,060', likes: '1,840', saves: '402', comments: '116', score: '76', next: '做封面 A/B' },
    ],
  },
  wx: {
    label: '微信公众号',
    platform: 'WX',
    theme: T.navy,
    headline: '公众号账号结果',
    note: '先看关注、点赞、收藏和评论，再用完读率判断长文结构是否需要重排。',
    overviewCards: [
      { title: '开头', value: '首段要稳', note: '先交代清楚为什么要看', accent: T.navy },
      { title: '中段', value: '结构要顺', note: '让长文有节奏感', accent: T.iris },
      { title: '结尾', value: '收藏与回看', note: '是否值得被保存', accent: T.success },
    ],
    metrics: [
      { label: '涨粉', value: '+1,284', delta: '+12%' },
      { label: '点赞', value: '11.9k', delta: '+18%' },
      { label: '收藏', value: '4.8k', delta: '+24%' },
      { label: '评论', value: '928', delta: '+12%' },
    ],
    analysisMetrics: [
      { label: '封面点击率', value: '4.1%', delta: '+0.3%' },
      { label: '完播 / 完读率', value: '55.2%', delta: '+1.8%' },
      { label: '收藏率', value: '1.7%', delta: '+0.2%' },
      { label: '净涨粉', value: '+56', delta: '+12%' },
    ],
    chart: {
      '7d': [12, 14, 18, 16, 22, 21, 28, 30, 34, 36, 42, 48],
      '30d': [15, 17, 20, 22, 25, 27, 32, 35, 38, 40, 46, 50],
      '90d': [18, 20, 22, 24, 28, 30, 34, 37, 40, 44, 48, 54],
    },
    rows: [
      { id: 'w1', title: '上海小饭店怎么留住回头客', platform: 'WX', platformLabel: '微信公众号', exposure: '8,600', likes: '320', saves: '410', comments: '38', score: '71', next: '前 20% 重写' },
      { id: 'w2', title: '一份菜单复盘笔记', platform: 'WX', platformLabel: '微信公众号', exposure: '12,480', likes: '560', saves: '620', comments: '52', score: '79', next: '补案例截图' },
      { id: 'w3', title: '每周饭点观察', platform: 'WX', platformLabel: '微信公众号', exposure: '7,240', likes: '210', saves: '330', comments: '26', score: '68', next: '加目录和小标题' },
    ],
  },
  sp: {
    label: '视频号',
    platform: 'SP',
    theme: T.peach,
    headline: '视频号账号结果',
    note: '先看涨粉、点赞、收藏和评论，再用完播率判断真实场景是否足够抓人。',
    overviewCards: [
      { title: '信任', value: '真实场景', note: '有没有让人觉得靠谱', accent: T.peach },
      { title: '节奏', value: '稳住完播', note: '短视频结构是否清楚', accent: T.iris },
      { title: '复看', value: '收藏与转发', note: '是否值得留给熟人', accent: T.success },
    ],
    metrics: [
      { label: '涨粉', value: '+1,284', delta: '+15%' },
      { label: '点赞', value: '11.9k', delta: '+18%' },
      { label: '收藏', value: '4.8k', delta: '+24%' },
      { label: '评论', value: '928', delta: '+12%' },
    ],
    analysisMetrics: [
      { label: '封面点击率', value: '5.3%', delta: '+0.5%' },
      { label: '完播 / 完读率', value: '44.8%', delta: '+1.6%' },
      { label: '收藏率', value: '2.4%', delta: '+0.3%' },
      { label: '净涨粉', value: '+92', delta: '+15%' },
    ],
    chart: {
      '7d': [10, 13, 15, 17, 22, 24, 26, 28, 30, 33, 37, 42],
      '30d': [11, 14, 16, 19, 21, 25, 28, 31, 34, 36, 40, 45],
      '90d': [13, 15, 18, 20, 23, 26, 30, 33, 35, 39, 42, 48],
    },
    rows: [
      { id: 's1', title: '社区小馆的一天', platform: 'SP', platformLabel: '视频号', exposure: '14,230', likes: '680', saves: '260', comments: '40', score: '74', next: '加人物采访' },
      { id: 's2', title: '门店真实出餐', platform: 'SP', platformLabel: '视频号', exposure: '18,520', likes: '920', saves: '310', comments: '57', score: '78', next: '补字幕条' },
      { id: 's3', title: '顾客常问 5 个问题', platform: 'SP', platformLabel: '视频号', exposure: '9,840', likes: '420', saves: '180', comments: '23', score: '69', next: '压缩时长' },
    ],
  },
};

const insightTabs = [
  { id: 'review', label: '数据复盘' },
  { id: 'hot', label: '热点' },
];

const LargeSegmentedTabs = ({ tabs, active, onChange, mobile, minWidth = 300 }) => (
  <div style={{
    display: 'grid',
    gridTemplateColumns: `repeat(${tabs.length}, minmax(0, 1fr))`,
    gap: 6,
    padding: 6,
    borderRadius: 23,
    border: `1px solid ${T.hairlineSoft}`,
    background: 'rgba(255,255,255,.84)',
    boxShadow: '0 14px 30px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.80)',
    minWidth: mobile ? 0 : minWidth,
    width: mobile ? '100%' : 'auto',
  }}>
    {tabs.map(tab => {
      const selected = active === tab.id;
      return (
        <button
          key={tab.id}
          onClick={() => onChange(tab.id)}
          style={{
            height: mobile ? 44 : 46,
            minWidth: 0,
            padding: mobile ? '0 11px' : '0 24px',
            borderRadius: 18,
            border: 'none',
            background: selected ? T.navy : 'transparent',
            color: selected ? T.white : T.navyMid,
            boxShadow: selected ? '0 10px 22px rgba(14,14,44,.16)' : 'none',
            cursor: 'pointer',
            fontSize: mobile ? 13.5 : 15,
            fontWeight: selected ? 760 : 640,
            whiteSpace: 'nowrap',
            transition: `background .18s ${T.ease}, color .18s ${T.ease}, box-shadow .18s ${T.ease}, transform .18s ${T.ease}`,
          }}
          onMouseEnter={e => {
            if (!selected) e.currentTarget.style.background = 'rgba(14,14,44,.035)';
          }}
          onMouseLeave={e => {
            if (!selected) e.currentTarget.style.background = 'transparent';
          }}
        >
          {tab.label}
        </button>
      );
    })}
  </div>
);

const InsightTopBar = ({ active, onChange, mobile }) => (
  <header style={{
    display: 'flex',
    flexDirection: mobile ? 'column' : 'row',
    alignItems: mobile ? 'stretch' : 'flex-end',
    justifyContent: 'space-between',
    gap: mobile ? 18 : 24,
    marginBottom: mobile ? 22 : 26,
  }}>
    <div style={{ minWidth: 0 }}>
      <div style={{ fontSize: 12, fontWeight: 800, letterSpacing: '0.08em', textTransform: 'uppercase', color: T.navyLight, marginBottom: 8 }}>
        Insights
      </div>
      <h1 style={{ margin: 0, fontSize: mobile ? 27 : 34, lineHeight: 1.14, letterSpacing: 0, color: T.navy, fontWeight: 720 }}>
        数据洞察
      </h1>
    </div>

    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      width: mobile ? '100%' : 'auto',
      justifyContent: mobile ? 'space-between' : 'flex-end',
      flexWrap: mobile ? 'nowrap' : 'wrap',
    }}>
      <LargeSegmentedTabs tabs={insightTabs} active={active} onChange={onChange} mobile={mobile} minWidth={338} />
    </div>
  </header>
);

const InsightBrief = ({ mobile, platformData }) => (
  <InsightPanel style={{
    padding: mobile ? 20 : 24,
    background: 'linear-gradient(135deg, rgba(255,255,255,.86), rgba(250,252,254,.72))',
  }}>
    <div style={{
      display: 'grid',
      gridTemplateColumns: mobile ? '1fr' : 'minmax(0, 1.25fr) repeat(3, minmax(0, .92fr))',
      gap: mobile ? 14 : 18,
      alignItems: 'stretch',
    }}>
      <div style={{
        padding: mobile ? 4 : '2px 12px 2px 2px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
      }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, color: T.iris, fontSize: 12.5, fontWeight: 820, marginBottom: 10 }}>
          <Icon name="sparkles" size={14} />
          Nori 今日结论
        </div>
        <div style={{ color: T.navy, fontSize: mobile ? 20 : 23, lineHeight: 1.34, fontWeight: 730 }}>
          {platformData.headline}
        </div>
        <div style={{ marginTop: 12, color: T.navyMid, fontSize: 13.6, lineHeight: 1.72 }}>
          {platformData.note}
        </div>
      </div>
      {platformData.overviewCards.map(item => (
        <div key={item.title} style={{
          minHeight: 126,
          borderRadius: 20,
          border: `1px solid ${T.hairlineSoft}`,
          background: 'rgba(255,255,255,.68)',
          boxShadow: 'inset 0 1px 0 rgba(255,255,255,.82)',
          padding: 18,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          minWidth: 0,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 10 }}>
            <div style={{ color: T.navyLight, fontSize: 12, fontWeight: 820 }}>{item.title}</div>
            <span style={{ width: 9, height: 9, borderRadius: '50%', background: item.accent, boxShadow: `0 0 0 4px ${item.accent}22`, flexShrink: 0 }} />
          </div>
          <div>
            <div style={{ color: T.navy, fontSize: 15.2, lineHeight: 1.42, fontWeight: 740 }}>{item.value}</div>
            <div style={{ marginTop: 8, color: T.navyMid, fontSize: 12.8, lineHeight: 1.58 }}>{item.note}</div>
          </div>
        </div>
      ))}
    </div>
  </InsightPanel>
);

const InsightPanel = ({ children, style }) => (
  <section style={{
    borderRadius: 26,
    background: 'rgba(255,255,255,.82)',
    border: `1px solid ${T.hairlineSoft}`,
    boxShadow: '0 16px 38px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.78)',
    backdropFilter: 'blur(18px) saturate(1.08)',
    overflow: 'hidden',
    ...style,
  }}>
    {children}
  </section>
);

const InsightRangeToggle = ({ options, value, onChange, wide = false }) => (
  <div style={{
    display: 'inline-grid',
    gridTemplateColumns: `repeat(${options.length}, minmax(0, 1fr))`,
    gap: 3,
    padding: 4,
    borderRadius: 15,
    border: `1px solid ${T.hairlineSoft}`,
    background: 'rgba(250,252,254,.78)',
    minWidth: wide ? 360 : (options.length === 3 ? 196 : 176),
  }}>
    {options.map(option => {
      const active = value === option;
      return (
        <button
          key={option}
          onClick={() => onChange(option)}
          style={{
            height: 36,
            borderRadius: 11,
            border: 'none',
            background: active ? T.white : 'transparent',
            color: active ? T.iris : T.navyLight,
            boxShadow: active ? '0 8px 18px rgba(14,14,44,.08)' : 'none',
            fontSize: 13,
            fontWeight: 760,
            cursor: 'pointer',
          }}
        >
          {option}
        </button>
      );
    })}
  </div>
);

const InsightMetric = ({ label, value, delta, down, mobile, compact, index, last, total = 4 }) => (
  <div style={{
    minHeight: mobile ? 116 : 138,
    padding: mobile ? '21px 22px' : '28px 26px',
    borderRight: !mobile && (compact ? index % 2 === 0 : !last) ? `1px solid ${T.hairlineSoft}` : 'none',
    borderBottom: (mobile && !last) || (compact && index < total - 2) ? `1px solid ${T.hairlineSoft}` : 'none',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    minWidth: 0,
  }}>
    <div style={{ fontSize: 12.5, color: T.navyLight, fontWeight: 620, marginBottom: 14 }}>{label}</div>
    <div style={{ fontSize: mobile ? 26 : 28, lineHeight: 1, color: T.navy, fontWeight: 660, fontFamily: T.fontMono }}>{value}</div>
    <div style={{
      marginTop: 17,
      color: down ? T.error : T.success,
      fontSize: 12.5,
      fontWeight: 650,
      fontFamily: T.fontMono,
    }}>
      {down ? '↓' : '↑'} {delta}
    </div>
  </div>
);

const InsightLineChart = ({ range, platformData }) => {
  const values = platformData.chart[range];
  const points = values.map((v, i) => {
    const x = 36 + i * (808 / (values.length - 1));
    const y = 276 - v * 2.55;
    return [x, y];
  });
  const line = points.map(([x, y], i) => `${i === 0 ? 'M' : 'L'}${x.toFixed(1)} ${y.toFixed(1)}`).join(' ');
  const area = `${line} L844 304 L36 304 Z`;

  return (
    <svg viewBox="0 0 880 320" width="100%" height="100%" style={{ display: 'block' }} preserveAspectRatio="none">
      <defs>
        <linearGradient id={`reviewChartFill-${range}`} x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stopColor={platformData.theme} stopOpacity=".18" />
          <stop offset="100%" stopColor={T.success} stopOpacity="0" />
        </linearGradient>
      </defs>
      {[64, 124, 184, 244, 304].map(y => (
        <line key={y} x1="36" x2="844" y1={y} y2={y} stroke="rgba(14,14,44,.045)" strokeWidth="1" />
      ))}
      <path d={area} fill={`url(#reviewChartFill-${range})`} />
      <path d={line} fill="none" stroke={platformData.theme} strokeWidth="3.2" strokeLinecap="round" strokeLinejoin="round" />
      {points.map(([x, y], i) => i % 3 === 0 || i === points.length - 1 ? (
        <circle key={`${x}-${y}`} cx={x} cy={y} r="4.2" fill={T.white} stroke={platformData.theme} strokeWidth="2.2" />
      ) : null)}
    </svg>
  );
};

const InsightTable = ({ rows, mobile }) => {
  if (mobile) {
    return (
      <div style={{ display: 'grid', gap: 10, padding: '14px 16px 18px' }}>
        {rows.map(row => (
          <div key={row.id} style={{ border: `1px solid ${T.hairlineSoft}`, borderRadius: 18, padding: 14, background: 'rgba(250,252,254,.74)' }}>
            <div style={{ fontSize: 14, fontWeight: 820, color: T.navy }}>{row.title}</div>
            <div style={{ marginTop: 10, display: 'flex', gap: 8, flexWrap: 'wrap', fontSize: 12, color: T.navyLight }}>
              <PlatformBadge row={row} />
              <span>曝光 {row.exposure}</span>
              <span>点赞 {row.likes}</span>
              <span>收藏 {row.saves}</span>
              <span>评论 {row.comments}</span>
              <span>Nori {row.score}</span>
              <span>{row.next}</span>
            </div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div style={{ overflowX: 'auto' }}>
      <div style={{ minWidth: 860 }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(250px, 1.35fr) 112px repeat(4, minmax(92px, .48fr)) 92px minmax(150px, .75fr)',
          minHeight: 58,
          alignItems: 'center',
          color: T.navyLight,
          fontSize: 13,
          fontWeight: 820,
          borderBottom: `1px solid ${T.hairline}`,
          padding: '0 28px',
        }}>
          {['内容', '平台', '曝光', '点赞', '收藏', '评论', '评分', '下一步'].map(item => <div key={item}>{item}</div>)}
        </div>
        {rows.map(row => (
          <div key={row.id} style={{
            display: 'grid',
            gridTemplateColumns: 'minmax(250px, 1.35fr) 112px repeat(4, minmax(92px, .48fr)) 92px minmax(150px, .75fr)',
            minHeight: 76,
            alignItems: 'center',
            padding: '0 28px',
            color: T.navy,
            fontSize: 16,
            fontWeight: 760,
          }}>
            <div>{row.title}</div>
            <div><PlatformBadge row={row} /></div>
            <div style={{ fontFamily: T.fontMono, color: T.navyMid }}>{row.exposure}</div>
            <div style={{ fontFamily: T.fontMono, color: T.navyMid }}>{row.likes}</div>
            <div style={{ fontFamily: T.fontMono, color: T.navyMid }}>{row.saves}</div>
            <div style={{ fontFamily: T.fontMono, color: T.navyMid }}>{row.comments}</div>
            <div style={{ fontFamily: T.fontMono, color: Number(row.score) >= 85 ? T.success : T.warn }}>{row.score}</div>
            <div style={{ color: T.navyMid, fontSize: 13.5, fontWeight: 680 }}>{row.next}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

const PlatformBadge = ({ row }) => {
  const bg = row.platform === 'RED' ? '#f04455' : row.platform === 'DY' || row.platform === 'd' ? '#111111' : row.platform === 'WX' ? T.success : T.iris;
  return (
    <span title={row.platformLabel} style={{
      minWidth: 24,
      height: 24,
      padding: '0 6px',
      borderRadius: 7,
      background: bg,
      color: T.white,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 9,
      fontWeight: 840,
      fontFamily: row.platform === '微' ? T.fontSans : T.fontMono,
    }}>
      {row.platform}
    </span>
  );
};

const InsightReviewTab = ({ mobile, compact, platform, onPlatformChange }) => {
  const [chartRange, setChartRange] = React.useState('7d');
  const [tableRange, setTableRange] = React.useState('近 7 天');
  const [timeGranularity, setTimeGranularity] = React.useState('Daily');
  const platformData = INSIGHT_PLATFORM_PROFILES[platform] || INSIGHT_PLATFORM_PROFILES.overall;
  const metrics = platformData.metrics;
  const platformKeys = ['overall', 'red', 'dy', 'wx', 'sp'];

  return (
    <div style={{ display: 'grid', gap: mobile ? 22 : 30 }}>
      <InsightPanel>
        <div style={{
          padding: mobile ? '22px 20px 4px' : '28px 30px 6px',
          display: 'flex',
          justifyContent: 'flex-end',
          alignItems: mobile ? 'stretch' : 'flex-start',
          gap: mobile ? 14 : 18,
          flexDirection: mobile ? 'column' : 'row',
        }}>
          <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: mobile ? 'flex-start' : 'flex-end', gap: 10 }}>
            <InsightRangeToggle options={['Daily', 'Weekly', 'Monthly']} value={timeGranularity} onChange={setTimeGranularity} />
            <InsightRangeToggle
              options={platformKeys.map(key => INSIGHT_PLATFORM_PROFILES[key].label)}
              value={platformData.label}
              onChange={(label) => {
                const next = platformKeys.find(key => INSIGHT_PLATFORM_PROFILES[key].label === label);
                if (next) onPlatformChange(next);
              }}
              wide={!mobile}
            />
          </div>
        </div>
        <div style={{
          display: 'grid',
          gridTemplateColumns: mobile ? '1fr' : compact ? 'repeat(2, minmax(0, 1fr))' : 'repeat(4, minmax(0, 1fr))',
        }}>
          {metrics.map((metric, index) => (
            <InsightMetric
              key={metric.label}
              {...metric}
              mobile={mobile}
              compact={compact}
              index={index}
              total={metrics.length}
              last={index === metrics.length - 1}
            />
          ))}
        </div>
      </InsightPanel>

      <InsightPanel style={{
        padding: mobile ? 22 : 30,
        background: 'linear-gradient(135deg, rgba(224,250,244,.88), rgba(245,255,224,.54))',
        border: '1px solid rgba(49,208,170,.16)',
        boxShadow: '0 18px 44px rgba(49,208,170,.08), inset 0 1px 0 rgba(255,255,255,.72)',
      }}>
        <div style={{ display: 'flex', alignItems: 'flex-start', gap: 14 }}>
          <span style={{
            width: 42,
            height: 42,
            borderRadius: 16,
            background: 'rgba(255,255,255,.78)',
            color: T.success,
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
            boxShadow: '0 10px 22px rgba(49,208,170,.10)',
          }}>
            <Icon name="sparkles" size={18} />
          </span>
          <div style={{ minWidth: 0 }}>
            <div style={{ color: T.success, fontSize: 12.5, fontWeight: 720, marginBottom: 10 }}>Nori 今日结论</div>
            <div style={{ color: T.navy, fontSize: mobile ? 18 : 20, lineHeight: 1.56, fontWeight: 620 }}>
              {platformData.conclusion || '现在适合发布「上海小饭店第一次去怎么点」的收藏型内容。用明确菜单结论带点击，用真实到店场景带收藏，再把同一主题拆成短视频和长文承接。'}
            </div>
            <div style={{ marginTop: 12, color: T.navyMid, fontSize: 13.2, lineHeight: 1.82, fontWeight: 430 }}>
              建议今天先做一条「第一次去照着点」的版本：标题不要太文艺，第一屏直接给菜单结论，正文再补人均、位置和避坑提醒。
            </div>
          </div>
        </div>
      </InsightPanel>

      <div style={{
        display: 'grid',
        gridTemplateColumns: mobile ? '1fr' : 'minmax(0, 1.42fr) minmax(340px, .72fr)',
        gap: mobile ? 22 : 30,
        alignItems: 'stretch',
      }}>
        <InsightPanel style={{ padding: mobile ? '26px 22px 22px' : '34px 36px 30px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16, flexWrap: 'wrap', alignItems: 'flex-start' }}>
            <div>
              <div style={{ fontSize: 13, color: T.navyLight, fontWeight: 650, marginBottom: 16 }}>七日核心指标趋势</div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 12, flexWrap: 'wrap' }}>
                <span style={{ fontSize: mobile ? 30 : 34, lineHeight: 1, color: T.navy, fontWeight: 660, fontFamily: T.fontMono }}>{platformData.analysisMetrics?.[1]?.value || platformData.metrics[1].value}</span>
                <span style={{ color: T.success, fontSize: 13.2, fontWeight: 650, fontFamily: T.fontMono }}>↑ {(platformData.analysisMetrics?.[1]?.delta || platformData.metrics[1].delta).replace('+', '')}</span>
              </div>
              <div style={{ marginTop: 12, color: T.navyLight, fontSize: 12.5, lineHeight: 1.7, fontWeight: 430 }}>这里看分析数据：封面点击率、完播 / 完读率、收藏率与净涨粉。</div>
            </div>
            <InsightRangeToggle options={['7d', '30d', '90d']} value={chartRange} onChange={setChartRange} />
          </div>
          <div style={{ height: mobile ? 230 : 336, marginTop: mobile ? 24 : 34 }}>
            <InsightLineChart range={chartRange} platformData={platformData} />
          </div>
        </InsightPanel>

        <InsightPanel style={{ padding: mobile ? 24 : 30 }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, marginBottom: 24 }}>
            <div>
              <div style={{ color: T.navyLight, fontSize: 13, fontWeight: 650, marginBottom: 9 }}>平台适配建议</div>
              <div style={{ color: T.navy, fontSize: 17, lineHeight: 1.42, fontWeight: 640 }}>{platformData.label} 当前打法</div>
            </div>
            <span style={{ width: 38, height: 38, borderRadius: 14, background: T.irisTint, color: platformData.theme, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <Icon name="target" size={18} />
            </span>
          </div>
          {platformData.overviewCards.map((item, index) => (
            <div key={item.title} style={{ padding: '18px 0', borderTop: `1px solid ${T.hairlineSoft}` }}>
              <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', gap: 12 }}>
                <div style={{ color: T.navy, fontSize: 14.5, fontWeight: 650 }}>{item.title}</div>
                <div style={{ color: T.navyLight, fontSize: 12.5, fontFamily: T.fontMono }}>{index === 0 ? '1h' : index === 1 ? '3h' : '24h'}</div>
              </div>
              <div style={{ marginTop: 9, color: T.navyMid, fontSize: 12.8, lineHeight: 1.68, fontWeight: 430 }}>{item.note}</div>
              <div style={{ marginTop: 12, height: 5, borderRadius: 999, background: 'rgba(14,14,44,.055)', overflow: 'hidden' }}>
                <div style={{ width: `${74 - index * 12}%`, height: '100%', borderRadius: 999, background: item.accent }} />
              </div>
            </div>
          ))}
        </InsightPanel>
      </div>

      <InsightPanel>
        <PanelHeader title="今天 Nori 给你的观察" action="查看全部" />
        <div style={{ display: 'grid' }}>
          {INSIGHT_OBSERVATIONS.map((item, i) => (
            <div key={item.title} style={{
              display: 'grid',
              gridTemplateColumns: mobile ? '1fr' : '140px minmax(0, 1fr) minmax(230px, .58fr)',
              gap: mobile ? 12 : 24,
              padding: mobile ? '22px 20px' : '26px 30px',
              borderTop: i === 0 ? `1px solid ${T.hairlineSoft}` : `1px solid ${T.hairline}`,
              alignItems: 'start',
            }}>
              <div>
                <div style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  height: 26,
                  padding: '0 10px',
                  borderRadius: 999,
                  background: `${item.accent}18`,
                  color: item.accent,
                  fontSize: 12,
                  fontWeight: 840,
                }}>{item.type}</div>
                <div style={{ marginTop: 6, color: T.navyLight, fontSize: 13, fontFamily: T.fontMono }}>{item.time}</div>
              </div>
              <div>
                <div style={{ color: T.navy, fontSize: mobile ? 16.5 : 17.5, lineHeight: 1.45, fontWeight: 760 }}>{item.title}</div>
                <div style={{ marginTop: 8, color: T.navyMid, fontSize: mobile ? 14 : 14.8, lineHeight: 1.76, fontWeight: 500 }}>{item.body}</div>
              </div>
              <div style={{
                borderRadius: 18,
                border: `1px solid ${T.hairlineSoft}`,
                background: 'rgba(250,252,254,.72)',
                padding: 14,
                minWidth: 0,
              }}>
                <div style={{ color: T.navyLight, fontSize: 12, fontWeight: 820, marginBottom: 8 }}>建议动作</div>
                <div style={{ color: T.navy, fontSize: 13.2, lineHeight: 1.62, fontWeight: 650 }}>{item.action}</div>
                <div style={{ marginTop: 12, display: 'flex', gap: 8, justifyContent: mobile ? 'flex-start' : 'space-between', flexWrap: 'wrap', alignItems: 'center' }}>
                  <span style={{ color: T.iris, fontSize: 12.5, fontWeight: 780 }}>{item.platform}</span>
                  <button style={{ ...pillButtonStyle(true), height: 36, padding: '0 12px', fontSize: 12.5 }}>生成草稿 <Icon name="arrowRight" size={13} /></button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </InsightPanel>

      <InsightPanel>
        <PanelHeader title="单条内容表现" right={<InsightRangeToggle options={['近 7 天', '近 30 天']} value={tableRange} onChange={setTableRange} />} />
        <InsightTable rows={platformData.rows} mobile={mobile} />
      </InsightPanel>
    </div>
  );
};

const PanelHeader = ({ title, action, right }) => (
  <div style={{
    minHeight: 82,
    padding: '0 32px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    gap: 14,
    borderBottom: `1px solid ${T.hairlineSoft}`,
    flexWrap: 'wrap',
  }}>
    <h2 style={{ margin: 0, color: T.navy, fontSize: 17, fontWeight: 650 }}>{title}</h2>
    {right || (action && (
      <button style={{
        border: 'none',
        background: 'transparent',
        color: T.navyLight,
        fontSize: 13.2,
        fontWeight: 650,
        cursor: 'pointer',
        display: 'inline-flex',
        alignItems: 'center',
        gap: 8,
      }}>
        {action}
        <Icon name="chevronRight" size={15} />
      </button>
    ))}
  </div>
);

const pillButtonStyle = (dark) => ({
  height: 42,
  padding: '0 17px',
  borderRadius: 14,
  border: dark ? '1px solid rgba(75,77,237,.16)' : `1px solid ${T.hairline}`,
  background: dark ? 'rgba(239,239,253,.92)' : 'rgba(255,255,255,.72)',
  color: dark ? T.iris : T.navy,
  boxShadow: dark ? '0 10px 22px rgba(75,77,237,.10)' : T.shadowXs,
  display: 'inline-flex',
  alignItems: 'center',
  gap: 7,
  fontSize: 14,
  fontWeight: 820,
  cursor: 'pointer',
  whiteSpace: 'nowrap',
});

const InsightProfileTab = ({ mobile }) => (
  <div style={{ display: 'grid', gap: mobile ? 18 : 24 }}>
    <InsightPanel style={{ padding: mobile ? 22 : 30 }}>
      <div style={{
        display: 'grid',
        gridTemplateColumns: mobile ? '1fr' : 'minmax(0, 1.08fr) minmax(300px, .72fr)',
        gap: mobile ? 22 : 28,
        alignItems: 'center',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 18 }}>
          <img src={ONION_BURST_ASSETS[0]} alt="" style={{ width: 62, height: 62, borderRadius: '50%', objectFit: 'cover', background: T.primaryTint }} />
          <div>
            <div style={{ color: T.navy, fontSize: 21, fontWeight: 760 }}>账号定位</div>
            <div style={{ marginTop: 7, color: T.navyLight, fontSize: 14, fontWeight: 650 }}>来自账号规划输出，后续创作会自动引用</div>
          </div>
        </div>
        <div style={{
          borderRadius: 18,
          border: `1px solid ${T.hairlineSoft}`,
          background: 'rgba(250,252,254,.74)',
          padding: 16,
        }}>
          <div style={{ color: T.navyLight, fontSize: 12, fontWeight: 760, marginBottom: 8 }}>定位一句话</div>
          <div style={{ color: T.navy, fontSize: 16, lineHeight: 1.45, fontWeight: 700 }}>做附近人愿意收藏的上海饭店推荐账号，主打真实复吃和不踩雷菜单。</div>
        </div>
      </div>
    </InsightPanel>

    <InsightPanel style={{ padding: mobile ? 22 : 30 }}>
        <div style={{ color: T.navyLight, fontSize: 13, fontWeight: 760, marginBottom: 18 }}>账号定位五维</div>
        <div style={{
          display: 'grid',
          gridTemplateColumns: mobile ? '1fr' : 'repeat(5, minmax(0, 1fr))',
          gap: 12,
        }}>
          {[
            ['赛道细分', ['上海本地饭店', '社区小馆', '下班约饭']],
            ['目标受众', ['25-38 岁', '附近上班族', '周末聚餐']],
            ['人设标签', ['亲切', '真实主理人', '懂本地生活']],
            ['内容价值', ['不踩雷菜单', '真实种草', '到店决策']],
            ['表达风格', ['口语化', '轻松', '先给结论']],
          ].map(([title, tags]) => (
            <div key={title} style={{
              borderRadius: 18,
              border: `1px solid ${T.hairlineSoft}`,
              background: 'rgba(250,252,254,.72)',
              padding: 16,
              minHeight: 146,
            }}>
              <div style={{ color: T.navy, fontSize: 15, fontWeight: 760, marginBottom: 12 }}>{title}</div>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                {tags.map(tag => (
                  <span key={tag} style={{
                    minHeight: 30,
                    padding: '6px 10px',
                    borderRadius: 999,
                    background: 'rgba(255,255,255,.78)',
                    border: `1px solid ${T.hairlineSoft}`,
                    color: T.navyMid,
                    fontSize: 12.4,
                    lineHeight: 1.35,
                    fontWeight: 620,
                  }}>{tag}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </InsightPanel>

    <InsightPanel>
      <PanelHeader title="运营计划摘要" action="查看完整运营计划" />
      <div style={{
        display: 'grid',
        gridTemplateColumns: mobile ? '1fr' : 'repeat(3, minmax(0, 1fr))',
      }}>
        {[
          ['选题库', '第一次来怎么点、附近午餐不踩雷、老板的一天'],
          ['发布节奏', '一周 7 篇，图文和短视频交替，先验证收藏率'],
          ['数据目标', '7 天验证一套稳定标题结构，重点看收藏和净涨粉'],
        ].map(([title, body], index) => (
          <div key={title} style={{
            padding: mobile ? 22 : 26,
            borderTop: mobile || index < 3 ? `1px solid ${T.hairlineSoft}` : 'none',
            borderRight: !mobile && index < 2 ? `1px solid ${T.hairlineSoft}` : 'none',
          }}>
            <div style={{ color: T.iris, fontSize: 13, fontWeight: 840, marginBottom: 10 }}>{title}</div>
            <div style={{ color: T.navy, fontSize: 14.5, lineHeight: 1.68, fontWeight: 650 }}>{body}</div>
          </div>
        ))}
      </div>
    </InsightPanel>
  </div>
);

const ToggleSwitch = ({ on }) => (
  <span style={{
    width: 54,
    height: 32,
    borderRadius: 999,
    background: on ? T.success : 'rgba(14,14,44,.12)',
    padding: 3,
    display: 'inline-flex',
    justifyContent: on ? 'flex-end' : 'flex-start',
    boxShadow: 'inset 0 1px 2px rgba(14,14,44,.12)',
  }}>
    <span style={{ width: 26, height: 26, borderRadius: '50%', background: T.white, boxShadow: T.shadowSm }} />
  </span>
);

const InsightCalendarTab = ({ mobile, calendar }) => {
  const [range, setRange] = React.useState('本周');
  const [anchorDate, setAnchorDate] = React.useState('2026-05-18');
  const dayNumbers = ['18', '19', '20', '21', '22', '23', '24'];
  const times = ['09:00', '11:30', '14:00', '16:30', '20:00'];
  const eventColors = [
    { bg: 'rgba(239,239,253,.82)', border: 'rgba(75,77,237,.16)', fg: T.iris },
    { bg: 'rgba(224,250,244,.78)', border: 'rgba(49,208,170,.16)', fg: T.success },
    { bg: 'rgba(245,255,224,.88)', border: 'rgba(214,255,0,.28)', fg: '#6e8400' },
    { bg: 'rgba(253,245,245,.88)', border: 'rgba(243,219,218,.95)', fg: T.navyMid },
  ];
  const events = calendar.map((item, index) => ({
    ...item,
    date: dayNumbers[index] || `${18 + index}`,
    time: times[index % times.length],
    top: 34 + (index % 5) * 68,
    height: index % 3 === 1 ? 92 : 78,
    tone: eventColors[index % eventColors.length],
  }));

  if (mobile) {
    return (
      <div style={{ display: 'grid', gap: 18 }}>
        <InsightPanel style={{ padding: 16 }}>
          <div style={{ display: 'grid', gap: 10, marginBottom: 14 }}>
            <div style={{ color: T.navy, fontSize: 18, fontWeight: 700 }}>2026 年 5 月</div>
            <InsightRangeToggle options={['本周', '下周', '本月']} value={range} onChange={setRange} />
            <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) auto', gap: 10 }}>
              <input
                type="date"
                value={anchorDate}
                onChange={e => setAnchorDate(e.target.value)}
                style={{
                  height: 40,
                  borderRadius: 13,
                  border: `1px solid ${T.hairlineSoft}`,
                  background: 'rgba(255,255,255,.80)',
                  color: T.navyMid,
                  padding: '0 12px',
                  fontFamily: T.fontSans,
                  fontSize: 13,
                  outline: 'none',
                }}
              />
              <button style={{ ...pillButtonStyle(false), height: 40, borderRadius: 13, justifyContent: 'center' }}>
                <Icon name="plus" size={15} />
                新增内容
              </button>
            </div>
          </div>
          <div style={{ display: 'grid', gap: 10 }}>
            {events.map((item, index) => (
              <div key={`${item.day}-${index}`} style={{
                borderRadius: 18,
                border: `1px solid ${item.tone.border}`,
                background: item.tone.bg,
                padding: 14,
                display: 'grid',
                gridTemplateColumns: '58px minmax(0, 1fr)',
                gap: 12,
              }}>
                <div>
                  <div style={{ color: item.tone.fg, fontSize: 12, fontFamily: T.fontMono, fontWeight: 720 }}>{item.time}</div>
                  <div style={{ marginTop: 7, color: T.navyLight, fontSize: 12, fontWeight: 650 }}>{item.day}</div>
                </div>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                    <span style={{ color: item.tone.fg, fontSize: 12, fontWeight: 760 }}>{item.type}</span>
                    <span style={{ color: T.navyLight, fontSize: 11.5 }}>{item.date} 日</span>
                  </div>
                  <div style={{ marginTop: 7, color: T.navy, fontSize: 14.2, lineHeight: 1.5, fontWeight: 660 }}>{item.topic}</div>
                  <div style={{ marginTop: 8, color: T.navyLight, fontSize: 12.2, lineHeight: 1.5 }}>{item.ref}</div>
                </div>
              </div>
            ))}
          </div>
        </InsightPanel>
      </div>
    );
  }

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <InsightPanel style={{ padding: 0 }}>
        <div style={{
          height: 62,
          padding: '0 22px',
          borderBottom: `1px solid ${T.hairlineSoft}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 14,
        }}>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
            <div style={{ color: T.navy, fontSize: 18, fontWeight: 700 }}>2026 年 5 月</div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 10, flexWrap: 'wrap' }}>
            <InsightRangeToggle options={['本周', '下周', '本月']} value={range} onChange={setRange} />
            <input
              type="date"
              value={anchorDate}
              onChange={e => setAnchorDate(e.target.value)}
              style={{
                height: 38,
                borderRadius: 13,
                border: `1px solid ${T.hairlineSoft}`,
                background: 'rgba(255,255,255,.78)',
                color: T.navyMid,
                padding: '0 10px',
                fontFamily: T.fontSans,
                fontSize: 12.5,
                outline: 'none',
              }}
            />
            <button style={{ ...pillButtonStyle(false), height: 38, borderRadius: 13, justifyContent: 'center' }}>
              <Icon name="plus" size={15} />
              新增内容
            </button>
          </div>
        </div>
        <div style={{
          display: 'grid',
          gridTemplateColumns: '74px repeat(7, minmax(120px, 1fr))',
          overflowX: 'auto',
        }}>
          <div style={{ borderRight: `1px solid ${T.hairlineSoft}`, background: 'rgba(250,252,254,.58)' }}>
            <div style={{ height: 58, borderBottom: `1px solid ${T.hairlineSoft}` }} />
            {times.map(time => (
              <div key={time} style={{
                height: 68,
                padding: '12px 12px 0',
                borderBottom: `1px solid ${T.hairlineSoft}`,
                color: T.navyLight,
                fontSize: 11.5,
                fontFamily: T.fontMono,
              }}>{time}</div>
            ))}
          </div>
          {events.map((day, index) => (
            <div key={`${day.day}-${index}`} style={{ minWidth: 120, borderRight: index === events.length - 1 ? 'none' : `1px solid ${T.hairlineSoft}`, position: 'relative', minHeight: 398 }}>
              <div style={{
                height: 58,
                borderBottom: `1px solid ${T.hairlineSoft}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexDirection: 'column',
                gap: 4,
                background: index === 3 ? 'rgba(239,239,253,.34)' : 'rgba(255,255,255,.28)',
              }}>
                <div style={{ color: index === 3 ? T.iris : T.navy, fontSize: 13.2, fontWeight: 720 }}>{day.day}</div>
                <div style={{ color: T.navyLight, fontSize: 11.5, fontFamily: T.fontMono }}>05/{day.date}</div>
              </div>
              {times.map(time => (
                <div key={time} style={{ height: 68, borderBottom: `1px solid ${T.hairlineSoft}`, background: index === 3 ? 'rgba(239,239,253,.16)' : 'transparent' }} />
              ))}
              <div style={{
                position: 'absolute',
                left: 10,
                right: 10,
                top: day.top,
                minHeight: day.height,
                borderRadius: 16,
                border: `1px solid ${day.tone.border}`,
                background: day.tone.bg,
                boxShadow: '0 10px 22px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.66)',
                padding: 12,
                overflow: 'hidden',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8, marginBottom: 8 }}>
                  <span style={{ color: day.tone.fg, fontSize: 11.5, fontWeight: 760 }}>{day.type}</span>
                  <span style={{ color: T.navyLight, fontSize: 10.5, fontFamily: T.fontMono }}>{day.time}</span>
                </div>
                <div style={{ color: T.navy, fontSize: 13.1, lineHeight: 1.42, fontWeight: 660 }}>{day.topic}</div>
                <div style={{ marginTop: 7, color: T.navyLight, fontSize: 11.5, lineHeight: 1.4 }}>{day.ref}</div>
              </div>
            </div>
          ))}
        </div>
      </InsightPanel>
    </div>
  );
};

const MineAssetLibraryTab = ({ mobile }) => {
  const categories = ['媒体库', '品牌风格', '品牌声音', '品牌简介', '原始资料'];
  const media = [
    { src: PLANNING_BENCHMARK_PHOTOS[0], title: '招牌菜俯拍', used: true },
    { src: PLANNING_BENCHMARK_PHOTOS[1], title: '门店环境', used: false },
    { src: PLANNING_BENCHMARK_PHOTOS[2], title: '午餐套餐', used: true },
    { src: './src/onion-burst-real.png', title: '菜单截图', used: true },
    { src: './src/onion-burst-collage.png', title: '评论截图合集', used: false },
    { src: './src/inspiration-skill-card.png', title: '活动海报参考', used: true },
    { src: './src/insight-avatar-reference.png', title: '账号头像参考', used: false },
    { src: './src/onion-burst-ring.png', title: '品牌视觉素材', used: true },
  ];
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: mobile ? '1fr' : '180px minmax(0, 1fr)',
      gap: mobile ? 18 : 26,
      alignItems: 'start',
    }}>
      <InsightPanel style={{ padding: mobile ? 10 : 12 }}>
        <div style={{ display: 'grid', gap: 2 }}>
          {categories.map((item, index) => (
            <button key={item} style={{
              height: 44,
              border: `1px solid ${index === 0 ? 'rgba(75,77,237,.16)' : 'transparent'}`,
              background: index === 0 ? 'rgba(239,239,253,.70)' : 'transparent',
              color: index === 0 ? T.iris : T.navyLight,
              cursor: 'pointer',
              textAlign: 'left',
              padding: '0 16px',
              borderRadius: 13,
              fontSize: 13.4,
              fontWeight: index === 0 ? 760 : 650,
              fontFamily: T.fontSans,
              boxShadow: index === 0 ? 'inset 0 1px 0 rgba(255,255,255,.78)' : 'none',
            }}>{item}</button>
          ))}
        </div>
      </InsightPanel>

      <div style={{ display: 'grid', gap: mobile ? 18 : 24 }}>
        <InsightPanel style={{ padding: mobile ? 22 : 30 }}>
          <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 16, flexWrap: 'wrap' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'baseline', gap: 10, flexWrap: 'wrap' }}>
                <h2 style={{ margin: 0, color: T.navy, fontSize: mobile ? 28 : 34, lineHeight: 1.16, fontWeight: 710 }}>
                  媒体库
                </h2>
                <span style={{ color: T.navyLight, fontSize: 16, fontWeight: 650 }}>12 张图片，0 个视频</span>
              </div>
              <div style={{ marginTop: 28, color: T.navy, fontSize: mobile ? 19 : 22, lineHeight: 1.32, fontWeight: 720 }}>
                添加媒体内容，保持内容新鲜度
              </div>
              <p style={{ margin: '8px 0 0', maxWidth: 760, color: T.navyMid, fontSize: 14.2, lineHeight: 1.74 }}>
                Nori 使用你的图片和视频，根据你的营销活动创建相关的社交媒体帖子、公众号内容和短视频脚本。
              </p>
            </div>
            <button style={{ ...pillButtonStyle(true), height: 42, borderRadius: 14, justifyContent: 'center' }}>
              <Icon name="plus" size={15} />
              添加新媒体
            </button>
          </div>
        </InsightPanel>

        <div style={{
          display: 'grid',
          gridTemplateColumns: mobile ? 'repeat(2, minmax(0, 1fr))' : 'repeat(4, minmax(0, 1fr))',
          gap: mobile ? 14 : 22,
        }}>
          {media.map((item, index) => (
            <div key={item.title} style={{ minWidth: 0 }}>
              <div style={{
                position: 'relative',
                aspectRatio: '1 / 1',
                borderRadius: 20,
                overflow: 'hidden',
                background: T.surface,
                border: `1px solid ${T.hairlineSoft}`,
                boxShadow: '0 12px 28px rgba(14,14,44,.065)',
              }}>
                <img src={item.src} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} />
                <span style={{
                  position: 'absolute',
                  left: 13,
                  top: 13,
                  width: 24,
                  height: 24,
                  borderRadius: 7,
                  border: `1px solid ${T.hairline}`,
                  background: 'rgba(255,255,255,.88)',
                  boxShadow: '0 6px 14px rgba(14,14,44,.09)',
                }} />
                {item.used && (
                  <span style={{
                    position: 'absolute',
                    left: 13,
                    bottom: 13,
                    height: 28,
                    padding: '0 11px',
                    borderRadius: 999,
                    background: 'rgba(255,255,255,.86)',
                    color: T.navyMid,
                    display: 'inline-flex',
                    alignItems: 'center',
                    fontSize: 12.2,
                    fontWeight: 650,
                    backdropFilter: 'blur(10px)',
                  }}>用过的</span>
                )}
              </div>
              <div style={{ marginTop: 14, color: T.navy, fontSize: 14.5, lineHeight: 1.35, fontWeight: 650, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{item.title}</div>
              <div style={{ marginTop: 5, color: T.navyLight, fontSize: 12.4, lineHeight: 1.45 }}>图像 · {index < 4 ? '6 天前上传' : '今天加入'}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const InsightHotTab = ({ mobile }) => (
  <div style={{ display: 'grid', gap: mobile ? 18 : 24 }}>
    <InsightPanel style={{ padding: mobile ? 24 : 30 }}>
      <div style={{
        display: 'grid',
        gridTemplateColumns: mobile ? '1fr' : 'minmax(0, 1fr) auto',
        gap: 18,
        alignItems: 'center',
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12 }}>
            <span style={{
              height: 28,
              padding: '0 12px',
              borderRadius: 999,
              background: T.navy,
              color: T.primary,
              fontSize: 13,
              fontWeight: 860,
              fontFamily: T.fontMono,
              display: 'inline-flex',
              alignItems: 'center',
            }}>PRO</span>
            <div style={{ color: T.navyLight, fontSize: 13, fontWeight: 820 }}>热点机会雷达</div>
          </div>
          <div style={{ color: T.navy, fontSize: mobile ? 21 : 24, lineHeight: 1.32, fontWeight: 740 }}>
            今天适合追「上海饭店推荐 / 午市套餐」，不建议追泛娱乐热词。
          </div>
          <p style={{ margin: '12px 0 0', maxWidth: 720, color: T.navyMid, fontSize: 14.5, lineHeight: 1.7 }}>
            Nori 会根据你的门店定位过滤热点，只留下既有增长空间、又不破坏小饭店真实感的选题。
          </p>
        </div>
        <button style={{ ...pillButtonStyle(true), justifyContent: 'center' }}>
          <Icon name="bell" size={16} />
          绑定飞书日报
        </button>
      </div>
    </InsightPanel>

    <div style={{
      display: 'grid',
      gridTemplateColumns: mobile ? '1fr' : 'minmax(0, 1.35fr) minmax(320px, .72fr)',
      gap: mobile ? 18 : 24,
      alignItems: 'stretch',
    }}>
    <InsightPanel>
      <PanelHeader title="可追热点" action="刷新雷达" />
      <div style={{ display: 'grid', padding: mobile ? '0 20px 8px' : '0 26px 10px' }}>
        {INSIGHT_HOT_TOPICS.map(topic => (
          <div key={topic.tag} style={{
            display: 'grid',
            gridTemplateColumns: mobile ? '1fr' : 'minmax(0, 1fr) 96px 112px auto',
            gap: 16,
            padding: '20px 0',
            borderBottom: `1px solid ${T.hairlineSoft}`,
            alignItems: 'center',
          }}>
            <div>
              <div style={{ color: T.navy, fontSize: 16, fontWeight: 760 }}>{topic.tag}</div>
              <div style={{ marginTop: 8, color: T.navyLight, fontSize: 13.2, lineHeight: 1.62 }}>{topic.note}</div>
            </div>
            <div style={{ color: T.iris, fontSize: 13, fontWeight: 820 }}>{topic.fit}</div>
            <div style={{ color: T.navyMid, fontSize: 13, fontWeight: 720 }}>{topic.format}</div>
            <div style={{ color: T.success, fontSize: 16, fontWeight: 840, fontFamily: T.fontMono }}>{topic.change}</div>
          </div>
        ))}
      </div>
    </InsightPanel>

    <InsightPanel style={{ padding: mobile ? 24 : 30 }}>
      <div style={{ color: T.navyLight, fontSize: 13, fontWeight: 840, marginBottom: 12 }}>推送渠道</div>
      <h2 style={{ margin: '0 0 26px', color: T.navy, fontSize: mobile ? 22 : 24, fontWeight: 740 }}>飞书 / 微信 日报</h2>
      {[
        { name: '飞书', sub: '@巷口暖胃小馆 · 每日 09:00 · 热点 + 昨日数据', on: true, tag: '已开启' },
        { name: '微信', sub: '未绑定 · 通过公众号"Nori 播报"接收', on: false, tag: '待绑定' },
      ].map((row, index) => (
        <div key={row.name} style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(0, 1fr) auto',
          gap: 16,
          alignItems: 'center',
          padding: '26px 0',
          borderTop: index === 0 ? `1px solid ${T.hairlineSoft}` : `1px solid ${T.hairline}`,
        }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
              <div style={{ color: T.navy, fontSize: 18, fontWeight: 860 }}>{row.name}</div>
              <span style={{ color: row.on ? T.success : T.navyLight, fontSize: 12, fontWeight: 820 }}>{row.tag}</span>
            </div>
            <div style={{ marginTop: 8, color: T.navyLight, fontSize: 14, lineHeight: 1.6, fontWeight: 680 }}>{row.sub}</div>
          </div>
          <ToggleSwitch on={row.on} />
        </div>
      ))}
    </InsightPanel>
    </div>
  </div>
);

const InsightsPage = ({ onBackHome, onOpenAssets, onOpenMine, onNewChat, initialTab = 'review' }) => {
  const { isTablet, isMobile } = useViewport();
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [activeTab, setActiveTab] = React.useState(initialTab);
  const [platformTab, setPlatformTab] = React.useState('overall');
  const [refreshing, setRefreshing] = React.useState(false);
  const sessions = INSIGHT_CONTENTS.map(item => item.title);
  const savedPlanCalendar = React.useMemo(() => loadPlanDraft()?.calendar || DEFAULT_ACCOUNT_PLAN_CALENDAR, []);

  React.useEffect(() => {
    setActiveTab(initialTab);
  }, [initialTab]);

  const refresh = () => {
    setRefreshing(true);
    window.setTimeout(() => setRefreshing(false), 620);
  };

  return (
    <div style={{
      display: 'flex',
      width: '100%',
      height: '100%',
      overflow: 'hidden',
      background: T.surfaceWh,
      color: T.navy,
      fontFamily: T.fontSans,
    }}>
      {!isTablet && (
        <Sidebar
          active="insights"
          onNew={onNewChat}
          onNavigate={(id) => {
            if (id === 'home') onBackHome();
            if (id === 'library') onOpenAssets && onOpenAssets();
            if (id === 'mine') onOpenMine && onOpenMine();
          }}
          sessions={sessions}
          collapsed={navCollapsed}
          onToggle={() => setNavCollapsed(v => !v)}
        />
      )}
      <main style={{
        flex: 1,
        minWidth: 0,
        overflow: 'auto',
        position: 'relative',
        background: 'linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)',
      }}>
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(circle at 18% 12%, rgba(214,255,0,.14), transparent 18%), radial-gradient(circle at 82% 10%, rgba(75,77,237,.08), transparent 22%), radial-gradient(circle at 63% 72%, rgba(49,208,170,.06), transparent 22%)',
          pointerEvents: 'none',
        }} />
        <div style={{
          position: 'relative',
          zIndex: 1,
          maxWidth: 1640,
          margin: '0 auto',
          padding: isMobile ? '18px 18px 36px' : '28px 30px 50px',
        }}>
          {isTablet && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <NoriLogo size={28} />
                <div>
                  <div style={{ fontSize: 15, fontWeight: 760, color: T.navy }}>数据洞察</div>
                  <div style={{ fontSize: 11, color: T.navyLight }}>复盘与热点工作台</div>
                </div>
              </div>
              <button onClick={onBackHome} style={iconBtnStyle()}><Icon name="home" size={16} color={T.navyMid} /></button>
            </div>
          )}

          <InsightTopBar
            active={activeTab}
            onChange={setActiveTab}
            mobile={isMobile}
          />

          <div style={{ animation: refreshing ? 'fadeInScale .32s ease both' : 'none' }}>
            {activeTab === 'review' && <InsightReviewTab mobile={isMobile} compact={isTablet && !isMobile} platform={platformTab} onPlatformChange={setPlatformTab} />}
            {activeTab === 'hot' && <InsightHotTab mobile={isMobile} />}
          </div>
        </div>
      </main>
    </div>
  );
};

window.InsightsPage = InsightsPage;

const MinePage = ({ onBackHome, onOpenAssets, onOpenInsights, onNewChat }) => {
  const { isTablet, isMobile } = useViewport();
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [activeTab, setActiveTab] = React.useState('profile');
  const savedPlanCalendar = React.useMemo(() => loadPlanDraft()?.calendar || DEFAULT_ACCOUNT_PLAN_CALENDAR, []);
  const sessions = ['我的账号定位', '本周内容日历', '账号规划文档'];
  const tabs = [
    { id: 'profile', label: '账号定位' },
    { id: 'calendar', label: '内容日历' },
    { id: 'assets', label: '资产库' },
  ];

  return (
    <div style={{
      display: 'flex',
      width: '100%',
      height: '100%',
      overflow: 'hidden',
      background: T.surfaceWh,
      color: T.navy,
      fontFamily: T.fontSans,
    }}>
      {!isTablet && (
        <Sidebar
          active="mine"
          onNew={onNewChat}
          onNavigate={(id) => {
            if (id === 'home') onBackHome();
            if (id === 'library') onOpenAssets && onOpenAssets();
            if (id === 'insights') onOpenInsights && onOpenInsights();
          }}
          sessions={sessions}
          collapsed={navCollapsed}
          onToggle={() => setNavCollapsed(v => !v)}
        />
      )}
      <main style={{
        flex: 1,
        minWidth: 0,
        overflow: 'auto',
        position: 'relative',
        background: 'linear-gradient(180deg, #ffffff 0%, #f8fbfd 48%, #fafcfe 100%)',
      }}>
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'radial-gradient(circle at 18% 12%, rgba(214,255,0,.12), transparent 18%), radial-gradient(circle at 82% 10%, rgba(75,77,237,.07), transparent 22%), radial-gradient(circle at 63% 72%, rgba(49,208,170,.06), transparent 22%)',
          pointerEvents: 'none',
        }} />
        <div style={{
          position: 'relative',
          zIndex: 1,
          maxWidth: 1440,
          margin: '0 auto',
          padding: isMobile ? '18px 18px 36px' : '30px 34px 54px',
        }}>
          {isTablet && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 18 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                <NoriLogo size={28} />
                <div>
                  <div style={{ fontSize: 15, fontWeight: 760, color: T.navy }}>我的</div>
                  <div style={{ fontSize: 11, color: T.navyLight }}>账号定位、内容日历与资产库</div>
                </div>
              </div>
              <button onClick={onBackHome} style={iconBtnStyle()}><Icon name="home" size={16} color={T.navyMid} /></button>
            </div>
          )}

          <header style={{
            display: 'flex',
            flexDirection: isMobile ? 'column' : 'row',
            justifyContent: 'space-between',
            alignItems: isMobile ? 'stretch' : 'flex-end',
            gap: isMobile ? 18 : 24,
            marginBottom: isMobile ? 22 : 28,
          }}>
            <div>
              <div style={{ fontSize: 12, fontWeight: 800, letterSpacing: '0.08em', textTransform: 'uppercase', color: T.navyLight, marginBottom: 8 }}>
                Mine
              </div>
              <h1 style={{ margin: 0, fontSize: isMobile ? 27 : 34, lineHeight: 1.14, color: T.navy, fontWeight: 720 }}>
                我的
              </h1>
              <p style={{ margin: '10px 0 0', maxWidth: 640, fontSize: 14, lineHeight: 1.68, color: T.navyMid }}>
                这里放你的账号定位、运营计划、内容排期和品牌资产。
              </p>
            </div>
            <LargeSegmentedTabs tabs={tabs} active={activeTab} onChange={setActiveTab} mobile={isMobile} minWidth={338} />
          </header>

          {activeTab === 'profile' && <InsightProfileTab mobile={isMobile} />}
          {activeTab === 'calendar' && <InsightCalendarTab mobile={isMobile} calendar={savedPlanCalendar} />}
          {activeTab === 'assets' && <MineAssetLibraryTab mobile={isMobile} />}
        </div>
      </main>
    </div>
  );
};

window.MinePage = MinePage;
/* ─── Generation Chat Steps ─── */

/* ── Common atoms ── */

const Avatar = ({ kind = 'nori' }) => {
  if (kind === 'user') {
    return (
      <div style={{
        width: 28, height: 28, borderRadius: '50%', flexShrink: 0,
        background: `linear-gradient(135deg, ${T.iris}, ${T.peach})`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        color: T.white, fontSize: 11.5, fontWeight: 700,
      }}>L</div>
    );
  }
  return null;
};

const Bubble = ({ from = 'nori', children, style }) => {
  const isUser = from === 'user';
  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: isUser ? 'minmax(0, 1fr) 36px' : 'minmax(0, 1fr)',
      gap: isUser ? 12 : 0,
      alignItems: 'flex-start',
      animation: `${isUser ? 'userMessageReveal .72s' : 'messageReveal 1.04s'} ${T.ease} both`,
      width: '100%',
      ...style,
    }}>
      <div style={{
        gridColumn: 1,
        justifySelf: isUser ? 'end' : 'start',
        width: isUser ? 'fit-content' : '100%',
        maxWidth: isUser ? 'calc(100% - 52px)' : '100%',
        minWidth: 0,
        padding: isUser ? '10px 14px' : 0,
        borderRadius: isUser ? 16 : 0,
        background: isUser ? 'rgba(255,255,255,.88)' : 'transparent',
        color: isUser ? T.navyMid : T.navy,
        boxShadow: isUser ? '0 8px 18px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.84)' : 'none',
        border: isUser ? `1px solid ${T.hairlineSoft}` : 'none',
        fontSize: 14, lineHeight: 1.72, fontWeight: 440,
      }}>
        {children}
      </div>
      {isUser && (
        <div style={{ gridColumn: 2, justifySelf: 'end', paddingTop: 1 }}>
          <Avatar kind="user" />
        </div>
      )}
    </div>
  );
};

const NoriSays = ({ children, style }) => (
  <AgentReply style={style}>
    {children}
  </AgentReply>
);

const TypingDots = () => (
  <div style={{ display: 'inline-flex', gap: 3, padding: '4px 0' }}>
    {[0, 1, 2].map(i => (
      <span key={i} style={{
        width: 5, height: 5, borderRadius: '50%', background: T.navyLight,
        animation: `pulse 1.2s ${i * 0.15}s infinite`,
      }} />
    ))}
  </div>
);

const AGENT_CARD_WIDTH = 'min(100%, 664px)';

const NoriThinkingOnion = ({ style }) => (
  <div style={{
    width: AGENT_CARD_WIDTH,
    display: 'flex',
    alignItems: 'center',
    minHeight: 30,
    animation: `agentFadeIn .22s ${T.ease} both`,
    ...style,
  }}>
    <span style={{
      width: 20,
      height: 20,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      animation: 'agentOnionThink 1.18s ease-in-out infinite',
      transformOrigin: '50% 50%',
    }}>
      <img src={NORI_LOGO_SRC} alt="" style={{ width: 18, height: 18, objectFit: 'contain', display: 'block' }} />
    </span>
  </div>
);

const AgentParseLine = ({ messages = ['解析中'], active = true, style }) => {
  const [index, setIndex] = React.useState(0);
  React.useEffect(() => {
    if (!active || messages.length < 2) return undefined;
    const timer = window.setInterval(() => setIndex(i => (i + 1) % messages.length), 980);
    return () => window.clearInterval(timer);
  }, [active, messages.length]);
  return (
    <div style={{
      width: AGENT_CARD_WIDTH,
      height: 22,
      display: 'flex',
      alignItems: 'center',
      gap: 7,
      color: T.navyLight,
      fontSize: 12.2,
      lineHeight: 1,
      fontWeight: 560,
      whiteSpace: 'nowrap',
      overflow: 'hidden',
      textOverflow: 'ellipsis',
      animation: `agentFadeIn .28s ${T.ease} both`,
      ...style,
    }}>
      <span style={{ width: 6, height: 6, borderRadius: '50%', background: 'rgba(14,14,44,.22)', flexShrink: 0, animation: 'agentDotPulse 1s ease-in-out infinite' }} />
      <span key={index} style={{ overflow: 'hidden', textOverflow: 'ellipsis', animation: `agentTextSwap .36s ${T.ease} both` }}>{messages[index]}</span>
    </div>
  );
};

const AgentReply = ({ children, style }) => (
  <Bubble from="nori" style={{ width: AGENT_CARD_WIDTH, ...style }}>
    <div style={{
      paddingTop: 1,
      color: T.navyMid,
      fontSize: 13.4,
      lineHeight: 1.74,
      fontWeight: 460,
      whiteSpace: 'pre-wrap',
    }}>
      {children}
    </div>
  </Bubble>
);

const AgentCardShell = ({ label = 'Agent', icon = 'sparkles', title, children, action, defaultOpen = true, style, bodyStyle }) => {
  const [open, setOpen] = React.useState(defaultOpen);
  return (
    <section style={{
      width: AGENT_CARD_WIDTH,
      borderRadius: 20,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.82)',
      boxShadow: '0 14px 34px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.84)',
      backdropFilter: 'blur(18px) saturate(1.14)',
      padding: 15,
      display: 'grid',
      gap: open ? 12 : 0,
      animation: `messageReveal .72s ${T.ease} both`,
      ...style,
    }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 30px', gap: 10, alignItems: 'start' }}>
        <div style={{ minWidth: 0 }}>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, color: T.navyLight, fontSize: 11.2, lineHeight: 1.3, fontWeight: 650, marginBottom: 6 }}>
            <Icon name={icon} size={12} />
            {label}
          </div>
          {title && <h3 style={{ margin: 0, color: T.navy, fontSize: 15.2, lineHeight: 1.42, fontWeight: 730 }}>{title}</h3>}
        </div>
        <button onClick={() => setOpen(v => !v)} aria-label={open ? '折叠' : '展开'} style={{
          width: 30,
          height: 30,
          borderRadius: 10,
          border: `1px solid ${T.hairlineSoft}`,
          background: 'rgba(250,252,254,.74)',
          color: T.navyLight,
          cursor: 'pointer',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <Icon name={open ? 'chevronDown' : 'chevronRight'} size={13} />
        </button>
      </div>
      {open && (
        <>
          <div style={{ color: T.navyMid, fontSize: 12.9, lineHeight: 1.68, fontWeight: 460, ...bodyStyle }}>
            {children}
          </div>
          {action && <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8, flexWrap: 'wrap' }}>{action}</div>}
        </>
      )}
    </section>
  );
};

const AgentChoice = ({ children, active, multiple = false, onClick }) => (
  <button onClick={onClick} style={{
    minHeight: 34,
    borderRadius: 999,
    border: `1px solid ${active ? 'rgba(14,14,44,.16)' : T.hairlineSoft}`,
    background: active ? 'rgba(14,14,44,.92)' : 'rgba(255,255,255,.78)',
    color: active ? T.white : T.navyMid,
    cursor: 'pointer',
    display: 'inline-flex',
    alignItems: 'center',
    gap: 8,
    padding: '0 12px 0 10px',
    fontSize: 12.4,
    lineHeight: 1,
    fontWeight: active ? 690 : 560,
    boxShadow: active ? '0 10px 20px rgba(14,14,44,.12)' : '0 6px 14px rgba(14,14,44,.035)',
    transition: `transform .22s ${T.spring}, background .2s ${T.ease}, color .2s ${T.ease}, box-shadow .22s ${T.spring}`,
  }}>
    <span style={{
      width: 15,
      height: 15,
      borderRadius: multiple ? 5 : '50%',
      border: `1.4px solid ${active ? 'rgba(255,255,255,.76)' : 'rgba(14,14,44,.18)'}`,
      background: active ? T.primary : 'rgba(255,255,255,.58)',
      color: active ? T.navy : 'transparent',
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0,
    }}>
      {active && <Icon name="check" size={9} stroke={2.6} />}
    </span>
    {children}
  </button>
);

const AgentThinkingSequence = ({
  messages = ['正在查看', '解析中', '正在组织回复'],
  showOnion = true,
  showParse = true,
  children,
  style,
}) => (
  <div style={{ width: AGENT_CARD_WIDTH, display: 'grid', gap: 10, ...style }}>
    {showOnion && <NoriThinkingOnion />}
    {showParse && <AgentParseLine active messages={messages} />}
    {children}
  </div>
);

const PlanningThinkingSequence = AgentThinkingSequence;

const AgentParseFlow = ({
  messages = ['解析中', '正在分析你的内容', '正在整理结论'],
  conclusion = '已经完成解析',
  steps = [],
  active = true,
  showThinking = true,
  settled,
  initialOpen = false,
  resetKey,
  style,
}) => {
  const controlled = typeof settled === 'boolean';
  const [phase, setPhase] = React.useState(showThinking ? 0 : (settled ? 2 : 1));
  const [open, setOpen] = React.useState(initialOpen);
  const [messageIndex, setMessageIndex] = React.useState(0);

  React.useEffect(() => {
    if (!active) return undefined;
    if (controlled) {
      setPhase(showThinking ? 0 : settled ? 2 : 1);
      setMessageIndex(settled ? Math.max(0, messages.length - 1) : 0);
      const timers = [];
      if (showThinking && !settled) {
        timers.push(window.setTimeout(() => setPhase(1), 720));
      }
      if (!settled && messages.length > 1) {
        const msgTimer = window.setInterval(() => {
          setMessageIndex(i => (i + 1) % messages.length);
        }, 920);
        timers.push(msgTimer);
      }
      return () => timers.forEach(timer => {
        if (typeof timer === 'number') window.clearTimeout(timer);
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
        setMessageIndex(i => (i + 1) % messages.length);
      }, 920);
      timers.push(msgTimer);
    }
    timers.push(window.setTimeout(() => {
      setPhase(2);
      setMessageIndex(messages.length - 1);
    }, showThinking ? 720 + 920 * Math.max(1, Math.min(messages.length, 3)) : 920 * Math.max(1, Math.min(messages.length, 3))));
    return () => timers.forEach(timer => {
      if (typeof timer === 'number') window.clearTimeout(timer);
      else window.clearInterval(timer);
    });
  }, [active, showThinking, messages.length, resetKey, controlled, settled]);

  if (!active) return null;
  const currentMessage = phase === 0 ? null : phase === 1 ? messages[messageIndex] : conclusion;
  const detailSteps = steps.length ? steps : [
    { label: '理解输入', text: '读取用户刚刚提供的目标、素材和上下文。', note: '先锁定内容类型，再判断需要的下一步。' },
    { label: '匹配规则', text: '对照当前页面的任务阶段，判断下一步应该生成什么。', note: '避免把已知信息再问一遍。' },
    { label: '整理输出', text: '把可执行结论压缩成一条回复，并准备后续卡片内容。', note: '让回复和下一张卡之间的衔接更顺。' },
  ];

  return (
    <div style={{
      width: AGENT_CARD_WIDTH,
      display: 'grid',
      gap: 8,
      padding: '2px 0',
      ...style,
    }}>
      <div style={{ display: 'flex', alignItems: 'flex-start', gap: 7, color: T.navyLight }}>
        {phase === 0 ? (
          <span style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: T.iris,
            marginTop: 6,
            animation: 'agentDotPulse 0.9s ease-in-out 2',
            boxShadow: '0 0 0 0 rgba(75,77,237,.18)',
          }} />
        ) : (
          null
        )}
        <div style={{ minWidth: 0, flex: 1 }}>
          {phase >= 1 && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 5, minWidth: 0 }}>
              <div style={{
                color: T.navyLight,
                fontSize: 12.2,
                lineHeight: 1.5,
                fontWeight: 560,
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
              }}>
                {currentMessage}
              </div>
              <button onClick={() => setOpen(v => !v)} aria-label={open ? '折叠' : '展开'} style={{
                border: 'none',
                background: 'transparent',
                padding: 0,
                width: 16,
                height: 16,
                color: T.navyLight,
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                flexShrink: 0,
                opacity: phase >= 2 ? .88 : .42,
              }}>
                <Icon name={open ? 'chevronDown' : 'chevronRight'} size={11} />
              </button>
            </div>
          )}
          {open && phase >= 2 && (
            <div style={{
              marginTop: 9,
              paddingLeft: 12,
              borderLeft: `1px solid ${T.hairlineSoft}`,
              display: 'grid',
              gap: 8,
            }}>
              {detailSteps.map((step, index) => (
                <div key={`${step.label}-${index}`} style={{ display: 'grid', gap: 2, color: T.navyLight, fontSize: 12.1, lineHeight: 1.58, fontWeight: 520 }}>
                  <span>{index + 1} {step.label}：{step.text}</span>
                  {step.note && <span style={{ opacity: .72 }}>{step.note}</span>}
                </div>
              ))}
              <div style={{ color: T.navyLight, opacity: .62, fontSize: 11.8, lineHeight: 1.55 }}>
                已保留这一步的判断，后续生成会继续沿用。
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

const AgentStepSequence = ({
  parseMessages = ['正在查看', '解析中', '正在组织回复'],
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
  style,
}) => {
  const hasReply = reply !== undefined && reply !== null;
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

  return (
    <div style={{ width: AGENT_CARD_WIDTH, display: 'grid', gap: 12, ...style }}>
      {phase === 0 && <NoriThinkingOnion />}
      {phase >= 1 && showParse && (
        <AgentParseFlow
          showThinking={false}
          settled={phase >= 2}
          resetKey={resetKey}
          messages={parseMessages}
          conclusion={phase >= 3 ? (parseConclusion || parseMessages[parseMessages.length - 1] || '已经完成解析') : parseMessages[parseMessages.length - 1] || '已经完成解析'}
          steps={parseSteps}
          initialOpen={parseOpen}
        />
      )}
      {phase >= 2 && hasReply && <AgentReply>{reply}</AgentReply>}
      {phase >= 3 && cardNode && (
        <div style={{ width: AGENT_CARD_WIDTH, display: 'grid', gap: 12, animation: `messageReveal .84s ${T.ease} both` }}>
          {cardNode}
        </div>
      )}
    </div>
  );
};

const isNearScrollBottom = (node, threshold = 92) => {
  if (!node) return true;
  return node.scrollHeight - node.scrollTop - node.clientHeight < threshold;
};

const scrollNodeToBottom = (node, behavior = 'auto') => {
  if (!node) return;
  node.scrollTo({ top: node.scrollHeight, behavior });
};

/* ── Step 1: 关键信息确认 ── */
const Step1KeyInfo = ({ onComplete, onSkip }) => {
  const [audience, setAudience] = React.useState(null);
  const [style, setStyle] = React.useState(null);
  const [length, setLength] = React.useState(null);
  const ready = audience && style && length;

  const Question = ({ q, options, value, onPick, hint }) => (
    <div style={{ marginBottom: 18 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
        <span style={{ fontSize: 13.5, fontWeight: 600, color: T.navy }}>{q}</span>
        {hint && <span style={{ fontSize: 11.5, color: T.navyLight }}>{hint}</span>}
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
        {options.map(o => {
          const active = value === o.id;
          return (
            <button key={o.id} onClick={() => onPick(o.id)} style={{
              padding: '8px 14px', borderRadius: 99,
              border: `1px solid ${active ? T.navy : T.hairline}`,
              background: active ? T.navy : T.white,
              color: active ? T.white : T.navy,
              fontSize: 12.5, fontWeight: 500, cursor: 'pointer',
              display: 'inline-flex', alignItems: 'center', gap: 6,
              boxShadow: active ? '0 9px 22px rgba(14,14,44,.11)' : '0 5px 14px rgba(14,14,44,.035)',
              transition: `transform .24s ${T.spring}, background .22s ${T.ease}, color .22s ${T.ease}, box-shadow .24s ${T.spring}`,
            }}>
              {o.emoji && <span style={{ fontSize: 13 }}>{o.emoji}</span>}
              {o.label}
            </button>
          );
        })}
      </div>
    </div>
  );

  return (
    <NoriSays>
      <p style={{ marginBottom: 16 }}>
        好主意！「<b>猛男喜欢的粉色植物</b>」这个角度反差感很有梗。在开始前，
        我想跟你确认几个关键信息，这样生成的内容会更精准 ——
      </p>

      <div style={{
        background: 'rgba(255,255,255,.84)', border: `1px solid ${T.hairlineSoft}`,
        borderRadius: 18, padding: '18px 20px', boxShadow: '0 12px 28px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.82)',
        backdropFilter: 'blur(18px) saturate(1.12)',
      }}>
        <Question q="目标读者是谁？" hint="选一个最贴近的画像" value={audience} onPick={setAudience}
          options={[
            { id: 'novice', label: '植物新手', emoji: '🌱' },
            { id: 'cat-people', label: '宠物 / 室内派', emoji: '🐈' },
            { id: 'gym-bro', label: '健身硬汉', emoji: '💪' },
            { id: 'pro', label: '园艺老手', emoji: '🪴' },
            { id: 'all', label: '泛用户' },
          ]} />

        <Question q="你想做成什么风格？" value={style} onPick={setStyle}
          options={[
            { id: 'edu', label: '硬核科普' },
            { id: 'meme', label: '反差梗 / 整活' },
            { id: 'visual', label: '颜值向 / 美图' },
            { id: 'guide', label: '实用养护' },
          ]} />

        <Question q="期望长度？" value={length} onPick={setLength}
          options={[
            { id: 's', label: '短平快 · 6 图以内' },
            { id: 'm', label: '标准 · 8–10 图' },
            { id: 'l', label: '深度 · 长文 + 图' },
          ]} />

        <div style={{
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          marginTop: 6, paddingTop: 14, borderTop: `1px solid ${T.hairlineSoft}`,
        }}>
          <button onClick={onSkip} style={{
            background: 'transparent', border: 'none', cursor: 'pointer',
            color: T.navyLight, fontSize: 12.5, fontWeight: 500,
            display: 'inline-flex', alignItems: 'center', gap: 5, padding: '6px 4px',
          }}>
            <Icon name="skip" size={12} /> 跳过这步
          </button>
          <button onClick={() => onComplete({ audience, style, length })}
            disabled={!ready}
            style={{
              height: 38, padding: '0 18px', borderRadius: 10,
              border: 'none',
              background: ready ? T.navy : T.surface,
              color: ready ? T.primary : T.navyLight,
              fontSize: 13, fontWeight: 600, cursor: ready ? 'pointer' : 'not-allowed',
              display: 'inline-flex', alignItems: 'center', gap: 6,
              boxShadow: ready ? T.shadowSm : 'none',
              transition: `transform .24s ${T.spring}, box-shadow .24s ${T.spring}, background .22s ${T.ease}, color .22s ${T.ease}`,
            }}>
            <Icon name="sparkles" size={13} /> 开始生成
          </button>
        </div>
      </div>
    </NoriSays>
  );
};

/* ── Step 2: 拆解爆款 + 选题方案 ── */

const HotCard = ({ post }) => {
  return (
    <div style={{
      background: 'rgba(255,255,255,.86)', border: `1px solid ${T.hairlineSoft}`,
      borderRadius: 16, overflow: 'hidden',
      cursor: 'pointer', transition: `transform .3s ${T.spring}, box-shadow .3s ${T.spring}`,
      display: 'flex', flexDirection: 'column',
    }}
      onMouseEnter={e => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = T.shadowMd; }}
      onMouseLeave={e => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = 'none'; }}>
      <div style={{
        aspectRatio: '3 / 4', background: post.bg,
        position: 'relative', overflow: 'hidden',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        {/* placeholder visual */}
        {post.visual}
        <div style={{
          position: 'absolute', top: 8, left: 8,
          padding: '3px 7px', borderRadius: 99,
          background: 'rgba(14,14,44,.7)', color: T.white,
          fontSize: 10, fontWeight: 600, letterSpacing: '0.04em',
          display: 'inline-flex', alignItems: 'center', gap: 4,
          backdropFilter: 'blur(4px)',
        }}>
          <Icon name="trending" size={9} /> {post.platform}
        </div>
        <div style={{
          position: 'absolute', top: 8, right: 8,
          padding: '3px 7px', borderRadius: 4,
          background: T.primary, color: T.navy,
          fontSize: 10, fontWeight: 700,
        }}>{post.hotScore}</div>
      </div>
      <div style={{ padding: '12px 12px 12px' }}>
        <div style={{
          fontSize: 12.5, fontWeight: 600, color: T.navy,
          lineHeight: 1.45, marginBottom: 8,
          display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical',
          overflow: 'hidden',
        }}>{post.title}</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, fontSize: 11, color: T.navyLight }}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 3 }}>
            <Icon name="heart" size={11} /> {post.likes}
          </span>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 3 }}>
            <Icon name="bookmark" size={11} /> {post.saves}
          </span>
          <span style={{ marginLeft: 'auto', fontFamily: T.fontMono, fontSize: 10 }}>{post.time}</span>
        </div>
      </div>
    </div>
  );
};

/* placeholder visuals for the four hot posts */
const FlowerVisual = ({ palette }) => (
  <svg viewBox="0 0 100 130" width="100%" height="100%" style={{ display: 'block' }} preserveAspectRatio="xMidYMid slice">
    <rect width="100" height="130" fill={palette[0]} />
    {/* leaf */}
    <path d="M10 110 Q 5 70, 30 60 Q 55 50, 50 100 Q 45 130, 20 125 Z" fill={palette[1]} opacity=".85" />
    {/* flower clusters */}
    {[
      [40, 30, 18, palette[2]],
      [62, 45, 14, palette[3]],
      [55, 70, 16, palette[2]],
      [78, 28, 10, palette[3]],
      [30, 55, 11, palette[3]],
    ].map(([cx, cy, r, c], i) => (
      <g key={i}>
        {[0, 72, 144, 216, 288].map(a => {
          const rad = (a * Math.PI) / 180;
          return <ellipse key={a} cx={cx + Math.cos(rad) * r * 0.55} cy={cy + Math.sin(rad) * r * 0.55} rx={r * 0.6} ry={r * 0.45} fill={c} opacity={0.85} transform={`rotate(${a} ${cx} ${cy})`} />;
        })}
        <circle cx={cx} cy={cy} r={r * 0.25} fill={palette[4]} />
      </g>
    ))}
  </svg>
);

const Step2HotPosts = ({ onSelectAngle }) => {
  const posts = [
    {
      title: '深蓝幕布下的粉蝶兰，谁懂这种反差感',
      platform: '小红书', hotScore: 'HOT 9.2',
      likes: '5.6w', saves: '2.6w', time: '2 天前',
      bg: '#1a3a5c',
      visual: <FlowerVisual palette={['#1a3a5c', '#2c5a3c', '#f5b8c8', '#e896b0', '#fdf5f5']} />,
    },
    {
      title: '硬汉养花指北 · 8 种粉得直男都爱的植物',
      platform: '小红书', hotScore: 'HOT 8.8',
      likes: '4.2w', saves: '1.9w', time: '5 天前',
      bg: '#2a1a2e',
      visual: <FlowerVisual palette={['#2a1a2e', '#3c5a4c', '#fab1c4', '#f78bb0', T.peachTint]} />,
    },
    {
      title: '不养仙人掌后，我家粉色植物收藏 Top 6',
      platform: '小红书', hotScore: 'HOT 8.5',
      likes: '3.8w', saves: '1.5w', time: '1 周前',
      bg: '#fdf0ee',
      visual: <FlowerVisual palette={['#fdf0ee', '#9bbfa8', '#e8a0bc', '#d987a8', '#fff']} />,
    },
    {
      title: '阳台改造 | 把粉红仙境搬回家 ¥300 搞定',
      platform: '小红书', hotScore: 'HOT 7.9',
      likes: '3.1w', saves: '1.2w', time: '2 周前',
      bg: '#3a2c4a',
      visual: <FlowerVisual palette={['#3a2c4a', '#5c7a5c', '#f0a8c4', '#dc8aa8', '#fff']} />,
    },
  ];

  const [openConclusion, setOpenConclusion] = React.useState(false);
  const [phase, setPhase] = React.useState(0);

  React.useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 1000),
      setTimeout(() => setPhase(2), 2600),
      setTimeout(() => setPhase(3), 4300),
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <>
      <NoriSays>
        <p style={{ marginBottom: 14 }}>
          收到，开始动了 ✨ 我先去小红书 / 抖音上扒了一圈 <b>粉色植物</b> 相关爆款，
          这个话题有真实的流量盘子，近 30 天爆款 200+ 篇，收藏评论表现持续走高，
          <span style={{ color: T.success, fontWeight: 600 }}>「可打造为爆款」诊断通过</span>。
        </p>
        <p style={{ marginBottom: 14, color: T.navyMid }}>
          下面是 4 篇可参考的爆款，已按选题贴合度排序 ——
        </p>
        {phase === 0 && <TypingDots />}
      </NoriSays>

      {phase >= 1 && (
      <div style={{ marginLeft: 38, marginTop: -6, animation: 'fadeIn .28s ease' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginBottom: 14 }}>
          {posts.map((p, i) => <HotCard key={i} post={p} />)}
        </div>
        <button style={{
          fontSize: 12, color: T.navyMid, background: 'transparent',
          border: 'none', cursor: 'pointer', padding: '4px 0',
          fontWeight: 500, display: 'inline-flex', alignItems: 'center', gap: 4,
        }}>
          查看其余 21 篇爆款 <Icon name="chevronRight" size={11} />
        </button>
      </div>
      )}

      {/* 拆解 */}
      {phase >= 2 && (
      <NoriSays style={{ marginTop: 22 }}>
        <p style={{ marginBottom: 14 }}>我把这些爆款的共同结构拆给你看 ——</p>
        <div style={{
          background: 'rgba(255,255,255,.86)', border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 16, padding: '4px 0', overflow: 'hidden',
          boxShadow: '0 10px 24px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)',
        }}>
          {[
            { label: '标题公式', body: '「反差词 + 具体植物 + 情绪/态度」 例如「猛男 / 直男 + 粉色植物 + 谁懂这种反差感」', icon: 'edit' },
            { label: '封面参考', body: '深色背景 +  单株植物特写 + 极简留白；冷暖反差是关键，避免甜腻', icon: 'image' },
            { label: '内文长度', body: '8 张图 / 600–800 字。「人设钩子 → 6 种植物 → 养护 Tips → 互动结尾」', icon: 'document' },
            { label: '互动钩子', body: '结尾抛 1 个具体问题：「你家有几盆？」「猛男能 hold 几种？」', icon: 'chat' },
          ].map((row, i, arr) => (
            <div key={i} style={{
              display: 'flex', alignItems: 'flex-start', gap: 14,
              padding: '14px 18px',
              borderBottom: i < arr.length - 1 ? `1px solid ${T.hairlineSoft}` : 'none',
            }}>
              <div style={{
                width: 28, height: 28, borderRadius: 8,
                background: T.irisTint, color: T.iris,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                flexShrink: 0, marginTop: 1,
              }}>
                <Icon name={row.icon} size={14} />
              </div>
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: 12, fontWeight: 700, letterSpacing: '0.04em', color: T.navy, marginBottom: 4, textTransform: 'uppercase' }}>
                  {row.label}
                </div>
                <div style={{ fontSize: 13, color: T.navyMid, lineHeight: 1.6 }}>{row.body}</div>
              </div>
            </div>
          ))}
        </div>
      </NoriSays>
      )}

      {/* 选题结论卡片 */}
      {phase >= 3 && (
      <NoriSays style={{ marginTop: 22 }}>
        <p style={{ marginBottom: 14 }}>
          综合上面的拆解，我给你的选题结论是 ——
          <span style={{ color: T.navyLight, fontSize: 12.5 }}>（点击后进入封面选择）</span>
        </p>
        <button onClick={() => onSelectAngle()} style={{
          width: '100%', textAlign: 'left',
          background: 'rgba(255,255,255,.86)', border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 16, padding: '14px 18px',
          display: 'flex', alignItems: 'center', gap: 14,
          cursor: 'pointer', transition: `transform .3s ${T.spring}, box-shadow .3s ${T.spring}, border .22s ${T.ease}`,
          boxShadow: '0 10px 24px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)',
        }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(75,77,237,.32)'; e.currentTarget.style.boxShadow = T.shadowSm; }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = T.hairlineSoft; e.currentTarget.style.boxShadow = '0 10px 24px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)'; }}>
          <div style={{
            width: 44, height: 44, borderRadius: 10,
            background: T.primary, color: T.navy,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            flexShrink: 0,
          }}>
            <Icon name="target" size={22} />
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 14, fontWeight: 700, color: T.navy, marginBottom: 2 }}>
              选题结论 · 反差人设 + 6 种粉色植物种草
            </div>
            <div style={{ fontSize: 12, color: T.navyLight }}>
              小红书图文 · 8 张图 · 高收藏方向 · Nori 推荐
            </div>
          </div>
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: 6,
            padding: '6px 12px', borderRadius: 8,
            background: T.surface, color: T.navy,
            fontSize: 12, fontWeight: 600,
          }}>
            <Icon name="expand" size={12} /> 在 Canvas 查看
          </div>
        </button>
      </NoriSays>
      )}
    </>
  );
};

/* ── Step 3: 素材调研 ── */

const SourceRow = ({ source, idx }) => {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 12,
      padding: '10px 14px', borderRadius: 10,
      cursor: 'pointer', transition: 'background .12s',
    }}
      onMouseEnter={e => e.currentTarget.style.background = T.surface}
      onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
      <div style={{
        width: 24, height: 24, borderRadius: 6,
        background: source.tint, color: source.color,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        flexShrink: 0,
      }}>
        <Icon name={source.icon} size={12} />
      </div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: 12.5, fontWeight: 500, color: T.navy, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
          {source.title}
        </div>
        <div style={{ fontSize: 10.5, color: T.navyLight, fontFamily: T.fontMono }}>
          {source.host} · {source.kind}
        </div>
      </div>
      <Icon name="link" size={12} color={T.navyLight} />
    </div>
  );
};

const Step3Research = ({ selectedAsset, onSelectAsset }) => {
  const [imgsExpanded, setImgsExpanded] = React.useState(false);
  const [phase, setPhase] = React.useState(0);

  const sources = [
    { title: '《观赏植物色素分布与花色稳定性研究》', host: 'cnki.net', kind: 'PDF · 论文', icon: 'book', tint: T.irisTint, color: T.iris },
    { title: '粉掌、姬秋丽、花叶冷水花养护要点', host: 'huayuan.com', kind: '科普文章', icon: 'document', tint: '#fff8e0', color: '#c89b00' },
    { title: 'Pink Plants Care Guide 2025', host: 'gardenista.com', kind: '英文 Guide', icon: 'globe', tint: T.successTint, color: T.success },
    { title: '【粉色植物 Top10】完整盘点', host: 'bilibili.com', kind: '视频 · 7:32', icon: 'play', tint: '#ffe5ec', color: '#ff4488' },
  ];

  /* image grid: 4 highlighted + 8 hidden */
  const Img = ({ asset, featured }) => (
    <div style={{
      borderRadius: 10, overflow: 'hidden',
      background: asset.palette[0], aspectRatio: '1 / 1.25',
      cursor: 'pointer', transition: 'transform .15s',
      position: 'relative',
      outline: selectedAsset?.id === asset.id ? `2px solid ${T.primary}` : 'none',
      boxShadow: selectedAsset?.id === asset.id ? '0 0 0 5px rgba(214,255,0,.14)' : 'none',
    }}
      onClick={() => onSelectAsset && onSelectAsset(asset)}
      onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.02)'}
      onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}>
      <FlowerVisual palette={asset.palette} />
      <div style={{
        position: 'absolute', top: 6, right: 6,
        width: 22, height: 22, borderRadius: 6,
        background: selectedAsset?.id === asset.id ? T.primary : 'rgba(0,0,0,.5)', color: selectedAsset?.id === asset.id ? T.navy : T.white,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        backdropFilter: 'blur(4px)', opacity: selectedAsset?.id === asset.id ? 1 : 0,
        transition: 'opacity .15s, background .15s',
      }}>
        <Icon name={selectedAsset?.id === asset.id ? 'check' : 'expand'} size={11} />
      </div>
      {featured && <div style={{
        position: 'absolute', top: 6, left: 6,
        fontSize: 9, fontWeight: 700, letterSpacing: '0.04em',
        color: T.navy, background: T.primary,
        padding: '2px 6px', borderRadius: 4,
      }}>★ TOP {featured}</div>}
      {selectedAsset?.id === asset.id && (
        <div style={{
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
          backdropFilter: 'blur(8px)',
        }}>
          已用于右侧预览
        </div>
      )}
    </div>
  );

  const assets = [
    { id: 'asset-1', label: '幕布光影', shape: 'ribbon', rotate: -4, palette: ['#1a3a5c', '#2c5a3c', '#f5b8c8', '#e896b0', '#fdf5f5'] },
    { id: 'asset-2', label: '夜色花影', shape: 'petal', rotate: 3, palette: ['#2a1a2e', '#3c5a4c', '#fab1c4', '#f78bb0', T.peachTint] },
    { id: 'asset-3', label: '奶油清晨', shape: 'bloom', rotate: -2, palette: ['#fdf0ee', '#9bbfa8', '#e8a0bc', '#d987a8', '#fff'] },
    { id: 'asset-4', label: '紫调反差', shape: 'ribbon', rotate: 4, palette: ['#3a2c4a', '#5c7a5c', '#f0a8c4', '#dc8aa8', '#fff'] },
    { id: 'asset-5', label: '海盐深蓝', shape: 'petal', rotate: -3, palette: ['#0e2a3a', '#3c4a3c', '#ffb8c8', '#ff8aa8', '#fff'] },
    { id: 'asset-6', label: '莓果晚风', shape: 'bloom', rotate: 4, palette: ['#2c1a3a', '#5c3c5c', '#f8a8c0', '#e890b0', '#fff'] },
    { id: 'asset-7', label: '雾粉白昼', shape: 'ribbon', rotate: -2, palette: ['#fce5ec', '#a8c8a8', '#dc8aa8', '#b86890', '#fff'] },
    { id: 'asset-8', label: '森林幕墙', shape: 'petal', rotate: 3, palette: ['#1a2a3a', '#5c7a4c', '#f0c0d0', '#e090b0', '#fff'] },
    { id: 'asset-9', label: '酒红场景', shape: 'bloom', rotate: -4, palette: ['#3a1a2a', '#4c5a4c', '#ffa0c0', '#d088a8', '#fff'] },
    { id: 'asset-10', label: '柔粉留白', shape: 'ribbon', rotate: 2, palette: ['#fdf5f5', '#88aa88', '#e890a8', '#b87090', '#fff'] },
    { id: 'asset-11', label: '雾蓝暗涌', shape: 'petal', rotate: -3, palette: ['#22334a', '#4a6a4a', '#fcb4cc', '#e088a8', '#fff'] },
    { id: 'asset-12', label: '暮色花房', shape: 'bloom', rotate: 3, palette: ['#2a2a3c', '#5a7a5a', '#f8a0c0', '#cc7898', '#fff'] },
  ];

  React.useEffect(() => {
    if (!selectedAsset && phase >= 2 && onSelectAsset) onSelectAsset(assets[0]);
  }, [phase, selectedAsset, onSelectAsset]);

  React.useEffect(() => {
    const timers = [
      setTimeout(() => setPhase(1), 1100),
      setTimeout(() => setPhase(2), 2800),
      setTimeout(() => setPhase(3), 4500),
    ];
    return () => timers.forEach(clearTimeout);
  }, []);

  return (
    <>
      <NoriSays>
        <p style={{ marginBottom: 14 }}>
          策略定了，我开始为你调研素材。先扒了一圈学术论文 + 科普文章 + 视频 ——
        </p>
        {phase === 0 && <TypingDots />}
        {phase >= 1 && (
        <div style={{
          background: 'rgba(255,255,255,.86)', border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 16, padding: 6, overflow: 'hidden',
          animation: `fadeIn .32s ${T.spring}`,
          boxShadow: '0 10px 24px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)',
        }}>
          {sources.map((s, i) => <SourceRow key={i} source={s} idx={i} />)}
        </div>
        )}
        {phase >= 1 && (
        <button style={{
          marginTop: 8, fontSize: 12, color: T.navyMid,
          background: 'transparent', border: 'none', cursor: 'pointer',
          fontWeight: 500, display: 'inline-flex', alignItems: 'center', gap: 4, padding: '4px 0',
        }}>
          查看其余 5 个来源 <Icon name="chevronDown" size={11} />
        </button>
        )}
      </NoriSays>

      {phase >= 2 && (
      <NoriSays style={{ marginTop: 22 }}>
        <p style={{ marginBottom: 12 }}>
          再扒了一些粉色植物的图片素材 —— 高亮的这 4 张是我觉得封面 / 主图最能用的：
        </p>
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8,
          animation: 'fadeIn .28s ease',
        }}>
          {assets.slice(0, 4).map((asset, i) => <Img key={asset.id} asset={asset} featured={i + 1} />)}
        </div>

        {imgsExpanded && (
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8,
            marginTop: 8, animation: 'fadeIn .3s ease',
          }}>
            {assets.slice(4).map(asset => <Img key={asset.id} asset={asset} />)}
          </div>
        )}

        <button onClick={() => setImgsExpanded(v => !v)} style={{
          marginTop: 12, fontSize: 12, color: T.navyMid,
          background: 'transparent', border: 'none', cursor: 'pointer',
          fontWeight: 500, display: 'inline-flex', alignItems: 'center', gap: 4, padding: '4px 0',
        }}>
          {imgsExpanded ? '收起' : `查看其余 ${assets.length - 4} 张图片`}
          <Icon name={imgsExpanded ? 'chevronDown' : 'chevronRight'} size={11} />
        </button>

        {phase >= 3 && (
        <div style={{
          marginTop: 14, display: 'inline-flex', alignItems: 'center', gap: 6,
          padding: '6px 12px', borderRadius: 99,
          background: T.successTint, color: T.success,
          fontSize: 12, fontWeight: 600,
          animation: 'fadeIn .26s ease',
        }}>
          <Icon name="check" size={12} /> 素材搜集完成 · 9 篇资料 + 12 张图
        </div>
        )}
      </NoriSays>
      )}
    </>
  );
};

/* ── Step 4: 内容生成 TODO 列表 ── */

const Step4Generate = ({ onAllDone, onRevealCanvas }) => {
  const tasks = [
    { id: 't1', label: '生成标题与正文中', sub: '反差钩子 + 6 种植物 + 养护 Tips' },
    { id: 't2', label: '生成图片卡片中', sub: '8 张图 · 封面 + 内页 + 互动页' },
    { id: 't3', label: '排版优化中', sub: '小红书图文格式 · emoji 与排版' },
    { id: 't4', label: '一致性校对中', sub: '术语 · 风格 · 标点统一' },
  ];
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
      setDone(d => ({ ...d, [tasks[current].id]: true }));
      setCurrent(c => c + 1);
    }, 1400);
    return () => clearTimeout(t);
  }, [current]);

  return (
    <NoriSays>
      <p style={{ marginBottom: 14 }}>
        所有准备就绪，开始生成内容了 —— 你可以在右边 Canvas 实时预览：
      </p>
      <div style={{
        background: 'rgba(255,255,255,.86)', border: `1px solid ${T.hairlineSoft}`,
        borderRadius: 16, padding: '12px 16px', overflow: 'hidden',
        boxShadow: '0 10px 24px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)',
      }}>
        {tasks.map((t, i) => {
          const isDone = done[t.id];
          const isActive = current === i && !isDone;
          return (
            <div key={t.id} style={{
              display: 'flex', alignItems: 'center', gap: 12,
              padding: '10px 0',
              borderBottom: i < tasks.length - 1 ? `1px solid ${T.hairlineSoft}` : 'none',
            }}>
              <div style={{
                width: 22, height: 22, borderRadius: 6,
                border: `1.5px solid ${isDone ? T.success : T.navySoft}`,
                background: isDone ? T.success : T.white,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                flexShrink: 0,
                position: 'relative',
                animation: isDone ? 'checkPop .35s ease' : 'none',
              }}>
                {isDone && <Icon name="check" size={12} color={T.white} stroke={2.5} />}
                {isActive && (
                  <div style={{
                    position: 'absolute', inset: -3,
                    border: `2px solid ${T.iris}`, borderTopColor: 'transparent',
                    borderRadius: 8, animation: 'spin 0.9s linear infinite',
                  }} />
                )}
              </div>
              <div style={{ flex: 1 }}>
                <div style={{
                  fontSize: 13, fontWeight: 600,
                  color: isDone ? T.navyLight : T.navy,
                  textDecoration: isDone ? 'line-through' : 'none',
                }}>{t.label}</div>
                <div style={{ fontSize: 11, color: T.navyLight, marginTop: 1 }}>{t.sub}</div>
              </div>
              {isActive && (
                <span style={{ fontSize: 11, color: T.iris, fontWeight: 600, animation: 'pulse 1.4s infinite' }}>进行中…</span>
              )}
              {isDone && (
                <span style={{ fontSize: 11, color: T.success, fontWeight: 600 }}>完成</span>
              )}
            </div>
          );
        })}
      </div>

      {allDone && (
        <button
          onClick={() => onRevealCanvas && onRevealCanvas()}
          style={{
          marginTop: 14, display: 'flex', alignItems: 'center', gap: 10,
          padding: '12px 16px', borderRadius: 12,
          background: `linear-gradient(90deg, ${T.primary} 0%, #edff7a 42%, ${T.successTint} 72%, #f8ffcc 100%)`,
          backgroundSize: '220% 100%',
          color: T.navy, fontWeight: 600, fontSize: 13.5,
          animation: `doneButtonReveal 1.35s ${T.spring} both, doneButtonGlow 1.4s ease-in-out .12s 2`,
          position: 'relative', overflow: 'hidden',
          width: '100%',
          border: 'none',
          cursor: 'pointer',
          justifyContent: 'space-between',
          textAlign: 'left',
          boxShadow: '0 12px 30px rgba(214,255,0,.22)',
          transition: `transform .28s ${T.spring}, box-shadow .28s ${T.spring}`,
        }}>
          <span style={{
            position: 'absolute',
            inset: 0,
            background: 'linear-gradient(110deg, transparent 0%, rgba(255,255,255,.72) 48%, transparent 62%)',
            transform: 'translateX(-120%)',
            animation: `doneButtonSweep 1.1s ${T.spring} .16s both`,
            pointerEvents: 'none',
          }} />
          <span>全部完成！内容已就绪，去 Canvas 看看吧</span>
          <span style={{
            width: 30,
            height: 30,
            borderRadius: '50%',
            background: 'rgba(14,14,44,.08)',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexShrink: 0,
          }}>
            <Icon name="chevronRight" size={14} color={T.navy} />
          </span>
        </button>
      )}
    </NoriSays>
  );
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

const PhoneFrame = ({ children }) => (
  <div style={{
    position: 'relative',
    width: 'min(356px, 100%)',
    height: 704,
    margin: '0 auto',
    filter: 'drop-shadow(0 30px 58px rgba(14,14,44,.18))',
  }}>
    <div style={{
      position: 'absolute',
      inset: 0,
      borderRadius: 55,
      background: 'linear-gradient(145deg, #fbfbfc, #d9dce2)',
      boxShadow: 'inset 0 0 0 1px rgba(14,14,44,.12), inset 0 0 0 3px rgba(255,255,255,.72)',
    }} />
    <span style={{
      position: 'absolute',
      left: -5,
      top: 164,
      width: 4,
      height: 46,
      borderRadius: '4px 0 0 4px',
      background: 'linear-gradient(180deg, #d5d8df, #f8f8fa)',
      boxShadow: '0 98px 0 #e4e6eb, 0 157px 0 #e4e6eb',
    }} />
    <span style={{
      position: 'absolute',
      right: -46,
      top: 315,
      width: 44,
      height: 44,
      borderRadius: '50%',
      background: 'linear-gradient(145deg, #f5f6f8, #dfe2e7)',
      border: '1px solid rgba(14,14,44,.08)',
      boxShadow: '0 9px 18px rgba(14,14,44,.10), inset 0 1px 0 rgba(255,255,255,.8)',
    }} />
    <div style={{
      position: 'absolute',
      inset: 8,
      borderRadius: 49,
      background: '#050507',
      boxShadow: 'inset 0 0 0 1px rgba(255,255,255,.10)',
    }} />
    <div style={{
      position: 'absolute',
      left: '50%',
      top: 18,
      width: 122,
      height: 34,
      transform: 'translateX(-50%)',
      borderRadius: '0 0 19px 19px',
      background: '#050507',
      zIndex: 5,
    }} />
    <div style={{
      position: 'absolute',
      left: 17,
      right: 17,
      top: 17,
      bottom: 17,
      borderRadius: 39,
      overflow: 'hidden',
      background: '#fff',
    }}>
      {children}
    </div>
  </div>
);

const CanvasDocumentEditor = ({ data, onSetData }) => (
  <article style={{
    width: 'min(720px, 100%)',
    minHeight: 'calc(100vh - 188px)',
    background: 'rgba(255,255,255,.82)',
    border: `1px solid ${T.hairlineSoft}`,
    borderRadius: 16,
    boxShadow: '0 18px 44px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.84)',
    padding: '50px min(7vw, 62px) 58px',
    color: T.navy,
  }}>
    <EditableText tag="h1" onChange={v => onSetData({ ...data, title: v })}
      style={{ fontSize: 26, lineHeight: 1.28, fontWeight: 680, letterSpacing: 0, margin: '0 0 18px', color: T.navy }}>
      {data.title}
    </EditableText>

    <EditableText tag="h2" onChange={v => onSetData({ ...data, hook: v })}
      style={{ fontSize: 17, lineHeight: 1.58, fontWeight: 620, margin: '0 0 14px', color: T.navy }}>
      {data.hook}
    </EditableText>
    <EditableText tag="p" onChange={v => onSetData({ ...data, intro: v })}
      style={{ fontSize: 14.6, lineHeight: 1.86, margin: '0 0 26px', color: T.navyMid }}>
      {data.intro}
    </EditableText>

    <div style={{ display: 'grid', gap: 18 }}>
      {data.items.map((it, i) => (
        <section key={i}>
          <EditableText tag="h3" onChange={v => {
            const items = [...data.items]; items[i] = { ...it, name: v };
            onSetData({ ...data, items });
          }} style={{ fontSize: 15.8, fontWeight: 650, lineHeight: 1.55, margin: '0 0 5px', color: T.navy }}>
            {i + 1}. {it.name}
          </EditableText>
          <EditableText tag="p" onChange={v => {
            const items = [...data.items]; items[i] = { ...it, desc: v };
            onSetData({ ...data, items });
          }} style={{ fontSize: 14.2, lineHeight: 1.86, color: T.navyMid, margin: 0 }}>
            {it.desc}
          </EditableText>
        </section>
      ))}
    </div>

    <EditableText tag="p" onChange={v => onSetData({ ...data, cta: v })}
      style={{ margin: '28px 0 0', fontSize: 14.8, fontWeight: 600, lineHeight: 1.82, color: T.navy }}>
      {data.cta}
    </EditableText>

    <div style={{ marginTop: 22, color: T.navyLight, fontSize: 12.5, lineHeight: 1.7 }}>
      {data.tags.map(tag => `#${tag}`).join('  ')}
    </div>
  </article>
);

const CanvasToolbar = ({ onClose, onTransform, onPublish, mode, setMode, expanded, setExpanded, collapsed, onToggleCollapse }) => {
  const Btn = ({ icon, label, onClick, primary, accent, active, children, muted }) => {
    const [hov, setHov] = React.useState(false);
    const bg = primary
      ? 'linear-gradient(135deg, #5c62ef, #6c6ff2)'
      : active
        ? (accent === 'green' ? 'rgba(49,208,170,.18)' : 'rgba(75,77,237,.12)')
      : muted
        ? (hov ? 'rgba(14,14,44,.08)' : 'rgba(14,14,44,.045)')
      : accent === 'green'
        ? (hov ? 'rgba(49,208,170,.18)' : 'rgba(49,208,170,.10)')
        : accent === 'purple'
          ? (hov ? 'rgba(75,77,237,.14)' : 'rgba(75,77,237,.08)')
          : (hov ? 'rgba(14,14,44,.09)' : 'rgba(14,14,44,.045)');
    return (
      <button onClick={(e) => onClick?.(e.currentTarget.getBoundingClientRect())}
        onMouseEnter={() => setHov(true)} onMouseLeave={() => setHov(false)}
        style={{
          height: label ? 42 : 40,
          minWidth: label ? (label === '编辑正文' || label === '手机预览' ? 106 : 92) : 40,
          padding: label ? '0 16px' : 0,
          borderRadius: label ? 15 : 14,
          border: primary ? 'none' : `1px solid ${active ? 'rgba(49,208,170,.16)' : 'rgba(14,14,44,.075)'}`,
          cursor: 'pointer',
          background: bg,
          color: primary ? T.white : T.navy,
          fontSize: 13, fontWeight: 700,
          display: 'inline-flex', alignItems: 'center', gap: 6,
          justifyContent: 'center',
          whiteSpace: 'nowrap',
          flexWrap: 'nowrap',
          lineHeight: 1,
          transition: 'transform .16s cubic-bezier(.2,.8,.2,1), box-shadow .16s cubic-bezier(.2,.8,.2,1), background .16s cubic-bezier(.2,.8,.2,1)',
          boxShadow: primary ? '0 12px 24px rgba(75,77,237,.22)' : '0 6px 14px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.72)',
        }}>
        {icon && <Icon name={icon} size={label ? 16 : 15} />}
        {label}
        {children}
      </button>
    );
  };

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '7px 8px',
      background: 'rgba(251,252,255,.88)',
      borderRadius: 19,
      boxShadow: '0 14px 34px rgba(14,14,44,.09), inset 0 1px 0 rgba(255,255,255,.86)',
      gap: 7,
      backdropFilter: 'blur(18px)',
      border: '1px solid rgba(255,255,255,.76)',
    }}>
      <Btn icon="phone" label="手机预览" accent="green" active={mode === 'preview'} onClick={() => { setExpanded(true); setMode('preview'); }} />
    </div>
  );
};

/* Floating text-edit menu — appears when text is selected */
const TextSelectionMenu = ({ pos, onAction, onClose }) => {
  if (!pos) return null;
  const actions = [
    { id: 'rewrite', label: '改写', icon: 'edit' },
    { id: 'expand', label: '扩展', icon: 'plus' },
    { id: 'simplify', label: '简化', icon: 'minus' },
    { id: 'tone', label: '调整语气', icon: 'sliders' },
  ];
  return (
    <div style={{
      position: 'absolute', top: pos.y, left: pos.x,
      transform: 'translate(-50%, -100%)',
      background: T.navy, color: T.white, borderRadius: 10,
      padding: 4, display: 'flex', gap: 2,
      boxShadow: T.shadowLg, zIndex: 50,
      animation: 'fadeIn .15s ease',
    }}>
      {actions.map(a => (
        <button key={a.id} onClick={() => onAction(a.id)} style={{
          padding: '6px 10px', borderRadius: 6,
          background: 'transparent', color: T.white,
          border: 'none', cursor: 'pointer',
          fontSize: 12, fontWeight: 500,
          display: 'inline-flex', alignItems: 'center', gap: 5,
        }}
          onMouseEnter={e => e.currentTarget.style.background = 'rgba(255,255,255,.12)'}
          onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
          <Icon name={a.icon} size={12} /> {a.label}
        </button>
      ))}
    </div>
  );
};

/* Editable text */
const EditableText = ({ tag = 'p', children, onChange, style }) => {
  const ref = React.useRef(null);
  return React.createElement(tag, {
    ref,
    contentEditable: true,
    suppressContentEditableWarning: true,
    onBlur: e => onChange && onChange(e.currentTarget.innerText),
    style: { outline: 'none', cursor: 'text', ...style },
    spellCheck: false,
  }, children);
};

/* The mock generated post — small-red-book style */
const PostPreview = ({ data, onSetData, onSelectText, selectedAsset }) => {
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
  const coverPalette = selectedAsset?.palette || ['#1a3a5c', '#2c5a3c', '#f5b8c8', '#e896b0', '#fdf5f5'];
  const coverShape = selectedAsset?.shape || 'petal';
  const coverRotate = selectedAsset?.rotate || 0;
  const coverLabel = selectedAsset?.label || '精选素材';
  const clipPaths = {
    petal: 'polygon(12% 16%, 34% 9%, 46% 0%, 60% 12%, 81% 8%, 100% 22%, 93% 44%, 100% 71%, 82% 88%, 61% 84%, 44% 100%, 22% 92%, 0% 74%, 7% 48%, 0% 24%)',
    ribbon: 'polygon(6% 7%, 44% 0%, 64% 9%, 100% 4%, 90% 38%, 100% 65%, 83% 100%, 46% 92%, 26% 100%, 0% 81%, 9% 48%, 0% 17%)',
    bloom: 'polygon(11% 0%, 38% 8%, 58% 0%, 74% 15%, 100% 17%, 94% 50%, 100% 80%, 76% 100%, 49% 93%, 30% 100%, 0% 82%, 8% 51%, 0% 18%)',
  };

  return (
    <div onMouseUp={handleMouseUp} style={{
      width: '100%',
      height: '100%',
      background: T.white,
      overflowY: 'auto',
      overflowX: 'hidden',
      position: 'relative',
      WebkitOverflowScrolling: 'touch',
    }}>
      <div style={{
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
        backdropFilter: 'blur(10px)',
      }}>
        <span>9:41</span>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6, color: 'rgba(14,14,44,.72)' }}>
          <span style={{ width: 14, height: 9, borderRadius: 3, border: '1.8px solid currentColor', position: 'relative', display: 'inline-block' }}>
            <span style={{ position: 'absolute', inset: 1.5, borderRadius: 1.5, background: 'currentColor' }} />
          </span>
          <span style={{ width: 14, height: 10, display: 'inline-flex', alignItems: 'flex-end', gap: 1 }}>
            {[4, 6, 8, 10].map((h, i) => <span key={i} style={{ width: 2, height: h, borderRadius: 2, background: 'currentColor', display: 'inline-block' }} />)}
          </span>
        </div>
      </div>

      {/* Cover */}
      <div style={{
        aspectRatio: '3 / 4', background: '#1a3a5c',
        position: 'relative', overflow: 'hidden',
      }}>
        <FlowerVisual palette={coverPalette} />
        <div style={{
          position: 'absolute',
          right: 18,
          top: 18,
          width: 110,
          transform: `rotate(${coverRotate}deg)`,
        }}>
          <div style={{
            aspectRatio: '0.82 / 1',
            clipPath: clipPaths[coverShape],
            overflow: 'hidden',
            boxShadow: '0 18px 34px rgba(14,14,44,.24)',
            border: '1px solid rgba(255,255,255,.28)',
          }}>
            <FlowerVisual palette={coverPalette} />
          </div>
          <div style={{
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
            textTransform: 'uppercase',
          }}>
            <Icon name="image" size={10} color="currentColor" />
            {coverLabel}
          </div>
        </div>
        <div style={{
          position: 'absolute', inset: 0,
          padding: 22, display: 'flex', flexDirection: 'column', justifyContent: 'flex-end',
          background: 'linear-gradient(to top, rgba(0,0,0,.55), transparent 50%)',
        }}>
          <EditableText tag="div" onChange={v => onSetData({ ...data, title: v })}
            style={{
              color: T.white, fontSize: 26, fontWeight: 700,
              lineHeight: 1.2, letterSpacing: '-0.01em',
              textShadow: '0 2px 8px rgba(0,0,0,.3)',
            }}>
            {data.title}
          </EditableText>
          <div style={{ marginTop: 10, display: 'flex', alignItems: 'center', gap: 6 }}>
            {data.tags.map((t, i) => (
              <span key={i} style={{
                fontSize: 10.5, fontWeight: 600,
                color: T.white, background: 'rgba(255,255,255,.15)',
                padding: '3px 8px', borderRadius: 99,
                backdropFilter: 'blur(6px)',
                border: '1px solid rgba(255,255,255,.2)',
              }}>#{t}</span>
            ))}
          </div>
        </div>
      </div>

      {/* Body */}
      <div style={{ padding: '18px 20px 30px' }}>
        <EditableText tag="h3" onChange={v => onSetData({ ...data, hook: v })}
          style={{ fontSize: 16, fontWeight: 700, color: T.navy, marginBottom: 10, lineHeight: 1.4 }}>
          {data.hook}
        </EditableText>

        <EditableText tag="p" onChange={v => onSetData({ ...data, intro: v })}
          style={{ fontSize: 13.5, color: T.navyMid, lineHeight: 1.75, marginBottom: 16 }}>
          {data.intro}
        </EditableText>

        {data.items.map((it, i) => (
          <div key={i} style={{ marginBottom: 14 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
              <span style={{
                width: 22, height: 22, borderRadius: 6,
                background: T.primary, color: T.navy,
                display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 11, fontWeight: 700, fontFamily: T.fontMono,
              }}>0{i + 1}</span>
              <EditableText tag="span" onChange={v => {
                const items = [...data.items]; items[i] = { ...it, name: v };
                onSetData({ ...data, items });
              }} style={{ fontSize: 14, fontWeight: 700, color: T.navy }}>{it.name}</EditableText>
            </div>
            <EditableText tag="p" onChange={v => {
              const items = [...data.items]; items[i] = { ...it, desc: v };
              onSetData({ ...data, items });
            }} style={{ fontSize: 12.5, color: T.navyMid, lineHeight: 1.7, paddingLeft: 30 }}>{it.desc}</EditableText>
          </div>
        ))}

        <div style={{
          marginTop: 18, padding: '12px 14px', borderRadius: 10,
          background: T.peachTint, color: T.navy,
          fontSize: 13, fontWeight: 600, lineHeight: 1.6,
        }}>
          <EditableText tag="div" onChange={v => onSetData({ ...data, cta: v })}>
            {data.cta}
          </EditableText>
        </div>

        <div style={{ marginTop: 16, fontSize: 11.5, color: T.navyLight, fontFamily: T.fontMono }}>
          上海 · 8 张图 · 预估阅读 1 分钟
        </div>
      </div>
    </div>
  );
};

const SimplePhonePreview = ({ data, selectedAsset }) => {
  const previewAsset = selectedAsset || GENERATED_IMAGES[0];
  const coverPalette = previewAsset?.palette || GENERATION_COVER_OPTIONS[0].palette;
  return (
    <PhoneFrame>
      <div style={{
        height: '100%',
        background: '#fbfbfd',
        overflow: 'auto',
        color: T.navy,
      }}>
        <div style={{
          height: 34,
          padding: '0 18px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          fontSize: 11,
          fontWeight: 650,
          color: 'rgba(14,14,44,.76)',
          borderBottom: `1px solid ${T.hairlineSoft}`,
        }}>
          <span>预览</span>
          <span style={{ color: T.navyLight }}>低保真</span>
        </div>
        <div style={{ padding: 14 }}>
          <div style={{ aspectRatio: '3 / 4', borderRadius: 18, overflow: 'hidden', background: coverPalette[0], boxShadow: '0 10px 28px rgba(14,14,44,.10)' }}>
            <GenerationImageVisual item={previewAsset} />
          </div>
          <h2 style={{ margin: '14px 0 8px', fontSize: 17, lineHeight: 1.42, fontWeight: 680, color: T.navy }}>
            {generatedPostCopy.title}
          </h2>
          <p style={{ margin: 0, fontSize: 13.2, lineHeight: 1.75, color: T.navyMid }}>
            {generatedPostCopy.body[0]}
          </p>
          <div style={{ marginTop: 12, display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {generatedPostCopy.tags.slice(0, 4).map(tag => (
              <span key={tag} style={{
                height: 24,
                padding: '0 8px',
                borderRadius: 999,
                background: T.surface,
                color: T.navyMid,
                display: 'inline-flex',
                alignItems: 'center',
                fontSize: 10.5,
                fontWeight: 600,
              }}>{tag}</span>
            ))}
          </div>
          <div style={{ marginTop: 14, paddingTop: 12, borderTop: `1px solid ${T.hairlineSoft}`, color: T.navyLight, fontSize: 11.5 }}>
            手机端大致排布，仅用于确认封面、标题和正文顺序。
          </div>
        </div>
      </div>
    </PhoneFrame>
  );
};

const CanvasMiniButton = ({ icon, label, active, onClick, children }) => {
  const [hov, setHov] = React.useState(false);
  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      title={label}
      style={{
        position: 'relative',
        width: 42,
        height: 42,
        borderRadius: 14,
        border: active ? `1px solid rgba(75,77,237,.28)` : `1px solid ${T.hairlineSoft}`,
        background: active ? T.navy : (hov ? 'rgba(14,14,44,.06)' : 'rgba(255,255,255,.82)'),
        color: active ? T.white : T.navyMid,
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        cursor: 'pointer',
        boxShadow: active ? '0 10px 22px rgba(14,14,44,.14)' : '0 6px 16px rgba(14,14,44,.045)',
        transition: `background .2s ${T.ease}, color .2s ${T.ease}, transform .22s ${T.spring}`,
      }}
    >
      {children || <Icon name={icon} size={18} stroke={1.8} />}
      {hov && (
        <span style={{
          position: 'absolute',
          left: 52,
          top: '50%',
          transform: 'translateY(-50%)',
          height: 32,
          padding: '0 12px',
          borderRadius: 12,
          background: T.navy,
          color: T.white,
          display: 'inline-flex',
          alignItems: 'center',
          whiteSpace: 'nowrap',
          fontSize: 12.5,
          fontWeight: 650,
          boxShadow: '0 14px 30px rgba(14,14,44,.18)',
          zIndex: 8,
          pointerEvents: 'none',
        }}>{label}</span>
      )}
    </button>
  );
};

const ImageCanvasToolbar = ({ onDownload }) => {
  const tools = [
    { id: 'quick', label: '编辑图片', icon: 'settings', active: true },
    { id: 'text', label: '编辑封面文字', icon: 'edit' },
  ];
  return (
    <div style={{
      position: 'absolute',
      left: 18,
      right: 68,
      top: 16,
      zIndex: 30,
      display: 'flex',
      alignItems: 'center',
      gap: 6,
      padding: 6,
      borderRadius: 18,
      background: 'rgba(255,255,255,.90)',
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: '0 16px 36px rgba(14,14,44,.095), inset 0 1px 0 rgba(255,255,255,.86)',
      backdropFilter: 'blur(18px) saturate(1.18)',
      overflowX: 'auto',
    }}>
      {tools.map(tool => (
        <button key={tool.id} style={{
          height: 38,
          minWidth: tool.id === 'quick' ? 118 : 86,
          padding: '0 12px',
          borderRadius: 13,
          border: tool.active ? `1px solid rgba(14,14,44,.12)` : '1px solid transparent',
          background: tool.active ? 'rgba(14,14,44,.055)' : 'transparent',
          color: T.navy,
          cursor: 'pointer',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 8,
          fontSize: 13,
          fontWeight: 620,
          whiteSpace: 'nowrap',
        }}>
          <Icon name={tool.icon} size={16} stroke={1.75} />
          {tool.label}
          {tool.hint && <span style={{ color: T.navyLight, fontWeight: 500 }}>{tool.hint}</span>}
        </button>
      ))}
    </div>
  );
};

const ImageCanvasToolTip = ({ text, anchor }) => {
  if (!anchor) return null;
  return (
    <div style={{
      position: 'fixed',
      left: anchor.left + 52,
      top: anchor.top + 4,
      zIndex: 90,
      height: 28,
      padding: '0 10px',
      borderRadius: 10,
      background: 'rgba(14,14,44,.92)',
      color: T.white,
      display: 'inline-flex',
      alignItems: 'center',
      whiteSpace: 'nowrap',
      fontSize: 11.5,
      fontWeight: 620,
      boxShadow: '0 14px 28px rgba(14,14,44,.20)',
      pointerEvents: 'none',
    }}>
      {text}
    </div>
  );
};

const CanvasFloatingTextToolbar = ({ rect, onClose }) => {
  if (!rect) return null;
  return (
    <div style={{
      position: 'absolute',
      left: rect.left,
      top: rect.top,
      transform: 'translate(-50%, -118%)',
      zIndex: 35,
      display: 'flex',
      alignItems: 'center',
      gap: 4,
      padding: 4,
      borderRadius: 12,
      background: 'rgba(255,255,255,.96)',
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: '0 12px 28px rgba(14,14,44,.12)',
    }}>
      {['B', 'I', 'L', 'A'].map((item, index) => (
        <button key={item} style={{
          width: 26,
          height: 26,
          borderRadius: 8,
          border: 'none',
          background: index === 0 ? 'rgba(14,14,44,.06)' : 'transparent',
          color: T.navy,
          fontSize: 11.5,
          fontWeight: 700,
          cursor: 'pointer',
        }}>
          {item}
        </button>
      ))}
      <button onClick={onClose} style={{
        width: 26,
        height: 26,
        borderRadius: 8,
        border: 'none',
        background: 'transparent',
        color: T.navyLight,
        cursor: 'pointer',
      }}>
        <Icon name="close" size={11} />
      </button>
    </div>
  );
};

const ImageQuickMenu = ({ menu, onClose, onPick }) => {
  if (!menu) return null;
  const actions = [
    { id: 'upscale', label: '放大', icon: 'expand' },
    { id: 'remove-bg', label: '去背景', icon: 'user' },
    { id: 'erase', label: '橡皮工具', icon: 'minus' },
    { id: 'text', label: '编辑文字', icon: 'edit' },
    { id: 'download', label: '下载', icon: 'download' },
  ];
  return (
    <>
      <div onClick={onClose} style={{ position: 'fixed', inset: 0, zIndex: 70 }} />
      <div style={{
        position: 'fixed',
        left: menu.x,
        top: menu.y,
        width: 180,
        padding: 6,
        borderRadius: 14,
        background: 'rgba(255,255,255,.96)',
        border: `1px solid ${T.hairlineSoft}`,
        boxShadow: T.shadowLg,
        zIndex: 71,
        backdropFilter: 'blur(18px) saturate(1.16)',
      }}>
        {actions.map(action => (
          <button key={action.id} onClick={() => onPick(action)} style={{
            width: '100%',
            height: 38,
            border: 'none',
            borderRadius: 10,
            background: 'transparent',
            color: T.navy,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            padding: '0 10px',
            fontSize: 13,
            fontWeight: 600,
            textAlign: 'left',
          }}
            onMouseEnter={e => e.currentTarget.style.background = T.surface}
            onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
            <Icon name={action.icon} size={15} />
            {action.label}
          </button>
        ))}
      </div>
    </>
  );
};

const ImageInlineMenu = ({ menu, onClose, onPick }) => {
  if (!menu) return null;
  const actions = [
    { id: 'edit', label: '编辑图片', icon: 'edit' },
    { id: 'upscale', label: '放大', icon: 'expand' },
    { id: 'remove-bg', label: '去背景', icon: 'user' },
    { id: 'download', label: '下载', icon: 'download' },
  ];
  return (
    <>
      <div onClick={onClose} style={{ position: 'fixed', inset: 0, zIndex: 64 }} />
      <div style={{
        position: 'fixed',
        left: menu.x,
        top: menu.y,
        width: 168,
        padding: 6,
        borderRadius: 14,
        background: 'rgba(255,255,255,.96)',
        border: `1px solid ${T.hairlineSoft}`,
        boxShadow: T.shadowLg,
        zIndex: 65,
        backdropFilter: 'blur(18px) saturate(1.16)',
      }}>
        {actions.map(action => (
          <button key={action.id} onClick={() => onPick(action)} style={{
            width: '100%',
            height: 38,
            border: 'none',
            borderRadius: 10,
            background: 'transparent',
            color: T.navy,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 10,
            padding: '0 10px',
            fontSize: 13,
            fontWeight: 600,
          }}
            onMouseEnter={e => e.currentTarget.style.background = T.surface}
            onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
            <Icon name={action.icon} size={15} />
            {action.label}
          </button>
        ))}
      </div>
    </>
  );
};

const ImageCanvasEditor = ({ image, onAction, initialPrompt = '', onOpenInspiration }) => {
  const [activeTool, setActiveTool] = React.useState('upload');
  const [menu, setMenu] = React.useState(null);
  const [prompt, setPrompt] = React.useState(initialPrompt);
  const [notes, setNotes] = React.useState([]);
  const [pendingRefs, setPendingRefs] = React.useState([]);
  const [canvasMenu, setCanvasMenu] = React.useState(null);
  const [canvasText, setCanvasText] = React.useState({ open: false, value: '在此输入文本', x: 50, y: 52, selected: false });
  const [dragState, setDragState] = React.useState(null);
  const [toolTip, setToolTip] = React.useState(null);
  const filePickerRef = React.useRef(null);
  const chatFileRef = React.useRef(null);
  const selected = image || GENERATED_IMAGES[0];
  const palette = selected.palette || GENERATION_COVER_OPTIONS[0].palette;
  const paletteTools = [
    { id: 'upload', label: '本地上传', icon: 'upload' },
    { id: 'asset', label: '导入资产', icon: 'folder' },
    { id: 'board', label: '添加画板', icon: 'grid' },
    { id: 'text', label: '添加文本', icon: 'edit' },
  ];
  const submitPrompt = () => {
    const clean = prompt.trim();
    if (!clean) return;
    setNotes(v => [...v, { id: Date.now(), text: clean }]);
    setPrompt('');
  };
  React.useEffect(() => {
    if (!initialPrompt) return;
    setPrompt(initialPrompt);
  }, [initialPrompt]);
  React.useEffect(() => {
    if (!dragState) return undefined;
    const move = (event) => {
      setCanvasText(v => ({
        ...v,
        x: Math.max(8, Math.min(92, dragState.startX + ((event.clientX - dragState.pointerX) / Math.max(1, dragState.width)) * 100)),
        y: Math.max(10, Math.min(88, dragState.startY + ((event.clientY - dragState.pointerY) / Math.max(1, dragState.height)) * 100)),
      }));
    };
    const up = () => setDragState(null);
    window.addEventListener('mousemove', move);
    window.addEventListener('mouseup', up);
    return () => {
      window.removeEventListener('mousemove', move);
      window.removeEventListener('mouseup', up);
    };
  }, [dragState]);
  const pickAction = (action) => {
    setMenu(null);
    setNotes(v => [...v, { id: Date.now(), text: `已选择：${action.label}` }]);
    onAction && onAction(action);
  };
  const openToolMenu = (toolId, event) => {
    setActiveTool(toolId);
    const rect = event?.currentTarget?.getBoundingClientRect?.();
    if (toolId === 'upload') {
      filePickerRef.current?.click();
      return;
    }
    if (toolId === 'asset') {
      setCanvasMenu({ kind: 'asset', left: rect ? rect.right + 12 : 92, top: rect ? rect.top : 88 });
      return;
    }
    if (toolId === 'board') {
      setCanvasMenu({ kind: 'board', left: rect ? rect.right + 12 : 92, top: rect ? rect.top : 154 });
      return;
    }
    if (toolId === 'text') {
      setCanvasMenu(null);
      setCanvasText({ open: true, value: canvasText.value || '在此输入文本', x: canvasText.x || 50, y: canvasText.y || 52, selected: true });
      setNotes(v => [...v, { id: Date.now(), text: '已添加文本框' }]);
    }
  };
  return (
    <div style={{
      width: '100%',
      minHeight: '100%',
      display: 'flex',
      flexDirection: 'column',
      position: 'relative',
    }}>
      <div style={{
        flex: 1,
        minHeight: 0,
        padding: '72px 24px 104px',
        display: 'grid',
        gridTemplateColumns: '76px minmax(320px, 1fr)',
        gap: 20,
        alignItems: 'center',
      }}>
        <input
          ref={filePickerRef}
          type="file"
          accept="image/*"
          style={{ display: 'none' }}
          onChange={e => {
            const file = e.target.files?.[0];
            if (file) setNotes(v => [...v, { id: Date.now(), text: `已上传：${file.name}` }]);
            e.target.value = '';
          }}
        />
        <input
          ref={chatFileRef}
          type="file"
          accept="image/*"
          multiple
          style={{ display: 'none' }}
          onChange={e => {
            const files = Array.from(e.target.files || []).map(file => ({
              file,
              preview: file.type?.startsWith('image/') ? URL.createObjectURL(file) : null,
            }));
            if (files.length) {
              setPendingRefs(list => [...list, ...files]);
              setNotes(v => [...v, { id: Date.now(), text: `已添加 ${files.length} 张参考图` }]);
            }
            e.target.value = '';
          }}
        />
        <div style={{
          alignSelf: 'center',
          justifySelf: 'center',
          display: 'grid',
          gap: 9,
          padding: 7,
          borderRadius: 20,
          background: 'rgba(255,255,255,.90)',
          border: `1px solid ${T.hairlineSoft}`,
          boxShadow: '0 16px 36px rgba(14,14,44,.08)',
        }}>
          {paletteTools.map(tool => (
            <CanvasMiniButton
              key={tool.id}
              label={tool.label}
              icon={tool.icon}
              active={activeTool === tool.id}
              onClick={(event) => openToolMenu(tool.id, event)}
            >
              {tool.text ? <span style={{ fontSize: tool.text === 'T' ? 22 : 20, fontWeight: 650, lineHeight: 1 }}>{tool.text}</span> : null}
            </CanvasMiniButton>
          ))}
        </div>

        <div style={{
          height: 'min(68vh, 640px)',
          minHeight: 420,
          borderRadius: 0,
          background: 'transparent',
          border: 'none',
          boxShadow: 'none',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative',
          overflow: 'hidden',
        }}>
          <div style={{
            position: 'absolute',
            inset: 22,
            backgroundImage: `linear-gradient(${T.hairlineSoft} 1px, transparent 1px), linear-gradient(90deg, ${T.hairlineSoft} 1px, transparent 1px)`,
            backgroundSize: '34px 34px',
            opacity: activeTool === 'grid' ? 1 : .34,
            pointerEvents: 'none',
          }} />
          <button
            onContextMenu={(e) => {
              e.preventDefault();
              setMenu({ x: Math.min(e.clientX, window.innerWidth - 196), y: Math.min(e.clientY, window.innerHeight - 230) });
            }}
            onClick={() => setNotes(v => [...v, { id: Date.now(), text: `正在编辑：${selected.title}` }])}
            style={{
              width: 'min(380px, 62%)',
              maxHeight: '86%',
              aspectRatio: '3 / 4',
              borderRadius: 0,
              border: 'none',
              background: palette[0],
              overflow: 'hidden',
              position: 'relative',
              cursor: 'default',
              boxShadow: '0 26px 60px rgba(14,14,44,.16)',
              padding: 0,
            }}
          >
            <GenerationImageVisual item={selected} />
            <div style={{
              position: 'absolute',
              left: 20,
              right: 20,
              bottom: 22,
              color: T.white,
              textAlign: 'left',
              textShadow: '0 10px 28px rgba(14,14,44,.35)',
            }}>
              <div style={{ fontSize: 28, lineHeight: 1.1, fontWeight: 760, letterSpacing: 0 }}>{selected.title}</div>
              <div style={{
                marginTop: 8,
                display: 'inline-flex',
                height: 28,
                padding: '0 10px',
                borderRadius: 999,
                alignItems: 'center',
                background: 'rgba(255,255,255,.66)',
                color: T.navyMid,
                fontSize: 11.5,
                fontWeight: 650,
              }}>{selected.sub}</div>
            </div>
          </button>
          {canvasMenu?.kind === 'asset' && (
            <div style={{ position: 'fixed', left: canvasMenu.left, top: canvasMenu.top, width: 196, borderRadius: 16, background: 'rgba(255,255,255,.96)', border: `1px solid ${T.hairlineSoft}`, boxShadow: T.shadowLg, padding: 10, zIndex: 88 }}>
              <div style={{ display: 'grid', gap: 7 }}>
                <div style={{ color: T.navy, fontSize: 13.5, fontWeight: 700, padding: '2px 4px' }}>导入资产</div>
                <button style={{ height: 34, borderRadius: 11, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(250,252,254,.88)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 7, padding: '0 10px', color: T.navy, fontSize: 13 }}>
                  <Icon name="image" size={14} />
                  导入图片
                </button>
                <button style={{ height: 34, borderRadius: 11, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(250,252,254,.88)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 7, padding: '0 10px', color: T.navy, fontSize: 13 }}>
                  <Icon name="video" size={14} />
                  导入视频
                </button>
              </div>
            </div>
          )}
          {canvasMenu?.kind === 'board' && (
            <div style={{ position: 'fixed', left: canvasMenu.left, top: canvasMenu.top, width: 224, borderRadius: 16, background: 'rgba(255,255,255,.96)', border: `1px solid ${T.hairlineSoft}`, boxShadow: T.shadowLg, padding: 10, zIndex: 88 }}>
              <div style={{ display: 'grid', gap: 7 }}>
                <div style={{ color: T.navy, fontSize: 13.5, fontWeight: 700, padding: '2px 4px' }}>画板大小</div>
                {['16:9 1920 × 1080', '4:3 1536 × 1024', '1:1 1024 × 1024', '3:4 1024 × 1536', '9:16 1080 × 1920'].map(item => (
                  <button key={item} style={{ height: 32, borderRadius: 11, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(250,252,254,.88)', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 10px', color: T.navy, fontSize: 13 }}>
                    <span style={{ fontWeight: 650 }}>{item.split(' ')[0]}</span>
                    <span style={{ color: T.navyLight, fontSize: 11.5 }}>{item.split(' ').slice(1).join(' ')}</span>
                  </button>
                ))}
                <button style={{ height: 32, borderRadius: 11, border: 'none', background: 'transparent', color: T.navy, cursor: 'pointer', display: 'flex', alignItems: 'center', gap: 7, padding: '0 4px', fontSize: 13 }}>
                  <Icon name="plus" size={14} />
                  新增预设尺寸
                </button>
              </div>
            </div>
          )}
          {canvasText.open && (
            <>
              <CanvasFloatingTextToolbar
                rect={{ left: `${canvasText.x}%`, top: `${canvasText.y}%` }}
                onClose={() => setCanvasText(v => ({ ...v, selected: false }))}
              />
              <input
                autoFocus
                value={canvasText.value}
                onMouseDown={e => {
                  const bounds = e.currentTarget.parentElement?.getBoundingClientRect();
                  if (bounds) setDragState({ pointerX: e.clientX, pointerY: e.clientY, startX: canvasText.x, startY: canvasText.y, width: bounds.width, height: bounds.height });
                  setCanvasText(v => ({ ...v, selected: true }));
                }}
                onClick={() => setCanvasText(v => ({ ...v, selected: true }))}
                onChange={e => setCanvasText(v => ({ ...v, value: e.target.value }))}
                style={{
                  position: 'absolute',
                  left: `${canvasText.x}%`,
                  top: `${canvasText.y}%`,
                  transform: 'translate(-50%, -50%)',
                  width: 212,
                  border: `1.5px solid ${canvasText.selected ? 'rgba(75,77,237,.38)' : 'rgba(14,14,44,.12)'}`,
                  background: 'rgba(255,255,255,.86)',
                  color: T.navy,
                  fontSize: 15,
                  fontFamily: T.fontSans,
                  padding: '7px 9px',
                  outline: 'none',
                  cursor: dragState ? 'grabbing' : 'grab',
                  boxShadow: '0 10px 24px rgba(14,14,44,.09)',
                }}
              />
            </>
          )}
          <ImageQuickMenu menu={menu} onClose={() => setMenu(null)} onPick={pickAction} />
        </div>

      </div>
      <div style={{
        position: 'absolute',
        left: '50%',
        bottom: 18,
        transform: 'translateX(-50%)',
        width: 'min(720px, calc(100% - 56px))',
        borderRadius: 18,
        background: 'rgba(255,255,255,.92)',
        border: `1px solid ${T.hairlineSoft}`,
        boxShadow: '0 18px 42px rgba(14,14,44,.10), inset 0 1px 0 rgba(255,255,255,.86)',
        backdropFilter: 'blur(18px) saturate(1.16)',
        padding: '10px 10px 10px 14px',
        display: 'flex',
        alignItems: 'flex-end',
        gap: 10,
      }}>
        <button onClick={() => chatFileRef.current?.click()} style={{ ...iconBtnStyle(), flexShrink: 0 }}><Icon name="plus" size={14} /></button>
        <textarea
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              submitPrompt();
            }
          }}
          placeholder="描述你想怎么改这张图，比如：让标题更清楚，背景更干净…"
          rows={1}
          style={{
            flex: 1,
            minHeight: 28,
            maxHeight: 96,
            resize: 'none',
            border: 'none',
            outline: 'none',
            background: 'transparent',
            color: T.navy,
            fontFamily: T.fontSans,
            fontSize: 13.5,
            lineHeight: 1.6,
          }}
        />
        <button onClick={submitPrompt} disabled={!prompt.trim()} style={{
          width: 34,
          height: 34,
          borderRadius: '50%',
          border: 'none',
          background: prompt.trim() ? T.navy : T.surface,
          color: prompt.trim() ? T.white : T.navyLight,
          cursor: prompt.trim() ? 'pointer' : 'not-allowed',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexShrink: 0,
        }}>
          <Icon name="arrowUp" size={15} />
        </button>
      </div>
    </div>
  );
};

const Canvas = ({ open, expanded, setExpanded, onClose, onTransform, onPublish, mode, setMode, selectedAsset, selectedImage, width = 540, toolbarCollapsed, setToolbarCollapsed, imagePrompt = '', onOpenInspiration }) => {
  const [data, setData] = React.useState({
    title: '上海这 5 家饭店，第一次去照着点就很稳',
    tags: ['上海饭店推荐', '上海美食', '周末约饭'],
    hook: '第一次去别乱点，先看这份不踩雷菜单。',
    intro: '我把最近收藏率高的上海饭店内容拆了一遍，真正有用的不是氛围词，而是点什么、什么时候去、适合和谁去。',
    items: [
      { name: '先看招牌菜', desc: '每家只保留 2-3 个第一次去最稳的菜，不做大而全清单。' },
      { name: '写清适合谁', desc: '下班约饭、朋友局、情侣小聚分开讲，用户更容易判断。' },
      { name: '补一句避坑', desc: '排队时间、口味偏甜偏咸、人均价格都比空泛夸奖更有用。' },
      { name: '给到发布时间', desc: '饭点前后更适合推送，标题里保留地点和场景关键词。' },
    ],
    cta: '今天 18:40 发，饭点前适合推给正在找约饭地点的人。',
  });

  const [textMenu, setTextMenu] = React.useState(null);
  const handleTextAction = (act) => {
    setTextMenu(null);
    window.getSelection().removeAllRanges();
    // Hook into chat: dispatched action would land in chat as a follow-up
    if (window.__noriOnTextAction) window.__noriOnTextAction(act);
  };

  if (!open) return null;

  return (
    <aside style={{
      width: expanded ? '100%' : width,
      flexShrink: 0,
      height: '100%',
      background: 'linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)',
      borderLeft: `1px solid ${T.hairlineSoft}`,
      display: 'flex', flexDirection: 'column',
      animation: `slideInRight .46s ${T.spring}`,
      position: expanded ? 'absolute' : 'relative',
      right: 0, top: 0, zIndex: 20,
      boxShadow: expanded ? 'none' : '-18px 0 48px rgba(14,14,44,.055)',
    }}>
      {/* Preview area */}
      <div style={{
        flex: 1,
        overflow: mode === 'image' ? 'hidden' : 'auto',
        padding: mode === 'image' ? 0 : '84px 42px 34px',
        position: 'relative',
        background: mode === 'image'
          ? 'linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)'
          : mode === 'preview'
          ? '#f6f7f8'
          : 'linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)',
      }}>
        <div style={{
          maxWidth: mode === 'image' ? 'none' : mode === 'preview' ? 560 : 860,
          margin: '0 auto',
          minHeight: '100%',
          display: 'flex',
          alignItems: mode === 'preview' ? 'center' : mode === 'image' ? 'stretch' : 'flex-start',
          justifyContent: 'center',
        }}>
          {mode === 'image' ? (
            <ImageCanvasEditor image={selectedImage} initialPrompt={imagePrompt} onOpenInspiration={onOpenInspiration} onAction={() => {}} />
          ) : mode === 'preview' ? (
            <SimplePhonePreview data={data} selectedAsset={selectedAsset} />
          ) : (
            <CanvasDocumentEditor data={data} onSetData={setData} />
          )}
        </div>
        {mode !== 'image' && <TextSelectionMenu pos={textMenu} onAction={handleTextAction} onClose={() => setTextMenu(null)} />}
      </div>

      {/* Floating right toolbar */}
      {mode !== 'image' && (
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            left: 18,
            top: 18,
            zIndex: 44,
            width: 38,
            height: 38,
            borderRadius: 14,
            border: `1px solid ${T.hairlineSoft}`,
            background: 'rgba(255,255,255,.90)',
            color: T.navy,
            cursor: 'pointer',
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 12px 28px rgba(14,14,44,.08)',
          }}
        >
          <Icon name="chevronLeft" size={15} />
        </button>
      )}
      {mode === 'image' && (
        <button onClick={onClose} style={{
          position: 'absolute',
          left: 18,
          top: 18,
          zIndex: 44,
          width: 78,
          height: 40,
          borderRadius: 14,
          border: `1px solid ${T.hairlineSoft}`,
          background: 'rgba(255,255,255,.90)',
          color: T.navy,
          cursor: 'pointer',
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 7,
          fontSize: 13,
          fontWeight: 680,
          boxShadow: '0 12px 28px rgba(14,14,44,.08)',
        }}>
          <Icon name="arrowLeft" size={15} />
          退出
        </button>
      )}
    </aside>
  );
};

window.Canvas = Canvas;
window.PostPreview = PostPreview;
/* ─── Generation Page: orchestrates 4 chat steps + Canvas ─── */

const StepperRail = ({ stage }) => {
  const steps = [
    { id: 1, label: '选题' },
    { id: 2, label: '封面' },
    { id: 3, label: '出图' },
    { id: 4, label: '文案' },
    { id: 5, label: '输出' },
  ];
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 6,
      padding: '8px 14px', borderRadius: 99,
      background: 'rgba(255,255,255,.78)', border: `1px solid ${T.hairlineSoft}`,
      boxShadow: '0 8px 20px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)',
      backdropFilter: 'blur(16px) saturate(1.18)',
    }}>
      {steps.map((s, i) => {
        const done = stage > s.id;
        const active = stage === s.id;
        return (
          <React.Fragment key={s.id}>
            <div style={{
              display: 'inline-flex', alignItems: 'center', gap: 6,
              opacity: stage >= s.id ? 1 : 0.45,
            }}>
              <span style={{
                width: 18, height: 18, borderRadius: '50%',
                background: done ? T.success : (active ? T.navy : T.surface),
                color: done ? T.white : (active ? T.primary : T.navyLight),
                display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
                fontSize: 10, fontWeight: 700, fontFamily: T.fontMono,
              }}>{done ? '✓' : s.id}</span>
              <span style={{ fontSize: 12, fontWeight: active ? 700 : 500, color: active ? T.navy : T.navyMid }}>{s.label}</span>
            </div>
            {i < steps.length - 1 && <span style={{ width: 14, height: 1, background: T.hairline }} />}
          </React.Fragment>
        );
      })}
    </div>
  );
};

const ComposerAttachmentPreview = ({ files = [], onRemove }) => {
  if (!files.length) return null;
  return (
    <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 10 }}>
      {files.map((file, index) => {
        const isImage = file.type?.startsWith('image/');
        return (
          <div key={`${file.name}-${index}`} style={{
            width: isImage ? 58 : 132,
            height: 58,
            borderRadius: 14,
            border: `1px solid ${T.hairlineSoft}`,
            background: isImage ? T.surface : 'rgba(250,252,254,.86)',
            overflow: 'hidden',
            position: 'relative',
            boxShadow: '0 8px 18px rgba(14,14,44,.045)',
            }}>
            {isImage ? (
              <img src={file.preview || file.url} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} />
            ) : (
              <div style={{ height: '100%', display: 'grid', gridTemplateColumns: '34px minmax(0, 1fr)', gap: 7, alignItems: 'center', padding: 9 }}>
                <span style={{ width: 32, height: 32, borderRadius: 11, background: T.irisTint, color: T.iris, display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Icon name={file.type?.startsWith('video/') ? 'video' : 'document'} size={15} />
                </span>
                <span style={{ minWidth: 0, color: T.navyMid, fontSize: 11.5, lineHeight: 1.35, fontWeight: 650, overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }}>
                  {file.name}
                </span>
              </div>
            )}
            <button onClick={() => onRemove?.(index)} style={{
              position: 'absolute',
              right: -5,
              top: -5,
              width: 21,
              height: 21,
              borderRadius: '50%',
              border: `1px solid ${T.hairlineSoft}`,
              background: 'rgba(255,255,255,.92)',
              color: T.navyMid,
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 6px 14px rgba(14,14,44,.10)',
            }}>
              <Icon name="close" size={9} />
            </button>
          </div>
        );
      })}
    </div>
  );
};

const ChatComposer = ({ onSend, placeholder = '继续追问 Nori，或描述你的想法…', initialValue = '', autoFocusKey, onAttach, canSendExtra = false, attachmentCount = 0, attachmentFiles = [], onRemoveAttachment }) => {
  const [text, setText] = React.useState(initialValue);
  const [focused, setFocused] = React.useState(false);
  const inputRef = React.useRef(null);
  const canSend = Boolean(text.trim()) || canSendExtra;
  React.useEffect(() => {
    if (!initialValue) return;
    setText(initialValue);
    window.setTimeout(() => inputRef.current?.focus(), 80);
  }, [initialValue, autoFocusKey]);
  return (
    <div style={{
      background: 'rgba(255,255,255,.86)', borderRadius: 18,
      border: `1px solid ${focused ? 'rgba(75,77,237,.20)' : T.hairlineSoft}`,
      boxShadow: focused ? `0 0 0 5px rgba(75,77,237,.07), ${T.shadowMd}` : '0 8px 20px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.82)',
      padding: '16px 17px 12px',
      transition: `border .28s ${T.ease}, box-shadow .36s ${T.spring}`,
      backdropFilter: 'blur(22px) saturate(1.18)',
    }}>
      <ComposerAttachmentPreview files={attachmentFiles} onRemove={onRemoveAttachment} />
      <textarea
        ref={inputRef}
        value={text} onChange={e => setText(e.target.value)}
        onFocus={() => setFocused(true)} onBlur={() => setFocused(false)}
        onKeyDown={e => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (canSend) { onSend(text.trim()); setText(''); }
          }
        }}
        placeholder={placeholder}
        rows={1}
        style={{
          width: '100%', border: 'none', outline: 'none',
          resize: 'none', background: 'transparent',
          fontSize: 14, lineHeight: 1.55, color: T.navy,
          fontFamily: T.fontSans, minHeight: 46, maxHeight: 148,
        }}
      />
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 4 }}>
        <div style={{ display: 'flex', gap: 4 }}>
          <ToolPill icon="paperclip" label="附件" onClick={onAttach} />
          {attachmentCount > 0 && (
            <span style={{
              height: 32,
              padding: '0 10px',
              borderRadius: 999,
              background: 'rgba(224,250,244,.88)',
              border: '1px solid rgba(49,208,170,.16)',
              color: T.success,
              display: 'inline-flex',
              alignItems: 'center',
              fontSize: 12,
              fontWeight: 700,
            }}>{attachmentCount} 个文件</span>
          )}
        </div>
        <button
          onClick={() => { if (canSend) { onSend(text.trim()); setText(''); } }}
          disabled={!canSend}
          style={{
            width: 32, height: 32, borderRadius: '50%',
            border: 'none', cursor: canSend ? 'pointer' : 'not-allowed',
            background: canSend ? T.navy : T.surface,
            color: canSend ? T.white : T.navyLight,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            transition: `transform .24s ${T.spring}, background .22s ${T.ease}, color .22s ${T.ease}`,
          }}>
          <Icon name="arrowUp" size={15} stroke={2} />
        </button>
      </div>
    </div>
  );
};

/* Transform menu — appears when transform clicked */
const TransformMenu = ({ open, onClose, onPick, anchorRect }) => {
  if (!open || !anchorRect) return null;
  const opts = [
    { id: 'gzh',   label: '公众号长文',   sub: '深度长文 · 1500–3000 字', icon: 'document', tint: '#fff8e0', accent: '#c89b00' },
    { id: 'dy',    label: '抖音短视频',   sub: '60s 口播脚本 + 分镜', icon: 'video', tint: '#e8e8fd', accent: T.iris },
    { id: 'wxsph', label: '微信视频号',   sub: '90s 横屏 · 适合科普', icon: 'play', tint: '#e0faf4', accent: T.success },
    { id: 'bili',  label: 'B 站视频',    sub: '5 分钟以上 · 长内容', icon: 'bilibili', tint: '#ffe5ec', accent: '#ff4488' },
  ];
  const menuWidth = 320;
  const menuHeight = 286;
  const viewportWidth = typeof window !== 'undefined' ? window.innerWidth : 1440;
  const viewportHeight = typeof window !== 'undefined' ? window.innerHeight : 900;
  const left = Math.max(16, Math.min(anchorRect.right + 12, viewportWidth - menuWidth - 16));
  const top = Math.max(16, Math.min(anchorRect.top - 28, viewportHeight - menuHeight - 16));
  return (
    <>
      <div onClick={onClose} style={{ position: 'fixed', inset: 0, zIndex: 100 }} />
      <div style={{
        position: 'fixed', top, left,
        background: T.white, borderRadius: 14,
        boxShadow: T.shadowXl, border: `1px solid ${T.hairline}`,
        padding: 8, width: 320, zIndex: 101,
        animation: 'fadeIn .18s ease',
      }}>
        <div style={{ padding: '6px 10px 8px', fontSize: 11, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: T.navyLight }}>
          转化为
        </div>
        {opts.map(o => (
          <button key={o.id} onClick={() => onPick(o)} style={{
            width: '100%', display: 'flex', alignItems: 'center', gap: 12,
            padding: '10px 10px', borderRadius: 8,
            background: 'transparent', border: 'none', cursor: 'pointer',
            textAlign: 'left',
          }}
            onMouseEnter={e => e.currentTarget.style.background = T.surface}
            onMouseLeave={e => e.currentTarget.style.background = 'transparent'}>
            <div style={{
              width: 32, height: 32, borderRadius: 8,
              background: o.tint, color: o.accent,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <Icon name={o.icon} size={16} />
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: T.navy }}>{o.label}</div>
              <div style={{ fontSize: 11, color: T.navyLight }}>{o.sub}</div>
            </div>
            <Icon name="chevronRight" size={12} color={T.navyLight} />
          </button>
        ))}
      </div>
    </>
  );
};

/* Publish flow messages — after step 4 */
const PublishLinkAccount = ({ onLinked }) => {
  const [linking, setLinking] = React.useState(false);
  const [linked, setLinked] = React.useState(false);
  const trigger = () => {
    setLinking(true);
    setTimeout(() => { setLinking(false); setLinked(true); setTimeout(() => onLinked(), 800); }, 1600);
  };
  return (
    <NoriSays>
      {!linked ? (
        <>
          <p style={{ marginBottom: 12 }}>发布前需要先链接你的小红书账号。<span style={{ color: T.navyLight, fontSize: 12.5 }}>(只有第一次需要，之后会自动链接)</span></p>
          <div style={{
            background: T.white, border: `1px solid ${T.hairline}`,
            borderRadius: 12, padding: '14px 16px',
            display: 'flex', alignItems: 'center', gap: 12,
          }}>
            <div style={{
              width: 36, height: 36, borderRadius: 10,
              background: '#ffe5ec', color: '#ff4488',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontWeight: 800, fontSize: 16,
            }}>红</div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: T.navy }}>小红书</div>
              <div style={{ fontSize: 11.5, color: T.navyLight }}>{linking ? '正在跳转授权…' : '未链接'}</div>
            </div>
            <button onClick={trigger} disabled={linking} style={{
              height: 34, padding: '0 14px', borderRadius: 8,
              border: 'none', cursor: linking ? 'wait' : 'pointer',
              background: T.navy, color: T.primary,
              fontSize: 12.5, fontWeight: 600,
              display: 'inline-flex', alignItems: 'center', gap: 6,
            }}>
              {linking ? <><span style={{ width: 12, height: 12, border: `2px solid ${T.primary}`, borderTopColor: 'transparent', borderRadius: '50%', animation: 'spin .9s linear infinite', display: 'inline-block' }} /> 授权中</> : <><Icon name="link" size={12} /> 链接账号</>}
            </button>
          </div>
        </>
      ) : (
        <div style={{
          background: T.white, border: `1px solid ${T.hairline}`,
          borderRadius: 12, padding: '14px 16px',
          display: 'flex', alignItems: 'center', gap: 12,
          animation: 'fadeIn .3s',
        }}>
          <div style={{
            width: 36, height: 36, borderRadius: 10,
            background: T.successTint, color: T.success,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}>
            <Icon name="check" size={18} stroke={2.4} />
          </div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: T.navy }}>已链接 · 小红书 @luna_writes</div>
            <div style={{ fontSize: 11.5, color: T.navyLight }}>下次可以直接发布</div>
          </div>
        </div>
      )}
    </NoriSays>
  );
};

const PublishDraftSaved = () => (
  <NoriSays>
    <div style={{
      background: `linear-gradient(135deg, ${T.primaryTint}, ${T.peachTint})`,
      border: `1px solid ${T.hairline}`,
      borderRadius: 14, padding: '16px 18px',
      display: 'flex', alignItems: 'center', gap: 14,
    }}>
      <div style={{
        width: 40, height: 40, borderRadius: 12,
        background: T.primary, color: T.navy,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        <Icon name="check" size={20} stroke={2.6} />
      </div>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 14, fontWeight: 700, color: T.navy }}>已存入你的草稿箱</div>
        <div style={{ fontSize: 11.5, color: T.navyMid, marginTop: 2 }}>小红书 App · 草稿箱 · 1 篇待审</div>
      </div>
      <button style={{
        height: 36, padding: '0 14px', borderRadius: 10,
        background: T.navy, color: T.white,
        border: 'none', cursor: 'pointer',
        fontSize: 12.5, fontWeight: 600,
        display: 'inline-flex', alignItems: 'center', gap: 6,
      }}>
        去确认 <Icon name="arrowRight" size={12} />
      </button>
    </div>
  </NoriSays>
);

/* Transform launched — new round of chat */
const TransformLaunched = ({ target }) => (
  <NoriSays>
    <p>
      好，开始把当前内容转化为 <b>{target.label}</b>。
      <span style={{ color: T.navyLight, fontSize: 12.5 }}> ({target.sub})</span>
    </p>
    <div style={{
      marginTop: 10, padding: '10px 14px', borderRadius: 10,
      background: T.surface, color: T.navyMid,
      fontSize: 12.5, display: 'flex', alignItems: 'center', gap: 8,
    }}>
      <span style={{
        width: 14, height: 14, borderRadius: '50%',
        border: `2px solid ${T.iris}`, borderTopColor: 'transparent',
        animation: 'spin 1s linear infinite',
      }} />
      正在重组结构与节奏 · 适配 {target.label} 平台特性…
    </div>
  </NoriSays>
);

const GENERATION_TOPIC_OPTIONS = [
  {
    id: 'shanghai-first-list',
    title: '上海饭店第一次去怎么点',
    desc: '适合做成高收藏图文，直接解决「点什么不踩雷」的问题。',
    score: '收藏潜力 94',
  },
  {
    id: 'city-dinner-map',
    title: '上海下班后小馆地图',
    desc: '更有城市生活感，适合做系列化饭店推荐。',
    score: '涨粉潜力 88',
  },
  {
    id: 'budget-date',
    title: '人均 80 的约饭不踩雷',
    desc: '价格锚点清楚，容易吸引情侣、朋友局和周末聚餐人群。',
    score: '传播潜力 84',
  },
];

const GENERATION_COVER_OPTIONS = [
  { id: 'cover-a', label: 'A', title: '招牌菜近景', palette: ['#F7F9FC', '#D6FF00', '#4B4DED', '#31D0AA', '#0e0e2c'], note: '适合收藏型内容', image: 'https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=900&q=82' },
  { id: 'cover-b', label: 'B', title: '店内烟火气', palette: ['#F3DBDA', '#FAFCFE', '#8C8CA1', '#31D0AA', '#0e0e2c'], note: '更像真实探店', image: 'https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=900&q=82' },
  { id: 'cover-c', label: 'C', title: '城市饭点感', palette: ['#0e0e2c', '#D6FF00', '#EFEFFD', '#F3DBDA', '#ffffff'], note: '点击率优先', image: 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=900&q=82' },
];

const GENERATED_IMAGES = [
  { id: 'img-1', title: '封面', sub: '上海饭店推荐', palette: ['#F7F9FC', '#D6FF00', '#4B4DED', '#31D0AA', '#0e0e2c'], image: 'https://images.unsplash.com/photo-1559339352-11d035aa65de?auto=format&fit=crop&w=900&q=82' },
  { id: 'img-2', title: '第 2 图', sub: '适合谁去', palette: ['#EFEFFD', '#ffffff', '#4B4DED', '#D6FF00', '#0e0e2c'], image: 'https://images.unsplash.com/photo-1528605248644-14dd04022da1?auto=format&fit=crop&w=900&q=82' },
  { id: 'img-3', title: '第 3 图', sub: '必点菜单', palette: ['#E0FAF4', '#ffffff', '#31D0AA', '#4B4DED', '#0e0e2c'], image: 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=900&q=82' },
  { id: 'img-4', title: '第 4 图', sub: '避坑提醒', palette: ['#FDF5F5', '#F3DBDA', '#8C8CA1', '#D6FF00', '#0e0e2c'], image: 'https://images.unsplash.com/photo-1551218808-94e220e084d2?auto=format&fit=crop&w=900&q=82' },
  { id: 'img-5', title: '第 5 图', sub: '路线与时间', palette: ['#FAFCFE', '#ECF1F4', '#0e0e2c', '#D6FF00', '#31D0AA'], image: 'https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?auto=format&fit=crop&w=900&q=82' },
];

const generatedPostCopy = {
  title: '上海这 5 家饭店，第一次去照着点就很稳',
  body: [
    '我把最近收藏率高的上海饭店内容拆了一遍，发现大家最想要的不是氛围词，而是：第一次去到底点什么、什么时候去、适合和谁去。',
    '这版适合下班约饭、周末朋友局和来上海短暂停留的人。每家都用「招牌菜 + 适合场景 + 避坑提醒」来写，读完可以直接收藏。',
    '先看菜品稳定度，再看排队成本，最后看拍照氛围。别只为了网红感去，真正值得推荐的是吃完还愿意二刷。',
  ],
  tags: ['#上海饭店推荐', '#上海美食', '#周末约饭', '#小红书探店', '#不踩雷菜单'],
  publishTime: '今天 18:40',
};

const GenerationImageVisual = ({ item, overlay = true }) => {
  const palette = item?.palette || GENERATION_COVER_OPTIONS[0].palette;
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative', background: palette[0], overflow: 'hidden' }}>
      {item?.image ? (
        <img src={item.image} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block', filter: 'saturate(.94) contrast(.98)' }} />
      ) : (
        <FlowerVisual palette={palette} />
      )}
      {overlay && (
        <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(14,14,44,0) 42%, rgba(14,14,44,.34) 100%)' }} />
      )}
    </div>
  );
};

const TopicChoiceStep = ({ selected, onSelect, onAiDecide }) => (
  <AgentCardShell
    label="Agent 选题方向"
    icon="target"
    title="我先给你 3 个选题方向，选一个继续；也可以让我直接决定。"
    action={<button onClick={onAiDecide} style={{ ...pillButtonStyle(false), height: 38, borderRadius: 13, fontSize: 13 }}><Icon name="sparkles" size={14} />AI 帮我决定</button>}
  >
    <div style={{ display: 'grid', gap: 10 }}>
      {GENERATION_TOPIC_OPTIONS.map(option => {
        const active = selected?.id === option.id;
        return (
          <button
            key={option.id}
            onClick={() => onSelect(option)}
            style={{
              width: '100%',
              border: `1px solid ${active ? 'rgba(75,77,237,.24)' : T.hairlineSoft}`,
              background: active ? 'rgba(239,239,253,.72)' : 'rgba(255,255,255,.82)',
              borderRadius: 16,
              padding: 15,
              cursor: 'pointer',
              textAlign: 'left',
              boxShadow: active ? '0 12px 26px rgba(75,77,237,.08)' : '0 8px 20px rgba(14,14,44,.04)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'flex-start' }}>
              <div style={{ minWidth: 0 }}>
                <div style={{ color: T.navy, fontSize: 15, fontWeight: 700, lineHeight: 1.4 }}>{option.title}</div>
                <div style={{ marginTop: 6, color: T.navyMid, fontSize: 12.8, lineHeight: 1.62 }}>{option.desc}</div>
              </div>
              <span style={{ flexShrink: 0, height: 26, padding: '0 9px', borderRadius: 999, background: active ? T.white : 'rgba(250,252,254,.88)', color: active ? T.iris : T.navyLight, fontSize: 11.5, fontWeight: 650, display: 'inline-flex', alignItems: 'center' }}>{option.score}</span>
            </div>
          </button>
        );
      })}
    </div>
  </AgentCardShell>
);

const CoverThumb = ({ cover, active, onClick, onEdit }) => (
  <button
    onClick={() => {
      onClick?.();
      onEdit?.();
    }}
    style={{
      border: `1px solid ${active ? 'rgba(75,77,237,.34)' : T.hairlineSoft}`,
      background: active ? 'rgba(239,239,253,.68)' : 'rgba(255,255,255,.82)',
      borderRadius: 16,
      padding: 10,
      cursor: 'pointer',
      textAlign: 'left',
      boxShadow: active ? '0 12px 26px rgba(75,77,237,.09)' : '0 8px 20px rgba(14,14,44,.04)',
    }}
  >
    <div style={{ aspectRatio: '3 / 4', borderRadius: 0, overflow: 'hidden', background: cover.palette[0], position: 'relative', marginBottom: 10 }}>
      <GenerationImageVisual item={cover} />
      <div style={{ position: 'absolute', left: 12, right: 12, bottom: 12 }}>
        <div style={{ fontSize: 20, lineHeight: 1.1, fontWeight: 780, color: T.white, textShadow: '0 8px 24px rgba(14,14,44,.34)' }}>上海饭店推荐</div>
        <div style={{ marginTop: 6, height: 24, padding: '0 8px', borderRadius: 999, background: 'rgba(255,255,255,.78)', color: T.navyMid, display: 'inline-flex', alignItems: 'center', fontSize: 10.5, fontWeight: 650 }}>{cover.label}</div>
      </div>
    </div>
    <div style={{ color: T.navy, fontSize: 13.2, fontWeight: 700 }}>{cover.title}</div>
    <div style={{ marginTop: 4, color: T.navyLight, fontSize: 11.8 }}>{cover.note}</div>
  </button>
);

const CoverChoiceStep = ({ selected, onSelect, onContinue, onRegenerate, onEditCover }) => (
  <NoriSays>
    <p style={{ marginBottom: 14 }}>先出封面。我给你 3 个方向，选定封面后再继续生成剩下的图。</p>
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: 10 }}>
      {GENERATION_COVER_OPTIONS.map(cover => (
        <CoverThumb key={cover.id} cover={cover} active={selected?.id === cover.id} onClick={() => onSelect(cover)} onEdit={() => onEditCover?.(cover)} />
      ))}
    </div>
    {selected && (
      <div style={{ marginTop: 12, display: 'flex', justifyContent: 'flex-end', gap: 8, flexWrap: 'wrap' }}>
        <button onClick={onRegenerate} style={{ ...pillButtonStyle(false), height: 38, borderRadius: 13, fontSize: 13 }}>
          <Icon name="refresh" size={14} />
          重新生成
        </button>
        <button onClick={onContinue} style={{ ...pillButtonStyle(true), height: 38, borderRadius: 13, fontSize: 13 }}>
          用这个封面继续
          <Icon name="arrowRight" size={14} />
        </button>
      </div>
    )}
  </NoriSays>
);

const ImageGenerationStep = ({ done, onEditImage }) => {
  const [menu, setMenu] = React.useState(null);
  const pick = (action) => {
    const image = menu?.image || GENERATED_IMAGES[0];
    setMenu(null);
    onEditImage(image);
  };
  return (
    <NoriSays>
      <p style={{ marginBottom: 14 }}>{done ? '图片、正文、标签和发布时间都放在一起了。点击图片可以进入图片编辑。' : '封面定了，现在开始生成剩下的图。'}</p>
      {!done ? (
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: T.navyMid, fontSize: 13 }}>
          <span style={{ width: 14, height: 14, borderRadius: '50%', border: `2px solid ${T.iris}`, borderTopColor: 'transparent', animation: 'spin .9s linear infinite' }} />
          正在生成内页图、正文、标签和推荐发布时间
        </div>
      ) : (
        <div style={{ display: 'grid', gap: 16 }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, minmax(0, 1fr))', gap: 12 }}>
            {GENERATED_IMAGES.map((img, index) => (
              <button
                key={img.id}
                onClick={() => onEditImage(img)}
                onContextMenu={(e) => {
                  e.preventDefault();
                  setMenu({ image: img, x: Math.min(e.clientX, window.innerWidth - 184), y: Math.min(e.clientY, window.innerHeight - 198) });
                }}
                style={{
                  minWidth: 0,
                  cursor: 'pointer',
                  textAlign: 'left',
                  border: 'none',
                  background: 'transparent',
                  padding: 0,
                  boxShadow: 'none',
                }}
              >
                <div style={{ aspectRatio: '3 / 4', borderRadius: 0, overflow: 'hidden', background: img.palette[0], position: 'relative', boxShadow: '0 10px 24px rgba(14,14,44,.055)' }}>
                  <GenerationImageVisual item={img} />
                  <span style={{
                    position: 'absolute',
                    left: 8,
                    top: 8,
                    width: 24,
                    height: 24,
                    borderRadius: 9,
                    background: 'rgba(255,255,255,.74)',
                    color: T.navyMid,
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    boxShadow: '0 6px 14px rgba(14,14,44,.08)',
                    fontSize: 10.5,
                    fontWeight: 760,
                  }}>{index + 1}</span>
                </div>
                <div style={{ marginTop: 7, color: T.navy, fontSize: 11.8, fontWeight: 700 }}>{img.title}</div>
                <div style={{ marginTop: 2, color: T.navyLight, fontSize: 10.5, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{img.sub}</div>
              </button>
            ))}
            <ImageInlineMenu menu={menu} onClose={() => setMenu(null)} onPick={pick} />
          </div>
        </div>
      )}
    </NoriSays>
  );
};

const CopyGenerationStep = () => (
  <NoriSays>
    <div style={{ display: 'grid', gap: 10 }}>
      <p style={{ margin: 0 }}>图出来后，我再补正文、标签和推荐发布时间。</p>
      <div style={{ color: T.navy, fontSize: 16.5, fontWeight: 730, lineHeight: 1.48 }}>{generatedPostCopy.title}</div>
      <div style={{ display: 'grid', gap: 8 }}>
        {generatedPostCopy.body.map((line, index) => (
          <p key={index} style={{ margin: 0, color: T.navyMid, fontSize: 13.4, lineHeight: 1.78 }}>{line}</p>
        ))}
      </div>
      <div style={{ display: 'flex', gap: 7, flexWrap: 'wrap', marginTop: 2 }}>
        {generatedPostCopy.tags.map(tag => (
          <span key={tag} style={{ height: 28, padding: '0 10px', borderRadius: 999, background: 'rgba(255,255,255,.72)', border: `1px solid ${T.hairlineSoft}`, color: T.navyMid, display: 'inline-flex', alignItems: 'center', fontSize: 12, fontWeight: 620 }}>{tag}</span>
        ))}
      </div>
      <div style={{ color: T.success, fontSize: 13.2, fontWeight: 680 }}>
        推荐发布时间：{generatedPostCopy.publishTime}
      </div>
    </div>
  </NoriSays>
);

const GenerationStatusFlow = ({ title, subtitle, steps, conclusion, onComplete, defaultOpen = false, plain = false }) => {
  const [phase, setPhase] = React.useState(0);
  const [open, setOpen] = React.useState(defaultOpen);
  const onCompleteRef = React.useRef(onComplete);
  onCompleteRef.current = onComplete;
  React.useEffect(() => {
    const timers = steps.map((_, index) => window.setTimeout(() => setPhase(index + 1), 520 + index * 520));
    const doneTimer = window.setTimeout(() => onCompleteRef.current?.(), 760 + steps.length * 520);
    return () => {
      timers.forEach(window.clearTimeout);
      window.clearTimeout(doneTimer);
    };
  }, []);
  const complete = phase >= steps.length;
  return (
    <AgentParseFlow
      messages={[subtitle, '解析中', conclusion]}
      conclusion={conclusion}
      steps={steps}
      initialOpen={defaultOpen}
      active
      showThinking={false}
      style={{ gap: 10 }}
    />
  );
};

const IntentClarificationStep = ({ onConfirm, onSkip }) => {
  const [form, setForm] = React.useState({
    location: '',
    price: '人均 80-120',
    platform: '小红书',
  });
  const Field = ({ label, hint, children }) => (
    <label style={{ display: 'grid', gap: 7 }}>
      <span style={{ display: 'flex', justifyContent: 'space-between', gap: 10, alignItems: 'baseline' }}>
        <span style={{ color: T.navy, fontSize: 13.2, fontWeight: 700 }}>{label}</span>
        <span style={{ color: T.navyLight, fontSize: 11.5 }}>{hint}</span>
      </span>
      {children}
    </label>
  );
  const inputStyle = {
    width: '100%',
    height: 38,
    borderRadius: 13,
    border: `1px solid ${T.hairlineSoft}`,
    background: 'rgba(250,252,254,.82)',
    outline: 'none',
    padding: '0 11px',
    color: T.navy,
    fontSize: 13,
    fontFamily: T.fontSans,
  };
  return (
    <AgentCardShell
      label="Agent 意图澄清"
      icon="chat"
      title="我只补问缺失的信息"
      action={(
        <>
          <button onClick={onSkip} style={{ ...pillButtonStyle(false), height: 36, borderRadius: 12, fontSize: 12.5 }}>跳过，先生成</button>
          <button onClick={() => onConfirm(form)} style={{ ...pillButtonStyle(true), height: 36, borderRadius: 12, fontSize: 12.5 }}>确认继续<Icon name="arrowRight" size={13} /></button>
        </>
      )}
    >
      <p style={{ margin: '0 0 12px', color: T.navyMid, fontSize: 13.1, lineHeight: 1.66 }}>已知道你要做上海饭店推荐，所以这里只展示缺失项。</p>
      <div style={{ display: 'grid', gap: 13 }}>
        <Field label="店铺具体位置" hint="缺失项">
          <input value={form.location} onChange={e => setForm(v => ({ ...v, location: e.target.value }))} placeholder="例如：静安寺 / 武康路 / 人民广场附近" style={inputStyle} />
        </Field>
        <Field label="预算与场景" hint="可调整">
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 7 }}>
            {['人均 80-120', '朋友聚餐', '约会晚餐', '下班快吃'].map(option => (
              <button key={option} onClick={() => setForm(v => ({ ...v, price: option }))} style={{ ...pillButtonStyle(form.price === option), height: 32, borderRadius: 999, fontSize: 12, padding: '0 11px', fontWeight: 650 }}>
                {option}
              </button>
            ))}
          </div>
        </Field>
        <Field label="首发平台" hint="已推断，可改">
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 7 }}>
            {['小红书', '抖音', '公众号', '视频号'].map(option => (
              <button key={option} onClick={() => setForm(v => ({ ...v, platform: option }))} style={{ ...pillButtonStyle(form.platform === option), height: 32, borderRadius: 999, fontSize: 12, padding: '0 11px', fontWeight: 650 }}>
                {option}
              </button>
            ))}
          </div>
        </Field>
      </div>
    </AgentCardShell>
  );
};

const GenerationResearchStep = ({ onOpenDocument, onContinue }) => {
  const sources = [
    { title: '小红书上海饭店收藏型标题趋势', url: 'https://www.xiaohongshu.com', meta: '收藏向 · 标题公式' },
    { title: '大众点评静安 / 黄浦热门餐厅评价摘要', url: 'https://www.dianping.com', meta: '评价痛点 · 人均区间' },
    { title: 'Nori 爆款素材库：城市探店 42 条', url: '#', meta: '知识库 · 内部沉淀' },
  ];
  return (
    <>
      <AgentCardShell
        label="Agent Research 文档"
        icon="search"
        title="上海饭店推荐研究结果与内容策略"
        action={<button onClick={onContinue} style={{ ...pillButtonStyle(true), height: 38, borderRadius: 13, fontSize: 13 }}>进入内容制作<Icon name="arrowRight" size={14} /></button>}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center' }}>
          <div style={{ color: T.navyLight, fontSize: 11.5, fontWeight: 700 }}>内容文档</div>
          <button onClick={onOpenDocument} style={{ ...pillButtonStyle(false), height: 34, borderRadius: 12, fontSize: 12.5 }}>
            Canvas 查看
            <Icon name="expand" size={13} />
          </button>
        </div>
        <div style={{ display: 'grid', gap: 12 }}>
          {[
            ['研究结果', '收藏率更高的内容通常先回答“第一次去怎么点”，再补位置、价格和适合场景。'],
            ['内容策略', '切入角度放在“第一次去照着点”，图片负责建立食欲和真实感，正文负责降低决策成本。'],
            ['素材使用', '优先使用菜品近景、餐桌环境和菜单局部，不做过度精修，保留真实到店感。'],
          ].map(([label, text]) => (
            <div key={label} style={{ display: 'grid', gap: 4 }}>
              <span style={{ color: T.navy, fontSize: 12.8, fontWeight: 700 }}>{label}</span>
              <span style={{ color: T.navyMid, fontSize: 13, lineHeight: 1.72, fontWeight: 460 }}>{text}</span>
            </div>
          ))}
        </div>
        <div style={{ display: 'grid', gap: 8 }}>
          {sources.map(source => (
            <a key={source.title} href={source.url} target="_blank" style={{ textDecoration: 'none', display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center', padding: '9px 10px', borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(250,252,254,.72)', color: T.navyMid }}>
              <span style={{ minWidth: 0, fontSize: 12.6, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{source.title}</span>
              <span style={{ flexShrink: 0, color: T.navyLight, fontSize: 11.2 }}>{source.meta}</span>
            </a>
          ))}
        </div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, minmax(0, 1fr))', gap: 9 }}>
          {GENERATED_IMAGES.map((img, index) => (
            <a key={img.id} href={img.image} target="_blank" style={{ textDecoration: 'none', color: T.navyMid, minWidth: 0 }}>
              <div style={{ aspectRatio: '1 / 1', overflow: 'hidden', borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: img.palette[0] }}>
                <GenerationImageVisual item={img} overlay={false} />
              </div>
              <div style={{ marginTop: 5, fontSize: 10.8, color: T.navyLight, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>素材 {index + 1}</div>
            </a>
          ))}
        </div>
      </AgentCardShell>
    </>
  );
};

const FinalOutputStep = ({ onPreview, onTransform, onPublish, onEditImage }) => {
  const [title, setTitle] = React.useState(generatedPostCopy.title);
  const [body, setBody] = React.useState(generatedPostCopy.body.join('\n\n'));
  const [tags, setTags] = React.useState(generatedPostCopy.tags);
  return (
  <AgentCardShell
    label="Agent 输出"
    icon="document"
    title=""
    style={{ gap: 14 }}
  >
    <div style={{ display: 'grid', gap: 10 }}>
      <div style={{ display: 'grid', gap: 12 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, minmax(0, 1fr))', gap: 10 }}>
          {GENERATED_IMAGES.map((img, index) => (
            <button
              key={img.id}
              onClick={() => onEditImage?.(img)}
              style={{
                minWidth: 0,
                border: 'none',
                background: 'transparent',
                padding: 0,
                cursor: 'pointer',
                textAlign: 'left',
              }}
            >
              <div style={{ aspectRatio: '3 / 4', borderRadius: 0, overflow: 'hidden', background: img.palette[0], position: 'relative' }}>
                <GenerationImageVisual item={img} />
                <span style={{
                  position: 'absolute',
                  right: 8,
                  top: 8,
                  width: 22,
                  height: 22,
                  borderRadius: 8,
                  background: 'rgba(255,255,255,.76)',
                  color: T.navyMid,
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: 10.5,
                  fontWeight: 760,
                }}>{index + 1}</span>
              </div>
              <div style={{ marginTop: 6, color: T.navy, fontSize: 11.8, fontWeight: 700 }}>{img.title}</div>
            </button>
          ))}
        </div>
      </div>
      <div style={{
        paddingTop: 10,
        borderTop: `1px solid ${T.hairlineSoft}`,
        display: 'grid',
        gap: 10,
      }}>
        <input
          value={title}
          onChange={e => setTitle(e.target.value)}
          style={{
            width: '100%',
            border: 'none',
            background: 'transparent',
            outline: 'none',
            color: T.navy,
            fontSize: 17,
            fontWeight: 760,
            lineHeight: 1.42,
            fontFamily: T.fontSans,
            padding: 0,
          }}
        />
        <textarea
          value={body}
          onChange={e => setBody(e.target.value)}
          rows={7}
          style={{
            width: '100%',
            margin: 0,
            border: 'none',
            background: 'transparent',
            color: T.navyMid,
            fontSize: 13.5,
            lineHeight: 1.82,
            fontFamily: T.fontSans,
            resize: 'vertical',
            outline: 'none',
            padding: 0,
          }}
        />
      </div>
    </div>
    <div style={{ display: 'flex', gap: 7, flexWrap: 'wrap', marginTop: 8 }}>
      {tags.map((tag, index) => (
        <input
          key={`${tag}-${index}`}
          value={tag}
          onChange={e => setTags(list => list.map((item, i) => i === index ? e.target.value : item))}
          style={{
            width: `${Math.max(84, tag.length * 13)}px`,
            height: 28,
            padding: '0 10px',
            borderRadius: 999,
            background: 'rgba(255,255,255,.78)',
            border: `1px solid ${T.hairlineSoft}`,
            color: T.navyMid,
            display: 'inline-flex',
            alignItems: 'center',
            fontSize: 12,
            fontWeight: 620,
            outline: 'none',
            fontFamily: T.fontSans,
          }}
        />
      ))}
    </div>
    <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginTop: 16 }}>
      <button onClick={onPreview} style={{ ...pillButtonStyle(false), height: 36, borderRadius: 12, fontSize: 12.5 }}>
        <Icon name="eye" size={14} />
        预览模式
      </button>
      <button onClick={(e) => onTransform?.(e.currentTarget.getBoundingClientRect())} style={{ ...pillButtonStyle(false), height: 36, borderRadius: 12, fontSize: 12.5, background: 'rgba(255,255,255,.78)', color: T.navyMid, border: `1px solid ${T.hairlineSoft}` }}>
        <Icon name="transform" size={14} />
        转换
      </button>
      <button onClick={onPublish} style={{ ...pillButtonStyle(true), height: 36, borderRadius: 12, fontSize: 12.5, background: T.navy, color: T.white, border: '1px solid rgba(14,14,44,.12)', boxShadow: '0 12px 24px rgba(14,14,44,.14)' }}>
        <Icon name="send" size={14} />
        发布
      </button>
    </div>
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', gap: 8 }}>
      <div style={{ color: T.success, fontSize: 13.2, fontWeight: 680, marginTop: 8 }}>推荐发布时间：{generatedPostCopy.publishTime}</div>
    </div>
  </AgentCardShell>
  );
};

/* Main GenerationPage */
const GenerationPage = ({ initialPrompt, assetDraft, skillDraft, onboardingDraft, inspirationDraft, onBackHome, onNewChat, onOpenAssets, onOpenInsights, onOpenMine, onOpenHomeInspiration }) => {
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
  const [mode, setMode] = React.useState('edit');
  const [canvasWidth, setCanvasWidth] = React.useState(760);
  const [toolbarCollapsed, setToolbarCollapsed] = React.useState(false);
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [transformOpen, setTransformOpen] = React.useState(false);
  const [transformAnchor, setTransformAnchor] = React.useState(null);
  const [followUps, setFollowUps] = React.useState([]);
  const [imagePrompt, setImagePrompt] = React.useState(inspirationDraft?.prompt || '');
  const scrollRef = React.useRef(null);
  const contentRef = React.useRef(null);
  const bottomAnchorRef = React.useRef(null);
  const scrollJobRef = React.useRef(null);
  const shouldFollowScrollRef = React.useRef(true);

  const selectedCanvasAsset = selectedCover ? {
    palette: selectedCover.palette,
    shape: selectedCover.id === 'cover-b' ? 'ribbon' : selectedCover.id === 'cover-c' ? 'bloom' : 'petal',
    rotate: selectedCover.id === 'cover-c' ? -3 : selectedCover.id === 'cover-b' ? 4 : 0,
    label: selectedCover.title,
  } : null;

  const sessions = [
    '上海饭店推荐 · 当前',
    '下班后小馆地图',
    '人均 80 约饭清单',
    '产品测评 · AI 视频工具横评',
  ];

  const scrollToLatest = React.useCallback((behavior = 'auto', force = false) => {
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
    scrollToLatest('auto', true);
    const t1 = window.setTimeout(() => scrollToLatest('auto', true), 80);
    const t2 = window.setTimeout(() => scrollToLatest('auto', true), 260);
    return () => {
      window.clearTimeout(t1);
      window.clearTimeout(t2);
    };
  }, [stage, followUps.length, selectedTopic, scrollToLatest]);

  React.useEffect(() => {
    const node = scrollRef.current;
    if (!node) return undefined;
    const onScroll = () => {
      shouldFollowScrollRef.current = isNearScrollBottom(node, 140);
    };
    node.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    return () => node.removeEventListener('scroll', onScroll);
  }, []);

  React.useEffect(() => {
    if (!scrollRef.current || !contentRef.current) return undefined;
    const observer = new MutationObserver(() => scrollToLatest('auto'));
    const resizeObserver = new ResizeObserver(() => scrollToLatest('auto'));
    observer.observe(contentRef.current, { childList: true, subtree: true, characterData: true });
    resizeObserver.observe(contentRef.current);
    return () => {
      observer.disconnect();
      resizeObserver.disconnect();
    };
  }, [scrollToLatest]);

  const startFromUserPrompt = React.useCallback((text) => {
    if (!text.trim()) return;
    setFollowUps(f => [...f, { kind: 'msg', payload: text.trim(), id: Date.now() }]);
    setStage(1);
  }, []);

  const pickTopic = (topic, ai = false) => {
    setSelectedTopic(topic);
    setClarification(null);
    setFollowUps(f => [...f, { kind: 'msg', payload: ai ? `AI 帮我决定：${topic.title}` : `选择选题：${topic.title}`, id: Date.now() }]);
    window.setTimeout(() => setStage(2), 280);
  };

  const advanceGenerationStage = React.useCallback((nextStage) => {
    setStage(current => current < nextStage ? nextStage : current);
  }, []);

  const onTransformPick = (target) => {
    setTransformOpen(false);
    setTransformAnchor(null);
    setFollowUps(f => [...f, { kind: 'transform', payload: target, id: Date.now() }]);
  };

  const onPublish = () => {
    setFollowUps(f => [...f, { kind: 'link', id: Date.now() }]);
  };
  const onLinked = () => {
    setFollowUps(f => [...f, { kind: 'draft', id: Date.now() + 1 }]);
  };

  const openEditor = () => {
    setMode('text');
    setCanvasExpanded(true);
    setCanvasOpen(true);
  };

  const openPreviewCanvas = () => {
    setMode('preview');
    setCanvasExpanded(false);
    setCanvasWidth(520);
    setCanvasOpen(true);
  };

  const openImageEditor = (image) => {
    setSelectedImage(image);
    setMode('image');
    setCanvasExpanded(true);
    setCanvasOpen(true);
  };

  React.useEffect(() => {
    if (!inspirationDraft?.prompt) return;
    setImagePrompt(inspirationDraft.prompt);
    openImageEditor(GENERATED_IMAGES[0]);
  }, [inspirationDraft?.prompt]);

  return (
    <div style={{ display: 'flex', height: '100%', width: '100%', background: 'linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)', position: 'relative', overflow: 'hidden' }}>
      <Sidebar
        active="home"
        onNew={onNewChat || (() => {})}
        onNavigate={(id) => {
          if (id === 'home') onBackHome();
          if (id === 'library' && onOpenAssets) onOpenAssets();
          if (id === 'insights' && onOpenInsights) onOpenInsights();
          if (id === 'mine' && onOpenMine) onOpenMine();
        }}
        sessions={sessions}
        collapsed={navCollapsed}
        onToggle={() => setNavCollapsed(v => !v)}
      />

      <main style={{
        flex: 1,
        display: 'flex',
        flexDirection: 'column',
        minWidth: 0,
        position: 'relative',
      }}>
        <div style={{
          height: 56,
          padding: '0 24px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          borderBottom: `1px solid ${T.hairlineSoft}`,
          background: 'rgba(250,252,254,.76)',
          backdropFilter: 'blur(18px) saturate(1.16)',
          flexShrink: 0,
        }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0 }}>
          <button onClick={onBackHome} style={iconBtnStyle()}>
            <Icon name="home" size={16} color={T.navyMid} />
          </button>
            <div style={{ minWidth: 0 }}>
            <div style={{ fontSize: 13, fontWeight: 600, color: T.navy, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {onboardingDraft?.topic || selectedTopic?.title || '上海饭店推荐图文'}
            </div>
              <div style={{ fontSize: 10.5, color: T.navyLight, fontFamily: T.fontMono }}>Chat 生成 · 编辑时进入 Canvas</div>
          </div>
        </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }} />
        </div>

        <div ref={scrollRef} style={{ flex: 1, minHeight: 0, overflowY: 'auto', padding: '28px 0 24px' }}>
          <div ref={contentRef} style={{
            maxWidth: 780,
            margin: '0 auto',
            padding: '0 24px',
            display: 'flex',
            flexDirection: 'column',
            gap: 24,
          }}>
            {stage === 0 ? (
              <AgentCardShell
                label="Agent 开场"
                icon="chat"
                title={isSkillStart ? `已载入「${skillDraft.title}」Skill` : '我是 Nori，可以帮你把内容一步步做出来'}
              >
                <p style={{ margin: 0 }}>我会按选题、意图澄清、任务规划、Research、内容制作、Review 和 Output 的顺序，在 chat 里逐步生成并保留历史。</p>
              </AgentCardShell>
            ) : (
              <Bubble from="user">
                {initialPrompt || onboardingDraft?.topic || followUps.find(f => f.kind === 'msg')?.payload || '我想做一篇上海饭店推荐图文'}
              </Bubble>
            )}

            {stage >= 1 && (
              <TopicChoiceStep
                selected={selectedTopic}
                onSelect={(topic) => pickTopic(topic)}
                onAiDecide={() => pickTopic(GENERATION_TOPIC_OPTIONS[0], true)}
              />
            )}

            {selectedTopic && stage >= 2 && (
              <>
                <Bubble from="user">选择选题：{selectedTopic.title}</Bubble>
                <AgentStepSequence
                  resetKey={`topic-${selectedTopic.id}`}
                  parseMessages={['正在解析你选择的选题', '解析中', '正在匹配上海饭店推荐内容结构']}
                  reply="我先拆一下这个选题：它适合做成收藏型上海饭店推荐，核心是先降低第一次到店的决策成本，再用真实图片建立食欲和信任。"
                  onComplete={() => advanceGenerationStage(3)}
                />
              </>
            )}

            {stage >= 3 && (
              <>
                <IntentClarificationStep
                  onConfirm={(form) => {
                    setClarification(form);
                    setStage(4);
                  }}
                  onSkip={() => setStage(4)}
                />
                {stage > 3 && (
                  <Bubble from="user">
                    {clarification ? `补充信息：${[clarification.location || '位置稍后补充', clarification.price, clarification.platform].filter(Boolean).join(' / ')}` : '跳过补充信息，先进入任务规划'}
                  </Bubble>
                )}
              </>
            )}

            {stage >= 4 && (
                <AgentStepSequence
                  resetKey="generation-planning"
                  parseMessages={['正在生成任务规划', '解析中', '正在拆解执行步骤']}
                  reply="下面是任务规划。我会先把检索、爆款拆解、素材沉淀和内容制作分开跑，保证后面的图文不是凭空生成。"
                  onComplete={() => advanceGenerationStage(5)}
              />
            )}

            {stage >= 5 && (
              <GenerationResearchStep
                onOpenDocument={openEditor}
                onContinue={() => setStage(6)}
              />
              )}

            {stage >= 6 && (
                <AgentStepSequence
                  resetKey="generation-making"
                  parseMessages={['正在制作内容', '生成中', '正在整合图片、正文和标签']}
                  reply="开始制作内容。我会把封面、正文图、标题、正文、标签和发布时间放在同一份可编辑结果里。"
                  onComplete={() => advanceGenerationStage(7)}
                />
              )}

            {stage >= 7 && (
              <FinalOutputStep
                onPreview={openPreviewCanvas}
                onTransform={(rect) => {
                  setTransformAnchor(rect);
                  setTransformOpen(true);
                }}
                onPublish={onPublish}
                onEditImage={openImageEditor}
              />
            )}

            {followUps.map(f => {
              if (f.kind === 'transform') return <TransformLaunched key={f.id} target={f.payload} />;
              if (f.kind === 'link') return <PublishLinkAccount key={f.id} onLinked={onLinked} />;
              if (f.kind === 'draft') return <PublishDraftSaved key={f.id} />;
              return null;
            })}
            <div ref={bottomAnchorRef} style={{ height: 1 }} />
          </div>
        </div>

        <div style={{
          padding: '12px 24px 18px',
          background: 'linear-gradient(to top, rgba(250,252,254,.98) 62%, rgba(250,252,254,0))',
          flexShrink: 0,
        }}>
          <div style={{ maxWidth: 780, margin: '0 auto' }}>
            {onboardingDraft && (
              <div style={{
                marginBottom: 10,
                padding: '9px 11px',
                borderRadius: 13,
                background: 'rgba(255,255,255,.78)',
                border: `1px solid ${T.hairlineSoft}`,
                boxShadow: '0 8px 18px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.86)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                gap: 12,
                flexWrap: 'wrap',
              }}>
                <div style={{ display: 'inline-flex', alignItems: 'center', gap: 8, minWidth: 0 }}>
                  <span style={{
                    width: 24,
                    height: 24,
                    borderRadius: 9,
                    background: T.successTint,
                    color: T.success,
                    display: 'inline-flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                  }}>
                    <Icon name="check" size={13} stroke={2.2} />
                  </span>
                  <span style={{ fontSize: 12.5, color: T.navyMid, fontWeight: 580, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                    账号规划已启用 · 来自账号定位 · {onboardingDraft.positioning}
                  </span>
                </div>
              </div>
            )}
            <ChatComposer
              placeholder={stage === 0 ? '告诉 Nori：你想做什么内容？' : '继续追问 Nori，或描述你的修改想法…'}
              initialValue={stage === 0 ? (skillDraft ? skillDraft.prompt : onboardingDraft?.topic || '') : ''}
              autoFocusKey={skillDraft?.id || onboardingDraft?.topic}
              onSend={(t) => {
                if (stage === 0) startFromUserPrompt(t);
                else setFollowUps(f => [...f, { kind: 'msg', payload: t, id: Date.now() }]);
              }}
            />
          </div>
        </div>
      </main>

      <Canvas
        open={canvasOpen}
        expanded={canvasExpanded}
        setExpanded={setCanvasExpanded}
        onClose={() => setCanvasOpen(false)}
        onTransform={(rect) => {
          setTransformAnchor(rect);
          setTransformOpen(true);
        }}
        onPublish={onPublish}
        mode={mode}
        setMode={setMode}
        selectedAsset={selectedCanvasAsset}
        selectedImage={selectedImage}
        imagePrompt={imagePrompt}
        onOpenInspiration={onOpenHomeInspiration}
        width={canvasWidth}
        toolbarCollapsed={toolbarCollapsed}
        setToolbarCollapsed={setToolbarCollapsed}
      />

      <TransformMenu
        open={transformOpen}
        anchorRect={transformAnchor}
        onClose={() => {
          setTransformOpen(false);
          setTransformAnchor(null);
        }}
        onPick={onTransformPick}
      />
    </div>
  );
};

window.GenerationPage = GenerationPage;
window.ToolPill = window.ToolPill; // already global from home

/* ─── Account planning onboarding ─── */

const PlanningOption = ({ icon, title, desc, active, onClick }) => (
  <button
    onClick={onClick}
    style={{
      border: `1px solid ${active ? 'rgba(75,77,237,.22)' : T.hairlineSoft}`,
      background: active ? 'rgba(239,239,253,.76)' : 'rgba(255,255,255,.76)',
      borderRadius: 16,
      padding: '13px 14px',
      cursor: 'pointer',
      textAlign: 'left',
      display: 'flex',
      alignItems: 'flex-start',
      gap: 11,
      boxShadow: active ? '0 10px 24px rgba(75,77,237,.07), inset 0 1px 0 rgba(255,255,255,.86)' : '0 8px 20px rgba(14,14,44,.035)',
      transition: `transform .28s ${T.spring}, box-shadow .28s ${T.spring}, border .24s ${T.ease}, background .24s ${T.ease}`,
    }}
    onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-2px)'}
    onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}
  >
    <span style={{
      width: 34,
      height: 34,
      borderRadius: 12,
      background: active ? T.white : T.surfaceWh,
      color: active ? T.iris : T.navyMid,
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      flexShrink: 0,
      boxShadow: 'inset 0 1px 0 rgba(255,255,255,.8)',
    }}>
      <Icon name={icon} size={16} />
    </span>
    <span>
      <span style={{ display: 'block', fontSize: 13.5, fontWeight: 720, color: T.navy }}>{title}</span>
      <span style={{ display: 'block', marginTop: 4, fontSize: 11.8, lineHeight: 1.45, color: T.navyLight }}>{desc}</span>
    </span>
  </button>
);

const PlanningStepper = ({ steps, step, isMobile }) => (
  <div style={{
    display: 'inline-flex',
    alignItems: 'center',
    gap: isMobile ? 6 : 8,
    maxWidth: '100%',
    overflowX: 'auto',
    padding: isMobile ? '5px' : '6px',
    borderRadius: 999,
    background: 'rgba(255,255,255,.86)',
    border: `1px solid ${T.hairlineSoft}`,
    boxShadow: '0 10px 26px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.86)',
  }}>
    {steps.map((s, i) => {
      const done = step > s.id;
      const active = step === s.id;
      return (
        <React.Fragment key={s.id}>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 8,
            height: 34,
            padding: '0 10px',
            borderRadius: 999,
            color: active ? T.navy : done ? T.navyMid : T.navySoft,
            fontSize: isMobile ? 12 : 12.5,
            fontWeight: active ? 760 : 680,
            whiteSpace: 'nowrap',
          }}>
            <span style={{
              width: 24,
              height: 24,
              borderRadius: '50%',
              background: done ? T.success : active ? T.navy : 'rgba(14,14,44,.055)',
              color: done ? T.white : active ? T.primary : T.navySoft,
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 11,
              fontFamily: T.fontMono,
              fontWeight: 800,
              flexShrink: 0,
              boxShadow: active ? '0 8px 18px rgba(14,14,44,.14)' : 'none',
            }}>{done ? '✓' : s.id}</span>
            {s.label}
          </div>
          {i < steps.length - 1 && <span style={{ width: 22, height: 1, background: 'rgba(14,14,44,.10)', flexShrink: 0 }} />}
        </React.Fragment>
      );
    })}
  </div>
);

const PlanningCompactProgress = ({ steps, step, isMobile }) => (
  <div style={{
    display: 'inline-flex',
    alignItems: 'center',
    gap: isMobile ? 8 : 12,
    minWidth: 0,
  }}>
    <div style={{ display: 'inline-flex', alignItems: 'center', gap: isMobile ? 5 : 7 }}>
      {steps.map(s => {
        const active = step === s.id;
        const done = step > s.id;
        return (
          <span
            key={s.id}
            aria-label={`${s.label}${active ? '，当前步骤' : ''}`}
            style={{
              width: active ? 34 : 14,
              height: 7,
              borderRadius: 999,
              background: active || done ? T.navy : 'rgba(14,14,44,.12)',
              opacity: active ? 1 : done ? .9 : .72,
              transition: `width .28s ${T.spring}, background .2s ${T.ease}, opacity .2s ${T.ease}`,
              flexShrink: 0,
            }}
          />
        );
      })}
    </div>
    <span style={{
      color: T.navyLight,
      fontSize: isMobile ? 12.5 : 14,
      fontWeight: 560,
      whiteSpace: 'nowrap',
      fontFamily: T.fontMono,
    }}>
      第 {step} / {steps.length} 步
    </span>
  </div>
);

const AttachmentChip = ({ attachment, onRemove }) => {
  const icon = attachment.type === 'link' ? 'link' : attachment.type === 'image' ? 'image' : 'document';
  return (
    <span style={{
      maxWidth: '100%',
      height: 34,
      padding: '0 9px 0 10px',
      borderRadius: 12,
      background: 'rgba(255,255,255,.86)',
      border: `1px solid ${T.hairlineSoft}`,
      boxShadow: '0 6px 14px rgba(14,14,44,.035), inset 0 1px 0 rgba(255,255,255,.86)',
      display: 'inline-flex',
      alignItems: 'center',
      gap: 8,
      color: T.navyMid,
      fontSize: 12.5,
      fontWeight: 620,
    }}>
      <Icon name={icon} size={14} color={attachment.type === 'image' ? T.iris : T.navyMid} />
      <span style={{ minWidth: 0, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{attachment.label}</span>
      <button onClick={onRemove} style={{ border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', padding: 0, display: 'inline-flex' }}>
        <Icon name="close" size={12} />
      </button>
    </span>
  );
};

const InputMethodModal = ({ type, onClose, onConfirm }) => {
  const [value, setValue] = React.useState(type === 'link' ? 'https://example.com/meituan/shop/暖胃小馆' : type === 'text' ? '我在社区附近开了一家家常小馆，想做小红书引流到店。' : '');
  const fileRef = React.useRef(null);
  const title = type === 'link' ? '粘贴网址' : type === 'image' ? '上传图片' : '直接描述';
  const hint = type === 'link' ? '可以是店铺、账号、文章或竞品链接' : type === 'image' ? '选择产品图、菜单截图或账号截图' : '用一句话说清楚你是做什么的';
  const confirm = () => {
    const clean = value.trim();
    if (!clean) return;
    onConfirm({
      type,
      label: type === 'link' ? clean.replace(/^https?:\/\//, '') : clean,
      value: clean,
    });
  };
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 1200, background: 'rgba(14,14,44,.22)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 18 }}>
      <div style={{
        width: 'min(460px, 100%)',
        borderRadius: 24,
        background: T.white,
        border: `1px solid ${T.hairlineSoft}`,
        boxShadow: '0 36px 90px rgba(14,14,44,.22)',
        padding: 20,
        animation: `fadeInScale .32s ${T.spring} both`,
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', gap: 14, alignItems: 'flex-start', marginBottom: 16 }}>
          <div>
            <h3 style={{ margin: 0, fontSize: 18, fontWeight: 760, color: T.navy, letterSpacing: 0 }}>{title}</h3>
            <p style={{ margin: '6px 0 0', fontSize: 12.5, color: T.navyLight, lineHeight: 1.55 }}>{hint}</p>
          </div>
          <button onClick={onClose} style={iconBtnStyle()}><Icon name="close" size={13} /></button>
        </div>

        {type === 'image' ? (
          <div>
            <input
              ref={fileRef}
              type="file"
              accept="image/*"
              style={{ display: 'none' }}
              onChange={e => {
                const file = e.target.files?.[0];
                if (file) setValue(file.name);
              }}
            />
            <button onClick={() => fileRef.current?.click()} style={{
              width: '100%',
              height: 118,
              borderRadius: 18,
              border: '1.5px dashed rgba(14,14,44,.14)',
              background: 'rgba(250,252,254,.88)',
              color: T.navyMid,
              cursor: 'pointer',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 9,
              fontSize: 13,
              fontWeight: 650,
            }}>
              <Icon name="upload" size={22} />
              {value || '选择本地图片'}
            </button>
          </div>
        ) : (
          <textarea
            value={value}
            onChange={e => setValue(e.target.value)}
            rows={type === 'text' ? 5 : 3}
            style={{
              width: '100%',
              border: `1px solid ${T.hairlineSoft}`,
              borderRadius: 16,
              background: 'rgba(250,252,254,.86)',
              padding: '12px 13px',
              resize: 'vertical',
              outline: 'none',
              color: T.navy,
              fontSize: 13.5,
              lineHeight: 1.62,
              fontFamily: T.fontSans,
            }}
          />
        )}

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, marginTop: 16 }}>
          <button onClick={onClose} style={{ height: 38, padding: '0 14px', border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', fontSize: 13, fontWeight: 650 }}>取消</button>
          <button onClick={confirm} disabled={!value.trim()} style={{
            height: 38,
            padding: '0 16px',
            borderRadius: 13,
            border: 'none',
            background: value.trim() ? T.navy : T.surface,
            color: value.trim() ? T.white : T.navyLight,
            cursor: value.trim() ? 'pointer' : 'not-allowed',
            fontSize: 13,
            fontWeight: 720,
          }}>确认</button>
        </div>
      </div>
    </div>
  );
};

const PlanningComposerBox = ({ attachment, text, setText, onRemoveAttachment, onSend }) => (
  <div style={{
    borderRadius: 20,
    border: `1px solid ${T.hairlineSoft}`,
    background: 'rgba(255,255,255,.86)',
    boxShadow: '0 14px 32px rgba(14,14,44,.05), inset 0 1px 0 rgba(255,255,255,.86)',
    padding: 12,
  }}>
    {attachment && (
      <div style={{ display: 'flex', marginBottom: 10, maxWidth: '100%' }}>
        <AttachmentChip attachment={attachment} onRemove={onRemoveAttachment} />
      </div>
    )}
    <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 38px', gap: 9, alignItems: 'end' }}>
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        rows={2}
        placeholder={attachment ? '可以继续补充一句说明...' : '先选择一种输入方式，或直接补充你的想法'}
        style={{
          width: '100%',
          border: 'none',
          outline: 'none',
          resize: 'none',
          background: 'transparent',
          color: T.navy,
          minHeight: 48,
          fontSize: 13.5,
          lineHeight: 1.6,
          fontFamily: T.fontSans,
        }}
      />
      <button onClick={onSend} disabled={!attachment && !text.trim()} style={{
        width: 38,
        height: 38,
        borderRadius: '50%',
        border: 'none',
        background: attachment || text.trim() ? T.navy : 'rgba(14,14,44,.075)',
        color: attachment || text.trim() ? T.white : T.navyLight,
        cursor: attachment || text.trim() ? 'pointer' : 'not-allowed',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <Icon name="arrowUp" size={15} stroke={2} />
      </button>
    </div>
  </div>
);

const PlanningComposerMulti = ({ attachments, text, setText, onRemoveAttachment, onSend }) => (
  <div style={{
    borderRadius: 20,
    border: `1px solid ${T.hairlineSoft}`,
    background: 'rgba(255,255,255,.86)',
    boxShadow: '0 14px 32px rgba(14,14,44,.05), inset 0 1px 0 rgba(255,255,255,.86)',
    padding: 12,
  }}>
    {attachments.length > 0 && (
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 10, maxWidth: '100%' }}>
        {attachments.map((att, index) => (
          <AttachmentChip key={`${att.type}-${att.label}-${index}`} attachment={att} onRemove={() => onRemoveAttachment(index)} />
        ))}
      </div>
    )}
    <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 38px', gap: 9, alignItems: 'end' }}>
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        rows={2}
        placeholder={attachments.length ? '可以继续补充一句说明...' : '先选择一种输入方式，或直接补充你的想法'}
        style={{
          width: '100%',
          border: 'none',
          outline: 'none',
          resize: 'none',
          background: 'transparent',
          color: T.navy,
          minHeight: 48,
          fontSize: 13.5,
          lineHeight: 1.6,
          fontFamily: T.fontSans,
        }}
      />
      <button onClick={onSend} disabled={!attachments.length && !text.trim()} style={{
        width: 38,
        height: 38,
        borderRadius: '50%',
        border: 'none',
        background: attachments.length || text.trim() ? T.navy : 'rgba(14,14,44,.075)',
        color: attachments.length || text.trim() ? T.white : T.navyLight,
        cursor: attachments.length || text.trim() ? 'pointer' : 'not-allowed',
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <Icon name="arrowUp" size={15} stroke={2} />
      </button>
    </div>
  </div>
);

const InlineEditableCard = ({ title, value, onChange, rows = 4 }) => (
  <PlanningPanel title={title}>
    <textarea
      value={value}
      onChange={e => onChange(e.target.value)}
      rows={rows}
      style={{
        width: '100%',
        border: 'none',
        borderRadius: 14,
        background: 'rgba(250,252,254,.76)',
        padding: 12,
        resize: 'vertical',
        outline: 'none',
        color: T.navyMid,
        fontSize: 13,
        lineHeight: 1.68,
        fontFamily: T.fontSans,
        boxShadow: `inset 0 0 0 1px ${T.hairlineSoft}`,
      }}
    />
  </PlanningPanel>
);

const EditableListPanel = ({ title, items, onChange, muted }) => (
  <PlanningPanel title={title} muted={muted}>
    <div style={{ display: 'grid', gap: 8 }}>
      {items.map((text, index) => (
        <input
          key={`${title}-${index}`}
          value={text}
          onChange={e => onChange(items.map((item, i) => i === index ? e.target.value : item))}
          style={{
            width: '100%',
            minHeight: 36,
            border: `1px solid ${T.hairlineSoft}`,
            borderRadius: 12,
            background: 'rgba(250,252,254,.72)',
            color: T.navyMid,
            padding: '0 10px',
            outline: 'none',
            fontSize: 12.8,
            fontFamily: T.fontSans,
          }}
        />
      ))}
    </div>
  </PlanningPanel>
);

const DiagnosisCard = ({ title, value, defaultValue, onChange, confirmed, onConfirm }) => {
  const [editing, setEditing] = React.useState(false);
  const [draft, setDraft] = React.useState(value);
  React.useEffect(() => setDraft(value), [value]);
  return (
    <PlanningPanel
      title={title}
      action={!editing && (
        <div style={{ display: 'flex', gap: 7 }}>
          <button onClick={() => setEditing(true)} style={{ height: 30, padding: '0 10px', borderRadius: 10, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.72)', color: T.navyMid, cursor: 'pointer', fontSize: 12, fontWeight: 650 }}>修改</button>
          <button onClick={onConfirm} style={{ height: 30, padding: '0 10px', borderRadius: 10, border: 'none', background: confirmed ? T.successTint : T.navy, color: confirmed ? T.success : T.white, cursor: 'pointer', fontSize: 12, fontWeight: 700 }}>{confirmed ? '已确认' : '确认'}</button>
        </div>
      )}
    >
      {editing ? (
        <div>
          <textarea
            value={draft}
            onChange={e => setDraft(e.target.value)}
            rows={4}
            style={{
              width: '100%',
              border: `1px solid ${T.hairlineSoft}`,
              borderRadius: 14,
              background: 'rgba(250,252,254,.88)',
              padding: 12,
              resize: 'vertical',
              outline: 'none',
              color: T.navy,
              fontSize: 13,
              lineHeight: 1.65,
              fontFamily: T.fontSans,
            }}
          />
          <div style={{ marginTop: 10, display: 'flex', justifyContent: 'flex-end', gap: 8 }}>
            <button onClick={() => setDraft(defaultValue)} style={{ ...iconBtnStyle(), width: 34, height: 34 }}><Icon name="refresh" size={13} /></button>
            <button onClick={() => { onChange(draft); onConfirm(); setEditing(false); }} style={{ height: 34, padding: '0 13px', border: 'none', borderRadius: 12, background: T.navy, color: T.white, cursor: 'pointer', fontSize: 12.5, fontWeight: 700 }}>确认</button>
          </div>
        </div>
      ) : (
        <p style={{ margin: 0, color: T.navyMid, fontSize: 13, lineHeight: 1.68 }}>{value}</p>
      )}
    </PlanningPanel>
  );
};

const CopyableRow = ({ text, copied, onCopy }) => (
  <div style={{
    display: 'grid',
    gridTemplateColumns: 'minmax(0, 1fr) 28px',
    gap: 8,
    alignItems: 'center',
    padding: '9px 10px',
    borderRadius: 12,
    background: 'rgba(250,252,254,.72)',
    border: `1px solid ${T.hairlineSoft}`,
  }}>
    <span style={{ fontSize: 12.8, color: T.navyMid, lineHeight: 1.52 }}>{text}</span>
    <button onClick={() => onCopy(text)} title="复制" style={{ border: 'none', background: copied === text ? T.successTint : 'rgba(255,255,255,.76)', color: copied === text ? T.success : T.navyLight, width: 28, height: 28, borderRadius: 9, cursor: 'pointer', display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
      <Icon name={copied === text ? 'check' : 'copy'} size={12} />
    </button>
  </div>
);

const MiniOnionBurst = ({ active }) => {
  if (!active) return null;
  return (
    <div aria-hidden="true" style={{ position: 'absolute', top: 38, right: 56, width: 1, height: 1, pointerEvents: 'none', zIndex: 3 }}>
      {ONION_BURST_ASSETS.map((src, i) => (
        <img key={src} src={src} alt="" style={{
          position: 'absolute',
          width: 34,
          height: 34,
          objectFit: 'contain',
          '--x': `${[-74, 58, 82, -86, 18][i]}px`,
          '--y': `${[-48, -62, 24, 22, -88][i]}px`,
          '--r': `${[-16, 18, 12, -9, 7][i]}deg`,
          animation: `onionPop 1.25s ${i * 38}ms ${T.spring} both`,
          filter: 'drop-shadow(0 10px 18px rgba(14,14,44,.12))',
        }} />
      ))}
    </div>
  );
};

const PlanningChoice = ({ children, active, onClick }) => (
  <button
    onClick={onClick}
    style={{
      minHeight: 32,
      padding: '0 12px',
      borderRadius: 999,
      border: `1px solid ${active ? 'rgba(75,77,237,.16)' : T.hairlineSoft}`,
      background: active ? T.navy : 'rgba(255,255,255,.78)',
      color: active ? T.white : T.navyMid,
      fontSize: 12.2,
      fontWeight: active ? 680 : 560,
      cursor: 'pointer',
      boxShadow: active ? '0 10px 20px rgba(14,14,44,.12)' : '0 6px 14px rgba(14,14,44,.035)',
      transition: `transform .24s ${T.spring}, box-shadow .24s ${T.spring}, background .2s ${T.ease}, color .2s ${T.ease}`,
    }}
    onMouseEnter={e => e.currentTarget.style.transform = 'translateY(-1px)'}
    onMouseLeave={e => e.currentTarget.style.transform = 'translateY(0)'}
  >
    {children}
  </button>
);

const PlanningChoiceGroup = ({ title, hint, options, selected, onToggle, allowMultiple = false }) => (
  <AgentCardShell
    label={`Agent ${allowMultiple ? '多选' : '单选'}`}
    icon={allowMultiple ? 'layers' : 'target'}
    title={title}
    bodyStyle={{ color: T.navyMid, fontSize: 13.2, lineHeight: 1.68 }}
  >
    <div style={{ display: 'grid', gap: 10 }}>
      {hint && <div style={{ color: T.navyLight, fontSize: 12.1, lineHeight: 1.5 }}>{hint}</div>}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
        {options.map(option => {
          const active = allowMultiple ? selected.includes(option) : selected === option;
          return (
            <AgentChoice key={option} active={active} multiple={allowMultiple} onClick={() => onToggle(option)}>
              {option}
            </AgentChoice>
          );
        })}
      </div>
    </div>
  </AgentCardShell>
);

const PlanningReveal = ({ show = true, delay = 0, children, style }) => {
  if (!show) return null;
  return (
    <div style={{
      animation: `planningReveal 1.18s ${delay}ms ${T.ease} both`,
      overflow: 'hidden',
      willChange: 'opacity, transform, clip-path, filter',
      ...style,
    }}>
      {children}
    </div>
  );
};

const PLANNING_CHAT_INSET = 36;

const PlanningPanel = ({ title, children, action, muted, style }) => (
  <section style={{
    width: `calc(100% - ${PLANNING_CHAT_INSET}px)`,
    marginLeft: PLANNING_CHAT_INSET,
    border: `1px solid ${T.hairlineSoft}`,
    background: muted ? 'rgba(250,252,254,.68)' : 'rgba(255,255,255,.82)',
    borderRadius: 20,
    padding: 18,
    boxShadow: '0 14px 34px rgba(14,14,44,.045), inset 0 1px 0 rgba(255,255,255,.84)',
    backdropFilter: 'blur(18px) saturate(1.14)',
    ...style,
  }}>
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, marginBottom: 14 }}>
      <h3 style={{ margin: 0, fontSize: 15.5, fontWeight: 730, color: T.navy, letterSpacing: 0 }}>{title}</h3>
      {action}
    </div>
    {children}
  </section>
);

const EditableMiniField = ({ label, value, onChange, multiline }) => (
  <label style={{ display: 'block' }}>
    <span style={{ display: 'block', marginBottom: 6, fontSize: 11.5, color: T.navyLight, fontWeight: 620 }}>{label}</span>
    {multiline ? (
      <textarea
        value={value}
        onChange={e => onChange(e.target.value)}
        rows={3}
        style={{
          width: '100%',
          border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 13,
          background: 'rgba(255,255,255,.72)',
          padding: '10px 11px',
          resize: 'vertical',
          outline: 'none',
          color: T.navy,
          fontSize: 13,
          lineHeight: 1.55,
          fontFamily: T.fontSans,
        }}
      />
    ) : (
      <input
        value={value}
        onChange={e => onChange(e.target.value)}
        style={{
          width: '100%',
          height: 38,
          border: `1px solid ${T.hairlineSoft}`,
          borderRadius: 13,
          background: 'rgba(255,255,255,.72)',
          padding: '0 11px',
          outline: 'none',
          color: T.navy,
          fontSize: 13,
          fontFamily: T.fontSans,
        }}
      />
    )}
  </label>
);

const AccountPlanningPage = ({ onBackHome, onNewChat, onOpenAssets, onOpenSkills, onOpenInsights, onComplete }) => {
  const { isCompact, isTablet, isMobile } = useViewport();
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [step, setStep] = React.useState(1);
  const [method, setMethod] = React.useState(null);
  const [modalType, setModalType] = React.useState(null);
  const [attachment, setAttachment] = React.useState(null);
  const [rawInput, setRawInput] = React.useState('');
  const [sentIntro, setSentIntro] = React.useState(false);
  const [goal, setGoal] = React.useState(null);
  const [platform, setPlatform] = React.useState(null);
  const [confirmed, setConfirmed] = React.useState({});
  const [copied, setCopied] = React.useState('');
  const [reportBurst, setReportBurst] = React.useState(false);
  const [reportVariant, setReportVariant] = React.useState(0);
  const [diagnosisText, setDiagnosisText] = React.useState({
    position: '做附近人愿意收藏的烟火气小馆账号。你的优势不是大品牌感，而是稳定、真实、离用户很近。内容要让人觉得下班就能去。',
    audience: '23-38 岁附近上班族、情侣和周末约饭人群，关心味道稳定、价格舒服、距离方便。',
    directions: '招牌菜故事：让用户记住你和别的店不一样的地方。\n真实到店场景：降低第一次到店的心理成本。\n本地生活攻略：把餐厅内容变成可收藏的信息。',
    benchmarks: '@本地吃喝指南：标题清楚，适合学习选题包装。\n@街角小店日记：擅长把小店日常拍得有人情味。\n@城市午餐研究所：午餐场景切得细，容易引流到店。',
    selling: '稳定家常味 + 店主真实感 + 离附近人生活很近。',
  });
  const [persona, setPersona] = React.useState({
    name: '巷口暖胃小馆',
    bio: '每天认真做一碗有烟火气的家常饭',
    keywords: '亲切、会讲故事、懂本地生活',
    tone: '像熟人推荐一样自然，少一点广告感，多一点真实体验',
    cover: '暖色自然光、店内细节、菜品近景，标题留白清楚',
  });
  const [pillars, setPillars] = React.useState(['招牌菜背后的故事', '附近上班族午餐选择', '老板的一天', '真实顾客反馈']);
  const [calendar, setCalendar] = React.useState([
    { day: '周一', type: '探店图文', topic: '第一次来店里，先点这 3 道招牌菜', ref: '@本地吃喝指南' },
    { day: '周二', type: '短视频', topic: '后厨备菜 30 秒，看看一碗饭怎么被认真做好', ref: '@街角小店日记' },
    { day: '周三', type: '图文', topic: '附近上班族午餐不踩雷菜单', ref: '@城市午餐研究所' },
    { day: '周四', type: '长文', topic: '一家小店怎么把回头客留住', ref: '@主理人手记' },
    { day: '周五', type: '短视频', topic: '顾客最常问的 5 个问题', ref: '@真实探店' },
    { day: '周六', type: '图文', topic: '周末带朋友来吃，怎么点更划算', ref: '@本地生活家' },
    { day: '周日', type: '复盘', topic: '这周最受欢迎的一道菜', ref: '@小店经营笔记' },
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
    return undefined;
  }, [step, reportVariant]);

  const defaultDiagnosisText = {
    position: '做附近人愿意收藏的烟火气小馆账号。你的优势不是大品牌感，而是稳定、真实、离用户很近。内容要让人觉得下班就能去。',
    audience: '23-38 岁附近上班族、情侣和周末约饭人群，关心味道稳定、价格舒服、距离方便。',
    directions: '招牌菜故事：让用户记住你和别的店不一样的地方。\n真实到店场景：降低第一次到店的心理成本。\n本地生活攻略：把餐厅内容变成可收藏的信息。',
    benchmarks: '@本地吃喝指南：标题清楚，适合学习选题包装。\n@街角小店日记：擅长把小店日常拍得有人情味。\n@城市午餐研究所：午餐场景切得细，容易引流到店。',
    selling: '稳定家常味 + 店主真实感 + 离附近人生活很近。',
  };
  const canAdvanceStep1 = sentIntro && goal && platform;
  const steps = [
    { id: 1, label: '入口信息' },
    { id: 2, label: '账号诊断' },
    { id: 3, label: 'IP 画像' },
    { id: 4, label: '内容日历' },
    { id: 5, label: '开始制作' },
  ];
  const diagnosis = {
    position: '做附近人愿意收藏的烟火气小馆账号',
    reason: '你的优势不是大品牌感，而是稳定、真实、离用户很近。内容要让人觉得下班就能去。',
    audience: '23-38 岁附近上班族、情侣和周末约饭人群，关心味道稳定、价格舒服、距离方便。',
    directions: [
      ['招牌菜故事', '让用户记住你和别的店不一样的地方。'],
      ['真实到店场景', '降低第一次到店的心理成本。'],
      ['本地生活攻略', '把餐厅内容变成可收藏的信息。'],
    ],
    benchmarks: [
      ['@本地吃喝指南', '标题清楚，适合学习选题包装。'],
      ['@街角小店日记', '擅长把小店日常拍得有人情味。'],
      ['@城市午餐研究所', '午餐场景切得细，容易引流到店。'],
    ],
    selling: '稳定家常味 + 店主真实感 + 离附近人生活很近。',
  };
  const reportSets = [
    {
      names: ['巷口暖胃小馆', '附近人的家常饭', '下班来吃一口'],
      keywords: ['亲切但不油腻', '懂本地生活', '真实主理人', '稳定好吃'],
      phrases: ['今天这碗饭，适合下班后来一口。', '第一次来不知道点什么，先看这一篇。', '不是网红店，但想把每顿饭认真做好。'],
      bio: '每天认真做一碗有烟火气的家常饭，给附近人一个不用纠结的吃饭选择。',
      pillars: ['招牌菜故事', '午餐不踩雷', '老板的一天', '真实顾客反馈', '周末朋友局菜单'],
      bloggers: ['@本地吃喝指南', '@街角小店日记', '@城市午餐研究所'],
      covers: ['暖色自然光 + 菜品近景 + 大留白标题', '店门口/餐桌/后厨细节三图拼贴', '人物手部入镜，弱化摆拍感'],
    },
    {
      names: ['今天吃暖胃饭', '社区饭点研究所', '小馆认真饭'],
      keywords: ['靠谱推荐', '邻里感', '价格友好', '下班治愈'],
      phrases: ['这不是探店广告，是附近人真的会复吃的菜单。', '如果你只有 30 分钟吃午饭，可以这么点。', '小店最动人的地方，是每天都稳定。'],
      bio: '记录一家社区小馆的日常菜单、真实客人和让人安心的家常味。',
      pillars: ['30 分钟午餐方案', '复吃菜单', '小店幕后', '本周新品', '附近生活路线'],
      bloggers: ['@通勤午餐地图', '@小店观察员', '@附近生活手册'],
      covers: ['浅色桌面 + 俯拍套餐 + 手写感标题', '老板出镜 + 菜品特写 + 真实环境', '低饱和暖色，强调干净和可信'],
    },
  ];
  const report = reportSets[reportVariant % reportSets.length];

  const setCalendarItem = (index, patch) => {
    setCalendar(items => items.map((item, i) => i === index ? { ...item, ...patch } : item));
  };
  const firstTopic = calendar[0]?.topic || '第一次来店里，先点这 3 道招牌菜';
  const complete = () => onComplete({
    topic: `小红书图文：${firstTopic}`,
    platform: platform || '小红书',
    positioning: diagnosis.position,
    persona,
    pillars,
  });

  const memory = (
    <section style={{
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.82)',
      borderRadius: 22,
      padding: 16,
      boxShadow: '0 16px 38px rgba(14,14,44,.052), inset 0 1px 0 rgba(255,255,255,.86)',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 }}>
        <h3 style={{ margin: 0, fontSize: 14.5, fontWeight: 760, color: T.navy }}>IP Memory</h3>
        <span style={{ fontSize: 10.5, color: T.navyLight, fontFamily: T.fontMono }}>{Math.min(5, [sentIntro, goal, platform, method, step >= 2].filter(Boolean).length)}/5</span>
      </div>
      <div style={{ display: 'grid', gap: 9 }}>
        {[
          ['赛道', '本地生活 / 小餐饮', sentIntro],
          ['目标', goal || '待选择', !!goal],
          ['平台', platform || '待选择', !!platform],
          ['产品', methods.length ? '家常菜、午餐、附近到店' : '待识别', methods.length > 0],
          ['定位', step >= 2 ? diagnosis.position : '待诊断', step >= 2],
        ].map(([k, v, done]) => (
          <div key={k} style={{
            padding: '10px 10px',
            borderRadius: 13,
            background: done ? 'rgba(224,250,244,.62)' : 'rgba(246,248,251,.72)',
            border: `1px solid ${done ? 'rgba(49,208,170,.20)' : T.hairlineSoft}`,
            animation: done ? `memoryReady .48s ${T.spring} both` : 'none',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8, marginBottom: 4 }}>
              <span style={{ color: done ? T.success : T.navyLight, fontSize: 11.5, fontWeight: 720 }}>{k}</span>
              <span style={{ width: 18, height: 18, borderRadius: '50%', background: done ? T.success : 'rgba(14,14,44,.06)', color: T.white, display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
                {done && <Icon name="check" size={10} stroke={2.4} />}
              </span>
            </div>
            <div style={{ color: done ? T.navy : T.navyLight, fontSize: 12.2, fontWeight: done ? 650 : 520, lineHeight: 1.45 }}>{v}</div>
          </div>
        ))}
      </div>
    </section>
  );
  const copyText = (text) => {
    setCopied(text);
    navigator.clipboard?.writeText(text).catch(() => {});
    window.setTimeout(() => setCopied(''), 1100);
  };

  return (
    <div style={{ display: 'flex', height: '100%', width: '100%', background: 'linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)', overflow: 'hidden' }}>
      {!isTablet && (
        <Sidebar
          active="home"
          onNew={onNewChat}
          onNavigate={(id) => {
            if (id === 'home') onBackHome();
            if (id === 'library') onOpenAssets && onOpenAssets();
            if (id === 'skills') onOpenSkills && onOpenSkills();
            if (id === 'insights') onOpenInsights && onOpenInsights();
          }}
          sessions={['账号规划 · 当前', '上海咖啡馆 City Walk Top 10', '产品测评 · AI 视频工具横评']}
          collapsed={navCollapsed}
          onToggle={() => setNavCollapsed(v => !v)}
        />
      )}
      <main style={{ flex: 1, overflow: 'auto', position: 'relative', background: 'linear-gradient(180deg, #FFFFFF 0%, #FBFCFE 54%, #F7F9FC 100%)' }}>
        <div style={{
          position: 'sticky',
          top: 0,
          zIndex: 8,
          height: isMobile ? 'auto' : 58,
          padding: isMobile ? '12px 16px' : '0 24px',
          display: 'flex',
          alignItems: isMobile ? 'stretch' : 'center',
          justifyContent: 'space-between',
          gap: 14,
          borderBottom: `1px solid ${T.hairlineSoft}`,
          background: 'rgba(250,252,254,.78)',
          backdropFilter: 'blur(18px) saturate(1.16)',
          flexDirection: isMobile ? 'column' : 'row',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0 }}>
            <button onClick={onBackHome} style={iconBtnStyle()}><Icon name="home" size={15} color={T.navyMid} /></button>
            <div>
              <div style={{ fontSize: 13.5, fontWeight: 720, color: T.navy }}>账号规划</div>
              <div style={{ fontSize: 11, color: T.navyLight }}>用最少的信息，建立可执行的账号系统</div>
            </div>
          </div>
          {isMobile ? nav : <div style={{ width: isCompact ? 520 : 610 }}>{nav}</div>}
        </div>

        <div style={{
          maxWidth: isMobile ? '100%' : 1180,
          margin: '0 auto',
          padding: isMobile ? '22px 18px 42px' : '34px 42px 58px',
          display: 'grid',
          gridTemplateColumns: isMobile ? '1fr' : isCompact ? 'minmax(0, 1fr) 260px' : '170px minmax(0, 1fr) 292px',
          gap: isMobile ? 18 : 22,
          alignItems: 'start',
        }}>
          {!isMobile && <div style={{ position: 'sticky', top: 88 }}>{nav}</div>}
          <div style={{ display: 'grid', gap: 18 }}>
            {isMobile && memory}
            {step === 1 && (
              <>
                <NoriSays>
                  <p style={{ marginBottom: 8, fontSize: 15, fontWeight: 680 }}>先给我一点线索就行。</p>
                  <p style={{ color: T.navyMid, fontSize: 13 }}>可以贴链接、传截图，或者直接说你是做什么的。我会把后面的问题压到 3 轮以内。</p>
                </NoriSays>
                <PlanningPanel title="选择输入方式">
                  <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(3, minmax(0, 1fr))', gap: 10 }}>
                    <PlanningOption icon="link" title="粘贴链接" desc="店铺 / 账号 / 文章" active={method === 'link'} onClick={() => { setMethod('link'); setRawInput('https://example.com/meituan/shop/暖胃小馆'); }} />
                    <PlanningOption icon="image" title="上传图片" desc="产品图 / 截图" active={method === 'image'} onClick={() => { setMethod('image'); setRawInput('已模拟上传：店铺菜单截图.png'); }} />
                    <PlanningOption icon="chat" title="直接描述" desc="我是做什么的" active={method === 'text'} onClick={() => { setMethod('text'); setRawInput('我在社区附近开了一家家常小馆，想做小红书引流到店。'); }} />
                  </div>
                  <textarea
                    value={rawInput}
                    onChange={e => setRawInput(e.target.value)}
                    placeholder="把链接、截图说明或一句描述放在这里"
                    rows={3}
                    style={{
                      marginTop: 12,
                      width: '100%',
                      border: `1px solid ${T.hairlineSoft}`,
                      borderRadius: 15,
                      background: 'rgba(250,252,254,.72)',
                      padding: '12px 13px',
                      resize: 'vertical',
                      outline: 'none',
                      color: T.navy,
                      fontSize: 13,
                      lineHeight: 1.55,
                      fontFamily: T.fontSans,
                    }}
                  />
                </PlanningPanel>
                {method && (
                  <NoriSays>
                    <p style={{ marginBottom: 12 }}>收到！我看到你是做本地小餐饮的，主打家常菜和附近到店。你想通过社媒主要做什么？</p>
                    <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                      {['引流到店', '品牌曝光', '线上卖货'].map(v => <PlanningChoice key={v} active={goal === v} onClick={() => setGoal(v)}>{v}</PlanningChoice>)}
                    </div>
                  </NoriSays>
                )}
                {goal && (
                  <NoriSays>
                    <p style={{ marginBottom: 12 }}>明白。你希望先在哪个平台做？</p>
                    <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                      {['小红书', '抖音', '都想试试'].map(v => <PlanningChoice key={v} active={platform === v} onClick={() => setPlatform(v)}>{v}</PlanningChoice>)}
                    </div>
                  </NoriSays>
                )}
                <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <button onClick={() => setStep(2)} disabled={!canAdvanceStep1} style={{
                    height: 40,
                    padding: '0 18px',
                    borderRadius: 13,
                    border: 'none',
                    background: canAdvanceStep1 ? T.navy : T.surface,
                    color: canAdvanceStep1 ? T.white : T.navyLight,
                    cursor: canAdvanceStep1 ? 'pointer' : 'not-allowed',
                    fontSize: 13,
                    fontWeight: 700,
                    boxShadow: canAdvanceStep1 ? '0 12px 24px rgba(14,14,44,.14)' : 'none',
                  }}>进入账号诊断</button>
                </div>
              </>
            )}

            {step === 2 && (
              <>
                <NoriSays>
                  <p style={{ marginBottom: 4, fontSize: 15, fontWeight: 680 }}>我先把账号定位拆出来。</p>
                  <p style={{ color: T.navyMid, fontSize: 13 }}>下面每一项都可以确认或调整；现在先用最容易执行的版本。</p>
                </NoriSays>
                <PlanningPanel title="推荐账号定位">
                  <h2 style={{ margin: 0, fontSize: isMobile ? 20 : 23, lineHeight: 1.22, color: T.navy, fontWeight: 760 }}>{diagnosis.position}</h2>
                  <p style={{ margin: '10px 0 0', color: T.navyMid, fontSize: 13, lineHeight: 1.65 }}>{diagnosis.reason}</p>
                </PlanningPanel>
                {[
                  ['目标受众画像', diagnosis.audience],
                  ['差异化卖点', diagnosis.selling],
                ].map(([title, body]) => (
                  <PlanningPanel key={title} title={title} action={<PlanningChoice active={confirmed[title]} onClick={() => setConfirmed(c => ({ ...c, [title]: !c[title] }))}>{confirmed[title] ? '已确认' : '确认'}</PlanningChoice>}>
                    <p style={{ margin: 0, color: T.navyMid, fontSize: 13, lineHeight: 1.65 }}>{body}</p>
                  </PlanningPanel>
                ))}
                <PlanningPanel title="内容方向建议">
                  <div style={{ display: 'grid', gap: 10 }}>
                    {diagnosis.directions.map(([title, body]) => (
                      <div key={title} style={{ padding: 13, borderRadius: 14, background: 'rgba(250,252,254,.72)', border: `1px solid ${T.hairlineSoft}` }}>
                        <div style={{ fontSize: 13.5, fontWeight: 720, color: T.navy }}>{title}</div>
                        <div style={{ marginTop: 4, fontSize: 12.5, color: T.navyMid, lineHeight: 1.55 }}>{body}</div>
                      </div>
                    ))}
                  </div>
                </PlanningPanel>
                <PlanningPanel title="对标账号推荐">
                  <div style={{ display: 'grid', gap: 9 }}>
                    {diagnosis.benchmarks.map(([name, body]) => (
                      <div key={name} style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                        <span style={{ width: 34, height: 34, borderRadius: '50%', background: T.irisTint, color: T.iris, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontSize: 12, fontWeight: 800 }}>{name.slice(1, 2)}</span>
                        <span style={{ minWidth: 0 }}>
                          <span style={{ display: 'block', fontSize: 13, fontWeight: 700, color: T.navy }}>{name}</span>
                          <span style={{ display: 'block', fontSize: 12, color: T.navyLight }}>{body}</span>
                        </span>
                      </div>
                    ))}
                  </div>
                </PlanningPanel>
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
                  <button onClick={() => setStep(4)} style={{ border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', fontSize: 12.5, fontWeight: 600 }}>跳过，直接生成</button>
                  <button onClick={() => setStep(3)} style={{ height: 40, padding: '0 18px', borderRadius: 13, border: 'none', background: T.navy, color: T.white, cursor: 'pointer', fontSize: 13, fontWeight: 700, boxShadow: '0 12px 24px rgba(14,14,44,.14)' }}>看起来不错，继续</button>
                </div>
              </>
            )}

            {step === 3 && (
              <>
                <NoriSays>
                  <p style={{ marginBottom: 4, fontSize: 15, fontWeight: 680 }}>定位可以落成一个可执行的 IP 系统。</p>
                  <p style={{ color: T.navyMid, fontSize: 13 }}>这些内容都可以改，确认后会用于后续内容生成。</p>
                </NoriSays>
                <PlanningPanel title="人设卡片">
                  <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : '1fr 1fr', gap: 12 }}>
                    <EditableMiniField label="账号名建议" value={persona.name} onChange={v => setPersona(p => ({ ...p, name: v }))} />
                    <EditableMiniField label="人设关键词" value={persona.keywords} onChange={v => setPersona(p => ({ ...p, keywords: v }))} />
                    <div style={{ gridColumn: isMobile ? 'auto' : 'span 2' }}>
                      <EditableMiniField label="签名建议" value={persona.bio} onChange={v => setPersona(p => ({ ...p, bio: v }))} />
                    </div>
                  </div>
                </PlanningPanel>
                <PlanningPanel title="内容风格">
                  <div style={{ display: 'grid', gap: 12 }}>
                    <EditableMiniField label="语气调性 / 常用句式" multiline value={persona.tone} onChange={v => setPersona(p => ({ ...p, tone: v }))} />
                    <EditableMiniField label="封面风格方向" multiline value={persona.cover} onChange={v => setPersona(p => ({ ...p, cover: v }))} />
                  </div>
                </PlanningPanel>
                <PlanningPanel title="内容支柱">
                  <div style={{ display: 'grid', gap: 8 }}>
                    {pillars.map((pillar, index) => (
                      <div key={index} style={{ display: 'flex', gap: 8 }}>
                        <input value={pillar} onChange={e => setPillars(list => list.map((p, i) => i === index ? e.target.value : p))} style={{ flex: 1, height: 36, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: 'rgba(255,255,255,.72)', padding: '0 11px', outline: 'none', color: T.navy, fontSize: 13 }} />
                        <button onClick={() => setPillars(list => list.filter((_, i) => i !== index))} style={iconBtnStyle()}><Icon name="close" size={12} /></button>
                      </div>
                    ))}
                    <button onClick={() => setPillars(list => [...list, '新的固定选题方向'])} style={{ height: 34, borderRadius: 12, border: `1px dashed ${T.hairline}`, background: 'rgba(255,255,255,.58)', color: T.navyMid, cursor: 'pointer', fontSize: 12.5, fontWeight: 620 }}>新增内容支柱</button>
                  </div>
                </PlanningPanel>
                <PlanningPanel title="我的 IP 系统预览">
                  <div style={{ padding: 18, borderRadius: 18, background: 'linear-gradient(135deg, rgba(239,239,253,.76), rgba(224,250,244,.66))', border: '1px solid rgba(255,255,255,.72)' }}>
                    <div style={{ fontSize: 20, fontWeight: 780, color: T.navy }}>{persona.name}</div>
                    <div style={{ marginTop: 6, color: T.navyMid, fontSize: 13 }}>{persona.bio}</div>
                    <div style={{ marginTop: 12, display: 'flex', gap: 7, flexWrap: 'wrap' }}>{persona.keywords.split(/[、,，]/).filter(Boolean).map(k => <span key={k} style={{ padding: '5px 9px', borderRadius: 999, background: 'rgba(255,255,255,.66)', color: T.navyMid, fontSize: 11.5, fontWeight: 650 }}>{k}</span>)}</div>
                  </div>
                </PlanningPanel>
                <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <button onClick={() => setStep(4)} style={{ height: 40, padding: '0 18px', borderRadius: 13, border: 'none', background: T.navy, color: T.white, cursor: 'pointer', fontSize: 13, fontWeight: 700, boxShadow: '0 12px 24px rgba(14,14,44,.14)' }}>确认画像</button>
                </div>
              </>
            )}

            {step === 4 && (
              <>
                <NoriSays>
                  <p style={{ marginBottom: 4, fontSize: 15, fontWeight: 680 }}>我先排出未来一周的内容建议。</p>
                  <p style={{ color: T.navyMid, fontSize: 13 }}>V1 先不发布，只把计划和第一篇制作入口准备好。</p>
                </NoriSays>
                <PlanningPanel title="一周内容规划">
                  <div style={{ display: 'grid', gap: 10 }}>
                    {calendar.map((item, index) => (
                      <div key={`${item.day}-${index}`} style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : '64px 86px minmax(0, 1fr) 34px', gap: 8, alignItems: 'center', padding: 10, borderRadius: 14, background: index === 0 ? 'rgba(239,239,253,.58)' : 'rgba(250,252,254,.72)', border: `1px solid ${index === 0 ? 'rgba(75,77,237,.14)' : T.hairlineSoft}` }}>
                        <input value={item.day} onChange={e => setCalendarItem(index, { day: e.target.value })} style={{ border: 'none', background: 'transparent', color: T.navy, fontSize: 12.5, fontWeight: 720, outline: 'none' }} />
                        <input value={item.type} onChange={e => setCalendarItem(index, { type: e.target.value })} style={{ border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.62)', borderRadius: 10, height: 32, padding: '0 9px', color: T.navyMid, fontSize: 12, outline: 'none' }} />
                        <input value={item.topic} onChange={e => setCalendarItem(index, { topic: e.target.value })} style={{ border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.62)', borderRadius: 10, height: 32, padding: '0 9px', color: T.navy, fontSize: 12.5, outline: 'none' }} />
                        <button onClick={() => setCalendar(list => list.filter((_, i) => i !== index))} style={{ ...iconBtnStyle(), width: 32, height: 32 }}><Icon name="close" size={11} /></button>
                        <div style={{ gridColumn: isMobile ? 'auto' : '3 / 4', color: T.navyLight, fontSize: 11.5 }}>参考：{item.ref}</div>
                      </div>
                    ))}
                    <button onClick={() => setCalendar(list => [...list, { day: '新增', type: '图文', topic: '新的内容选题', ref: '@参考账号' }])} style={{ height: 36, borderRadius: 13, border: `1px dashed ${T.hairline}`, background: 'rgba(255,255,255,.58)', color: T.navyMid, cursor: 'pointer', fontSize: 12.5, fontWeight: 650 }}>新增一天</button>
                  </div>
                </PlanningPanel>
                <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <button onClick={complete} style={{ height: 42, padding: '0 20px', borderRadius: 14, border: 'none', background: T.navy, color: T.white, cursor: 'pointer', fontSize: 13.2, fontWeight: 740, boxShadow: '0 14px 28px rgba(14,14,44,.16)' }}>开始制作第一篇</button>
                </div>
              </>
            )}
          </div>
          {!isMobile && <div style={{ position: 'sticky', top: 88 }}>{memory}</div>}
        </div>
      </main>
    </div>
  );
};

window.AccountPlanningPage = AccountPlanningPage;

const AccountPlanningPagePolished = ({ onBackHome, onNewChat, onOpenAssets, onOpenSkills, onOpenInsights, onComplete }) => {
  const { isCompact, isTablet, isMobile } = useViewport();
  const [navCollapsed, setNavCollapsed] = React.useState(false);
  const [step, setStep] = React.useState(1);
  const [modalType, setModalType] = React.useState(null);
  const [method, setMethod] = React.useState(null);
  const [methods, setMethods] = React.useState([]);
  const [attachment, setAttachment] = React.useState(null);
  const [attachments, setAttachments] = React.useState([]);
  const [rawInput, setRawInput] = React.useState('');
  const [sentIntro, setSentIntro] = React.useState(false);
  const [goal, setGoal] = React.useState(null);
  const [platform, setPlatform] = React.useState(null);
  const [confirmed, setConfirmed] = React.useState({});
  const [copied, setCopied] = React.useState('');
  const [reportVariant, setReportVariant] = React.useState(0);
  const [reportBurst, setReportBurst] = React.useState(false);
  const [weekStart, setWeekStart] = React.useState('2026-05-18');
  const [showWeekPicker, setShowWeekPicker] = React.useState(false);
  const [diagnosisText, setDiagnosisText] = React.useState({
    position: '做附近人愿意收藏的烟火气小馆账号。你的优势不是大品牌感，而是稳定、真实、离用户很近。内容要让人觉得下班就能去。',
    audience: '23-38 岁附近上班族、情侣和周末约饭人群，关心味道稳定、价格舒服、距离方便。',
    directions: '招牌菜故事：让用户记住你和别的店不一样的地方。\n真实到店场景：降低第一次到店的心理成本。\n本地生活攻略：把餐厅内容变成可收藏的信息。',
    benchmarks: '@本地吃喝指南：标题清楚，适合学习选题包装。\n@街角小店日记：擅长把小店日常拍得有人情味。\n@城市午餐研究所：午餐场景切得细，容易引流到店。',
    selling: '稳定家常味 + 店主真实感 + 离附近人生活很近。',
  });
  const [calendar, setCalendar] = React.useState([
    { day: '周一', type: '探店图文', topic: '第一次来店里，先点这 3 道招牌菜', ref: '@本地吃喝指南' },
    { day: '周二', type: '短视频', topic: '后厨备菜 30 秒，看看一碗饭怎么被认真做好', ref: '@街角小店日记' },
    { day: '周三', type: '图文', topic: '附近上班族午餐不踩雷菜单', ref: '@城市午餐研究所' },
    { day: '周四', type: '长文', topic: '一家小店怎么把回头客留住', ref: '@主理人手记' },
    { day: '周五', type: '短视频', topic: '顾客最常问的 5 个问题', ref: '@真实探店' },
    { day: '周六', type: '图文', topic: '周末带朋友来吃，怎么点更划算', ref: '@本地生活家' },
    { day: '周日', type: '复盘', topic: '这周最受欢迎的一道菜', ref: '@小店经营笔记' },
  ]);
  const [reportDraft, setReportDraft] = React.useState(null);
  const steps = [
    { id: 1, label: '入口信息' },
    { id: 2, label: '账号诊断' },
    { id: 3, label: 'IP 画像' },
    { id: 4, label: '内容日历' },
    { id: 5, label: '开始制作' },
  ];
  const defaultDiagnosis = {
    position: '做附近人愿意收藏的烟火气小馆账号。你的优势不是大品牌感，而是稳定、真实、离用户很近。内容要让人觉得下班就能去。',
    audience: '23-38 岁附近上班族、情侣和周末约饭人群，关心味道稳定、价格舒服、距离方便。',
    directions: '招牌菜故事：让用户记住你和别的店不一样的地方。\n真实到店场景：降低第一次到店的心理成本。\n本地生活攻略：把餐厅内容变成可收藏的信息。',
    benchmarks: '@本地吃喝指南：标题清楚，适合学习选题包装。\n@街角小店日记：擅长把小店日常拍得有人情味。\n@城市午餐研究所：午餐场景切得细，容易引流到店。',
    selling: '稳定家常味 + 店主真实感 + 离附近人生活很近。',
  };
  const reports = [
    {
      names: ['巷口暖胃小馆', '附近人的家常饭', '下班来吃一口'],
      keywords: ['亲切但不油腻', '懂本地生活', '真实主理人', '稳定好吃'],
      phrases: ['今天这碗饭，适合下班后来一口。', '第一次来不知道点什么，先看这一篇。', '不是网红店，但想把每顿饭认真做好。'],
      bio: '每天认真做一碗有烟火气的家常饭，给附近人一个不用纠结的吃饭选择。',
      pillars: ['招牌菜故事', '午餐不踩雷', '老板的一天', '真实顾客反馈', '周末朋友局菜单'],
      bloggers: ['@本地吃喝指南', '@街角小店日记', '@城市午餐研究所'],
      covers: ['暖色自然光 + 菜品近景 + 大留白标题', '店门口/餐桌/后厨细节三图拼贴', '人物手部入镜，弱化摆拍感'],
    },
    {
      names: ['今天吃暖胃饭', '社区饭点研究所', '小馆认真饭'],
      keywords: ['靠谱推荐', '邻里感', '价格友好', '下班治愈'],
      phrases: ['这不是探店广告，是附近人真的会复吃的菜单。', '如果你只有 30 分钟吃午饭，可以这么点。', '小店最动人的地方，是每天都稳定。'],
      bio: '记录一家社区小馆的日常菜单、真实客人和让人安心的家常味。',
      pillars: ['30 分钟午餐方案', '复吃菜单', '小店幕后', '本周新品', '附近生活路线'],
      bloggers: ['@通勤午餐地图', '@小店观察员', '@附近生活手册'],
      covers: ['浅色桌面 + 俯拍套餐 + 手写感标题', '老板出镜 + 菜品特写 + 真实环境', '低饱和暖色，强调干净和可信'],
    },
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
      covers: [...next.covers],
    });
  }, [reportVariant]);
  const activeReport = reportDraft || report;

  React.useEffect(() => {
    if (step !== 3) return undefined;
    setReportBurst(false);
    const raf = window.requestAnimationFrame(() => setReportBurst(true));
    const timer = window.setTimeout(() => setReportBurst(false), 1500);
    return () => {
      window.cancelAnimationFrame(raf);
      window.clearTimeout(timer);
    };
  }, [step, reportVariant]);

  const canAdvanceStep1 = sentIntro && goal && platform;
  const firstTopic = calendar[0]?.topic || '第一次来店里，先点这 3 道招牌菜';
  const copyText = (text) => {
    setCopied(text);
    navigator.clipboard?.writeText(text).catch(() => {});
    window.setTimeout(() => setCopied(''), 1100);
  };
  const confirmAttachment = (att) => {
    setAttachment(att);
    setAttachments(list => [...list, att]);
    setMethod(att.type);
    setMethods(list => list.includes(att.type) ? list : [...list, att.type]);
    setModalType(null);
  };
  const sendIntro = () => {
    if (!attachments.length && !rawInput.trim()) return;
    setSentIntro(true);
  };
  const complete = () => onComplete({
    topic: `小红书图文：${firstTopic}`,
    platform: platform || '小红书',
    positioning: '做附近人愿意收藏的烟火气小馆账号',
    persona: {
      name: activeReport.names[0],
      bio: activeReport.bio,
      keywords: activeReport.keywords.join('、'),
      tone: activeReport.phrases.join(' / '),
      cover: activeReport.covers[0],
    },
    pillars: activeReport.pillars,
  });
  const memory = (
    <section style={{
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(255,255,255,.84)',
      borderRadius: 22,
      padding: 16,
      boxShadow: '0 16px 38px rgba(14,14,44,.052), inset 0 1px 0 rgba(255,255,255,.86)',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 14 }}>
        <h3 style={{ margin: 0, fontSize: 14.5, fontWeight: 760, color: T.navy }}>IP Memory</h3>
        <span style={{ fontSize: 10.5, color: T.navyLight, fontFamily: T.fontMono }}>{Math.min(5, [sentIntro, goal, platform, method, step >= 2].filter(Boolean).length)}/5</span>
      </div>
      <div style={{ display: 'grid', gap: 9 }}>
        {[
          ['赛道', '本地生活 / 小餐饮', sentIntro],
          ['目标', goal || '待选择', !!goal],
          ['平台', platform || '待选择', !!platform],
          ['产品', method ? '家常菜、午餐、附近到店' : '待识别', !!method],
          ['定位', step >= 2 ? '烟火气小馆账号' : '待诊断', step >= 2],
        ].map(([k, v, done]) => (
          <div key={k} style={{ padding: '10px 10px', borderRadius: 13, background: done ? 'rgba(224,250,244,.62)' : 'rgba(246,248,251,.72)', border: `1px solid ${done ? 'rgba(49,208,170,.20)' : T.hairlineSoft}`, animation: done ? `memoryReady .48s ${T.spring} both` : 'none' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 8, marginBottom: 4 }}>
              <span style={{ color: done ? T.success : T.navyLight, fontSize: 11.5, fontWeight: 720 }}>{k}</span>
              <span style={{ width: 18, height: 18, borderRadius: '50%', background: done ? T.success : 'rgba(14,14,44,.06)', color: T.white, display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>{done && <Icon name="check" size={10} stroke={2.4} />}</span>
            </div>
            <div style={{ color: done ? T.navy : T.navyLight, fontSize: 12.2, fontWeight: done ? 650 : 520, lineHeight: 1.45 }}>{v}</div>
          </div>
        ))}
      </div>
    </section>
  );

  return (
    <div style={{ display: 'flex', height: '100%', width: '100%', background: 'linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)', overflow: 'hidden' }}>
      {!isTablet && (
        <Sidebar
          active="home"
          onNew={onNewChat}
          onNavigate={(id) => {
            if (id === 'home') onBackHome();
            if (id === 'library') onOpenAssets && onOpenAssets();
            if (id === 'skills') onOpenSkills && onOpenSkills();
            if (id === 'insights') onOpenInsights && onOpenInsights();
          }}
          sessions={['账号规划 · 当前', '上海咖啡馆 City Walk Top 10', '产品测评 · AI 视频工具横评']}
          collapsed={navCollapsed}
          onToggle={() => setNavCollapsed(v => !v)}
        />
      )}
      <main style={{ flex: 1, overflow: 'auto', position: 'relative', background: 'linear-gradient(180deg, #FFFFFF 0%, #FBFCFE 54%, #F7F9FC 100%)' }}>
        <div style={{ position: 'sticky', top: 0, zIndex: 8, minHeight: isMobile ? 'auto' : 66, padding: isMobile ? '12px 16px' : '0 24px', display: 'flex', alignItems: isMobile ? 'stretch' : 'center', justifyContent: 'space-between', gap: 14, borderBottom: `1px solid ${T.hairlineSoft}`, background: 'rgba(250,252,254,.84)', backdropFilter: 'blur(18px) saturate(1.16)', flexDirection: isMobile ? 'column' : 'row' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0 }}>
            <button onClick={onBackHome} style={iconBtnStyle()}><Icon name="home" size={15} color={T.navyMid} /></button>
            <div>
              <div style={{ fontSize: 13.5, fontWeight: 720, color: T.navy }}>账号规划</div>
              <div style={{ fontSize: 11, color: T.navyLight }}>用最少的信息，建立可执行的账号系统</div>
            </div>
          </div>
          <PlanningStepper steps={steps} step={step} isMobile={isMobile} />
        </div>

        <div style={{ maxWidth: isMobile ? '100%' : 1160, margin: '0 auto', padding: isMobile ? '22px 18px 42px' : '34px 42px 58px', display: 'grid', gridTemplateColumns: isMobile ? '1fr' : isCompact ? 'minmax(0, 1fr) 260px' : 'minmax(0, 1fr) 292px', gap: isMobile ? 18 : 24, alignItems: 'start' }}>
          <div style={{ display: 'grid', gap: 18, minWidth: 0 }}>
            {isMobile && memory}
            {step === 1 && (
              <>
                <NoriSays>
                  <p style={{ marginBottom: 8, fontSize: 15, fontWeight: 680 }}>先给我一点线索就行。</p>
                  <p style={{ color: T.navyMid, fontSize: 13 }}>可以贴链接、传截图，或者直接说你是做什么的。我会把后面的问题压到 3 轮以内。</p>
                </NoriSays>
                <PlanningPanel title="选择输入方式">
                  <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(3, minmax(0, 1fr))', gap: 10, marginBottom: 12 }}>
                    <PlanningOption icon="link" title="粘贴链接" desc="店铺 / 账号 / 文章" active={methods.includes('link')} onClick={() => setModalType('link')} />
                    <PlanningOption icon="image" title="上传图片" desc="产品图 / 截图" active={methods.includes('image')} onClick={() => setModalType('image')} />
                    <PlanningOption icon="chat" title="直接描述" desc="我是做什么的" active={methods.includes('text')} onClick={() => setModalType('text')} />
                  </div>
                  <PlanningComposerMulti
                    attachments={attachments}
                    text={rawInput}
                    setText={setRawInput}
                    onRemoveAttachment={(index) => {
                      setAttachments(list => {
                        const next = list.filter((_, i) => i !== index);
                        setMethods([...new Set(next.map(item => item.type))]);
                        setMethod(next[next.length - 1]?.type || null);
                        setAttachment(next[next.length - 1] || null);
                        return next;
                      });
                    }}
                    onSend={sendIntro}
                  />
                </PlanningPanel>
                {sentIntro && (
                  <NoriSays>
                    <p style={{ marginBottom: 12 }}>收到！我看到你是做本地小餐饮的，主打家常菜和附近到店。你想通过社媒主要做什么？</p>
                    <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                      {['引流到店', '品牌曝光', '线上卖货'].map(v => <PlanningChoice key={v} active={goal === v} onClick={() => setGoal(v)}>{v}</PlanningChoice>)}
                    </div>
                  </NoriSays>
                )}
                {goal && (
                  <NoriSays>
                    <p style={{ marginBottom: 12 }}>明白。你希望先在哪个平台做？</p>
                    <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                      {['小红书', '抖音', '都想试试'].map(v => <PlanningChoice key={v} active={platform === v} onClick={() => setPlatform(v)}>{v}</PlanningChoice>)}
                    </div>
                  </NoriSays>
                )}
                <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <button onClick={() => setStep(2)} disabled={!canAdvanceStep1} style={{ height: 40, padding: '0 18px', borderRadius: 13, border: 'none', background: canAdvanceStep1 ? T.navy : T.surface, color: canAdvanceStep1 ? T.white : T.navyLight, cursor: canAdvanceStep1 ? 'pointer' : 'not-allowed', fontSize: 13, fontWeight: 700, boxShadow: canAdvanceStep1 ? '0 12px 24px rgba(14,14,44,.14)' : 'none' }}>进入账号诊断</button>
                </div>
              </>
            )}

            {step === 2 && (
              <>
                <NoriSays>
                  <p style={{ marginBottom: 4, fontSize: 15, fontWeight: 680 }}>我先把账号定位拆出来。</p>
                  <p style={{ color: T.navyMid, fontSize: 13 }}>每个板块都可以直接编辑，改完会自动保留在这份账号规划里。</p>
                </NoriSays>
                <InlineEditableCard title="推荐账号定位" rows={4} value={diagnosisText.position} onChange={v => setDiagnosisText(d => ({ ...d, position: v }))} />
                <InlineEditableCard title="目标受众画像" rows={3} value={diagnosisText.audience} onChange={v => setDiagnosisText(d => ({ ...d, audience: v }))} />
                <InlineEditableCard title="内容方向建议" rows={5} value={diagnosisText.directions} onChange={v => setDiagnosisText(d => ({ ...d, directions: v }))} />
                <InlineEditableCard title="对标账号推荐" rows={5} value={diagnosisText.benchmarks} onChange={v => setDiagnosisText(d => ({ ...d, benchmarks: v }))} />
                <InlineEditableCard title="差异化卖点" rows={3} value={diagnosisText.selling} onChange={v => setDiagnosisText(d => ({ ...d, selling: v }))} />
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, flexWrap: 'wrap' }}>
                  <button onClick={() => setStep(4)} style={{ border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', fontSize: 12.5, fontWeight: 600 }}>跳过，直接生成</button>
                  <button onClick={() => setStep(3)} style={{ height: 40, padding: '0 18px', borderRadius: 13, border: 'none', background: T.navy, color: T.white, cursor: 'pointer', fontSize: 13, fontWeight: 700, boxShadow: '0 12px 24px rgba(14,14,44,.14)' }}>看起来不错，继续</button>
                </div>
              </>
            )}

            {step === 3 && (
              <>
                <NoriSays>
                  <p style={{ marginBottom: 4, fontSize: 15, fontWeight: 680 }}>我把定位整理成一份可执行的 IP 画像报告。</p>
                  <p style={{ color: T.navyMid, fontSize: 13 }}>后面做内容时，这些会成为 Nori 默认记住的账号规则。</p>
                </NoriSays>
                <section style={{ position: 'relative', borderRadius: 24, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.88)', boxShadow: '0 18px 42px rgba(14,14,44,.055), inset 0 1px 0 rgba(255,255,255,.88)', padding: isMobile ? 18 : 22, overflow: 'hidden' }}>
                  <MiniOnionBurst active={reportBurst} />
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 14, marginBottom: 18 }}>
                    <div>
                      <div style={{ fontSize: 11.5, color: T.navyLight, fontWeight: 720, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 6 }}>IP System Report</div>
                      <h2 style={{ margin: 0, color: T.navy, fontSize: isMobile ? 22 : 28, lineHeight: 1.16, fontWeight: 780 }}>我的 IP 系统</h2>
                    </div>
                    <span style={{ height: 30, padding: '0 10px', borderRadius: 999, background: T.successTint, color: T.success, fontSize: 11.5, fontWeight: 720, display: 'inline-flex', alignItems: 'center', gap: 5 }}><Icon name="check" size={12} /> 已生成</span>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : '1fr 1fr', gap: 14 }}>
                    <EditableListPanel title="账号名建议" items={activeReport.names} onChange={items => setReportDraft(r => ({ ...activeReport, ...r, names: items }))} />
                    <EditableListPanel title="人设关键词" items={activeReport.keywords} onChange={items => setReportDraft(r => ({ ...activeReport, ...r, keywords: items }))} />
                    <EditableListPanel title="常用句式" items={activeReport.phrases} onChange={items => setReportDraft(r => ({ ...activeReport, ...r, phrases: items }))} muted />
                    <EditableListPanel title="账号主要内容支柱" items={activeReport.pillars} onChange={items => setReportDraft(r => ({ ...activeReport, ...r, pillars: items }))} />
                    <EditableListPanel title="对标博主" items={activeReport.bloggers} onChange={items => setReportDraft(r => ({ ...activeReport, ...r, bloggers: items }))} />
                    <EditableListPanel title="推荐封面图片" items={activeReport.covers} onChange={items => setReportDraft(r => ({ ...activeReport, ...r, covers: items }))} muted />
                    <div style={{ gridColumn: isMobile ? 'auto' : 'span 2' }}>
                      <PlanningPanel title="签名">
                        <textarea
                          value={activeReport.bio}
                          onChange={e => setReportDraft(r => ({ ...activeReport, ...r, bio: e.target.value }))}
                          rows={3}
                          style={{
                            width: '100%',
                            border: `1px solid ${T.hairlineSoft}`,
                            borderRadius: 12,
                            background: 'rgba(250,252,254,.72)',
                            color: T.navyMid,
                            padding: 10,
                            outline: 'none',
                            resize: 'vertical',
                            fontSize: 12.8,
                            lineHeight: 1.55,
                            fontFamily: T.fontSans,
                          }}
                        />
                      </PlanningPanel>
                    </div>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 8, marginTop: 14 }}>
                    {[
                      ['heart', '喜欢'],
                      ['download', '下载'],
                      ['copy', copied === 'ip-system' ? '已复制' : '复制'],
                    ].map(([icon, label]) => (
                      <button
                        key={icon}
                        title={label}
                        aria-label={label}
                        onClick={() => {
                          if (icon === 'copy') {
                            copyText([...activeReport.names, activeReport.bio, ...activeReport.keywords, ...activeReport.phrases, ...activeReport.pillars, ...activeReport.bloggers, ...activeReport.covers].join('\n'));
                            setCopied('ip-system');
                          }
                        }}
                        style={{
                          width: 34,
                          height: 34,
                          borderRadius: 12,
                          border: `1px solid ${T.hairlineSoft}`,
                          background: 'rgba(255,255,255,.78)',
                          color: T.navyMid,
                          cursor: 'pointer',
                          display: 'inline-flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: 6,
                          fontSize: 12,
                          fontWeight: 650,
                        }}
                      >
                        <Icon name={icon} size={13} />
                      </button>
                    ))}
                  </div>
                </section>
                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, flexWrap: 'wrap' }}>
                  <button onClick={() => setReportVariant(v => v + 1)} style={{ height: 40, padding: '0 15px', borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.78)', color: T.navyMid, cursor: 'pointer', fontSize: 13, fontWeight: 700, display: 'inline-flex', alignItems: 'center', gap: 6 }}><Icon name="refresh" size={13} /> 重新生成</button>
                  <button onClick={() => setStep(4)} style={{ height: 40, padding: '0 18px', borderRadius: 13, border: 'none', background: T.navy, color: T.white, cursor: 'pointer', fontSize: 13, fontWeight: 700, boxShadow: '0 12px 24px rgba(14,14,44,.14)' }}>确认</button>
                </div>
              </>
            )}

            {step === 4 && (
              <>
                <NoriSays>
                  <p style={{ marginBottom: 4, fontSize: 15, fontWeight: 680 }}>我先排出未来一周的内容建议。</p>
                  <p style={{ color: T.navyMid, fontSize: 13 }}>V1 先不发布，只把计划和第一篇制作入口准备好。</p>
                </NoriSays>
                <PlanningPanel
                  title="一周内容规划"
                  action={(
                    <div style={{ position: 'relative' }}>
                      <button onClick={() => setShowWeekPicker(v => !v)} style={{ height: 32, padding: '0 11px', borderRadius: 12, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.78)', color: T.navyMid, cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 12, fontWeight: 650 }}>
                        <Icon name="calendar" size={13} />
                        选择周
                      </button>
                      {showWeekPicker && (
                        <input
                          type="date"
                          value={weekStart}
                          onChange={e => { setWeekStart(e.target.value); setShowWeekPicker(false); }}
                          style={{
                            position: 'absolute',
                            right: 0,
                            top: 38,
                            zIndex: 10,
                            height: 36,
                            border: `1px solid ${T.hairlineSoft}`,
                            borderRadius: 12,
                            background: T.white,
                            padding: '0 9px',
                            color: T.navyMid,
                            boxShadow: T.shadowMd,
                            fontFamily: T.fontSans,
                          }}
                        />
                      )}
                    </div>
                  )}
                >
                  <div style={{ margin: '-2px 0 12px', color: T.navyLight, fontSize: 12.2 }}>
                    规划周起始日：{weekStart}
                  </div>
                  <div style={{ display: 'grid', gap: 10 }}>
                    {calendar.map((item, index) => (
                      <div key={`${item.day}-${index}`} style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : '64px 86px minmax(0, 1fr) 34px', gap: 8, alignItems: 'center', padding: 10, borderRadius: 14, background: index === 0 ? 'rgba(239,239,253,.58)' : 'rgba(250,252,254,.72)', border: `1px solid ${index === 0 ? 'rgba(75,77,237,.14)' : T.hairlineSoft}` }}>
                        <input value={item.day} onChange={e => setCalendar(list => list.map((row, i) => i === index ? { ...row, day: e.target.value } : row))} style={{ border: 'none', background: 'transparent', color: T.navy, fontSize: 12.5, fontWeight: 720, outline: 'none' }} />
                        <input value={item.type} onChange={e => setCalendar(list => list.map((row, i) => i === index ? { ...row, type: e.target.value } : row))} style={{ border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.62)', borderRadius: 10, height: 32, padding: '0 9px', color: T.navyMid, fontSize: 12, outline: 'none' }} />
                        <textarea value={item.topic} rows={isMobile ? 2 : 1} onChange={e => setCalendar(list => list.map((row, i) => i === index ? { ...row, topic: e.target.value } : row))} style={{ border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.62)', borderRadius: 10, minHeight: 32, padding: '7px 9px', color: T.navy, fontSize: 12.5, outline: 'none', resize: 'vertical', fontFamily: T.fontSans, lineHeight: 1.45 }} />
                        <button onClick={() => setCalendar(list => list.filter((_, i) => i !== index))} style={{ ...iconBtnStyle(), width: 32, height: 32 }}><Icon name="close" size={11} /></button>
                        <input
                          value={item.ref}
                          onChange={e => setCalendar(list => list.map((row, i) => i === index ? { ...row, ref: e.target.value } : row))}
                          aria-label="参考账号"
                          style={{
                            gridColumn: isMobile ? 'auto' : '3 / 4',
                            border: 'none',
                            background: 'transparent',
                            color: T.navyLight,
                            fontSize: 11.5,
                            outline: 'none',
                            fontFamily: T.fontSans,
                          }}
                        />
                      </div>
                    ))}
                    <button onClick={() => setCalendar(list => [...list, { day: '新增', type: '图文', topic: '新的内容选题', ref: '@参考账号' }])} style={{ height: 36, borderRadius: 13, border: `1px dashed ${T.hairline}`, background: 'rgba(255,255,255,.58)', color: T.navyMid, cursor: 'pointer', fontSize: 12.5, fontWeight: 650 }}>新增一天</button>
                  </div>
                </PlanningPanel>
                <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <button onClick={complete} style={{ height: 42, padding: '0 20px', borderRadius: 14, border: 'none', background: T.navy, color: T.white, cursor: 'pointer', fontSize: 13.2, fontWeight: 740, boxShadow: '0 14px 28px rgba(14,14,44,.16)' }}>开始制作第一篇</button>
                </div>
              </>
            )}
          </div>
          {!isMobile && <div style={{ position: 'sticky', top: 92 }}>{memory}</div>}
        </div>
      </main>
      {modalType && <InputMethodModal type={modalType} onClose={() => setModalType(null)} onConfirm={confirmAttachment} />}
    </div>
  );
};

window.AccountPlanningPagePolished = AccountPlanningPagePolished;

const PLAN_STORAGE_KEY = 'nori-account-plan-draft-v2';

const buildPlanExportText = (state) => {
  const planPersona = state.persona || {};
  const personaName = planPersona.name || planPersona.names?.[0] || '巷口暖胃小馆';
  const personaKeywords = Array.isArray(planPersona.keywords) ? planPersona.keywords.join('、') : planPersona.keywords;
  const personaTone = Array.isArray(planPersona.phrases) ? planPersona.phrases.join(' / ') : planPersona.tone;
  const personaCover = Array.isArray(planPersona.covers) ? planPersona.covers[0] : planPersona.cover;
  const lines = [
    '《账号定位 + 运营计划 + 内容排期》',
    '',
    `账号定位：${state.diagnosisText.position}`,
    `目标受众：${state.diagnosisText.audience}`,
    `内容方向：${state.diagnosisText.directions.replace(/\n/g, ' / ')}`,
    `对标账号：${state.diagnosisText.benchmarks.replace(/\n/g, ' / ')}`,
    `差异化卖点：${state.diagnosisText.selling}`,
    '',
    `人设：${personaName}`,
    `签名：${planPersona.bio}`,
    `关键词：${personaKeywords}`,
    `语气：${personaTone}`,
    `封面：${personaCover}`,
    '',
    `选题库：${state.pillars.join(' / ')}`,
    `发布节奏：${state.calendar.map(item => `${item.day} ${item.type} ${item.topic}`).join(' | ')}`,
    `数据目标：7 天内验证 1 套稳定选题结构，收藏率 / 完读率 / 点击率保持可持续提升`,
  ];
  return lines.join('\n');
};

const PlanningChatDivider = ({ label }) => (
  <div style={{
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    margin: '4px 0',
    color: T.navyLight,
    fontSize: 11.5,
    fontWeight: 650,
  }}>
    <span style={{ height: 1, flex: 1, background: T.hairlineSoft }} />
    <span>{label}</span>
    <span style={{ height: 1, flex: 1, background: T.hairlineSoft }} />
  </div>
);

const PlanningUserSummary = ({ children }) => (
  <Bubble from="user" style={{ margin: '2px 0' }}>
    <div style={{ whiteSpace: 'pre-wrap' }}>{children}</div>
  </Bubble>
);

const PlanningPlainReply = ({ children, style }) => (
  <AgentReply style={style}>{children}</AgentReply>
);

const PlanningPlainText = ({ children, style }) => (
  <AgentReply style={style}>{children}</AgentReply>
);

const PlanningChatCard = ({ children, style, label = 'Agent', title = '协作卡片', icon = 'sparkles', action }) => (
  <AgentCardShell label={label} title={title} icon={icon} action={action} style={style}>
    {children}
  </AgentCardShell>
);

const PlanningStartPanel = ({ quickLink, setQuickLink, onUploadImage, onUploadDoc, onPasteLink }) => (
  <div style={{ display: 'grid', gap: 10 }}>
    <div style={{
      minWidth: 0,
      height: 46,
      borderRadius: 16,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(250,252,254,.76)',
      display: 'flex',
      alignItems: 'center',
      padding: '0 14px',
      boxShadow: 'inset 0 1px 0 rgba(255,255,255,.84)',
    }}>
      <Icon name="link" size={14} color={T.navyLight} />
      <input
        value={quickLink}
        onChange={e => setQuickLink(e.target.value)}
        placeholder="粘贴美团 / 大众点评 / 小红书店铺链接"
        style={{
          flex: 1,
          minWidth: 0,
          border: 'none',
          outline: 'none',
          background: 'transparent',
          color: T.navy,
          fontSize: 13.5,
          lineHeight: 1.5,
          marginLeft: 10,
          fontFamily: T.fontSans,
        }}
      />
    </div>
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(3, minmax(0, 1fr))',
      gap: 10,
    }}>
      <button onClick={onUploadImage} style={{ ...pillButtonStyle(false), height: 38, borderRadius: 13, justifyContent: 'center' }}>
        <Icon name="upload" size={14} />
        上传图片
      </button>
      <button onClick={onUploadDoc} style={{ ...pillButtonStyle(false), height: 38, borderRadius: 13, justifyContent: 'center' }}>
        <Icon name="document" size={14} />
        上传文档
      </button>
      <button onClick={onPasteLink} style={{ ...pillButtonStyle(false), height: 38, borderRadius: 13, justifyContent: 'center' }}>
        <Icon name="link" size={14} />
        粘贴链接
      </button>
    </div>
  </div>
);

const PlanningUploadedAssetStrip = ({ attachments, onAddMore, onConfirm }) => {
  const [open, setOpen] = React.useState(false);
  const fallback = [
    { type: 'link', label: '美团店铺链接', value: '上海暖胃小馆 · 店铺主页', thumb: PLANNING_ASSET_THUMBS[2] },
    { type: 'image', label: '菜单与环境图片', value: '4 张', thumb: PLANNING_ASSET_THUMBS[0] },
    { type: 'file', label: '用户评价摘要', value: '32 条评论', thumb: PLANNING_ASSET_THUMBS[3] },
  ];
  const assets = (attachments.length ? attachments : fallback).map((item, index) => ({
    ...item,
    thumb: item.thumb || (item.preview && item.type === 'image' ? item.preview : PLANNING_ASSET_THUMBS[index % PLANNING_ASSET_THUMBS.length]),
  }));
  const shown = open ? assets : assets.slice(0, 4);
  const iconFor = (type) => type === 'link' ? 'link' : type === 'image' ? 'image' : type === 'video' ? 'video' : 'file';
  return (
    <AgentCardShell
      label="Agent 资产识别"
      icon="folder"
      title="已读到的资料"
      action={(
        <>
          <button onClick={onAddMore} style={{ ...pillButtonStyle(false), height: 34, borderRadius: 12, fontSize: 12.4 }}><Icon name="plus" size={13} />添加更多</button>
          {onConfirm && <button onClick={onConfirm} style={{ ...planningActionButtonStyle('primary'), height: 34, borderRadius: 12, fontSize: 12.4 }}>确认，下一步<Icon name="arrowRight" size={13} /></button>}
        </>
      )}
      style={{ padding: 13 }}
      bodyStyle={{ fontSize: 12.6 }}
    >
      <div style={{ display: 'grid', gap: 10 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(112px, 1fr))', gap: 8 }}>
          {shown.map((item, index) => (
            <div key={`${item.type}-${index}`} style={{
              minWidth: 0,
              borderRadius: 14,
              border: `1px solid ${T.hairlineSoft}`,
              background: 'rgba(250,252,254,.76)',
              padding: 7,
              display: 'grid',
              gridTemplateColumns: '34px minmax(0, 1fr)',
              gap: 8,
              alignItems: 'center',
            }}>
              <span style={{ width: 34, height: 34, borderRadius: 10, overflow: 'hidden', background: T.surface, color: T.navyLight, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
                {item.thumb ? <img src={item.thumb} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} /> : <Icon name={iconFor(item.type)} size={14} />}
              </span>
              <span style={{ minWidth: 0 }}>
                <span style={{ display: 'block', color: T.navy, fontSize: 11.8, lineHeight: 1.35, fontWeight: 680, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{item.label || item.value || item.type}</span>
                <span style={{ display: 'block', marginTop: 2, color: T.navyLight, fontSize: 10.8, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{item.value || (item.type === 'image' ? '图片素材' : item.type === 'link' ? '链接线索' : '文档资料')}</span>
              </span>
            </div>
          ))}
        </div>
        {assets.length > 4 && (
          <button onClick={() => setOpen(v => !v)} style={{ border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', justifySelf: 'start', fontSize: 12, fontWeight: 650, padding: 0 }}>
            {open ? '收起资料' : `展开全部 ${assets.length} 个资料`}
          </button>
        )}
      </div>
    </AgentCardShell>
  );
};

const PlanningResearchFlow = ({ bullets, conclusion, isMobile, onComplete, showThinking = true }) => {
  React.useEffect(() => {
    const timers = [window.setTimeout(() => onComplete?.(), 1200)];
    return () => timers.forEach(window.clearTimeout);
  }, [bullets, onComplete]);
  return null;
};

const PlanningAnalysisPreview = ({ thumbnail, title, bullets }) => (
  <div style={{
    borderRadius: 18,
    border: `1px solid ${T.hairlineSoft}`,
    background: 'rgba(255,255,255,.82)',
    boxShadow: '0 12px 28px rgba(14,14,44,.04), inset 0 1px 0 rgba(255,255,255,.84)',
    padding: 12,
  }}>
    <div style={{ display: 'grid', gridTemplateColumns: '92px minmax(0, 1fr)', gap: 12, alignItems: 'stretch' }}>
      <div style={{
        borderRadius: 16,
        overflow: 'hidden',
        background: T.surface,
        minHeight: 130,
        position: 'relative',
        border: `1px solid ${T.hairlineSoft}`,
      }}>
        <img src={thumbnail} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} />
        <div style={{
          position: 'absolute',
          left: 8,
          right: 8,
          bottom: 8,
          padding: '6px 8px',
          borderRadius: 12,
          background: 'rgba(255,255,255,.82)',
          color: T.navyMid,
          fontSize: 10.8,
          fontWeight: 650,
          lineHeight: 1.45,
        }}>
          资料缩略图
        </div>
      </div>
      <div style={{ minWidth: 0, display: 'grid', gap: 9 }}>
        <div>
          <div style={{ color: T.navy, fontSize: 14.8, fontWeight: 720 }}>{title}</div>
          <div style={{ marginTop: 4, color: T.navyLight, fontSize: 12.3, lineHeight: 1.6 }}>
            我先看了同赛道头部账号和你给的素材，目的是把定位做出差异，避免一上来就和别人长得一样。
          </div>
        </div>
        <div style={{ display: 'grid', gap: 6 }}>
          {bullets.map(item => (
            <div key={item.label} style={{
              display: 'grid',
              gridTemplateColumns: '58px minmax(0, 1fr)',
              gap: 8,
              alignItems: 'start',
            }}>
              <span style={{
                height: 22,
                padding: '0 8px',
                borderRadius: 999,
                background: item.tint,
                color: item.color,
                display: 'inline-flex',
                alignItems: 'center',
                fontSize: 11.2,
                fontWeight: 700,
              }}>{item.label}</span>
              <div style={{ color: T.navyMid, fontSize: 12.8, lineHeight: 1.58 }}>{item.text}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
);

const PlanningBenchmarkList = ({ accounts }) => (
  <div style={{ display: 'grid', gap: 8 }}>
    {accounts.map((item, index) => (
      <div key={`${item.name}-${index}`} style={{
        display: 'grid',
        gridTemplateColumns: '40px minmax(0, 1fr) auto',
        gap: 10,
        alignItems: 'center',
        borderRadius: 16,
        padding: 10,
        border: `1px solid ${T.hairlineSoft}`,
        background: 'rgba(250,252,254,.76)',
        }}>
        <img src={item.photo} alt="" style={{ width: 40, height: 40, borderRadius: 14, objectFit: 'cover' }} />
        <div style={{ minWidth: 0 }}>
          <div style={{ color: T.navy, fontSize: 12.8, fontWeight: 700, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{item.name}</div>
          <div style={{ marginTop: 3, color: T.navyLight, fontSize: 11.5, lineHeight: 1.45 }}>
            {item.platform}
          </div>
        </div>
        <div style={{
          padding: '5px 8px',
          borderRadius: 999,
          background: 'rgba(224,250,244,.88)',
          color: T.success,
          fontSize: 11.2,
          fontWeight: 700,
          whiteSpace: 'nowrap',
        }}>
          相似度 {item.similarity}
        </div>
      </div>
    ))}
  </div>
);

const planningActionButtonStyle = (variant = 'secondary') => ({
  ...pillButtonStyle(variant === 'primary'),
  height: 38,
  padding: '0 15px',
  borderRadius: 13,
  fontSize: 13,
  fontWeight: 720,
});

const PLANNING_BENCHMARK_PHOTOS = [
  'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=900&q=80',
  'https://images.unsplash.com/photo-1498654896293-37aacf113fd9?auto=format&fit=crop&w=900&q=80',
];

const PLANNING_ASSET_THUMBS = [
  './src/inspiration-skill-card.png',
  './src/onion-burst-real.png',
  './src/insight-avatar-reference.png',
  './src/onion-burst-collage.png',
];

const PLANNING_STRATEGY_IMAGES = [
  'https://images.unsplash.com/photo-1528712306091-ed0763094c98?auto=format&fit=crop&w=1400&q=80',
  'https://images.unsplash.com/photo-1504674900247-0877df9cc836?auto=format&fit=crop&w=1400&q=80',
  'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1400&q=80',
];

const PlanningBenchmarkAccounts = ({ isMobile }) => {
  const accounts = [
    { name: '@本地吃喝指南', platform: '小红书', desc: '标题清楚，强收藏结构，适合学习「第一次来怎么点」。', stat: '8.6w 粉', tone: T.iris, photo: PLANNING_BENCHMARK_PHOTOS[0] },
    { name: '@街角小店日记', platform: '抖音', desc: '人物感强，后厨和主理人日常能建立信任。', stat: '12.4w 粉', tone: T.success, photo: PLANNING_BENCHMARK_PHOTOS[1] },
    { name: '@城市午餐研究所', platform: '小红书', desc: '细分通勤午餐场景，选题切口很适合引流到店。', stat: '5.2w 粉', tone: '#6e8400', photo: PLANNING_BENCHMARK_PHOTOS[2] },
  ];
  return (
    <PlanningChatCard style={{ padding: 16 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, marginBottom: 14 }}>
        <div>
          <div style={{ color: T.navy, fontSize: 15, fontWeight: 720 }}>对标账号</div>
          <div style={{ marginTop: 4, color: T.navyLight, fontSize: 12.2 }}>先看这 3 个账号的结构，不照抄视觉。</div>
        </div>
        <Icon name="trending" size={18} color={T.navyLight} />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(3, minmax(0, 1fr))', gap: 10 }}>
        {accounts.map((account, index) => (
          <div key={account.name} style={{
            borderRadius: 18,
            border: `1px solid ${T.hairlineSoft}`,
            background: 'rgba(250,252,254,.78)',
            overflow: 'hidden',
            boxShadow: '0 10px 24px rgba(14,14,44,.04)',
          }}>
            <div style={{
              height: 124,
              background: `linear-gradient(180deg, rgba(14,14,44,.02), rgba(14,14,44,.20)), url(${account.photo}) center / cover`,
              borderBottom: `1px solid ${T.hairlineSoft}`,
              position: 'relative',
            }}>
              <div style={{ position: 'absolute', left: 12, bottom: 12, width: 42, height: 42, borderRadius: 16, background: 'rgba(255,255,255,.82)', color: account.tone, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', fontWeight: 820, boxShadow: '0 10px 24px rgba(14,14,44,.12)', backdropFilter: 'blur(10px)' }}>
                {account.platform === '抖音' ? '抖' : '红'}
              </div>
              <span style={{ position: 'absolute', right: 12, top: 12, height: 26, padding: '0 9px', borderRadius: 999, background: 'rgba(255,255,255,.78)', color: T.navyMid, display: 'inline-flex', alignItems: 'center', fontSize: 11.5, fontWeight: 700, backdropFilter: 'blur(10px)' }}>{account.platform}</span>
            </div>
            <div style={{ padding: 13 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8, alignItems: 'center' }}>
                <div style={{ color: T.navy, fontSize: 13.5, fontWeight: 740 }}>{account.name}</div>
                <span style={{ color: T.navyLight, fontSize: 11.5, fontFamily: T.fontMono }}>{account.stat}</span>
              </div>
              <div style={{ marginTop: 7, color: T.navyMid, fontSize: 12.2, lineHeight: 1.58 }}>{account.desc}</div>
              <button onClick={() => window.open(account.platform === '抖音' ? 'https://www.douyin.com/' : 'https://www.xiaohongshu.com/', '_blank')} style={{ marginTop: 12, height: 32, borderRadius: 11, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.78)', color: T.navyMid, cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: 6, padding: '0 10px', fontSize: 12, fontWeight: 650 }}>
                打开平台
                <Icon name="arrowRight" size={12} />
              </button>
            </div>
          </div>
        ))}
      </div>
    </PlanningChatCard>
  );
};

const PlanningGeneLibrary = ({ attachments, onAddMore }) => {
  const fallback = [
    { type: 'link', label: '店铺主页链接', thumb: PLANNING_ASSET_THUMBS[2] },
    { type: 'image', label: '菜单截图 2 张', thumb: PLANNING_ASSET_THUMBS[0] },
    { type: 'file', label: '历史笔记 / 文案片段', thumb: PLANNING_ASSET_THUMBS[3] },
    { type: 'video', label: '门店短视频素材', thumb: PLANNING_ASSET_THUMBS[1] },
  ];
  const assets = (attachments.length ? attachments : fallback).map((item, index) => ({
    ...item,
    thumb: item.thumb || (item.preview && item.type === 'image' ? item.preview : PLANNING_ASSET_THUMBS[index % PLANNING_ASSET_THUMBS.length]),
  }));
  const iconFor = (type) => type === 'link' ? 'link' : type === 'image' ? 'image' : type === 'video' ? 'video' : 'file';
  return (
    <PlanningChatCard style={{ padding: 16 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, marginBottom: 14 }}>
        <div>
          <div style={{ color: T.navy, fontSize: 15, fontWeight: 720 }}>资产库</div>
          <div style={{ marginTop: 4, color: T.navyLight, fontSize: 12.2 }}>你已经有一个可被 Nori 理解的资产库。</div>
        </div>
        <button onClick={onAddMore} style={{ border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', fontSize: 12.2, fontWeight: 650 }}>
          添加更多
        </button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(148px, 1fr))', gap: 9 }}>
        {assets.map((item, index) => (
          <div key={`${item.type}-${index}`} style={{
            minHeight: 58,
            padding: 8,
            borderRadius: 16,
            background: 'rgba(250,252,254,.78)',
            border: `1px solid ${T.hairlineSoft}`,
            color: T.navyMid,
            display: 'grid',
            gridTemplateColumns: '44px minmax(0, 1fr)',
            alignItems: 'center',
            gap: 9,
            fontSize: 12,
            fontWeight: 620,
          }}>
            <div style={{ width: 44, height: 44, borderRadius: 13, overflow: 'hidden', background: T.surface, position: 'relative', border: `1px solid ${T.hairlineSoft}` }}>
              <img src={item.thumb} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', filter: item.type === 'file' || item.type === 'link' ? 'saturate(.85) opacity(.72)' : 'none' }} />
              <span style={{ position: 'absolute', right: 4, bottom: 4, width: 18, height: 18, borderRadius: 7, background: 'rgba(255,255,255,.82)', color: T.navyMid, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 4px 10px rgba(14,14,44,.10)' }}>
                <Icon name={iconFor(item.type)} size={10} />
              </span>
            </div>
            <div style={{ minWidth: 0 }}>
              <div style={{ color: T.navy, fontSize: 12.4, fontWeight: 690, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{item.label || item.value || item.type}</div>
              <div style={{ marginTop: 3, color: T.navyLight, fontSize: 11.2 }}>{item.type === 'image' ? '图片素材' : item.type === 'video' ? '视频素材' : item.type === 'link' ? '链接线索' : '文档资料'}</div>
            </div>
          </div>
        ))}
      </div>
    </PlanningChatCard>
  );
};

const PlanningTagEditor = ({ label, tags, onChange, singleRow = false }) => {
  const addTag = () => onChange([...tags, '新增']);
  return (
    <div>
      <div style={{ color: T.navyLight, fontSize: 11.8, fontWeight: 690, marginBottom: 7 }}>{label}</div>
      <div style={{ display: 'flex', flexWrap: singleRow ? 'nowrap' : 'wrap', gap: 7, overflowX: singleRow ? 'auto' : 'visible', paddingBottom: singleRow ? 2 : 0 }}>
        {tags.map((tag, index) => (
          <span key={`${label}-${index}`} style={{
            minHeight: 33,
            padding: '0 7px 0 11px',
            borderRadius: 999,
            border: `1px solid ${T.hairlineSoft}`,
            background: 'rgba(250,252,254,.78)',
            display: 'inline-flex',
            alignItems: 'center',
            gap: 6,
            maxWidth: '100%',
            boxShadow: 'inset 0 1px 0 rgba(255,255,255,.82)',
          }}>
            <input
              value={tag}
              onChange={e => onChange(tags.map((item, i) => i === index ? e.target.value : item))}
              style={{
                width: `${Math.min(240, Math.max(64, tag.length * 14 + 18))}px`,
                minWidth: 64,
                maxWidth: 240,
                border: 'none',
                outline: 'none',
                background: 'transparent',
                color: T.navy,
                fontSize: 12.4,
                lineHeight: 1.5,
                fontFamily: T.fontSans,
                fontWeight: 560,
                padding: 0,
              }}
            />
            <button onClick={() => onChange(tags.filter((_, i) => i !== index))} style={{ border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', padding: 0, width: 18, height: 18, borderRadius: '50%', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <Icon name="close" size={11} />
            </button>
          </span>
        ))}
        <button onClick={addTag} style={{ height: 31, padding: '0 10px', borderRadius: 999, border: `1px dashed ${T.hairline}`, background: 'rgba(255,255,255,.66)', color: T.navyMid, cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: 5, fontSize: 12, fontWeight: 650 }}>
          <Icon name="plus" size={13} />
          添加
        </button>
      </div>
    </div>
  );
};

const PlanningTagReadOnly = ({ label, tags, singleRow = false }) => (
  <div>
    <div style={{ color: T.navyLight, fontSize: 11.8, fontWeight: 690, marginBottom: 7 }}>{label}</div>
    <div style={{ display: 'flex', flexWrap: singleRow ? 'nowrap' : 'wrap', gap: 7, overflowX: singleRow ? 'auto' : 'visible', paddingBottom: singleRow ? 2 : 0 }}>
      {tags.map((tag, index) => (
        <span key={`${label}-${index}`} style={{
          minHeight: 33,
          padding: '0 10px',
          borderRadius: 999,
          border: `1px solid ${T.hairlineSoft}`,
          background: 'rgba(250,252,254,.78)',
          display: 'inline-flex',
          alignItems: 'center',
          color: T.navy,
          fontSize: 12.6,
          lineHeight: 1.45,
          fontWeight: 560,
        }}>{tag}</span>
      ))}
    </div>
  </div>
);

const PlanningSkeletonCard = ({ diagnosisText, setDiagnosisText, audienceTags, setAudienceTags, appearanceTags, setAppearanceTags, marketTags, setMarketTags, isMobile }) => {
  return (
    <PlanningChatCard style={{ padding: 16 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', gap: 14, alignItems: 'flex-start', marginBottom: 14 }}>
        <div>
          <div style={{ color: T.navy, fontSize: 15, fontWeight: 720 }}>账号定位</div>
          <div style={{ marginTop: 4, color: T.navyLight, fontSize: 12.2 }}>Nori 先把基础判断整理成可编辑结构。</div>
        </div>
        <span style={{ width: 34, height: 34, borderRadius: 13, background: T.irisTint, color: T.iris, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
          <Icon name="target" size={16} />
        </span>
      </div>
      <div style={{ display: 'grid', gap: 14 }}>
        <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(2, minmax(0, 1fr))', gap: 14 }}>
          <section style={{ display: 'grid', gap: 12 }}>
            <div>
              <h4 style={{ margin: '0 0 8px', color: T.navy, fontSize: 14.6, fontWeight: 690 }}>目标受众</h4>
              <PlanningTagEditor label="年龄 / 城市 / 需求" tags={audienceTags} onChange={setAudienceTags} singleRow />
            </div>
            <div>
              <h4 style={{ margin: '0 0 8px', color: T.navy, fontSize: 14.6, fontWeight: 690 }}>赛道细分</h4>
              <PlanningTagEditor label="大领域切小切口" tags={marketTags} onChange={setMarketTags} />
            </div>
          </section>
          <section style={{ display: 'grid', gap: 12 }}>
            <div>
              <h4 style={{ margin: '0 0 8px', color: T.navy, fontSize: 14.6, fontWeight: 690 }}>人设标签</h4>
              <PlanningTagReadOnly label="专业 / 亲切 / 干货" tags={['亲切', '真实主理人', '懂本地生活']} singleRow />
            </div>
            <div>
              <h4 style={{ margin: '0 0 8px', color: T.navy, fontSize: 14.6, fontWeight: 690 }}>内容价值</h4>
              <PlanningTagReadOnly label="干货 / 种草 / 测评 / 剧情" tags={['不踩雷菜单', '真实种草', '到店决策']} singleRow />
            </div>
          </section>
        </div>
        <section>
          <h4 style={{ margin: '0 0 8px', color: T.navy, fontSize: 14.6, fontWeight: 690 }}>内容出镜元素</h4>
          <PlanningTagEditor label="角色 / 语气 / 视觉线索" tags={appearanceTags} onChange={setAppearanceTags} />
        </section>
        <section>
          <h4 style={{ margin: '0 0 8px', color: T.navy, fontSize: 14.6, fontWeight: 690 }}>账号定位</h4>
          <textarea
            value={`${diagnosisText.position}\n\n${diagnosisText.selling}`}
            onChange={e => {
              const [position, ...rest] = e.target.value.split('\n\n');
              setDiagnosisText(prev => ({ ...prev, position, selling: rest.join('\n\n') || prev.selling }));
            }}
            rows={4}
            style={{ width: '100%', border: `1px solid ${T.hairlineSoft}`, background: 'rgba(250,252,254,.72)', borderRadius: 16, padding: 13, resize: 'vertical', outline: 'none', color: T.navy, fontSize: 13.2, lineHeight: 1.66, fontFamily: T.fontSans }}
          />
        </section>
      </div>
    </PlanningChatCard>
  );
};

const PlanningSkeletonMerge = ({ diagnosisText, setDiagnosisText, audienceTags, setAudienceTags, appearanceTags, setAppearanceTags, marketTags, setMarketTags, pillars = [], setPillars = () => {}, isMobile, action }) => {
  const accounts = [
    { name: '@本地吃喝指南', platform: '小红书', similarity: '86%', photo: PLANNING_BENCHMARK_PHOTOS[0] },
    { name: '@街角小店日记', platform: '抖音', similarity: '79%', photo: PLANNING_BENCHMARK_PHOTOS[1] },
    { name: '@城市午餐研究所', platform: '小红书', similarity: '74%', photo: PLANNING_BENCHMARK_PHOTOS[2] },
  ];
  return (
    <AgentCardShell label="Agent 账号定位确认" icon="target" title="账号定位 / 对标账号" style={{ padding: 16 }} action={action}>
      <div style={{ display: 'grid', gap: 14 }}>
        {[
          ['你的观众是：', '23-38 岁附近上班族、情侣和周末约饭人群。他们关心味道稳定、价格舒服、离自己近，最好读完就知道第一次怎么点。'],
          ['你的赛道是：', '上海本地生活里的社区饭店推荐，不做泛探店，重点切「附近人真实复吃」和「下班后不纠结的一顿饭」。'],
          ['你的人设是：', '亲切、真实主理人、懂本地生活。说话像熟人推荐，不夸张种草，也不做过度精修。'],
          ['你的内容价值是：', '帮用户降低到店决策成本：点什么、什么时候去、适合谁去、有哪些避坑信息。'],
          ['你的风格是：', '口语化、轻松、干净。封面用真实菜品和店内细节，正文用清晰小标题。'],
          ['你的内容大纲是：', pillars.join(' / ')],
          ['你的账号定位是：', `${diagnosisText.position} ${diagnosisText.selling}`],
        ].map(([label, value]) => (
          <section key={label} style={{ display: 'grid', gap: 5 }}>
            <h4 style={{ margin: 0, color: T.navy, fontSize: 14.2, lineHeight: 1.42, fontWeight: 700 }}>{label}</h4>
            <p style={{ margin: 0, color: T.navyMid, fontSize: 13.1, lineHeight: 1.68 }}>{value}</p>
          </section>
        ))}
        <section>
          <h4 style={{ margin: '0 0 8px', color: T.navy, fontSize: 14.2, fontWeight: 700 }}>你的对标博主是：</h4>
          <PlanningBenchmarkList accounts={accounts} />
        </section>
        <section style={{ display: 'grid', gap: 8 }}>
          <h4 style={{ margin: 0, color: T.navy, fontSize: 14.2, lineHeight: 1.42, fontWeight: 700 }}>品牌资产沉淀</h4>
          <div style={{
            borderRadius: 16,
            border: `1px solid ${T.hairlineSoft}`,
            background: 'rgba(250,252,254,.72)',
            padding: isMobile ? 12 : 14,
            display: 'grid',
            gridTemplateColumns: isMobile ? '1fr' : 'repeat(2, minmax(0, 1fr))',
            gap: 10,
          }}>
            {[
              ['店铺名', '巷口暖胃小馆，可作为账号主名或系列栏目名。'],
              ['Logo 线索', '暖色小碗图形适合做头像、封面角标和水印。'],
              ['视觉风格', '真实菜品近景、暖色自然光、干净小标题。'],
              ['语气资产', '熟人推荐、不夸张，先给点单结论再补理由。'],
            ].map(([label, value]) => (
              <div key={label} style={{ minWidth: 0 }}>
                <div style={{ color: T.navyLight, fontSize: 11.4, lineHeight: 1.35, fontWeight: 680, marginBottom: 4 }}>{label}</div>
                <div style={{ color: T.navyMid, fontSize: 12.6, lineHeight: 1.58, fontWeight: 480 }}>{value}</div>
              </div>
            ))}
          </div>
        </section>
      </div>
    </AgentCardShell>
  );
};

const PlanningAssetSummaryPanel = ({ onAddMore }) => (
  <AgentReply>
    你已经给了店铺链接、店铺图片和很多真实评价，这些都能组成可用的资产库。
  </AgentReply>
);

const PlanningAssetPermissionPrompt = ({ onAddMore, onConfirm }) => null;

const PlanningAssetUploadGrid = ({ attachments, onAddMore }) => {
  const fallback = [
    { type: 'link', label: '店铺主页链接', thumb: PLANNING_ASSET_THUMBS[2] },
    { type: 'image', label: '菜单截图 2 张', thumb: PLANNING_ASSET_THUMBS[0] },
    { type: 'file', label: '历史笔记 / 文案片段', thumb: PLANNING_ASSET_THUMBS[3] },
    { type: 'video', label: '门店短视频素材', thumb: PLANNING_ASSET_THUMBS[1] },
  ];
  const assets = (attachments.length ? attachments : fallback).map((item, index) => ({
    ...item,
    thumb: item.thumb || (item.preview && item.type === 'image' ? item.preview : PLANNING_ASSET_THUMBS[index % PLANNING_ASSET_THUMBS.length]),
  }));
  const iconFor = (type) => type === 'link' ? 'link' : type === 'image' ? 'image' : type === 'video' ? 'video' : 'file';
  return (
    <PlanningChatCard style={{ padding: 18 }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, marginBottom: 12 }}>
        <div>
          <div style={{ color: T.navy, fontSize: 15, fontWeight: 720 }}>资产库</div>
          <div style={{ marginTop: 4, color: T.navyLight, fontSize: 12.2 }}>你已经有一个可被 Nori 理解的资产库。</div>
        </div>
        <button onClick={onAddMore} style={{ ...pillButtonStyle(false), height: 34, borderRadius: 12, justifyContent: 'center' }}>
          <Icon name="plus" size={13} />
          添加更多
        </button>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 10 }}>
        {assets.map((item, index) => (
          <div key={`${item.type}-${index}`} style={{
            borderRadius: 18,
            overflow: 'hidden',
            border: `1px solid ${T.hairlineSoft}`,
            background: 'rgba(250,252,254,.76)',
            boxShadow: '0 10px 22px rgba(14,14,44,.04)',
          }}>
            <div style={{ height: 118, position: 'relative', background: T.surface }}>
              <img src={item.thumb} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block', filter: item.type === 'file' || item.type === 'link' ? 'saturate(.88) opacity(.76)' : 'none' }} />
              <span style={{ position: 'absolute', left: 10, top: 10, width: 20, height: 20, borderRadius: 7, background: 'rgba(255,255,255,.92)', border: `1px solid ${T.hairlineSoft}`, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', color: T.navyMid }}>
                <Icon name={iconFor(item.type)} size={10} />
              </span>
              <span style={{ position: 'absolute', left: 10, bottom: 10, height: 24, padding: '0 9px', borderRadius: 999, background: 'rgba(255,255,255,.88)', color: T.navyMid, fontSize: 11.2, fontWeight: 650, display: 'inline-flex', alignItems: 'center' }}>用过的</span>
            </div>
            <div style={{ padding: 12 }}>
              <div style={{ color: T.navy, fontSize: 12.8, fontWeight: 700, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{item.label || item.value || item.type}</div>
              <div style={{ marginTop: 4, color: T.navyLight, fontSize: 11.4 }}>{item.type === 'image' ? '图片素材' : item.type === 'video' ? '视频素材' : item.type === 'link' ? '链接线索' : '文档资料'}</div>
            </div>
          </div>
        ))}
      </div>
    </PlanningChatCard>
  );
};

const PlanningStrategyDocModal = ({ strategy, onClose }) => {
  if (!strategy) return null;
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 1000, background: 'rgba(8,8,18,.46)', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24 }}>
      <div style={{ width: 'min(920px, 100%)', maxHeight: '86vh', overflow: 'hidden', borderRadius: 26, background: T.white, border: `1px solid ${T.hairlineSoft}`, boxShadow: '0 44px 110px rgba(14,14,44,.24)' }}>
        <div style={{ height: 64, padding: '0 22px', borderBottom: `1px solid ${T.hairlineSoft}`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <span style={{ width: 38, height: 38, borderRadius: 14, background: T.irisTint, color: T.iris, display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
              <Icon name="document" size={18} />
            </span>
            <div>
              <div style={{ color: T.navy, fontSize: 16, fontWeight: 740 }}>{strategy.name} · 完整运营计划</div>
              <div style={{ marginTop: 3, color: T.navyLight, fontSize: 12.2 }}>刚刚生成 · 可用于后续创作</div>
            </div>
          </div>
          <button onClick={onClose} style={iconBtnStyle()}><Icon name="close" size={15} color={T.navyMid} /></button>
        </div>
        <div style={{ overflowY: 'auto', maxHeight: 'calc(86vh - 64px)', padding: '34px min(9vw, 86px) 48px' }}>
          <h1 style={{ margin: 0, color: T.navy, fontSize: 34, lineHeight: 1.18, fontWeight: 740 }}>{strategy.name} 完整运营计划</h1>
          {[
            ['1. 账号定位', strategy.position],
            ['2. 人设关键词', strategy.keyword],
            ['3. 内容支柱', strategy.pillar],
            ['4. 签名', strategy.bio],
            ['5. 发布节奏', '第一周先用「真实场景 + 可收藏清单」验证点击和收藏，图文与短视频交替。'],
            ['6. 数据目标', '7 天内验证 1 套稳定标题结构，重点看收藏、评论和净涨粉。'],
          ].map(([title, body]) => (
            <section key={title} style={{ marginTop: 30 }}>
              <h2 style={{ margin: '0 0 12px', color: T.navy, fontSize: 22, fontWeight: 740 }}>{title}</h2>
              <p style={{ margin: 0, color: T.navyMid, fontSize: 15, lineHeight: 1.9 }}>{body}</p>
            </section>
          ))}
        </div>
      </div>
    </div>
  );
};

const PlanningStrategyCards = ({ isMobile, activeReport, pillars, onOpenDoc, onConfirm }) => {
  const [expandedId, setExpandedId] = React.useState('warm');
  const [selectedId, setSelectedId] = React.useState('warm');
  const [checkedId, setCheckedId] = React.useState(null);
  const strategies = [
    {
      id: 'warm',
      name: activeReport.names?.[0] || '巷口暖胃小馆',
      keyword: activeReport.keywords?.[0] || '真实主理人',
      pillar: pillars?.[0] || '招牌菜故事',
      bio: activeReport.bio || '每天认真做一碗有烟火气的家常饭。',
      position: '做附近人愿意收藏的烟火气小馆账号，先建立信任，再引导到店。',
      recommended: true,
      image: PLANNING_STRATEGY_IMAGES[0],
      why: '最贴近你现有素材和门店气质，第一周验证成本最低。',
    },
    {
      id: 'city',
      name: '附近午餐研究所',
      keyword: '效率友好',
      pillar: '30 分钟午餐方案',
      bio: '帮附近上班族快速找到一顿不踩雷的饭。',
      position: '用细分场景切入本地午餐需求，主打收藏和搜索。',
      image: PLANNING_STRATEGY_IMAGES[1],
      why: '适合做搜索流量和菜单合集，内容更工具化。',
    },
    {
      id: 'owner',
      name: '主理人认真饭',
      keyword: '主理人视角',
      pillar: '老板的一天',
      bio: '把小店日常讲给真正会复吃的人听。',
      position: '提高人物记忆点，让用户先记住人，再记住菜。',
      image: PLANNING_STRATEGY_IMAGES[2],
      why: '适合主理人愿意稳定出镜时使用，信任感更强。',
    },
  ];
  return (
    <AgentCardShell
      label="Agent 运营计划"
      icon="layers"
      title="三套可执行运营计划"
      action={<button onClick={() => onConfirm?.()} style={{ ...planningActionButtonStyle('primary') }}>确认运营计划，排期<Icon name="arrowRight" size={14} /></button>}
    >
      <div style={{ display: 'grid', gap: 11 }}>
      {strategies.map((item, index) => {
        const expanded = isMobile || expandedId === item.id;
        const selected = selectedId === item.id;
        const checked = checkedId === item.id;
        return (
        <div key={item.id} style={{
          padding: 0,
          overflow: 'hidden',
          borderRadius: 18,
          background: expanded ? 'rgba(255,255,255,.90)' : 'rgba(255,255,255,.74)',
          border: expanded ? '1px solid rgba(14,14,44,.14)' : `1px solid ${T.hairlineSoft}`,
          boxShadow: expanded ? '0 22px 54px rgba(14,14,44,.11), inset 0 1px 0 rgba(255,255,255,.90)' : '0 8px 18px rgba(14,14,44,.035), inset 0 1px 0 rgba(255,255,255,.80)',
          cursor: expanded ? 'default' : 'pointer',
          transition: `box-shadow .32s ${T.spring}, border .24s ${T.ease}, background .24s ${T.ease}`,
        }}>
          <div onClick={() => { setExpandedId(item.id); setSelectedId(item.id); }} style={{
            display: 'grid',
            gridTemplateColumns: isMobile ? '1fr' : expanded ? 'minmax(0, 1.05fr) minmax(230px, .55fr)' : '56px minmax(0, 1fr) auto',
            gap: expanded ? 0 : 13,
            alignItems: 'stretch',
            minHeight: expanded ? 216 : 74,
          }}>
            {expanded ? (
              <>
                <div style={{ padding: isMobile ? 18 : item.recommended ? 22 : 19, display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: 18, background: item.recommended ? 'linear-gradient(135deg, rgba(255,255,255,.92), rgba(245,255,224,.34))' : 'transparent' }}>
                  <div>
                    <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap', marginBottom: 13 }}>
                      {item.recommended && <span style={{ height: 28, padding: '0 11px', borderRadius: 999, background: T.primary, color: T.navy, fontSize: 12, fontWeight: 800, boxShadow: '0 10px 22px rgba(214,255,0,.22)' }}>Nori 推荐</span>}
                      <span style={{ height: 27, padding: '0 10px', borderRadius: 999, background: 'rgba(250,252,254,.82)', border: `1px solid ${T.hairlineSoft}`, color: T.navyLight, fontSize: 11.8, fontWeight: 680 }}>运营计划 {index + 1}</span>
                    </div>
                    <div style={{ color: T.navy, fontSize: isMobile ? 22 : item.recommended ? 28 : 25, lineHeight: 1.16, fontWeight: item.recommended ? 800 : 760, letterSpacing: 0 }}>{item.name}</div>
                    <p style={{ margin: '11px 0 0', color: T.navyMid, fontSize: 13.6, lineHeight: 1.66, maxWidth: 560 }}>{item.position}</p>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(3, minmax(0, 1fr))', gap: 9 }}>
                    {[
                      ['账号名', item.name],
                      ['人设关键词', item.keyword],
                      ['内容支柱', item.pillar],
                      ['签名', item.bio],
                    ].map(([label, value], detailIndex) => (
                      <div key={label} style={{ gridColumn: detailIndex === 3 && !isMobile ? 'span 3' : 'auto', borderRadius: 14, background: 'rgba(250,252,254,.72)', border: `1px solid ${T.hairlineSoft}`, padding: '10px 11px' }}>
                        <div style={{ color: T.navyLight, fontSize: 11.2, fontWeight: 680, marginBottom: 4 }}>{label}</div>
                        <div style={{ color: T.navy, fontSize: 12.7, lineHeight: 1.48, fontWeight: 640 }}>{value}</div>
                      </div>
                    ))}
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
                    <div style={{ color: T.navyLight, fontSize: 12.2, lineHeight: 1.5 }}>推荐原因：{item.why}</div>
                    <button onClick={(e) => { e.stopPropagation(); onOpenDoc(item); }} style={{ ...planningActionButtonStyle('secondary'), height: 36, borderRadius: 13, fontSize: 12.6, justifyContent: 'center' }}>
                      查看完整运营计划
                    </button>
                  </div>
                </div>
                <div style={{ minHeight: isMobile ? 168 : 'auto', background: `linear-gradient(90deg, rgba(14,14,44,.10), rgba(14,14,44,.34)), url(${item.image}) center / cover`, position: 'relative' }}>
                  <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(180deg, rgba(255,255,255,0), rgba(14,14,44,.18))' }} />
                  <button
                    onClick={(e) => { e.stopPropagation(); setCheckedId(item.id); setSelectedId(item.id); }}
                    style={{
                      position: 'absolute',
                      right: 16,
                      top: 16,
                      height: 34,
                      minWidth: 34,
                      padding: checked ? '0 11px' : 0,
                      borderRadius: 999,
                      border: checked ? '1px solid rgba(49,208,170,.24)' : '1px solid rgba(14,14,44,.12)',
                      background: checked ? T.success : 'rgba(255,255,255,.78)',
                      color: checked ? T.white : T.navyLight,
                      display: 'inline-flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: 6,
                      boxShadow: checked ? '0 14px 30px rgba(49,208,170,.22)' : '0 12px 28px rgba(14,14,44,.18)',
                      cursor: 'pointer',
                      fontSize: 12,
                      fontWeight: 780,
                      transition: `transform .24s ${T.spring}, background .2s ${T.ease}, box-shadow .24s ${T.spring}, color .2s ${T.ease}`,
                    }}
                  >
                    <Icon name="check" size={15} stroke={2.2} />
                    {checked && '已选择'}
                  </button>
                </div>
              </>
            ) : (
              <>
                <div style={{ margin: 12, width: 50, height: 50, borderRadius: 16, background: `url(${item.image}) center / cover`, border: `1px solid ${T.hairlineSoft}`, boxShadow: '0 8px 18px rgba(14,14,44,.06)', filter: item.recommended ? 'saturate(1.06)' : 'saturate(.92) brightness(.98)' }} />
                <div style={{ padding: '12px 0', minWidth: 0 }}>
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 5 }}>
                    <span style={{ color: T.navyLight, fontSize: 11.8, fontWeight: 650 }}>运营计划 {index + 1}</span>
                    <span style={{ color: T.navySoft, fontSize: 11 }}>点击展开</span>
                  </div>
                  <div style={{ color: T.navy, fontSize: 15, lineHeight: 1.35, fontWeight: 700, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{item.name}</div>
                </div>
                <button onClick={(e) => { e.stopPropagation(); setExpandedId(item.id); setSelectedId(item.id); }} style={{ margin: '18px 14px 18px 0', height: 34, padding: '0 12px', borderRadius: 12, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.72)', color: T.navyMid, cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 12.2, fontWeight: 650, boxShadow: 'none' }}>
                  展开
                  <Icon name="chevronRight" size={12} />
                </button>
              </>
            )}
          </div>
        </div>
        );
      })}
      </div>
    </AgentCardShell>
  );
};

const PlanningCalendarPreviewCard = ({ calendar = [], onView, onGenerate }) => (
  <AgentCardShell
    label="Agent 内容日历"
    icon="calendar"
    title="第一周内容排期已生成"
    style={{ padding: 14 }}
    bodyStyle={{ fontSize: 12.8 }}
    action={(
      <>
        <button onClick={onView} style={{ ...planningActionButtonStyle('secondary'), height: 34, borderRadius: 12, fontSize: 12.5 }}>
          查看
          <Icon name="expand" size={13} />
        </button>
        <button onClick={onGenerate} style={{ ...planningActionButtonStyle('primary'), height: 34, borderRadius: 12, fontSize: 12.5 }}>
          直接生成
          <Icon name="arrowRight" size={13} />
        </button>
      </>
    )}
  >
    <div style={{
      minHeight: 82,
      borderRadius: 14,
      border: `1px solid ${T.hairlineSoft}`,
      background: 'rgba(250,252,254,.72)',
      display: 'grid',
      gridTemplateColumns: 'repeat(5, minmax(0, 1fr))',
      gap: 6,
      padding: 8,
    }}>
      {['周一', '周二', '周三', '周四', '周五'].map((day, index) => {
        const item = calendar.find(row => row.day === day) || calendar[index] || {};
        const topic = item.topic || '内容选题';
        return (
        <div key={day} style={{
          borderRadius: 10,
          background: index === 0 ? T.irisTint : 'rgba(255,255,255,.74)',
          border: `1px solid ${index === 0 ? 'rgba(75,77,237,.12)' : T.hairlineSoft}`,
          display: 'grid',
          gap: 5,
          alignContent: 'start',
          padding: '8px 8px 7px',
          color: index === 0 ? T.iris : T.navyLight,
        }}>
          <span style={{ fontSize: 11.1, lineHeight: 1, fontWeight: 760 }}>{day}</span>
          <span style={{
            color: T.navyMid,
            fontSize: 10.8,
            lineHeight: 1.34,
            fontWeight: 560,
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}>
            {topic}
          </span>
        </div>
      );})}
    </div>
  </AgentCardShell>
);

const PlanningCalendarModal = ({ open, onClose, children, onGenerate }) => {
  if (!open) return null;
  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      zIndex: 1200,
      background: 'rgba(8,8,18,.34)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 24,
    }}>
      <div style={{
        width: 'min(1180px, calc(100vw - 48px))',
        maxHeight: '88vh',
        overflow: 'hidden',
        borderRadius: 24,
        border: `1px solid ${T.hairlineSoft}`,
        background: T.white,
        boxShadow: '0 34px 90px rgba(14,14,44,.22)',
        display: 'flex',
        flexDirection: 'column',
      }}>
        <div style={{
          height: 58,
          padding: '0 18px',
          borderBottom: `1px solid ${T.hairlineSoft}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 12,
          flexShrink: 0,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, color: T.navy, fontSize: 15, fontWeight: 730 }}>
            <span style={{ width: 30, height: 30, borderRadius: 11, background: T.irisTint, color: T.iris, display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
              <Icon name="calendar" size={15} />
            </span>
            第一周内容日历
          </div>
          <button onClick={onClose} style={iconBtnStyle()}>
            <Icon name="close" size={14} color={T.navyMid} />
          </button>
        </div>
        <div style={{ overflow: 'auto', padding: 16 }}>
          {children}
        </div>
        <div style={{ padding: '0 16px 16px', display: 'flex', justifyContent: 'flex-end', flexShrink: 0 }}>
          <button onClick={onGenerate} style={{ ...planningActionButtonStyle('primary') }}>
            开始生成第一篇
            <Icon name="arrowRight" size={14} />
          </button>
        </div>
      </div>
    </div>
  );
};

const PlanningCalendarBoard = ({ calendar, setCalendar, weekStart, setWeekStart, isMobile, wide = false }) => {
  const [activeEvent, setActiveEvent] = React.useState(null);
  const [draggingId, setDraggingId] = React.useState(null);
  const times = ['09:00', '11:30', '14:00', '16:30', '20:00'];
  const dayDates = ['05/18', '05/19', '05/20', '05/21', '05/22', '05/23', '05/24'];
  const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'];
  const tones = [
    { bg: 'rgba(239,239,253,.76)', border: 'rgba(75,77,237,.16)', fg: T.iris },
    { bg: 'rgba(224,250,244,.76)', border: 'rgba(49,208,170,.16)', fg: T.success },
    { bg: 'rgba(245,255,224,.86)', border: 'rgba(214,255,0,.28)', fg: '#6e8400' },
    { bg: 'rgba(253,245,245,.86)', border: 'rgba(243,219,218,.95)', fg: T.navyMid },
  ];
  const events = calendar.map((item, index) => {
    const dayIndex = Math.max(0, days.indexOf(item.day));
    const timeIndex = Math.max(0, times.indexOf(item.time || times[index % times.length]));
    return {
      ...item,
      id: item.id || `calendar-${index}`,
      date: dayDates[dayIndex] || dayDates[index] || '05/25',
      time: item.time || times[index % times.length],
      dayIndex,
      timeIndex,
      top: 72 + timeIndex * 84,
      tone: tones[index % tones.length],
    };
  });
  const addCalendarItem = () => {
    const id = `calendar-new-${Date.now()}`;
    setCalendar(list => [{ id, day: '周一', time: '11:30', type: '图文', topic: '新增内容选题，点击后可修改', ref: '@参考账号' }, ...list]);
    setActiveEvent(id);
  };
  const moveEventToDay = (eventId, nextDay) => {
    setCalendar(list => list.map((row, index) => ((row.id || `calendar-${index}`) === eventId ? { ...row, id: eventId, day: nextDay } : { ...row, id: row.id || `calendar-${index}` })));
  };

  if (isMobile) {
    return (
      <AgentCardShell label="Agent 内容日历" icon="calendar" title="第一周内容排期" style={{ padding: 16, width: wide ? '100%' : AGENT_CARD_WIDTH }}>
        <div style={{ display: 'grid', gap: 8, marginBottom: 12 }}>
          <div style={{ color: T.navy, fontSize: 17, fontWeight: 730 }}>2026 年 5 月</div>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <input type="date" value={weekStart} onChange={e => setWeekStart(e.target.value)} style={{ height: 38, borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: T.white, color: T.navyMid, padding: '0 10px', fontFamily: T.fontSans, fontSize: 12.5 }} />
            <button onClick={addCalendarItem} style={{ ...pillButtonStyle(true), height: 38, borderRadius: 13, fontSize: 13 }}>
              <Icon name="plus" size={14} />
              新增内容
            </button>
          </div>
        </div>
        <div style={{ display: 'grid', gap: 9 }}>
          {events.map((item, index) => (
            <div key={`${item.day}-${index}`} onClick={() => setActiveEvent(activeEvent === index ? null : index)} style={{ borderRadius: 16, border: `1px solid ${item.tone.border}`, background: item.tone.bg, padding: 12, cursor: 'pointer' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8, alignItems: 'center' }}>
                <div style={{ color: item.tone.fg, fontSize: 11.8, fontWeight: 760 }}>{item.day} · {item.type}</div>
                <div style={{ color: T.navyLight, fontSize: 11.2, fontFamily: T.fontMono }}>{item.time}</div>
              </div>
              <textarea value={item.topic} rows={2} onChange={e => setCalendar(list => list.map((row, i) => i === index ? { ...row, topic: e.target.value } : row))} style={{ marginTop: 7, width: '100%', border: 'none', background: 'transparent', color: T.navy, fontSize: 13, outline: 'none', resize: 'vertical', fontFamily: T.fontSans, lineHeight: 1.52 }} />
              <div style={{ color: T.navyLight, fontSize: 11.2 }}>参考：{item.ref}</div>
            </div>
          ))}
        </div>
      </AgentCardShell>
    );
  }

  return (
    <AgentCardShell label="Agent 内容日历" icon="calendar" title="第一周内容排期" style={{ padding: 0, overflow: 'hidden', width: wide ? '100%' : AGENT_CARD_WIDTH }} bodyStyle={{ fontSize: 13 }}>
      <div style={{ height: 60, padding: '0 18px', borderBottom: `1px solid ${T.hairlineSoft}`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
        <div style={{ color: T.navy, fontSize: 18, fontWeight: 740 }}>2026 年 5 月</div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <input type="date" value={weekStart} onChange={e => setWeekStart(e.target.value)} style={{ height: 38, borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: T.white, color: T.navyMid, padding: '0 10px', fontFamily: T.fontSans, fontSize: 12.5 }} />
          <button onClick={addCalendarItem} style={{ ...pillButtonStyle(true), height: 38, borderRadius: 13 }}>
            <Icon name="plus" size={15} />
            新增内容
          </button>
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: wide ? '68px repeat(7, minmax(105px, 1fr))' : '74px repeat(7, minmax(130px, 1fr))', minHeight: wide ? 492 : 518, overflowX: 'auto' }}>
        <div style={{ borderRight: `1px solid ${T.hairlineSoft}`, background: 'rgba(250,252,254,.58)' }}>
          <div style={{ height: 70, borderBottom: `1px solid ${T.hairlineSoft}` }} />
          {times.map(time => <div key={time} style={{ height: 84, borderBottom: `1px solid ${T.hairlineSoft}`, padding: '14px 12px', color: T.navyLight, fontSize: 12, fontFamily: T.fontMono }}>{time}</div>)}
        </div>
        {days.map((day, index) => (
          <div
            key={day}
            onDragOver={e => e.preventDefault()}
            onDrop={e => {
              e.preventDefault();
              const eventId = e.dataTransfer.getData('text/plain') || draggingId;
              if (eventId) moveEventToDay(eventId, day);
              setDraggingId(null);
            }}
            style={{ minWidth: 130, borderRight: index === days.length - 1 ? 'none' : `1px solid ${T.hairlineSoft}`, position: 'relative', background: draggingId ? 'rgba(250,252,254,.42)' : 'transparent' }}
          >
            <div style={{ height: 70, borderBottom: `1px solid ${T.hairlineSoft}`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', background: index === 3 ? 'rgba(239,239,253,.28)' : 'transparent' }}>
              <div style={{ color: index === 3 ? T.iris : T.navy, fontSize: 13.5, fontWeight: 740 }}>{day}</div>
              <div style={{ marginTop: 4, color: T.navyLight, fontSize: 11.2, fontFamily: T.fontMono }}>{dayDates[index]}</div>
            </div>
            {times.map(time => <div key={time} style={{ height: 84, borderBottom: `1px solid ${T.hairlineSoft}`, background: index === 3 ? 'rgba(239,239,253,.12)' : 'transparent' }} />)}
            {events.filter(event => event.day === day).map(event => (
              <div
                key={event.id}
                draggable
                onDragStart={e => {
                  setDraggingId(event.id);
                  e.dataTransfer.setData('text/plain', event.id);
                  e.dataTransfer.effectAllowed = 'move';
                }}
                onDragEnd={() => setDraggingId(null)}
                onClick={() => setActiveEvent(activeEvent === event.id ? null : event.id)}
                style={{
                  position: 'absolute',
                  top: event.top,
                  left: 12,
                  right: 12,
                  borderRadius: 17,
                  border: `1px solid ${event.tone.border}`,
                  background: event.tone.bg,
                  padding: 12,
                  boxShadow: activeEvent === event.id ? '0 18px 34px rgba(14,14,44,.10)' : '0 14px 28px rgba(14,14,44,.055)',
                  cursor: 'grab',
                  zIndex: activeEvent === event.id ? 4 : 2,
                  opacity: draggingId === event.id ? .58 : 1,
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: 8, marginBottom: 7 }}>
                  <span style={{ color: event.tone.fg, fontSize: 11.8, fontWeight: 780 }}>{event.type}</span>
                  <span style={{ color: T.navyLight, fontSize: 11.2, fontFamily: T.fontMono }}>{event.time}</span>
                </div>
                <textarea value={event.topic} rows={3} onChange={e => setCalendar(list => list.map((row, i) => (row.id || `calendar-${i}`) === event.id ? { ...row, id: event.id, topic: e.target.value } : row))} style={{ width: '100%', border: 'none', background: 'transparent', color: T.navy, fontSize: 13, lineHeight: 1.48, fontWeight: 650, resize: 'vertical', outline: 'none', fontFamily: T.fontSans }} />
                <div style={{ color: T.navyLight, fontSize: 11.2, lineHeight: 1.4 }}>{event.ref}</div>
                {activeEvent === event.id && null}
              </div>
            ))}
          </div>
        ))}
      </div>
    </AgentCardShell>
  );
};

const PlanningDocPreview = ({ diagnosisText, persona, pillars, calendar, activeSection, setActiveSection, mobile }) => {
  const planPersona = persona || {};
  const sections = {
    定位: [
      ['账号定位', diagnosisText.position],
      ['目标受众', diagnosisText.audience],
      ['差异化卖点', diagnosisText.selling],
    ],
    人设: [
      ['账号名', planPersona.names?.[0] || planPersona.name || '巷口暖胃小馆'],
      ['签名', planPersona.bio || '每天认真做一碗有烟火气的家常饭。'],
      ['关键词', Array.isArray(planPersona.keywords) ? planPersona.keywords.join('、') : planPersona.keywords],
      ['语气', Array.isArray(planPersona.phrases) ? planPersona.phrases.join(' / ') : planPersona.tone],
    ],
    对标: (planPersona.bloggers || ['@本地吃喝指南', '@街角小店日记', '@城市午餐研究所']).map((item, index) => [`对标 ${index + 1}`, item]),
    选题库: pillars.map((item, index) => [`选题 ${index + 1}`, item]),
    发布节奏: calendar.map(item => [item.day, `${item.type} · ${item.topic}`]),
    数据目标: [
      ['7 天目标', '验证 1 套稳定选题结构'],
      ['核心指标', '封面点击率、完读率、收藏率、净涨粉'],
      ['复盘节奏', '发布后 1h / 3h / 12h / 24h 必看'],
    ],
  };
  const current = sections[activeSection] || sections.定位;
  return (
    <aside style={{
      width: mobile ? '100%' : 390,
      flexShrink: 0,
      borderLeft: mobile ? 'none' : `1px solid ${T.hairlineSoft}`,
      borderTop: mobile ? `1px solid ${T.hairlineSoft}` : 'none',
      background: 'rgba(255,255,255,.64)',
      padding: mobile ? '16px 16px 22px' : '22px 22px 24px',
      overflowY: 'auto',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12, marginBottom: 16 }}>
        <div>
          <div style={{ color: T.navyLight, fontSize: 12.2, fontWeight: 720, marginBottom: 5 }}>文档预览</div>
          <div style={{ color: T.navy, fontSize: 18, fontWeight: 730 }}>账号定位 + 运营计划 + 内容排期</div>
        </div>
        <span style={{ width: 34, height: 34, borderRadius: 13, background: T.primaryTint, color: T.iris, display: 'inline-flex', alignItems: 'center', justifyContent: 'center' }}>
          <Icon name="document" size={16} />
        </span>
      </div>
      <div style={{ display: 'flex', gap: 7, flexWrap: 'wrap', marginBottom: 16 }}>
        {Object.keys(sections).map(section => {
          const active = activeSection === section;
          return (
            <button key={section} onClick={() => setActiveSection(section)} style={{
              height: 30,
              padding: '0 10px',
              borderRadius: 999,
              border: `1px solid ${active ? 'rgba(75,77,237,.24)' : T.hairlineSoft}`,
              background: active ? T.irisTint : 'rgba(255,255,255,.74)',
              color: active ? T.iris : T.navyMid,
              cursor: 'pointer',
              fontSize: 12,
              fontWeight: 650,
            }}>
              {section}
            </button>
          );
        })}
      </div>
      <div style={{
        borderRadius: 20,
        border: `1px solid ${T.hairlineSoft}`,
        background: 'rgba(250,252,254,.82)',
        padding: 18,
        display: 'grid',
        gap: 16,
      }}>
        {current.map(([label, value]) => (
          <div key={label}>
            <div style={{ color: T.navyLight, fontSize: 12, fontWeight: 720, marginBottom: 6 }}>{label}</div>
            <div style={{ color: T.navy, fontSize: 13.8, lineHeight: 1.68, fontWeight: 520, whiteSpace: 'pre-wrap' }}>{value}</div>
          </div>
        ))}
      </div>
    </aside>
  );
};

const loadPlanDraft = () => {
  try {
    const raw = window.localStorage?.getItem(PLAN_STORAGE_KEY);
    if (!raw) return null;
    return JSON.parse(raw);
  } catch {
    return null;
  }
};

const clearPlanDraftStorage = () => {
  try {
    window.localStorage?.removeItem(PLAN_STORAGE_KEY);
  } catch {
    // Some file:// contexts can reject storage access; navigation should still continue.
  }
};

const AccountPlanningPagePolishedV2 = ({ onBackHome, onNewChat, onOpenAssets, onOpenSkills, onOpenInsights, onComplete }) => {
  const { isMobile } = useViewport();
  const savedDraft = null;
  const [step, setStep] = React.useState(1);
  const [modalType, setModalType] = React.useState(null);
  const [attachments, setAttachments] = React.useState([]);
  const [rawInput, setRawInput] = React.useState('');
  const [sentIntro, setSentIntro] = React.useState(false);
  const [goalSelections, setGoalSelections] = React.useState([]);
  const [platformSelections, setPlatformSelections] = React.useState([]);
  const [diagnosisText, setDiagnosisText] = React.useState({
    position: '做附近人愿意收藏的烟火气小馆账号。你的优势不是大品牌感，而是稳定、真实、离用户很近。内容要让人觉得下班就能去。',
    audience: '23-38 岁附近上班族、情侣和周末约饭人群，关心味道稳定、价格舒服、距离方便。',
    directions: '招牌菜故事：让用户记住你和别的店不一样的地方。\n真实到店场景：降低第一次到店的心理成本。\n本地生活攻略：把餐厅内容变成可收藏的信息。',
    benchmarks: '@本地吃喝指南：标题清楚，适合学习选题包装。\n@街角小店日记：擅长把小店日常拍得有人情味。\n@城市午餐研究所：午餐场景切得细，容易引流到店。',
    selling: '稳定家常味 + 店主真实感 + 离附近人生活很近。',
  });
  const [persona, setPersona] = React.useState({
    name: '巷口暖胃小馆',
    bio: '每天认真做一碗有烟火气的家常饭，给附近人一个不用纠结的吃饭选择。',
    keywords: '亲切但不油腻、懂本地生活、真实主理人、稳定好吃',
    tone: '今天这碗饭，适合下班后来一口。 / 第一次来不知道点什么，先看这一篇。',
    cover: '暖色自然光 + 菜品近景 + 大留白标题',
  });
  const [pillars, setPillars] = React.useState(['招牌菜故事', '午餐不踩雷', '老板的一天', '真实顾客反馈', '周末朋友局菜单']);
  const [calendar, setCalendar] = React.useState([
    { day: '周一', type: '探店图文', topic: '第一次来店里，先点这 3 道招牌菜', ref: '@本地吃喝指南' },
    { day: '周二', type: '短视频', topic: '后厨备菜 30 秒，看看一碗饭怎么被认真做好', ref: '@街角小店日记' },
    { day: '周三', type: '图文', topic: '附近上班族午餐不踩雷菜单', ref: '@城市午餐研究所' },
    { day: '周四', type: '长文', topic: '一家小店怎么把回头客留住', ref: '@主理人手记' },
    { day: '周五', type: '短视频', topic: '顾客最常问的 5 个问题', ref: '@真实探店' },
    { day: '周六', type: '图文', topic: '周末带朋友来吃，怎么点更划算', ref: '@本地生活家' },
    { day: '周日', type: '复盘', topic: '这周最受欢迎的一道菜', ref: '@小店经营笔记' },
  ]);
  const [weekStart, setWeekStart] = React.useState('2026-05-18');
  const [showWeekPicker, setShowWeekPicker] = React.useState(false);
  const [reportVariant, setReportVariant] = React.useState(0);
  const [copied, setCopied] = React.useState('');
  const [liked, setLiked] = React.useState(false);
  const [toast, setToast] = React.useState('');
  const [stage, setStage] = React.useState(0);
  const [followUps, setFollowUps] = React.useState([]);
  const [activePreviewSection, setActivePreviewSection] = React.useState('定位');
  const [strategyDoc, setStrategyDoc] = React.useState(null);
  const [pendingFiles, setPendingFiles] = React.useState([]);
  const [quickLink, setQuickLink] = React.useState('');
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
    { label: '调研同赛道头部账号', text: '我先看了本地饭店、探店和社区午餐账号的封面、标题和评论区高频问题。' },
    { label: '提取用户痛点', text: '用户最怕网红店踩雷、排队久、价格不透明，所以内容必须先给可执行建议。' },
    { label: '寻找差异化机会', text: '你的机会不是泛探店，而是把「附近人真实复吃」和「主理人认真饭」讲稳定。' },
  ];

  const steps = [
    { id: 1, label: '输入线索' },
    { id: 2, label: '账号定位' },
    { id: 3, label: '运营计划' },
    { id: 4, label: '内容排期' },
  ];

  const reports = [
    {
      names: ['巷口暖胃小馆', '附近人的家常饭', '下班来吃一口'],
      keywords: ['亲切但不油腻', '懂本地生活', '真实主理人', '稳定好吃'],
      phrases: ['今天这碗饭，适合下班后来一口。', '第一次来不知道点什么，先看这一篇。', '不是网红店，但想把每顿饭认真做好。'],
      bio: '每天认真做一碗有烟火气的家常饭，给附近人一个不用纠结的吃饭选择。',
      pillars: ['招牌菜故事', '午餐不踩雷', '老板的一天', '真实顾客反馈', '周末朋友局菜单'],
      bloggers: ['@本地吃喝指南', '@街角小店日记', '@城市午餐研究所'],
      covers: ['暖色自然光 + 菜品近景 + 大留白标题', '店门口 / 餐桌 / 后厨细节三图拼贴', '人物手部入镜，弱化摆拍感'],
    },
    {
      names: ['今天吃暖胃饭', '社区饭点研究所', '小馆认真饭'],
      keywords: ['靠谱推荐', '邻里感', '价格友好', '下班治愈'],
      phrases: ['这不是探店广告，是附近人真的会复吃的菜单。', '如果你只有 30 分钟吃午饭，可以这么点。', '小店最动人的地方，是每天都稳定。'],
      bio: '记录一家社区小馆的日常菜单、真实客人和让人安心的家常味。',
      pillars: ['30 分钟午餐方案', '复吃菜单', '小店幕后', '本周新品', '附近生活路线'],
      bloggers: ['@通勤午餐地图', '@小店观察员', '@附近生活手册'],
      covers: ['浅色桌面 + 俯拍套餐 + 手写感标题', '老板出镜 + 菜品特写 + 真实环境', '低饱和暖色，强调干净和可信'],
    },
  ];
  const report = reports[reportVariant % reports.length];
  const reportDraft = React.useMemo(() => ({
    names: [...report.names],
    keywords: [...report.keywords],
    phrases: [...report.phrases],
    bio: report.bio,
    pillars: [...report.pillars],
    bloggers: [...report.bloggers],
    covers: [...report.covers],
  }), [reportVariant]);

  const [activeReport, setActiveReport] = React.useState(reportDraft);
  const [audienceTags, setAudienceTags] = React.useState(['25-38 岁', '附近上班族', '情侣约饭', '周末聚餐']);
  const [appearanceTags, setAppearanceTags] = React.useState(['真实主理人', '后厨日常', '菜品近景']);
  const [marketTags, setMarketTags] = React.useState(['本地生活', '社区周边', '小红书搜索']);

  React.useEffect(() => {
    revealTimersRef.current.forEach(window.clearTimeout);
    setStage(0);
    if (step === 2) setAnalysisComplete(false);
    const timers = [
      window.setTimeout(() => setStage(1), 180),
      window.setTimeout(() => setStage(2), 520),
      window.setTimeout(() => setStage(3), 900),
    ];
    revealTimersRef.current = timers;
    return () => timers.forEach(window.clearTimeout);
  }, [step]);

  const scrollToBottom = React.useCallback((behavior = 'smooth', force = false) => {
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
    const t = window.setTimeout(() => scrollToBottom('smooth', true), 80);
    return () => window.clearTimeout(t);
  }, [step, sentIntro, goalSelections.length, platformSelections.length, followUps.length, attachments.length, scrollToBottom]);

  React.useEffect(() => {
    const node = scrollRef.current;
    if (!node || !contentRef.current) return undefined;
    const onScroll = () => {
      shouldFollowScrollRef.current = isNearScrollBottom(node, 140);
    };
    node.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
    const observer = new MutationObserver(() => {
      scrollToBottom('auto');
    });
    const resizeObserver = new ResizeObserver(() => {
      scrollToBottom('auto');
    });
    observer.observe(contentRef.current, { childList: true, subtree: true, characterData: true });
    resizeObserver.observe(contentRef.current);
    return () => {
      node.removeEventListener('scroll', onScroll);
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
      activeReport: activeReport,
      pillars,
      calendar,
      weekStart,
      reportVariant,
      followUps,
      quickLink,
    };
    window.localStorage?.setItem(PLAN_STORAGE_KEY, JSON.stringify(payload));
    setToast('已暂存');
    window.setTimeout(() => setToast(''), 1200);
    onBackHome();
  };

  const copyPlan = (text) => {
    setCopied(text);
    navigator.clipboard?.writeText(text).catch(() => {});
    window.setTimeout(() => setCopied(''), 1200);
  };

  const downloadPlan = () => {
    const blob = new Blob([buildPlanExportText({
      diagnosisText,
      persona: activeReport || persona,
      pillars,
      calendar,
    })], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'nori-account-plan.md';
    a.click();
    URL.revokeObjectURL(url);
    setToast('已下载文档');
    window.setTimeout(() => setToast(''), 1200);
  };

  const completePlan = () => {
    const finalPersona = activeReport || persona;
    onComplete({
      topic: `小红书图文：${calendar[0]?.topic || '账号规划'}`,
      platform: platformSelections[0] || '小红书',
      positioning: diagnosisText.position,
      persona: {
        name: finalPersona.names ? finalPersona.names[0] : finalPersona.name,
        bio: finalPersona.bio,
        keywords: finalPersona.keywords?.join ? finalPersona.keywords.join('、') : finalPersona.keywords,
        tone: finalPersona.phrases ? finalPersona.phrases.join(' / ') : finalPersona.tone,
        cover: finalPersona.covers ? finalPersona.covers[0] : finalPersona.cover,
      },
      pillars,
    });
    clearPlanDraftStorage();
  };

  const startFirstContent = () => {
    const finalPersona = activeReport || persona;
    onComplete({
      topic: `小红书图文：${calendar[0]?.topic || '账号规划'}`,
      platform: platformSelections[0] || '小红书',
      positioning: diagnosisText.position,
      persona: {
        name: finalPersona.names ? finalPersona.names[0] : finalPersona.name,
        bio: finalPersona.bio,
        keywords: finalPersona.keywords?.join ? finalPersona.keywords.join('、') : finalPersona.keywords,
        tone: finalPersona.phrases ? finalPersona.phrases.join(' / ') : finalPersona.tone,
        cover: finalPersona.covers ? finalPersona.covers[0] : finalPersona.cover,
      },
      pillars,
      calendar,
    });
    clearPlanDraftStorage();
  };

  const toggleMulti = (value, setter) => {
    setter(prev => prev.includes(value) ? prev.filter(item => item !== value) : [...prev, value]);
  };

  const restartRevealSequence = React.useCallback(() => {
    revealTimersRef.current.forEach(window.clearTimeout);
    setStage(0);
    const timers = [
      window.setTimeout(() => setStage(1), 220),
      window.setTimeout(() => setStage(2), 680),
      window.setTimeout(() => setStage(3), 1180),
    ];
    revealTimersRef.current = timers;
  }, []);

  const contentProfiles = [
    { title: '账号定位', value: diagnosisText.position },
    { title: '目标受众', value: diagnosisText.audience },
    { title: '内容方向', value: diagnosisText.directions },
    { title: '对标账号', value: diagnosisText.benchmarks },
    { title: '差异化卖点', value: diagnosisText.selling },
  ];

  const sendPlanningMessage = (text) => {
    const quickLinkText = !sentIntro && /^https?:\/\//i.test(quickLink.trim()) ? quickLink.trim() : '';
    if (!text.trim() && pendingFiles.length === 0 && !quickLinkText) return;
    const now = Date.now();
    const selectedFiles = pendingFiles.map(item => item.file || item);
    const fileAttachments = selectedFiles.map(file => ({
      type: file.type?.startsWith('image/') ? 'image' : file.type?.startsWith('video/') ? 'video' : 'file',
      label: file.name,
      value: `${file.name} · ${Math.max(1, Math.round(file.size / 1024))}KB`,
      preview: file.type?.startsWith('image/') ? URL.createObjectURL(file) : null,
    }));
    if (fileAttachments.length) {
      setAttachments(list => [...list, ...fileAttachments]);
      pendingFiles.forEach(item => item.preview && URL.revokeObjectURL(item.preview));
      setPendingFiles([]);
    }
    const linkAttachment = quickLinkText ? { type: 'link', label: '店铺链接', value: quickLinkText, thumb: PLANNING_ASSET_THUMBS[2] } : null;
    if (linkAttachment) {
      setAttachments(list => list.some(item => item.value === quickLinkText) ? list : [...list, linkAttachment]);
    }
    const userText = text.trim() || quickLinkText || `已上传 ${fileAttachments.length} 个文件`;
    if (!sentIntro) {
      setRawInput(userText);
      setAssetConfirmed(false);
      setSentIntro(true);
      restartRevealSequence();
      return;
    }
    setFollowUps(list => [
      ...list,
      { id: now, from: 'user', text: fileAttachments.length ? `${userText}\n${fileAttachments.map(item => item.label).join('、')}` : userText },
      { id: now + 1, from: 'nori', text: step < 5 ? '收到，我会把这条补充进账号规划里。你也可以继续发链接、截图或直接描述。' : '收到，我会按这个方向更新右侧文档预览里的内容。' },
    ]);
  };

  const pasteQuickLink = () => {
    const link = quickLink.trim() || 'https://www.meituan.com/shop/上海暖胃小馆';
    setQuickLink(link);
    setRawInput(link);
    setAttachments(list => list.some(item => item.value === link) ? list : [...list, { type: 'link', label: '美团店铺链接', value: link, thumb: PLANNING_ASSET_THUMBS[2] }]);
  };

  return (
    <div style={{
      height: '100%',
      minHeight: 0,
      width: '100%',
      display: 'flex',
      flexDirection: 'column',
      background: 'linear-gradient(180deg, #FAFCFE 0%, #ECF1F4 100%)',
      color: T.navy,
      overflow: 'hidden',
      fontFamily: T.fontSans,
    }}>
      <header style={{
        height: isMobile ? 'auto' : 56,
        padding: isMobile ? '12px 16px' : '0 24px',
        display: 'flex',
        alignItems: isMobile ? 'stretch' : 'center',
        justifyContent: 'space-between',
        gap: 14,
        flexDirection: isMobile ? 'column' : 'row',
        borderBottom: `1px solid ${T.hairlineSoft}`,
        background: 'rgba(250,252,254,.78)',
        backdropFilter: 'blur(18px) saturate(1.16)',
        flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0 }}>
          <button onClick={onBackHome} style={iconBtnStyle()}>
            <Icon name="arrowLeft" size={16} color={T.navyMid} />
          </button>
          <div style={{ minWidth: 0 }}>
            <div style={{ fontSize: 13.5, fontWeight: 670, color: T.navy }}>账号规划</div>
          </div>
        </div>
        <div />
      </header>

      <div style={{ flex: 1, minHeight: 0, display: 'flex', overflow: 'hidden' }}>
        <main style={{ flex: 1, minWidth: 0, display: 'flex', flexDirection: 'column' }}>
          <div ref={scrollRef} style={{ flex: 1, minHeight: 0, overflowY: 'auto', padding: isMobile ? '22px 0 20px' : '28px 0 24px' }}>
            <div ref={contentRef} style={{
              maxWidth: chatMaxWidth,
              margin: '0 auto',
              padding: isMobile ? '0 16px' : '0 30px',
              display: 'flex',
              flexDirection: 'column',
              gap: 22,
            }}>
              {toast && (
                <div style={{
                  alignSelf: 'flex-start',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 8,
                  padding: '9px 13px',
                  borderRadius: 999,
                  background: 'rgba(255,255,255,.82)',
                  border: `1px solid ${T.hairlineSoft}`,
                  boxShadow: '0 10px 26px rgba(14,14,44,.06)',
                  color: T.navyMid,
                  fontSize: 12.5,
                  fontWeight: 650,
                }}>
                  <Icon name="check" size={13} /> {toast}
                </div>
              )}

              <PlanningReveal show delay={0}>
                <PlanningPlainReply>
                  <p style={{ margin: '0 0 8px', color: T.navy, fontSize: 14.1, lineHeight: 1.62, fontWeight: 650 }}>我是 Nori，可以帮你交付一份「账号定位 + 运营计划 + 内容排期」。</p>
                  <p style={{ margin: 0 }}>你可以发主页链接、竞品链接、截图、菜单 / 产品文件，也可以直接用一句话描述你想做什么。</p>
                </PlanningPlainReply>
              </PlanningReveal>

              {!sentIntro && (
                <PlanningReveal show delay={120}>
                  <PlanningStartPanel
                    quickLink={quickLink}
                    setQuickLink={setQuickLink}
                    onUploadImage={() => fileInputRef.current?.click()}
                    onUploadDoc={() => fileInputRef.current?.click()}
                    onPasteLink={pasteQuickLink}
                  />
                </PlanningReveal>
              )}

              {attachments.length > 0 && !sentIntro && (
                <PlanningReveal show delay={200}>
                  <PlanningUploadedAssetStrip attachments={attachments} onAddMore={() => fileInputRef.current?.click()} />
                </PlanningReveal>
              )}

              {sentIntro && (
                <PlanningReveal show delay={80}>
                  <Bubble from="user">
                    {rawInput || attachments.map(item => item.label || item.value || item.type).join('、') || '我已经提供了一些账号线索'}
                  </Bubble>
                </PlanningReveal>
              )}

              {sentIntro && step === 1 && (
                <PlanningReveal show delay={100}>
                  <AgentStepSequence
                    resetKey="planning-intro-response"
                    parseMessages={['正在查看你提供的资料', '解析中', '正在提炼店铺线索']}
                    reply={(
                      <div style={{ display: 'grid', gap: 8 }}>
                        <div style={{ color: T.navy, fontSize: 14.1, fontWeight: 650 }}>我先看到了你的店铺链接、图片和评价，这些已经足够让我开始判断你适合什么样的账号。</div>
                        <div style={{ color: T.navyMid, fontSize: 12.9, lineHeight: 1.72 }}>我会先做竞品与行业分析，再给你账号定位，避免和同赛道的内容长得太像。我需要先知道两个问题。</div>
                      </div>
                    )}
                    card={(
                      <>
                        <PlanningUploadedAssetStrip attachments={attachments} onAddMore={() => fileInputRef.current?.click()} onConfirm={() => setAssetConfirmed(true)} />
                        {assetConfirmed && (
                          <>
                            <PlanningPlainReply>了解了你的品牌 / 个人资产，还有两个问题需要提前确认。</PlanningPlainReply>
                            <AgentCardShell
                              label="Agent 偏好确认"
                              icon="target"
                              title="先把两个关键问题说清楚"
                              action={(
                                <button onClick={() => setStep(2)} disabled={!canAdvanceStep1} style={{ ...planningActionButtonStyle(canAdvanceStep1 ? 'primary' : 'secondary'), opacity: canAdvanceStep1 ? 1 : .56, cursor: canAdvanceStep1 ? 'pointer' : 'not-allowed' }}>
                                  下一步
                                  <Icon name="arrowRight" size={14} />
                                </button>
                              )}
                            >
                              <div style={{ display: 'grid', gap: 16 }}>
                                <div>
                                  <div style={{ color: T.navy, fontSize: 13.6, fontWeight: 700, marginBottom: 8 }}>最想用社媒账号做什么？</div>
                                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                                    {['引流到店', '品牌曝光', '线上卖货', '积累口碑'].map(option => (
                                      <AgentChoice key={option} active={goalSelections.includes(option)} multiple onClick={() => toggleMulti(option, setGoalSelections)}>
                                        {option}
                                      </AgentChoice>
                                    ))}
                                  </div>
                                </div>
                                <div>
                                  <div style={{ color: T.navy, fontSize: 13.6, fontWeight: 700, marginBottom: 8 }}>最想在哪个平台做？</div>
                                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                                    {['小红书', '抖音', '视频号', '公众号'].map(option => (
                                      <AgentChoice key={option} active={platformSelections.includes(option)} multiple onClick={() => toggleMulti(option, setPlatformSelections)}>
                                        {option}
                                      </AgentChoice>
                                    ))}
                                  </div>
                                </div>
                              </div>
                            </AgentCardShell>
                          </>
                        )}
                      </>
                    )}
                  />
                </PlanningReveal>
              )}

              {step >= 2 && (
                <PlanningReveal show delay={100}>
                  <PlanningUserSummary>{`目标：${goalSelections.join('、') || '待确认'}\n平台：${platformSelections.join('、') || '待确认'}`}</PlanningUserSummary>
                </PlanningReveal>
              )}

              {step >= 2 && !analysisComplete && (
                <PlanningReveal show delay={200}>
                  <AgentStepSequence
                    resetKey="planning-position-analysis"
                    parseMessages={['正在对照同赛道账号', '解析中', '正在提炼差异化机会']}
                    reply="我正在结合你的资料与同赛道内容做对照，先找出用户真正会收藏、会到店的理由，再确定定位。"
                    card={(
                      <PlanningResearchFlow
                        bullets={analysisBullets}
                        conclusion="建议把内容定位在「附近人真实复吃 + 主理人认真饭」，先建立信任，再放大到到店决策。"
                        isMobile={isMobile}
                        onComplete={() => setAnalysisComplete(true)}
                        showThinking={false}
                      />
                    )}
                  />
                </PlanningReveal>
              )}

              {step >= 2 && analysisComplete && (
                <PlanningReveal show delay={120}>
                  <PlanningPlainReply>下面是我整理出的账号定位。它会同步到「我的 · 账号定位」，并用于后续生成内容。</PlanningPlainReply>
                  <PlanningSkeletonMerge
                    diagnosisText={diagnosisText}
                    setDiagnosisText={setDiagnosisText}
                    audienceTags={audienceTags}
                    setAudienceTags={setAudienceTags}
                    appearanceTags={appearanceTags}
                    setAppearanceTags={setAppearanceTags}
                    marketTags={marketTags}
                    setMarketTags={setMarketTags}
                    pillars={pillars}
                    setPillars={setPillars}
                    isMobile={isMobile}
                    action={(
                      <button onClick={() => setStep(3)} style={{ ...planningActionButtonStyle('primary') }}>
                        继续生成运营计划
                        <Icon name="arrowRight" size={14} />
                      </button>
                    )}
                  />
                </PlanningReveal>
              )}

              {step >= 3 && (
                <PlanningReveal show delay={120}>
                  <AgentStepSequence
                    resetKey="planning-strategy"
                    parseMessages={['正在生成你的运营计划', '解析中', '正在比较三套账号打法']}
                    parseConclusion="已生成三套运营计划"
                    reply="这是你的运营计划，我更推荐第一套哦。"
                    card={(
                      <PlanningStrategyCards
                        isMobile={isMobile}
                        activeReport={activeReport}
                        pillars={pillars}
                        onOpenDoc={setStrategyDoc}
                        onConfirm={() => setStep(4)}
                      />
                    )}
                  />
                </PlanningReveal>
              )}

              {step >= 4 && (
                <PlanningReveal show delay={120}>
                  <AgentStepSequence
                    resetKey="planning-calendar"
                    parseMessages={['正在生成你的内容日历', '解析中', '正在整理一周排期']}
                    parseConclusion="正在整理一周排期"
                    reply="这是你第一周的内容排期。这份内容排期会同步到「我的 · 内容日历」，确认后可以直接开始生成第一篇。"
                    card={(
                      <PlanningCalendarPreviewCard
                        calendar={calendar}
                        onView={() => setCalendarModalOpen(true)}
                        onGenerate={startFirstContent}
                      />
                    )}
                  />
                </PlanningReveal>
              )}

              {followUps.map(item => item.from === 'user' ? (
                <PlanningReveal key={item.id} show delay={60}>
                  <Bubble from="user">{item.text}</Bubble>
                </PlanningReveal>
              ) : (
                <PlanningReveal key={item.id} show delay={140}>
                  <PlanningPlainReply>{item.text}</PlanningPlainReply>
                </PlanningReveal>
              ))}

              <div ref={endRef} style={{ height: 1 }} />
            </div>
          </div>

          <PlanningCalendarModal
            open={calendarModalOpen}
            onClose={() => setCalendarModalOpen(false)}
            onGenerate={startFirstContent}
          >
            <PlanningCalendarBoard
              calendar={calendar}
              setCalendar={setCalendar}
              weekStart={weekStart}
              setWeekStart={setWeekStart}
              isMobile={isMobile}
              wide
            />
          </PlanningCalendarModal>

          <div style={{
            padding: isMobile ? '8px 16px 14px' : '8px 24px 16px',
            background: 'linear-gradient(to top, rgba(250,252,254,.98) 62%, rgba(250,252,254,0))',
            flexShrink: 0,
          }}>
            <div style={{ maxWidth: chatMaxWidth, margin: '0 auto', padding: isMobile ? 0 : '0 30px' }}>
              <input
                ref={fileInputRef}
                type="file"
                multiple
                accept="image/*,video/*,.pdf,.doc,.docx,.txt,.md,.csv"
                onChange={e => {
                  const files = Array.from(e.target.files || []).map(file => ({
                    file,
                    preview: file.type?.startsWith('image/') ? URL.createObjectURL(file) : null,
                  }));
                  setPendingFiles(list => [...list, ...files]);
                  e.target.value = '';
                }}
                style={{ display: 'none' }}
              />
              <ChatComposer
                placeholder="继续跟 Nori 说：补充资料、修改定位、调整日历..."
                onSend={sendPlanningMessage}
                onAttach={() => fileInputRef.current?.click()}
                canSendExtra={pendingFiles.length > 0}
                attachmentCount={pendingFiles.length}
                attachmentFiles={pendingFiles.map(item => ({ name: item.file?.name || item.name, type: item.file?.type || item.type, preview: item.preview }))}
                onRemoveAttachment={(index) => setPendingFiles(list => {
                  const next = list.filter((_, i) => i !== index);
                  const removed = list[index];
                  if (removed?.preview) URL.revokeObjectURL(removed.preview);
                  return next;
                })}
              />
              <div style={{ marginTop: 9, textAlign: 'center', color: T.navyLight, fontSize: 11.5, lineHeight: 1.45 }}>
                Nori is AI and can make mistakes. Please double-check responses.
              </div>
            </div>
          </div>
        </main>

        {false && step >= 5 && !isMobile && (
          <PlanningDocPreview
            diagnosisText={diagnosisText}
            persona={activeReport || persona}
            pillars={pillars}
            calendar={calendar}
            activeSection={activePreviewSection}
            setActiveSection={setActivePreviewSection}
            mobile={false}
          />
        )}
      </div>

      {modalType && <InputMethodModal type={modalType} onClose={() => setModalType(null)} onConfirm={(att) => {
        setAttachments(list => [...list, att]);
        if (att.type === 'text') setRawInput(att.value);
        setModalType(null);
        setSentIntro(true);
      }} />}
      <PlanningStrategyDocModal strategy={strategyDoc} onClose={() => setStrategyDoc(null)} />
    </div>
  );

  return (
    <div style={{
      height: '100%',
      minHeight: 0,
      width: '100%',
      display: 'flex',
      flexDirection: 'column',
      background: 'linear-gradient(180deg, #FCFDFE 0%, #F4F7FA 100%)',
      color: T.navy,
      overflow: 'hidden',
    }}>
      <header style={{
        position: 'sticky',
        top: 0,
        zIndex: 8,
        display: 'block',
        gap: 14,
        padding: isMobile ? '14px 16px 10px' : '18px 24px 12px',
        background: 'rgba(252,253,254,.82)',
        backdropFilter: 'blur(16px) saturate(1.12)',
      }}>
        <div style={{
          maxWidth: 1120,
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 14,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: isMobile ? 12 : 22, minWidth: 0 }}>
            <button onClick={onBackHome} style={{
              border: 'none',
              background: 'transparent',
              color: T.navyMid,
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              fontSize: 13.5,
              fontWeight: 650,
              padding: '6px 2px',
              flexShrink: 0,
            }}>
              <Icon name="arrowLeft" size={16} />
              退出
            </button>
            <PlanningCompactProgress steps={steps} step={step} isMobile={isMobile} />
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
            <button onClick={() => persistDraft(step)} style={{
              height: 34,
              padding: '0 13px',
              borderRadius: 12,
              border: `1px solid ${T.hairlineSoft}`,
              background: 'rgba(255,255,255,.78)',
              color: T.navyMid,
              cursor: 'pointer',
              fontSize: 12.5,
              fontWeight: 650,
            }}>
              暂时保存
            </button>
            {!isMobile && (
              <div style={{ fontSize: 12.5, color: T.navyLight, fontFamily: T.fontMono }}>
                第 {step} / {steps.length} 步
              </div>
            )}
          </div>
        </div>
      </header>

      <main style={{
        flex: 1,
        minHeight: 0,
        overflowY: 'auto',
        overflowX: 'hidden',
        WebkitOverflowScrolling: 'touch',
        padding: isMobile ? '4px 16px 34px' : '6px 24px 40px',
      }} ref={scrollRef}>
        <div style={{ maxWidth: 1120, margin: '0 auto' }}>
          {toast && (
            <div style={{
              position: 'sticky',
              top: 12,
              zIndex: 5,
              marginBottom: 12,
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              padding: '10px 14px',
              borderRadius: 999,
              background: 'rgba(255,255,255,.82)',
              border: `1px solid ${T.hairlineSoft}`,
              boxShadow: '0 10px 26px rgba(14,14,44,.06)',
              color: T.navyMid,
              fontSize: 12.5,
              fontWeight: 650,
            }}>
              <Icon name="check" size={13} /> {toast}
            </div>
          )}

          {step >= 1 && (
            <div style={{ display: 'grid', gap: 18 }}>
              <PlanningReveal show delay={0}>
              <NoriSays>
                <p style={{ marginBottom: 8, fontSize: 16, fontWeight: 680 }}>先聊聊，你手上有点什么？</p>
                <p style={{ color: T.navyMid, fontSize: 13.5 }}>三种方式可以同时使用，给的信息越全，Nori 读得越准。</p>
              </NoriSays>
              </PlanningReveal>

              <PlanningReveal show={stage >= 1} delay={0}>
              <PlanningPanel title="输入方式" style={{ padding: isMobile ? 16 : 20 }}>
                <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(3, minmax(0, 1fr))', gap: 10, marginBottom: 12 }}>
                  <PlanningOption icon="link" title="粘贴链接" desc="店铺 / 主页 / 文章" active={attachments.some(item => item.type === 'link')} onClick={() => setModalType('link')} />
                  <PlanningOption icon="image" title="上传图片" desc="产品图 / 截图" active={attachments.some(item => item.type === 'image')} onClick={() => setModalType('image')} />
                  <PlanningOption icon="chat" title="直接描述" desc="我是做什么的" active={attachments.some(item => item.type === 'text')} onClick={() => setModalType('text')} />
                </div>
                <PlanningComposerMulti
                  attachments={attachments}
                  text={rawInput}
                  setText={setRawInput}
                  onRemoveAttachment={(index) => setAttachments(list => list.filter((_, i) => i !== index))}
                  onSend={() => setSentIntro(true)}
                />
              </PlanningPanel>
              </PlanningReveal>

              <PlanningReveal show={stage >= 2 && sentIntro} delay={0}>
              <PlanningPanel title="先把两个关键问题说清楚" style={{ padding: isMobile ? 16 : 20 }}>
                <div style={{ display: 'grid', gap: 18 }}>
                  <PlanningChoiceGroup
                    title="最想用社媒账号做什么？"
                    hint="可多选"
                    options={['引流到店', '品牌曝光', '线上卖货', '积累口碑']}
                    selected={goalSelections}
                    onToggle={(value) => toggleMulti(value, setGoalSelections)}
                    allowMultiple
                  />
                  <PlanningChoiceGroup
                    title="最想在哪个平台做？"
                    hint="可多选"
                    options={['小红书', '抖音', '视频号', '公众号']}
                    selected={platformSelections}
                    onToggle={(value) => toggleMulti(value, setPlatformSelections)}
                    allowMultiple
                  />
                </div>
              </PlanningPanel>
              </PlanningReveal>

              {step === 1 && <PlanningReveal show={stage >= 3 && sentIntro} delay={0}>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 10, flexWrap: 'wrap' }}>
                <button onClick={onBackHome} style={{ height: 40, padding: '0 14px', borderRadius: 13, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.78)', color: T.navyMid, cursor: 'pointer', fontSize: 13, fontWeight: 650 }}>
                  退出
                </button>
                <button onClick={() => setStep(2)} disabled={!canAdvanceStep1} style={{ height: 40, padding: '0 18px', borderRadius: 13, border: 'none', background: canAdvanceStep1 ? T.navy : T.surface, color: canAdvanceStep1 ? T.white : T.navyLight, cursor: canAdvanceStep1 ? 'pointer' : 'not-allowed', fontSize: 13, fontWeight: 700, boxShadow: canAdvanceStep1 ? '0 12px 24px rgba(14,14,44,.14)' : 'none' }}>
                  进入账号诊断
                </button>
              </div>
              </PlanningReveal>}
            </div>
            )}

          {step >= 2 && (
            <div style={{ display: 'grid', gap: 18 }}>
              <PlanningUserSummary>
                {`我提供了 ${attachments.length || rawInput ? '账号线索' : '基础信息'}。\n目标：${goalSelections.join('、') || '待确认'}\n平台：${platformSelections.join('、') || '待确认'}`}
              </PlanningUserSummary>
              <PlanningChatDivider label="账号诊断" />
              <PlanningReveal show delay={0}>
              <NoriSays>
                <p style={{ marginBottom: 8, fontSize: 16, fontWeight: 680 }}>读完了，这是我看到的你。</p>
                <p style={{ color: T.navyMid, fontSize: 13.5 }}>每一项都可以直接编辑，改完 Nori 自动记住。</p>
              </NoriSays>
              </PlanningReveal>

              <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(2, minmax(0, 1fr))', gap: 14 }}>
                {contentProfiles.map((item, index) => (
                  <PlanningReveal
                    key={item.title}
                    show={stage >= Math.min(index + 1, 3)}
                    delay={index * 80}
                    style={{ gridColumn: index === 4 && !isMobile ? 'span 2' : 'auto' }}
                  >
                  <PlanningPanel title={item.title} style={{ padding: 18 }}>
                    <textarea
                      value={item.value}
                      onChange={e => setDiagnosisText(prev => ({ ...prev, [Object.keys(diagnosisText)[index]]: e.target.value }))}
                      rows={index < 2 ? 4 : 5}
                      style={{
                        width: '100%',
                        border: `1px solid ${T.hairlineSoft}`,
                        borderRadius: 14,
                        background: 'rgba(250,252,254,.76)',
                        padding: 12,
                        resize: 'vertical',
                        outline: 'none',
                        color: T.navyMid,
                        fontSize: 13,
                        lineHeight: 1.72,
                        fontFamily: T.fontSans,
                        boxShadow: `inset 0 0 0 1px ${T.hairlineSoft}`,
                      }}
                    />
                  </PlanningPanel>
                  </PlanningReveal>
                ))}
              </div>

              {step === 2 && <PlanningReveal show={stage >= 3} delay={180}>
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 10, flexWrap: 'wrap' }}>
                <button onClick={() => setStep(1)} style={{ border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', fontSize: 12.8, fontWeight: 650 }}>返回上一步</button>
                <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                  <button onClick={() => setStep(3)} style={{ height: 40, padding: '0 18px', borderRadius: 13, border: 'none', background: T.navy, color: T.white, cursor: 'pointer', fontSize: 13, fontWeight: 700, boxShadow: '0 12px 24px rgba(14,14,44,.14)' }}>
                    看起来不错，继续
                  </button>
                </div>
              </div>
              </PlanningReveal>}
            </div>
          )}

          {step >= 3 && (
            <div style={{ display: 'grid', gap: 18 }}>
              <PlanningUserSummary>看起来不错，继续生成账号定位。</PlanningUserSummary>
              <PlanningChatDivider label="账号定位" />
              <NoriSays>
                <p style={{ marginBottom: 8, fontSize: 16, fontWeight: 680 }}>这是你的账号定位。</p>
                <p style={{ color: T.navyMid, fontSize: 13.5 }}>每一项都可以直接编辑，确认后 Nori 会按这套规则生成。</p>
              </NoriSays>

              <PlanningPanel style={{ padding: isMobile ? 16 : 20, position: 'relative', overflow: 'hidden' }}>
                <MiniOnionBurst active={true} />
                <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'minmax(0, 1.15fr) minmax(280px, .75fr)', gap: 16, alignItems: 'start' }}>
                  <div style={{ display: 'grid', gap: 12 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                      <div style={{ width: 54, height: 54, borderRadius: 18, background: T.irisTint, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', color: T.iris }}>
                        <Icon name="sparkles" size={22} />
                      </div>
                      <div>
                        <div style={{ color: T.navyLight, fontSize: 12.5, fontWeight: 650 }}>创作者 · Holly</div>
                        <div style={{ marginTop: 4, color: T.navy, fontSize: 21, fontWeight: 720 }}>理性解读 · 克制抒情 · 先结论再展开</div>
                      </div>
                    </div>
                    <div style={{ color: T.navyMid, fontSize: 13.5, lineHeight: 1.72 }}>
                      把复杂工具讲成普通人能立刻上手的生活方法。
                    </div>
                  </div>
                  <div style={{ borderRadius: 18, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(250,252,254,.72)', padding: 16 }}>
                    <div style={{ color: T.navyLight, fontSize: 12, fontWeight: 680, marginBottom: 8 }}>账号定位记忆</div>
                    <div style={{ marginTop: 12, color: T.navyMid, fontSize: 13, lineHeight: 1.68 }}>
                      再发布 2 条，Nori 就能把你的首段钩子偏好沉淀成规则。
                    </div>
                  </div>
                </div>
              </PlanningPanel>

                <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(2, minmax(0, 1fr))', gap: 14 }}>
                  <PlanningPanel title="账号名建议" style={{ padding: 18 }}>
                    <div style={{ display: 'grid', gap: 8 }}>
                      {(activeReport.names || []).map((item, index) => (
                        <input key={index} value={item} onChange={e => setActiveReport(prev => ({ ...prev, names: prev.names.map((row, i) => i === index ? e.target.value : row) }))} style={{ width: '100%', minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: 'rgba(250,252,254,.72)', color: T.navyMid, padding: '0 10px', outline: 'none', fontSize: 13 }} />
                      ))}
                    </div>
                  </PlanningPanel>
                  <PlanningPanel title="人设关键词" style={{ padding: 18 }}>
                    <div style={{ display: 'grid', gap: 8 }}>
                      {(activeReport.keywords || []).map((item, index) => (
                        <input key={index} value={item} onChange={e => setActiveReport(prev => ({ ...prev, keywords: prev.keywords.map((row, i) => i === index ? e.target.value : row) }))} style={{ width: '100%', minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: 'rgba(250,252,254,.72)', color: T.navyMid, padding: '0 10px', outline: 'none', fontSize: 13 }} />
                      ))}
                    </div>
                  </PlanningPanel>
                  <PlanningPanel title="常用句式" style={{ padding: 18 }}>
                    <div style={{ display: 'grid', gap: 8 }}>
                      {(activeReport.phrases || []).map((item, index) => (
                        <input key={index} value={item} onChange={e => setActiveReport(prev => ({ ...prev, phrases: prev.phrases.map((row, i) => i === index ? e.target.value : row) }))} style={{ width: '100%', minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: 'rgba(250,252,254,.72)', color: T.navyMid, padding: '0 10px', outline: 'none', fontSize: 13 }} />
                      ))}
                    </div>
                  </PlanningPanel>
                  <PlanningPanel title="账号主要内容支柱" style={{ padding: 18 }}>
                    <div style={{ display: 'grid', gap: 8 }}>
                      {(pillars || []).map((item, index) => (
                        <input key={index} value={item} onChange={e => setPillars(list => list.map((row, i) => i === index ? e.target.value : row))} style={{ width: '100%', minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: 'rgba(250,252,254,.72)', color: T.navyMid, padding: '0 10px', outline: 'none', fontSize: 13 }} />
                      ))}
                    </div>
                  </PlanningPanel>
                  <PlanningPanel title="对标博主" style={{ padding: 18 }}>
                    <div style={{ display: 'grid', gap: 8 }}>
                      {(activeReport.bloggers || []).map((item, index) => (
                        <input key={index} value={item} onChange={e => setActiveReport(prev => ({ ...prev, bloggers: prev.bloggers.map((row, i) => i === index ? e.target.value : row) }))} style={{ width: '100%', minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: 'rgba(250,252,254,.72)', color: T.navyMid, padding: '0 10px', outline: 'none', fontSize: 13 }} />
                      ))}
                    </div>
                  </PlanningPanel>
                  <PlanningPanel title="推荐封面图片" style={{ padding: 18 }}>
                    <div style={{ display: 'grid', gap: 8 }}>
                      {(activeReport.covers || []).map((item, index) => (
                        <input key={index} value={item} onChange={e => setActiveReport(prev => ({ ...prev, covers: prev.covers.map((row, i) => i === index ? e.target.value : row) }))} style={{ width: '100%', minHeight: 38, border: `1px solid ${T.hairlineSoft}`, borderRadius: 12, background: 'rgba(250,252,254,.72)', color: T.navyMid, padding: '0 10px', outline: 'none', fontSize: 13 }} />
                      ))}
                    </div>
                  </PlanningPanel>
                  <div style={{ gridColumn: isMobile ? 'auto' : 'span 2' }}>
                    <PlanningPanel title="签名" style={{ padding: 18 }}>
                      <textarea
                        value={activeReport.bio}
                        onChange={e => setActiveReport(prev => ({ ...prev, bio: e.target.value }))}
                        rows={3}
                        style={{ width: '100%', border: `1px solid ${T.hairlineSoft}`, borderRadius: 14, background: 'rgba(250,252,254,.76)', color: T.navyMid, padding: 12, outline: 'none', resize: 'vertical', fontSize: 13, lineHeight: 1.7, fontFamily: T.fontSans }}
                      />
                    </PlanningPanel>
                  </div>
                </div>

              {step === 3 && <div style={{ display: 'flex', justifyContent: 'space-between', gap: 10, flexWrap: 'wrap' }}>
                <button onClick={() => setStep(2)} style={{ border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', fontSize: 12.8, fontWeight: 650 }}>返回上一步</button>
                <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
                  <button onClick={() => setStep(4)} style={{ height: 40, padding: '0 18px', borderRadius: 13, border: 'none', background: T.navy, color: T.white, cursor: 'pointer', fontSize: 13, fontWeight: 700, boxShadow: '0 12px 24px rgba(14,14,44,.14)' }}>
                    确认画像
                  </button>
                </div>
              </div>}
            </div>
          )}

          {step >= 4 && (
            <div style={{ display: 'grid', gap: 18 }}>
              <PlanningUserSummary>确认运营计划，继续排内容排期。</PlanningUserSummary>
              <PlanningChatDivider label="内容排期" />
              <NoriSays>
                <p style={{ marginBottom: 8, fontSize: 16, fontWeight: 680 }}>先选一段时间，我把一周内容排期放进去。</p>
                <p style={{ color: T.navyMid, fontSize: 13.5 }}>默认一周 7 篇，按内容支柱轮转，右上角可单独改时间。</p>
              </NoriSays>

              <PlanningPanel
                title="一周内容排期"
                action={(
                  <div style={{ position: 'relative' }}>
                    <button onClick={() => setShowWeekPicker(v => !v)} style={{ height: 32, padding: '0 11px', borderRadius: 12, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.78)', color: T.navyMid, cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: 12, fontWeight: 650 }}>
                      <Icon name="calendar" size={13} />
                      选择周
                    </button>
                    {showWeekPicker && (
                      <input
                        type="date"
                        value={weekStart}
                        onChange={e => { setWeekStart(e.target.value); setShowWeekPicker(false); }}
                        style={{
                          position: 'absolute',
                          right: 0,
                          top: 38,
                          zIndex: 10,
                          height: 36,
                          border: `1px solid ${T.hairlineSoft}`,
                          borderRadius: 12,
                          background: T.white,
                          padding: '0 9px',
                          color: T.navyMid,
                          boxShadow: T.shadowMd,
                          fontFamily: T.fontSans,
                        }}
                      />
                    )}
                  </div>
                )}
                style={{ padding: 18 }}
              >
        <div style={{ margin: '-2px 0 14px', color: T.navyLight, fontSize: 12.5 }}>
                  规划周起始日：{weekStart}
                </div>
                <div style={{ display: 'grid', gap: 10 }}>
                  {calendar.map((item, index) => (
                    <div key={`${item.day}-${index}`} style={{
                      borderRadius: 18,
                      background: index === 0 ? 'rgba(239,239,253,.56)' : 'rgba(250,252,254,.76)',
                      border: `1px solid ${index === 0 ? 'rgba(75,77,237,.14)' : T.hairlineSoft}`,
                      padding: 14,
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', gap: 12, alignItems: 'center', marginBottom: 10 }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                          <span style={{ height: 24, padding: '0 9px', borderRadius: 999, background: T.white, color: T.navy, display: 'inline-flex', alignItems: 'center', fontSize: 12.5, fontWeight: 720 }}>{item.day}</span>
                          <span style={{ color: T.navyLight, fontSize: 12.2 }}>{item.type}</span>
                        </div>
                        <button onClick={() => setCalendar(list => list.filter((_, i) => i !== index))} style={{ ...iconBtnStyle(), width: 32, height: 32 }}><Icon name="close" size={11} /></button>
                      </div>
                      <textarea
                        value={item.topic}
                        rows={2}
                        onChange={e => setCalendar(list => list.map((row, i) => i === index ? { ...row, topic: e.target.value } : row))}
                        style={{
                          width: '100%',
                          border: `1px solid ${T.hairlineSoft}`,
                          background: 'rgba(255,255,255,.7)',
                          borderRadius: 14,
                          minHeight: 54,
                          padding: '10px 11px',
                          color: T.navy,
                          fontSize: 13,
                          outline: 'none',
                          resize: 'vertical',
                          fontFamily: T.fontSans,
                          lineHeight: 1.58,
                        }}
                      />
                      <div style={{ marginTop: 10, color: T.navyLight, fontSize: 11.8 }}>
                        参考：{item.ref}
                      </div>
                    </div>
                  ))}
                  <button onClick={() => setCalendar(list => [...list, { day: '新增', type: '图文', topic: '新的内容选题', ref: '@参考账号' }])} style={{ height: 38, borderRadius: 13, border: `1px dashed ${T.hairline}`, background: 'rgba(255,255,255,.58)', color: T.navyMid, cursor: 'pointer', fontSize: 12.5, fontWeight: 650 }}>
                    新增一天
                  </button>
                </div>
              </PlanningPanel>

              {step === 4 && <div style={{ display: 'flex', justifyContent: 'space-between', gap: 10, flexWrap: 'wrap' }}>
                <button onClick={() => setStep(3)} style={{ border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', fontSize: 12.8, fontWeight: 650 }}>返回上一步</button>
                <button onClick={() => setStep(5)} style={{ height: 40, padding: '0 18px', borderRadius: 13, border: 'none', background: T.navy, color: T.white, cursor: 'pointer', fontSize: 13, fontWeight: 700, boxShadow: '0 12px 24px rgba(14,14,44,.14)' }}>
                  生成最终交付
                </button>
              </div>}
            </div>
          )}

          {step >= 5 && (
            <div style={{ display: 'grid', gap: 18 }}>
              <PlanningUserSummary>生成最终交付。</PlanningUserSummary>
              <PlanningChatDivider label="最终交付" />
              <NoriSays>
                <p style={{ marginBottom: 8, fontSize: 16, fontWeight: 680 }}>交付好了，这是你可以直接带走的版本。</p>
                <p style={{ color: T.navyMid, fontSize: 13.5 }}>《账号定位 + 运营计划 + 内容排期》1 份，含定位、人设、对标、选题库、发布节奏、数据目标。</p>
              </NoriSays>

              <PlanningPanel title="最终交付" style={{ padding: 18 }}>
                <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'minmax(0, 1.08fr) 280px', gap: 14 }}>
                  <div style={{ borderRadius: 18, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(250,252,254,.76)', padding: 16 }}>
                    <div style={{ fontSize: 19, fontWeight: 740, color: T.navy }}>《账号定位 + 运营计划 + 内容排期》</div>
                    <div style={{ marginTop: 8, color: T.navyMid, fontSize: 13.5, lineHeight: 1.7 }}>
                      1 份，含定位、人设、对标、选题库、发布节奏、数据目标。
                    </div>
                    <div style={{ marginTop: 14, display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                      {['定位', '人设', '对标', '选题库', '发布节奏', '数据目标'].map(tag => (
                        <span key={tag} style={{ height: 32, padding: '0 11px', borderRadius: 999, background: 'rgba(255,255,255,.78)', border: `1px solid ${T.hairlineSoft}`, color: T.navyMid, display: 'inline-flex', alignItems: 'center', fontSize: 12.2, fontWeight: 650 }}>{tag}</span>
                      ))}
                    </div>
                    <div style={{ marginTop: 14, color: T.navyLight, fontSize: 12.2, lineHeight: 1.64 }}>
                      这份文档会同步到 Nori 后续创作里。
                    </div>
                  </div>
                  <div style={{ borderRadius: 18, border: `1px solid ${T.hairlineSoft}`, background: 'rgba(255,255,255,.72)', padding: 16, display: 'grid', gap: 8, alignContent: 'start' }}>
                    <button onClick={downloadPlan} style={{ ...pillButtonStyle(true), justifyContent: 'center' }}>
                      <Icon name="download" size={15} />
                      下载文档
                    </button>
                    <button onClick={() => setLiked(v => !v)} style={{ ...pillButtonStyle(false), justifyContent: 'center' }}>
                      <Icon name="heart" size={15} />
                      {liked ? '已点赞' : '点赞'}
                    </button>
                    <button onClick={() => copyPlan(buildPlanExportText({ diagnosisText, persona: activeReport || persona, pillars, calendar }))} style={{ ...pillButtonStyle(false), justifyContent: 'center' }}>
                      <Icon name={copied ? 'check' : 'copy'} size={15} />
                      {copied ? '已复制' : '复制'}
                    </button>
                  <button onClick={completePlan} style={{ ...pillButtonStyle(false), justifyContent: 'center' }}>
                    <Icon name="sparkles" size={15} />
                    完成并开始制作
                  </button>
                  </div>
                </div>
              </PlanningPanel>

              <div style={{ display: 'flex', justifyContent: 'space-between', gap: 10, flexWrap: 'wrap' }}>
                <button onClick={() => setStep(4)} style={{ border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', fontSize: 12.8, fontWeight: 650 }}>返回上一步</button>
                <button onClick={completePlan} style={{ height: 40, padding: '0 18px', borderRadius: 13, border: 'none', background: T.navy, color: T.white, cursor: 'pointer', fontSize: 13, fontWeight: 700, boxShadow: '0 12px 24px rgba(14,14,44,.14)' }}>
                  完成交付
                </button>
              </div>
            </div>
          )}
          <div ref={endRef} style={{ height: 1 }} />
        </div>
      </main>
      {modalType && <InputMethodModal type={modalType} onClose={() => setModalType(null)} onConfirm={(att) => {
        setAttachments(list => [...list, att]);
        if (att.type === 'text') setRawInput(att.value);
        setModalType(null);
        setSentIntro(true);
      }} />}
    </div>
  );
};

window.AccountPlanningPagePolishedV2 = AccountPlanningPagePolishedV2;
window.AccountPlanningPagePolished = AccountPlanningPagePolishedV2;

const WelcomeIntroOverlay = ({ open, leaving, onStartPlan, onTry }) => {
  const { isMobile } = useViewport();
  if (!open) return null;
  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      zIndex: 999,
      background: 'rgba(8,8,13,.56)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 22,
      opacity: leaving ? 0 : 1,
      transform: leaving ? 'scale(1.015)' : 'scale(1)',
      transition: `opacity .46s ${T.ease}, transform .46s ${T.spring}`,
    }}>
      <div style={{
        width: 'min(620px, 100%)',
        borderRadius: 28,
        background: T.white,
        border: `1px solid ${T.hairlineSoft}`,
        boxShadow: '0 42px 110px rgba(14,14,44,.24), 0 8px 24px rgba(14,14,44,.08)',
        padding: isMobile ? '24px 22px 22px' : '32px 34px 30px',
        color: T.navy,
        animation: `welcomeRise .72s ${T.spring} both`,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 13, marginBottom: 24 }}>
          <NoriLogo size={38} />
          <div>
            <div style={{ fontFamily: T.fontSerif, fontSize: 34, lineHeight: .96, fontStyle: 'italic', fontWeight: 700, letterSpacing: 0 }}>Nori</div>
            <div style={{ marginTop: 7, color: T.navyLight, fontSize: 12.2, lineHeight: 1.45 }}>懂你，会进化的自媒体账号代理</div>
          </div>
        </div>
        <h1 style={{ margin: 0, fontSize: isMobile ? 25 : 32, lineHeight: 1.18, letterSpacing: 0, fontWeight: 760 }}>
          从一个模糊想法，长成一个能持续运营的账号。
        </h1>
        <p style={{ margin: '14px 0 22px', color: T.navyMid, fontSize: 14, lineHeight: 1.76, maxWidth: 520, fontWeight: 430 }}>
          Nori 会帮你完成账号定位、运营计划和内容排期，并把第一篇内容直接带进工作台。
        </p>
        <div style={{ display: 'grid', gridTemplateColumns: isMobile ? '1fr' : 'repeat(3, minmax(0, 1fr))', gap: 10, marginBottom: 24 }}>
          {[
            ['target', '账号定位', '把赛道、目标和平台说清楚'],
            ['sparkles', '运营计划', '形成可复用的人设和内容支柱'],
            ['document', '内容排期', '自动排出一周选题建议'],
          ].map(([icon, title, desc]) => (
            <div key={title} style={{ borderRadius: 17, background: 'rgba(246,248,251,.76)', border: `1px solid ${T.hairlineSoft}`, padding: 14 }}>
              <span style={{ width: 32, height: 32, borderRadius: 12, background: T.white, color: T.iris, display: 'inline-flex', alignItems: 'center', justifyContent: 'center', marginBottom: 12, boxShadow: 'inset 0 1px 0 rgba(255,255,255,.86)' }}>
                <Icon name={icon} size={15} />
              </span>
              <div style={{ fontSize: 13.2, fontWeight: 740, color: T.navy }}>{title}</div>
              <div style={{ marginTop: 5, fontSize: 11.8, lineHeight: 1.52, color: T.navyLight }}>{desc}</div>
            </div>
          ))}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: 12, flexWrap: 'wrap' }}>
          <button onClick={onTry} style={{ height: 42, padding: '0 12px', border: 'none', background: 'transparent', color: T.navyLight, cursor: 'pointer', fontSize: 13, fontWeight: 650 }}>
            跳过，稍后再做
          </button>
          <button onClick={onStartPlan} style={{
            height: 44,
            padding: '0 18px',
            borderRadius: 14,
            border: 'none',
            background: T.navy,
            color: T.white,
            cursor: 'pointer',
            fontSize: 13.5,
            fontWeight: 760,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 8,
            boxShadow: '0 14px 30px rgba(14,14,44,.18)',
          }}>
            开始账号规划
            <Icon name="arrowRight" size={14} />
          </button>
        </div>
      </div>
    </div>
  );
};

window.WelcomeIntroOverlay = WelcomeIntroOverlay;
/* ─── App root ─── */

const GlobalPolish = () => (
  <style>{`
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
  `}</style>
);

const App = () => {
  const [page, setPage] = React.useState('home'); // 'home' | 'assets' | 'insights' | 'mine' | 'accountPlan' | 'gen'
  const [prompt, setPrompt] = React.useState('');
  const [assetDraft, setAssetDraft] = React.useState(null);
  const [skillDraft, setSkillDraft] = React.useState(null);
  const [accountPlanDraft, setAccountPlanDraft] = React.useState(null);
  const [showIntro, setShowIntro] = React.useState(true);
  const [introLeaving, setIntroLeaving] = React.useState(false);
  const [recentProject, setRecentProject] = React.useState(null);
  const [insightInitialTab, setInsightInitialTab] = React.useState('review');
  const [homeFocusKey, setHomeFocusKey] = React.useState(0);
  const [inspirationDraft, setInspirationDraft] = React.useState(null);

  const goGen = (p) => {
    const clean = p || '';
    setPrompt(clean);
    setInspirationDraft(null);
    setAssetDraft(null);
    setSkillDraft(null);
    setAccountPlanDraft(null);
    if (clean.trim()) {
      setRecentProject({
        title: clean.replace(/^\[[^\]]+\]\s*/, '').slice(0, 34),
        summary: clean.length > 34 ? `${clean.slice(0, 54)}...` : '来自首页对话框的第一轮创作',
        date: '今天',
        prompt: clean,
      });
    }
    setPage('gen');
  };

  const startFreshAccountPlan = ({ hideIntroImmediately = false } = {}) => {
    clearPlanDraftStorage();
    setAccountPlanDraft(null);
    if (hideIntroImmediately) {
      setShowIntro(false);
      setIntroLeaving(false);
    }
    setPage('accountPlan');
  };

  const withPolish = (node) => (
    <>
      <GlobalPolish />
      {node}
      <WelcomeIntroOverlay
        open={showIntro}
        leaving={introLeaving}
        onTry={() => {
          setIntroLeaving(true);
          window.setTimeout(() => {
            setShowIntro(false);
            setIntroLeaving(false);
          }, 460);
        }}
        onStartPlan={() => {
          setIntroLeaving(true);
          window.setTimeout(() => {
            setShowIntro(false);
            setIntroLeaving(false);
            startFreshAccountPlan();
          }, 460);
        }}
      />
    </>
  );

  if (page === 'home') return withPolish(
    <HomePage
      onSubmit={goGen}
    onOpenAssets={() => setPage('assets')}
    onOpenInsights={() => { setInsightInitialTab('review'); setPage('insights'); }}
    onOpenMine={() => setPage('mine')}
      onAccountPlan={() => startFreshAccountPlan({ hideIntroImmediately: true })}
      accountPlanDraft={accountPlanDraft}
      recentProject={recentProject}
      onOpenInspiration={(draft) => {
        setPage('gen');
        setInspirationDraft({
          item: draft?.item || null,
          prompt: draft?.prompt || '参考首页灵感发现里的内容，把这张图改成更像上海饭店探店封面的样式。',
        });
      }}
      focusInspirationKey={homeFocusKey}
      onOpenProject={() => {
        if (!recentProject) return;
        setPrompt(recentProject.prompt);
        setAssetDraft(null);
        setSkillDraft(null);
        setAccountPlanDraft(null);
        setPage('gen');
      }}
    />
  );

  if (page === 'accountPlan') {
    return withPolish(
      <AccountPlanningPagePolishedV2
        onBackHome={() => setPage('home')}
        onOpenAssets={() => setPage('assets')}
        onOpenInsights={() => { setInsightInitialTab('review'); setPage('insights'); }}
        onNewChat={() => {
          setPrompt('');
          setAssetDraft(null);
          setSkillDraft(null);
          setAccountPlanDraft(null);
          setPage('gen');
        }}
        onComplete={(draft) => {
          setPrompt('');
          setAssetDraft(null);
          setSkillDraft(null);
          setAccountPlanDraft(draft);
          setPage('gen');
        }}
      />
    );
  }

  if (page === 'assets') {
    return withPolish(
      <AssetsPage
        onBackHome={() => setPage('home')}
        onOpenInsights={() => { setInsightInitialTab('review'); setPage('insights'); }}
        onOpenMine={() => setPage('mine')}
        onNewChat={() => {
          setPrompt('');
          setAssetDraft(null);
          setSkillDraft(null);
          setAccountPlanDraft(null);
          setPage('gen');
        }}
        onOpenAsset={(asset) => {
          setPrompt(`继续编辑内容资产：${asset.title}`);
          setAssetDraft(asset);
          setSkillDraft(null);
          setAccountPlanDraft(null);
          setPage('gen');
        }}
      />
    );
  }

  if (page === 'mine') {
    return withPolish(
      <MinePage
        onBackHome={() => setPage('home')}
        onOpenAssets={() => setPage('assets')}
        onOpenInsights={() => { setInsightInitialTab('review'); setPage('insights'); }}
        onNewChat={() => {
          setPrompt('');
          setAssetDraft(null);
          setSkillDraft(null);
          setAccountPlanDraft(null);
          setPage('gen');
        }}
      />
    );
  }

  if (page === 'insights') {
    return withPolish(
      <InsightsPage
        onBackHome={() => setPage('home')}
        onOpenAssets={() => setPage('assets')}
        onOpenMine={() => setPage('mine')}
        initialTab={insightInitialTab}
        onNewChat={() => {
          setPrompt('');
          setAssetDraft(null);
          setSkillDraft(null);
          setAccountPlanDraft(null);
          setPage('gen');
        }}
      />
    );
  }

  return withPolish(
    <GenerationPage
      initialPrompt={prompt}
      assetDraft={assetDraft}
      skillDraft={skillDraft}
      onboardingDraft={accountPlanDraft}
      inspirationDraft={inspirationDraft}
      onBackHome={() => setPage('home')}
      onOpenAssets={() => setPage('assets')}
      onOpenInsights={() => { setInsightInitialTab('review'); setPage('insights'); }}
      onOpenMine={() => setPage('mine')}
      onOpenHomeInspiration={() => {
        setHomeFocusKey(v => v + 1);
        setPage('home');
      }}
      onNewChat={() => {
        setPrompt('');
        setAssetDraft(null);
        setSkillDraft(null);
        setAccountPlanDraft(null);
        setPage('gen');
      }}
    />
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
