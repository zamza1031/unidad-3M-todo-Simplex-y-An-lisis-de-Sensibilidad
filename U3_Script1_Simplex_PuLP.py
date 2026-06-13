# =============================================================================
# LENGUAJE DE PROGRAMACIÓN V  |  UMECIT  |  Unidad III
# Script 1: Método Simplex con PuLP — Mollejitas e Hígado
# =============================================================================
#
# PROBLEMA ADAPTADO:
#   Max Z = $0.515·x₁ + $0.575·x₂
#   s.a.
#     0.275x₁ + 0.215x₂ ≤ 30      (Presupuesto en $)
#       100x₁ +   200x₂ ≤ 10000   (Aceite en ml)
#          x₁           ≤ 45      (Límite empaques Mollejitas)
#                    x₂ ≤ 60      (Límite empaques Hígado)
#     x₁, x₂   ≥  0
#
# SOLUCIÓN ESPERADA:
#   x₁* = 45.00 porciones de Mollejitas
#   x₂* = 27.50 porciones de Hígado
#   Z* = $38.99 / día
#
# INSTALACIÓN:  pip install pulp
# EJECUCIÓN:    python U3_Script1_Simplex_PuLP.py
# =============================================================================

from pulp import *

SEP  = "=" * 65
SEP2 = "─" * 65

print(SEP)
print("  UNIDAD III  |  Método Simplex con PuLP")
print("  Emprendimiento: El Buen Sabor (Mollejitas e Hígado)")
print(SEP)

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN A: DEFINICIÓN DEL MODELO
# ─────────────────────────────────────────────────────────────────────────────
print("\n── A. MODELO ────────────────────────────────────────────")

prob = LpProblem("Maximizacion_Ganancias", LpMaximize)

x1 = LpVariable("mollejitas", lowBound=0, cat="Continuous")
x2 = LpVariable("higado",     lowBound=0, cat="Continuous")

# Función objetivo
prob += 0.515*x1 + 0.575*x2,      "Z_Utilidad_Diaria"

# Restricciones nombradas (necesario para leer precios sombra)
prob += 0.275*x1 + 0.215*x2 <= 30.0,    "Presupuesto_USD"
prob += 100.0*x1 + 200.0*x2 <= 10000.0, "Aceite_ml"
prob += 1.0*x1 <= 45.0,                 "Lim_Mollejitas"
prob += 1.0*x2 <= 60.0,                 "Lim_Higado"

print("  Max Z  = 0.515·mollejitas + 0.575·hígado")
print("  s.a.     0.275·moll + 0.215·híg ≤ 30     (Presupuesto, $)")
print("           100·moll   + 200·híg   ≤ 10000 (Aceite, ml)")
print("           1·moll                 ≤ 45    (Límite Mollejitas, u)")
print("                        1·híg     ≤ 60    (Límite Hígado, u)")
print("           mollejitas, higado ≥ 0")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN B: RESOLUCIÓN
# ─────────────────────────────────────────────────────────────────────────────
print("\n── B. RESOLUCIÓN ────────────────────────────────────────")

prob.solve(PULP_CBC_CMD(msg=0))

print(f"  Estado   : {LpStatus[prob.status]}")
print(f"  Mollejitas : x₁* = {x1.value():.2f}  porciones/día")
print(f"  Hígado     : x₂* = {x2.value():.2f}  porciones/día")
print(f"  Utilidad   : Z* = $ {value(prob.objective):,.4f} / día")

# Verificar manualmente
z_check = 50 * x1.value() + 30 * x2.value()
print(f"\n  Verificación: 50×{x1.value():.0f} + 30×{x2.value():.0f} = ${z_check:,.2f}  "
      f"{'✓' if abs(z_check - value(prob.objective)) < 0.01 else '✗'}")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN C: PRECIOS SOMBRA (ANÁLISIS DUAL)
# ─────────────────────────────────────────────────────────────────────────────
print("\n── C. PRECIOS SOMBRA ────────────────────────────────────")
print(f"  {'Restricción':<16} {'Recurso usado':>14} {'Límite':>8} "
      f"{'Holgura':>10} {'PS (yᵢ*)':>12}  Estado")
print(f"  {SEP2}")

for nombre, restr in prob.constraints.items():
    limite  = -restr.constant
    uso     = limite + restr.value()
    holgura = limite - uso
    pi      = restr.pi if hasattr(restr, "pi") and restr.pi is not None else 0.0
    estado  = "★ ACTIVA" if abs(holgura) < 1e-6 else f"holgada  (slack={holgura:.1f})"
    print(f"  {nombre:<16} {uso:>14.2f} {limite:>8.0f} "
          f"{holgura:>10.2f} {pi:>12.4f}  {estado}")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN D: VERIFICACIÓN — HOLGURA COMPLEMENTARIA
# Condición de optimalidad: yᵢ* × (bᵢ − aᵢᵀx*) = 0  ∀ i
# ─────────────────────────────────────────────────────────────────────────────
print("\n── D. HOLGURA COMPLEMENTARIA ────────────────────────────")
print("  Condición: yᵢ* × slackᵢ = 0  (debe cumplirse en el óptimo)\n")

todos_ok = True
for nombre, restr in prob.constraints.items():
    limite  = -restr.constant
    uso     = limite + restr.value()
    holgura = limite - uso
    pi      = restr.pi if hasattr(restr, "pi") and restr.pi is not None else 0.0
    prod    = abs(pi * holgura)
    ok      = prod < 1e-5
    if not ok:
        todos_ok = False
    print(f"  {nombre}: y*={pi:.4f} × slack={holgura:.4f} = {prod:.2e}  "
          f"{'✓' if ok else '✗ ERROR'}")

print()
print(f"  {'✓  Holgura Complementaria VERIFICADA' if todos_ok else '✗  Revisar formulación'}")

# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN E: INTERPRETACIÓN ECONÓMICA
# ─────────────────────────────────────────────────────────────────────────────
print("\n── E. INTERPRETACIÓN ECONÓMICA ──────────────────────────")
print(f"  Plan de producción óptimo:")
print(f"    • Producir {x1.value():.0f} mesas/semana  →  ${50*x1.value():,.0f}")
print(f"    • Producir {x2.value():.0f} sillas/semana →  ${30*x2.value():,.0f}")
print(f"    • Utilidad total semanal: Z* = ${value(prob.objective):,.2f}")

print()
for nombre, restr in prob.constraints.items():
    limite  = -restr.constant
    uso     = limite + restr.value()
    holgura = limite - uso
    pi      = restr.pi if hasattr(restr, "pi") and restr.pi is not None else 0.0
    if abs(pi) > 1e-6:
        print(f"  ▶ {nombre} (capacidad actual: {limite:.0f} h/sem):")
        print(f"    Precio sombra = ${pi:.4f}/hora")
        print(f"    → Cada hora extra aumenta Z* en ${pi:.4f}")
        print(f"    → Conviene pagar hasta ${pi:.4f} extra por hora adicional")
    else:
        print(f"  ▷ {nombre}: precio sombra = $0  (holgura disponible: {holgura:.1f}h)")
    print()

print(SEP)
print("  Script 1 completado.")
print("  Siguiente: U3_Script2_Simplex_Tablas_Manuales.py")
print(SEP)
