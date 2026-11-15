# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown"]
# ///
"""Build README.md (with live shieldcn URLs) and a local light/dark preview.html.

Run: uv run scripts/build_readme.py && uv run scripts/vendor_images.py
"""

import re
from pathlib import Path
from urllib.parse import quote, urlencode

import markdown

ROOT = Path(__file__).parent.parent
RAW = "https://raw.githubusercontent.com/skafai/skafai/main/assets"
SC = "https://shieldcn.dev"

HEADER = {
    "title": "Wadie Skaf",
    "subtitle": "AI Research Scientist · Developer · Passionate Technologist",
    "align": "center",
    "font": "serif",
    "width": 1280,
    "height": 400,
    "overlay": 0,
    "border": "false",
}
HEADER_MODES = {
    "dark": {"bg": "000000", "titleColor": "ffffff", "subtitleColor": "6cb8e6"},
    "light": {"bg": "f7f7f5", "titleColor": "0a0a0a", "subtitleColor": "1f6f9f"},
}

LINKS = [
    ("skaf.ai", "lu:Globe", "https://skaf.ai", "Website"),
    ("Google Scholar", "googlescholar",
     "https://scholar.google.com/citations?user=odODvZgAAAAJ", "Google Scholar"),
    ("ORCID", "orcid", "https://orcid.org/0000-0002-4298-6694", "ORCID"),
    ("LinkedIn", "lu:Linkedin", "https://linkedin.com/in/skafai", "LinkedIn"),
    ("Email", "lu:Mail", "mailto:hello@skaf.ai", "Email"),
]
SKILL_ROWS = [
    ("Core", [
        ("Machine Learning", "lu:Brain"), ("Deep Learning", "lu:Network"),
        ("Statistics", "lu:ChartLine"), ("Mathematics", "lu:Sigma"),
        ("Scientific Computing", "lu:Cpu"), ("Software Engineering", "lu:Code"),
        ("Cloud Engineering", "lu:Cloud"),
    ]),
    ("Languages", [
        ("Python", "python"), ("C++", "cplusplus"), ("Rust", "rust"),
        ("JavaScript", "javascript"), ("TypeScript", "typescript"), ("SQL", "lu:Database"),
        ("Bash", "gnubash"),
    ]),
    ("ML & DL", [
        ("PyTorch", "pytorch"), ("Lightning", "lightning"), ("TensorFlow", "tensorflow"),
        ("Keras", "keras"), ("scikit-learn", "scikitlearn"),
    ]),
    ("Data", [
        ("Pandas", "pandas"), ("NumPy", "numpy"), ("Apache Spark", "apachespark"),
        ("Apache Airflow", "apacheairflow"),
    ]),
    ("MLOps & infra", [
        ("MLflow", "mlflow"), ("Docker", "docker"), ("Linux", "linux"), ("Slurm", "lu:Server"),
        ("AWS", "lu:Cloud"), ("Git", "git"),
    ]),
    ("Web", [
        ("React", "react"), ("Next.js", "nextdotjs"), ("Django", "django"),
        ("Tailwind CSS", "tailwindcss"),
    ]),
]
SPOKEN = "English (full) · German (professional, B2–C1) · Hungarian (elementary)"


def header_url(mode: str, image: str | None) -> str:
    params = {**HEADER, **HEADER_MODES[mode], "mode": mode}
    if image:
        params["image"] = image
    return f"{SC}/header/surface.svg?{urlencode(params)}"


def label_path(text: str) -> str:
    return quote(text.replace("-", "--").replace(" ", "_"))


def link_badge(label: str, logo: str, href: str, alt: str) -> str:
    src = f"{SC}/badge/{label_path(label)}-6cb8e6.svg?" + urlencode(
        {"logo": logo, "variant": "secondary", "font": "inter"})
    return f'<a href="{href}"><img alt="{alt}" src="{src}" /></a>'


def tool_badge(label: str, logo: str) -> str:
    def url(mode: str) -> str:
        return f"{SC}/badge/{label_path(label)}.svg?" + urlencode(
            {"logo": logo, "variant": "outline", "size": "xs", "font": "inter", "mode": mode})
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{url("dark")}" />'
            f'<img alt="{label}" src="{url("light")}" /></picture>')


