import os
import json
import glob

def main():
    try:
        metadata_files = glob.glob(os.path.join("**", "metadata.json"), recursive=True)
        templates = []
        
        for file in metadata_files:
            try:
                with open(file, "r", encoding="utf-8-sig") as f:
                    data = json.load(f)
                    
                    if not isinstance(data, dict):
                        continue
                    
                    templates.append({
                        "course": data.get("course", "N/A"),
                        "author": data.get("author", "Anónimo"),
                        "type": data.get("template_type", "N/A"),
                        "path": os.path.dirname(file).replace("\\", "/")
                    })
                    
            except Exception:
                continue

        table = [
            "## Templates",
            "",
            "| Curso | Autor | Tipo | Enlace |",
            "|-------|-------|------|--------|"
        ]
        for tpl in templates:
            table.append(f"| {tpl['course']} | {tpl['author']} | {tpl['type']} | [Ver]({tpl['path']}) |")

        with open("README.md", "r+", encoding="utf-8") as f:
            content = f.read()
            start = content.find("<!-- TABLE_START -->")
            end = content.find("<!-- TABLE_END -->") + len("<!-- TABLE_END -->")
            new_content = content[:start] + "<!-- TABLE_START -->\n" + "\n".join(table) + "\n<!-- TABLE_END -->" + content[end:]
            f.seek(0)
            f.write(new_content)
            f.truncate()

    except Exception:
        exit(1)

if __name__ == "__main__":
    main()