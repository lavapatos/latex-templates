# Template AFIC — [Miki](https://github.com/miki-m0use)

> Para el mejor peruano que he conocido, una gran persona que intenta no romper
> lo que construye y está dispuesto a ayudar, aunque haya que decírselo veinte
> veces.

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
- `assets/svg/`: archivos fuente de la iconografía.
- `main.pdf`: vista previa del template.

## Recursos gráficos

La iconografía está definida dentro de `settings/_illustrations.tex`. La
carpeta `assets/svg/` conserva los recursos fuente si quieres revisar o volver
a trabajar los dibujos.

## Créditos

Diseñado por [Edicson Solar Salinas](https://github.com/lavapatos) para
Ayudantías FIC.
