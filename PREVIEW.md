# Instalación y personalización

## Estructura

```text
README.md
assets/
  hero.svg
  divider.svg
  project-indemnizaciones.svg
  project-pensional.svg
  project-historias360.svg
  project-pos-heladeria.svg
  project-web-products.svg
```

## Uso

1. Copia `README.md` y la carpeta `assets/` en la raíz del repositorio `Javiervalenciam/Javiervalenciam`.
2. Conserva exactamente las rutas relativas `./assets/...`.
3. Haz commit solo después de revisar el resultado en la vista previa de GitHub.

## Personalización rápida

- Usuario de estadísticas: busca `username=Javiervalenciam` en `README.md`.
- Colores: modifica las variables hexadecimales dentro de cada SVG.
- Texto: edita títulos y descripciones tanto en el README como en las etiquetas accesibles `<title>` y `<desc>` de cada SVG.
- Movimiento: las animaciones usan CSS dentro del SVG y quedan desactivadas cuando el sistema solicita `prefers-reduced-motion`.

## Compatibilidad

- Los SVG no cargan JavaScript ni fuentes externas.
- Las rutas son relativas y compatibles con GitHub.
- Las estadísticas dependen de servicios externos, pero el contenido principal no.
- Los SVG incluyen alternativa estática mediante reducción de movimiento.

## Limitaciones verificadas

- `AppPensional` y `AppHistorias360` aparecen como repositorios privados; se usó únicamente la descripción y el stack visibles en las capturas.
- No fue posible inspeccionar públicamente el detalle técnico de `SistemaPOS-Heladeria`.
- `dashboardns.vercel.app` no respondió durante la revisión.
- `Finanzas JV` solo mostró su pantalla de restauración de sesión segura; no se infirieron funciones internas adicionales.
