#!/usr/bin/env python3
"""Render the animated profile cards in ./assets, one dark and one light file each.

Run from the repo root:  python3 scripts/build_assets.py
Everything is plain SVG + CSS/SMIL, uses system fonts only, and honours
prefers-reduced-motion, so it renders the same through GitHub's image proxy.
"""
from pathlib import Path
from xml.sax.saxutils import escape

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


# ───────────────────────────── delivery pipeline ─────────────────────────────
def pipeline(t):
    W, H = 1200, 300
    stages = [("commit", "git push", t["muted"]), ("test", "pytest · SonarQube", t["blue"]),
              ("scan", "Trivy CVE gate", t["warn"]), ("build", "multi-stage image", t["blue"]),
              ("deploy", "Argo CD · canary", t["accent2"]), ("observe", "Prom · Loki · Tempo", t["accent"]),
              ("live", "promoted", t["ok"])]
    bw, gap, x0, y0, bh = 142, 26, 26, 92, 74
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" class="card"/>',
         f'<text x="28" y="40" class="mono mu" font-size="13">pipeline / <tspan class="tx">self-healing-delivery</tspan></text>',
         f'<text x="{W - 28}" y="40" text-anchor="end" class="mono mu" font-size="12">every commit: gated, scanned, canaried, watched</text>']
    cy = y0 + bh / 2
    main = f"M{x0},{cy} H{x0 + 7 * bw + 6 * gap}"
    b.append(f'<path d="{main}" stroke="{t["border"]}" stroke-width="2"/>')
    for i, (name, tool, col) in enumerate(stages):
        x = x0 + i * (bw + gap)
        b.append(f'<g class="rise" style="animation-delay:{.1 + i * .12:.2f}s">'
                 f'<rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="12" class="card2"/>'
                 f'<rect x="{x}" y="{y0}" width="4" height="{bh}" rx="2" fill="{col}"/>'
                 f'<text x="{x + bw / 2 + 2}" y="{y0 + 32}" text-anchor="middle" class="sans tx" font-size="16" font-weight="700">{name}</text>'
                 f'<text x="{x + bw / 2 + 2}" y="{y0 + 54}" text-anchor="middle" class="mono mu" font-size="10.5">{escape(tool)}</text></g>')
        if i < 6:
            ax = x + bw + gap / 2
            b.append(f'<path d="M{ax - 4},{cy - 5} l6,5 l-6,5" fill="none" stroke="{t["muted"]}" stroke-width="1.6"/>')
    for k in range(3):
        b.append(f'<circle r="5" class="ac"><animateMotion dur="6s" begin="{k * 2}s" repeatCount="indefinite" path="{main}"/>'
                 f'<animate attributeName="opacity" dur="6s" begin="{k * 2}s" repeatCount="indefinite" values="0;1;1;0" keyTimes="0;.05;.92;1"/></circle>')
    # rollback arc from observe back to deploy
    ox = x0 + 5 * (bw + gap) + bw / 2
    dx = x0 + 4 * (bw + gap) + bw / 2
    arc = f"M{ox},{y0 + bh} C{ox},{y0 + bh + 70} {dx},{y0 + bh + 70} {dx},{y0 + bh + 4}"
    b.append(f'<path d="{arc}" fill="none" stroke="{t["warn"]}" stroke-width="2" class="flow"/>')
    b.append(f'<path d="M{dx - 5},{y0 + bh + 12} l5,-8 l5,8" fill="none" stroke="{t["warn"]}" stroke-width="2"/>')
    b.append(f'<circle r="5" class="wn"><animateMotion dur="4s" repeatCount="indefinite" path="{arc}"/></circle>')
    b.append(f'<text x="{(ox + dx) / 2}" y="{y0 + bh + 82}" text-anchor="middle" class="mono wn" font-size="12">SLO breach → automatic rollback</text>')
    # gate legend
    lx = 28
    for lbl, col in [("security gates on every commit", t["warn"]), ("canary traffic shifting", t["accent2"]),
                     ("metrics · logs · traces", t["accent"])]:
        b.append(f'<circle cx="{lx + 5}" cy="{H - 30}" r="4" fill="{col}"/><text x="{lx + 16}" y="{H - 26}" class="mono mu" font-size="11.5">{lbl}</text>')
        lx += len(lbl) * 7.2 + 44
    return svg(W, H, "".join(b), t, label="Self-healing delivery pipeline: commit, test with SonarQube, Trivy scan, build, Argo CD canary deploy, observe with Prometheus, Loki and Tempo, then promote; an SLO breach triggers automatic rollback.")


