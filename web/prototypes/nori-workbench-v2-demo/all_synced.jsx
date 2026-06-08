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
  shadowXs:   '0 1px 2px rgba(14,14,44,.04), 0 1px 4px rgba(14,14,44,.03)',
  shadowSm:   '0 2px 6px rgba(14,14,44,.06), 0 1px 2px rgba(14,14,44,.04)',
  shadowMd:   '0 4px 12px rgba(14,14,44,.08), 0 1px 3px rgba(14,14,44,.05)',
  shadowLg:   '0 8px 24px rgba(14,14,44,.10), 0 2px 6px rgba(14,14,44,.06)',
  shadowXl:   '0 16px 48px rgba(14,14,44,.12), 0 4px 12px rgba(14,14,44,.07)',
  shadowBtn:  '0 2px 6px rgba(14,14,44,.06), 0 1px 2px rgba(14,14,44,.04), inset 0 -1px 0 rgba(14,14,44,.12)',

  // Type
  fontSans:   "'Source Han Sans CN', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif",
  fontSerif:  "'Fraunces', Georgia, serif",
  fontMono:   "'DM Mono', 'Monaco', monospace",
};



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
    chevronDown: <path d="M6 9l6 6 6-6"/>,
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
    file: <><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/></>,
    search: <><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></>,
    chat: <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>,
    library: <><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></>,
    home: <><path d="M3 9.5l9-7 9 7V20a2 2 0 0 1-2 2h-4v-7H9v7H5a2 2 0 0 1-2-2z"/></>,
    grid: <><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></>,
    expand: <><path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/></>,
    collapse: <><path d="M4 14h6v6"/><path d="M20 10h-6V4"/><path d="M14 10l7-7"/><path d="M3 21l7-7"/></>,
    download: <><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></>,
    trash: <><path d="M3 6h18"/><path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M19 6l-1 15H6L5 6"/><path d="M10 11v6M14 11v6"/></>,
    upload: <><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M17 8l-5-5-5 5"/><path d="M12 3v12"/></>,
    sync: <><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M3 21v-5h5"/></>,
    transform: <><path d="M16 3l4 4-4 4"/><path d="M20 7H4"/><path d="M8 21l-4-4 4-4"/><path d="M4 17h16"/></>,
    phone: <rect x="6" y="2" width="12" height="20" rx="2"/>,
    pen: <><path d="M12 19l7-7 3 3-7 7-3-3z"/><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"/><path d="M2 2l7.6 7.6"/><circle cx="11" cy="11" r="2"/></>,
    sliders: <><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></>,
    filter: <><path d="M4 5h16"/><path d="M7 12h10"/><path d="M10 19h4"/></>,
    clock: <><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></>,
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

/* Nori brand logo — nori = 海苔/seaweed-like organism. A friendly water-drop with eyes. */
const NoriLogo = ({ size = 28, dark = true }) => {
  const fg = dark ? T.navy : '#fff';
  const bg = T.primary;
  return (
    <div style={{
      width: size, height: size, borderRadius: size * 0.32,
      background: bg, display: 'flex', alignItems: 'center', justifyContent: 'center',
      flexShrink: 0,
    }}>
      <svg width={size * 0.62} height={size * 0.62} viewBox="0 0 24 24" fill="none">
        {/* nori mascot: rounded blob with two dot eyes */}
        <path d="M12 3c-3 0-6 2.5-6 6.5 0 2 .8 3.6 2 4.8.4.4.4 1 0 1.4l-.5.5a1 1 0 0 0 .7 1.7H10v1.6a1 1 0 0 0 2 0V18h1.8a1 1 0 0 0 .7-1.7l-.5-.5a1 1 0 0 1 0-1.4c1.2-1.2 2-2.8 2-4.8C16 5.5 13 3 12 3z"
          fill={fg} />
        <circle cx="9.7" cy="9.5" r="1" fill={bg} />
        <circle cx="14.3" cy="9.5" r="1" fill={bg} />
      </svg>
    </div>
  );
};




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

const Sidebar = ({ active, onNew, onNavigate, sessions = [] }) => {
  return (
    <aside style={{
      width: 232,
      flexShrink: 0,
      background: T.surfaceWh,
      borderRight: `1px solid ${T.hairline}`,
      display: 'flex',
      flexDirection: 'column',
      padding: '20px 14px',
      height: '100%',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '4px 10px 20px' }}>
        <NoriLogo size={28} />
        <span style={{ fontSize: 18, fontWeight: 700, letterSpacing: '-0.02em' }}>Nori</span>
        <span style={{
          fontSize: 9,
          fontFamily: T.fontMono,
          color: T.navyLight,
          background: T.surface,
          padding: '2px 5px',
          borderRadius: 3,
          marginLeft: 'auto',
        }}>v2.1</span>
      </div>

      <button
        onClick={onNew}
        style={{
          height: 40,
          borderRadius: 10,
          border: `1px solid ${T.hairline}`,
          background: T.white,
          color: T.navy,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 14px',
          fontSize: 13,
          fontWeight: 500,
          cursor: 'pointer',
          marginBottom: 18,
          boxShadow: T.shadowXs,
          transition: 'all .15s',
        }}
        onMouseEnter={e => e.currentTarget.style.background = T.surface}
        onMouseLeave={e => e.currentTarget.style.background = T.white}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <Icon name="edit" size={15} color={T.navyMid} />
          <span>新建对话</span>
        </div>
        <span style={{ fontSize: 10, fontFamily: T.fontMono, color: T.navyLight, background: T.surface, padding: '2px 5px', borderRadius: 3 }}>⌘K</span>
      </button>

      <nav style={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
        {[
          { id: 'home', label: '首页', icon: 'home' },
          { id: 'library', label: '我的内容库', icon: 'library' },
          { id: 'skills', label: 'Skill 广场', icon: 'sparkles' },
          { id: 'insights', label: '账号洞察', icon: 'chart' },
        ].map(item => (
          <button
            key={item.id}
            type="button"
            onClick={() => onNavigate && onNavigate(item.id)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              width: '100%',
              padding: '8px 10px',
              borderRadius: 8,
              border: 'none',
              fontSize: 13,
              fontWeight: active === item.id ? 600 : 500,
              color: active === item.id ? T.navy : T.navyMid,
              background: active === item.id ? T.surface : 'transparent',
              fontFamily: T.fontSans,
              textAlign: 'left',
              cursor: 'pointer',
              transition: 'all .12s',
            }}
            onMouseEnter={e => { if (active !== item.id) e.currentTarget.style.background = 'rgba(14,14,44,.03)'; }}
            onMouseLeave={e => { if (active !== item.id) e.currentTarget.style.background = 'transparent'; }}
          >
            <Icon name={item.icon} size={16} color={active === item.id ? T.navy : T.navyLight} />
            {item.label}
          </button>
        ))}
      </nav>

      <div style={{ marginTop: 24, flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column' }}>
        <div style={{ fontSize: 10, fontWeight: 600, letterSpacing: '0.1em', textTransform: 'uppercase', color: T.navyLight, padding: '0 10px 8px' }}>
          最近创作
        </div>
        <div style={{ overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 1 }}>
          {sessions.map((s, i) => (
            <a
              key={i}
              href="#"
              style={{
                padding: '7px 10px',
                borderRadius: 6,
                fontSize: 12.5,
                color: T.navyMid,
                fontWeight: 450,
                textDecoration: 'none',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                transition: 'background .12s',
              }}
              onMouseEnter={e => e.currentTarget.style.background = 'rgba(14,14,44,.03)'}
              onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
            >
              {s}
            </a>
          ))}
        </div>
      </div>

      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 10,
          padding: '10px',
          borderRadius: 10,
          marginTop: 12,
          cursor: 'pointer',
          transition: 'background .12s',
        }}
        onMouseEnter={e => e.currentTarget.style.background = T.surface}
        onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
      >
        <div style={{
          width: 30,
          height: 30,
          borderRadius: '50%',
          background: `linear-gradient(135deg, ${T.iris}, ${T.peach})`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: T.white,
          fontSize: 12,
          fontWeight: 700,
        }}>L</div>
        <div style={{ display: 'flex', flexDirection: 'column', minWidth: 0, flex: 1 }}>
          <span style={{ fontSize: 12.5, fontWeight: 600, color: T.navy }}>Luna</span>
          <span style={{ fontSize: 10.5, color: T.navyLight }}>Pro · 87 / 200 次</span>
        </div>
        <Icon name="moreH" size={14} color={T.navyLight} />
      </div>
    </aside>
  );
};

