# Empresa OS — las reglas

Los tres documentos que rigen **cómo se trabaja**, en cualquier sesión y cualquier
negocio. Valen para agentes de IA y para personas del equipo por igual.

| Archivo | Qué es | Cuándo se lee |
|---|---|---|
| `01-CONSTITUCION.md` | Lo no negociable: 23 reglas numeradas + la regla final. | **Siempre.** Se carga sola en cada sesión, importada desde `~/.claude/CLAUDE.md`. |
| `02-PLAYBOOK.md` | Cómo se ejecuta: pre-flight, delegación, checklist de cierre, qué hacer cuando algo se rompe. | Antes de cualquier trabajo no trivial. |
| `03-EMPRESA.md` | Qué se mide (KPIs con su fuente), los estándares y dónde se escribe cada cosa. | Cuando hay un número, un KPI, o duda de dónde guardar algo. |

## Cómo se relaciona con el resto

```
~/.claude/CLAUDE.md          quién es Facu, los negocios, el idioma   (global, siempre)
      └── importa →  os/01-CONSTITUCION.md   las reglas              (siempre)
                     os/02-PLAYBOOK.md       el método               (por referencia)
                     os/03-EMPRESA.md        KPIs y estándares       (por referencia)

~/facu-os/.claude/CLAUDE.md  la mecánica del repo: skills, agentes, stack, paths
```

**No se duplica nada entre ellos.** Si un dato aparece en dos archivos, uno ya está
mintiendo: se borra de uno y se deja el link.

## Cómo se cambian

1. Se edita el archivo y **se sube la versión** del tag de arriba (`CONSTITUCION-v1` → `v2`).
2. Se anota abajo qué cambió y por qué.
3. Commit. Estos tres archivos van a git: son la historia de cómo fuimos aprendiendo.

Una regla nueva se agrega cuando **algo salió mal y no queremos que se repita**, o
cuando Facu corrigió lo mismo dos veces. No por completitud.

## Historial

| Fecha | Cambio |
|---|---|
| 04/08/2026 | `CONSTITUCION-v3`. **Regla 23**: el software crece cuando aparece trabajo nuevo, nunca cuando aparece una idea nueva. Salió del sprint del escritorio de Astronomy — Facu la dictó como Ley 8 del repo y vale para los cuatro negocios. La pregunta que autoriza a construir es *¿esta persona necesitó salir del sistema?* |
| 03/08/2026 | `CONSTITUCION-v2`. Sección **"Cómo crece esto"**: el chequeo de cierre, los tres disparadores de una regla nueva, y a qué capa va cada aprendizaje. Sin eso los tres documentos se congelaban. |
| 03/08/2026 | `v1`. Sobre el esqueleto que bajó Facu (guardado en `archive/empresa-os-esqueleto-2026-08-03/`), reescrito con sus modos de falla reales, sus KPIs y sus fuentes. |
