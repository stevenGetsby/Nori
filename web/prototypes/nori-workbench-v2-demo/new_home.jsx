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

const Sidebar = ({ active, onNew, sessions = [] }) => {
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
          <a
            key={item.id}
            href="#"
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: 10,
              padding: '8px 10px',
              borderRadius: 8,
              fontSize: 13,
              fontWeight: active === item.id ? 600 : 500,
              color: active === item.id ? T.navy : T.navyMid,
              background: active === item.id ? T.surface : 'transparent',
              textDecoration: 'none',
              transition: 'all .12s',
            }}
            onMouseEnter={e => { if (active !== item.id) e.currentTarget.style.background = 'rgba(14,14,44,.03)'; }}
            onMouseLeave={e => { if (active !== item.id) e.currentTarget.style.background = 'transparent'; }}
          >
            <Icon name={item.icon} size={16} color={active === item.id ? T.navy : T.navyLight} />
            {item.label}
          </a>
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

  const triggerBurst = React.useCallback(() => {
    window.clearTimeout(timerRef.current);
    setBursting(false);
    requestAnimationFrame(() => {
      setBursting(true);
      timerRef.current = window.setTimeout(() => setBursting(false), 1550);
    });
  }, []);

  React.useEffect(() => () => window.clearTimeout(timerRef.current), []);

  const lineOneSize = mobile ? 36 : compact ? 52 : 68;
  const ideaSize = mobile ? 58 : compact ? 84 : 112;
  const lineTwoSize = mobile ? 36 : compact ? 48 : 60;
  const everywhereSize = mobile ? 48 : compact ? 70 : 92;

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
              color: 'rgba(14,14,44,.74)',
            }}>From one</span>
            <span style={{
              fontFamily: T.fontSerif,
              fontSize: ideaSize,
              fontWeight: 600,
              fontStyle: 'italic',
              letterSpacing: '-0.04em',
              color: T.navy,
              textShadow: '0 18px 40px rgba(14,14,44,.08)',
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
              color: 'rgba(14,14,44,.74)',
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
              <span style={{ position: 'relative', zIndex: 1 }}>content</span>
            </span>
            <span style={{
              fontFamily: T.fontSerif,
              fontSize: everywhereSize,
              fontWeight: 560,
              letterSpacing: '-0.06em',
              color: T.navy,
            }}>everywhere</span>
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
  const items = [
    { title: '当家居博主爱上拼豆后', desc: '从兴趣到内容，记录每一粒色彩的故事', tint: '#fbe9c5', emoji: '🐱' },
    { title: '深夜食堂里的治愈系主厨', desc: '把烟火气变成社媒上最暖的那条视频', tint: '#e6e9d8', emoji: '🍜' },
    { title: '植物人的城市阳台改造计划', desc: '一个 10㎡ 阳台能长出多少个爆款选题', tint: '#dde6c8', emoji: '🌿' },
    { title: '职场人的知识 IP 变现路径', desc: '把你五年的工作经验做成会流量的内容', tint: '#f3dbda', emoji: '💼' },
  ];
  const [hov, setHov] = React.useState(null);

  if (mobile) {
    return (
      <div>
        <div style={{ fontSize: 12, color: T.navyLight, marginBottom: 12, letterSpacing: '0.02em' }}>快速开始</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: 10 }}>
          {items.map((it, i) => (
            <button
              key={i}
              onClick={() => onPick(it.title)}
              style={{
                background: it.tint,
                border: `1px solid rgba(14,14,44,.06)`,
                borderRadius: 20,
                padding: '16px 16px 18px',
                textAlign: 'left',
                display: 'flex',
                flexDirection: 'column',
                gap: 10,
                boxShadow: T.shadowSm,
                cursor: 'pointer',
              }}
            >
              <div style={{ fontSize: 34 }}>{it.emoji}</div>
              <div style={{ fontSize: 15, fontWeight: 700, color: T.navy, lineHeight: 1.25 }}>{it.title}</div>
              <div style={{ fontSize: 12.5, color: 'rgba(14,14,44,.64)', lineHeight: 1.55 }}>{it.desc}</div>
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div>
      <div style={{ fontSize: 12, color: T.navyLight, marginBottom: 10, letterSpacing: '0.02em' }}>快速开始</div>
      <div style={{ position: 'relative', height: compact ? 196 : 214 }} onMouseLeave={() => setHov(null)}>
        {items.map((it, i) => {
          const isHov = hov === i;
          const hasHov = hov !== null;
          const baseLeft = compact ? i * 20 : i * 22;
          return (
            <button
              key={i}
              onClick={() => onPick(it.title)}
              onMouseEnter={() => setHov(i)}
              style={{
                position: 'absolute',
                top: 0,
                left: `calc(${baseLeft}% - 0px)`,
                width: compact ? '38%' : '34%',
                height: '100%',
                borderRadius: 22,
                border: `1px solid rgba(14,14,44,.06)`,
                background: it.tint,
                padding: compact ? '16px 16px 18px' : '18px 18px 20px',
                textAlign: 'left',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                transform: isHov ? 'translateY(-8px)' : (hasHov ? 'translateY(0)' : 'translateY(0)'),
                boxShadow: isHov ? '0 22px 46px rgba(14,14,44,.16)' : '0 8px 18px rgba(14,14,44,.06)',
                zIndex: isHov ? 10 : i,
                transition: 'transform .25s cubic-bezier(.2,.7,.2,1), box-shadow .25s',
                overflow: 'hidden',
              }}
            >
              <div style={{
                position: 'absolute',
                top: 12,
                right: 12,
                opacity: isHov ? 1 : 0,
                transition: 'opacity .2s',
                width: 24,
                height: 24,
                borderRadius: 8,
                background: 'rgba(255,255,255,.72)',
                backdropFilter: 'blur(10px)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: T.navyMid,
              }}>
                <Icon name="expand" size={11} />
              </div>
              <div style={{
                width: '100%',
                height: compact ? 94 : 102,
                borderRadius: 18,
                background: 'linear-gradient(135deg, rgba(255,255,255,.56), rgba(255,255,255,.16))',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: compact ? 42 : 46,
                boxShadow: 'inset 0 0 0 1px rgba(255,255,255,.22)',
              }}>
                <span>{it.emoji}</span>
              </div>
              <div>
                <div style={{ fontSize: 14, fontWeight: 700, color: T.navy, marginBottom: 6, letterSpacing: '-0.01em', lineHeight: 1.28 }}>
                  {it.title}
                </div>
                <div style={{
                  fontSize: 11.5,
                  color: 'rgba(14,14,44,.62)',
                  lineHeight: 1.55,
                  display: '-webkit-box',
                  WebkitLineClamp: 2,
                  WebkitBoxOrient: 'vertical',
                  overflow: 'hidden',
                }}>
                  {it.desc}
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};

const SkillSquare = ({ compact, mobile }) => {
  const skills = [
    { name: '小红书爆款图文', author: '@Nori', uses: '12.4w', tint: T.peachTint, accent: '#d49e9c', icon: 'image' },
    { name: '公众号深度长文', author: '@Lina', uses: '8.6w', tint: '#fff8e0', accent: '#c89b00', icon: 'document' },
    { name: '抖音口播脚本', author: '@Theo', uses: '6.2w', tint: '#e8e8fd', accent: T.iris, icon: 'video' },
    { name: '产品测评结构化', author: '@Mia', uses: '4.1w', tint: '#e0faf4', accent: T.success, icon: 'list' },
    { name: '爆款标题公式 12 招', author: '@Nori', uses: '9.8w', tint: T.primaryTint, accent: '#96b800', icon: 'sparkles' },
    { name: '小红书封面拆解师', author: '@Yuki', uses: '3.7w', tint: '#e0faf4', accent: T.success, icon: 'palette' },
  ];
  const cols = mobile ? '1fr' : compact ? 'repeat(2, 1fr)' : 'repeat(3, 1fr)';

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginBottom: 16, gap: 12, flexWrap: 'wrap' }}>
        <div>
          <h3 style={{ fontSize: 14, fontWeight: 600, color: T.navy, letterSpacing: '0.01em', marginBottom: 2 }}>Skill 广场</h3>
          <p style={{ fontSize: 11.5, color: T.navyLight }}>来自创作者社群的可复用爆款配方</p>
        </div>
        <a href="#" style={{ fontSize: 12, color: T.navyLight, textDecoration: 'none', fontWeight: 500 }}>逛 Skill 市场 ›</a>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: cols, gap: 12 }}>
        {skills.map((s, i) => (
          <div
            key={i}
            style={{
              background: 'rgba(255,255,255,.88)',
              border: `1px solid ${T.hairline}`,
              borderRadius: 18,
              padding: '14px 14px 12px',
              display: 'flex',
              flexDirection: 'column',
              gap: 10,
              cursor: 'pointer',
              transition: 'all .15s',
              boxShadow: T.shadowXs,
            }}
            onMouseEnter={e => { e.currentTarget.style.borderColor = 'rgba(75,77,237,.28)'; e.currentTarget.style.transform = 'translateY(-1px)'; }}
            onMouseLeave={e => { e.currentTarget.style.borderColor = T.hairline; e.currentTarget.style.transform = 'translateY(0)'; }}
          >
            <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
              <div style={{
                width: 32,
                height: 32,
                borderRadius: 10,
                background: s.tint,
                color: s.accent,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}>
                <Icon name={s.icon} size={16} />
              </div>
              <span style={{ fontSize: 10.5, fontFamily: T.fontMono, color: T.navyLight }}>{s.uses} 次使用</span>
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 13.5, fontWeight: 600, color: T.navy, marginBottom: 3 }}>{s.name}</div>
              <div style={{ fontSize: 11, color: T.navyLight }}>{s.author}</div>
            </div>
            <button style={{
              alignSelf: 'flex-start',
              padding: '5px 10px',
              borderRadius: 99,
              border: `1px solid ${T.hairline}`,
              background: 'transparent',
              fontSize: 11,
              fontWeight: 500,
              color: T.navyMid,
              cursor: 'pointer',
              display: 'inline-flex',
              alignItems: 'center',
              gap: 4,
            }}>
              <Icon name="plus" size={11} /> 使用
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

const HomePage = ({ onSubmit }) => {
  const { width, isCompact, isTablet, isMobile } = useViewport();
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
        {!isTablet && <Sidebar active="home" onNew={() => {}} sessions={sessions} />}

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
                  width: isMobile ? 48 : 58,
                  height: isMobile ? 48 : 58,
                  borderRadius: isMobile ? 18 : 22,
                  background: 'linear-gradient(180deg, rgba(214,255,0,1), rgba(214,255,0,.88))',
                  boxShadow: '0 20px 40px rgba(214,255,0,.18), inset 0 -1px 0 rgba(14,14,44,.12)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}>
                  <NoriLogo size={isMobile ? 28 : 34} />
                </div>
              </div>

              <HeroHeadline compact={isCompact} mobile={isMobile} />

              <p style={{
                maxWidth: isMobile ? 320 : 640,
                textAlign: 'center',
                fontSize: isMobile ? 14 : 15.5,
                lineHeight: 1.7,
                color: T.navyMid,
                fontWeight: 450,
                marginBottom: isMobile ? 18 : 22,
              }}>
                以 Apple 风格的克制与柔光为基调，把一次灵感输入，延展成图文、长文和脚本。
                你只需要说出一个想法，Nori 就会把它铺成完整的内容系统。
              </p>

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
