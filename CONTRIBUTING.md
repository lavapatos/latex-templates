# Cómo Contribuir

Gracias por querer contribuir. Sigue estos pasos para agregar tu template.

## Pasos

### 1. Estructura de carpetas

Coloca tu template en la ruta correcta. Usa el nombre de curso según [CURSOS.md](CURSOS.md):

```
eit/[curso]/templates/[nombre-de-tu-template]/
```

para templates misceláneos:

```
misc/[categoria]/templates/[nombre-de-tu-template]/
```

### 2. Archivos requeridos

Tu carpeta debe contener **mínimo**:

| Archivo | Descripción |
|---------|-------------|
| `*.tex` | El archivo principal del template |
| `metadata.json` | Información del template (ver abajo) |

### 3. Formato del metadata.json

```json
{
    "name": "Nombre del template",
    "course": "nombre-del-curso",
    "area": "eit",
    "institution": "eit",
    "author": "Tu Nombre",
    "template_type": "lab-report",
    "file_path": "eit/curso/templates/tu-template"
}
```

**Campos:**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| `name` | Nombre visible del template (opcional, por defecto el nombre de la carpeta) | `"Informe de Redes"` |
| `course` | Nombre del curso (ver CURSOS.md) | `"redes"`, `"eda"` |
| `area` | Área principal | `"eit"`, `"misc"` |
| `institution` | Institución | `"eit"`, `"caea"` |
| `author` | Tu nombre completo | `"Juan Transistor"` |
| `template_type` | Tipo de documento (ver TIPOS.md) | `"lab-report"`, `"presentation"`, `"mesa"` |
| `file_path` | Ruta relativa al template | `"eit/redes/templates/mi-template"` |

El `author` y la fecha que aparecen en la tabla se toman del commit que agregó
el `metadata.json` por primera vez. Si después otra persona mejora el template o
le cambia el `name`, se sigue mostrando a quien lo aportó y la fecha en que lo
agregó.

### 4. Convenciones de nombres

- **Carpetas:** con guiones, por ejemplo `mi-template/`
- **Archivos:** sin espacios ni tildes, por ejemplo `main.tex` o `settings/_colores.tex`
- **Cursos:** usar abreviación de [CURSOS.md](CURSOS.md)

### 5. Hacer el Pull Request

1. Haz fork del repositorio
2. Crea tu branch: `git checkout -b agregar-template-[nombre]`
3. Agrega tus archivos
4. Commit: `git commit -m "agregar template [nombre] para [curso]"`
5. Push: `git push origin agregar-template-[nombre]`
6. Abre un pull request

Las pull requests son revisadas por [@lavapatos](https://github.com/lavapatos) (Edicson).

## La tabla se actualiza sola

No necesitas editar el README principal. Un workflow automático detecta tu `metadata.json` y actualiza la tabla.

## Dudas

Abre un Issue.
