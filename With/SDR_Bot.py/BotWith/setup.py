"""
Setup simples do Gabriel AI - SDR Automation Bot
"""
import os
import subprocess
import sys

def install_dependencies():
    """Instala dependências necessárias"""
    print("🚀 Instalando dependências do Gabriel AI...")
    
    dependencies = [
        "python-dotenv",
        "colorama", 
        "rich"
    ]
    
    for dep in dependencies:
        try:
            print(f"📦 Instalando {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} instalado com sucesso!")
        except subprocess.CalledProcessError:
            print(f"❌ Erro ao instalar {dep}")
            return False
    
    return True

def create_env_file():
    """Cria arquivo .env se não existir"""
    if not os.path.exists('.env'):
        print("📝 Criando arquivo .env...")
        with open('.env', 'w') as f:
            f.write("""# Gabriel AI - Configurações
OPENAI_API_KEY=sua_chave_openai_aqui
CLINT_API_KEY=sua_chave_clint_aqui
CLINT_BASE_URL=https://api.clint.com
""")
        print("✅ Arquivo .env criado!")
    else:
        print("ℹ️  Arquivo .env já existe")

def create_directories():
    """Cria diretórios necessários"""
    dirs = ['logs', 'database/persona/audios', 'database/persona/conversas', 
            'database/persona/documentos', 'database/persona/imagens']
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"📁 Diretório {dir_path} criado/verificado")

def main():
    print("🤖 Setup do Gabriel AI - SDR Automation Bot")
    print("=" * 50)
    
    # Instala dependências
    if not install_dependencies():
        print("❌ Falha na instalação de dependências")
        return
    
    # Cria arquivo .env
    create_env_file()
    
    # Cria diretórios
    create_directories()
    
    print("\n🎉 Setup concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Edite data/mensagens_simples.txt com suas conversas")
    print("2. Execute: python run_upload.py")
    print("3. Teste: python terminal_bot.py")
    print("\n✨ Gabriel AI está pronto para uso!")

if __name__ == "__main__":
    main()