const HeroHeadline = ({ compact, mobile }) => {
  const burstIcons = [
    { name: 'sparkles', top: '6%', left: '18%', tint: T.primary, delay: '0ms', size: 15 },
    { name: 'star', top: '22%', right: '16%', tint: T.iris, delay: '60ms', size: 12 },
    { name: 'heart', top: '66%', left: '11%', tint: '#d49e9c', delay: '120ms', size: 11 },
    { name: 'bookmark', top: '74%', right: '12%', tint: T.navyMid, delay: '180ms', size: 11 },
    { name: 'globe', top: '44%', right: '3%', tint: T.iris, delay: '240ms', size: 12 },
    { name: 'pen', top: '48%', left: '2%', tint: '#95b200', delay: '300ms', size: 12 },
    { name: 'sparkle', top: '84%', left: '42%', tint: T.primary, delay: '360ms', size: 12 },
  ];
  const [bursting, setBursting] = React.useState(false);
  const timerRef = React.useRef(null);
  const platformPills = [
    { label: '微', name: '微信', tint: '#31D0AA', top: '18%', left: '8%' },
    { label: '抖', name: '抖音', tint: '#111111', top: '30%', right: '8%' },
    { label: '红', name: '小红书', tint: '#ff6b81', top: '68%', left: '7%' },
    { label: 'B', name: 'B站', tint: '#5f70d6', top: '76%', right: '14%' },
  ];

  const triggerBurst = React.useCallback(() => {
    window.clearTimeout(timerRef.current);
    setBursting(false);
    requestAnimationFrame(() => {
      setBursting(true);
      timerRef.current = window.setTimeout(() => setBursting(false), 1550);
    });
  }, []);

  React.useEffect(() => () => window.clearTimeout(timerRef.current), []);

  const lineOneSize = mobile ? 30 : compact ? 42 : 54;
  const ideaSize = mobile ? 48 : compact ? 68 : 88;
  const lineTwoSize = mobile ? 30 : compact ? 40 : 50;
  const everywhereSize = mobile ? 40 : compact ? 56 : 74;

  return (
    <div style={{ position: 'relative', width: '100%', marginBottom: mobile ? 22 : 28 }}>
      {!mobile && burstIcons.map((item, index) => (
        <div
          key={`${item.name}-${index}`}
          style={{
            position: 'absolute',
            top: item.top,
            left: item.left,
            right: item.right,
            opacity: bursting ? 1 : 0,
            transform: bursting ? 'translate3d(0, 0, 0) scale(1)' : 'translate3d(0, 8px, 0) scale(.5)',
            transition: `opacity .26s ${item.delay} ease, transform .46s ${item.delay} cubic-bezier(.2,.8,.2,1)`,
            pointerEvents: 'none',
            zIndex: 3,
          }}
        >
          <div style={{
            width: item.size + 10,
            height: item.size + 10,
            borderRadius: 999,
            background: 'rgba(255,255,255,.78)',
            border: `1px solid ${T.hairlineSoft}`,
            boxShadow: T.shadowSm,
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            backdropFilter: 'blur(14px)',
          }}>
            <Icon name={item.name} size={item.size} color={item.tint} />
          </div>
        </div>
      ))}

      {!mobile && platformPills.map((item, index) => (
        <div
          key={`${item.name}-${index}`}
          style={{
            position: 'absolute',
            top: item.top,
            left: item.left,
            right: item.right,
            opacity: bursting ? 1 : 0,
            transform: bursting ? 'translate3d(0, 0, 0) scale(1)' : 'translate3d(0, 10px, 0) scale(.65)',
            transition: `opacity .3s ${420 + index * 70}ms ease, transform .42s ${420 + index * 70}ms cubic-bezier(.2,.8,.2,1)`,
            pointerEvents: 'none',
            zIndex: 3,
          }}
        >
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 6,
            padding: '8px 10px',
            borderRadius: 999,
            background: 'rgba(255,255,255,.82)',
            border: `1px solid ${T.hairlineSoft}`,
            boxShadow: T.shadowSm,
            backdropFilter: 'blur(14px)',
          }}>
            <span style={{
              width: 18,
              height: 18,
              borderRadius: 999,
              background: item.tint,
              color: item.name === '抖音' ? '#fff' : T.white,
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 10,
              fontWeight: 700,
            }}>{item.label}</span>
            <span style={{ fontSize: 11.5, fontWeight: 600, color: T.navyMid }}>{item.name}</span>
          </div>
        </div>
      ))}

      <button
        type="button"
        onClick={triggerBurst}
        style={{
          width: '100%',
          border: 'none',
          background: 'transparent',
          padding: 0,
          cursor: 'pointer',
          textAlign: 'center',
        }}
      >
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: 8,
          padding: mobile ? '6px 10px' : '8px 12px',
          marginBottom: mobile ? 18 : 22,
          borderRadius: 999,
          background: 'rgba(255,255,255,.72)',
          border: `1px solid ${T.hairlineSoft}`,
          boxShadow: T.shadowXs,
          backdropFilter: 'blur(18px)',
        }}>
          <span style={{
            width: 8,
            height: 8,
            borderRadius: '50%',
            background: T.primary,
            boxShadow: `0 0 0 6px rgba(214,255,0,.16)`,
          }} />
          <span style={{ fontSize: 11, fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase', color: T.navyMid }}>
            Editorial OS for creators
          </span>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: mobile ? 2 : 4 }}>
          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            alignItems: 'baseline',
            gap: mobile ? '0 10px' : '0 14px',
            lineHeight: .95,
          }}>
            <span style={{
              fontFamily: T.fontSans,
              fontSize: lineOneSize,
              fontWeight: 520,
              letterSpacing: '-0.055em',
              color: bursting ? '#5f70d6' : 'rgba(14,14,44,.74)',
              transition: 'color .35s ease',
            }}>From one</span>
            <span style={{
              fontFamily: T.fontSerif,
              fontSize: ideaSize,
              fontWeight: 600,
              fontStyle: 'italic',
              letterSpacing: '-0.04em',
              color: bursting ? '#c26f8b' : T.navy,
              textShadow: bursting ? '0 0 18px rgba(194,111,139,.18)' : '0 18px 40px rgba(14,14,44,.08)',
              transition: 'color .35s ease, text-shadow .35s ease',
            }}>idea</span>
          </div>

          <div style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            alignItems: 'baseline',
            gap: mobile ? '0 10px' : '0 14px',
            lineHeight: .92,
          }}>
            <span style={{
              fontFamily: T.fontSans,
              fontSize: lineTwoSize,
              fontWeight: 520,
              letterSpacing: '-0.05em',
              color: bursting ? '#557f98' : 'rgba(14,14,44,.74)',
              transition: 'color .35s ease',
            }}>to</span>
            <span style={{
              position: 'relative',
              display: 'inline-flex',
              alignItems: 'center',
              fontFamily: T.fontSans,
              fontSize: lineTwoSize,
              fontWeight: 720,
              letterSpacing: '-0.065em',
              color: T.navy,
            }}>
              <span style={{
                position: 'absolute',
                inset: mobile ? '46% -2% -8% -2%' : '50% -3% -10% -3%',
                background: `linear-gradient(90deg, rgba(214,255,0,.12), rgba(243,219,218,.22), rgba(75,77,237,.12))`,
                filter: 'blur(8px)',
                borderRadius: 999,
                zIndex: 0,
              }} />
              <span style={{
                position: 'relative',
                zIndex: 1,
                color: bursting ? '#8a7d52' : T.navy,
                transition: 'color .35s ease',
              }}>content</span>
            </span>
            <span style={{
              position: 'relative',
              fontFamily: T.fontSerif,
              fontSize: everywhereSize,
              fontWeight: 560,
              letterSpacing: '-0.06em',
              color: bursting ? '#0f8f73' : T.navy,
              transition: 'color .35s ease',
            }}>
              everywhere
              <span style={{
                position: 'absolute',
                right: mobile ? -12 : -18,
                top: '8%',
                width: mobile ? 2 : 3,
                height: mobile ? 32 : 46,
                borderRadius: 999,
                background: bursting
                  ? `linear-gradient(180deg, rgba(214,255,0,.96), rgba(255,255,255,.18), rgba(75,77,237,.92))`
                  : `linear-gradient(180deg, rgba(214,255,0,.92), rgba(255,255,255,.12), rgba(214,255,0,.72))`,
                boxShadow: bursting
                  ? '0 0 0 4px rgba(214,255,0,.10), 0 0 18px rgba(214,255,0,.5), 0 0 24px rgba(75,77,237,.18)'
                  : '0 0 10px rgba(214,255,0,.38)',
                animation: bursting ? 'pulse .48s 3 ease-in-out' : 'pulse 1.35s infinite ease-in-out',
              }} />
              <span style={{
                position: 'absolute',
                right: mobile ? -18 : -25,
                top: mobile ? -6 : -8,
                opacity: bursting ? 1 : .48,
                transform: bursting ? 'scale(1.08) rotate(10deg)' : 'scale(.92) rotate(0deg)',
                transition: 'opacity .24s ease, transform .24s ease',
                color: T.primary,
                textShadow: '0 0 16px rgba(214,255,0,.42)',
              }}>
                <Icon name="sparkles" size={mobile ? 10 : 12} color={T.primary} />
              </span>
            </span>
          </div>
        </div>
      </button>

      <div style={{
        display: 'flex',
        justifyContent: 'center',
        gap: 10,
        flexWrap: 'wrap',
        marginTop: mobile ? 16 : 18,
      }}>
        {[
          { icon: 'sparkles', label: 'tap for micro-motion' },
          { icon: 'layers', label: 'responsive editorial layout' },
          { icon: 'palette', label: 'iOS softness + brand contrast' },
        ].map((item, index) => (
          <div key={index} style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 6,
            padding: '7px 11px',
            borderRadius: 999,
            background: 'rgba(255,255,255,.68)',
            border: `1px solid ${T.hairlineSoft}`,
            boxShadow: T.shadowXs,
            fontSize: 11.5,
            fontWeight: 520,
            color: T.navyMid,
            backdropFilter: 'blur(16px)',
          }}>
            <Icon name={item.icon} size={12} color={index === 0 ? T.primaryHov : index === 1 ? T.iris : '#d49e9c'} />
            {item.label}
          </div>
        ))}
      </div>
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

  return (
    <div style={{
      position: 'relative',
      background: 'linear-gradient(180deg, rgba(255,255,255,.94), rgba(255,255,255,.88))',
      borderRadius: mobile ? 22 : 28,
      border: `1px solid ${focused ? 'rgba(75,77,237,.24)' : 'rgba(14,14,44,.06)'}`,
      boxShadow: focused
        ? `0 0 0 4px rgba(75,77,237,.10), 0 32px 80px rgba(14,14,44,.10), ${T.shadowLg}`
        : '0 28px 80px rgba(14,14,44,.08), 0 6px 18px rgba(14,14,44,.04)',
      padding: mobile ? '16px 16px 12px' : compact ? '18px 18px 14px' : '20px 22px 14px',
      transition: 'border .18s, box-shadow .18s, transform .18s',
      backdropFilter: 'blur(20px)',
      overflow: 'hidden',
    }}>
      <div style={{
        position: 'absolute',
        inset: 0,
        background: 'radial-gradient(circle at 14% 12%, rgba(214,255,0,.12), transparent 30%), radial-gradient(circle at 88% 14%, rgba(75,77,237,.08), transparent 22%)',
        pointerEvents: 'none',
      }} />

      <div style={{ position: 'relative', zIndex: 1 }}>
        {format && <FormatTag label={format.label} sub={format.sub} onCancel={onClearFormat} />}

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
          placeholder="Share one idea. Nori turns it into content everywhere..."
          rows={mobile ? 3 : 2}
          style={{
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
            maxHeight: 180,
          }}
        />

        <div style={{
          display: 'flex',
          alignItems: mobile ? 'stretch' : 'center',
          justifyContent: 'space-between',
          gap: 10,
          marginTop: 4,
          flexDirection: mobile ? 'column' : 'row',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexWrap: 'wrap' }}>
            <ToolPill icon="paperclip" label="Attach" />
            <ToolPill icon="globe" label="Search" active />
            <ToolPill icon="sparkles" label="Refine" />
          </div>

          <button
            onClick={() => value.trim() && onSubmit()}
            disabled={!value.trim()}
            style={{
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
              transition: 'all .15s',
            }}
          >
            <Icon name="paperPlane" size={15} stroke={2} />
            {mobile && <span style={{ fontSize: 13, fontWeight: 600 }}>Start crafting</span>}
          </button>
        </div>
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
  ];
  const subs = {
    xhs: ['爆款种草', '攻略干货', '生活记录', '产品测评'],
    wechat: ['深度长文', '观点专栏', '人物访谈', '行业分析'],
    video: ['科普视频', '产品宣传', '漫剧', '口播'],
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
                backdropFilter: 'blur(10px)',
              }}
            >
              <Icon name={c.icon} size={14} />
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
          animation: 'fadeIn .2s ease',
          justifyContent: mobile ? 'center' : 'flex-start',
        }}>
          {subs[current.key].map((s, i) => (
            <button
              key={i}
              onClick={() => { onPick({ cat: current.key, label: current.label, sub: s }); setOpenCat(null); }}
              style={{
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
                boxShadow: T.shadowXs,
              }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(75,77,237,.4)'; e.currentTarget.style.transform = 'translateY(-1px)'; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = T.hairline; e.currentTarget.style.transform = 'translateY(0)'; }}
            >
              <span style={{ fontSize: 13, fontWeight: 600, color: T.navy }}>{s}</span>
              <span style={{ fontSize: 11, color: T.navyLight }}>{current.label} · {s}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

const ToolPill = ({ icon, label, active }) => {
  const [hov, setHov] = React.useState(false);
  return (
    <button
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        height: 30,
        padding: '0 10px',
        borderRadius: 99,
        background: active ? T.irisTint : (hov ? T.surface : 'transparent'),
        border: `1px solid ${active ? 'transparent' : (hov ? 'transparent' : T.hairline)}`,
        color: active ? T.iris : T.navyMid,
        display: 'inline-flex',
        alignItems: 'center',
        gap: 5,
        fontSize: 12,
        fontWeight: 500,
        cursor: 'pointer',
        transition: 'all .12s',
      }}
    >
      <Icon name={icon} size={13} />
      {label}
    </button>
  );
};

const QuickStart = ({ onPick, compact, mobile }) => {
  const shelves = [
    [
      { title: '阳台植物的情绪板改造', desc: '从一个小阳台出发，延展成封面、图文和短视频脚本。', tint: '#eef3e3', accent: '#6d8355', emoji: '🌿', tag: 'Balcony Reset' },
      { title: '当家居博主爱上拼豆后', desc: '把手作过程变成更有记忆点的生活方式内容。', tint: '#fff0d8', accent: '#b8862f', emoji: '🐱', tag: 'Craft Loop' },
      { title: '深夜食堂里的治愈系主厨', desc: '从一碗热汤，做出一整套有人情味的社媒叙事。', tint: '#f2eedf', accent: '#8a7d52', emoji: '🍜', tag: 'Warm Series' },
      { title: '职场人的知识 IP 变现路径', desc: '把五年经验整理成会传播、可连载的知识内容。', tint: '#f7e8ea', accent: '#b5707a', emoji: '💼', tag: 'Pro Story' },
    ],
    [
      { title: '猫咪日常也能拍出栏目感', desc: '把碎片化生活切成固定栏目，轻松做持续更新。', tint: '#fff1df', accent: '#bf7d36', emoji: '🐈', tag: 'Soft Habit' },
      { title: 'City Walk 变成城市策展笔记', desc: '不是打卡清单，而是有审美和路线逻辑的内容包。', tint: '#e7f0f6', accent: '#557f98', emoji: '🚶', tag: 'Urban Edit' },
      { title: '咖啡入门 12 个名词', desc: '做成对新手友好的知识卡片和短内容矩阵。', tint: '#f2e7dc', accent: '#9c7352', emoji: '☕', tag: 'Starter Pack' },
      { title: '极简通勤穿搭一周 OOTD', desc: '让日常穿搭更像连载内容，而不是单条记录。', tint: '#eceaf6', accent: '#7973b3', emoji: '🧥', tag: 'Week Format' },
    ],
    [
      { title: '租房避雷指南 v2', desc: '把经验帖升级成更有结构、更有分享欲的攻略。', tint: '#eef0f8', accent: '#6977ad', emoji: '🏠', tag: 'Field Notes' },
      { title: 'AI 视频工具横评', desc: '从工具参数转成更适合传播的体验型结论。', tint: '#edf5ec', accent: '#5f8b66', emoji: '🪄', tag: 'Tool Review' },
      { title: '品牌主理人的幕后手帐', desc: '把产品思考、开会片段和灵感卡片织成系列。', tint: '#f8ece3', accent: '#ba7b52', emoji: '📒', tag: 'Behind Scene' },
      { title: '健身猛男为什么爱粉色植物', desc: '反差感、观点感和视觉记忆点一次给足。', tint: '#f7e6ec', accent: '#af6280', emoji: '🪴', tag: 'Contrast Hook' },
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
      background: 'rgba(255,255,255,.72)',
      border: `1px solid ${T.hairline}`,
      borderRadius: mobile ? 24 : 30,
      padding: mobile ? '18px 16px 18px' : compact ? '22px 20px 22px' : '24px 24px 26px',
      boxShadow: '0 18px 42px rgba(14,14,44,.05), inset 0 1px 0 rgba(255,255,255,.7)',
      backdropFilter: 'blur(18px)',
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
            Quick Start
          </div>
          <h3 style={{ fontSize: mobile ? 22 : 28, fontWeight: 450, lineHeight: 1.08, letterSpacing: '-0.04em', color: T.navy }}>
            Discover and remix content angles
          </h3>
          <p style={{ fontSize: 13, color: T.navyLight, lineHeight: 1.6, marginTop: 8, maxWidth: 520 }}>
            更像灵感展架，而不是普通模板列表。点进去就能直接生成，点「换一换」会切到另一组方向。
          </p>
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
                borderRadius: mobile ? 22 : 24,
                overflow: 'hidden',
                background: 'rgba(255,255,255,.9)',
                border: `1px solid rgba(14,14,44,.06)`,
                boxShadow: '0 8px 22px rgba(14,14,44,.05)',
                transition: 'transform .28s cubic-bezier(.2,.8,.2,1), box-shadow .28s cubic-bezier(.2,.8,.2,1)',
              }}
              onMouseEnter={e => {
                e.currentTarget.style.transform = 'translateY(-6px) scale(1.01)';
                e.currentTarget.style.boxShadow = '0 20px 40px rgba(14,14,44,.12)';
              }}
              onMouseLeave={e => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)';
                e.currentTarget.style.boxShadow = '0 8px 22px rgba(14,14,44,.05)';
              }}
            >
              <div style={{
                height: mobile ? 170 : compact ? 178 : 186,
                padding: 16,
                background: `linear-gradient(160deg, rgba(255,255,255,.76), rgba(255,255,255,.14)), ${it.tint}`,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
              }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 10 }}>
                  <span style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 6,
                    padding: '7px 10px',
                    borderRadius: 999,
                    background: 'rgba(255,255,255,.62)',
                    boxShadow: 'inset 0 0 0 1px rgba(255,255,255,.28)',
                    fontSize: 11,
                    fontWeight: 600,
                    color: it.accent,
                    letterSpacing: '0.02em',
                    backdropFilter: 'blur(8px)',
                  }}>
                    <Icon name="sparkles" size={10} color={it.accent} />
                    {it.tag}
                  </span>
                  <div style={{
                    width: 34,
                    height: 34,
                    borderRadius: 12,
                    background: 'rgba(255,255,255,.58)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backdropFilter: 'blur(8px)',
                  }}>
                    <span style={{ fontSize: 22 }}>{it.emoji}</span>
                  </div>
                </div>

                <div style={{
                  alignSelf: i === 1 && !mobile ? 'center' : 'flex-start',
                  transform: i === 1 && !mobile ? 'rotate(-5deg)' : i === 2 && !mobile ? 'rotate(4deg)' : 'rotate(0deg)',
                  width: i === 1 && !mobile ? '76%' : '100%',
                  height: mobile ? 76 : 88,
                  borderRadius: 18,
                  background: 'rgba(255,255,255,.48)',
                  boxShadow: 'inset 0 0 0 1px rgba(255,255,255,.28)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'rgba(14,14,44,.46)',
                }}>
                  <Icon name={i % 4 === 0 ? 'layers' : i % 4 === 1 ? 'image' : i % 4 === 2 ? 'quote' : 'pen'} size={30} />
                </div>
              </div>

              <div style={{ padding: '14px 14px 14px' }}>
                <div style={{ fontSize: 10.5, color: T.navyLight, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 8 }}>
                  快速开始
                </div>
                <div style={{ fontSize: 15, fontWeight: 600, color: T.navy, lineHeight: 1.24, marginBottom: 8, letterSpacing: '-0.01em' }}>
                  {it.title}
                </div>
                <div style={{ fontSize: 12.5, color: T.navyMid, lineHeight: 1.58, minHeight: mobile ? 'auto' : 58 }}>
                  {it.desc}
                </div>
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 14 }}>
                  <span style={{
                    height: 34,
                    padding: '0 12px',
                    borderRadius: 999,
                    border: `1px solid ${T.hairline}`,
                    background: T.white,
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

const HomePage = ({ onSubmit, onNavigate }) => {
  const { isCompact, isTablet, isMobile } = useViewport();
  const [text, setText] = React.useState('');
  const [format, setFormat] = React.useState(null);

  const submit = () => {
    if (text.trim()) {
      onSubmit(format ? `[${format.label} · ${format.sub}] ${text.trim()}` : text.trim());
    }
  };

  const sessions = [
    '猛男喜欢的粉色植物 · 小红书图文',
    '上海咖啡馆 City Walk Top 10',
    '租房避雷指南 v2',
    '产品测评 · AI 视频工具横评',
    '极简通勤穿搭一周 OOTD',
    '咖啡入门 12 个名词',
    '我和我的猫 · 7 个瞬间',
  ];

  return (
    <div style={{
      display: 'flex',
      height: '100%',
      width: '100%',
      background: T.surface,
      padding: isMobile ? 0 : 20,
    }}>
      <div style={{
        display: 'flex',
        flex: 1,
        background: T.white,
        borderRadius: isMobile ? 0 : 24,
        boxShadow: isMobile ? 'none' : '0 1px 3px rgba(14,14,44,.04)',
        overflow: 'hidden',
      }}>
        {!isTablet && (
          <Sidebar
            active="home"
            onNew={() => { setText(''); setFormat(null); }}
            onNavigate={onNavigate}
            sessions={sessions}
          />
        )}

        <main style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'auto',
          position: 'relative',
          background: 'linear-gradient(180deg, #ffffff 0%, #fbfcff 52%, #fafcfe 100%)',
        }}>
          <div style={{
            position: 'absolute',
            inset: 0,
            background: 'radial-gradient(circle at 52% 14%, rgba(214,255,0,.18), transparent 16%), radial-gradient(circle at 70% 18%, rgba(75,77,237,.07), transparent 18%), radial-gradient(circle at 34% 24%, rgba(243,219,218,.22), transparent 18%)',
            pointerEvents: 'none',
          }} />

          <div style={{
            height: isMobile ? 58 : 54,
            padding: isMobile ? '0 18px' : '0 24px',
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
                  <div style={{ fontSize: 15, fontWeight: 700, color: T.navy }}>Nori</div>
                  <div style={{ fontSize: 11, color: T.navyLight }}>v2.1 · creative system</div>
                </div>
              </div>
            ) : <div />}

            <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
              {isTablet && (
                <button onClick={() => onNavigate && onNavigate('library')} style={iconBtnStyle()}>
                  <Icon name="library" size={15} color={T.navyLight} />
                </button>
              )}
              <button style={iconBtnStyle()}><Icon name="bell" size={15} color={T.navyLight} /></button>
              <button style={iconBtnStyle()}><Icon name="settings" size={15} color={T.navyLight} /></button>
            </div>
          </div>

          <div style={{
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
            zIndex: 1,
          }}>
            <section style={{
              position: 'relative',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              padding: isMobile ? '14px 0 0' : '18px 0 0',
            }}>
              <div style={{ display: 'flex', justifyContent: 'center', marginBottom: isMobile ? 10 : 14 }}>
                <div style={{
                  borderRadius: isMobile ? 18 : 22,
                  boxShadow: '0 20px 40px rgba(214,255,0,.18), 0 4px 12px rgba(14,14,44,.08)',
                }}>
                  <NoriLogo size={isMobile ? 48 : 58} />
                </div>
              </div>

              <HeroHeadline compact={isCompact} mobile={isMobile} />

              <div style={{ width: '100%', maxWidth: 880 }}>
                <HomeComposer
                  value={text}
                  onChange={setText}
                  onSubmit={submit}
                  format={format}
                  onClearFormat={() => setFormat(null)}
                  compact={isCompact}
                  mobile={isMobile}
                />

                <div style={{ marginTop: 14 }}>
                  <FormatPicker format={format} onPick={setFormat} compact={isCompact} mobile={isMobile} />
                </div>
              </div>
            </section>

            <section>
              <QuickStart onPick={t => setText(`帮我做一篇 ${t}`)} compact={isCompact} mobile={isMobile} />
            </section>

            <section>
              <SkillSquare compact={isCompact} mobile={isMobile} />
            </section>
          </div>
        </main>
      </div>
    </div>
  );
};

