import streamlit as st

st.set_page_config(
    page_title="GreenHabit",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css');

:root {
  --gh-green: #2D6A4F; --gh-mint: #52B788; --gh-gold: #E9C46A;
  --gh-dark: #1B4332; --gh-light: #D8F3DC;
}
.main .block-container { max-width: 520px; padding: 1rem 1rem 4rem; }
h1,h2,h3 { font-weight: 600 !important; }

.gh-header {
  background: var(--gh-green); color: white;
  border-radius: 16px; padding: 20px 24px; margin-bottom: 16px;
}
.gh-logo { font-size: 22px; font-weight: 700; letter-spacing: -0.5px; }
.gh-logo span { color: var(--gh-gold); }
.gh-pts-row { display:flex; gap:12px; margin-top:14px; }
.gh-pts-box {
  background: rgba(255,255,255,0.12); border-radius: 12px;
  padding: 12px 18px; flex:1;
}
.gh-pts-num { font-size:28px; font-weight:700; color:var(--gh-gold); }
.gh-pts-label { font-size:11px; color:rgba(255,255,255,0.7); margin-top:2px; }
.gh-streak-box {
  background:rgba(255,255,255,0.12); border-radius:12px;
  padding:12px 16px; text-align:center;
}
.gh-streak-num { font-size:22px; font-weight:700; color:#FFD166; }
.gh-streak-label { font-size:10px; color:rgba(255,255,255,0.7); }

.gh-card {
  background:white; border:1px solid rgba(0,0,0,0.07);
  border-radius:14px; padding:16px; margin-bottom:12px;
}
.gh-section { font-size:11px; font-weight:600; color:#6B7280;
  text-transform:uppercase; letter-spacing:0.6px; margin:16px 0 10px; }

.tree-row { display:flex; align-items:center; gap:14px; }
.tree-emoji { font-size:48px; }
.tree-info { flex:1; }
.tree-name { font-size:15px; font-weight:600; color:#111; }
.tree-level { font-size:12px; color:#6B7280; margin:2px 0 8px; }
.progress-track { background:#f0f0f0; border-radius:4px; height:6px; }
.progress-fill { height:6px; border-radius:4px; background:var(--gh-mint); }

.action-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; }
.action-card {
  background:white; border:1px solid rgba(0,0,0,0.07);
  border-radius:12px; padding:14px 12px; cursor:pointer; position:relative;
}
.action-card.done { opacity:0.6; background:#f0fbf4; border-color:var(--gh-mint); }
.action-icon { font-size:22px; margin-bottom:6px; }
.action-name { font-size:13px; font-weight:500; color:#111; }
.action-pts { font-size:11px; color:var(--gh-green); margin-top:2px; }
.done-tag {
  position:absolute; top:8px; right:8px; background:var(--gh-mint);
  color:white; font-size:10px; border-radius:4px; padding:2px 5px;
}

.rank-item {
  display:flex; align-items:center; gap:12px;
  background:white; border:1px solid rgba(0,0,0,0.07);
  border-radius:12px; padding:12px 16px; margin-bottom:8px;
}
.rank-item.me { border-color:var(--gh-mint); background:#f0fbf4; }
.rank-pos { width:24px; text-align:center; font-weight:700; font-size:15px; color:#9CA3AF; }
.rank-avatar {
  width:36px; height:36px; border-radius:50%; display:flex;
  align-items:center; justify-content:center; font-size:13px; font-weight:700; color:white;
}
.rank-name { flex:1; font-size:14px; font-weight:500; }
.rank-pts { font-size:13px; font-weight:600; color:var(--gh-green); }

.reward-item {
  display:flex; align-items:center; gap:12px;
  background:white; border:1px solid rgba(0,0,0,0.07);
  border-radius:12px; padding:14px; margin-bottom:10px;
}
.reward-icon { font-size:28px; }
.reward-info { flex:1; }
.reward-name { font-size:14px; font-weight:500; color:#111; }
.reward-desc { font-size:12px; color:#6B7280; }
.reward-cost { font-size:13px; font-weight:600; color:var(--gh-green); }

.stat-grid { display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-bottom:12px; }
.stat-card { background:white; border:1px solid rgba(0,0,0,0.07); border-radius:12px; padding:12px; text-align:center; }
.stat-num { font-size:20px; font-weight:700; color:var(--gh-green); }
.stat-label { font-size:11px; color:#6B7280; margin-top:2px; }

.badge-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; }
.badge-item { background:white; border:1px solid rgba(0,0,0,0.07); border-radius:12px; padding:10px 6px; text-align:center; }
.badge-item.locked { opacity:0.35; }
.badge-icon { font-size:22px; }
.badge-name { font-size:10px; color:#6B7280; margin-top:4px; }

.stButton > button {
  background: var(--gh-green) !important; color:white !important;
  border:none !important; border-radius:10px !important;
  font-weight:600 !important; padding:8px 16px !important;
  transition:background 0.15s !important;
}
.stButton > button:hover { background: var(--gh-dark) !important; }

div[data-testid="stTabs"] button {
  font-weight:500; font-size:13px;
}
</style>
""", unsafe_allow_html=True)

# ── State ─────────────────────────────────────────────────────────────────────
def init():
    defaults = {
        "points": 1250, "streak": 7, "checkin_count": 0, "total_actions": 38,
        "done": set(), "week_pts": 420, "week_actions": 12,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()
s = st.session_state

TREES = [
    ("🌰","Hạt Giống",200),("🌱","Cây Xanh Con",500),
    ("🪴","Cây Nhỏ",1000),("🌿","Cây Xanh",2000),("🌳","Cây Trưởng Thành",5000),
]
def get_tree(pts):
    lvl = 0
    for i,(e,n,m) in enumerate(TREES):
        if pts >= (0 if i==0 else TREES[i-1][2]): lvl=i
    return lvl, TREES[lvl], TREES[min(lvl+1,len(TREES)-1)]

ACTIONS = [
    (0,"♻️","Phân loại rác",50),
    (1,"🍶","Bình nước cá nhân",30),
    (2,"🛍️","Không dùng túi nilon",25),
    (3,"💡","Tắt điện khi ra ngoài",20),
    (4,"🚌","Xe buýt / xe đạp",60),
    (5,"🚶","Đi bộ đến lớp",35),
    (6,"🌿","Sản phẩm xanh",40),
    (7,"🍱","Mang hộp cơm",45),
]
REWARDS = [
    ("🥤","Giảm 10% căng tin A","Căng tin tầng 1 nhà B3",300),
    ("🍜","Combo cơm + nước miễn phí","Căng tin sinh thái",500),
    ("🛒","Voucher 20.000đ Co.op Xtra","Siêu thị trong khuôn viên",400),
    ("🎁","Túi vải canvas miễn phí","Thay thế túi nilon",200),
    ("📋","+2 điểm rèn luyện","Quy đổi điểm RLSV",1000),
]
LEADERBOARD = [
    ("MT","Minh Tuấn","#2D6A4F",3240),
    ("LH","Lan Hương","#52B788",2910),
    ("QN","Quốc Nam","#74C69D",2650),
    ("TL","Thu Linh","#95D5B2",2420),
    ("ĐH","Đức Hoà","#1B4332",2180),
    ("BT","Bảo Thy","#40916C",1980),
    ("KH","Khánh Hiền","#52B788",1760),
]

# ── Header ────────────────────────────────────────────────────────────────────
lvl, tree, next_tree = get_tree(s["points"])
prev_pts = 0 if lvl==0 else TREES[lvl-1][2]
pct = min(100, int((s["points"]-prev_pts)/(next_tree[2]-prev_pts)*100))

st.markdown(f"""
<div class="gh-header">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <div class="gh-logo">Green<span>Habit</span></div>
    <div style="width:38px;height:38px;border-radius:50%;background:#52B788;
      display:flex;align-items:center;justify-content:center;font-weight:700;color:white">AN</div>
  </div>
  <div class="gh-pts-row">
    <div class="gh-pts-box">
      <div class="gh-pts-num">{s['points']:,}</div>
      <div class="gh-pts-label">điểm xanh tích lũy</div>
    </div>
    <div class="gh-streak-box">
      <div class="gh-streak-num">{s['streak']}</div>
      <div class="gh-streak-label">ngày liên tiếp 🔥</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Trang chủ","✅ Check-in","🏆 Xếp hạng","🎁 Đổi thưởng","👤 Hồ sơ"])

# ── Tab 1: Dashboard ──────────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="gh-section">Cây xanh của bạn</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="gh-card">
      <div class="tree-row">
        <div class="tree-emoji">{tree[0]}</div>
        <div class="tree-info">
          <div class="tree-name">{tree[1]}</div>
          <div class="tree-level">Cấp {lvl+1} · {s['points']-prev_pts}/{next_tree[2]-prev_pts} điểm lên cấp</div>
          <div class="progress-track"><div class="progress-fill" style="width:{pct}%"></div></div>
          <div style="font-size:11px;color:#6B7280;margin-top:4px">Tích thêm {next_tree[2]-s['points']}đ để lên cấp {lvl+2}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gh-section">Hành vi hôm nay</div>', unsafe_allow_html=True)
    cols = st.columns(2)
    quick = [(0,"♻️","Phân loại rác",50),(1,"🍶","Bình nước cá nhân",30),
             (4,"🚌","Xe buýt / xe đạp",60),(6,"🌿","Sản phẩm xanh",40)]
    for i,(idx,icon,name,pts) in enumerate(quick):
        with cols[i%2]:
            done = idx in s["done"]
            st.markdown(f"""
            <div class="action-card {'done' if done else ''}">
              {'<div class="done-tag">Done</div>' if done else ''}
              <div class="action-icon">{icon}</div>
              <div class="action-name">{name}</div>
              <div class="action-pts">+{pts} điểm</div>
            </div>
            """, unsafe_allow_html=True)
            if not done:
                if st.button(f"Check-in", key=f"home_cb_{idx}"):
                    s["done"].add(idx); s["points"]+=pts
                    s["checkin_count"]+=1; s["total_actions"]+=1
                    s["week_pts"]+=pts; s["week_actions"]+=1
                    st.rerun()

    st.markdown('<div class="gh-section">Thống kê tuần này</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-num">{s['week_actions']}</div><div class="stat-label">Hành vi xanh</div></div>
      <div class="stat-card"><div class="stat-num">{s['week_pts']}</div><div class="stat-label">Điểm kiếm được</div></div>
      <div class="stat-card"><div class="stat-num">#8</div><div class="stat-label">Xếp hạng lớp</div></div>
    </div>
    """, unsafe_allow_html=True)

# ── Tab 2: Check-in ───────────────────────────────────────────────────────────
with tab2:
    st.markdown(f"""
    <div style="background:#f0fbf4;border:1px solid #52B788;border-radius:10px;
      padding:10px 14px;margin-bottom:12px;font-size:13px;color:#2D6A4F">
      Hôm nay bạn đã check-in <strong>{s['checkin_count']}</strong> hành vi xanh
    </div>
    """, unsafe_allow_html=True)

    groups = [
        ("Hành vi môi trường", [0,1,2,3]),
        ("Di chuyển xanh", [4,5]),
        ("Tiêu dùng bền vững", [6,7]),
    ]
    action_map = {a[0]:a for a in ACTIONS}

    for group_name, idxs in groups:
        st.markdown(f'<div class="gh-section">{group_name}</div>', unsafe_allow_html=True)
        cols = st.columns(2)
        for ci, idx in enumerate(idxs):
            _,icon,name,pts = action_map[idx]
            done = idx in s["done"]
            with cols[ci%2]:
                st.markdown(f"""
                <div class="action-card {'done' if done else ''}">
                  {'<div class="done-tag">Done ✓</div>' if done else ''}
                  <div class="action-icon">{icon}</div>
                  <div class="action-name">{name}</div>
                  <div class="action-pts">+{pts} điểm</div>
                </div>
                """, unsafe_allow_html=True)
                if not done:
                    if st.button("Xác nhận", key=f"ci_{idx}"):
                        s["done"].add(idx); s["points"]+=pts
                        s["checkin_count"]+=1; s["total_actions"]+=1
                        s["week_pts"]+=pts; s["week_actions"]+=1
                        st.success(f"+{pts} điểm! 🌿")
                        st.rerun()

# ── Tab 3: Leaderboard ────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="gh-section">Top sinh viên xanh – Tháng 6</div>', unsafe_allow_html=True)
    medals = ["🥇","🥈","🥉"]
    for i,(initials,name,color,pts) in enumerate(LEADERBOARD):
        pos = medals[i] if i<3 else str(i+1)
        st.markdown(f"""
        <div class="rank-item">
          <div class="rank-pos">{pos}</div>
          <div class="rank-avatar" style="background:{color}">{initials}</div>
          <div class="rank-name">{name}</div>
          <div class="rank-pts">{pts:,}đ</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="rank-item me">
      <div class="rank-pos">8</div>
      <div class="rank-avatar" style="background:#2D6A4F">AN</div>
      <div class="rank-name">Anh Nguyên (Bạn)</div>
      <div class="rank-pts">{s['points']:,}đ</div>
    </div>
    """, unsafe_allow_html=True)

# ── Tab 4: Rewards ────────────────────────────────────────────────────────────
with tab4:
    st.markdown(f"""
    <div style="background:#fff8e8;border:1px solid #E9C46A;border-radius:10px;
      padding:10px 14px;margin-bottom:12px;font-size:13px;color:#856404">
      Điểm hiện tại: <strong>{s['points']:,} điểm</strong>
    </div>
    """, unsafe_allow_html=True)

    for icon,name,desc,cost in REWARDS:
        can = s["points"] >= cost
        col1, col2 = st.columns([4,1])
        with col1:
            st.markdown(f"""
            <div class="reward-item" style="margin-bottom:0">
              <div class="reward-icon">{icon}</div>
              <div class="reward-info">
                <div class="reward-name">{name}</div>
                <div class="reward-desc">{desc}</div>
                <div class="reward-cost">🌿 {cost:,} điểm</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
            if can:
                if st.button("Đổi", key=f"r_{name}"):
                    s["points"] -= cost
                    st.success(f"Đổi thành công: {name}! 🎉")
                    st.rerun()
            else:
                st.button("Đổi", key=f"r_{name}", disabled=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# ── Tab 5: Profile ────────────────────────────────────────────────────────────
with tab5:
    lvl2, tree2, _ = get_tree(s["points"])
    st.markdown(f"""
    <div class="gh-card" style="text-align:center">
      <div style="width:64px;height:64px;border-radius:50%;background:#52B788;
        display:flex;align-items:center;justify-content:center;font-size:22px;
        font-weight:700;color:white;margin:0 auto 10px">AN</div>
      <div style="font-size:18px;font-weight:700;color:#111">Anh Nguyên</div>
      <div style="font-size:13px;color:#6B7280;margin-top:2px">
        Sinh viên năm 2 · Khoa CNTT · ĐH Bách Khoa
      </div>
      <div style="margin-top:8px;display:inline-block;background:#f0fbf4;
        color:#2D6A4F;border-radius:8px;padding:4px 12px;font-size:12px;font-weight:600">
        {tree2[0]} Cấp {lvl2+1} – {tree2[1]}
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-num">{s['points']:,}</div><div class="stat-label">Tổng điểm</div></div>
      <div class="stat-card"><div class="stat-num">{s['streak']}</div><div class="stat-label">Ngày streak</div></div>
      <div class="stat-card"><div class="stat-num">{s['total_actions']}</div><div class="stat-label">Hành vi xanh</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gh-section">Huy hiệu</div>', unsafe_allow_html=True)
    badges = [
        ("🌱","Người mới",True),("♻️","Tái chế 10x",True),
        ("🚌","Di chuyển xanh",True),("🔥","Streak 7 ngày",True),
        ("🌳","Cây trưởng thành",False),("🏆","Top 3 lớp",False),
        ("⭐","Streak 30 ngày",False),("💎","Huyền thoại xanh",False),
    ]
    badge_html = '<div class="badge-grid">'
    for icon,name,unlocked in badges:
        badge_html += f'<div class="badge-item {"" if unlocked else "locked"}"><div class="badge-icon">{icon}</div><div class="badge-name">{name}</div></div>'
    badge_html += '</div>'
    st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown('<div class="gh-section">Tác động môi trường</div>', unsafe_allow_html=True)
    co2 = round(s['total_actions'] * 0.032, 1)
    water = s['total_actions'] * 0.63
    bags = s['total_actions'] // 5
    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card"><div class="stat-num">{co2}kg</div><div class="stat-label">CO₂ tiết kiệm</div></div>
      <div class="stat-card"><div class="stat-num">{int(water)}L</div><div class="stat-label">Nước tiết kiệm</div></div>
      <div class="stat-card"><div class="stat-num">{bags}</div><div class="stat-label">Túi nilon thay thế</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reset dữ liệu demo"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()