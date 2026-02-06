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


# actualizar el readme (en serio?)
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
        
        print(f"Procesando: {ruta_metadata}")
        
        # leer la metadata
        try:
            metadata = leer_metadata(ruta_metadata)
        except Exception as error:
            print(f"error de lectura de metadata: {error}")
            continue
        
        # si no se pudo leer, saltar
        if metadata is None:
            print(f"saltan porque metadata invalida")
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
    
    # generar la tabla markdown
    print("")
    print("generando tabla markdown")
    tabla = generar_tabla_markdown(lista_templates)
    
    # actualizar el README
    print("actualizando README.md")
    actualizar_readme(tabla)
    
    print("listo")


main()