const iconBtnStyle = () => ({
  width: 32,
  height: 32,
  borderRadius: 8,
  border: 'none',
  background: 'transparent',
  cursor: 'pointer',
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  transition: 'background .12s',
});

window.HomePage = HomePage;
window.Sidebar = Sidebar;
window.iconBtnStyle = iconBtnStyle;

/* ─── Assets Library ─── */

const platformMeta = {
  xhs: { label: '小红书', short: '红', tint: '#ffe5ec', accent: '#ff4488' },
  wechat: { label: '公众号', short: '微', tint: T.successTint, accent: T.success },
  podcast: { label: '播客', short: '播', tint: '#fff8e0', accent: '#c89b00' },
  short: { label: '短视频', short: '视', tint: T.irisTint, accent: T.iris },
  bilibili: { label: 'B 站', short: 'B', tint: '#e7f0f6', accent: '#557f98' },
};

const typeMeta = {
  graphic: { label: '图文', icon: 'image' },
  video: { label: '视频', icon: 'video' },
  text: { label: '文字', icon: 'document' },
};

const assetItems = [
  {
    id: 'a1',
    type: 'graphic',
    platform: 'xhs',
    title: '深蓝幕布下的粉蝶兰，谁懂这种反差感？',
    subtitle: '反差人设 + 6 种粉色植物种草',
    storedAt: '今天 19:24',
    iso: '2026-05-06T19:24:00+08:00',
    status: '已发布',
    ratio: '4 / 5',
    theme: { bg: '#1a3a5c', fg: '#f5b8c8', accent: '#2c5a3c', wash: '#fdf5f5' },
  },
  {
    id: 'a2',
    type: 'video',
    platform: 'short',
    title: 'AI 视频工具横评：哪些真的适合个人创作者',
    subtitle: '60s 口播脚本 + 分镜',
    storedAt: '今天 16:10',
    iso: '2026-05-06T16:10:00+08:00',
    status: '草稿',
    ratio: '16 / 10',
    theme: { bg: '#eceaf6', fg: '#7973b3', accent: '#d6ff00', wash: '#fbfcff' },
  },
  {
    id: 'a3',
    type: 'text',
    platform: 'wechat',
    title: '职场人的知识 IP 变现路径',
    subtitle: '把五年经验整理成可连载的观点文章',
    storedAt: '昨天 22:41',
    iso: '2026-05-05T22:41:00+08:00',
    status: '自动保存',
    excerpt: '一个可靠的知识 IP，不是把经验一次性倒出来，而是把一个领域拆成连续、可复用、可验证的表达系统。',
    theme: { bg: '#edf1ff', fg: '#4b4ded', accent: '#c4c4d4', wash: '#ffffff' },
  },
  {
    id: 'a4',
    type: 'graphic',
    platform: 'xhs',
    title: '上海咖啡馆 City Walk Top 10',
    subtitle: '路线策展 + 收藏型攻略',
    storedAt: '5 月 4 日',
    iso: '2026-05-04T14:12:00+08:00',
    status: '已发布',
    ratio: '1 / 1',
    theme: { bg: '#f2e7dc', fg: '#9c7352', accent: '#557f98', wash: '#fffaf4' },
  },
  {
    id: 'a5',
    type: 'video',
    platform: 'bilibili',
    title: 'Claude Code 深度解析：从需求到可运行原型',
    subtitle: '5 分钟长视频结构',
    storedAt: '5 月 2 日',
    iso: '2026-05-02T10:38:00+08:00',
    status: '草稿',
    ratio: '16 / 9',
    theme: { bg: '#e7f0f6', fg: '#557f98', accent: '#31d0aa', wash: '#f7fbff' },
  },
  {
    id: 'a6',
    type: 'text',
    platform: 'podcast',
    title: '创作者如何建立自己的素材复利',
    subtitle: '播客提纲 · 12 个问题',
    storedAt: '4 月 28 日',
    iso: '2026-04-28T21:08:00+08:00',
    status: '自动保存',
    excerpt: '素材库的价值不在数量，而在它能不能被重新点亮：一个观察、一句金句、一个案例，最后都要回到可被调用的结构里。',
    theme: { bg: '#fff8e0', fg: '#c89b00', accent: '#f3dbda', wash: '#fffdf5' },
  },
  {
    id: 'a7',
    type: 'graphic',
    platform: 'xhs',
    title: '租房避雷指南 v2：签合同前一定要看',
    subtitle: '收藏型清单 + 实用攻略',
    storedAt: '4 月 24 日',
    iso: '2026-04-24T12:16:00+08:00',
    status: '已发布',
    ratio: '3 / 4',
    theme: { bg: '#eef0f8', fg: '#6977ad', accent: '#af6280', wash: '#ffffff' },
  },
  {
    id: 'a8',
    type: 'video',
    platform: 'short',
    title: '极简通勤穿搭一周 OOTD',
    subtitle: '7 条短视频脚本',
    storedAt: '4 月 20 日',
    iso: '2026-04-20T18:35:00+08:00',
    status: '草稿',
    ratio: '9 / 12',
    theme: { bg: '#f8ece3', fg: '#ba7b52', accent: '#4b4ded', wash: '#fff8f2' },
  },
  {
    id: 'a9',
    type: 'graphic',
    platform: 'wechat',
    title: 'MCP 协议到底是什么？给产品经理的版本',
    subtitle: '长文 + 配图卡片',
    storedAt: '3 月 29 日',
    iso: '2026-03-29T09:22:00+08:00',
    status: '已发布',
    ratio: '16 / 10',
    theme: { bg: '#edf5ec', fg: '#5f8b66', accent: '#d6ff00', wash: '#fbfff7' },
  },
];

