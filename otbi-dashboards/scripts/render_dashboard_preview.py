"""Draw preview images of the two OTBI dashboard pages using made-up data.
Run:  python render_dashboard_preview.py
"""
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter, MaxNLocator

random.seed(7)
OUT = os.path.join(os.path.dirname(__file__), "..", "screenshots")
os.makedirs(OUT, exist_ok=True)

SURFACE, CANVAS = "#fcfcfb", "#f3f2ee"
INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#8a8984", "#e4e3de"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
GOOD, WARN = "#0b7a3e", "#b26b00"
HEADER = "#312d2a"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "text.color": INK,
                     "axes.edgecolor": GRID, "xtick.color": INK2, "ytick.color": INK2})
money = lambda v: f"${v/1e6:.2f}M" if abs(v) >= 1e6 else f"${v/1e3:,.1f}K"
axfmt = FuncFormatter(lambda v, _: f"${v/1e6:.1f}M" if abs(v) >= 1e6 else f"${v/1e3:.0f}K")


def panel(fig, x, y, w, h, title=None):
    fig.patches.append(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.004",
                                      transform=fig.transFigure, facecolor=SURFACE,
                                      edgecolor=GRID, linewidth=0.8, zorder=-5))
    if title:
        fig.text(x + 0.012, y + h - 0.033, title, fontsize=10.5, fontweight="bold")


def frame(title, prompts):
    fig = plt.figure(figsize=(16, 9), dpi=110, facecolor=CANVAS)
    fig.patches.append(plt.Rectangle((0, 0.935), 1, 0.065, transform=fig.transFigure,
                                     facecolor=HEADER, zorder=-5))
    fig.text(0.015, 0.967, "Finance Close Dashboard", fontsize=11, color="#cfc9c2", va="center")
    fig.text(0.16, 0.967, "›  " + title, fontsize=15, fontweight="bold", color="white", va="center")
    fig.text(0.985, 0.967, "OTBI · sample data", fontsize=9.5, color="#cfc9c2", va="center", ha="right")
    for i, (k, v) in enumerate(prompts):
        x = 0.015 + i * 0.13
        panel(fig, x, 0.87, 0.12, 0.05)
        fig.text(x + 0.008, 0.902, k, fontsize=8, color=MUTED)
        fig.text(x + 0.008, 0.879, v + "  ▾", fontsize=9.5)
    panel(fig, 0.015 + len(prompts) * 0.13, 0.87, 0.06, 0.05)
    fig.text(0.045 + len(prompts) * 0.13, 0.889, "Apply", fontsize=9.5, ha="center",
             color=BLUE, fontweight="bold")
    return fig


