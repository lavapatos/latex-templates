import os
import json
import glob
import subprocess


# ejecutar un comando git y devolver su salida (None si falla)
def ejecutar_git(argumentos):

    comando = ["git", "-c", "core.quotePath=false"] + argumentos

    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True
        )
        return resultado.stdout

    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None


# convertir el texto de un metadata.json en diccionario (None si no sirve)
def parsear_metadata(texto):

    try:
        contenido = json.loads(texto.lstrip("﻿"))
    except (ValueError, AttributeError):
        return None

    if not isinstance(contenido, dict):
        return None

    return contenido


# leer un archivo metadata.json
def leer_metadata(ruta_archivo_metadata):

    with open(ruta_archivo_metadata, "r", encoding="utf-8-sig") as archivo:
        return parsear_metadata(archivo.read())


# buscar el commit que agrego el metadata.json por primera vez
# --follow sigue los renombres de carpeta y --diff-filter=A deja solo el commit
# que creo el archivo, asi la fecha y el autor no cambian aunque alguien edite
# el template despues
def obtener_primer_aporte(ruta_metadata):

    salida = ejecutar_git([
        "log",
        "--follow",
        "--diff-filter=A",
        "--format=commit %H %as",  # %as = fecha corta (yyyy-mm-dd) del autor del commit
        "--name-only",
        "--",
        ruta_metadata
    ])

    # sin salida: el archivo todavia no esta commiteado
    if not salida:
        return None

    # la salida viene asi, del commit mas nuevo al mas viejo:
    # commit <hash> <fecha>
    #
    # <ruta del archivo en ese commit>
    commits = []
    for linea in salida.splitlines():
        linea = linea.strip()

        if linea.startswith("commit "):
            _, hash_commit, fecha = linea.split(" ", 2)
            commits.append({"hash": hash_commit, "fecha": fecha, "ruta": None})

        elif linea != "" and len(commits) > 0 and commits[-1]["ruta"] is None:
            commits[-1]["ruta"] = linea

    if len(commits) == 0:
        return None

    # el ultimo de la lista es el mas viejo, o sea, el aporte original
    primero = commits[-1]
    ruta_original = primero["ruta"] if primero["ruta"] else ruta_metadata

    # leer el metadata.json tal como venia en ese primer commit
    texto_original = ejecutar_git(["show", primero["hash"] + ":" + ruta_original])
    metadata_original = parsear_metadata(texto_original) if texto_original else None

    return {
        "fecha": primero["fecha"],
        "metadata": metadata_original
    }


# escapar texto para que no rompa una celda de tabla markdown
def celda(texto):

    return str(texto).replace("|", "\\|").strip()


# construir fila de la tabla principal
def construir_fila_tabla(template):

    # formato: | nombre | curso | autor | tipo | agregado | enlace |
    enlace = f"[Ver]({template['ruta']})"
    fila = (
        f"| {celda(template['nombre'])} | {celda(template['curso'])} "
        f"| {celda(template['autor'])} | {celda(template['tipo'])} "
        f"| {template['fecha']} | {enlace} |"
    )

    return fila


# construir fila para readme de curso (sin columna curso)
def construir_fila_tabla_curso(template):

    # ruta relativa desde el readme del curso
    enlace = f"[Ver](templates/{template['carpeta']})"
    fila = (
        f"| {celda(template['nombre'])} | {celda(template['autor'])} "
        f"| {celda(template['tipo'])} | {template['fecha']} | {enlace} |"
    )

    return fila


# generar tabla markdown completa
def generar_tabla_markdown(lista_templates):

    lineas = []
    lineas.append("## Templates")
    lineas.append("")
    lineas.append("| Nombre | Curso | Autor | Tipo | Agregado | Enlace |")
    lineas.append("|--------|-------|-------|------|----------|--------|")

    for template in lista_templates:
        lineas.append(construir_fila_tabla(template))

    return "\n".join(lineas)


# generar readme para un curso especifico
def generar_readme_curso(nombre_curso, templates_del_curso):

    lineas = []
    lineas.append(f"# {nombre_curso}")
    lineas.append("")
    lineas.append("| Nombre | Autor | Tipo | Agregado | Enlace |")
    lineas.append("|--------|-------|------|----------|--------|")

    for template in templates_del_curso:
        lineas.append(construir_fila_tabla_curso(template))

    return "\n".join(lineas) + "\n"


