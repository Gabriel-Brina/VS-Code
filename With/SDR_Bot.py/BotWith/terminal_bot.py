"""
Terminal Bot - Interface de linha de comando para testar o Gabriel AI
"""
import asyncio
import logging
import sys
from pathlib import Path
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
import os

# Adiciona o diretório pai ao path para imports
sys.path.append(str(Path(__file__).parent))

from config import Config
from core.gabriel_ai import GabrielAI
from core.database_manager import DatabaseManager

# Inicializa colorama e rich
init(autoreset=True)
console = Console()

class TerminalBot:
    """Interface de terminal para o Gabriel AI"""
    
    def __init__(self):
        self.config = Config()
        self.gabriel_ai = None
        self.db_manager = None
        self.conversation_id = "terminal_session"
        self.setup_logging()
    
    def setup_logging(self):
        """Configura logging para o terminal"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/terminal_bot.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    async def initialize(self):
        """Inicializa componentes do bot"""
        try:
            console.print("🤖 Inicializando Gabriel AI...", style="cyan")
            
            # Inicializa database
            self.db_manager = DatabaseManager(self.config)
            await self.db_manager.initialize()
            
            # Inicializa Gabriel AI
            self.gabriel_ai = GabrielAI(self.config)
            await self.gabriel_ai.initialize()
            
            console.print("✅ Gabriel AI inicializado com sucesso!", style="green")
            return True
            
        except Exception as e:
            console.print(f"❌ Erro na inicialização: {e}", style="red")
            return False
    
    def show_welcome(self):
        """Mostra mensagem de boas-vindas"""
        welcome_text = Text()
        welcome_text.append("🤖 Gabriel AI - SDR Automation Bot\n", style="bold cyan")
        welcome_text.append("Desenvolvido para automação de SDR na Clint\n", style="white")
        welcome_text.append("Criado por Gabriel\n\n", style="yellow")
        welcome_text.append("Comandos disponíveis:\n", style="bold white")
        welcome_text.append("• Digite suas mensagens normalmente\n", style="white")
        welcome_text.append("• /help - Mostra ajuda\n", style="white")
        welcome_text.append("• /status - Mostra status do sistema\n", style="white")
        welcome_text.append("• /persona - Mostra informações da persona\n", style="white")
        welcome_text.append("• /upload <arquivo> - Faz upload de arquivo\n", style="white")
        welcome_text.append("• /history - Mostra histórico da conversa\n", style="white")
        welcome_text.append("• /clear - Limpa histórico da conversa\n", style="white")
        welcome_text.append("• /quit ou /exit - Sai do programa\n", style="white")
        
        panel = Panel(welcome_text, title="🚀 BotWith Terminal", border_style="cyan")
        console.print(panel)
    
    def show_help(self):
        """Mostra ajuda detalhada"""
        help_text = Text()
        help_text.append("📚 Guia de Uso do Gabriel AI\n\n", style="bold cyan")
        help_text.append("CONVERSAÇÃO:\n", style="bold yellow")
        help_text.append("• Digite qualquer mensagem e pressione Enter\n", style="white")
        help_text.append("• O Gabriel AI responderá como um SDR profissional\n", style="white")
        help_text.append("• Ele manterá contexto da conversa\n\n", style="white")
        
        help_text.append("UPLOADS:\n", style="bold yellow")
        help_text.append("• /upload arquivo.pdf - Processa documentos PDF\n", style="white")
        help_text.append("• /upload arquivo.docx - Processa documentos Word\n", style="white")
        help_text.append("• /upload arquivo.xlsx - Processa planilhas Excel\n", style="white")
        help_text.append("• /upload arquivo.mp3 - Transcreve áudios\n", style="white")
        help_text.append("• /upload arquivo.jpg - Extrai texto de imagens\n", style="white")
        help_text.append("• /upload arquivo.txt - Processa textos\n\n", style="white")
        
        help_text.append("PERSONA:\n", style="bold yellow")
        help_text.append("• O Gabriel AI age como Gabriel, um SDR profissional\n", style="white")
        help_text.append("• Ele usa conhecimento treinado sobre sua personalidade\n", style="white")
        help_text.append("• Responde de forma natural e contextual\n", style="white")
        
        panel = Panel(help_text, title="📖 Ajuda", border_style="yellow")
        console.print(panel)
    
    async def show_status(self):
        """Mostra status do sistema"""
        try:
            status_text = Text()
            status_text.append("🔍 Status do Sistema\n\n", style="bold cyan")
            
            # Status do banco de dados
            db_status = "🟢 Conectado" if self.db_manager else "🔴 Desconectado"
            status_text.append(f"Database: {db_status}\n", style="white")
            
            # Status do Gabriel AI
            ai_status = "🟢 Ativo" if self.gabriel_ai else "🔴 Inativo"
            status_text.append(f"Gabriel AI: {ai_status}\n", style="white")
            
            # Contadores
            if self.db_manager:
                stats = await self.db_manager.get_conversation_stats(self.conversation_id)
                status_text.append(f"Mensagens na sessão: {stats.get('message_count', 0)}\n", style="white")
                status_text.append(f"Documentos processados: {stats.get('document_count', 0)}\n", style="white")
            
            # Configurações
            status_text.append(f"\nPersona ativa: Gabriel\n", style="yellow")
            status_text.append(f"Modelo AI: {self.config.AI_MODEL_NAME}\n", style="yellow")
            status_text.append(f"Max tokens: {self.config.MAX_TOKENS}\n", style="yellow")
            
            panel = Panel(status_text, title="📊 Status", border_style="green")
            console.print(panel)
            
        except Exception as e:
            console.print(f"❌ Erro ao obter status: {e}", style="red")
    
    async def show_persona(self):
        """Mostra informações da persona"""
        try:
            if self.gabriel_ai:
                persona_info = await self.gabriel_ai.get_persona_info()
                
                persona_text = Text()
                persona_text.append("👤 Informações da Persona\n\n", style="bold cyan")
                persona_text.append(f"Nome: {persona_info.get('name', 'Gabriel')}\n", style="white")
                persona_text.append(f"Papel: {persona_info.get('role', 'SDR Profissional')}\n", style="white")
                persona_text.append(f"Estilo: {persona_info.get('style', 'Profissional e amigável')}\n", style="white")
                
                if persona_info.get('context'):
                    persona_text.append(f"\nContexto:\n{persona_info['context'][:200]}...\n", style="yellow")
                
                panel = Panel(persona_text, title="🎭 Persona Gabriel", border_style="magenta")
                console.print(panel)
            else:
                console.print("❌ Gabriel AI não está inicializado", style="red")
                
        except Exception as e:
            console.print(f"❌ Erro ao obter persona: {e}", style="red")
    
    async def show_history(self):
        """Mostra histórico da conversa"""
        try:
            if self.gabriel_ai:
                history = await self.gabriel_ai.get_conversation_history(self.conversation_id)
                
                if not history:
                    console.print("📝 Nenhum histórico encontrado para esta sessão", style="yellow")
                    return
                
                console.print("📜 Histórico da Conversa:", style="bold cyan")
                console.print()
                
                for i, message in enumerate(history[-10:], 1):  # Últimas 10 mensagens
                    sender = message.get('sender', 'unknown')
                    content = message.get('content', '')
                    timestamp = message.get('timestamp', '')
                    
                    if sender == 'user':
                        console.print(f"👤 Você: {content}", style="white")
                    elif sender == 'assistant':
                        console.print(f"🤖 Gabriel: {content}", style="cyan")
                    console.print()
            else:
                console.print("❌ Gabriel AI não está inicializado", style="red")
                
        except Exception as e:
            console.print(f"❌ Erro ao obter histórico: {e}", style="red")
    
    async def clear_history(self):
        """Limpa histórico da conversa"""
        try:
            if self.gabriel_ai:
                await self.gabriel_ai.clear_conversation_history(self.conversation_id)
                console.print("🧹 Histórico da conversa limpo!", style="green")
            else:
                console.print("❌ Gabriel AI não está inicializado", style="red")
                
        except Exception as e:
            console.print(f"❌ Erro ao limpar histórico: {e}", style="red")
    
    async def upload_file(self, file_path: str):
        """Faz upload e processa arquivo"""
        try:
            path = Path(file_path)
            
            if not path.exists():
                console.print(f"❌ Arquivo não encontrado: {file_path}", style="red")
                return
            
            console.print(f"📤 Processando arquivo: {path.name}...", style="cyan")
            
            # Processa arquivo
            result = await self.gabriel_ai.process_file(path)
            
            if result.get('error'):
                console.print(f"❌ Erro ao processar arquivo: {result['error']}", style="red")
            else:
                console.print(f"✅ Arquivo processado com sucesso!", style="green")
                
                # Mostra resumo
                file_type = result.get('file_type', 'unknown')
                word_count = result.get('word_count', 0)
                console.print(f"📄 Tipo: {file_type}, Palavras: {word_count}", style="yellow")
                
                # Se há texto extraído, mostra prévia
                if result.get('text'):
                    preview = result['text'][:200] + "..." if len(result['text']) > 200 else result['text']
                    console.print(f"📝 Prévia: {preview}", style="white")
                
        except Exception as e:
            console.print(f"❌ Erro no upload: {e}", style="red")
    
    async def process_message(self, message: str):
        """Processa mensagem do usuário"""
        try:
            console.print("🤖 Gabriel está pensando...", style="cyan")
            
            response = await self.gabriel_ai.process_message(
                message=message,
                conversation_id=self.conversation_id,
                message_type='text'
            )
            
            if response.get('error'):
                console.print(f"❌ Erro: {response['error']}", style="red")
            else:
                ai_response = response.get('response', 'Desculpe, não consegui processar sua mensagem.')
                console.print(f"🤖 Gabriel: {ai_response}", style="cyan")
                
                # Mostra análise se disponível
                if response.get('analysis'):
                    analysis = response['analysis']
                    if analysis.get('intent'):
                        console.print(f"💡 Intenção detectada: {analysis['intent']}", style="dim yellow")
                
        except Exception as e:
            console.print(f"❌ Erro ao processar mensagem: {e}", style="red")
    
    async def run(self):
        """Executa o bot no terminal"""
        self.show_welcome()
        
        # Inicializa componentes
        if not await self.initialize():
            console.print("❌ Falha na inicialização. Encerrando...", style="red")
            return
        
        console.print("\n💬 Digite sua mensagem (ou /help para ajuda):", style="bold green")
        
        # Loop principal
        while True:
            try:
                # Obtém input do usuário
                user_input = Prompt.ask("\n[bold blue]Você[/bold blue]").strip()
                
                if not user_input:
                    continue
                
                # Comandos especiais
                if user_input.lower() in ['/quit', '/exit']:
                    console.print("👋 Até logo!", style="cyan")
                    break
                
                elif user_input.lower() == '/help':
                    self.show_help()
                
                elif user_input.lower() == '/status':
                    await self.show_status()
                
                elif user_input.lower() == '/persona':
                    await self.show_persona()
                
                elif user_input.lower() == '/history':
                    await self.show_history()
                
                elif user_input.lower() == '/clear':
                    await self.clear_history()
                
                elif user_input.startswith('/upload '):
                    file_path = user_input[8:].strip()
                    await self.upload_file(file_path)
                
                else:
                    # Processa mensagem normal
                    await self.process_message(user_input)
                
            except KeyboardInterrupt:
                console.print("\n👋 Interrompido pelo usuário. Até logo!", style="yellow")
                break
            except Exception as e:
                console.print(f"❌ Erro inesperado: {e}", style="red")

async def main():
    """Função principal"""
    try:
        bot = TerminalBot()
        await bot.run()
    except Exception as e:
        console.print(f"❌ Erro fatal: {e}", style="red")

if __name__ == "__main__":
    asyncio.run(main())