def pub_links(doi: str, code: str | None = None) -> str:
    links = [("Paper", "lu:FileText", doi)] + ([("Code", "github", code)] if code else [])
    return " ".join(f'<a href="{href}">{tool_badge(label, logo)}</a>' for label, logo, href in links)


def expand_pubs(text: str) -> str:
    return re.sub(r"\{pub:([^}|]+)(?:\|([^}]+))?\}", lambda m: pub_links(m[1], m[2]), text)


def picture(dark: str, light: str, alt: str, extra: str = "") -> str:
    return (f'<picture>\n    <source media="(prefers-color-scheme: dark)" srcset="{dark}" />\n'
            f'    <img alt="{alt}" src="{light}" {extra}/>\n  </picture>')


HEADER_ALT = "Wadie Skaf: AI Research Scientist, Developer, and Passionate Technologist"

BODY = """
I am an AI Research Scientist and PhD candidate in Computer Science at
RWTH Aachen University. I research uncertainty
quantification, conformal prediction, and self-supervised representation learning
for time series, building trustworthy, uncertainty-aware models that depend less
on labelled data and manual algorithm design.

---

## Research Focus

| Area | Topics |
| :--- | :--- |
| **Time series** | Self-supervised representation learning, anomaly detection, and forecasting |
| **AutoML** | Meta-learning, neural architecture and hyperparameter selection |
| **Uncertainty quantification** | Conformal prediction |

---

## Technical Skills

| Category | Skills |
| :--- | :--- |
{skill_rows}

---

## Projects

| Project | Role | What It Is |
| :--- | :--- | :--- |
| [**Chronocratic**](https://github.com/chronocratic) | Founder | Open-source infrastructure, datasets, and models for time series research |
| [**rewrite.rs**](https://rewrite.rs/) | Founder | Guide and AI skills for rewriting software in Rust |
| [**PCGA**](https://github.com/skafai/PCGA) | Author | Genetic algorithm for controlling label proportions across containers |

---

## Open Source Contributions

| Project | What It Is |
| :--- | :--- |
| [**Relflow**](https://github.com/relflow/relflow) | Open-source model factory that builds and adapts foundation models for typed, nested structured data |
| [**RATS**](https://github.com/HyperVectors/RATS) | High-performance time series augmentation library in Rust, with a Python wrapper (RATSpy) |

--- | :--- | :--- |
| [**Chronocratic**](https://github.com/chronocratic) | Founder | Open-source infrastructure, datasets, and models for time series research |
| [**rewrite.rs**](https://rewrite.rs/) | Founder | Guide and AI skills for rewriting software in Rust |
| [**Relflow**](https://github.com/relflow/relflow) | Contributor | Open-source model factory that builds and adapts foundation models for typed, nested structured data |
| [**RATS**](https://github.com/HyperVectors/RATS) | Contributor | High-performance time series augmentation library in Rust, with a Python wrapper (RATSpy) |
| [**PCGA**](https://github.com/skafai/PCGA) | Author | Genetic algorithm for controlling label proportions across containers |

---

## Main Publications

- **Skaf, W.**, Baratchi, M., & Hoos, H. (2025). Time Series Representations Classroom (TSRC):
  A teacher-student-based framework for interpretability-enhanced unsupervised time series
  representation learning. *Machine Learning*.<br />{pub:https://doi.org/10.1007/s10994-025-06895-x|https://github.com/ADA-research/TSRC}
- Moeini, E., Vox, C., Anastacio, M., **Skaf, W.**, Baratchi, M., & Hoos, H. H. (2026). Neural
  architecture and hyperparameter selection through meta-learning on time series. In
  *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI)*.<br />{pub:https://doi.org/10.1609/aaai.v40i29.39622}
- **Skaf, W.**, & Horváth, T. (2022). Denoising architecture for unsupervised anomaly detection
  in time-series. In *Proceedings of the European Conference on Advances in Databases and
  Information Systems (ADBIS)*.<br />{pub:https://doi.org/10.1007/978-3-031-15743-1_17|https://github.com/skafai/denoising_architecture_time_series_paper}

---

## Education

| Degree | Institution | Notes |
| :--- | :--- | :--- |
| Dr. rer. nat. (PhD), Computer Science (AI) <picture><source media="(prefers-color-scheme: dark)" srcset="assets/ongoing-dark.svg" /><img alt="ongoing" src="assets/ongoing-light.svg" align="absmiddle" /></picture> | RWTH Aachen University | AutoML, uncertainty quantification, time series, and representation learning |
| M.Sc., Computer Science (AI) | Eötvös Loránd University | Machine learning, deep learning, anomaly detection, and audio signals |
| B.Sc., Informatics (Software Engineering) | Latakia University | Software engineering, information systems, databases, and mobile apps |

---

## Open to Work

I am available for freelance and consulting projects across my skill set, including but not
limited to:

- Machine learning research and development
- Time series analysis and forecasting
- Uncertainty quantification
- MLOps and AI systems engineering
- Software and web development

Reach out on LinkedIn or by email.

---

## Links

<p>
{links}
</p>
"""


