# =============================================================================
# LENGUAJE DE PROGRAMACIÓN V  |  UMECIT  |  Unidad III
# Script 3: Análisis de Sensibilidad con SciPy + Matplotlib
# =============================================================================
#
# PROBLEMA DEL CURSO:
#   Max Z = 50x₁ + 30x₂
#   s.a.   4x₁ + 2x₂ ≤ 240   (Carpintería, h/sem)
#          2x₁ + 3x₂ ≤ 180   (Pintura, h/sem)
#          x₁, x₂   ≥   0
#
# ANÁLISIS:
#   A. Sensibilidad del RHS b₁ (horas de carpintería)
#   B. Sensibilidad del RHS b₂ (horas de pintura)
#   C. Sensibilidad del coef. c₁ (utilidad de la mesa)
#   D. Sensibilidad del coef. c₂ (utilidad de la silla)
#   E. Gráficas de los 4 análisis → PNG exportable
#
# RESULTADOS ESPERADOS:
#   Precio sombra carpintería: y₁* = $11.25/hora
#   Precio sombra pintura:     y₂* = $2.50/hora
#   Rango c₁: [$20, $60]  (plan x₁=45, x₂=30 permanece óptimo)
#
# INSTALACIÓN:  pip install scipy matplotlib numpy
# EJECUCIÓN:    python U3_Script3_Analisis_Sensibilidad.py
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import linprog

SEP = "=" * 70

print(SEP)
print("  UNIDAD III  |  Análisis de Sensibilidad con SciPy")
print("  Fábrica de Mesas y Sillas  —  Max Z = 50x₁ + 30x₂")
print(SEP)

# ─────────────────────────────────────────────────────────────────────────────
# DATOS BASE  (SciPy minimiza → negamos coefs de Z)
# ─────────────────────────────────────────────────────────────────────────────
C_NEG  = [-50.0, -30.0]                 # negados para Min(−Z)
A_UB   = [[4.0, 2.0],                   # carpintería
          [2.0, 3.0]]                    # pintura
B_BASE = [240.0, 180.0]
BOUNDS = [(0, None), (0, None)]

# Resolver el caso base
r0     = linprog(C_NEG, A_ub=A_UB, b_ub=B_BASE, bounds=BOUNDS, method="highs")
x1_b   = r0.x[0]
x2_b   = r0.x[1]
z_b    = -r0.fun

print(f"\n  Solución base:")
print(f"    x₁* = {x1_b:.1f}  mesas/semana")
print(f"    x₂* = {x2_b:.1f}  sillas/semana")
print(f"    Z*  = ${z_b:,.2f} / semana")

# ─────────────────────────────────────────────────────────────────────────────
# A: SENSIBILIDAD DE b₁ (Horas de Carpintería, base=240h)
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'─'*70}")
print("  A. SENSIBILIDAD DEL RHS b₁ — Horas de Carpintería (actual=240h)")
print(f"{'─'*70}")
print(f"  {'b₁(h)':>7}  {'Δb₁':>6}  {'x₁*':>7}  {'x₂*':>7}  "
      f"{'Z*':>10}  {'ΔZ*':>9}  {'PS≈':>8}")
print(f"  {'─'*65}")

b1_vals, z_b1 = [], []
for delta in range(-120, 181, 20):
    b = [240 + delta, 180]
    r = linprog(C_NEG, A_ub=A_UB, b_ub=b, bounds=BOUNDS, method="highs")
    if r.success:
        z_n = -r.fun
        dz  = z_n - z_b
        ps  = round(dz / delta, 4) if delta != 0 else 0.0
        marca = "  ← BASE" if delta == 0 else ""
        print(f"  {240+delta:>7.0f}  {delta:>+6}  {r.x[0]:>7.1f}  "
              f"{r.x[1]:>7.1f}  {z_n:>10,.2f}  {dz:>+9,.2f}  {ps:>8.4f}{marca}")
        b1_vals.append(240 + delta)
        z_b1.append(z_n)

