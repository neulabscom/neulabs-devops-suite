import sys
import yaml
import os
import subprocess
import argparse

PROJECTS_FILEPATH = "./projects"
PROJECTS_DEFINATION_FILENAME = ".projects.yml"
EXCLUDE_PROJECTS_NAME = (".gitignore", )

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
    return parser

def main() -> bool:
    def add(**projects):
        for project, data in projects.items():
            print(f"[MODULE] Add {project}")
            path = os.path.join(PROJECTS_FILEPATH, data.get('target', "defualt"), project)
            cmd = f"git clone {data['url']} {path}"
            print(f"Command: {cmd}")
            subprocess.check_call(cmd, shell=True)

    def update(**projects):
        for project, data in projects.items():
            print(f"[MODULE] Update {project}")
            remove(**{project:data})
            add(**{project:data})

    def remove(**projects):
        for project, data in projects:
            print(f"[MODULE] Remove {project}")
            path = os.path.join(PROJECTS_FILEPATH, data.get('target', "default"), project)
            subprocess.check_call(f"rm -rf ./{path}", shell=True)
            
    try:
        args = argparser().parse_args()

        if not os.path.isfile(args.filename):
            raise FileExistsError(args.filename)

        file_parsed = yaml.load(open(args.filename), Loader=yaml.FullLoader) or {}
        
        base_projects = [ i for i in os.listdir(PROJECTS_FILEPATH) if i not in EXCLUDE_PROJECTS_NAME ]
        projects = []

        for k in base_projects:
            projects += os.listdir(os.path.join(PROJECTS_FILEPATH, k))

        project_add = list(set(file_parsed.keys()).difference(projects))
        project_update = list(set(file_parsed.keys()).intersection(projects))
        project_remove = list(set(projects).difference(file_parsed.keys()))

        print("[CHANGES]")
        [print(f"\t+ {k}") for k in project_add]
        [print(f"\t= {k}") for k in project_update]
        [print(f"\t- {k}") for k in project_remove]
        
        if input("Do you want to proceed with the indicated changes? [y/n] ").lower() not in ("y", "yes"):
            return 0

        remove(*project_remove)
        add(**{ k:v for k, v in file_parsed.items() if k in project_add})
        if args.force:
            update(**{ k:v for k, v in file_parsed.items() if k in project_update})
    except KeyboardInterrupt as e:
        raise Exception(str(e))
    except Exception as e:
        raise Exception(str(e))
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())