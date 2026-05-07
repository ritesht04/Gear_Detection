import streamlit as st
import requests
import os
import tempfile
import time
import numpy as np
from pathlib import Path
from PIL import Image
import cv2
from collections import Counter

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GEAR_DEFECT_APP",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Bebas+Neue&family=Rajdhani:wght@300;400;600;700&display=swap');

:root {
  --bg:      #050608;
  --surface: #0d0f12;
  --panel:   #111419;
  --border:  #1e2530;
  --cyan:    #00f5ff;
  --orange:  #ff6b00;
  --green:   #00ff88;
  --red:     #ff2d55;
  --yellow:  #ffd700;
  --text:    #c8d0e0;
  --dim:     #4a5568;
}

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0;}

html,body,[data-testid="stAppViewContainer"],[data-testid="stMain"],.main{
  background:var(--bg) !important;color:var(--text);
}
[data-testid="stSidebar"]{display:none !important;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none !important;}

.block-container{padding:0 !important;max-width:100% !important;}
[data-testid="stVerticalBlock"]{gap:0 !important;}
[data-testid="stHorizontalBlock"]{gap:0 !important;}

/* HERO */
.hero{
  background:var(--bg);border-bottom:1px solid var(--border);
  padding:1.1rem 2rem 0.9rem;
  display:flex;align-items:center;justify-content:space-between;
  position:relative;overflow:hidden;
}
.hero::before{
  content:'';position:absolute;inset:0;
  background:radial-gradient(ellipse 60% 80% at 15% 50%,rgba(0,245,255,0.04) 0%,transparent 70%),
             radial-gradient(ellipse 40% 60% at 85% 50%,rgba(255,107,0,0.03) 0%,transparent 70%);
  pointer-events:none;
}
.app-name{
  font-family:'Bebas Neue',sans-serif;
  font-size:clamp(1.8rem,3.5vw,2.8rem);letter-spacing:0.12em;
  background:linear-gradient(90deg,var(--cyan),#0088ff,var(--cyan));
  background-size:200% auto;
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  animation:flow 3s linear infinite;line-height:1;
}
@keyframes flow{0%{background-position:0% center;}100%{background-position:200% center;}}
.app-sub{
  font-family:'Share Tech Mono',monospace;font-size:0.58rem;
  color:var(--dim);letter-spacing:0.28em;text-transform:uppercase;margin-top:0.15rem;
}
.hero-right{display:flex;flex-direction:column;align-items:flex-end;gap:0.25rem;}
.dev-tag{font-family:'Share Tech Mono',monospace;font-size:0.55rem;color:var(--dim);letter-spacing:0.15em;}
.dev-name{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:0.9rem;color:var(--orange);letter-spacing:0.08em;}
.model-pill{
  display:inline-flex;align-items:center;gap:0.4rem;
  background:rgba(0,245,255,0.06);border:1px solid rgba(0,245,255,0.2);
  border-radius:20px;padding:0.18rem 0.65rem;
  font-family:'Share Tech Mono',monospace;font-size:0.55rem;color:var(--cyan);letter-spacing:0.08em;
}
.dot-live{
  width:5px;height:5px;background:var(--green);border-radius:50%;
  animation:pulse-dot 1.5s ease-in-out infinite;
}
@keyframes pulse-dot{0%,100%{opacity:1;transform:scale(1);}50%{opacity:0.3;transform:scale(0.6);}}

/* STATUS BAR */
.status-bar{
  background:var(--surface);border-bottom:1px solid var(--border);
  padding:0.4rem 2rem;display:flex;align-items:center;gap:1.5rem;overflow-x:auto;
}
.stat-item{display:flex;align-items:center;gap:0.45rem;white-space:nowrap;}
.stat-label{font-family:'Share Tech Mono',monospace;font-size:0.55rem;color:var(--dim);letter-spacing:0.15em;text-transform:uppercase;}
.stat-val{font-family:'Bebas Neue',sans-serif;font-size:0.9rem;letter-spacing:0.08em;color:var(--cyan);}
.stat-div{width:1px;height:16px;background:var(--border);}

/* SECTION TITLE */
.sec-title{
  font-family:'Share Tech Mono',monospace;font-size:0.58rem;
  color:var(--dim);letter-spacing:0.22em;text-transform:uppercase;
  padding-bottom:0.45rem;border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  margin-bottom:0.7rem;
}
.sec-num{color:var(--cyan);}

/* UPLOAD */
[data-testid="stFileUploader"]{
  background:var(--panel) !important;border:1.5px dashed var(--border) !important;
  border-radius:8px !important;transition:border-color .3s,background .3s !important;
}
[data-testid="stFileUploader"]:hover{
  border-color:var(--cyan) !important;background:rgba(0,245,255,0.02) !important;
}
[data-testid="stFileUploaderDropzone"]{background:transparent !important;padding:1.8rem 1rem !important;}
[data-testid="stFileUploaderDropzoneInstructions"] p{
  font-family:'Share Tech Mono',monospace !important;font-size:0.7rem !important;color:var(--dim) !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] small{
  font-family:'Share Tech Mono',monospace !important;font-size:0.57rem !important;
}

/* SLIDERS */
[data-testid="stSlider"]{padding:0 !important;}
[data-testid="stSlider"] label p{
  font-family:'Share Tech Mono',monospace !important;font-size:0.58rem !important;
  color:var(--dim) !important;letter-spacing:0.1em !important;text-transform:uppercase !important;
}
[data-baseweb="slider"] [role="slider"]{background:var(--cyan) !important;border-color:var(--cyan) !important;}
[data-baseweb="slider"] [data-testid="stSliderTrackFill"]{background:var(--cyan) !important;}

/* TOGGLE */
[data-testid="stToggle"] label p{
  font-family:'Share Tech Mono',monospace !important;font-size:0.58rem !important;
  color:var(--dim) !important;letter-spacing:0.1em !important;text-transform:uppercase !important;
}

/* SELECT SLIDER */
[data-testid="stSlider"] p{font-family:'Share Tech Mono',monospace !important;font-size:0.58rem !important;color:var(--dim) !important;}

/* BUTTON */
.stButton>button{
  width:100% !important;background:transparent !important;
  border:1.5px solid var(--cyan) !important;color:var(--cyan) !important;
  font-family:'Bebas Neue',sans-serif !important;font-size:0.95rem !important;
  letter-spacing:0.25em !important;padding:0.65rem !important;border-radius:4px !important;
  transition:all .25s !important;
}
.stButton>button:hover{
  background:rgba(0,245,255,0.07) !important;
  box-shadow:0 0 18px rgba(0,245,255,0.18),inset 0 0 18px rgba(0,245,255,0.03) !important;
  transform:translateY(-1px) !important;
}
.stButton>button:disabled{
  border-color:var(--border) !important;color:var(--dim) !important;
  opacity:0.5 !important;cursor:not-allowed !important;
}

/* METRICS */
.metric-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:0.5rem;margin-bottom:0.8rem;}
.metric-cell{
  background:var(--panel);border:1px solid var(--border);border-radius:5px;
  padding:0.65rem 0.5rem;text-align:center;
}
.metric-num{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;line-height:1;color:var(--cyan);}
.metric-lbl{font-family:'Share Tech Mono',monospace;font-size:0.5rem;color:var(--dim);letter-spacing:0.1em;margin-top:0.15rem;}

