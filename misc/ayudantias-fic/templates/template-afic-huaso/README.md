# Template AFIC — Huaso ([Cristopher](https://github.com/LucipherDeVas))

> Para el huaso menos huaso del país. Curioso que no sea tan asquerosamente
> derechista como se autopercibe. Muu muu.

Creado por Edicson Solar Salinas para
[Ayudantías FIC](https://github.com/afic-udp).

## Antes de empezar

1. Edita `settings/_deck.tex` con el ramo, tema y fecha.
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
- `settings/_colors.tex`: paleta de colores.
- `settings/_illustrations.tex`: motivos gráficos de la presentación.
- `assets/svg/`: recursos originales editables.
- `assets/rendered/`: recursos PNG utilizados por la presentación.
- `main.pdf`: vista previa del template.

## Recursos gráficos

La presentación usa los PNG de `assets/rendered/` para sus motivos de portada.
Si cambias una ilustración, conserva su nombre o actualiza la referencia
correspondiente en `settings/_illustrations.tex`.

## Créditos

Diseñado por [Edicson Solar Salinas](https://github.com/lavapatos) para
Ayudantías FIC.
