# Template Ensayo PAES

Template para armar los ensayos PAES de Preuportaleanos. Sirve para cualquier
prueba (Competencia Matemática 1 y 2, Competencia Lectora, Ciencias, e Historia
y Ciencias Sociales). Desde los mismos archivos se compila una edición en blanco
y negro para imprimir y una a color para compartir en digital.

## Antes de empezar

1. Edita `settings/_datos.tex` con la prueba, la sigla, el período, la fecha,
   el número de preguntas, las alternativas y la duración.
2. Si la prueba no es de matemáticas, deja `\consideracionesmatematicasfalse`
   para quitar la página de consideraciones y símbolos.
3. Reemplaza las preguntas de ejemplo de `ejes/` por las del ensayo. Puedes
   cambiar la cantidad de archivos de eje; se cargan en orden desde `main.tex`.

## Ediciones

En `settings/_datos.tex`:

- `\edicioncolorfalse`: edición para imprimir, en blanco y negro.
- `\edicioncolortrue`: edición digital, con la paleta del logo.

Para que la misma fuente funcione en las dos ediciones:

- En las figuras usa solo los colores `relleno`, `rellenomedio`,
  `rellenofuerte`, `tinta` y `acento` (definidos en `settings/_colores.tex`),
  nunca `gray!NN` ni colores directos.
- Si un enunciado nombra un color, usa `\segunedicion{texto en b/n}{texto a color}`.
  Por ejemplo: `bolitas \segunedicion{grises}{rosadas} y blancas`.

## Formato de una pregunta

```latex
\item Enunciado de la pregunta.
\begin{enumerate}
    \item Alternativa
    \item Alternativa % <- correcta
    \item Alternativa
    \item Alternativa
\end{enumerate}
```

La alternativa correcta se marca solo con el comentario `% <- correcta`, que no
aparece en el PDF.

## Convenciones

- Decimales en modo matemático con punto: `$0.15$` se ve como 0,15. Escribir
  `$0,15$` deja un espacio de más.
- Miles en modo matemático con llaves: `$320{.}000$`. En texto: `\$320.000`.
- Flechas de TikZ con `-latex` o `latex-latex`. Con babel en español, `->`
  no compila.
- Coordenadas e intervalos con espacio: `$A(-2,\ 1)$`, `$[20,\ 25\,[$`.
- `\vspace{.1cm}` al final de las alternativas que llevan fracciones.
- Negrita solo para `\textbf{NO}` o `\textbf{SIN}` en un enunciado.
- Ninguna pregunta debe quedar cortada entre dos páginas. Si pasa, se pone
  `\newpage` justo antes de esa pregunta.
- Las preguntas corren seguidas, sin títulos de eje, como en la PAES.

## Compilación

Desde esta carpeta:

```bash
pdflatex main.tex
pdflatex main.tex
```

La segunda pasada es necesaria para el total de páginas del pie ("3 de 30").

## Estructura

- `main.tex`: orden del ensayo (portada, instrucciones, ejes y cierre).
- `settings/_datos.tex`: datos del ensayo y elección de la edición.
- `settings/_colores.tex`: paleta del preu y colores de uso en las figuras.
- `settings/_estilo.tex`: encabezado, pie de página, numeración y cierre.
- `settings/_packages.tex`: paquetes y página.
- `portada.tex`: portada con los datos del alumno.
- `instrucciones.tex`: instrucciones, consideraciones y símbolos matemáticos.
- `ejes/`: un archivo por eje temático, con preguntas de ejemplo.
- `assets/logo/`: logo de Preuportaleanos.
- `main.pdf`: vista previa (edición en blanco y negro).

## Créditos

Diseñado por [Edicson Solar Salinas](https://github.com/lavapatos) para Preuportaleanos.