/* VERDICT */
.verdict-wrap{display:flex;align-items:stretch;gap:0.6rem;margin:0.6rem 0;}
.verdict-score{
  flex:0 0 80px;border:1px solid var(--border);border-radius:5px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:0.7rem 0.4rem;background:rgba(0,0,0,0.3);
}
.verdict-icon{font-size:1.8rem;line-height:1;}
.verdict-word{font-family:'Bebas Neue',sans-serif;font-size:0.9rem;letter-spacing:0.1em;margin-top:0.15rem;}
.verdict-action{
  flex:1;border:1px solid var(--border);border-radius:5px;
  padding:0.7rem 0.9rem;display:flex;flex-direction:column;justify-content:center;gap:0.2rem;
}
.verdict-title{font-family:'Bebas Neue',sans-serif;font-size:1.1rem;letter-spacing:0.08em;}
.verdict-sub{font-family:'Share Tech Mono',monospace;font-size:0.58rem;color:var(--dim);letter-spacing:0.08em;}

/* CLASS ROWS */
.cls-row{
  display:flex;align-items:center;gap:0.6rem;
  padding:0.45rem 0;border-bottom:1px solid rgba(30,37,48,0.6);
}
.cls-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.cls-name{font-family:'Rajdhani',sans-serif;font-weight:700;font-size:0.82rem;letter-spacing:0.08em;text-transform:uppercase;flex:1;}
.cls-count{font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:var(--dim);}
.conf-track{flex:0 0 70px;height:3px;background:var(--border);border-radius:2px;overflow:hidden;}
.conf-fill{height:100%;border-radius:2px;}
.cls-conf{font-family:'Bebas Neue',sans-serif;font-size:0.9rem;letter-spacing:0.05em;min-width:36px;text-align:right;}

