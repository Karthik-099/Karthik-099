#!/usr/bin/env python3
"""Render the animated profile cards in ./assets, one dark and one light file each.

Run from the repo root:  python3 scripts/build_assets.py
Everything is plain SVG + CSS/SMIL, uses system fonts only, and honours
prefers-reduced-motion, so it renders the same through GitHub's image proxy.
"""
from pathlib import Path
from xml.sax.saxutils import escape

from icons import AZURE, ICONS

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": dict(
        bg="#0d1117", card="#161b22", card2="#0f141b", border="#30363d", grid="#21262d",
        text="#e6edf3", muted="#8b949e", accent="#22d3ee", accent2="#a78bfa", ok="#3fb950",
        warn="#f0b429", err="#f85149", blue="#58a6ff", glow="0.18",
    ),
    "light": dict(
        bg="#ffffff", card="#f6f8fa", card2="#ffffff", border="#d0d7de", grid="#eaeef2",
        text="#1f2328", muted="#57606a", accent="#0891b2", accent2="#7c3aed", ok="#1a7f37",
        warn="#9a6700", err="#cf222e", blue="#0969da", glow="0.10",
    ),
}

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"


def svg(w, h, body, t, extra_css="", label=""):
    css = f"""
    .mono{{font-family:{MONO}}} .sans{{font-family:{SANS}}}
    .tx{{fill:{t['text']}}} .mu{{fill:{t['muted']}}} .ac{{fill:{t['accent']}}} .ac2{{fill:{t['accent2']}}}
    .ok{{fill:{t['ok']}}} .wn{{fill:{t['warn']}}} .er{{fill:{t['err']}}} .bl{{fill:{t['blue']}}}
    .card{{fill:{t['card']};stroke:{t['border']};stroke-width:1}}
    .card2{{fill:{t['card2']};stroke:{t['border']};stroke-width:1}}
    @keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.35}}}}
    @keyframes ring{{0%{{r:6;opacity:.7}}100%{{r:18;opacity:0}}}}
    @keyframes blink{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
    @keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
    @keyframes draw{{to{{stroke-dashoffset:0}}}}
    @keyframes flow{{to{{stroke-dashoffset:-24}}}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    .pulse{{animation:pulse 2.4s ease-in-out infinite}}
    .blink{{animation:blink 1.1s step-end infinite}}
    .rise{{animation:rise .6s ease-out backwards}}
    .flow{{stroke-dasharray:6 6;animation:flow 1.2s linear infinite}}
    {extra_css}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important;opacity:1!important}}}}
    """
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(label)}"><title>{escape(label)}</title>'
        f"<style>{css}</style>{body}</svg>"
    )


def chip(x, y, label, t, color=None, fs=13):
    """Monospace pill; width is computed from the character count (0.62em per glyph)."""
    color = color or t["accent"]
    w = len(label) * fs * 0.62 + 22
    return (
        f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{fs + 14}" rx="{(fs + 14) / 2}" '
        f'fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".45"/>'
        f'<text x="{x + w / 2:.0f}" y="{y + fs + 3}" text-anchor="middle" class="mono" '
        f'font-size="{fs}" fill="{color}">{escape(label)}</text>'
    ), w


