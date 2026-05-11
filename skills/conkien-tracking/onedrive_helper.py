import os
import sys
import json
import argparse
import subprocess
import urllib.parse
import re
from datetime import datetime

# Configuration
API_BASE_URL = "https://gateway.maton.ai/one-drive/v1.0"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "shared-references", "vnpt_onedrive_structure.json"))

def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def get_api_key():
    key = os.environ.get("MATON_API_KEY")
    if not key:
        return "v2.q7eyXHFzT_Lr1YGzQxRIFA50CvegggHCdbojQf5zfoBqxaJe59-OaBGXkxRJw70jN2nsvRpDvPPKFEyMncX0Gn31JT8VNIkN_WV_RdJcId8d4Jg0F1KrfTp1"
    return key


def make_request(url, method="GET", headers=None, data=None):
    if headers is None:
        headers = {}
    
    api_key = get_api_key()
    # Use -w to get the HTTP status code at the end of the output
    cmd = ["curl", "-s", "-X", method, url, "-H", f"Authorization: Bearer {api_key}", "-w", "\n%{http_code}"]
    
    for k, v in headers.items():
        cmd.extend(["-H", f"{k}: {v}"])
    
    input_data = None
    if data:
        if isinstance(data, dict):
            input_data = json.dumps(data).encode('utf-8')
            if "Content-Type" not in headers:
                cmd.extend(["-H", "Content-Type: application/json"])
            # Tell curl to read data from stdin
            cmd.extend(["-d", "@-"])
        elif isinstance(data, bytes):
            input_data = data
            # Use --data-binary @- for files/binary to preserve integrity
            cmd.extend(["--data-binary", "@-"])

    if input_data:
        # Use stdin for data to avoid shell argument limits and handle binary
        result = subprocess.run(cmd, input=input_data, capture_output=True)
    else:
        result = subprocess.run(cmd, capture_output=True)
    
    output = result.stdout.decode('utf-8')
    if "\n" in output:
        parts = output.split("\n")
        status_code_str = parts[-1].strip()
        # Handle cases where -w might append more than one line or if body has newlines
        try:
            status_code = int(status_code_str)
            body_str = "\n".join(parts[:-1])
            try:
                body = json.loads(body_str) if body_str else {}
            except:
                body = body_str
            return status_code, body
        except ValueError:
            return 0, f"Failed to parse status code from: {status_code_str}"
    
    return 0, "Failed to get output from curl"

def create_folder(folder_name, parent_id):
    url = f"{API_BASE_URL}/drive/items/{parent_id}/children"
    data = {
        "name": folder_name,
        "folder": {},
        "@microsoft.graph.conflictBehavior": "fail"
    }
    
    status, body = make_request(url, method="POST", data=data)
    
    if status in [200, 201]:
        return body.get("id")
    elif status == 409: # Conflict
        return find_folder_in_parent(folder_name, parent_id)
    else:
        print(f"Error creating folder: {body}", file=sys.stderr)
        return None

def find_folder_in_parent(folder_name, parent_id):
    url = f"{API_BASE_URL}/drive/items/{parent_id}/children"
    status, body = make_request(url)
    
    if status == 200:
        children = body.get("value", [])
        target = folder_name.lower().strip()
        # Common prefixes to ignore or match flexibly
        prefixes = ["xã ", "phường ", "sở ", "ngành ", "ban "]
        
        # 1. Exact match (case-insensitive)
        for child in children:
            if "folder" in child:
                child_name = child.get("name", "").lower().strip()
                if child_name == target:
                    return child.get("id")
        
        # 2. Match with/without prefix
        for child in children:
            if "folder" in child:
                child_name = child.get("name", "").lower().strip()
                
                # Check if stripping prefixes from both sides makes them match
                clean_child = child_name
                for p in prefixes:
                    if clean_child.startswith(p):
                        clean_child = clean_child[len(p):].strip()
                        break
                
                clean_target = target
                for p in prefixes:
                    if clean_target.startswith(p):
                        clean_target = clean_target[len(p):].strip()
                        break
                
                if clean_child == clean_target and clean_target != "":
                    return child.get("id")
                    
    return None

def strip_uuid(filename):
    # Pattern for ---uuid.extension
    pattern = r"---[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
    name, ext = os.path.splitext(filename)
    clean_name = re.sub(pattern, "", name)
    return clean_name + ext

def get_available_name(parent_id, desired_name):
    # List children to check for name
    url = f"{API_BASE_URL}/drive/items/{parent_id}/children"
    status, body = make_request(url)
    if status != 200:
        return desired_name # Fallback
    
    children = body.get("value", [])
    existing_names = [child.get("name") for child in children]
    
    if desired_name not in existing_names:
        return desired_name
    
    # Generate new name: _v2, _v3...
    name_part, ext_part = os.path.splitext(desired_name)
    counter = 2
    while True:
        new_name = f"{name_part}_v{counter}{ext_part}"
        if new_name not in existing_names:
            return new_name
        counter += 1