/* IDLE */
.idle-box{
  border:1px dashed var(--border);border-radius:6px;padding:2.5rem 1rem;
  text-align:center;display:flex;flex-direction:column;align-items:center;gap:0.5rem;
}
.idle-icon{font-size:2.2rem;opacity:0.15;animation:spin-slow 14s linear infinite;}
@keyframes spin-slow{to{transform:rotate(360deg);}}
.idle-text{font-family:'Share Tech Mono',monospace;font-size:0.62rem;color:var(--dim);letter-spacing:0.2em;text-transform:uppercase;}

/* SCAN ANIM */
.scan-wrap{
  border:1px solid rgba(0,245,255,0.18);border-radius:6px;padding:2rem 1rem;
  text-align:center;background:rgba(0,245,255,0.02);position:relative;overflow:hidden;
}
.scan-line{
  position:absolute;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--cyan),transparent);
  animation:scan 1.4s ease-in-out infinite;
}
@keyframes scan{0%{top:0;opacity:0;}10%{opacity:1;}90%{opacity:1;}100%{top:100%;opacity:0;}}
.scan-text{
  font-family:'Share Tech Mono',monospace;font-size:0.68rem;color:var(--cyan);
  letter-spacing:0.25em;animation:blink .9s step-end infinite;
}
@keyframes blink{50%{opacity:0.2;}}

/* IMAGES */
[data-testid="stImage"] img{border-radius:4px !important;width:100% !important;}

/* DIVIDER LINE */
.col-sep{position:relative;}
.col-sep::before{
  content:'';position:absolute;top:0;left:0;bottom:0;width:1px;
  background:var(--border);
}

/* RESPONSIVE */
@media(max-width:768px){
  .metric-strip{grid-template-columns:repeat(2,1fr) !important;}
  .hero{flex-direction:column;align-items:flex-start;gap:0.4rem;}
  .hero-right{align-items:flex-start;}
  .status-bar{gap:0.8rem;padding:.4rem 1rem;}
}

