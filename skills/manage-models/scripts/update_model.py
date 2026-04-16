import json
import argparse
import os

# Danh sách 3 file cấu hình cần đồng bộ
PATHS = [
    "/opt/openclaw/.openclaw/openclaw.json",
    "/root/.openclaw/openclaw.json",
    "/opt/openclaw/config/openclaw.json"
]

def update_config(filepath, args):
    if not os.path.exists(filepath):
        print(f"[-] Bỏ qua {filepath} vì không tồn tại.")
        return

    try:
        with open(filepath, 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"[!] Lỗi khi đọc {filepath}: {e}")
        return

    # 1. Khởi tạo cấu trúc nếu chưa có
    if 'models' not in config: config['models'] = {}
    if 'providers' not in config['models']: config['models']['providers'] = {}

    # 2. Cập nhật Provider
    provider_id = args.provider_id
    if provider_id not in config['models']['providers']:
        config['models']['providers'][provider_id] = {
            "baseUrl": args.base_url,
            "api": args.api_type,
            "apiKey": args.api_key or "",
            "models": []
        }
    
    provider = config['models']['providers'][provider_id]
    if args.api_key: provider['apiKey'] = args.api_key
    if args.base_url: provider['baseUrl'] = args.base_url
    if args.api_type: provider['api'] = args.api_type

    # 3. Cập nhật danh sách Models trong Provider
    existing_models = [m['id'] for m in provider.get('models', [])]
    if args.model_id not in existing_models:
        provider.setdefault('models', []).append({
            "id": args.model_id,
            "name": args.model_name or args.model_id
        })

    # 4. Đăng ký với Agent Defaults
    if 'agents' not in config: config['agents'] = {}
    if 'defaults' not in config['agents']: config['agents']['defaults'] = {}
    if 'models' not in config['agents']['defaults']: config['agents']['defaults']['models'] = {}

    full_model_path = f"{provider_id}/{args.model_id}"
    if full_model_path not in config['agents']['defaults']['models']:
        config['agents']['defaults']['models'][full_model_path] = {}

    # 5. Cài đặt mô hình mặc định (Primary)
    if args.set_primary:
        if 'model' not in config['agents']['defaults']: config['agents']['defaults']['model'] = {}
        config['agents']['defaults']['model']['primary'] = full_model_path

    # Ghi lại file
    try:
        with open(filepath, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"[+] Đã cập nhật thành công: {filepath}")
    except Exception as e:
        print(f"[!] Lỗi khi ghi {filepath}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cập nhật cấu hình model cho OpenClaw")
    parser.add_argument("--provider-id", required=True, help="ID của provider (vd: openrouter-step)")
    parser.add_argument("--api-key", required=False, help="API Key của provider")
    parser.add_argument("--model-id", required=True, help="ID của model (vd: stepfun/step-3.5-flash)")
    parser.add_argument("--model-name", required=False, help="Tên hiển thị của model")
    parser.add_argument("--base-url", default="https://openrouter.ai/api/v1", help="Base URL của API")
    parser.add_argument("--api-type", default="openai-completions", help="Loại API (thường là openai-completions)")
    parser.add_argument("--set-primary", action="store_true", help="Đặt làm model mặc định")
    
    args = parser.parse_args()

    print(f"Tiến hành cập nhật model {args.model_id} cho provider {args.provider_id}...")
    for path in PATHS:
        update_config(path, args)
