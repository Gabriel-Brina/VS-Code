"""
Configurações do BotWith - Sistema SDR Automatizado
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class Config:
    """Classe de configuração centralizada"""
    
    def __init__(self):
        # Caminhos do projeto
        self.PROJECT_ROOT = Path(__file__).parent
        self.DATABASE_PATH = self.PROJECT_ROOT / "database"
        self.PERSONA_PATH = self.DATABASE_PATH / "persona"
        self.LOGS_PATH = self.PROJECT_ROOT / "logs"
        
        # Persona
        self.PERSONA_NAME = os.getenv("PERSONA_NAME", "Gabriel")
        self.PERSONA_ROLE = os.getenv("PERSONA_ROLE", "SDR Profissional")
        self.PERSONA_STYLE = os.getenv("PERSONA_STYLE", "Profissional e amigável")
        
        # AI Configuration
        self.AI_MODEL_NAME = os.getenv("AI_MODEL_NAME", "microsoft/DialoGPT-medium")
        self.MAX_TOKENS = int(os.getenv("MAX_TOKENS", "150"))
        self.TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
        
        # Database
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///database/botwith.db")
        
        # Clint Integration
        self.CLINT_API_URL = os.getenv("CLINT_API_URL", "https://api.clint.digital")
        self.CLINT_API_KEY = os.getenv("CLINT_API_KEY", "")
        self.CLINT_WEBHOOK_SECRET = os.getenv("CLINT_WEBHOOK_SECRET", "")
        
        # Server Configuration
        self.SERVER_URL = os.getenv("SERVER_URL", "http://localhost:8000")
        self.SEND_WELCOME_MESSAGE = os.getenv("SEND_WELCOME_MESSAGE", "true").lower() == "true"
        
        # Processing
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
        self.OVERLAP_SIZE = int(os.getenv("OVERLAP_SIZE", "200"))
        
        # Logging
        self.DEBUG = os.getenv("DEBUG", "false").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        
        # Setup directories
        self._setup_directories()
    
    def _setup_directories(self):
        """Cria diretórios necessários"""
        directories = [
            self.LOGS_PATH,
            self.DATABASE_PATH,
            self.PERSONA_PATH / "conversas",
            self.PERSONA_PATH / "documentos",
            self.PERSONA_PATH / "audios",
            self.PERSONA_PATH / "imagens"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

# Caminhos do projeto
PROJECT_ROOT = Path(__file__).parent
DATABASE_PATH = PROJECT_ROOT / "database"
PERSONA_PATH = DATABASE_PATH / "persona"
LOGS_PATH = PROJECT_ROOT / "logs"

# Configurações da Persona Gabriel
PERSONA_CONFIG = {
    "nome": "Gabriel",
    "empresa": "With Consultoria",
    "cargo": "SDR Especialista",
    "tom": "profissional_amigavel",
    "especialidades": ["automação de vendas", "CRM", "consultoria empresarial"],
    "saudacao_padrao": "Olá! Aqui é o Gabriel da With Consultoria.",
    "despedida_padrao": "Foi um prazer conversar! Estou à disposição."
}

# Configurações de IA
AI_CONFIG = {
    "modelo_texto": os.getenv("MODEL_TEXT", "microsoft/DialoGPT-medium"),
    "modelo_embeddings": os.getenv("MODEL_EMBEDDINGS", "sentence-transformers/all-MiniLM-L6-v2"),
    "modelo_audio": os.getenv("MODEL_AUDIO", "openai/whisper-base"),
    "modelo_imagem": os.getenv("MODEL_IMAGE", "microsoft/trocr-base-printed"),
    "max_tokens": int(os.getenv("MAX_TOKENS", "150")),
    "temperature": float(os.getenv("TEMPERATURE", "0.7")),
    "top_p": float(os.getenv("TOP_P", "0.9"))
}

# Configurações do Clint CRM
CLINT_CONFIG = {
    "api_url": os.getenv("CLINT_API_URL", "https://api.clint.digital/graphql"),
    "token": os.getenv("CLINT_TOKEN", ""),
    "webhook_url": os.getenv("CLINT_WEBHOOK_URL", ""),
    "timeout": int(os.getenv("CLINT_TIMEOUT", "30"))
}

# Configurações de Logging
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": LOGS_PATH / "botwith.log",
    "max_size": int(os.getenv("LOG_MAX_SIZE", "10485760")),  # 10MB
    "backup_count": int(os.getenv("LOG_BACKUP_COUNT", "5"))
}

# Configurações de Processamento
PROCESSING_CONFIG = {
    "max_file_size": int(os.getenv("MAX_FILE_SIZE", "52428800")),  # 50MB
    "supported_audio": [".mp3", ".wav", ".m4a", ".ogg", ".flac"],
    "supported_image": [".jpg", ".jpeg", ".png", ".bmp", ".tiff"],
    "supported_document": [".pdf", ".docx", ".txt", ".xlsx", ".csv"],
    "chunk_size": int(os.getenv("CHUNK_SIZE", "1000")),
    "overlap": int(os.getenv("OVERLAP", "200"))
}

def setup_logging():
    """Configura o sistema de logging"""
    LOGS_PATH.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG["level"]),
        format=LOGGING_CONFIG["format"],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG["file"]),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger("BotWith")

def validate_config():
    """Valida as configurações necessárias"""
    required_paths = [DATABASE_PATH, PERSONA_PATH, LOGS_PATH]
    
    for path in required_paths:
        path.mkdir(parents=True, exist_ok=True)
    
    logger = setup_logging()
    logger.info("🚀 BotWith configurado com sucesso!")
    
    return True

if __name__ == "__main__":
    validate_config()
