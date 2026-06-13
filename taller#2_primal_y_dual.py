# =============================================================================
# LENGUAJE DE PROGRAMACIÓN V  |  UMECIT  |  Unidad II
# Script 2: PLANTILLA ACTIVIDAD N.° 2 — Mollejitas e Hígado pio pio (Costos Reales)
# Instrucciones:
#   1. Reemplaza los datos de TU PROBLEMA en la sección de configuración.
#   2. Ejecuta el script y verifica que Z* = W* (Dualidad Fuerte).
#   3. Interpreta los precios sombra en el contexto de tu problema real.
# Librería: PuLP
# =============================================================================

from pulp import *

# =============================================================================
# ╔═══════════════════════════════════════════════════════════╗
# ║         CONFIGURA TU PROBLEMA AQUÍ                        ║
# ╚═══════════════════════════════════════════════════════════╝
#
# CASO INCLUIDO: Emprendimiento de comida rápida "El Buen Sabor"
#   Vende Porciones de Mollejitas (x1) y Hígado (x2) a $0.79 c/u
#   Utilidad: $0.515/porción (Mollejitas), $0.575/porción (Hígado)
#   Recurso 1 — Presupuesto ($) : 0.275x1 + 0.215x2 <= 30.00
#   Recurso 2 — Aceite (ml)     : 100x1 + 200x2 <= 10000
#   Recurso 3 — D. Mollejitas   : x1 <= 45 porciones
#   Recurso 4 — D. Hígado       : x2 <= 60 porciones
# =============================================================================

# ── Nombre del problema ───────────────────────────────────────
NOMBRE_PRIMAL = "Maximizacion_Ganancias_mollejitas_e_higado"   
NOMBRE_DUAL   = "Minimizacion_Ganancias_mollejitas_e_higado"

# ── Coeficientes de la función objetivo (c) ───────────────────
C1 = 0.515   # Utilidad de mollejitas 
C2 = 0.575   # Utilidad de Hígado

# ── Coeficientes de la matriz A (restricciones) ──────────────
# Restricción 1:  A11*x1 + A12*x2 <= b1
A11, A12, b1 = 0.275, 0.215, 30.00
# Restricción 2:    A21*x1 + A22*x2 <= b2
A21, A22, b2 = 100, 200, 10000
# Restricción 3:   x1 <= b3
b3 = 45
# Restricción 4:   x2 <= b4
b4 = 60

# ── Nombres de los recursos (para el reporte) ────────────────
nombre_r1 = "Presupuesto Compra ($)"
nombre_r2 = "Aceite Vegetal (ml)"
nombre_r3 = "Límite Empaque Mollejitas"
nombre_r4 = "Límite Empaque Hígado"
nombre_x1 = "Porciones de Mollejitas"
nombre_x2 = "Porciones de Hígado"
# =============================================================================
# AUTOMATIZACIÓN DE PROCESAMIENTO MATEMÁTICO
# =============================================================================

print("=" * 65)
print(f"  ACTIVIDAD N.° 2  |  Problema: {NOMBRE_PRIMAL}")
print("=" * 65)

# ── PRIMAL ────────────────────────────────────────────────────
print("\n── PROBLEMA PRIMAL ──────────────────────────────────────")

primal = LpProblem(NOMBRE_PRIMAL, LpMaximize)
x1 = LpVariable("x1", lowBound=0, cat="Continuous")
x2 = LpVariable("x2", lowBound=0, cat="Continuous")

primal += C1*x1 + C2*x2, "FO_Primal"
primal += A11*x1 + A12*x2 <= b1, "R1"
primal += A21*x1 + A22*x2 <= b2, "R2"
primal +=     x1           <= b3, "R3"
primal +=           x2     <= b4, "R4"

primal.solve(PULP_CBC_CMD(msg=0))

print(f"  Estado   : {LpStatus[primal.status]}")
print(f"  {nombre_x1} (x1) = {x1.value():.4f}")
print(f"  {nombre_x2} (x2) = {x2.value():.4f}")
print(f"  Z* = $ {value(primal.objective):,.4f}")

# ── DUAL ──────────────────────────────────────────────────────
print("\n── PROBLEMA DUAL ────────────────────────────────────────")

dual = LpProblem(NOMBRE_DUAL, LpMinimize)
y1 = LpVariable("y1", lowBound=0)
y2 = LpVariable("y2", lowBound=0)
y3 = LpVariable("y3", lowBound=0)
y4 = LpVariable("y4", lowBound=0)

dual += b1*y1 + b2*y2 + b3*y3 + b4*y4, "FO_Dual"
dual += A11*y1 + A21*y2 + y3       >= C1, "D1_para_x1"
dual += A12*y1 + A22*y2       + y4 >= C2, "D2_para_x2"

dual.solve(PULP_CBC_CMD(msg=0))

print(f"  Estado   : {LpStatus[dual.status]}")
print(f"  y1 ({nombre_r1}) = {y1.value():.6f}")
print(f"  y2 ({nombre_r2}) = {y2.value():.6f}")
print(f"  y3 ({nombre_r3}) = {y3.value():.6f}")
print(f"  y4 ({nombre_r4}) = {y4.value():.6f}")
print(f"  W* = $ {value(dual.objective):,.4f}")

# ── VERIFICACIÓN DUALIDAD FUERTE ──────────────────────────────
print("\n── VERIFICACIÓN: TEOREMA DE DUALIDAD FUERTE ─────────────")
z_opt = value(primal.objective)
w_opt = value(dual.objective)
gap   = abs(z_opt - w_opt)
print(f"  Z* = {z_opt:,.6f}")
print(f"  W* = {w_opt:,.6f}")
print(f"  Gap = {gap:.8f}  {'✓ DUALIDAD FUERTE VERIFICADA' if gap<0.01 else '✗ ERROR'}")

# ── PRECIOS SOMBRA ────────────────────────────────────────────
print("\n── PRECIOS SOMBRA E INTERPRETACIÓN ECONÓMICA ───────────")
vars_dual   = [y1, y2, y3, y4]
nombres_rec = [nombre_r1, nombre_r2, nombre_r3, nombre_r4]
limites_rec = [b1, b2, b3, b4]

for i, (yvar, nombre, limite) in enumerate(zip(vars_dual, nombres_rec, limites_rec)):
    val    = yvar.value()
    estado = "★ ACTIVA  → mejora Z*" if val > 0.001 else "  holgada → sin efecto"
    print(f"  y{i+1}* = {val:.4f}  |  {nombre:<20s}  |  {estado}")
    if val > 0.001:
        print(f"         → Incrementar {nombre} en 1 unidad aumenta Z* en ${val:.4f}")

# ── HOLGURA COMPLEMENTARIA ────────────────────────────────────
print("\n── HOLGURA COMPLEMENTARIA ───────────────────────────────")
usos    = [A11*x1.value()+A12*x2.value(), A21*x1.value()+A22*x2.value(), x1.value(), x2.value()]
for i, (yvar, uso, limite) in enumerate(zip(vars_dual, usos, limites_rec)):
    holgura  = limite - uso
    producto = yvar.value() * holgura
    ok = "✓" if abs(producto) < 0.001 else "✗"
    print(f"  R{i+1}: holgura={holgura:.4f}  y*={yvar.value():.4f}  y*(b-Ax)={producto:.6f}  {ok}")

print("\n" + "=" * 65)
print("=" * 65)