const FilterChip = ({ active, label, count, onClick }) => (
  <button
    type="button"
    onClick={onClick}
    style={{
      height: 34,
      padding: '0 12px',
      borderRadius: 999,
      border: `1px solid ${active ? 'rgba(14,14,44,.12)' : T.hairline}`,
      background: active ? T.navy : 'rgba(255,255,255,.74)',
      color: active ? T.white : T.navyMid,
      boxShadow: active ? T.shadowSm : 'none',
      fontSize: 12.5,
      fontWeight: active ? 650 : 520,
      cursor: 'pointer',
      display: 'inline-flex',
      alignItems: 'center',
      gap: 6,
      fontFamily: T.fontSans,
      transition: 'all .16s cubic-bezier(.2,.8,.2,1)',
    }}
  >
    {label}
    {typeof count === 'number' && (
      <span style={{
        minWidth: 19,
        height: 19,
        padding: '0 5px',
        borderRadius: 999,
        display: 'inline-flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: active ? 'rgba(214,255,0,.18)' : T.surface,
        color: active ? T.primary : T.navyLight,
        fontSize: 10.5,
        fontFamily: T.fontMono,
        fontWeight: 700,
      }}>{count}</span>
    )}
  </button>
);

const AssetArtwork = ({ asset, compact }) => {
  const meta = platformMeta[asset.platform];
  const type = typeMeta[asset.type];

  if (asset.type === 'text') {
    return (
      <div style={{
        padding: compact ? 16 : 18,
        minHeight: compact ? 172 : 198,
        borderRadius: compact ? 18 : 22,
        background: `linear-gradient(160deg, rgba(255,255,255,.82), rgba(255,255,255,.28)), ${asset.theme.bg}`,
        border: `1px solid rgba(14,14,44,.06)`,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        overflow: 'hidden',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 12 }}>
          <span style={{
            width: 36,
            height: 36,
            borderRadius: 12,
            background: 'rgba(255,255,255,.68)',
            color: asset.theme.fg,
            display: 'inline-flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'inset 0 0 0 1px rgba(255,255,255,.28)',
          }}>
            <Icon name="quote" size={17} />
          </span>
          <span style={{
            padding: '6px 9px',
            borderRadius: 999,
            background: meta.tint,
            color: meta.accent,
            fontSize: 11,
            fontWeight: 700,
          }}>{meta.label}</span>
        </div>
        <div style={{
          fontSize: compact ? 20 : 24,
          lineHeight: 1.15,
          letterSpacing: '-0.04em',
          color: T.navy,
          fontWeight: 560,
          maxWidth: '92%',
        }}>
          {asset.title}
        </div>
        <p style={{
          margin: 0,
          fontSize: 12.5,
          lineHeight: 1.65,
          color: T.navyMid,
          display: '-webkit-box',
          WebkitLineClamp: 3,
          WebkitBoxOrient: 'vertical',
          overflow: 'hidden',
        }}>{asset.excerpt}</p>
      </div>
    );
  }

  return (
    <div style={{
      position: 'relative',
      aspectRatio: asset.ratio || '4 / 5',
      minHeight: compact ? 168 : 190,
      borderRadius: compact ? 18 : 22,
      overflow: 'hidden',
      background: asset.theme.bg,
      border: `1px solid rgba(14,14,44,.06)`,
      boxShadow: 'inset 0 0 0 1px rgba(255,255,255,.12)',
    }}>
      <div style={{
        position: 'absolute',
        inset: 0,
        background: `radial-gradient(circle at 22% 20%, ${asset.theme.wash}, transparent 21%), radial-gradient(circle at 72% 28%, ${asset.theme.fg}, transparent 22%), radial-gradient(circle at 44% 76%, ${asset.theme.accent}, transparent 26%), linear-gradient(145deg, ${asset.theme.bg}, rgba(255,255,255,.32))`,
      }} />
      <div style={{
        position: 'absolute',
        inset: '18% 13% 18%',
        borderRadius: 22,
        background: 'rgba(255,255,255,.42)',
        border: '1px solid rgba(255,255,255,.38)',
        transform: asset.type === 'video' ? 'rotate(-4deg)' : 'rotate(3deg)',
        boxShadow: '0 20px 42px rgba(14,14,44,.12)',
      }} />
      <div style={{
        position: 'absolute',
        left: 16,
        right: 16,
        bottom: 16,
        display: 'flex',
        alignItems: 'flex-end',
        justifyContent: 'space-between',
        gap: 12,
      }}>
        <div style={{
          maxWidth: '78%',
          color: T.navy,
          fontSize: compact ? 22 : 28,
          lineHeight: 1.05,
          letterSpacing: '-0.045em',
          fontWeight: 720,
          textShadow: '0 1px 0 rgba(255,255,255,.42)',
        }}>{asset.title.split(/[：:，,]/)[0]}</div>
        <span style={{
          width: 42,
          height: 42,
          borderRadius: 14,
          background: 'rgba(255,255,255,.72)',
          color: asset.type === 'video' ? T.iris : asset.theme.fg,
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          backdropFilter: 'blur(10px)',
        }}>
          <Icon name={asset.type === 'video' ? 'play' : type.icon} size={18} />
        </span>
      </div>
      <div style={{
        position: 'absolute',
        top: 12,
        left: 12,
        display: 'inline-flex',
        alignItems: 'center',
        gap: 6,
        padding: '6px 9px',
        borderRadius: 999,
        background: 'rgba(255,255,255,.72)',
        color: meta.accent,
        fontSize: 11,
        fontWeight: 700,
        backdropFilter: 'blur(10px)',
      }}>
        <span style={{
          width: 18,
          height: 18,
          borderRadius: 999,
          background: meta.accent,
          color: T.white,
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: 10,
          fontWeight: 800,
        }}>{meta.short}</span>
        {meta.label}
      </div>
    </div>
  );
};

const AssetActionMenu = ({ asset, onAction }) => (
  <div
    onClick={e => e.stopPropagation()}
    style={{
      position: 'absolute',
      right: 12,
      bottom: 48,
      width: 154,
      padding: 6,
      borderRadius: 14,
      background: 'rgba(255,255,255,.94)',
      border: `1px solid ${T.hairline}`,
      boxShadow: T.shadowLg,
      backdropFilter: 'blur(18px)',
      zIndex: 5,
      animation: 'fadeIn .16s ease both',
    }}
  >
    {[
      { id: 'extend', label: 'Extend', icon: 'sparkles' },
      { id: 'download', label: '下载', icon: 'download' },
      { id: 'delete', label: '删除', icon: 'trash', danger: true },
    ].map(item => (
      <button
        key={item.id}
        type="button"
        onClick={() => onAction(item.id, asset)}
        style={{
          width: '100%',
          height: 36,
          border: 'none',
          borderRadius: 9,
          background: 'transparent',
          color: item.danger ? T.error : T.navy,
          cursor: 'pointer',
          fontSize: 12.5,
          fontWeight: 560,
          fontFamily: T.fontSans,
          display: 'flex',
          alignItems: 'center',
          gap: 9,
          padding: '0 10px',
          textAlign: 'left',
        }}
        onMouseEnter={e => e.currentTarget.style.background = item.danger ? 'rgba(229,57,53,.08)' : T.surface}
        onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
      >
        <Icon name={item.icon} size={14} />
        {item.label}
      </button>
    ))}
  </div>
);