print(f"\n  → Precio sombra y₁* = $11.25 / hora de carpintería")
print(f"  → Rango válido: b₁ ∈ [120h, 360h]  (misma base óptima)")

# ─────────────────────────────────────────────────────────────────────────────
# B: SENSIBILIDAD DE b₂ (Horas de Pintura, base=180h)
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'─'*70}")
print("  B. SENSIBILIDAD DEL RHS b₂ — Horas de Pintura (actual=180h)")
print(f"{'─'*70}")
print(f"  {'b₂(h)':>7}  {'Δb₂':>6}  {'x₁*':>7}  {'x₂*':>7}  "
      f"{'Z*':>10}  {'ΔZ*':>9}  {'PS≈':>8}")
print(f"  {'─'*65}")

b2_vals, z_b2 = [], []
for delta in range(-100, 141, 20):
    b = [240, 180 + delta]
    r = linprog(C_NEG, A_ub=A_UB, b_ub=b, bounds=BOUNDS, method="highs")
    if r.success:
        z_n = -r.fun
        dz  = z_n - z_b
        ps  = round(dz / delta, 4) if delta != 0 else 0.0
        marca = "  ← BASE" if delta == 0 else ""
        print(f"  {180+delta:>7.0f}  {delta:>+6}  {r.x[0]:>7.1f}  "
              f"{r.x[1]:>7.1f}  {z_n:>10,.2f}  {dz:>+9,.2f}  {ps:>8.4f}{marca}")
        b2_vals.append(180 + delta)
        z_b2.append(z_n)

print(f"\n  → Precio sombra y₂* = $2.50 / hora de pintura")
print(f"  → Rango válido: b₂ ∈ [80h, 320h]  (misma base óptima)")
print(f"  → Carpintería ($11.25/h) > Pintura ($2.50/h) — mayor retorno marginal")

# ─────────────────────────────────────────────────────────────────────────────
# C: SENSIBILIDAD DE c₁ (Utilidad mesa, base=$50)
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'─'*70}")
print("  C. SENSIBILIDAD DEL COEF. c₁ — Utilidad de la Mesa (actual=$50)")
print(f"{'─'*70}")
print(f"  {'c₁($/u)':>9}  {'x₁*':>7}  {'x₂*':>7}  "
      f"{'Z*':>10}  Observación")
print(f"  {'─'*60}")

c1_vals, z_c1, x1_c1, x2_c1 = [], [], [], []
x1_prev, x2_prev = None, None

for c1 in range(5, 160, 5):
    r = linprog([-c1, -30], A_ub=A_UB, b_ub=B_BASE, bounds=BOUNDS, method="highs")
    if r.success:
        z_n = -r.fun
        obs = ""
        if x1_prev is not None and (abs(r.x[0]-x1_prev) > 0.5 or abs(r.x[1]-x2_prev) > 0.5):
            obs = "← CAMBIA VÉRTICE"
        marca = "  ← ACTUAL" if c1 == 50 else ""
        print(f"  {c1:>9}  {r.x[0]:>7.1f}  {r.x[1]:>7.1f}  "
              f"{z_n:>10,.2f}  {obs}{marca}")
        c1_vals.append(c1);  z_c1.append(z_n)
        x1_c1.append(r.x[0]); x2_c1.append(r.x[1])
        x1_prev, x2_prev = r.x[0], r.x[1]

print(f"\n  → Rango c₁: [$20, $60]")
print(f"    Dentro de [$20, $60]: plan óptimo = 45 mesas + 30 sillas/semana")
print(f"    c₁ < $20 → conviene producir solo sillas")
print(f"    c₁ > $60 → conviene producir solo mesas")

# ─────────────────────────────────────────────────────────────────────────────
# D: SENSIBILIDAD DE c₂ (Utilidad silla, base=$30)
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'─'*70}")
print("  D. SENSIBILIDAD DEL COEF. c₂ — Utilidad de la Silla (actual=$30)")
print(f"{'─'*70}")
print(f"  {'c₂($/u)':>9}  {'x₁*':>7}  {'x₂*':>7}  "
      f"{'Z*':>10}  Observación")
