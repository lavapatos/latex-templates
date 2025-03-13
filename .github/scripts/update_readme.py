import os
import json
import glob

def main():
    try:
        metadata_files = glob.glob("latex-templates/**/metadata.json", recursive=True)
        templates = []
        
        for file in metadata_files:
            with open(file, "r") as f:
                data = json.load(f)
                rel_path = os.path.dirname(file)
                templates.append({
                    "course": data.get("course", "unknown"),
                    "author": data.get("author", "unknown"),
                    "type": data.get("template_type", "unknown"),
                    "path": rel_path
                })
        
        table = "## Templates\n\n"
        table += "| Curso | Autor | Tipo | Enlace |\n"
        table += "|-------|-------|------|--------|\n"
        for tpl in templates:
            table += f"| {tpl['course']} | {tpl['author']} | {tpl['type']} | [Ver]({tpl['path']}) |\n"
        
        with open("README.md", "r") as f:
            readme = f.read()
        
        if "<!-- TABLE_START -->" not in readme or "<!-- TABLE_END -->" not in readme:
            raise ValueError("Marcadores no encontrados en README.md")
        
        new_readme = readme.split("<!-- TABLE_START -->")[0] + "<!-- TABLE_START -->\n" + table + "\n<!-- TABLE_END -->" + readme.split("<!-- TABLE_END -->")[1]
        
        with open("README.md", "w") as f:
            f.write(new_readme)
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()