def build_readme() -> str:
    header = picture(header_url("dark", f"{RAW}/header-bg-dark.png"),
                     header_url("light", f"{RAW}/header-bg-light.png"), HEADER_ALT,
                     'width="100%" ')
    links = "\n  ".join(link_badge(*l) for l in LINKS)
    skill_rows = "\n".join(
        f"| **{name}** | " + " ".join(tool_badge(*t) for t in items) + " |"
        for name, items in SKILL_ROWS)
    return (f'<p align="center">\n  {header}\n</p>\n'
            + expand_pubs(BODY).replace("{skill_rows}", skill_rows)
            .replace("{links}", "  " + links))


def preview_pane(readme: str, mode: str) -> str:
    # Pick the source for this mode, and fake the header image with a local background,
    # because shieldcn can only fetch the background once it is pushed.
    html = re.sub(
        r'<picture>\s*<source media="\(prefers-color-scheme: dark\)" srcset="([^"]+)" />\s*'
        r'<img alt="([^"]*)" src="([^"]+)" ([^>]*)/>\s*</picture>',
        lambda m: f'<img alt="{m[2]}" src="{m[1] if mode == "dark" else m[3]}" {m[4]}/>',
        readme)
    first = re.search(r'<img alt="Wadie Skaf[^"]*" src="([^"]+)"', html)
    overlay = re.sub(r"(&|\?)image=[^&\"]+", "", first[1]).replace(
        f"bg={HEADER_MODES[mode]['bg']}", "bg=transparent")
    html = html.replace(
        first[0],
        f'<div class="hdr" style="background-image:url(assets/header-bg-{mode}.png)">'
        f'<img alt="{HEADER_ALT}" src="{overlay}"',
        1).replace('width="100%" />\n</p>', 'width="100%" /></div>\n</p>', 1)
    body = markdown.markdown(html, extensions=["tables"])
    return f'<section class="pane {mode}"><h6>{mode} mode</h6><article>{body}</article></section>'


CSS = """
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
background:#888;display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:16px}
@media(max-width:1100px){body{grid-template-columns:1fr}}
.pane{border-radius:8px;padding:24px 32px}
.pane h6{margin:0 0 12px;font-size:12px;letter-spacing:.08em;text-transform:uppercase;opacity:.6}
.dark{background:#0d1117;color:#f0f6fc}.light{background:#fff;color:#1f2328}
article{max-width:880px;margin:auto;line-height:1.5;font-size:15px}
article h2{border-bottom:1px solid #3d444d55;padding-bottom:.3em;font-size:1.5em}
article hr{border:0;height:2px;background:#3d444d55}
article table{border-collapse:collapse;width:100%}article td,article th{border:1px solid #3d444d55;padding:6px 13px}
.dark a{color:#4493f8}.light a{color:#0969da}
.hdr{background-size:cover;border-radius:12px;line-height:0}.hdr img{display:block}
p[align=center]{text-align:center}img{max-width:100%}
"""

if __name__ == "__main__":
    readme = build_readme()
    (ROOT / "README.md").write_text(readme)
    page = (f"<!doctype html><meta charset=utf-8><title>Profile preview</title><style>{CSS}</style>"
            + preview_pane(readme, "dark") + preview_pane(readme, "light"))
    (ROOT / "preview.html").write_text(page)
    print("ok")
