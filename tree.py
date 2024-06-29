import os

def generate_structure(root_dir, indent='', excluded_dirs=None):
    if excluded_dirs is None:
        excluded_dirs = []

    for item in os.listdir(root_dir):
        path = os.path.join(root_dir, item)
        if os.path.isdir(path):
            if item in excluded_dirs:
                continue
            print(indent + '├── ' + item)
            generate_structure(path, indent + '│   ', excluded_dirs)
        else:
            print(indent + '├── ' + item)

if __name__ == "__main__":
    project_root = '.'  # путь к корню вашего проекта
    excluded_dirs = ['venv', 'postgres-data', 'migrations', '.git']  # здесь укажите папки, которые хотите исключить
    print(f"{project_root}/")
    generate_structure(project_root, '', excluded_dirs)