# ───────────────────────────── hero ─────────────────────────────
def hero(t):
    W, H = 1200, 330
    b = [
        f'<defs><pattern id="g" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r="1" fill="{t["grid"]}"/></pattern>'
        f'<radialGradient id="glow" cx="80%" cy="35%" r="60%"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="{t["glow"]}"/>'
        f'<stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="name" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent2"]}"/></linearGradient></defs>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" class="card"/>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#g)"/>',
        f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="url(#glow)"/>',
        # prompt line
        f'<text x="60" y="70" class="mono mu" font-size="15">~ $ <tspan class="tx">kubectl describe engineer karthik</tspan>'
        f'<tspan class="ac blink"> ▍</tspan></text>',
        f'<text x="56" y="148" class="sans rise" font-size="76" font-weight="800" fill="url(#name)" style="animation-delay:.1s">Karthik</text>',
        f'<text x="60" y="190" class="sans tx rise" font-size="26" font-weight="600" style="animation-delay:.3s">DevOps · Platform · Site Reliability Engineer</text>',
        f'<text x="60" y="224" class="sans mu rise" font-size="17" style="animation-delay:.5s">Building reliable, observable and cost-efficient cloud infrastructure.</text>',
    ]
    x = 60
    for i, (lbl, col) in enumerate([("AKS · EKS", t["blue"]), ("GitOps", t["accent"]),
                                    ("Observability", t["accent2"]), ("GPU · Slurm", t["ok"]), ("FinOps", t["warn"])]):
        c, w = chip(x, 256, lbl, t, col)
        b.append(f'<g class="rise" style="animation-delay:{.7 + i * .1:.1f}s">{c}</g>')
        x += w + 10

    # right: a tiny live cluster
    px, py, pw, ph = 780, 34, 386, 262
    b.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" class="card2"/>')
    b.append(f'<text x="{px + 18}" y="{py + 28}" class="mono tx" font-size="13">prod-cluster</text>')
    b.append(f'<circle cx="{px + pw - 74}" cy="{py + 24}" r="4" class="ok pulse"/>'
             f'<text x="{px + pw - 64}" y="{py + 28}" class="mono ok" font-size="12">Ready</text>')
    lb = (px + pw / 2, py + 72)
    b.append(f'<circle cx="{lb[0]}" cy="{lb[1]}" r="17" fill="{t["accent"]}" fill-opacity=".15" stroke="{t["accent"]}"/>'
             f'<text x="{lb[0]}" y="{lb[1] + 4}" text-anchor="middle" class="mono ac" font-size="11" font-weight="700">LB</text>')
    nodes = [px + 18, px + 18 + 122, px + 18 + 244]
    for i, nx in enumerate(nodes):
        ny, nw, nh = py + 140, 106, 104
        cx = nx + nw / 2
        path = f"M{lb[0]},{lb[1] + 17} C{lb[0]},{lb[1] + 45} {cx},{ny - 30} {cx},{ny}"
        b.append(f'<path d="{path}" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>')
        for k in range(2):
            b.append(f'<circle r="3.5" class="ac"><animateMotion dur="2.2s" repeatCount="indefinite" '
                     f'begin="{i * .5 + k * 1.1:.1f}s" path="{path}"/></circle>')
        b.append(f'<rect x="{nx}" y="{ny}" width="{nw}" height="{nh}" rx="10" class="card"/>')
        b.append(f'<text x="{nx + 12}" y="{ny + 22}" class="mono mu" font-size="11">node-{i + 1}</text>')
        for p in range(6):
            qx, qy = nx + 12 + (p % 3) * 30, ny + 36 + (p // 3) * 30
            heal = i == 1 and p == 4
            if heal:
                b.append(f'<rect x="{qx}" y="{qy}" width="22" height="22" rx="5" fill="{t["ok"]}">'
                         f'<animate attributeName="fill" dur="9s" repeatCount="indefinite" keyTimes="0;.55;.6;.75;.8;1" '
                         f'values="{t["ok"]};{t["ok"]};{t["err"]};{t["warn"]};{t["ok"]};{t["ok"]}"/></rect>')
            else:
                b.append(f'<rect x="{qx}" y="{qy}" width="22" height="22" rx="5" class="ok" fill-opacity=".85" '
                         f'style="animation:pulse 3s ease-in-out {((i * 6 + p) * .37) % 3:.2f}s infinite"/>')
    b.append(f'<text x="{px + pw / 2}" y="{py + ph - 0}" text-anchor="middle" class="mono mu" font-size="11" dy="-6">'
             f'self-healing workloads · uninterrupted traffic</text>')
    return svg(W, H, "".join(b), t, label="Karthik. DevOps, Platform and Site Reliability Engineer. Building reliable, observable and cost-efficient cloud infrastructure.")


# ───────────────────────────── status ─────────────────────────────
def status(t):
    W, H = 1200, 76
    b = [
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" class="card"/>',
        f'<circle cx="38" cy="38" r="6" class="ok"/><circle cx="38" cy="38" r="6" fill="none" stroke="{t["ok"]}" stroke-width="2" style="animation:ring 1.8s ease-out infinite"/>',
        f'<text x="60" y="43" class="mono tx" font-size="15">karthik:443</text>',
        f'<text x="172" y="43" class="mono ok" font-size="15" font-weight="700">accepting connections</text>',
        f'<text x="390" y="43" class="sans mu" font-size="15">DevOps · SRE · Platform roles  ·  remote or onsite  ·  Bangalore, IST (UTC+5:30)</text>',
    ]
    c, w = chip(W - 170, 24, "get in touch →", t, t["accent"], 13)
    b.append(c)
    return svg(W, H, "".join(b), t, label="Open to DevOps, SRE and Platform roles. Remote or onsite. Bangalore, IST.")


# ───────────────────────────── impact board ─────────────────────────────
def impact(t):
    W, H = 1200, 250
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" class="card"/>',
         f'<text x="28" y="38" class="mono mu" font-size="13">grafana / <tspan class="tx">impact-in-production</tspan></text>',
         f'<circle cx="{W - 98}" cy="33" r="4" class="ok pulse"/><text x="{W - 88}" y="38" class="mono ok" font-size="12">from prod</text>']
    tiles = [
        ("−40%", "time to detect", "6 products on AKS · Datadog", t["accent"], "down"),
        ("−50%", "infrastructure cost", "spot migration · right-sizing", t["warn"], "down2"),
        ("98%", "GPU cluster availability", "H200 + MI300X · Slurm", t["ok"], "uptime"),
        ("0", "audit findings", "SOC 2 · ISO 27001", t["accent2"], "checks"),
    ]
    tw, gap, x0, y0 = 270, 16, 28, 58
    for i, (num, lbl, sub, col, kind) in enumerate(tiles):
        x = x0 + i * (tw + gap)
        d = .2 + i * .15
        b.append(f'<rect x="{x}" y="{y0}" width="{tw}" height="168" rx="12" class="card2"/>')
        b.append(f'<g class="rise" style="animation-delay:{d:.2f}s">'
                 f'<text x="{x + 18}" y="{y0 + 54}" class="sans" font-size="44" font-weight="800" fill="{col}">{num}</text>'
                 f'<text x="{x + 18}" y="{y0 + 80}" class="sans tx" font-size="15" font-weight="600">{lbl}</text>'
                 f'<text x="{x + 18}" y="{y0 + 100}" class="mono mu" font-size="11.5">{escape(sub)}</text></g>')
        gx, gy, gw, gh = x + 18, y0 + 116, tw - 36, 36
        if kind in ("down", "down2"):
            pts = [.15, .2, .1, .3, .25, .45, .5, .6, .7, .75, .85, .9] if kind == "down" else \
                  [.1, .12, .15, .1, .2, .5, .55, .6, .62, .65, .63, .66]
            line = " ".join(f"{gx + k * gw / (len(pts) - 1):.1f},{gy + p * gh:.1f}" for k, p in enumerate(pts))
            b.append(f'<polyline points="{line}" fill="none" stroke="{col}" stroke-width="2.2" stroke-linejoin="round" '
                     f'stroke-dasharray="400" stroke-dashoffset="400" style="animation:draw 2s ease-out {d + .3:.2f}s forwards"/>')
        elif kind == "uptime":
            n = 30
            bw = gw / n
            for k in range(n):
                c = t["warn"] if k in (11,) else t["ok"]
                b.append(f'<rect x="{gx + k * bw:.1f}" y="{gy + 4}" width="{bw - 2:.1f}" height="{gh - 8}" rx="1.5" fill="{c}" '
                         f'class="rise" style="animation-delay:{d + .3 + k * .03:.2f}s"/>')
        else:
            for k, lab in enumerate(["IAM", "logs", "crypto"]):
                cx = gx + k * 78
                b.append(f'<g class="rise" style="animation-delay:{d + .5 + k * .25:.2f}s">'
                         f'<circle cx="{cx + 10}" cy="{gy + 18}" r="10" fill="{col}" fill-opacity=".15" stroke="{col}"/>'
                         f'<path d="M{cx + 5},{gy + 18} l4,4 l7,-8" fill="none" stroke="{col}" stroke-width="2"/>'
                         f'<text x="{cx + 26}" y="{gy + 22}" class="mono mu" font-size="11.5">{lab}</text></g>')
    return svg(W, H, "".join(b), t, label="Impact in production: 40% faster detection across 6 products, 50% lower infrastructure cost, 98% GPU cluster availability, zero SOC 2 / ISO 27001 audit findings.")