const AssetCard = ({ asset, index, view, menuOpen, onToggleMenu, onOpen, onAction, compact }) => {
  const meta = platformMeta[asset.platform];
  const type = typeMeta[asset.type];
  const [hovered, setHovered] = React.useState(false);
  const list = view === 'list';

  return (
    <article
      onClick={() => onOpen(asset)}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        breakInside: 'avoid',
        display: list ? 'grid' : 'block',
        gridTemplateColumns: list ? (compact ? '112px minmax(0, 1fr)' : '184px minmax(0, 1fr)') : undefined,
        gap: list ? 16 : 0,
        width: '100%',
        marginBottom: list ? 12 : 18,
        padding: list ? 12 : 0,
        borderRadius: compact ? 22 : 26,
        background: 'rgba(255,255,255,.82)',
        border: `1px solid ${hovered ? 'rgba(75,77,237,.22)' : T.hairline}`,
        boxShadow: hovered ? '0 20px 42px rgba(14,14,44,.11)' : '0 8px 24px rgba(14,14,44,.05)',
        transform: hovered ? 'translateY(-4px)' : 'translateY(0)',
        transition: 'transform .24s cubic-bezier(.2,.8,.2,1), box-shadow .24s cubic-bezier(.2,.8,.2,1), border-color .24s',
        cursor: 'pointer',
        overflow: 'hidden',
        position: 'relative',
        animation: `fadeInScale .46s ${index * 55}ms both`,
      }}
    >
      {list ? (
        <div style={{ minWidth: 0 }}>
          <AssetArtwork asset={asset} compact />
        </div>
      ) : (
        <AssetArtwork asset={asset} compact={compact} />
      )}

      <div style={{
        padding: list ? '4px 8px 4px 0' : compact ? '14px 14px 14px' : '15px 16px 16px',
        minWidth: 0,
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        gap: list ? 18 : 12,
      }}>
        <div>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            flexWrap: 'wrap',
            marginBottom: 8,
          }}>
            <span style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 5,
              height: 24,
              padding: '0 8px',
              borderRadius: 999,
              background: meta.tint,
              color: meta.accent,
              fontSize: 11.5,
              fontWeight: 700,
            }}>
              <Icon name={type.icon} size={11} />
              {meta.label} · {type.label}
            </span>
            <span style={{
              height: 24,
              padding: '0 8px',
              borderRadius: 999,
              background: T.surface,
              color: T.navyLight,
              fontSize: 11.5,
              fontWeight: 600,
              display: 'inline-flex',
              alignItems: 'center',
            }}>{asset.status}</span>
          </div>

          <h3 style={{
            margin: 0,
            fontSize: list ? 16 : 15.5,
            lineHeight: 1.35,
            letterSpacing: '-0.02em',
            color: T.navy,
            fontWeight: 680,
            display: '-webkit-box',
            WebkitLineClamp: list ? 1 : 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}>{asset.title}</h3>
          <p style={{
            margin: '6px 0 0',
            fontSize: 12.5,
            lineHeight: 1.55,
            color: T.navyMid,
            display: '-webkit-box',
            WebkitLineClamp: list ? 1 : 2,
            WebkitBoxOrient: 'vertical',
            overflow: 'hidden',
          }}>{asset.subtitle}</p>
        </div>

        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 10,
          color: T.navyLight,
          fontSize: 11.5,
        }}>
          <span style={{ display: 'inline-flex', alignItems: 'center', gap: 5 }}>
            <Icon name="clock" size={12} />
            {asset.storedAt}
          </span>
          <button
            type="button"
            onClick={e => {
              e.stopPropagation();
              onToggleMenu(asset.id);
            }}
            style={{
              width: 30,
              height: 30,
              borderRadius: 9,
              border: 'none',
              background: menuOpen ? T.surface : 'transparent',
              color: T.navyLight,
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <Icon name="moreH" size={15} />
          </button>
        </div>
      </div>

      {menuOpen && <AssetActionMenu asset={asset} onAction={onAction} />}
    </article>
  );
};

