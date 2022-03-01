import pathlib
import sys
import yaml
import os
import subprocess
import argparse

PROJECTS_FILEPATH = os.getenv("NEULABS_DEVOPS_WORKSPACE", None)
if PROJECTS_FILEPATH is None:
    raise Exception("Neulabs env not found")

PROJECTS_DEFINATION_FILENAME = ".projects.yml"
PROJECTS_VS_EXTENSIONS_FILENAME = pathlib.Path(".vscode", "extensions.json")
PROJECTS_VS_SETTINGS_FILENAME = pathlib.Path(".vscode", "settings.json")
PROJECTS_VS_WORKSPACE_FILENAME = "projects.code-workspace"
WORKSPACE_EXCLUDE = ( PROJECTS_VS_WORKSPACE_FILENAME, "default", ".vscode" )

def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--filename",
        default=PROJECTS_DEFINATION_FILENAME,
        type=str,
        help="Name of the file containing the structure of the projects folder",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force to remove and add for existing projects",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        default=False,
        help="Force yes to answer",
    )
    return parser

def add_project(workspace, project, url):
        path = pathlib.Path(PROJECTS_FILEPATH, workspace, project)
        if not os.path.isdir(path):
            cmd = f"git clone {url} {path}"
            subprocess.check_call(cmd, shell=True)
            print(f"[SUCCESS] Add {project} in {path}")
        else:
            print(f"[ERROR] Add {project} in {path}")

def remove_workspace(workspace):
    path = pathlib.Path(PROJECTS_FILEPATH, workspace)
    if os.path.isdir(path):
        subprocess.check_call(f"rm -rf {path}", shell=True)
        print(f"[SUCCESS] Remove {workspace} in {path}")
    else:
        print(f"[ERROR] Remove {workspace} in {path}")

def remove_project(workspace, project):
    path = pathlib.Path(PROJECTS_FILEPATH, workspace, project)
    if os.path.isdir(path):
        subprocess.check_call(f"rm -rf {path}", shell=True)
        print(f"[SUCCESS] Remove {project} in {path}")
    else:
        print(f"[ERROR] Remove {project} in {path}")

def create_vs_workspace(file_parsed):
    import json
    os.makedirs(pathlib.Path(PROJECTS_FILEPATH, ".vscode"),exist_ok=True)
    vs_extensions = {
        "recommendations": [
            "esbenp.prettier-vscode",
            "eamodio.gitlens",
            "leodevbro.blockman",
            "ms-azuretools.vscode-docker",
            "hashicorp.terraform",
            "ms-python.python",
            "redhat.vscode-yaml",
            "shakram02.bash-beautify"
        ]
    }
    with open(pathlib.Path(PROJECTS_FILEPATH, PROJECTS_VS_EXTENSIONS_FILENAME), "w") as f:
        f.write(json.dumps(vs_extensions))

    vs_settins = {}
    with open(pathlib.Path(PROJECTS_FILEPATH, PROJECTS_VS_SETTINGS_FILENAME), "w") as f:
        f.write(json.dumps(vs_settins))

    vs_workspace = {
        "folders": [
            {
                "path": ".vscode"
            }
        ],
        "settings": {}
    }
    for workspace, data in file_parsed.items():
        vs_workspace["folders"].append({
            "name": workspace,
            "path": os.path.join(PROJECTS_FILEPATH, workspace)
        })
    with open(pathlib.Path(PROJECTS_FILEPATH, PROJECTS_VS_WORKSPACE_FILENAME), "w") as f:
        f.write(json.dumps(vs_workspace))

def create_projects_yml(file_parsed):
    with open(pathlib.Path(PROJECTS_DEFINATION_FILENAME), "w") as f:
        f.write(yaml.dump(file_parsed))
    

def main() -> bool:
    try:
        args = argparser().parse_args()

        if not os.path.isfile(args.filename):
            raise FileExistsError(args.filename)

        file_parsed = yaml.load(open(args.filename), Loader=yaml.FullLoader) or {}

        projects_to_add = []
        projects_to_update = []
        projects_to_remove = []
        projects_to_remove_workspace = []

        existing_workspace = {} 
        for target in [ w for w in os.listdir(PROJECTS_FILEPATH) if w not in WORKSPACE_EXCLUDE ]:
            existing_workspace[target] = os.listdir(pathlib.Path(PROJECTS_FILEPATH, target))

            if target in file_parsed.keys():
                remove = set(existing_workspace[target]).difference(file_parsed[target])
                if remove:
                    projects_to_remove.append((target, remove))
            else:
                projects_to_remove_workspace.append(target)

        for workspace, projects in {w:file_parsed[w] for w in file_parsed.keys() if w not in WORKSPACE_EXCLUDE}.items():
            add = set(projects).difference(existing_workspace.get(workspace, {}))
            if add:
                projects_to_add.append((workspace, { k:projects[k] for k in add}))

            update = set(projects).intersection(existing_workspace.get(workspace, {}))
            if update and args.force:
                projects_to_update.append((workspace, { k:projects[k] for k in update}))
        
        print("[ADD CHANGES]")
        for workspace, data in projects_to_add:
            print(f"\t{workspace} workspace:")
            [print(f"\t  + {project} (from {url})") for project, url in data.items()]

        print("\n[REMOVE CHANGES]")
        for workspace, data in projects_to_remove:
            print(f"\t{workspace} workspace:")
            [print(f"\t  - {project}") for project in data]

        print("\n[UPDATE CHANGES]")
        for workspace, data in projects_to_update:
            print(f"\t{workspace} workspace:")
            [print(f"\t  = {project} (from {url})") for project, url in data.items()]

        print("\n[REMOVE WORKSPACE]")
        for workspace in projects_to_remove_workspace:
            print(f"\tDelete {workspace} workspace")
            print("\n")
        
        if args.yes is False and input("Do you want to proceed with the indicated changes? [y/n] ").lower() not in ("y", "yes"):
            return 0

        for value in projects_to_remove:
            [ remove_project(workspace=value[0], project=project) for project in value[1]]

        for value in projects_to_remove_workspace:
            [ remove_workspace(workspace=value)]

        for value in projects_to_add:
            [ add_project(workspace=value[0], project=project, url=url) for project, url in value[1].items()]

        for value in projects_to_update:
            [ remove_project(workspace=value[0], project=project) for project in value[1]]
            [ add_project(workspace=value[0], project=project, url=url) for project, url in value[1].items()]

        create_vs_workspace(file_parsed)
        create_projects_yml(file_parsed)
    except KeyboardInterrupt as e:
        raise Exception(str(e))
    except Exception as e:
        raise Exception(str(e))
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())