# actualizar el readme principal
def actualizar_readme(tabla_nueva):

    with open("README.md", "r", encoding="utf-8") as archivo:
        contenido_actual = archivo.read()

    marcador_inicio = "<!-- TABLE_START -->"
    marcador_fin = "<!-- TABLE_END -->"

    posicion_inicio = contenido_actual.find(marcador_inicio)
    posicion_fin = contenido_actual.find(marcador_fin)

    # sin marcadores no se toca nada, para no romper el README
    if posicion_inicio == -1 or posicion_fin == -1 or posicion_fin < posicion_inicio:
        raise SystemExit("README.md no tiene los marcadores TABLE_START / TABLE_END")

    parte_antes = contenido_actual[:posicion_inicio]
    parte_despues = contenido_actual[posicion_fin + len(marcador_fin):]

    contenido_nuevo = parte_antes + marcador_inicio + "\n" + tabla_nueva + "\n" + marcador_fin + parte_despues

    with open("README.md", "w", encoding="utf-8") as archivo:
        archivo.write(contenido_nuevo)


# generar readmes por curso
def generar_readmes_por_curso(lista_templates):

    # agrupar templates por carpeta de curso (el directorio padre de "templates/")
    # ejemplo: eit/redes/templates/template-dylan-redes -> eit/redes
    cursos = {}

    for template in lista_templates:
        partes = template["ruta"].split("/")

        if "templates" not in partes:
            continue

        indice_templates = partes.index("templates")
        carpeta_curso = "/".join(partes[:indice_templates])
        nombre_curso = partes[indice_templates - 1] if indice_templates > 0 else "misc"

        if carpeta_curso not in cursos:
            cursos[carpeta_curso] = {"nombre": nombre_curso, "templates": []}

        cursos[carpeta_curso]["templates"].append(template)

    for carpeta_curso, info_curso in cursos.items():
        ruta_readme = os.path.join(carpeta_curso, "README.md")
        print(f"generando {ruta_readme}")

        with open(ruta_readme, "w", encoding="utf-8") as archivo:
            archivo.write(generar_readme_curso(info_curso["nombre"], info_curso["templates"]))


# armar la info de un template a partir de su metadata.json
def procesar_template(ruta_metadata):

    ruta_metadata = ruta_metadata.replace("\\", "/")  # por si windows

    try:
        metadata = leer_metadata(ruta_metadata)
    except OSError as error:
        print(f"error de lectura de metadata: {error}")
        return None

    if metadata is None:
        print("saltando porque metadata invalida")
        return None

    carpeta_template = os.path.dirname(ruta_metadata)
    carpeta = os.path.basename(carpeta_template)

    # fecha y autor salen del primer aporte, no de la version actual
    aporte = obtener_primer_aporte(ruta_metadata)
    metadata_original = aporte["metadata"] if aporte and aporte["metadata"] else {}

    autor_actual = str(metadata.get("author", "")).strip()
    autor_original = str(metadata_original.get("author", "")).strip()
    autor = autor_original or autor_actual or "Anonimo"

    if autor_original and autor_actual and autor_original != autor_actual:
        print(f"aviso: el author cambio a '{autor_actual}', se mantiene '{autor_original}'")

    # el nombre si se puede cambiar despues, si no hay se usa la carpeta
    nombre = str(metadata.get("name", "")).strip() or carpeta

    return {
        "nombre": nombre,
        "carpeta": carpeta,
        "curso": str(metadata.get("course", "N/A")),
        "autor": autor,
        "tipo": str(metadata.get("template_type", "N/A")),
        "fecha": aporte["fecha"] if aporte else "N/A",
        "ruta": carpeta_template
    }


def main():

    # buscar todos los archivos metadata.json en el repositorio
    archivos_metadata = sorted(glob.glob(os.path.join("**", "metadata.json"), recursive=True))
    print(f"encontrados {len(archivos_metadata)} archivos metadata.json")

    lista_templates = []

    for ruta_metadata in archivos_metadata:
        print(f"procesando: {ruta_metadata}")
        template = procesar_template(ruta_metadata)

        if template is None:
            continue

        lista_templates.append(template)
        print(f"ok: {template['nombre']} ({template['curso']}) por {template['autor']}, agregado {template['fecha']}")

    # orden estable: por curso y luego por nombre, para que la tabla no cambie sola
    lista_templates.sort(key=lambda t: (t["curso"].lower(), t["nombre"].lower(), t["ruta"]))

    print("")
    print("actualizando README.md")
    actualizar_readme(generar_tabla_markdown(lista_templates))

    print("")
    print("generando READMEs por curso")
    generar_readmes_por_curso(lista_templates)

    print("")
    print("listo")


if __name__ == "__main__":
    main()