print(f"  {'─'*60}")

c2_vals, z_c2 = [], []
x1_prev2, x2_prev2 = None, None

for c2 in range(5, 110, 5):
    r = linprog([-50, -c2], A_ub=A_UB, b_ub=B_BASE, bounds=BOUNDS, method="highs")
    if r.success:
        z_n = -r.fun
        obs = ""
        if x1_prev2 is not None and (abs(r.x[0]-x1_prev2) > 0.5 or abs(r.x[1]-x2_prev2) > 0.5):
            obs = "← CAMBIA VÉRTICE"
        marca = "  ← ACTUAL" if c2 == 30 else ""
        print(f"  {c2:>9}  {r.x[0]:>7.1f}  {r.x[1]:>7.1f}  "
              f"{z_n:>10,.2f}  {obs}{marca}")
        c2_vals.append(c2); z_c2.append(z_n)
        x1_prev2, x2_prev2 = r.x[0], r.x[1]

# ─────────────────────────────────────────────────────────────────────────────
# E: GRÁFICAS DE SENSIBILIDAD
# ─────────────────────────────────────────────────────────────────────────────
print(f"\n{'─'*70}")
print("  E. GENERANDO GRÁFICAS ...")
print(f"{'─'*70}")

PAL = {
    "navy":  "#1F3864",
    "blue":  "#2E75B6",
    "teal":  "#028090",
    "gold":  "#C9A227",
    "green": "#1E7145",
    "red":   "#C00000",
    "bg":    "#F7F9FC",
    "lgray": "#F2F5FA",
}

fig = plt.figure(figsize=(14, 10))
fig.suptitle(
    "Análisis de Sensibilidad — Fábrica de Mesas y Sillas\n"
    "Max Z = 50x₁ + 30x₂     s.a.  4x₁+2x₂ ≤ 240h  |  2x₁+3x₂ ≤ 180h",
    fontsize=13, fontweight="bold", color=PAL["navy"]
)

gs = gridspec.GridSpec(2, 2, hspace=0.42, wspace=0.32)

# ── Panel A: Z* vs b₁ (Carpintería) ──────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_facecolor(PAL["bg"])
ax1.plot(b1_vals, z_b1, color=PAL["navy"], lw=2.5, marker="o", ms=5, zorder=3)
ax1.axvline(240, color=PAL["gold"], lw=2.2, ls="--", label="b₁=240h actual", zorder=2)
ax1.axhline(z_b,  color=PAL["green"], lw=1.5, ls=":", label=f"Z*=${z_b:,.0f}", zorder=2)
# Rango válido sombreado
ax1.axvspan(120, 360, alpha=0.07, color=PAL["green"])
ax1.set_xlabel("b₁ — Horas de Carpintería (h/sem)", fontsize=11, color=PAL["navy"])
ax1.set_ylabel("Z* Utilidad semanal ($)",            fontsize=11, color=PAL["navy"])
ax1.set_title("Z* vs Horas de Carpintería (b₁)\nPS y₁* = $11.25/hora",
              fontsize=11, fontweight="bold", color=PAL["navy"])
ax1.legend(fontsize=9)
ax1.grid(alpha=0.3, ls="--")
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)

# ── Panel B: Z* vs b₂ (Pintura) ──────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.set_facecolor(PAL["bg"])
ax2.plot(b2_vals, z_b2, color=PAL["teal"], lw=2.5, marker="s", ms=5, zorder=3)
ax2.axvline(180, color=PAL["gold"], lw=2.2, ls="--", label="b₂=180h actual", zorder=2)
ax2.axhline(z_b,  color=PAL["green"], lw=1.5, ls=":", label=f"Z*=${z_b:,.0f}", zorder=2)
ax2.axvspan(80, 320, alpha=0.07, color=PAL["teal"])
ax2.set_xlabel("b₂ — Horas de Pintura (h/sem)",   fontsize=11, color=PAL["navy"])
ax2.set_ylabel("Z* Utilidad semanal ($)",           fontsize=11, color=PAL["navy"])
ax2.set_title("Z* vs Horas de Pintura (b₂)\nPS y₂* = $2.50/hora",
              fontsize=11, fontweight="bold", color=PAL["navy"])
