# Template OG Mesas de Estudio

Template para mesas de estudio del CAEA.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `main.tex` | Contenido de la mesa (ejercicios) |
| `config.sty` | Configuración y datos personalizables |
| `caea_logo.png` | Logo del CAEA |

## Uso

1. Copia esta carpeta a tu proyecto
2. Edita `config.sty` con los datos de tu mesa:
   - `\nroMesa` - número de la mesa
   - `\curso` - nombre del curso
   - `\semestre` y `\anho` - periodo
   - `\ayudanteUno`, `\ayudanteDos`, `\ayudanteTres` - nombres
   - `\ayudanteUnoMail`, etc. - correos
3. Edita `main.tex` con los ejercicios
4. Compila con `pdflatex` (si le temes a la vida solo ponlo en overleaf)

## Compilador

```
pdflatex main.tex
```

## Autor

Edicson Solar Salinas