# ───────────────────────────── observability architecture ─────────────────────────────
def observability(t):
    W, H = 1200, 430
    b = [f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" class="card"/>',
         f'<text x="28" y="40" class="mono mu" font-size="13">architecture / <tspan class="tx">hub-and-spoke-observability</tspan></text>']
    sig = [("metrics", t["accent"]), ("logs", t["warn"]), ("traces", t["accent2"])]
    # spokes
    spokes = ["prod", "staging", "dev"]
    hub_x, hub_y, hub_w, hub_h = 470, 80, 300, 270
    for i, s in enumerate(spokes):
        y = 80 + i * 96
        b.append(f'<rect x="28" y="{y}" width="250" height="78" rx="12" class="card2"/>')
        b.append(f'<text x="46" y="{y + 28}" class="sans tx" font-size="15" font-weight="700">AKS · {s}</text>')
        c, _ = chip(46, y + 40, "Grafana Alloy", t, t["accent"], 11)
        b.append(c)
        for k in range(3):
            b.append(f'<circle cx="{246 + k * 0}" cy="{y + 26 + k * 13}" r="3" fill="{sig[k][1]}"/>')
        path = f"M278,{y + 39} C370,{y + 39} 380,{hub_y + 135} {hub_x},{hub_y + 135}"
        b.append(f'<path d="{path}" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>')
        for k, (_, col) in enumerate(sig):
            b.append(f'<circle r="3.5" fill="{col}"><animateMotion dur="2.7s" begin="{i * .4 + k * .9:.1f}s" repeatCount="indefinite" path="{path}"/></circle>')
    # hub
    b.append(f'<rect x="{hub_x}" y="{hub_y}" width="{hub_w}" height="{hub_h}" rx="14" class="card2" stroke-dasharray="5 4"/>')
    b.append(f'<text x="{hub_x + hub_w / 2}" y="{hub_y + 28}" text-anchor="middle" class="mono mu" font-size="12">observability hub</text>')
    for k, (name, desc, col) in enumerate([("Mimir", "metrics · Prometheus API", t["accent"]),
                                           ("Loki", "logs", t["warn"]), ("Tempo", "traces", t["accent2"])]):
        y = hub_y + 46 + k * 70
        b.append(f'<rect x="{hub_x + 20}" y="{y}" width="{hub_w - 40}" height="56" rx="10" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-opacity=".5"/>')
        b.append(f'<text x="{hub_x + 40}" y="{y + 25}" class="sans" font-size="17" font-weight="700" fill="{col}">{name}</text>')
        b.append(f'<text x="{hub_x + 40}" y="{y + 44}" class="mono mu" font-size="11">{desc}</text>')
    # storage under hub
    sy = hub_y + hub_h + 22
    b.append(f'<path d="M{hub_x + hub_w / 2},{hub_y + hub_h} V{sy}" stroke="{t["blue"]}" stroke-width="1.5" class="flow"/>')
    b.append(f'<rect x="{hub_x + 40}" y="{sy}" width="{hub_w - 80}" height="40" rx="10" fill="{t["blue"]}" fill-opacity=".10" stroke="{t["blue"]}" stroke-opacity=".5"/>')
    b.append(f'<text x="{hub_x + hub_w / 2}" y="{sy + 25}" text-anchor="middle" class="mono bl" font-size="12.5">Azure Blob · long-term</text>')
    # right side: grafana + alerting
    gx = 880
    for k, (name, desc, col) in enumerate([("Grafana", "dashboards · SLOs", t["warn"]),
                                           ("Alerting", "routes · on-call", t["err"]),
                                           ("RCA", "timeline · fix · follow-up", t["ok"])]):
        y = 96 + k * 92
        b.append(f'<rect x="{gx}" y="{y}" width="292" height="70" rx="12" class="card2"/>')
        b.append(f'<rect x="{gx}" y="{y}" width="4" height="70" rx="2" fill="{col}"/>')
        b.append(f'<text x="{gx + 22}" y="{y + 30}" class="sans tx" font-size="16" font-weight="700">{name}</text>')
        b.append(f'<text x="{gx + 22}" y="{y + 50}" class="mono mu" font-size="11.5">{desc}</text>')
        if k:
            b.append(f'<path d="M{gx + 146},{y - 22} V{y}" stroke="{t["border"]}" stroke-width="1.5" class="flow"/>')
    path = f"M{hub_x + hub_w},{hub_y + 135} C{hub_x + hub_w + 50},{hub_y + 135} {gx - 50},{131} {gx},{131}"
    b.append(f'<path d="{path}" fill="none" stroke="{t["border"]}" stroke-width="1.5"/>')
    b.append(f'<circle r="4" class="ac"><animateMotion dur="1.8s" repeatCount="indefinite" path="{path}"/></circle>')
    # legend
    lx = 880
    for name, col in sig:
        b.append(f'<circle cx="{lx + 4}" cy="{H - 34}" r="4" fill="{col}"/><text x="{lx + 14}" y="{H - 30}" class="mono mu" font-size="11.5">{name}</text>')
        lx += len(name) * 7.2 + 34
    b.append(f'<text x="28" y="{H - 30}" class="mono mu" font-size="11.5">one agent per cluster · one place to look · cheap object storage</text>')
    return svg(W, H, "".join(b), t, label="Hub-and-spoke observability: Grafana Alloy agents on each AKS cluster ship metrics, logs and traces to a central Mimir, Loki and Tempo hub backed by Azure Blob storage, feeding Grafana dashboards, alerting and RCAs.")


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