def style(ax, xgrid=False):
    ax.set_facecolor(SURFACE)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.grid(axis="x" if xgrid else "y", color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    (ax.xaxis if xgrid else ax.yaxis).set_major_locator(MaxNLocator(4))


def tiles(fig, items):
    w = 0.235
    for i, (label, value, note, color) in enumerate(items):
        x = 0.015 + i * (w + 0.0083)
        panel(fig, x, 0.735, w, 0.12)
        fig.text(x + 0.012, 0.823, label, fontsize=9.5, color=INK2)
        fig.text(x + 0.012, 0.77, value, fontsize=22, fontweight="bold")
        fig.text(x + 0.012, 0.746, note, fontsize=8.5, color=color)


# ---------- Page 1: GL vs Cost Accounting reconciliation ----------
periods = ["Jan-26", "Feb-26", "Mar-26", "Apr-26", "May-26", "Jun-26", "Jul-26", "Aug-26"]
gl = [random.uniform(380e3, 620e3) for _ in periods]
diff = [0, 0, 1.42, 0, 3.07, 0, 2.18, 2.44]
sl = [g - d for g, d in zip(gl, diff)]
fig = frame("GL to Cost Accounting", [("Ledger", "Primary Ledger"), ("Account", "Clearing account"),
                                       ("Periods", "Jan-26 … Aug-26")])
tiles(fig, [
    ("GL balance (Cost Management source)", money(sum(gl)), "Posted journals, adjusting periods excluded", INK2),
    ("Cost Accounting distributions", money(sum(sl)), "GL Transfer Status = Yes", INK2),
    ("Difference", f"${sum(diff):,.2f}", "✓ Within tolerance (under $25)", GOOD),
    ("Batches with a difference", "4 of 186", "! Split / partial line amounts", WARN),
])
panel(fig, 0.015, 0.39, 0.97, 0.33, "GL vs Cost Accounting by period")
ax = fig.add_axes([0.055, 0.425, 0.91, 0.24])
xs = range(len(periods))
ax.bar([x - 0.2 for x in xs], gl, width=0.38, color=BLUE, label="General Ledger")
ax.bar([x + 0.2 for x in xs], sl, width=0.38, color=ORANGE, label="Cost Accounting")
ax.set_xticks(list(xs))
ax.set_xticklabels(periods)
ax.yaxis.set_major_formatter(axfmt)
ax.legend(frameon=False, loc="lower right", bbox_to_anchor=(1, 1.02), ncol=2)
style(ax)

panel(fig, 0.015, 0.03, 0.97, 0.345, "Batches that do not tie (drill from the chart)")
cols = ["Period", "GL batch", "GL amount", "Cost Accounting amount", "Difference", "Reason"]
xpos = [0.03, 0.12, 0.36, 0.5, 0.67, 0.77]
y0 = 0.305
for x, c in zip(xpos, cols):
    fig.text(x, y0, c, fontsize=9, fontweight="bold", color=INK2)
fig.lines.append(plt.Line2D([0.025, 0.975], [y0 - 0.012, y0 - 0.012], transform=fig.transFigure,
                            color=GRID, linewidth=1))
rows = [("Mar-26", "Cost Management A 104512", 18240.55, 1.42, "Partial receipt line"),
        ("May-26", "Cost Management A 108733", 9411.10, 3.07, "Split distribution"),
        ("Jul-26", "Cost Management A 112090", 22713.86, 2.18, "Partial receipt line"),
        ("Aug-26", "Cost Management A 113561", 5077.40, 2.44, "Rounding on split line")]
for i, (p, b, a, d, r) in enumerate(rows):
    y = y0 - 0.04 - i * 0.034
    for x, v in zip(xpos, [p, b, f"${a:,.2f}", f"${a-d:,.2f}", f"${d:,.2f}", r]):
        fig.text(x, y, v, fontsize=9)
fig.text(0.03, 0.06, "Fixed in this report: adjusting-period duplicates, late-transferred batches, "
         "date cut-off at period end, and PO line duplicates from the receipt folder.",
         fontsize=8.5, color=INK2)
fig.savefig(os.path.join(OUT, "page1_gl_reconciliation.png"), facecolor=CANVAS)
plt.close(fig)

# ---------- Page 2: AP aging and journal sources ----------
fig = frame("Payables Aging", [("Business unit", "All"), ("Supplier", "All"), ("As of", "Today")])
buckets = ["Current", "1-30 days", "31-60 days", "61-90 days", "Over 90 days"]
amounts = [4.62e6, 1.18e6, 0.41e6, 0.17e6, 0.23e6]
total = sum(amounts)
tiles(fig, [
    ("Total open payables", money(total), "Unpaid installments, cancelled invoices excluded", INK2),
    ("Past due", money(total - amounts[0]), f"{(total-amounts[0])/total:.1%} of open balance", INK2),
    ("Over 90 days", money(amounts[-1]), "! Review with AP team", WARN),
    ("Open invoices", "1,284", "Across 312 suppliers", INK2),
])
panel(fig, 0.015, 0.03, 0.48, 0.69, "Open balance by aging bucket")
ax = fig.add_axes([0.11, 0.08, 0.36, 0.55])
ax.barh(buckets[::-1], amounts[::-1], color=BLUE, height=0.55)
for i, v in enumerate(amounts[::-1]):
    ax.text(v + max(amounts) * 0.01, i, f"{money(v)}  ({v/total:.0%})", va="center", fontsize=8.5, color=INK2)
ax.xaxis.set_major_formatter(axfmt)
ax.set_xlim(0, max(amounts) * 1.3)
style(ax, xgrid=True)

panel(fig, 0.505, 0.03, 0.48, 0.69, "Top suppliers past due")
cols = ["Supplier", "Past due", "Oldest (days)", "Invoices"]
xpos = [0.52, 0.72, 0.82, 0.92]
y0 = 0.655
for x, c in zip(xpos, cols):
    fig.text(x, y0, c, fontsize=9, fontweight="bold", color=INK2)
fig.lines.append(plt.Line2D([0.515, 0.975], [y0 - 0.012, y0 - 0.012], transform=fig.transFigure,
                            color=GRID, linewidth=1))
sup = sorted([(f"Supplier {chr(65+i)}", random.uniform(40e3, 260e3), random.randint(35, 240),
               random.randint(2, 30)) for i in range(12)], key=lambda r: -r[1])
for i, (n, a, o, c) in enumerate(sup):
    y = y0 - 0.045 - i * 0.045
    for x, v in zip(xpos, [n, money(a), str(o), str(c)]):
        fig.text(x, y, v, fontsize=9)
fig.savefig(os.path.join(OUT, "page2_payables_aging.png"), facecolor=CANVAS)
plt.close(fig)
print("saved", os.listdir(OUT))
