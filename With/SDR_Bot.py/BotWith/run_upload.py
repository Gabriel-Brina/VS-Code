"""
Script direto para upload de mensagens - Execute este script para carregar as mensagens
"""
import asyncio
import sys
import re
from pathlib import Path

# Adiciona o diretório atual ao path
sys.path.append(str(Path(__file__).parent))

from config import Config
from core.database_manager import DatabaseManager

class SimpleMessageUploader:
    """Upload simples de mensagens via arquivo .txt"""
    
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager(self.config)
        
    async def initialize(self):
        """Inicializa componentes"""
        await self.db.initialize()
        print("✅ Uploader simples inicializado!")
    
    def parse_txt_file(self, txt_file: str) -> list:
        """
        Lê arquivo .txt e extrai pares cliente/gabriel
        Formato esperado:
        cliente: "pergunta do cliente"
        gabriel: "minha resposta"
        """
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Padrão para encontrar pares cliente/gabriel
            pattern = r'cliente:\s*"([^"]+)"\s*gabriel:\s*"([^"]+)"'
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            
            messages = []
            for user_msg, gabriel_resp in matches:
                messages.append({
                    'user_message': user_msg.strip(),
                    'gabriel_response': gabriel_resp.strip()
                })
            
            return messages
            
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
            return []
    
    async def upload_from_txt(self, txt_file: str) -> int:
        """Upload de mensagens do arquivo .txt"""
        messages = self.parse_txt_file(txt_file)
        
        if not messages:
            print("❌ Nenhuma mensagem encontrada no arquivo!")
            return 0
        
        print(f"📝 Encontradas {len(messages)} mensagens")
        
        uploaded = 0
        for i, msg in enumerate(messages, 1):
            try:
                # Salva no banco (o hash é criado automaticamente)
                success = self.db.save_conversation(
                    user_message=msg['user_message'],
                    gabriel_response=msg['gabriel_response'],
                    context={"source": "Importado via .txt"},
                    intent=""
                )
                
                if success:
                    print(f"✅ {i:2d}. {msg['user_message'][:50]}...")
                    uploaded += 1
                else:
                    print(f"⚠️  {i:2d}. Já existe: {msg['user_message'][:50]}...")
                    
            except Exception as e:
                print(f"❌ {i:2d}. Erro: {e}")
        
        print(f"\n🎉 {uploaded} mensagens carregadas com sucesso!")
        return uploaded
    
    async def show_stats(self):
        """Mostra estatísticas do banco"""
        stats = await self.db.get_conversation_stats()
        print("\n📊 Estatísticas do Banco de Dados")
        print("=" * 40)
        print(f"Total de conversas: {stats.get('total_conversations', 0)}")
        print(f"Última conversa: {stats.get('last_conversation', 'Nenhuma')}")

async def run_upload():
    print("🚀 Iniciando upload das mensagens...")
    
    uploader = SimpleMessageUploader()
    await uploader.initialize()
    
    # Executa upload
    result = await uploader.upload_from_txt('data/mensagens_simples.txt')
    print(f"✅ Total carregado: {result} mensagens")
    
    # Mostra estatísticas
    await uploader.show_stats()
    
    print("🎉 Upload concluído!")

if __name__ == "__main__":
    asyncio.run(run_upload())
