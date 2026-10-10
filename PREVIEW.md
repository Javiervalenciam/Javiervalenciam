# Mantenimiento del perfil

## Estructura

```text
README.md                         Perfil (Markdown + SVG)
assets/                           SVG animados (sin JS ni fuentes externas)
scripts/svgkit.py                 Paleta, tipografía, iconos y utilidades
scripts/build_assets.py           Diseño estático: portada, áreas, proyectos, contacto, botones
scripts/github_stats.py           Métricas y estadísticas con datos reales de la API
data/github-stats.json            Última instantánea de datos (solo agregados)
.github/workflows/profile-stats.yml  Regenera las estadísticas cada día
```

## Estadísticas automáticas (incluyen privados)

1. Crea un token *fine-grained* en GitHub → Settings → Developer settings, con acceso de solo lectura
   a **todos tus repositorios** (permisos *Metadata* y *Contents*: Read-only).
2. En este repositorio: Settings → Secrets and variables → Actions → **New repository secret**,
   nombre `PROFILE_STATS_TOKEN`, valor el token.
3. Ejecuta la acción *Actualizar estadísticas del perfil* desde la pestaña **Actions** o espera a la ejecución diaria.

Sin el secreto, la acción termina sin cambios y el perfil conserva la última instantánea.

## Editar el diseño

- Textos de proyectos y áreas: `PROJECTS` y `focus()` en `scripts/build_assets.py`.
- Colores: constantes al inicio de `scripts/svgkit.py` (terracota, azul, verde).
- Regenerar: `python scripts/build_assets.py` y `python scripts/github_stats.py`.
- El catálogo de los 30 repositorios es Markdown en `README.md`.
- Las animaciones usan CSS dentro de cada SVG y respetan `prefers-reduced-motion`.