# ───────────────────────────── canary rollout ─────────────────────────────
def canary(t):
    W, H = 520, 400
    T = 14  # cycle seconds
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" class="card"/>',
         f'<circle cx="26" cy="28" r="5" fill="{t["err"]}"/><circle cx="44" cy="28" r="5" fill="{t["warn"]}"/><circle cx="62" cy="28" r="5" fill="{t["ok"]}"/>',
         f'<text x="{W / 2}" y="32" text-anchor="middle" class="mono mu" font-size="12">argo rollouts · canary</text>',
         f'<text x="26" y="72" class="mono tx" font-size="15">rollout/<tspan class="ac">interview-api</tspan></text>',
         f'<text x="26" y="96" class="mono mu" font-size="12">stable <tspan fill="{t["blue"]}">v41</tspan>  →  canary <tspan fill="{t["accent2"]}">v42</tspan></text>']
    steps = [("setWeight 10", .08, .30), ("analysis", .30, .44), ("setWeight 50", .44, .62), ("setWeight 100", .62, .80), ("promoted", .80, 1)]
    # traffic bar
    bx, by, bw = 26, 124, W - 52
    b.append(f'<text x="{bx}" y="{by - 8}" class="mono mu" font-size="11">traffic split</text>')
    b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="26" rx="6" fill="{t["blue"]}" fill-opacity=".85"/>')
    kt = "0;.08;.12;.44;.48;.62;.66;.80;.95;1"
    vals = ";".join(str(v) for v in [0, 0, bw * .1, bw * .1, bw * .5, bw * .5, bw, bw, bw, 0])
    b.append(f'<rect x="{bx}" y="{by}" height="26" rx="6" fill="{t["accent2"]}" width="0">'
             f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" values="{vals}"/></rect>')
    # step list
    for i, (s, a, z) in enumerate(steps):
        y = 196 + i * 26
        b.append(f'<text x="{bx}" y="{y}" class="mono" font-size="13" fill="{t["muted"]}">'
                 f'<animate attributeName="fill" dur="{T}s" repeatCount="indefinite" keyTimes="0;{a};{a + .001:.3f};{z - .001:.3f};{z};1" '
                 f'values="{t["muted"]};{t["muted"]};{t["accent"]};{t["accent"]};{t["muted"]};{t["muted"]}"/>'
                 f'{"▸ " if i < 4 else "● "}{escape(s)}</text>')
    # error-rate sparkline with SLO line
    gx, gy, gw, gh = 250, 186, 244, 110
    b.append(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" rx="10" class="card2"/>')
    b.append(f'<text x="{gx + 12}" y="{gy + 20}" class="mono mu" font-size="11">canary error rate</text>')
    b.append(f'<line x1="{gx + 12}" x2="{gx + gw - 12}" y1="{gy + 44}" y2="{gy + 44}" stroke="{t["err"]}" stroke-dasharray="4 4" stroke-opacity=".7"/>')
    b.append(f'<text x="{gx + gw - 12}" y="{gy + 39}" text-anchor="end" class="mono er" font-size="10">SLO</text>')
    pts = [.82, .86, .8, .84, .79, .83, .85, .8, .82, .78, .81, .8]
    line = " ".join(f"{gx + 12 + k * (gw - 24) / (len(pts) - 1):.1f},{gy + p * gh:.1f}" for k, p in enumerate(pts))
    b.append(f'<polyline points="{line}" fill="none" stroke="{t["ok"]}" stroke-width="2" stroke-dasharray="300" stroke-dashoffset="300">'
             f'<animate attributeName="stroke-dashoffset" dur="{T}s" repeatCount="indefinite" keyTimes="0;.1;.85;1" values="300;300;0;0"/></polyline>')
    # pods
    b.append(f'<text x="{bx}" y="{338}" class="mono mu" font-size="11">pods</text>')
    for k in range(8):
        flip = [.12, .48, .48, .48, .66, .66, .66, .66][k]
        b.append(f'<rect x="{bx + 44 + k * 34}" y="324" width="24" height="20" rx="5" fill="{t["blue"]}">'
                 f'<animate attributeName="fill" dur="{T}s" repeatCount="indefinite" keyTimes="0;{flip};{flip + .001:.3f};.95;.951;1" '
                 f'values="{t["blue"]};{t["blue"]};{t["accent2"]};{t["accent2"]};{t["blue"]};{t["blue"]}"/></rect>')
    b.append(f'<text x="{bx}" y="378" class="mono mu" font-size="11">auto-rollback if the SLO is breached · zero manual steps</text>')
    return svg(W, H, "".join(b), t, label="Animated Argo Rollouts canary: traffic shifts 10%, 50%, 100% to the new version while error rate stays under the SLO, then the release is promoted.")


# ───────────────────────────── shared 3D helpers ─────────────────────────────
# Brand colours; a second value is used on dark backgrounds where the brand colour is too dark.
BRAND = {
    "github": ("#1f2328", "#e6edf3"), "pytest": ("#0a9edc",), "sonarqube": ("#4e9bcd",), "trivy": ("#1904da", "#6c8cff"),
    "terraform": ("#7b42bc", "#a97ff0"), "docker": ("#2496ed",), "argo": ("#ef7b4d",), "kubernetes": ("#326ce5", "#6b95f2"),
    "prometheus": ("#e6522c",), "grafana": ("#f46800",), "pagerduty": ("#06ac38",), "gcp": ("#4285f4",),
    "digitalocean": ("#0080ff",), "aws": ("#ff9900",), "opentelemetry": ("#f5a800",), "helm": ("#0f1689", "#7c8cff"),
    "git": ("#f05032",), "slack": ("#4a154b", "#e8a6e9"), "githubactions": ("#2088ff",),
}
# Hand-drawn glyphs (24 grid) for tools without a public mark.
GLYPHS = {
    "key": "M7 9a3 3 0 1 0 0 6 3 3 0 0 0 0-6zm0-2a5 5 0 0 1 4.9 4H22v2h-2v3h-3v-3h-5.1A5 5 0 1 1 7 7z",
    "shield": "M12 1.5 3.5 4.8v6.4c0 5.2 3.6 10 8.5 11.3 4.9-1.3 8.5-6.1 8.5-11.3V4.8L12 1.5zm-1.3 14.9-4-4 1.5-1.5 2.5 2.5 5.6-5.6 1.5 1.5-7.1 7.1z",
    "bell": "M12 22a2.5 2.5 0 0 0 2.4-2h-4.8a2.5 2.5 0 0 0 2.4 2zm7-6v-5a7 7 0 0 0-5.5-6.8V3a1.5 1.5 0 0 0-3 0v1.2A7 7 0 0 0 5 11v5l-2 2v1h18v-1l-2-2z",
    "heal": "M12 4V1L7.5 5.5 12 10V6.5a5.5 5.5 0 1 1-5.5 5.5H4a8 8 0 1 0 8-8z",
    "wave": "M2 10h2.5v4H2zm4.5-3H9v10H6.5zM11 3.5h2.5v17H11zM15.5 7H18v10h-2.5zm4.5 3h2.5v4H20z",
    "nat": "M4 7h11l-3-3 1.4-1.4L19 8.2l-5.6 5.6L12 12.4l3-3H4V7zm16 10H9l3 3-1.4 1.4L5 15.8l5.6-5.6 1.4 1.4-3 3h11v2z",
    "gauge": "M3 20h18v1.5H3zM5 13h3v6H5zm5-5h3v11h-3zm5 3h3v8h-3z",
    "check": "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm-1.5 14.6-4.3-4.3 1.6-1.6 2.7 2.7 5.9-5.9 1.6 1.6-7.5 7.5z",
    "rewind": "M11 18V6l-8.5 6 8.5 6zm.5-6 8.5 6V6l-8.5 6z",
    "seal": "M12 1 9.4 3.3 6 2.9l-.9 3.3L2 7.9l1.2 3.2L2 14.3l3.1 1.7.9 3.3 3.4-.4L12 21.2l2.6-2.3 3.4.4.9-3.3 3.1-1.7-1.2-3.2L22 7.9l-3.1-1.7-.9-3.3-3.4.4L12 1zm-1.4 14.4-3.8-3.8 1.4-1.4 2.4 2.4 5.1-5.1 1.4 1.4-6.5 6.5z",
    "vault": "M3 4h18v16H3V4zm2 2v12h14V6H5zm7 2.5a3.5 3.5 0 1 1 0 7 3.5 3.5 0 0 1 0-7zm0 2a1.5 1.5 0 1 0 0 3 1.5 1.5 0 0 0 0-3z",
}


def logo(name, x, y, s, t, color=None):
    """A brand mark or glyph as a nested <svg>; nothing external, so GitHub's proxy renders it."""
    if name == "azure":
        d0, d1, d2 = AZURE
        return (f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="20 26 216 204"><path fill="#0a4f9e" d="{d0}"/>'
                f'<path fill="#0078d4" d="{d1}"/><path fill="#36b4ec" d="{d2}"/></svg>')
    dark = t is THEMES["dark"]
    if color is None:
        c = BRAND.get(name, (t["text"],))
        color = c[-1] if dark else c[0]
    d = ICONS.get(name) or GLYPHS[name]
    return (f'<svg x="{x}" y="{y}" width="{s}" height="{s}" viewBox="0 0 24 24">'
            f'<path fill="{color}" fill-rule="evenodd" d="{d}"/></svg>')


def defs3d(t):
    """Shared gradients, shadow and the perspective floor every 3D card sits on."""
    return (f'<defs><linearGradient id="face" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t["card2"]}"/>'
            f'<stop offset="1" stop-color="{t["card"]}"/></linearGradient>'
            f'<filter id="sh" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="6" '
            f'flood-color="#000" flood-opacity="{.45 if t is THEMES["dark"] else .12}"/></filter>'
            f'<filter id="gl" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            f'<stop offset=".35" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity=".25"/></linearGradient>'
            f'<mask id="fm"><rect width="100%" height="100%" fill="url(#fade)"/></mask></defs>')


def floor(W, H, t):
    """Receding grid: lines converge on a vanishing point above the card, rows get closer towards the horizon."""
    vx, vy = W / 2, -H * 1.1
    g = []
    for k in range(-14, 15):
        bx = W / 2 + k * 110
        g.append(f'<line x1="{vx}" y1="{vy}" x2="{bx}" y2="{H}"/>')
    y = H
    step = 46
    while y > 40 and step > 6:
        g.append(f'<line x1="0" y1="{y:.1f}" x2="{W}" y2="{y:.1f}"/>')
        y -= step
        step *= .92
    return (f'<g mask="url(#fm)" stroke="{t["grid"]}" stroke-width="1" opacity=".9">'
            f'<clipPath id="cc"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16"/></clipPath>'
            f'<g clip-path="url(#cc)">{"".join(g)}</g></g>')


def prism(x, y, w, h, col, t, d=10):
    """Front-facing box extruded up and to the right (cabinet projection)."""
    return (f'<g filter="url(#sh)">'
            f'<polygon points="{x},{y} {x + d},{y - d} {x + w + d},{y - d} {x + w},{y}" fill="{col}" fill-opacity=".38"/>'
            f'<polygon points="{x + w},{y} {x + w + d},{y - d} {x + w + d},{y + h - d} {x + w},{y + h}" fill="{col}" fill-opacity=".62"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#face)" stroke="{t["border"]}"/></g>'
            f'<rect x="{x}" y="{y}" width="3" height="{h}" fill="{col}"/>')


def pulses(times, period, width=1.0):
    """keyTimes/values that flash 0→1→0 at each time (seconds) within a repeating period."""
    kt, vals = [0.0], [0]
    for s in sorted(times):
        for dt, v in ((0, 0), (.15, 1), (width, 0)):
            p = min((s + dt) / period, 1)
            if p > kt[-1]:
                kt.append(p)
                vals.append(v)
    if kt[-1] < 1:
        kt.append(1)
        vals.append(0)
    return ";".join(f"{k:.4f}" for k in kt), ";".join(map(str, vals))


def glow(x, y, w, h, col, times, period):
    kt, vals = pulses(times, period)
    return (f'<rect x="{x - 2}" y="{y - 2}" width="{w + 4}" height="{h + 4}" rx="3" fill="none" stroke="{col}" stroke-width="2.5" opacity="0">'
            f'<animate attributeName="opacity" dur="{period}s" repeatCount="indefinite" keyTimes="{kt}" values="{vals}"/></rect>')


class Track:
    """A path built from straight runs and quarter turns, with its length known so stages can sync to a moving packet."""

    def __init__(self, x, y):
        self.d, self.x, self.y, self.len, self.marks = [f"M{x},{y}"], x, y, 0.0, {}

    def h(self, x):
        self.len += abs(x - self.x)
        self.d.append(f"H{x}")
        self.x = x
        return self

    def v(self, y):
        self.len += abs(y - self.y)
        self.d.append(f"V{y}")
        self.y = y
        return self

    def turn(self, dx, dy):
        """Quarter circle of radius |dx| (= |dy|) ending dx, dy away."""
        sweep = 1 if (dx > 0) == (dy > 0) else 0
        sweep = sweep if self.d[-1].startswith("H") else 1 - sweep
        self.d.append(f"a{abs(dx)},{abs(dy)} 0 0 {sweep} {dx},{dy}")
        self.x += dx
        self.y += dy
        self.len += 1.5708 * abs(dx)
        return self

    def at(self, name):
        self.marks[name] = self.len
        return self

    def path(self):
        return " ".join(self.d)


def stage_card(x, y, w, h, num, name, tool, icon, col, t):
    out = [prism(x, y, w, h, col, t),
           f'<text x="{x + 12}" y="{y + 20}" class="mono mu" font-size="10">{num}</text>',
           logo(icon, x + w - 30, y + 8, 20, t),
           f'<text x="{x + 12}" y="{y + 46}" class="sans tx" font-size="13.5" font-weight="700">{escape(name)}</text>']
    for k, line in enumerate(tool.split("\n")):
        out.append(f'<text x="{x + 12}" y="{y + 65 + k * 14}" class="mono mu" font-size="10.5">{escape(line)}</text>')
    return "".join(out)


# ───────────────────────────── delivery pipeline ─────────────────────────────
def pipeline(t):
    W, H = 1200, 660
    P = 24.0            # one animation period = two releases: one promoted, one rolled back
    RUN = 8.5           # seconds for a commit to travel from PR to analysis
    SEC, BLD, OPS, OBS, PRD = t["warn"], t["blue"], t["accent2"], t["accent"], t["ok"]
    w, gap, x0, h = 134, 26, 46, 92
    ys = [128, 300, 482]
    slot = lambda i: x0 + i * (w + gap)
    rows = [
        [("Commit", "pull request\nbranch protection", "github", BLD),
         ("Secret scan", "Gitleaks\nno creds in git", "key", SEC),
         ("Unit tests", "pytest · Jest\ncoverage gate", "pytest", BLD),
         ("Code quality", "SonarQube\nquality gate", "sonarqube", SEC),
         ("Dependencies", "Trivy SCA\nSBOM · licences", "trivy", SEC),
         ("Policy as code", "Terraform plan\nKyverno CLI", "terraform", SEC),
         ("Docker build", "multi-stage\ndistroless base", "docker", BLD)],
        [("Image scan", "Trivy image\nfail on HIGH/CRIT", "trivy", SEC),
         ("Sign + push", "cosign signature\nDockerHub/ECR/ACR", "seal", BLD),
         ("Config repo", "Helm values bump\npin image digest", "git", OPS),
         ("Argo CD sync", "pull-based GitOps\ndrift auto-heal", "argo", OPS),
         ("Admission", "Kyverno: signed,\nnon-root, limits", "shield", SEC),
         ("Canary", "Argo Rollouts\n10 → 50 → 100%", "argo", OPS),
         ("Production", "AKS · EKS · GKE\nDOKS · Key Vault", "kubernetes", PRD)],
        [("Observe", "Prometheus · Loki\nTempo · Grafana", "prometheus", OBS),
         ("SLO analysis", "AnalysisRun\nerror rate · p99", "gauge", OBS)],
    ]
    b = [defs3d(t), f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" class="card"/>', floor(W, H, t),
         f'<text x="28" y="40" class="mono mu" font-size="13">pipeline / <tspan class="tx">enterprise-gitops-delivery</tspan></text>',
         f'<text x="{W - 28}" y="40" text-anchor="end" class="mono mu" font-size="12">shift-left security · immutable digests · pull-based deploys · self-healing</text>']
    lanes = [("01", "CONTINUOUS INTEGRATION", "every pull request is gated before it can merge"),
             ("02", "RELEASE + GITOPS DELIVERY", "Git is the source of truth; the cluster pulls, nothing pushes in"),
             ("03", "VERIFY + SELF-HEAL", "")]
    for (n, title, sub), y in zip(lanes, ys):
        b.append(f'<text x="{x0}" y="{y - 26}" class="mono" font-size="11" letter-spacing="1.2">'
                 f'<tspan class="ac" font-weight="700">{n}</tspan><tspan class="tx" font-weight="700">  {title}</tspan>'
                 f'<tspan class="mu" letter-spacing="0">{"   " + sub if sub else ""}</tspan></text>')

    # conveyor track under each row; row 2 runs right-to-left (snake)
    r = 16
    rail = [y + h + 18 for y in ys]
    tr = Track(x0 - 16, rail[0])
    marks = []
    xs_r0 = [slot(i) + w / 2 for i in range(7)]
    tr.h(x0)
    for cx in xs_r0:
        tr.h(cx).at(len(marks))
        marks.append(None)
    tr.h(W - 34 - r).turn(r, r).v(rail[1] - r).turn(-r, r)
    for i in range(6, -1, -1):
        tr.h(slot(i) + w / 2).at(len(marks))
        marks.append(None)
    tr.h(30).turn(-r, r).v(rail[2] - r).turn(r, r)
    for i in range(2):
        tr.h(slot(i) + w / 2).at(len(marks))
        marks.append(None)
    tr.h(slot(1) + w + 30)
    main = tr.path()
    L = tr.len
    fork_x, fork_y = tr.x, tr.y

    b.append(f'<path d="{main}" fill="none" stroke="{t["border"]}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(f'<path d="{main}" fill="none" stroke="{t["muted"]}" stroke-opacity=".55" stroke-width="1.5" class="flow"/>')

    # stage cards, each lights up as the packet passes underneath it
    order = [(0, i) for i in range(7)] + [(1, i) for i in range(6, -1, -1)] + [(2, i) for i in range(2)]
    num = 0
    pos = {}
    for k, (row, i) in enumerate(order):
        name, tool, icon, col = rows[row][i if row != 1 else 6 - i]
        x, y = slot(i), ys[row]
        pos[name] = (x, y)
        num += 1
        b.append(stage_card(x, y, w, h, f"{num:02d}", name, tool, icon, col, t))
        f = tr.marks[k] / L
        b.append(glow(x, y, w, h, col, [f * RUN, P / 2 + f * RUN], P))
        b.append(f'<line x1="{x + w / 2}" y1="{y + h}" x2="{x + w / 2}" y2="{rail[row] - 3}" stroke="{t["border"]}" stroke-width="2"/>')

    # the release packet: runs the whole track twice per period
    e = .001
    kp = "0;1;1;0;1;1"
    kt = f"0;{RUN / P:.4f};{.5 - e:.4f};.5;{.5 + RUN / P:.4f};1"
    vis_kt = f"0;.005;{RUN / P:.4f};{RUN / P + .02:.4f};.5;.505;{.5 + RUN / P:.4f};{.5 + RUN / P + .02:.4f};1"
    for rr, op in ((11, .25), (6, 1)):
        b.append(f'<circle r="{rr}" class="ac" opacity="0"{" filter=" + chr(34) + "url(#gl)" + chr(34) if rr > 6 else ""}>'
                 f'<animateMotion dur="{P}s" repeatCount="indefinite" path="{main}" keyPoints="{kp}" keyTimes="{kt}" calcMode="linear"/>'
                 f'<animate attributeName="opacity" dur="{P}s" repeatCount="indefinite" keyTimes="{vis_kt}" values="0;{op};{op};0;0;{op};{op};0;0"/></circle>')

    # decision fork: first release is promoted, second breaches the SLO and is reverted
    ox, ow, oh = fork_x + 40, 214, 58
    py_, ry_ = ys[2] - 14, ys[2] + 66
    outs = [("Promote", "100% traffic · release done", "check", PRD, py_),
            ("Auto-rollback", "abort · page PagerDuty · RCA", "rewind", t["err"], ry_)]
    branch = {}
    for name, sub, icon, col, oy in outs:
        b.append(prism(ox, oy, ow, oh, col, t))
        b.append(logo(icon, ox + 12, oy + 10, 18, t, col))
        b.append(f'<text x="{ox + 38}" y="{oy + 24}" class="sans tx" font-size="13.5" font-weight="700">{name}</text>')
        b.append(f'<text x="{ox + 12}" y="{oy + 46}" class="mono mu" font-size="10.5">{sub}</text>')
        p = f"M{fork_x},{fork_y} C{fork_x + 24},{fork_y} {ox - 26},{oy + oh / 2} {ox},{oy + oh / 2}"
        branch[name] = p
        b.append(f'<path d="{p}" fill="none" stroke="{col}" stroke-opacity=".5" stroke-width="2" class="flow"/>')
    logo_pd = logo("pagerduty", ox + ow - 28, ry_ + 10, 16, t)
    b.append(logo_pd)
    b.append(f'<text x="{fork_x - 6}" y="{fork_y - 10}" text-anchor="end" class="mono mu" font-size="10">SLO met?</text>')
    for name, start, col, oy in (("Promote", RUN, PRD, py_), ("Auto-rollback", P / 2 + RUN, t["err"], ry_)):
        kt2 = f"0;{start / P:.4f};{(start + 1.2) / P:.4f};1"
        b.append(f'<circle r="5.5" fill="{col}" opacity="0"><animateMotion dur="{P}s" repeatCount="indefinite" path="{branch[name]}" '
                 f'keyPoints="0;0;1;1" keyTimes="{kt2}" calcMode="linear"/>'
                 f'<animate attributeName="opacity" dur="{P}s" repeatCount="indefinite" keyTimes="0;{start / P:.4f};{(start + 1.2) / P:.4f};{(start + 1.25) / P:.4f};1" values="0;0;1;0;0"/></circle>')
        b.append(glow(ox, oy, ow, oh, col, [start + 1.1], P))

    # self-heal: rollback reverts the config repo to the last good digest, Argo CD re-syncs
    cx_, cy_ = pos["Config repo"]
    rb = f"M{ox + ow + 10},{ry_ + oh / 2} C{ox + ow + 120},{ry_ + oh / 2} {cx_ + w / 2},{rail[1] + 120} {cx_ + w / 2},{rail[1] + 8}"
    b.append(f'<path d="{rb}" fill="none" stroke="{t["err"]}" stroke-width="2" stroke-dasharray="6 6" class="flow"/>')
    b.append(f'<path d="M{cx_ + w / 2 - 6},{rail[1] + 18} l6,-9 l6,9" fill="none" stroke="{t["err"]}" stroke-width="2"/>')
    s0 = P / 2 + RUN + 1.3
    b.append(f'<circle r="5.5" fill="{t["err"]}" opacity="0"><animateMotion dur="{P}s" repeatCount="indefinite" path="{rb}" '
             f'keyPoints="0;0;1;1" keyTimes="0;{s0 / P:.4f};{(s0 + 1.6) / P:.4f};1" calcMode="linear"/>'
             f'<animate attributeName="opacity" dur="{P}s" repeatCount="indefinite" keyTimes="0;{s0 / P:.4f};{(s0 + 1.6) / P:.4f};{(s0 + 1.65) / P:.4f};1" values="0;0;1;0;0"/></circle>')
    b.append(glow(cx_, cy_, w, h, t["err"], [s0 + 1.5], P))
    b.append(f'<text x="{cx_ + w / 2 - 12}" y="{rail[1] + 30}" text-anchor="end" class="mono er" font-size="10.5">git revert → last good digest</text>')

    # deploy targets
    tx0, ty0 = 860, ys[2] - 14
    b.append(f'<text x="{tx0}" y="{ty0 - 12}" class="mono mu" font-size="10.5" letter-spacing="1">SAME PIPELINE, ANY CLUSTER</text>')
    targets = [("aws", "EKS"), ("azure", "AKS"), ("gcp", "GKE"), ("digitalocean", "DOKS"), ("wave", "LiveKit")]
    for k, (ic, lbl) in enumerate(targets):
        x = tx0 + k * 60
        b.append(prism(x, ty0, 50, 58, t["border"], t, 6))
        b.append(logo(ic, x + 12, ty0 + 8, 26, t, t["accent"] if ic == "wave" else None))
        b.append(f'<text x="{x + 25}" y="{ty0 + 50}" text-anchor="middle" class="mono tx" font-size="10">{lbl}</text>')
    b.append(f'<text x="{tx0}" y="{ty0 + 86}" class="mono mu" font-size="10.5">Terraform modules · Helm · one Argo CD</text>')
    b.append(f'<text x="{tx0}" y="{ty0 + 102}" class="mono mu" font-size="10.5">ApplicationSet per environment</text>')

    # legend
    lx = 28
    for lbl, col in [("security gate", SEC), ("build + release", BLD), ("GitOps (pull)", OPS),
                     ("observe", OBS), ("live", PRD), ("self-heal path", t["err"])]:
        b.append(f'<rect x="{lx}" y="{H - 34}" width="10" height="10" rx="2" fill="{col}"/>'
                 f'<text x="{lx + 16}" y="{H - 25}" class="mono mu" font-size="11">{lbl}</text>')
        lx += len(lbl) * 6.8 + 42
    b.append(f'<text x="{W - 28}" y="{H - 25}" text-anchor="end" class="mono mu" font-size="11">no kubectl from CI · no long-lived cloud keys (OIDC)</text>')
    return svg(W, H, "".join(b), t, label=PIPELINE_ALT)


PIPELINE_ALT = ("Enterprise GitOps delivery pipeline. CI: commit, Gitleaks secret scan, unit tests, SonarQube quality gate, "
                "Trivy dependency scan and SBOM, Terraform and Kyverno policy as code, Docker build. Release: Trivy image scan, "
                "cosign signing and push to Docker Hub, ECR or ACR, config repo bumped to the image digest, Argo CD pull-based sync, "
                "Kyverno admission, Argo Rollouts canary, production on AKS, EKS, GKE or DOKS. Verify: Prometheus, Loki and Tempo feed "
                "an SLO analysis that promotes the release or rolls it back automatically, pages PagerDuty and reverts the config repo.")


# ───────────────────────────── observability architecture ─────────────────────────────
def slab(cx, cy, a, bb, hh, col, t, title="", sub="", icon=None):
    """Isometric slab; title and subtitle are painted onto the top face."""
    top = f"{cx},{cy - bb} {cx + a},{cy} {cx},{cy + bb} {cx - a},{cy}"
    left = f"{cx - a},{cy} {cx},{cy + bb} {cx},{cy + bb + hh} {cx - a},{cy + hh}"
    right = f"{cx},{cy + bb} {cx + a},{cy} {cx + a},{cy + hh} {cx},{cy + bb + hh}"
    out = [f'<g filter="url(#sh)"><polygon points="{left}" fill="{col}" fill-opacity=".55"/>'
           f'<polygon points="{right}" fill="{col}" fill-opacity=".8"/>'
           f'<polygon points="{top}" fill="{t["card2"]}"/><polygon points="{top}" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".7"/></g>']
    # map the top face to a flat square of side s: local x runs down-right, local y down-left
    s = bb * 2
    sx = a / s
    m = f"matrix({sx:.4f} {.5:.4f} {-sx:.4f} {.5:.4f} {cx} {cy})"
    if icon:
        out.append(f'<g transform="{m}">{logo(icon, -s / 2 + 8, -s / 2 + 8, s * .2, t, col)}</g>')
    if title:
        out.append(f'<g transform="{m}"><text x="{-s / 2 + 8}" y="{s * .12:.1f}" class="sans" font-size="{min(s * .17, 22):.1f}" font-weight="800" fill="{col}">{title}</text>'
                   f'<text x="{-s / 2 + 8}" y="{s * .27:.1f}" class="mono tx" font-size="{s * .085:.1f}">{escape(sub)}</text></g>')
    return "".join(out)


def observability(t):
    W, H = 1200, 730
    P = 6.0
    M, LG, TR, SC = t["accent"], t["warn"], t["accent2"], t["err"]
    b = [defs3d(t), f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" class="card"/>', floor(W, H, t),
         f'<text x="28" y="40" class="mono mu" font-size="13">architecture / <tspan class="tx">multi-cloud-observability-and-self-healing</tspan></text>']
    lx = W - 28
    for name, col in reversed([("metrics", M), ("logs", LG), ("traces", TR), ("security", SC)]):
        lx -= len(name) * 7 + 26
        b.append(f'<circle cx="{lx + 4}" cy="36" r="4" fill="{col}"/><text x="{lx + 13}" y="40" class="mono mu" font-size="11.5">{name}</text>')

    # sources
    b.append(f'<text x="30" y="90" class="mono" font-size="11" letter-spacing="1.2"><tspan class="ac" font-weight="700">01</tspan><tspan class="tx" font-weight="700">  WORKLOADS</tspan></text>')
    srcs = [("azure", "AKS · prod + staging", "Alloy DaemonSet"), ("aws", "EKS", "Alloy · OTel SDK"),
            ("gcp", "GKE", "Alloy · OTel SDK"), ("digitalocean", "DOKS", "Alloy DaemonSet"),
            ("wave", "LiveKit SFU", "media nodes · VMs")]
    sx, sw, sh = 30, 250, 62
    gate = (396, 318)
    src_paths = []
    for i, (ic, name, sub) in enumerate(srcs):
        y = 112 + i * 80
        b.append(prism(sx, y, sw, sh, t["accent"], t, 9))
        b.append(logo(ic, sx + 14, y + 16, 30, t, t["accent"] if ic == "wave" else None))
        b.append(f'<text x="{sx + 58}" y="{y + 27}" class="sans tx" font-size="14" font-weight="700">{name}</text>')
        b.append(f'<text x="{sx + 58}" y="{y + 46}" class="mono mu" font-size="10.5">{sub}</text>')
        for k, col in enumerate((M, LG, TR, SC)):
            b.append(f'<circle cx="{sx + sw - 18}" cy="{y + 14 + k * 11.5}" r="3" fill="{col}" class="pulse" style="animation-delay:{(i + k) * .3:.1f}s"/>')
        p = f"M{sx + sw + 9},{y + sh / 2} C{sx + sw + 60},{y + sh / 2} {gate[0] - 50},{gate[1]} {gate[0]},{gate[1]}"
        src_paths.append(p)
        b.append(f'<path d="{p}" fill="none" stroke="{t["border"]}" stroke-width="1.6"/>')
        for k, col in enumerate((M, LG, TR, SC)):
            if col == SC and i % 2:
                continue
            b.append(f'<circle r="3.2" fill="{col}"><animateMotion dur="2.4s" begin="{(i * .37 + k * .6) % 2.4:.2f}s" repeatCount="indefinite" path="{p}"/></circle>')
    by = 112 + 5 * 80 + 4
    b.append(f'<rect x="{sx}" y="{by}" width="{sw + 9}" height="96" rx="10" class="card2"/>')
    for k, line in enumerate(["collected from every cluster",
                              "node · pod · container CPU + memory",
                              "restarts · OOMKilled · CPU throttling",
                              "k8s events · audit · ingress logs",
                              "OTLP spans · service graph"]):
        b.append(f'<text x="{sx + 14}" y="{by + 22 + k * 16}" class="mono {"tx" if k == 0 else "mu"}" font-size="{11 if k == 0 else 10.5}"'
                 f'{" font-weight=" + chr(34) + "700" + chr(34) if k == 0 else ""}>{line}</text>')

    # hub boundary
    hx, hy, hw, hh = 336, 70, 500, 596
    b.append(f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="18" fill="{t["accent"]}" fill-opacity=".03" stroke="{t["accent"]}" stroke-opacity=".45" stroke-dasharray="7 6"/>')
    b.append(f'<text x="{hx + 18}" y="{hy + 24}" class="mono" font-size="11" letter-spacing="1.2"><tspan class="ac" font-weight="700">02</tspan>'
             f'<tspan class="tx" font-weight="700">  HUB VNET</tspan><tspan class="mu" letter-spacing="0">   private endpoints · peering · RBAC</tspan></text>')

    # gateway
    gx, gy, gw, gh = gate[0], gate[1] - 40, 118, 80
    b.append(prism(gx, gy, gw, gh, t["accent"], t, 9))
    b.append(logo("grafana", gx + 12, gy + 12, 20, t))
    b.append(f'<text x="{gx + 38}" y="{gy + 27}" class="sans tx" font-size="13.5" font-weight="700">Alloy</text>')
    b.append(f'<text x="{gx + 12}" y="{gy + 50}" class="mono mu" font-size="10">gateway · OTLP</text>')
    b.append(f'<text x="{gx + 12}" y="{gy + 65}" class="mono mu" font-size="10">remote_write</text>')

    # LGTM stack as iso slabs, storage underneath
    cx, a, bb, th = 664, 112, 64.7, 16
    tiers = [("Mimir", "metrics · WAL", M, 176, "prometheus"), ("Loki", "logs · LogQL", LG, 288, "grafana"),
             ("Tempo", "traces · OTLP", TR, 400, "opentelemetry")]
    b.append(f'<line x1="{cx}" y1="176" x2="{cx}" y2="548" stroke="{t["blue"]}" stroke-width="2" class="flow"/>')
    for name, sub, col, cy, ic in tiers:
        b.append(slab(cx, cy, a, bb, th, col, t, name, sub, ic))
        p = f"M{gx + gw + 9},{gate[1]} C{gx + gw + 50},{gate[1]} {cx - a - 40},{cy} {cx - a},{cy}"
        b.append(f'<path d="{p}" fill="none" stroke="{col}" stroke-opacity=".45" stroke-width="1.6"/>')
        b.append(f'<circle r="3.6" fill="{col}"><animateMotion dur="1.6s" repeatCount="indefinite" path="{p}"/></circle>')
        b.append(f'<circle r="3.6" fill="{col}"><animateMotion dur="1.6s" begin=".8s" repeatCount="indefinite" path="{p}"/></circle>')
    b.append(slab(cx, 548, 124, 71.6, 20, t["blue"], t, "Storage", "Blob · S3 · GCS", "azure"))
    b.append(f'<path d="M{gx + gw / 2},{gy + gh} V500" stroke="{t["muted"]}" stroke-width="1.4" class="flow"/>')
    b.append(slab(gx + gw / 2, 520, 50, 28.9, 14, t["muted"], t))
    b.append(f'<text x="{gx + gw / 2}" y="{586}" text-anchor="middle" class="mono tx" font-size="10.5">PVC · WAL</text>')
    b.append(f'<text x="{gx + gw / 2}" y="{601}" text-anchor="middle" class="mono mu" font-size="10">gateway buffer</text>')
    b.append(f'<text x="{hx + 18}" y="{hy + hh - 18}" class="mono mu" font-size="10.5">retention tiers · lifecycle rules · egress via NAT only</text>')

    # alert + response chain
    rx, rw = 880, 290
    b.append(f'<text x="{rx}" y="90" class="mono" font-size="11" letter-spacing="1.2"><tspan class="ac" font-weight="700">03</tspan><tspan class="tx" font-weight="700">  DETECT + RESPOND</tspan></text>')
    chain = [("grafana", "Grafana", "dashboards · SLOs · burn rate", M, 62),
             ("bell", "Alerting", "multi-window burn-rate rules", LG, 62),
             ("nat", "NAT gateway", "static egress IP to SaaS", t["muted"], 46),
             ("pagerduty", "PagerDuty · Slack", "on-call · escalation · runbook", t["ok"], 62),
             ("heal", "Self-heal", "rollback · HPA/KEDA · restart", t["err"], 62)]
    y = 112
    ys_ = []
    for k, (ic, name, sub, col, hgt) in enumerate(chain):
        b.append(prism(rx, y, rw, hgt, col, t, 9))
        b.append(logo(ic, rx + 14, y + (hgt - 22) / 2, 22, t, col if ic in ("bell", "nat", "heal") else None))
        b.append(f'<text x="{rx + 48}" y="{y + (25 if hgt > 50 else 21)}" class="sans tx" font-size="14" font-weight="700">{name}</text>')
        b.append(f'<text x="{rx + 48}" y="{y + (44 if hgt > 50 else 36)}" class="mono mu" font-size="10.5">{sub}</text>')
        if k == 3:
            b.append(logo("slack", rx + rw - 32, y + 20, 18, t))
        ys_.append((y, hgt))
        y += hgt + 18
    for k in range(len(chain) - 1):
        y1 = ys_[k][0] + ys_[k][1]
        y2 = ys_[k + 1][0]
        b.append(f'<path d="M{rx + rw / 2},{y1} V{y2}" stroke="{t["muted"]}" stroke-width="1.6" class="flow"/>')
    for name, sub, col, cy, _ in tiers:
        p = f"M{cx + a},{cy} C{cx + a + 50},{cy} {rx - 50},{143} {rx},{143}"
        b.append(f'<path d="{p}" fill="none" stroke="{t["border"]}" stroke-width="1.6"/>')
        b.append(f'<circle r="3.4" fill="{col}"><animateMotion dur="2s" begin="{tiers.index((name, sub, col, cy, _)) * .5}s" repeatCount="indefinite" path="{p}"/></circle>')

    # closed loop back to the workloads
    last_y = ys_[-1][0] + ys_[-1][1] / 2
    loop = f"M{rx + rw + 9},{last_y} H{W - 14} V{H - 44} H14 V{112 + 31} H{sx}"
    b.append(f'<path d="{loop}" fill="none" stroke="{t["ok"]}" stroke-opacity=".7" stroke-width="2" stroke-dasharray="6 6" class="flow"/>')
    for k in range(3):
        b.append(f'<circle r="4.5" fill="{t["ok"]}"><animateMotion dur="7s" begin="{k * 2.33:.2f}s" repeatCount="indefinite" path="{loop}"/></circle>')
    b.append(f'<rect x="{W / 2 - 250}" y="{H - 56}" width="500" height="24" rx="12" fill="{t["card"]}" stroke="{t["ok"]}" stroke-opacity=".6"/>')
    b.append(f'<text x="{W / 2}" y="{H - 40}" text-anchor="middle" class="mono ok" font-size="11.5">closed loop: detect → page → auto-remediate → verify → RCA</text>')

    # security signals
    sy = 112 + sum(hgt + 18 for *_, hgt in chain) + 2
    b.append(f'<rect x="{rx}" y="{sy}" width="{rw + 9}" height="96" rx="10" class="card2"/>')
    b.append(logo("shield", rx + 14, sy + 10, 16, t, SC))
    for k, line in enumerate(["security signals", "Kyverno policy reports · Trivy CVEs",
                              "kube-audit · RBAC + IAM changes", "SOC 2 / ISO 27001 evidence trail"]):
        b.append(f'<text x="{rx + (38 if k == 0 else 14)}" y="{sy + 23 + k * 19}" class="mono {"tx" if k == 0 else "mu"}" font-size="{11 if k == 0 else 10.5}"'
                 f'{" font-weight=" + chr(34) + "700" + chr(34) if k == 0 else ""}>{line}</text>')
    return svg(W, H, "".join(b), t, label=OBS_ALT)


OBS_ALT = ("Multi-cloud observability and self-healing. Grafana Alloy on AKS, EKS, GKE, DOKS and LiveKit media nodes ships metrics, "
           "logs, traces and security events through private endpoints into a hub VNet: an Alloy gateway feeds Mimir, Loki and Tempo, "
           "backed by object storage and PVC write-ahead logs. Grafana SLO burn-rate alerts route through a NAT gateway to PagerDuty and "
           "Slack, and self-healing actions (rollback, autoscaling, restarts) close the loop back to the workloads.")


# ───────────────────────────── terminal card ─────────────────────────────
def terminal(t):
    W, H = 560, 400
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" class="card"/>',
         f'<circle cx="26" cy="28" r="5" fill="{t["err"]}"/><circle cx="44" cy="28" r="5" fill="{t["warn"]}"/><circle cx="62" cy="28" r="5" fill="{t["ok"]}"/>',
         f'<text x="{W / 2}" y="32" text-anchor="middle" class="mono mu" font-size="12">karthik@prod: ~</text>',
         f'<text x="24" y="70" class="mono" font-size="13"><tspan class="ok">karthik@prod</tspan><tspan class="mu">:~$</tspan> <tspan class="tx">neofetch</tspan></text>']
    # spinning helm-style wheel
    cx, cy, r = 104, 190, 64
    spokes = "".join(
        f'<line x1="0" y1="0" x2="0" y2="{-r + 8}" transform="rotate({k * 360 / 7:.2f})" stroke="{t["accent"]}" stroke-width="5" stroke-linecap="round"/>'
        for k in range(7))
    hept = " ".join(
        f"{(r + 6) * __import__('math').sin(k * 2 * 3.14159265 / 7):.1f},{-(r + 6) * __import__('math').cos(k * 2 * 3.14159265 / 7):.1f}"
        for k in range(7))
    b.append(f'<g transform="translate({cx},{cy})"><polygon points="{hept}" fill="{t["accent"]}" fill-opacity=".10" stroke="{t["accent"]}" stroke-width="2" stroke-linejoin="round"/>'
             f'<g style="animation:spin 18s linear infinite">'
             f'<circle r="{r - 18}" fill="none" stroke="{t["accent"]}" stroke-width="5"/>{spokes}<circle r="10" fill="{t["accent"]}"/></g></g>')
    rows = [("role", "DevOps Engineer @ InCruiter"), ("clouds", "Azure · AWS · GCP"),
            ("runs on", "AKS · EKS · bare metal"), ("iac", "Terraform · Ansible · Helm"),
            ("delivery", "Argo CD · GitHub Actions"), ("observe", "LGTM · Datadog · OTel"),
            ("gpus", "H200 · MI300X · Slurm"), ("ai/ml", "LLM serving · Langfuse"),
            ("papers", "5 · IEEE Access (Q1)"), ("tz", "Bangalore · IST")]
    for i, (k, v) in enumerate(rows):
        y = 104 + i * 22
        b.append(f'<text x="200" y="{y}" class="mono rise" font-size="13" style="animation-delay:{.3 + i * .15:.2f}s">'
                 f'<tspan class="ac" font-weight="700">{k}</tspan><tspan class="mu">: </tspan><tspan class="tx">{escape(v)}</tspan></text>')
    for i, c in enumerate([t["err"], t["warn"], t["ok"], t["accent"], t["blue"], t["accent2"], t["muted"], t["text"]]):
        b.append(f'<rect x="{200 + i * 24}" y="336" width="20" height="14" rx="3" fill="{c}" class="rise" style="animation-delay:{2 + i * .05:.2f}s"/>')
    b.append(f'<text x="24" y="380" class="mono" font-size="13"><tspan class="ok">karthik@prod</tspan><tspan class="mu">:~$</tspan><tspan class="ac blink"> ▍</tspan></text>')
    return svg(W, H, "".join(b), t, label="karthik@prod neofetch: DevOps Engineer at InCruiter; Azure, AWS, GCP; AKS, EKS, bare metal; Terraform, Ansible, Helm; Argo CD; LGTM, Datadog, OpenTelemetry; H200, MI300X, Slurm.")


# ───────────────────────────── divider + footer ─────────────────────────────
def divider(t):
    W, H = 1200, 24
    b = [f'<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="{t["accent"]}" stop-opacity=".6"/><stop offset="1" stop-color="{t["accent2"]}" stop-opacity="0"/></linearGradient></defs>',
         f'<rect x="0" y="11" width="{W}" height="2" fill="url(#d)"/>',
         f'<circle cy="12" r="3.5" class="ac"><animate attributeName="cx" dur="7s" repeatCount="indefinite" values="80;1120;80"/>'
         f'<animate attributeName="opacity" dur="7s" repeatCount="indefinite" values=".2;1;.2;1;.2"/></circle>']
    return svg(W, H, "".join(b), t)


def footer(t):
    W, H = 1200, 120
    w1a = f"M0,60 C200,20 400,100 600,60 C800,20 1000,100 1200,60 V{H} H0 Z"
    w1b = f"M0,60 C200,100 400,20 600,60 C800,100 1000,20 1200,60 V{H} H0 Z"
    w2a = f"M0,80 C250,50 450,110 700,80 C900,55 1050,105 1200,80 V{H} H0 Z"
    w2b = f"M0,80 C250,110 450,50 700,80 C900,105 1050,55 1200,80 V{H} H0 Z"
    b = [f'<defs><linearGradient id="f" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}"/><stop offset="1" stop-color="{t["accent2"]}"/></linearGradient></defs>',
         f'<path fill="url(#f)" fill-opacity=".25" d="{w1a}"><animate attributeName="d" dur="9s" repeatCount="indefinite" values="{w1a};{w1b};{w1a}"/></path>',
         f'<path fill="url(#f)" fill-opacity=".55" d="{w2a}"><animate attributeName="d" dur="7s" repeatCount="indefinite" values="{w2a};{w2b};{w2a}"/></path>']
    return svg(W, H, "".join(b), t)


CARDS = dict(hero=hero, status=status, impact=impact, canary=canary, pipeline=pipeline,
             observability=observability, terminal=terminal, divider=divider, footer=footer)

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, fn in CARDS.items():
        for theme, t in THEMES.items():
            (OUT / f"{name}-{theme}.svg").write_text(fn(t), encoding="utf-8")
    print(f"wrote {len(CARDS) * len(THEMES)} files to {OUT}")