p,li,label{color:var(--text) !important;}
h1,h2,h3{font-family:'Rajdhani',sans-serif !important;color:var(--text) !important;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────
MODEL_URL  = "https://huggingface.co/ritesht04/Gear_Detection/resolve/main/best%20(3).pt"
MODEL_PATH = Path("best.pt")
CLASS_NAMES = {0: "break", 1: "lack", 2: "scratch"}
CLASS_CSS   = {"break": "#ff2d55", "lack": "#00ff88", "scratch": "#00f5ff"}
CLASS_BGR   = {"break": (45, 45, 255), "lack": (136, 255, 0), "scratch": (255, 245, 0)}

# ─────────────────────────────────────────────────────────────
#  MODEL LOADER
# ─────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    from ultralytics import YOLO
    if not MODEL_PATH.exists():
        ph = st.empty()
        with requests.get(MODEL_URL, stream=True) as r:
            r.raise_for_status()
            total, downloaded = int(r.headers.get("content-length", 0)), 0
            with open(MODEL_PATH, "wb") as f:
                for chunk in r.iter_content(chunk_size=16384):
                    f.write(chunk); downloaded += len(chunk)
                    if total:
                        ph.progress(downloaded/total,
                                    text=f"⚡ Downloading model… {downloaded/1e6:.1f}/{total/1e6:.1f} MB")
        ph.empty()
    return YOLO(str(MODEL_PATH))

# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────
def run_inference(model, img_path, conf, iou, imgsz, augment):
    return model.predict(source=str(img_path), imgsz=imgsz,
                         conf=conf, iou=iou, device="cpu",
                         augment=augment, verbose=False)[0]

def draw_boxes(result, img_bgr):
    drawn = img_bgr.copy(); dets = []
    if result.obb is not None and len(result.obb) > 0:
        for i in range(len(result.obb)):
            cid   = int(result.obb.cls[i].item())
            cf    = float(result.obb.conf[i].item())
            cn    = CLASS_NAMES.get(cid, "unknown")
            color = CLASS_BGR.get(cn, (200, 200, 200))
            pts   = result.obb.xyxyxyxy[i].cpu().numpy().reshape((-1,1,2)).astype(np.int32)
            cv2.polylines(drawn, [pts], True, color, 3)
            xy    = result.obb.xyxyxyxy[i].cpu().numpy()
            x1,y1 = int(xy[:,0].min()), int(xy[:,1].min())
            lbl   = f"{cn} {cf:.0%}"
            fs,th = 0.55, 2
            (tw,thh),_ = cv2.getTextSize(lbl, cv2.FONT_HERSHEY_SIMPLEX, fs, th)
            cv2.rectangle(drawn,(x1,y1-thh-8),(x1+tw+5,y1),color,-1)
            cv2.putText(drawn,lbl,(x1+3,y1-3),cv2.FONT_HERSHEY_SIMPLEX,fs,(0,0,0),th)
            dets.append({"class":cn,"conf":cf})
    return drawn, dets

def verdict(total, dets):
    if total == 0:   return "✅","#00ff88","NORMAL","PASS — Clear for production"
    cls = {d["class"] for d in dets}
    if total>=5 or "break" in cls: return "❌","#ff2d55","HIGH",  "REJECT — Discard immediately"
    if total>=2:     return "⚠️","#ffd700","MEDIUM","INSPECT — Manual review required"
    return "🔎","#00f5ff","LOW","MONITOR — Flag for next inspection"

# ─────────────────────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div>
    <div class="app-name">GEAR_DEFECT_APP</div>
    <div class="app-sub">YOLOv8-OBB · Oriented Bounding Box · Industrial Quality Control</div>
  </div>
  <div class="hero-right">
    <div class="dev-tag">DEVELOPED BY</div>
    <div class="dev-name">SHUBHAM VERMA</div>
    <div class="model-pill"><div class="dot-live"></div>YOLOv8m-OBB · mAP50 99.4%</div>
  </div>
</div>
<div class="status-bar">
  <div class="stat-item"><span class="stat-label">MODEL</span><span class="stat-val">YOLOv8m-OBB</span></div>
  <div class="stat-div"></div>
  <div class="stat-item"><span class="stat-label">CLASSES</span><span class="stat-val">3</span></div>
  <div class="stat-div"></div>
  <div class="stat-item"><span class="stat-label">mAP50</span><span class="stat-val" style="color:#00ff88;">99.4%</span></div>
  <div class="stat-div"></div>
  <div class="stat-item"><span class="stat-label">PRECISION</span><span class="stat-val">98.7%</span></div>
  <div class="stat-div"></div>
  <div class="stat-item"><span class="stat-label">RECALL</span><span class="stat-val">99.7%</span></div>
  <div class="stat-div"></div>
  <div class="stat-item"><span class="stat-label">PARAMS</span><span class="stat-val">26.4M</span></div>
  <div class="stat-div"></div>
  <div class="stat-item"><span class="stat-label">DATASET</span><span class="stat-val">2978 IMGS</span></div>
  <div class="stat-div"></div>
  <div class="stat-item"><span class="stat-label">SOURCE</span><span class="stat-val">HuggingFace</span></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
#  LOAD MODEL
# ─────────────────────────────────────────────────────────────
try:
    model = load_model()
except Exception as e:
    st.error(f"Model load failed: {e}"); st.stop()

# ─────────────────────────────────────────────────────────────
#  MAIN — TWO COLUMNS
# ─────────────────────────────────────────────────────────────
L, R = st.columns([1, 1], gap="small")

# ══════════  LEFT  ══════════
with L:
    st.markdown('<div style="padding:1.2rem 1.6rem 0;">', unsafe_allow_html=True)

    # Upload
    st.markdown('<div class="sec-title"><span>UPLOAD GEAR IMAGE</span><span class="sec-num">01</span></div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=["jpg","jpeg","png","bmp","webp"], label_visibility="collapsed")

    # Settings
    st.markdown('<div class="sec-title" style="margin-top:0.9rem;"><span>DETECTION PARAMETERS</span><span class="sec-num">02</span></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        conf_t = st.slider("CONFIDENCE",  0.10, 0.90, 0.20, 0.05)
        img_sz = st.select_slider("RESOLUTION", [640,960,1280], 1280)
    with c2:
        iou_t  = st.slider("IoU THRESHOLD", 0.10, 0.70, 0.30, 0.05)
        use_tta = st.toggle("TEST-TIME AUG", True)

    # Legend
    st.markdown("""
    <div class="sec-title" style="margin-top:0.9rem;"><span>DEFECT LEGEND</span><span class="sec-num">03</span></div>
    <div style="display:flex;flex-direction:column;gap:0.35rem;margin-bottom:0.9rem;">
      <div style="display:flex;align-items:center;gap:0.7rem;padding:0.35rem 0.7rem;background:rgba(255,45,85,0.06);border:1px solid rgba(255,45,85,0.15);border-radius:4px;">
        <div style="width:9px;height:9px;border-radius:50%;background:#ff2d55;flex-shrink:0;box-shadow:0 0 6px #ff2d5580;"></div>
        <span style="font-family:Rajdhani,sans-serif;font-weight:700;font-size:0.82rem;color:#ff2d55;letter-spacing:0.1em;">BREAK</span>
        <span style="font-family:Share Tech Mono,monospace;font-size:0.57rem;color:#4a5568;margin-left:auto;">Broken / chipped gear tooth</span>
      </div>
      <div style="display:flex;align-items:center;gap:0.7rem;padding:0.35rem 0.7rem;background:rgba(0,255,136,0.06);border:1px solid rgba(0,255,136,0.15);border-radius:4px;">
        <div style="width:9px;height:9px;border-radius:50%;background:#00ff88;flex-shrink:0;box-shadow:0 0 6px #00ff8880;"></div>
        <span style="font-family:Rajdhani,sans-serif;font-weight:700;font-size:0.82rem;color:#00ff88;letter-spacing:0.1em;">LACK</span>
        <span style="font-family:Share Tech Mono,monospace;font-size:0.57rem;color:#4a5568;margin-left:auto;">Missing material / tooth gap</span>
      </div>
      <div style="display:flex;align-items:center;gap:0.7rem;padding:0.35rem 0.7rem;background:rgba(0,245,255,0.06);border:1px solid rgba(0,245,255,0.15);border-radius:4px;">
        <div style="width:9px;height:9px;border-radius:50%;background:#00f5ff;flex-shrink:0;box-shadow:0 0 6px #00f5ff80;"></div>
        <span style="font-family:Rajdhani,sans-serif;font-weight:700;font-size:0.82rem;color:#00f5ff;letter-spacing:0.1em;">SCRATCH</span>
        <span style="font-family:Share Tech Mono,monospace;font-size:0.57rem;color:#4a5568;margin-left:auto;">Surface scratch / abrasion</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Preview
    if uploaded:
        img_pil = Image.open(uploaded).convert("RGB")
        arr = np.array(img_pil)
        h, w = arr.shape[:2]
        st.markdown('<div class="sec-title"><span>PREVIEW</span><span class="sec-num">04</span></div>', unsafe_allow_html=True)
        st.image(img_pil, use_container_width=True)
        st.markdown(f"""
        <div style="display:flex;gap:1rem;margin-top:0.4rem;">
          <div style="flex:1;display:flex;justify-content:space-between;padding:0.3rem 0.5rem;background:var(--panel);border:1px solid var(--border);border-radius:4px;">
            <span style="font-family:Share Tech Mono,monospace;font-size:0.55rem;color:var(--dim);">SIZE</span>
            <span style="font-family:Bebas Neue,sans-serif;font-size:0.8rem;color:var(--cyan);">{w}×{h}</span>
          </div>
          <div style="flex:1;display:flex;justify-content:space-between;padding:0.3rem 0.5rem;background:var(--panel);border:1px solid var(--border);border-radius:4px;">
            <span style="font-family:Share Tech Mono,monospace;font-size:0.55rem;color:var(--dim);">FORMAT</span>
            <span style="font-family:Bebas Neue,sans-serif;font-size:0.8rem;color:var(--cyan);">{uploaded.type.split('/')[-1].upper()}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Button
    st.markdown('<div style="margin-top:0.9rem;">', unsafe_allow_html=True)
    clicked = st.button("⚡  ANALYZE GEAR SURFACE", disabled=(uploaded is None))
    st.markdown('</div></div>', unsafe_allow_html=True)

# ══════════  RIGHT  ══════════
with R:
    st.markdown('<div style="padding:1.2rem 1.6rem 0;border-left:1px solid #1e2530;">', unsafe_allow_html=True)
    st.markdown('<div class="sec-title"><span>DETECTION OUTPUT</span><span class="sec-num">05</span></div>', unsafe_allow_html=True)

    res_ph = st.empty()

    if not uploaded or not clicked:
        res_ph.markdown("""
        <div class="idle-box">
          <div class="idle-icon">⚙️</div>
          <div class="idle-text">Awaiting Gear Image</div>
          <div style="font-family:Share Tech Mono,monospace;font-size:0.52rem;color:#2d3748;letter-spacing:0.15em;margin-top:0.2rem;">
            Upload an image and click Analyze
          </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Save temp
        suffix = Path(uploaded.name).suffix
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            uploaded.seek(0); tmp.write(uploaded.read()); tmp_path = tmp.name

        img_orig = Image.open(tmp_path).convert("RGB")
        img_bgr  = cv2.cvtColor(np.array(img_orig), cv2.COLOR_RGB2BGR)

        # Scanning
        res_ph.markdown("""
        <div class="scan-wrap">
          <div class="scan-line"></div>
          <div class="scan-text">⚙ ANALYZING GEAR SURFACE...</div>
          <div style="font-family:Share Tech Mono,monospace;font-size:0.52rem;color:#2d3748;margin-top:0.4rem;letter-spacing:0.15em;">Running YOLOv8-OBB inference</div>
        </div>""", unsafe_allow_html=True)

        t0 = time.time()
        result = run_inference(model, tmp_path, conf_t, iou_t, img_sz, use_tta)
        elapsed = time.time() - t0
        drawn_bgr, dets = draw_boxes(result, img_bgr)
        drawn_rgb = cv2.cvtColor(drawn_bgr, cv2.COLOR_BGR2RGB)
        os.unlink(tmp_path)

        total = len(dets)
        cc    = Counter(d["class"] for d in dets)
        avgc  = np.mean([d["conf"] for d in dets]) if dets else 0.0
        vi, vc, vw, va = verdict(total, dets)

        res_ph.empty()

        # Metrics
        st.markdown(f"""
        <div class="metric-strip">
          <div class="metric-cell">
            <div class="metric-num" style="color:{'#ff2d55' if total>0 else '#00ff88'};">{total}</div>
            <div class="metric-lbl">DEFECTS</div>
          </div>
          <div class="metric-cell">
            <div class="metric-num">{elapsed*1000:.0f}<span style="font-size:0.7rem;">ms</span></div>
            <div class="metric-lbl">INFERENCE</div>
          </div>
          <div class="metric-cell">
            <div class="metric-num">{avgc:.0%}</div>
            <div class="metric-lbl">AVG CONF</div>
          </div>
          <div class="metric-cell">
            <div class="metric-num">{len(cc)}</div>
            <div class="metric-lbl">CLASS HITS</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Result image
        st.markdown('<div class="sec-title"><span>ANNOTATED OUTPUT</span></div>', unsafe_allow_html=True)
        st.image(drawn_rgb, use_container_width=True)

        # Verdict
        act_parts = va.split("—")
        act_title = act_parts[0].strip()
        act_sub   = act_parts[1].strip() if len(act_parts) > 1 else ""
        st.markdown(f"""
        <div class="verdict-wrap">
          <div class="verdict-score" style="border-color:{vc}25;">
            <div class="verdict-icon">{vi}</div>
            <div class="verdict-word" style="color:{vc};">{vw}</div>
          </div>
          <div class="verdict-action" style="border-color:{vc}25;background:{vc}05;">
            <div class="verdict-title" style="color:{vc};">{act_title}</div>
            <div class="verdict-sub">{act_sub}</div>
            <div style="height:2px;background:{vc};border-radius:1px;opacity:0.25;margin-top:0.3rem;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Breakdown
        st.markdown('<div class="sec-title"><span>DEFECT BREAKDOWN</span></div>', unsafe_allow_html=True)
        if not dets:
            st.markdown("""
            <div style="padding:0.7rem;background:rgba(0,255,136,0.04);
                        border:1px solid rgba(0,255,136,0.15);border-radius:5px;
                        font-family:Share Tech Mono,monospace;font-size:0.65rem;
                        color:#00ff88;letter-spacing:0.08em;">
              ✓ No defects detected — Gear is within normal parameters
            </div>""", unsafe_allow_html=True)
        else:
            rows = ""
            for cn, cnt in cc.items():
                confs = [d["conf"] for d in dets if d["class"]==cn]
                avg   = np.mean(confs)
                col   = CLASS_CSS[cn]
                rows += f"""
                <div class="cls-row">
                  <div class="cls-dot" style="background:{col};box-shadow:0 0 5px {col}70;"></div>
                  <div class="cls-name" style="color:{col};">{cn}</div>
                  <div class="cls-count">{cnt} instance{'s' if cnt>1 else ''}</div>
                  <div class="conf-track"><div class="conf-fill" style="width:{avg*100:.0f}%;background:{col};"></div></div>
                  <div class="cls-conf" style="color:{col};">{avg:.0%}</div>
                </div>"""
            st.markdown(rows, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div style="border-top:1px solid #1e2530;padding:0.5rem 2rem;
            display:flex;justify-content:space-between;align-items:center;background:#0d0f12;margin-top:1rem;">
  <span style="font-family:Share Tech Mono,monospace;font-size:0.52rem;color:#2d3748;letter-spacing:0.12em;">
    GEAR_DEFECT_APP · YOLOv8m-OBB · 99.4% mAP50 · Developed by Shubham Verma
  </span>
  <span style="font-family:Share Tech Mono,monospace;font-size:0.52rem;color:#2d3748;letter-spacing:0.12em;">
    🤗 ritesht04/Gear_Detection
  </span>
</div>
""", unsafe_allow_html=True)
