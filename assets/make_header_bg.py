# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Generate the profile header backgrounds: a time series whose forecast carries a
conformal prediction band, with the few points that leave the band marked in gold.

Run: uv run assets/make_header_bg.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

WIDTH, HEIGHT, DPI = 1280, 400, 100
SEED = 7
OUT_DIR = Path(__file__).parent

THEMES = {
    "dark": {
        "bg": "#000000",
        "line": "#6cb8e6",
        "band": "#6cb8e6",
        "band_alpha": 0.16,
        "miss": "#ffd700",
        "grid": "#ffffff",
        "grid_alpha": 0.05,
        "line_alpha": 0.5,
    },
    "light": {
        "bg": "#f7f7f5",
        "line": "#1f6f9f",
        "band": "#6cb8e6",
        "band_alpha": 0.28,
        "miss": "#b8860b",
        "grid": "#000000",
        "grid_alpha": 0.05,
        "line_alpha": 0.65,
    },
}


def make_signal(n: int) -> np.ndarray:
    t = np.linspace(0, 1, n)
    seasonal = 0.55 * np.sin(2 * np.pi * 5.5 * t) + 0.25 * np.sin(2 * np.pi * 13 * t + 1.1)
    trend = 0.35 * np.sin(2 * np.pi * 0.8 * t + 0.4)
    return seasonal + trend


def make_noise(rng: np.random.Generator, n: int, scale: float) -> np.ndarray:
    return np.convolve(rng.normal(0, scale, n), np.ones(3) / 3, mode="same")


def draw(theme: dict, path: Path, layout: str = "fade") -> None:
    rng = np.random.default_rng(SEED)
    n, split = 220, 176
    x = np.arange(n)
    signal = make_signal(n)
    y = signal + make_noise(rng, n, 0.3)
    y[[186, 199, 212]] += [0.85, -0.9, 0.75]  # a few observations leave the band
    forecast = signal
    width = 0.3 + 0.006 * np.clip(x - split, 0, None)
    lower, upper = forecast - width, forecast + width
    future = x >= split
    misses = future & ((y < lower) | (y > upper))

    fig = plt.figure(figsize=(WIDTH / DPI, HEIGHT / DPI), dpi=DPI)
    ax = fig.add_axes((0, 0, 1, 1))
    fig.patch.set_facecolor(theme["bg"])
    ax.set_facecolor(theme["bg"])

    for gx in np.linspace(0, n, 17):
        ax.axvline(gx, color=theme["grid"], alpha=theme["grid_alpha"], lw=0.8)
    for gy in np.linspace(-2.2, 2.2, 7):
        ax.axhline(gy, color=theme["grid"], alpha=theme["grid_alpha"], lw=0.8)

    ax.fill_between(x[future], lower[future], upper[future], color=theme["band"],
                    alpha=theme["band_alpha"], lw=0)
    ax.plot(x[future], forecast[future], color=theme["line"], alpha=theme["line_alpha"] * 0.8,
            lw=1.4, ls=(0, (4, 3)))
    ax.plot(x[: split + 1], y[: split + 1], color=theme["line"], alpha=theme["line_alpha"], lw=2)
    ax.plot(x[future], y[future], color=theme["line"], alpha=theme["line_alpha"] * 0.45, lw=1.2)
    ax.scatter(x[misses], y[misses], s=34, color=theme["miss"], alpha=0.95, zorder=6, lw=0)
    ax.scatter([split], [y[split]], s=60, color=theme["miss"], zorder=6, lw=0)
    ax.axvline(split, color=theme["line"], alpha=0.18, lw=1, ls=(0, (2, 3)))

    ax.set_xlim(0, n - 1)
    ax.set_ylim(-2.4, 2.4)
    if layout == "bottom":  # series lives in the lower third, the text above stays clear
        ax.set_ylim(-2.6, 9.0)
    elif layout == "right":  # series on the right half, left-aligned text on the left
        ax.set_xlim(-n * 0.95, n - 1)
    elif layout == "fade":  # series everywhere, faded out behind the centred text
        yy, xx = np.mgrid[-1:1:200j, -1:1:640j]
        mask = np.clip(1.1 - np.sqrt((xx / 0.5) ** 2 + (yy / 0.62) ** 2), 0, 1) ** 0.7
        rgba = np.zeros((*mask.shape, 4))
        rgba[..., :3] = matplotlib.colors.to_rgb(theme["bg"])
        rgba[..., 3] = np.clip(mask * 1.15, 0, 0.92)
        ax.imshow(rgba, extent=(*ax.get_xlim(), *ax.get_ylim()), aspect="auto", zorder=5)
    ax.axis("off")
    fig.savefig(path, dpi=DPI, facecolor=theme["bg"])
    plt.close(fig)


if __name__ == "__main__":
    import sys

    layouts = sys.argv[1:] or ["fade"]
    for layout in layouts:
        suffix = "" if len(layouts) == 1 else f"-{layout}"
        for name, theme in THEMES.items():
            draw(theme, OUT_DIR / f"header-bg{suffix}-{name}.png", layout)