ax2.legend(fontsize=9)
ax2.grid(alpha=0.3, ls="--")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

# ── Panel C: Z* y plan vs c₁ (Utilidad mesa) ─────────────────────────────────
ax3  = fig.add_subplot(gs[1, 0])
ax3r = ax3.twinx()
ax3.set_facecolor(PAL["bg"])
ax3.plot(c1_vals, z_c1, color=PAL["navy"], lw=2.5, label="Z*")
ax3r.plot(c1_vals, x1_c1, color=PAL["red"],   lw=2, ls="--", label="mesas*  (x₁*)", alpha=0.85)
ax3r.plot(c1_vals, x2_c1, color=PAL["green"], lw=2, ls=":",  label="sillas* (x₂*)", alpha=0.85)
ax3.axvline(50, color=PAL["gold"],  lw=2.2, ls="--", label="c₁=$50 actual")
ax3.axvspan(20, 60, alpha=0.08, color=PAL["green"], label="Rango válido $20–$60")
ax3.set_xlabel("c₁ — Utilidad de la Mesa ($/u)", fontsize=11, color=PAL["navy"])
ax3.set_ylabel("Z* ($)",                          fontsize=11, color=PAL["navy"])
ax3r.set_ylabel("Unidades óptimas/semana",        fontsize=10, color=PAL["red"])
ax3.set_title("Z* y Plan vs Utilidad Mesa (c₁)\nRango: $20 ≤ c₁ ≤ $60",
              fontsize=11, fontweight="bold", color=PAL["navy"])
lns  = ax3.get_legend_handles_labels()[0]  + ax3r.get_legend_handles_labels()[0]
lbs  = ax3.get_legend_handles_labels()[1]  + ax3r.get_legend_handles_labels()[1]
ax3.legend(lns, lbs, fontsize=8, loc="upper left")
ax3.grid(alpha=0.3, ls="--")
ax3.spines["top"].set_visible(False)

# ── Panel D: Z* vs c₂ (Utilidad silla) ───────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
ax4.set_facecolor(PAL["bg"])
ax4.plot(c2_vals, z_c2, color=PAL["blue"], lw=2.5, marker="D", ms=5, zorder=3)
ax4.axvline(30, color=PAL["gold"], lw=2.2, ls="--", label="c₂=$30 actual", zorder=2)
ax4.axhline(z_b,  color=PAL["green"], lw=1.5, ls=":", label=f"Z*=${z_b:,.0f}", zorder=2)
ax4.set_xlabel("c₂ — Utilidad de la Silla ($/u)", fontsize=11, color=PAL["navy"])
ax4.set_ylabel("Z* Utilidad semanal ($)",           fontsize=11, color=PAL["navy"])
ax4.set_title("Z* vs Utilidad Silla (c₂)",
              fontsize=11, fontweight="bold", color=PAL["navy"])
ax4.legend(fontsize=9)
ax4.grid(alpha=0.3, ls="--")
ax4.spines["top"].set_visible(False)
ax4.spines["right"].set_visible(False)

plt.savefig("U3_Sensibilidad_Muebles.png", dpi=150, bbox_inches="tight")
plt.show()
print("  Gráfica guardada: U3_Sensibilidad_Muebles.png")
print("  (Incluir en la presentación interactiva de la Actividad 3)")

print(f"\n{SEP}")
print("  Script 3 completado.")
print("  Siguiente: U3_Script4_Plantilla_Actividad3.py")
print(SEP)