def upload_file(file_path, parent_id, custom_name=None):
    if custom_name:
        file_name = custom_name
    else:
        file_name = os.path.basename(file_path)
        file_name = strip_uuid(file_name)
    
    # Handle conflict: (2), (3)...
    final_name = get_available_name(parent_id, file_name)
    
    # URL encode filename
    encoded_name = urllib.parse.quote(final_name)
    url = f"{API_BASE_URL}/drive/items/{parent_id}:/{encoded_name}:/content"
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    status, body = make_request(url, method="PUT", headers={"Content-Type": "application/octet-stream"}, data=file_data)
    
    if status in [200, 201]:
        item_id = body.get("id")
        share_link = create_share_link(item_id)
        return {
            "id": item_id,
            "name": body.get("name"),
            "webUrl": share_link or body.get("webUrl")
        }
    else:
        print(f"Error uploading file: {body}", file=sys.stderr)
        return None

def create_share_link(item_id):
    url = f"{API_BASE_URL}/drive/items/{item_id}/createLink"
    data = {
        "type": "view",
        "scope": "anonymous"
    }
    
    status, body = make_request(url, method="POST", data=data)
    if status in [200, 201]:
        return body.get("link", {}).get("webUrl")
    return None

def main():
    parser = argparse.ArgumentParser(description='OneDrive Helper for Conkien (Graph API)')
    parser.add_argument('--file', required=True, help='Path to file')
    parser.add_argument('--unit', required=True, help='Unit name (e.g. Xã Tân Châu)')
    parser.add_argument('--branch', required=True, choices=['Xa Phuong', 'So Nganh'], help='Branch name')
    parser.add_argument('--project', help='Project/Subfolder name (optional, e.g. Camera)')
    parser.add_argument('--name', help='Desired filename on OneDrive (optional)')
    
    args = parser.parse_args()
    if not os.path.exists(args.file):
        print(f"Error: File {args.file} not found", file=sys.stderr)
        sys.exit(1)
        
    config = load_config()
    branch_data = config['branches'].get(args.branch)
    
    if not branch_data:
        print(f"Error: Branch {args.branch} not found in config", file=sys.stderr)
        sys.exit(1)
        
    branch_id = branch_data['id']
    if 'units' not in branch_data:
        branch_data['units'] = {}
        
    # Find or create unit folder
    unit_info = branch_data['units'].get(args.unit)
    unit_id = unit_info.get('id') if unit_info else None
    
    if not unit_id:
        print(f"Checking folder for '{args.unit}' in '{args.branch}'...")
        unit_id = find_folder_in_parent(args.unit, branch_id)
        
        if not unit_id:
            print(f"Creating folder for '{args.unit}'...")
            unit_id = create_folder(args.unit, branch_id)
            
        if unit_id:
            # Update config with hierarchical unit
            branch_data['units'][args.unit] = {
                "id": unit_id,
                "projects": {}
            }
            save_config(config)
            print(f"Config updated for unit: {args.unit}")
            unit_info = branch_data['units'][args.unit]
        else:
            print(f"Failed to resolve unit folder for '{args.unit}'", file=sys.stderr)
            sys.exit(1)
            
    # Target folder defaults to unit folder
    target_folder_id = unit_id
    
    # If project is specified, find or create subfolder inside unit
    if args.project:
        if 'projects' not in unit_info:
            unit_info['projects'] = {}
            
        print(f"Checking subfolder for project '{args.project}' in '{args.unit}'...")
        
        # Check config first
        project_info = unit_info['projects'].get(args.project)
        project_id = project_info.get('id') if project_info else None
        
        if not project_id:
            project_id = find_folder_in_parent(args.project, unit_id)
            
            if not project_id:
                print(f"Creating subfolder for project '{args.project}'...")
                project_id = create_folder(args.project, unit_id)
                
            if project_id:
                # Update config with project
                unit_info['projects'][args.project] = {
                    "id": project_id
                }
                save_config(config)
                print(f"Config updated for project: {args.unit} > {args.project}")
        
        if project_id:
            target_folder_id = project_id
        else:
            print(f"Warning: Failed to resolve project folder '{args.project}', uploading to unit folder instead.", file=sys.stderr)

    # Upload file
    print(f"Uploading '{args.file}' to '{args.branch}' > '{args.unit}'" + (f" > '{args.project}'" if args.project else "") + "...")
    result = upload_file(args.file, target_folder_id, custom_name=args.name)
    
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
