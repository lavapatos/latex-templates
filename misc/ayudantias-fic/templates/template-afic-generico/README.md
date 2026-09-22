# Template AFIC — General

Template de presentación para cualquier ayudantía de
[Ayudantías FIC](https://github.com/afic-udp).

Creado por Edicson Solar Salinas para Ayudantías FIC.

## Antes de empezar

1. Edita `settings/_deck.tex` con el ramo, tema, nombre del ayudante, contacto y fecha.
2. Reemplaza las diapositivas de ejemplo en `main.tex` por el contenido de tu
   ayudantía.
3. Conserva la estructura de `settings/` mientras prepares tu presentación.

## Compilación

Desde esta carpeta:

```bash
lualatex main.tex
lualatex main.tex
```

## Estructura

- `main.tex`: contenido y orden de las diapositivas.
- `settings/_deck.tex`: datos de la ayudantía, cita y redes.
- `settings/_colors.tex`: paleta de colores de AFIC.
- `settings/_illustrations.tex`: motivos gráficos de la presentación.
- `assets/logo/`: logo de Ayudantías FIC.
- `assets/svg/`: recursos originales editables.
- `assets/rendered/`: recursos PNG utilizados por la presentación.
- `main.pdf`: vista previa del template.

## Recursos gráficos

La presentación usa el logo de AFIC y los PNG de `assets/rendered/`. Si cambias
una ilustración, conserva su nombre o actualiza la referencia correspondiente
en `settings/_illustrations.tex`.

## Créditos

Diseñado por [Edicson Solar Salinas](https://github.com/lavapatos) para
Ayudantías FIC.
