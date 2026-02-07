import os
import json
import glob
import subprocess


# obtener fecha del ultimo commit
def obtener_fecha_ultimo_commit(ruta_carpeta_template):
    
    # buscar archivos .tex en la carpeta del template
    patron_busqueda = os.path.join(ruta_carpeta_template, "*.tex")
    archivos_tex = glob.glob(patron_busqueda)
    
    # si no hay archivos .tex, retornar N/A
    if len(archivos_tex) == 0:
        return "N/A"
    
    # tomar el primer archivo .tex encontrado
    archivo_tex = archivos_tex[0]
    
    # construir comando git para obtener fecha
    # %cs = fecha corta ISO (yyy-mm-dd)
    comando_git = [
        "git",
        "log",
        "-1",
        "--format=%cs",
        "--",
        archivo_tex
    ]
    
    # ejecutar comando git
    try:
        resultado = subprocess.run(
            comando_git,
            capture_output=True,
            text=True,
            check=True
        )
        fecha = resultado.stdout.strip()
        
        # si no hay fecha porque hay archivo no commiteado, retornar N/A
        if fecha == "":
            return "N/A"
        
        return fecha
        
    except subprocess.CalledProcessError:
        return "N/A"
    except FileNotFoundError:
        return "N/A"


# leer un archivo metadata.json
def leer_metadata(ruta_archivo_metadata):
    
    # abrir y leer el archivo
    with open(ruta_archivo_metadata, "r", encoding="utf-8-sig") as archivo:
        contenido = json.load(archivo)
    
    # verificar que sea un diccionario
    if not isinstance(contenido, dict):
        return None
    
    return contenido


# construir fila de la tabla
def construir_fila_tabla(curso, autor, tipo, fecha, ruta):
    
    # formato: | curso | autor | tipo | fecha | enlace |
    enlace = f"[Ver]({ruta})"
    fila = f"| {curso} | {autor} | {tipo} | {fecha} | {enlace} |"
    
    return fila


# construir fila para readme de curso (mas simple)
def construir_fila_tabla_curso(nombre_template, autor, tipo, fecha):
    
    # ruta relativa desde el readme del curso
    enlace = f"[Ver](templates/{nombre_template})"
    fila = f"| {nombre_template} | {autor} | {tipo} | {fecha} | {enlace} |"
    
    return fila


# generar tabla markdown completa
def generar_tabla_markdown(lista_templates):
    
    # header de la tabla
    lineas = []
    lineas.append("## Templates")
    lineas.append("")
    lineas.append("| Curso | Autor | Tipo | Modificado | Enlace |")
    lineas.append("|-------|-------|------|------------|--------|")
    
    # agregar cada template como fila
    for template in lista_templates:
        fila = construir_fila_tabla(
            template["curso"],
            template["autor"],
            template["tipo"],
            template["fecha"],
            template["ruta"]
        )
        lineas.append(fila)
    
    # unir todas las lineas con salto de linea
    tabla_completa = "\n".join(lineas)
    
    return tabla_completa


# generar readme para un curso especifico
def generar_readme_curso(nombre_curso, templates_del_curso):
    
    lineas = []
    lineas.append(f"# {nombre_curso}")
    lineas.append("")
    lineas.append("| Template | Autor | Tipo | Modificado | Enlace |")
    lineas.append("|----------|-------|------|------------|--------|")
    
    for template in templates_del_curso:
        fila = construir_fila_tabla_curso(
            template["nombre_template"],
            template["autor"],
            template["tipo"],
            template["fecha"]
        )
        lineas.append(fila)
    
    contenido = "\n".join(lineas)
    return contenido


# actualizar el readme principal
def actualizar_readme(tabla_nueva):
    
    # leer contenido actual del readme
    with open("README.md", "r", encoding="utf-8") as archivo:
        contenido_actual = archivo.read()
    
    # buscar marcadores de inicio y fin
    marcador_inicio = "<!-- TABLE_START -->"
    marcador_fin = "<!-- TABLE_END -->"
    
    posicion_inicio = contenido_actual.find(marcador_inicio)
    posicion_fin = contenido_actual.find(marcador_fin) + len(marcador_fin)
    
    # armar el nuevo contenido
    parte_antes = contenido_actual[:posicion_inicio]
    parte_despues = contenido_actual[posicion_fin:]
    
    contenido_nuevo = parte_antes + marcador_inicio + "\n" + tabla_nueva + "\n" + marcador_fin + parte_despues
    
    # escribir nuevo contenido
    with open("README.md", "w", encoding="utf-8") as archivo:
        archivo.write(contenido_nuevo)


