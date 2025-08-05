"""
Database Manager - Gerencia todo o banco de dados da persona
"""
import sqlite3
import json
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime
import hashlib

logger = logging.getLogger("BotWith.Database")

class DatabaseManager:
    """Gerenciador do banco de dados do Gabriel"""
    
    def __init__(self, config=None):
        if config:
            self.db_path = Path(config.DATABASE_URL.replace("sqlite:///", ""))
        else:
            from config import DATABASE_PATH
            self.db_path = DATABASE_PATH / "gabriel_brain.db"
            
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        logger.info("🗃️ Database Manager inicializado")
    
    async def initialize(self):
        """Método de inicialização assíncrono"""
        logger.info("✅ Database inicializado")
        return True
    
    def _init_database(self):
        """Inicializa as tabelas do banco de dados"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tabela da persona
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS persona_config (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        key TEXT UNIQUE NOT NULL,
                        value TEXT NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de conversas
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_message TEXT NOT NULL,
                        gabriel_response TEXT NOT NULL,
                        context TEXT,
                        intent TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        message_hash TEXT UNIQUE
                    )
                ''')
                
                # Tabela de documentos processados
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS documents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        file_type TEXT NOT NULL,
                        content TEXT NOT NULL,
                        summary TEXT,
                        keywords TEXT,
                        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        file_hash TEXT UNIQUE
                    )
                ''')
                
                # Tabela de embeddings para busca semântica
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS embeddings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL,
                        embedding BLOB NOT NULL,
                        source_type TEXT NOT NULL,
                        source_id INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Tabela de contexto e memória
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memory_context (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        context_key TEXT NOT NULL,
                        context_value TEXT NOT NULL,
                        importance_score REAL DEFAULT 1.0,
                        last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                logger.info("✅ Banco de dados inicializado com sucesso")
                
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar banco: {e}")
            raise
    
    def save_persona_data(self, persona_config: Dict[str, Any]) -> bool:
        """Salva configurações da persona"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for key, value in persona_config.items():
                    cursor.execute('''
                        INSERT OR REPLACE INTO persona_config (key, value)
                        VALUES (?, ?)
                    ''', (key, json.dumps(value)))
                
                conn.commit()
                logger.info("✅ Persona salva no banco")
                return True
                
        except Exception as e:
            logger.error(f"❌ Erro ao salvar persona: {e}")
            return False
    
    def get_persona_data(self) -> Optional[Dict[str, Any]]:
        """Recupera configurações da persona"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT key, value FROM persona_config')
                
                data = {}
                for key, value in cursor.fetchall():
                    try:
                        data[key] = json.loads(value)
                    except json.JSONDecodeError:
                        data[key] = value
                
                return data if data else None
                
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar persona: {e}")
            return None
    
    def save_conversation(self, user_message: str, gabriel_response: str, 
                         context: Optional[Dict] = None, intent: str = "geral") -> bool:
        """Salva uma conversa no banco"""
        try:
            # Cria hash da mensagem para evitar duplicatas
            message_hash = hashlib.md5(
                (user_message + gabriel_response).encode()
            ).hexdigest()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO conversations 
                    (user_message, gabriel_response, context, intent, message_hash)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    user_message,
                    gabriel_response,
                    json.dumps(context) if context else None,
                    intent,
                    message_hash
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"❌ Erro ao salvar conversa: {e}")
            return False
    
    def find_similar_conversations(self, message: str, limit: int = 5) -> List[Dict]:
        """Encontra conversas similares (busca simples por palavras-chave)"""
        try:
            # Extrai palavras-chave da mensagem
            keywords = self._extract_keywords(message)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Busca por similaridade simples
                query = '''
                    SELECT user_message, gabriel_response, context, intent
                    FROM conversations
                    WHERE ''' + ' OR '.join([
                        'user_message LIKE ?'
                        for _ in keywords
                    ]) + '''
                    ORDER BY timestamp DESC
                    LIMIT ?
                '''
                
                params = [f'%{keyword}%' for keyword in keywords] + [limit]
                cursor.execute(query, params)
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        'user_message': row[0],
                        'gabriel_response': row[1],
                        'context': json.loads(row[2]) if row[2] else None,
                        'intent': row[3]
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"❌ Erro ao buscar conversas similares: {e}")
            return []
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrai palavras-chave básicas do texto"""
        # Remove palavras comuns
        stop_words = {
            'o', 'a', 'e', 'é', 'de', 'do', 'da', 'em', 'um', 'uma', 'para',
            'com', 'não', 'na', 'no', 'se', 'que', 'por', 'mais', 'como',
            'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua',
            'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está',
            'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela',
            'entre', 'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus',
            'suas', 'numa', 'pelos', 'pelas', 'sobre', 'pela', 'ante'
        }
        
        words = text.lower().split()
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        return keywords[:10]  # Limita a 10 palavras-chave
    
    def save_document(self, filename: str, file_type: str, content: str,
                     summary: str = "", keywords: str = "") -> bool:
        """Salva documento processado"""
        try:
            file_hash = hashlib.md5(content.encode()).hexdigest()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO documents
                    (filename, file_type, content, summary, keywords, file_hash)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (filename, file_type, content, summary, keywords, file_hash))
                
                conn.commit()
                logger.info(f"✅ Documento {filename} salvo no banco")
                return True
                
        except Exception as e:
            logger.error(f"❌ Erro ao salvar documento: {e}")
            return False
    
    def get_all_documents(self) -> List[Dict]:
        """Recupera todos os documentos"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT filename, file_type, content, summary, keywords, processed_at
                    FROM documents
                    ORDER BY processed_at DESC
                ''')
                
                documents = []
                for row in cursor.fetchall():
                    documents.append({
                        'filename': row[0],
                        'file_type': row[1],
                        'content': row[2],
                        'summary': row[3],
                        'keywords': row[4],
                        'processed_at': row[5]
                    })
                
                return documents
                
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar documentos: {e}")
            return []
    
    def save_memory_context(self, context_key: str, context_value: str, 
                           importance: float = 1.0) -> bool:
        """Salva contexto na memória"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO memory_context
                    (context_key, context_value, importance_score)
                    VALUES (?, ?, ?)
                ''', (context_key, context_value, importance))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"❌ Erro ao salvar contexto: {e}")
            return False
    

    
    async def get_conversation_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas do banco"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total de conversas
                cursor.execute('SELECT COUNT(*) FROM conversations')
                total_conversations = cursor.fetchone()[0]
                
                # Última conversa
                cursor.execute('''
                    SELECT user_message, timestamp 
                    FROM conversations 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                ''')
                last_conv = cursor.fetchone()
                last_conversation = last_conv[1] if last_conv else "Nenhuma"
                
                # Top intents
                cursor.execute('''
                    SELECT intent, COUNT(*) as count
                    FROM conversations 
                    WHERE intent IS NOT NULL AND intent != ''
                    GROUP BY intent 
                    ORDER BY count DESC
                    LIMIT 5
                ''')
                top_intents = [f"{intent} ({count})" for intent, count in cursor.fetchall()]
                
                return {
                    'total_conversations': total_conversations,
                    'last_conversation': last_conversation,
                    'top_intents': top_intents
                }
                
        except Exception as e:
            logger.error(f"❌ Erro ao obter estatísticas: {e}")
            return {}