const AssetsPage = ({ onNavigate, onOpenAsset, onNew }) => {
  const { isCompact, isTablet, isMobile } = useViewport();
  const [query, setQuery] = React.useState('');
  const [platform, setPlatform] = React.useState('all');
  const [kind, setKind] = React.useState('all');
  const [time, setTime] = React.useState('all');
  const [sort, setSort] = React.useState('newest');
  const [view, setView] = React.useState('grid');
  const [menuId, setMenuId] = React.useState(null);
  const [deleted, setDeleted] = React.useState({});
  const [toast, setToast] = React.useState('');

  React.useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(''), 1600);
    return () => clearTimeout(t);
  }, [toast]);

  const visibleAssets = assetItems.filter(a => !deleted[a.id]);
  const matchesTime = (asset) => {
    if (time === 'all') return true;
    const days = (Date.now() - new Date(asset.iso).getTime()) / 86400000;
    if (time === 'today') return days < 1;
    if (time === 'week') return days < 7;
    return days < 31;
  };

  const filtered = visibleAssets
    .filter(asset => platform === 'all' || asset.platform === platform)
    .filter(asset => kind === 'all' || asset.type === kind)
    .filter(matchesTime)
    .filter(asset => {
      const text = `${asset.title} ${asset.subtitle} ${platformMeta[asset.platform].label} ${typeMeta[asset.type].label}`.toLowerCase();
      return text.includes(query.trim().toLowerCase());
    })
    .sort((a, b) => sort === 'newest'
      ? new Date(b.iso).getTime() - new Date(a.iso).getTime()
      : new Date(a.iso).getTime() - new Date(b.iso).getTime());

  const platformTabs = [
    { key: 'all', label: '全部' },
    { key: 'xhs', label: '小红书' },
    { key: 'wechat', label: '公众号' },
    { key: 'podcast', label: '播客' },
    { key: 'short', label: '短视频' },
    { key: 'bilibili', label: 'B 站' },
  ];
  const typeTabs = [
    { key: 'all', label: '全部形态' },
    { key: 'graphic', label: '图文' },
    { key: 'video', label: '视频' },
    { key: 'text', label: '文字' },
  ];
  const timeTabs = [
    { key: 'all', label: '全部时间' },
    { key: 'today', label: '今天' },
    { key: 'week', label: '近 7 天' },
    { key: 'month', label: '近 30 天' },
  ];

  const countFor = (key) => key === 'all'
    ? visibleAssets.length
    : visibleAssets.filter(a => a.platform === key).length;

  const handleAction = (action, asset) => {
    setMenuId(null);
    if (action === 'delete') {
      setDeleted(prev => ({ ...prev, [asset.id]: true }));
      setToast('已删除');
      return;
    }
    if (action === 'download') {
      setToast('已准备下载');
      return;
    }
    onOpenAsset({ ...asset, title: `${asset.title} · Extend` });
  };

  const controlSurface = {
    height: 46,
    borderRadius: 17,
    border: `1px solid ${T.hairline}`,
    background: 'rgba(255,255,255,.78)',
    boxShadow: T.shadowXs,
    backdropFilter: 'blur(18px)',
  };

  return (
    <div style={{
      display: 'flex',
      height: '100%',
      width: '100%',
      background: T.surface,
      padding: isMobile ? 0 : 20,
    }}>
      <div style={{
        display: 'flex',
        flex: 1,
        background: T.white,
        borderRadius: isMobile ? 0 : 24,
        boxShadow: isMobile ? 'none' : '0 1px 3px rgba(14,14,44,.04)',
        overflow: 'hidden',
      }}>
        {!isTablet && (
          <Sidebar active="library" onNew={onNew} onNavigate={onNavigate} sessions={assetItems.slice(0, 6).map(a => a.title)} />
        )}

        <main style={{
          flex: 1,
          minWidth: 0,
          overflow: 'auto',
          position: 'relative',
          background: 'linear-gradient(180deg, #ffffff 0%, #fbfcff 48%, #f6f9fc 100%)',
        }}>
          <div style={{
            position: 'absolute',
            inset: 0,
            background: 'radial-gradient(circle at 18% 10%, rgba(214,255,0,.16), transparent 18%), radial-gradient(circle at 76% 12%, rgba(75,77,237,.07), transparent 21%), radial-gradient(circle at 54% 0%, rgba(243,219,218,.20), transparent 17%)',
            pointerEvents: 'none',
          }} />

          <div style={{
            position: 'sticky',
            top: 0,
            zIndex: 10,
            padding: isMobile ? '14px 16px 10px' : isTablet ? '18px 24px 12px' : '24px 36px 14px',
            background: 'linear-gradient(180deg, rgba(255,255,255,.92), rgba(255,255,255,.72))',
            backdropFilter: 'blur(18px)',
            borderBottom: `1px solid ${T.hairlineSoft}`,
          }}>
            <div style={{
              display: 'flex',
              alignItems: isMobile ? 'flex-start' : 'center',
              justifyContent: 'space-between',
              gap: 14,
              marginBottom: 16,
              flexWrap: 'wrap',
            }}>
              <div style={{ minWidth: 0 }}>
                {isTablet && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 14 }}>
                    <NoriLogo size={26} />
                    <div>
                      <div style={{ fontSize: 15, fontWeight: 700, color: T.navy }}>Nori</div>
                      <div style={{ fontSize: 11, color: T.navyLight }}>v2.1 · creative system</div>
                    </div>
                  </div>
                )}
                <div style={{ fontSize: 12, color: T.navyLight, marginBottom: 6, letterSpacing: '0.08em', textTransform: 'uppercase' }}>
                  Assets
                </div>
                <h1 style={{
                  margin: 0,
                  fontSize: isMobile ? 28 : 36,
                  lineHeight: 1.05,
                  letterSpacing: '-0.045em',
                  fontWeight: 520,
                  color: T.navy,
                }}>我的内容库</h1>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                {isTablet && (
                  <button
                    type="button"
                    onClick={() => onNavigate('home')}
                    style={{
                      ...controlSurface,
                      padding: '0 14px',
                      color: T.navy,
                      fontSize: 13,
                      fontWeight: 650,
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: 7,
                      fontFamily: T.fontSans,
                    }}
                  >
                    <Icon name="home" size={14} />
                    首页
                  </button>
                )}
                <button
                  type="button"
                  onClick={onNew}
                  style={{
                    ...controlSurface,
                    padding: '0 16px',
                    background: T.navy,
                    color: T.primary,
                    fontSize: 13,
                    fontWeight: 700,
                    cursor: 'pointer',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 8,
                    fontFamily: T.fontSans,
                  }}
                >
                  <Icon name="plus" size={14} />
                  新建
                </button>
              </div>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: isMobile ? '1fr' : 'minmax(240px, 1fr) auto auto',
              gap: 10,
              alignItems: 'center',
            }}>
              <label style={{
                ...controlSurface,
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                padding: '0 14px',
              }}>
                <Icon name="search" size={17} color={T.navyLight} />
                <input
                  value={query}
                  onChange={e => setQuery(e.target.value)}
                  placeholder="Search assets..."
                  style={{
                    flex: 1,
                    minWidth: 0,
                    border: 'none',
                    outline: 'none',
                    background: 'transparent',
                    color: T.navy,
                    fontSize: 14,
                    fontFamily: T.fontSans,
                  }}
                />
              </label>

              <button
                type="button"
                onClick={() => setSort(v => v === 'newest' ? 'oldest' : 'newest')}
                style={{
                  ...controlSurface,
                  padding: '0 15px',
                  color: T.navy,
                  fontSize: 13,
                  fontWeight: 650,
                  cursor: 'pointer',
                  display: 'inline-flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 8,
                  fontFamily: T.fontSans,
                }}
              >
                <Icon name="filter" size={15} color={T.navyMid} />
                {sort === 'newest' ? 'Newest' : 'Oldest'}
              </button>

              <div style={{
                ...controlSurface,
                padding: 4,
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: 3,
                minWidth: isMobile ? '100%' : 100,
              }}>
                {[
                  { key: 'grid', icon: 'grid' },
                  { key: 'list', icon: 'list' },
                ].map(item => (
                  <button
                    key={item.key}
                    type="button"
                    onClick={() => setView(item.key)}
                    style={{
                      border: 'none',
                      borderRadius: 13,
                      background: view === item.key ? T.white : 'transparent',
                      color: view === item.key ? T.navy : T.navyLight,
                      boxShadow: view === item.key ? T.shadowXs : 'none',
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                    }}
                  >
                    <Icon name={item.icon} size={17} />
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div style={{
            position: 'relative',
            zIndex: 1,
            maxWidth: 1240,
            margin: '0 auto',
            padding: isMobile ? '18px 16px 36px' : isTablet ? '22px 24px 42px' : '26px 36px 52px',
          }}>
            <div style={{ display: 'grid', gap: 12, marginBottom: 22 }}>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, alignItems: 'center' }}>
                {platformTabs.map(tab => (
                  <FilterChip
                    key={tab.key}
                    active={platform === tab.key}
                    label={tab.label}
                    count={countFor(tab.key)}
                    onClick={() => setPlatform(tab.key)}
                  />
                ))}
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, alignItems: 'center' }}>
                {typeTabs.map(tab => (
                  <FilterChip
                    key={tab.key}
                    active={kind === tab.key}
                    label={tab.label}
                    onClick={() => setKind(tab.key)}
                  />
                ))}
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, alignItems: 'center', justifyContent: 'space-between' }}>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                  {timeTabs.map(tab => (
                    <FilterChip
                      key={tab.key}
                      active={time === tab.key}
                      label={tab.label}
                      onClick={() => setTime(tab.key)}
                    />
                  ))}
                </div>
                <span style={{ fontSize: 12, color: T.navyLight, fontFamily: T.fontMono }}>
                  {filtered.length} / {visibleAssets.length}
                </span>
              </div>
            </div>

            {filtered.length ? (
              <div
                key={`${platform}-${kind}-${time}-${query}-${sort}-${view}`}
                style={view === 'grid' ? {
                  columnCount: isMobile ? 1 : isCompact ? 2 : 3,
                  columnGap: isMobile ? 14 : 18,
                } : {
                  display: 'grid',
                  gap: 2,
                }}
              >
                {filtered.map((asset, index) => (
                  <AssetCard
                    key={asset.id}
                    asset={asset}
                    index={index}
                    view={view}
                    compact={isMobile}
                    menuOpen={menuId === asset.id}
                    onToggleMenu={id => setMenuId(menuId === id ? null : id)}
                    onOpen={onOpenAsset}
                    onAction={handleAction}
                  />
                ))}
              </div>
            ) : (
              <div style={{
                minHeight: 360,
                borderRadius: 26,
                border: `1px solid ${T.hairline}`,
                background: 'rgba(255,255,255,.72)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: T.navyLight,
                fontSize: 13,
                boxShadow: T.shadowXs,
              }}>
                没有找到匹配的内容
              </div>
            )}
          </div>

          {toast && (
            <div style={{
              position: 'fixed',
              left: '50%',
              bottom: 28,
              transform: 'translateX(-50%)',
              zIndex: 50,
              padding: '10px 14px',
              borderRadius: 999,
              background: T.navy,
              color: T.primary,
              fontSize: 12.5,
              fontWeight: 700,
              boxShadow: T.shadowLg,
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              animation: 'fadeIn .18s ease both',
            }}>
              <Icon name="check" size={13} />
              {toast}
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

window.AssetsPage = AssetsPage;
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
  return <NoriLogo size={28} />;
};

const Bubble = ({ from = 'nori', children, style }) => {
  const isUser = from === 'user';
  return (
    <div style={{
      display: 'flex', gap: 10, alignItems: 'flex-start',
      flexDirection: isUser ? 'row-reverse' : 'row',
      animation: 'fadeIn .32s ease both',
      ...style,
    }}>
      <Avatar kind={isUser ? 'user' : 'nori'} />
      <div style={{
        maxWidth: '92%', padding: isUser ? '10px 14px' : 0,
        borderRadius: isUser ? 14 : 0,
        background: isUser ? T.navy : 'transparent',
        color: isUser ? T.white : T.navy,
        fontSize: 14, lineHeight: 1.65, fontWeight: 450,
        flex: isUser ? '0 1 auto' : '1 1 auto',
      }}>
        {children}
      </div>
    </div>
  );
};

const NoriSays = ({ children, style }) => (
  <Bubble from="nori" style={style}>
    <div style={{ paddingTop: 4, fontSize: 14, lineHeight: 1.7, color: T.navy, fontWeight: 450 }}>
      {children}
    </div>
  </Bubble>
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
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
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
              transition: 'all .12s',
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
        background: T.white, border: `1px solid ${T.hairline}`,
        borderRadius: 14, padding: '18px 20px', boxShadow: T.shadowXs,
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
              transition: 'all .15s',
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
      background: T.white, border: `1px solid ${T.hairline}`,
      borderRadius: 14, overflow: 'hidden',
      cursor: 'pointer', transition: 'all .15s',
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

  return (
    <>
      <NoriSays>
        <p style={{ marginBottom: 14 }}>
          收到，开始动了 ✨ 我先去小红书 / 抖音上扒了一圈 <b>粉色植物</b> 相关爆款，
          这个话题有真实的流量盘子 —— 近 30 天爆款 200+ 篇，平均互动率 5.8%，
          <span style={{ color: T.success, fontWeight: 600 }}>「可打造为爆款」诊断通过</span>。
        </p>
        <p style={{ marginBottom: 14, color: T.navyMid }}>
          下面是 4 篇可参考的爆款，已按选题贴合度排序 ——
        </p>
      </NoriSays>

      <div style={{ marginLeft: 38, marginTop: -6 }}>
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

      {/* 拆解 */}
      <NoriSays style={{ marginTop: 22 }}>
        <p style={{ marginBottom: 14 }}>我把这些爆款的共同结构拆给你看 ——</p>
        <div style={{
          background: T.white, border: `1px solid ${T.hairline}`,
          borderRadius: 14, padding: '4px 0', overflow: 'hidden',
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

      {/* 选题结论卡片 */}
      <NoriSays style={{ marginTop: 22 }}>
        <p style={{ marginBottom: 14 }}>
          综合上面的拆解，我给你的选题结论是 ——
          <span style={{ color: T.navyLight, fontSize: 12.5 }}>（点击展开右边 Canvas 查看完整策略）</span>
        </p>
        <button onClick={() => onSelectAngle()} style={{
          width: '100%', textAlign: 'left',
          background: T.white, border: `1px solid ${T.hairline}`,
          borderRadius: 14, padding: '14px 18px',
          display: 'flex', alignItems: 'center', gap: 14,
          cursor: 'pointer', transition: 'all .15s',
        }}
          onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(75,77,237,.32)'; e.currentTarget.style.boxShadow = T.shadowSm; }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = T.hairline; e.currentTarget.style.boxShadow = 'none'; }}>
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
              小红书图文 · 8 张图 · 预估爆款率 72% · Nori 推荐
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

const Step3Research = () => {
  const [imgsExpanded, setImgsExpanded] = React.useState(false);

  const sources = [
    { title: '《观赏植物色素分布与花色稳定性研究》', host: 'cnki.net', kind: 'PDF · 论文', icon: 'book', tint: T.irisTint, color: T.iris },
    { title: '粉掌、姬秋丽、花叶冷水花养护要点', host: 'huayuan.com', kind: '科普文章', icon: 'document', tint: '#fff8e0', color: '#c89b00' },
    { title: 'Pink Plants Care Guide 2025', host: 'gardenista.com', kind: '英文 Guide', icon: 'globe', tint: T.successTint, color: T.success },
    { title: '【粉色植物 Top10】完整盘点', host: 'bilibili.com', kind: '视频 · 7:32', icon: 'play', tint: '#ffe5ec', color: '#ff4488' },
  ];

  /* image grid: 4 highlighted + 8 hidden */
  const Img = ({ palette, w = 1, h = 1 }) => (
    <div style={{
      borderRadius: 10, overflow: 'hidden',
      background: palette[0], aspectRatio: `${w} / ${h}`,
      cursor: 'pointer', transition: 'transform .15s',
      position: 'relative',
    }}
      onMouseEnter={e => e.currentTarget.style.transform = 'scale(1.02)'}
      onMouseLeave={e => e.currentTarget.style.transform = 'scale(1)'}>
      <FlowerVisual palette={palette} />
      <div style={{
        position: 'absolute', top: 6, right: 6,
        width: 22, height: 22, borderRadius: 6,
        background: 'rgba(0,0,0,.5)', color: T.white,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        backdropFilter: 'blur(4px)', opacity: 0,
        transition: 'opacity .15s',
      }}>
        <Icon name="expand" size={11} />
      </div>
    </div>
  );

  const palettes = [
    ['#1a3a5c', '#2c5a3c', '#f5b8c8', '#e896b0', '#fdf5f5'],
    ['#2a1a2e', '#3c5a4c', '#fab1c4', '#f78bb0', T.peachTint],
    ['#fdf0ee', '#9bbfa8', '#e8a0bc', '#d987a8', '#fff'],
    ['#3a2c4a', '#5c7a5c', '#f0a8c4', '#dc8aa8', '#fff'],
    ['#0e2a3a', '#3c4a3c', '#ffb8c8', '#ff8aa8', '#fff'],
    ['#2c1a3a', '#5c3c5c', '#f8a8c0', '#e890b0', '#fff'],
    ['#fce5ec', '#a8c8a8', '#dc8aa8', '#b86890', '#fff'],
    ['#1a2a3a', '#5c7a4c', '#f0c0d0', '#e090b0', '#fff'],
    ['#3a1a2a', '#4c5a4c', '#ffa0c0', '#d088a8', '#fff'],
    ['#fdf5f5', '#88aa88', '#e890a8', '#b87090', '#fff'],
    ['#22334a', '#4a6a4a', '#fcb4cc', '#e088a8', '#fff'],
    ['#2a2a3c', '#5a7a5a', '#f8a0c0', '#cc7898', '#fff'],
  ];

  return (
    <>
      <NoriSays>
        <p style={{ marginBottom: 14 }}>
          策略定了，我开始为你调研素材。先扒了一圈学术论文 + 科普文章 + 视频 ——
        </p>
        <div style={{
          background: T.white, border: `1px solid ${T.hairline}`,
          borderRadius: 14, padding: 6, overflow: 'hidden',
        }}>
          {sources.map((s, i) => <SourceRow key={i} source={s} idx={i} />)}
        </div>
        <button style={{
          marginTop: 8, fontSize: 12, color: T.navyMid,
          background: 'transparent', border: 'none', cursor: 'pointer',
          fontWeight: 500, display: 'inline-flex', alignItems: 'center', gap: 4, padding: '4px 0',
        }}>
          查看其余 5 个来源 <Icon name="chevronDown" size={11} />
        </button>
      </NoriSays>

      <NoriSays style={{ marginTop: 22 }}>
        <p style={{ marginBottom: 12 }}>
          再扒了一些粉色植物的图片素材 —— 高亮的这 4 张是我觉得封面 / 主图最能用的：
        </p>
        <div style={{
          display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8,
        }}>
          {palettes.slice(0, 4).map((p, i) => (
            <div key={i} style={{ position: 'relative' }}>
              <Img palette={p} w={1} h={1.25} />
              <div style={{
                position: 'absolute', top: 6, left: 6,
                fontSize: 9, fontWeight: 700, letterSpacing: '0.04em',
                color: T.navy, background: T.primary,
                padding: '2px 6px', borderRadius: 4,
              }}>★ TOP {i + 1}</div>
            </div>
          ))}
        </div>

        {imgsExpanded && (
          <div style={{
            display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 8,
            marginTop: 8, animation: 'fadeIn .3s ease',
          }}>
            {palettes.slice(4).map((p, i) => <Img key={i} palette={p} w={1} h={1.25} />)}
          </div>
        )}

        <button onClick={() => setImgsExpanded(v => !v)} style={{
          marginTop: 12, fontSize: 12, color: T.navyMid,
          background: 'transparent', border: 'none', cursor: 'pointer',
          fontWeight: 500, display: 'inline-flex', alignItems: 'center', gap: 4, padding: '4px 0',
        }}>
          {imgsExpanded ? '收起' : `查看其余 ${palettes.length - 4} 张图片`}
          <Icon name={imgsExpanded ? 'chevronDown' : 'chevronRight'} size={11} />
        </button>

        <div style={{
          marginTop: 14, display: 'inline-flex', alignItems: 'center', gap: 6,
          padding: '6px 12px', borderRadius: 99,
          background: T.successTint, color: T.success,
          fontSize: 12, fontWeight: 600,
        }}>
          <Icon name="check" size={12} /> 素材搜集完成 · 9 篇资料 + 12 张图
        </div>
      </NoriSays>
    </>
  );
};

/* ── Step 4: 内容生成 TODO 列表 ── */

const Step4Generate = ({ onAllDone }) => {
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
        background: T.white, border: `1px solid ${T.hairline}`,
        borderRadius: 14, padding: '12px 16px', overflow: 'hidden',
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
        <div style={{
          marginTop: 14, display: 'flex', alignItems: 'center', gap: 10,
          padding: '12px 16px', borderRadius: 12,
          background: `linear-gradient(135deg, ${T.primary}, #f0ff99)`,
          color: T.navy, fontWeight: 600, fontSize: 13.5,
          animation: 'fadeInScale .4s ease',
          position: 'relative', overflow: 'hidden',
        }}>
          <div style={{ position: 'relative' }}>
            <div style={{
              position: 'absolute', inset: -8,
              border: `2px solid ${T.navy}`, borderRadius: '50%',
              animation: 'successRing .9s ease',
            }} />
            <Icon name="sparkles" size={18} />
          </div>
          <span>全部完成！内容已就绪，去 Canvas 看看吧 ✨</span>
        </div>
      )}
    </NoriSays>
  );
};











/* ─── Canvas: editable preview + toolbar ─── */

const CanvasToolbar = ({ onClose, onTransform, onPublish, mode, setMode, expanded, setExpanded }) => {
  const Btn = ({ icon, label, onClick, primary, ghost, dark, children }) => {
    const [hov, setHov] = React.useState(false);
    return (
      <button onClick={onClick}
        onMouseEnter={() => setHov(true)} onMouseLeave={() => setHov(false)}
        style={{
          height: 34, padding: label ? '0 12px' : '0 8px', borderRadius: 8,
          border: 'none', cursor: 'pointer',
          background: primary ? T.iris : (hov ? 'rgba(255,255,255,.1)' : 'transparent'),
          color: primary ? T.white : (dark ? T.white : T.navyMid),
          fontSize: 12.5, fontWeight: 600,
          display: 'inline-flex', alignItems: 'center', gap: 6,
          transition: 'all .12s',
        }}>
        {icon && <Icon name={icon} size={14} />}
        {label}
        {children}
      </button>
    );
  };

  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '8px 12px',
      background: T.navy,
      borderRadius: 12,
      boxShadow: T.shadowLg,
      gap: 6,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
        <Btn icon="plus" dark />
        <Btn icon="transform" dark onClick={onTransform} />
        <span style={{ width: 1, height: 20, background: 'rgba(255,255,255,.15)', margin: '0 4px' }} />
        {/* segmented mode toggle: phone | edit */}
        <div style={{
          display: 'inline-flex', background: 'rgba(255,255,255,.06)', borderRadius: 8, padding: 3, gap: 2,
        }}>
          {[
            { id: 'preview', icon: 'phone' },
            { id: 'edit', icon: 'edit' },
          ].map(m => (
            <button key={m.id} onClick={() => setMode(m.id)} style={{
              height: 28, width: 36, borderRadius: 6,
              border: 'none', cursor: 'pointer',
              background: mode === m.id ? T.white : 'transparent',
              color: mode === m.id ? T.navy : 'rgba(255,255,255,.7)',
              display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
              transition: 'all .12s',
            }}>
              <Icon name={m.icon} size={14} />
            </button>
          ))}
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
        <button onClick={onPublish} style={{
          height: 34, padding: '0 16px', borderRadius: 8,
          background: T.iris, color: T.white,
          border: 'none', cursor: 'pointer',
          fontSize: 13, fontWeight: 700,
          display: 'inline-flex', alignItems: 'center', gap: 6,
          boxShadow: '0 2px 6px rgba(75,77,237,.4)',
        }}>
          <Icon name="paperPlane" size={14} /> 发布
        </button>
        <Btn icon="download" dark />
        <Btn icon={expanded ? 'collapse' : 'expand'} dark onClick={() => setExpanded(v => !v)} />
        <Btn icon="close" dark onClick={onClose} />
      </div>
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
const PostPreview = ({ data, onSetData, onSelectText }) => {
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

  return (
    <div onMouseUp={handleMouseUp} style={{
      width: 380, margin: '0 auto',
      background: T.white,
      borderRadius: 22, overflow: 'hidden',
      boxShadow: T.shadowXl,
      border: `1px solid ${T.hairline}`,
      position: 'relative',
    }}>
      {/* Cover */}
      <div style={{
        aspectRatio: '3 / 4', background: '#1a3a5c',
        position: 'relative', overflow: 'hidden',
      }}>
        <FlowerVisual palette={['#1a3a5c', '#2c5a3c', '#f5b8c8', '#e896b0', '#fdf5f5']} />
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
      <div style={{ padding: '18px 20px 22px' }}>
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
          📍 上海 · 8 张图 · 预估阅读 1 分钟
        </div>
      </div>
    </div>
  );
};

const makeCanvasData = (asset) => ({
  title: asset ? asset.title : '深蓝幕布下的粉蝶兰\n谁懂这种反差感？',
  tags: asset
    ? [platformMeta[asset.platform]?.label || '内容', typeMeta[asset.type]?.label || '生成', asset.status]
    : ['粉色植物', '猛男养花', '室内绿植'],
  hook: asset ? asset.subtitle : '硬汉的家里，最浪漫的 6 盆粉色植物 🌸',
  intro: asset?.excerpt || (asset
    ? '这是一份从内容库打开的已保存内容。你可以继续编辑正文、补充素材、重新发布，或把它转换为其他平台形态。'
    : '别再以为粉色只属于女孩房间。健身房 + 一盆粉蝶兰 = 顶级反差感。我家这 6 盆，每一盆都被来串门的兄弟问爆。'),
  items: asset ? [
    { name: '内容定位', desc: `${platformMeta[asset.platform]?.label || '内容平台'} · ${typeMeta[asset.type]?.label || '生成内容'} · ${asset.status}` },
    { name: '核心结构', desc: asset.subtitle },
    { name: '下一步编辑', desc: '支持继续扩展、重写段落、转换成视频脚本或重新发布。' },
    { name: '保存记录', desc: `存储时间：${asset.storedAt}` },
  ] : [
    { name: '粉蝶兰 Phalaenopsis', desc: '花期长达 3 个月，对光线宽容，办公桌 / 茶几都能放。深色背景下的拍照效果尤其惊艳。' },
    { name: '姬秋丽 Graptopetalum', desc: '多肉里的颜值天花板。叶片粉嫩，全日照下会更红，懒人也养得活。' },
    { name: '花叶冷水花 Pilea', desc: '叶脉粉条纹，散光环境长得最好。喜欢湿度，浴室窗台一绝。' },
    { name: '粉掌 Anthurium', desc: '佛焰苞像 wax 质感，热带植物里的颜值担当。每周一次浸盆即可。' },
  ],
  cta: asset ? '继续编辑后，可直接发布、下载，或 Extend 成新的内容版本。' : '👇 你家有几盆？硬汉能 hold 住几种？评论区比个高低～',
});

const Canvas = ({ open, expanded, setExpanded, onClose, onTransform, onPublish, mode, setMode, asset }) => {
  const [data, setData] = React.useState(() => makeCanvasData(asset));

  const [textMenu, setTextMenu] = React.useState(null);
  const handleTextAction = (act) => {
    setTextMenu(null);
    window.getSelection().removeAllRanges();
    // Hook into chat: dispatched action would land in chat as a follow-up
    if (window.__noriOnTextAction) window.__noriOnTextAction(act);
  };

  if (!open) return null;

  const canvasPlatform = asset ? (platformMeta[asset.platform]?.label || '内容') : '小红书';
  const canvasTitle = asset ? asset.title : '深蓝幕布下的粉蝶兰';

  return (
    <aside style={{
      width: expanded ? '100%' : 540,
      flexShrink: 0,
      height: '100%',
      background: T.surface,
      borderLeft: `1px solid ${T.hairline}`,
      display: 'flex', flexDirection: 'column',
      animation: 'slideInRight .35s ease',
      position: expanded ? 'absolute' : 'relative',
      right: 0, top: 0, zIndex: 20,
    }}>
      {/* Header strip */}
      <div style={{
        padding: '12px 16px',
        borderBottom: `1px solid ${T.hairline}`,
        background: T.surfaceWh,
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', color: T.navyLight }}>Canvas</span>
          <span style={{ fontSize: 11, color: T.navyLight }}>·</span>
          <span style={{ fontSize: 12.5, fontWeight: 600, color: T.navy, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', maxWidth: 280 }}>
            {canvasPlatform} · {canvasTitle}
          </span>
          <span style={{
            padding: '1px 7px', borderRadius: 4,
            background: T.successTint, color: T.success,
            fontSize: 10, fontWeight: 700, letterSpacing: '0.04em', marginLeft: 4,
          }}>已自动保存</span>
        </div>
        <span style={{ fontSize: 11, color: T.navyLight, fontFamily: T.fontMono }}>v1 · 14:32</span>
      </div>

      {/* Preview area */}
      <div style={{
        flex: 1, overflow: 'auto', padding: '32px 24px 100px',
        position: 'relative',
        background: 'radial-gradient(circle at 50% 0%, rgba(75,77,237,.05), transparent 60%)',
      }}>
        <PostPreview data={data} onSetData={setData} onSelectText={setTextMenu} />
        <TextSelectionMenu pos={textMenu} onAction={handleTextAction} onClose={() => setTextMenu(null)} />
      </div>

      {/* Floating bottom toolbar */}
      <div style={{
        position: 'absolute', bottom: 24, left: '50%',
        transform: 'translateX(-50%)',
        zIndex: 30, width: 'auto',
      }}>
        <CanvasToolbar
          onClose={onClose}
          onTransform={onTransform}
          onPublish={onPublish}
          mode={mode} setMode={setMode}
          expanded={expanded} setExpanded={setExpanded}
        />
      </div>
    </aside>
  );
};




/* ─── Generation Page: orchestrates 4 chat steps + Canvas ─── */

const StepperRail = ({ stage }) => {
  const steps = [
    { id: 1, label: '关键信息' },
    { id: 2, label: '爆款拆解' },
    { id: 3, label: '素材调研' },
    { id: 4, label: '内容生成' },
  ];
  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: 6,
      padding: '8px 14px', borderRadius: 99,
      background: T.white, border: `1px solid ${T.hairline}`,
      boxShadow: T.shadowXs,
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

const ChatComposer = ({ onSend, placeholder = '继续追问 Nori，或描述你的想法…' }) => {
  const [text, setText] = React.useState('');
  const [focused, setFocused] = React.useState(false);
  return (
    <div style={{
      background: T.white, borderRadius: 16,
      border: `1px solid ${focused ? 'rgba(75,77,237,.3)' : T.hairline}`,
      boxShadow: focused ? `0 0 0 4px rgba(75,77,237,.1), ${T.shadowSm}` : T.shadowXs,
      padding: '14px 16px 10px',
      transition: 'all .15s',
    }}>
      <textarea
        value={text} onChange={e => setText(e.target.value)}
        onFocus={() => setFocused(true)} onBlur={() => setFocused(false)}
        onKeyDown={e => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (text.trim()) { onSend(text.trim()); setText(''); }
          }
        }}
        placeholder={placeholder}
        rows={1}
        style={{
          width: '100%', border: 'none', outline: 'none',
          resize: 'none', background: 'transparent',
          fontSize: 14, lineHeight: 1.5, color: T.navy,
          fontFamily: T.fontSans, minHeight: 24, maxHeight: 120,
        }}
      />
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 4 }}>
        <div style={{ display: 'flex', gap: 4 }}>
          <ToolPill icon="paperclip" label="附件" />
          <ToolPill icon="globe" label="联网" active />
        </div>
        <button
          onClick={() => { if (text.trim()) { onSend(text.trim()); setText(''); } }}
          disabled={!text.trim()}
          style={{
            width: 32, height: 32, borderRadius: '50%',
            border: 'none', cursor: text.trim() ? 'pointer' : 'not-allowed',
            background: text.trim() ? T.navy : T.surface,
            color: text.trim() ? T.white : T.navyLight,
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            transition: 'all .15s',
          }}>
          <Icon name="arrowUp" size={15} stroke={2} />
        </button>
      </div>
    </div>
  );
};

/* Transform menu — appears when transform clicked */
const TransformMenu = ({ open, onClose, onPick }) => {
  if (!open) return null;
  const opts = [
    { id: 'gzh',   label: '公众号长文',   sub: '深度长文 · 1500–3000 字', icon: 'document', tint: '#fff8e0', accent: '#c89b00' },
    { id: 'dy',    label: '抖音短视频',   sub: '60s 口播脚本 + 分镜', icon: 'video', tint: '#e8e8fd', accent: T.iris },
    { id: 'wxsph', label: '微信视频号',   sub: '90s 横屏 · 适合科普', icon: 'play', tint: '#e0faf4', accent: T.success },
    { id: 'bili',  label: 'B 站视频',    sub: '5 分钟以上 · 长内容', icon: 'bilibili', tint: '#ffe5ec', accent: '#ff4488' },
  ];
  return (
    <>
      <div onClick={onClose} style={{ position: 'fixed', inset: 0, zIndex: 100 }} />
      <div style={{
        position: 'absolute', bottom: 80, left: '50%',
        transform: 'translateX(-50%)',
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

/* Main GenerationPage */
const GenerationPage = ({ initialPrompt, onBackHome, onNavigate, asset }) => {
  const isAssetMode = Boolean(asset);
  /* stage 1..4 = active step; 5 = canvas open / done */
  const [stage, setStage] = React.useState(isAssetMode ? 5 : 1);
  const [canvasOpen, setCanvasOpen] = React.useState(isAssetMode);
  const [canvasExpanded, setCanvasExpanded] = React.useState(false);
  const [mode, setMode] = React.useState('preview');
  const [transformOpen, setTransformOpen] = React.useState(false);
  const [followUps, setFollowUps] = React.useState([]); // {kind: 'transform' | 'link' | 'draft' | 'msg', payload}
  const [keyInfo, setKeyInfo] = React.useState(null);
  const scrollRef = React.useRef(null);
  const pageTitle = asset?.title || '猛男喜欢的粉色植物科普与养护指导';
  const pageMeta = asset
    ? `${platformMeta[asset.platform]?.label || '内容'} · ${typeMeta[asset.type]?.label || '生成内容'} · ${asset.storedAt}`
    : `小红书图文 · ${new Date().toLocaleDateString('zh-CN')} · 自动保存中`;

  /* Auto-scroll to bottom when content changes */
  React.useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [stage, followUps.length, canvasOpen]);

  const sessions = [
    '猛男喜欢的粉色植物 · 当前',
    '上海咖啡馆 City Walk Top 10',
    '租房避雷指南 v2',
    '产品测评 · AI 视频工具横评',
  ];

  /* Step 1 done → step 2 starts (auto, with simulated delay) */
  const onStep1Done = (info) => {
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

  const onTransformPick = (target) => {
    setTransformOpen(false);
    setFollowUps(f => [...f, { kind: 'transform', payload: target, id: Date.now() }]);
  };

  const onPublish = () => {
    setFollowUps(f => [...f, { kind: 'link', id: Date.now() }]);
  };
  const onLinked = () => {
    setFollowUps(f => [...f, { kind: 'draft', id: Date.now() + 1 }]);
  };

  return (
    <div style={{ display: 'flex', height: '100%', width: '100%', background: T.surfaceWh, position: 'relative', overflow: 'hidden' }}>
      <Sidebar active={isAssetMode ? 'library' : 'home'} onNew={onBackHome} onNavigate={onNavigate} sessions={sessions} />

      {/* Chat column */}
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0, position: 'relative' }}>
        {/* Top bar */}
        <div style={{
          height: 56, padding: '0 24px',
          display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          borderBottom: `1px solid ${T.hairlineSoft}`,
          background: 'rgba(250,252,254,.8)', backdropFilter: 'blur(8px)',
          flexShrink: 0,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, minWidth: 0 }}>
            <button onClick={onBackHome} style={iconBtnStyle()}>
              <Icon name="home" size={16} color={T.navyMid} />
            </button>
            <div style={{ minWidth: 0 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: T.navy, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                {pageTitle}
              </div>
              <div style={{ fontSize: 10.5, color: T.navyLight, fontFamily: T.fontMono }}>
                {pageMeta}
              </div>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <StepperRail stage={Math.min(Math.ceil(stage), 4)} />
            <button style={iconBtnStyle()}><Icon name="moreH" size={16} color={T.navyMid} /></button>
          </div>
        </div>

        {/* Chat scroll */}
        <div ref={scrollRef} style={{ flex: 1, overflowY: 'auto', padding: '24px 0 24px' }}>
          <div style={{
            maxWidth: canvasOpen ? 640 : 760, margin: '0 auto', padding: '0 24px',
            display: 'flex', flexDirection: 'column', gap: 22,
          }}>
            {/* User initial message */}
            <Bubble from="user">
              {initialPrompt || (asset ? `打开内容库中的「${asset.title}」，继续查看和编辑。` : '我想生成一篇有关于猛男喜欢的粉色的植物科普与养护指导')}
            </Bubble>

            {asset && (
              <NoriSays>
                <div style={{
                  background: T.white,
                  border: `1px solid ${T.hairline}`,
                  borderRadius: 14,
                  padding: '14px 16px',
                  boxShadow: T.shadowXs,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                }}>
                  <div style={{
                    width: 36,
                    height: 36,
                    borderRadius: 10,
                    background: platformMeta[asset.platform]?.tint || T.surface,
                    color: platformMeta[asset.platform]?.accent || T.iris,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}>
                    <Icon name={typeMeta[asset.type]?.icon || 'document'} size={17} />
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 13.5, fontWeight: 700, color: T.navy, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      已从我的内容库打开
                    </div>
                    <div style={{ fontSize: 11.5, color: T.navyLight, marginTop: 2 }}>
                      可查看、编辑、重新发布，或用 Transform 转换为其他平台形态。
                    </div>
                  </div>
                  <button
                    onClick={() => setCanvasOpen(true)}
                    style={{
                      height: 34,
                      padding: '0 12px',
                      borderRadius: 9,
                      border: 'none',
                      background: T.navy,
                      color: T.primary,
                      fontSize: 12.5,
                      fontWeight: 700,
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: 6,
                    }}
                  >
                    <Icon name="expand" size={12} />
                    打开 Canvas
                  </button>
                </div>
              </NoriSays>
            )}

            {/* Step 1 */}
            {!isAssetMode && stage >= 1 && stage < 1.5 && (
              <Step1KeyInfo onComplete={onStep1Done} onSkip={onStep1Skip} />
            )}
            {!isAssetMode && stage >= 1.5 && (
              <Bubble from="user">
                {keyInfo ? '目标：植物新手 + 反差梗 / 整活 + 标准 8–10 图' : '直接开始吧～'}
              </Bubble>
            )}

            {/* between 1.5 and 2: typing */}
            {!isAssetMode && stage === 1.5 && (
              <NoriSays>
                <span style={{ color: T.navyMid }}>正在分析爆款数据 </span>
                <TypingDots />
              </NoriSays>
            )}

            {/* Step 2 */}
            {!isAssetMode && stage >= 2 && <Step2HotPosts onSelectAngle={onSelectAngle} />}

            {!isAssetMode && stage === 2.5 && (
              <NoriSays>
                <span style={{ color: T.navyMid }}>选题已确认，开始调研素材 </span>
                <TypingDots />
              </NoriSays>
            )}

            {/* Step 3 */}
            {!isAssetMode && stage >= 3 && <Step3Research />}
            {!isAssetMode && stage === 3.5 && (
              <NoriSays>
                <span style={{ color: T.navyMid }}>素材准备完毕，开始组装 </span>
                <TypingDots />
              </NoriSays>
            )}

            {/* Step 4 */}
            {!isAssetMode && stage >= 4 && <Step4Generate onAllDone={onAllDone} />}

            {/* Follow-up: transforms / publish / draft */}
            {followUps.map(f => {
              if (f.kind === 'transform') return <TransformLaunched key={f.id} target={f.payload} />;
              if (f.kind === 'link') return <PublishLinkAccount key={f.id} onLinked={onLinked} />;
              if (f.kind === 'draft') return <PublishDraftSaved key={f.id} />;
              return null;
            })}
          </div>
        </div>

        {/* Bottom composer */}
        <div style={{
          padding: '12px 24px 18px',
          background: 'linear-gradient(to top, rgba(250,252,254,1) 60%, rgba(250,252,254,0))',
          flexShrink: 0,
        }}>
          <div style={{ maxWidth: canvasOpen ? 640 : 760, margin: '0 auto' }}>
            <ChatComposer onSend={(t) => setFollowUps(f => [...f, { kind: 'msg', payload: t, id: Date.now() }])} />
          </div>
        </div>
      </main>

      {/* Canvas */}
      <Canvas
        open={canvasOpen}
        expanded={canvasExpanded}
        setExpanded={setCanvasExpanded}
        onClose={() => setCanvasOpen(false)}
        onTransform={() => setTransformOpen(true)}
        onPublish={onPublish}
        mode={mode} setMode={setMode}
        asset={asset}
      />

      <TransformMenu open={transformOpen} onClose={() => setTransformOpen(false)} onPick={onTransformPick} />
    </div>
  );
};




/* ─── App root ─── */

const App = () => {
  const [page, setPage] = React.useState('home'); // 'home' | 'gen' | 'library'
  const [prompt, setPrompt] = React.useState('');
  const [activeAsset, setActiveAsset] = React.useState(null);

  const goGen = (p) => {
    setPrompt(p);
    setActiveAsset(null);
    setPage('gen');
  };

  const goHome = () => {
    setActiveAsset(null);
    setPrompt('');
    setPage('home');
  };

  const goLibrary = () => {
    setActiveAsset(null);
    setPage('library');
  };

  const handleNavigate = (target) => {
    if (target === 'home') goHome();
    if (target === 'library') goLibrary();
  };

  const openAsset = (asset) => {
    setActiveAsset(asset);
    setPrompt(`打开内容库中的「${asset.title}」`);
    setPage('gen');
  };

  if (page === 'home') {
    return <HomePage onSubmit={goGen} onNavigate={handleNavigate} />;
  }

  if (page === 'library') {
    return <AssetsPage onNavigate={handleNavigate} onOpenAsset={openAsset} onNew={goHome} />;
  }

  return (
    <GenerationPage
      initialPrompt={prompt}
      asset={activeAsset}
      onBackHome={goHome}
      onNavigate={handleNavigate}
    />
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