# generar readmes por curso
def generar_readmes_por_curso(lista_templates):
    
    # agrupar templates por carpeta de curso
    # la carpeta de curso es el directorio padre de "templates/"
    cursos = {}
    
    for template in lista_templates:
        ruta = template["ruta"]
        
        # buscar donde esta "templates/" en la ruta
        # ejemplo: eit/redes/templates/template-dylan-redes
        # carpeta_curso seria: eit/redes
        partes = ruta.split("/")
        
        # encontrar el indice de "templates"
        if "templates" not in partes:
            continue
        
        indice_templates = partes.index("templates")
        
        # la carpeta del curso es todo antes de "templates"
        carpeta_curso = "/".join(partes[:indice_templates])
        
        # el nombre del template es lo que sigue despues de "templates"
        nombre_template = partes[indice_templates + 1] if indice_templates + 1 < len(partes) else "unknown"
        
        # obtener nombre legible del curso (ultima parte de la ruta del curso)
        nombre_curso = partes[indice_templates - 1] if indice_templates > 0 else "misc"
        
        # agregar al diccionario de cursos
        if carpeta_curso not in cursos:
            cursos[carpeta_curso] = {
                "nombre": nombre_curso,
                "templates": []
            }
        
        cursos[carpeta_curso]["templates"].append({
            "nombre_template": nombre_template,
            "autor": template["autor"],
            "tipo": template["tipo"],
            "fecha": template["fecha"]
        })
    
    # generar readme para cada curso
    for carpeta_curso, info_curso in cursos.items():
        
        contenido_readme = generar_readme_curso(
            info_curso["nombre"],
            info_curso["templates"]
        )
        
        ruta_readme = os.path.join(carpeta_curso, "README.md")
        
        print(f"generando {ruta_readme}")
        
        with open(ruta_readme, "w", encoding="utf-8") as archivo:
            archivo.write(contenido_readme)


# main porque si
def main():
    
    # buscar todos los archivos metadata.json en el repositorio
    patron_busqueda = os.path.join("**", "metadata.json")
    archivos_metadata = glob.glob(patron_busqueda, recursive=True)
    
    print(f"encontrados {len(archivos_metadata)} archivos metadata.json")
    
    # lista para guardar info de cada template
    lista_templates = []
    
    # procesar cada archivo metadata.json
    for ruta_metadata in archivos_metadata:
        
        print(f"procesando: {ruta_metadata}")
        
        # leer la metadata
        try:
            metadata = leer_metadata(ruta_metadata)
        except Exception as error:
            print(f"error de lectura de metadata: {error}")
            continue
        
        # si no se pudo leer, saltar
        if metadata is None:
            print(f"saltando porque metadata invalida")
            continue
        
        # obtener la carpeta donde esta el template
        carpeta_template = os.path.dirname(ruta_metadata)
        carpeta_template = carpeta_template.replace("\\", "/")  # por si windows
        
        # obtener fecha del ultimo commit
        fecha_modificacion = obtener_fecha_ultimo_commit(carpeta_template)
        print(f"fecha ultima modificacion: {fecha_modificacion}")
        
        # extraer datos del metadata
        curso = metadata.get("course", "N/A")
        autor = metadata.get("author", "Anonimo")
        tipo = metadata.get("template_type", "N/A")
        
        # agregar a la lista
        info_template = {
            "curso": curso,
            "autor": autor,
            "tipo": tipo,
            "fecha": fecha_modificacion,
            "ruta": carpeta_template
        }
        lista_templates.append(info_template)
        print(f"ok: {curso} por {autor}")
    
    # generar la tabla markdown principal
    print("")
    print("generando tabla markdown principal")
    tabla = generar_tabla_markdown(lista_templates)
    
    # actualizar el README principal
    print("actualizando README.md")
    actualizar_readme(tabla)
    
    # generar READMEs por curso
    print("")
    print("generando READMEs por curso")
    generar_readmes_por_curso(lista_templates)
    
    print("")
    print("listo")


main()