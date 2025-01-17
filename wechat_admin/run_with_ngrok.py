from pyngrok import ngrok
import os
import sys
import subprocess
import time
import json
from urllib.request import urlopen

def run_server_with_ngrok():
    # 启动ngrok
    http_tunnel = ngrok.connect(8000)
    public_url = http_tunnel.public_url
    
    print(f"\n{'='*50}")
    print(f"Ngrok URL: {public_url}")
    print(f"{'='*50}\n")
    
    # 更新Django设置
    settings_path = 'wechat_admin/settings.py'
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取域名（去掉协议前缀）
    domain = public_url.split('://')[-1]
    
    # 更新ALLOWED_HOSTS
    if 'ALLOWED_HOSTS = [' in content:
        content = content.replace(
            'ALLOWED_HOSTS = [',
            f'ALLOWED_HOSTS = [\n    "{domain}",  # ngrok domain\n    '
        )
    
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Django settings updated with ngrok domain")
    
    # 启动Django服务器
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wechat_admin.settings')
    subprocess.run([sys.executable, 'manage.py', 'runserver'])

if __name__ == '__main__':
    try:
        run_server_with_ngrok()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        ngrok.kill()
