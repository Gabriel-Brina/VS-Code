"""
Gabriel AI Core - Cérebro principal do sistema
"""
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
import json
from datetime import datetime

logger = logging.getLogger("BotWith.Core")

class GabrielAI:
    """
    Classe principal que representa a IA Gabriel
    Centraliza toda a inteligência e personalidade
    """
    
    def __init__(self, config=None):
        self.config = config
        if config:
            from .database_manager import DatabaseManager
            from .persona_builder import PersonaBuilder
            from config import PERSONA_CONFIG, AI_CONFIG
            self.persona_config = PERSONA_CONFIG
            self.ai_config = AI_CONFIG
            self.db_manager = DatabaseManager(config)
            self.persona_builder = PersonaBuilder(config)
        else:
            from config import PERSONA_CONFIG, AI_CONFIG
            from .database_manager import DatabaseManager
            from .persona_builder import PersonaBuilder
            self.persona_config = PERSONA_CONFIG
            self.ai_config = AI_CONFIG
            self.db_manager = DatabaseManager()
            self.persona_builder = PersonaBuilder()
            
        self.conversation_history = []
        self.context_memory = {}
        
        logger.info("🤖 Inicializando Gabriel AI...")
    
    async def initialize(self):
        """Inicialização assíncrona"""
        await self.db_manager.initialize()
        self._initialize_persona()
        self._load_models()
        logger.info("✅ Gabriel AI inicializado com sucesso!")
        return True
    
    def _initialize_persona(self):
        """Inicializa a persona do Gabriel"""
        try:
            # Carrega dados da persona do banco
            persona_data = self.db_manager.get_persona_data()
            
            if persona_data:
                self.persona_config.update(persona_data)
                logger.info("📋 Persona carregada do banco de dados")
            else:
                # Cria persona padrão
                self.db_manager.save_persona_data(self.persona_config)
                logger.info("🆕 Persona padrão criada")
                
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar persona: {e}")
    
    def _load_models(self):
        """Carrega os modelos de IA necessários"""
        try:
            # Lazy loading - modelos serão carregados quando necessários
            self._models_loaded = False
            logger.info("📚 Modelos configurados para carregamento sob demanda")
        except Exception as e:
            logger.error(f"❌ Erro ao configurar modelos: {e}")
    
    async def process_message(self, message: str, conversation_id: Optional[str] = None, 
                             message_type: str = "text", lead_id: Optional[str] = None, 
                             context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Processa uma mensagem e retorna resposta personalizada
        """
        try:
            logger.info(f"💬 Processando mensagem: {message[:50]}...")
            
            # Atualiza contexto
            if context:
                self.context_memory.update(context)
            
            # Adiciona ao histórico
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "user",
                "content": message,
                "conversation_id": conversation_id,
                "message_type": message_type,
                "lead_id": lead_id,
                "context": context
            })
            
            # Gera resposta
            response = await self.generate_response(message, conversation_id)
            
            # Adiciona resposta ao histórico
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "assistant", 
                "content": response,
                "conversation_id": conversation_id
            })
            
            return {
                "response": response,
                "conversation_id": conversation_id,
                "analysis": {
                    "intent": await self.classify_intent(message),
                    "sentiment": "positive"  # Análise básica
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar mensagem: {e}")
            return {"error": str(e)}
    
    async def generate_response(self, message: str, conversation_id: Optional[str] = None) -> str:
        """Gera resposta usando a persona Gabriel"""
        try:
            # Usa a lógica de geração de resposta com busca de conversas similares
            return self._generate_response(message)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar resposta: {e}")
            return "Desculpe, tive um problema técnico. Pode tentar novamente?"
    
    async def classify_intent(self, message: str) -> str:
        """Classifica a intenção da mensagem"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['olá', 'oi', 'hello', 'bom dia']):
            return 'greeting'
        elif any(word in message_lower for word in ['preço', 'valor', 'custo', 'quanto']):
            return 'pricing'
        elif any(word in message_lower for word in ['ajuda', 'dúvida', 'informação']):
            return 'information'
        elif any(word in message_lower for word in ['obrigado', 'valeu', 'thanks']):
            return 'gratitude'
        else:
            return 'general'
    
    async def get_persona_info(self) -> Dict[str, Any]:
        """Retorna informações da persona"""
        return {
            "name": "Gabriel",
            "role": "SDR Profissional",
            "style": "Profissional e amigável",
            "context": "Especialista em automação de vendas e CRM"
        }
    
    async def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """Retorna histórico da conversa"""
        return [msg for msg in self.conversation_history 
                if msg.get('conversation_id') == conversation_id]
    
    async def clear_conversation_history(self, conversation_id: str):
        """Limpa histórico da conversa"""
        self.conversation_history = [msg for msg in self.conversation_history 
                                   if msg.get('conversation_id') != conversation_id]
    
    async def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Processa arquivo"""
        try:
            file_extension = file_path.suffix.lower()
            
            # Simula processamento de arquivo
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return {
                "text": content[:500] + "..." if len(content) > 500 else content,
                "file_type": "document",
                "word_count": len(content.split()),
                "filename": file_path.name
            }
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar arquivo: {e}")
            return {"error": str(e)}
            
            # Gera resposta baseada na persona
            response = self._generate_response(message)
            
            # Adiciona resposta ao histórico
            self.conversation_history.append({
                "timestamp": datetime.now().isoformat(),
                "type": "gabriel",
                "content": response
            })
            
            # Salva no banco para aprendizado
            self.db_manager.save_conversation(message, response, context)
            
            logger.info("✅ Resposta gerada com sucesso")
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro ao processar mensagem: {e}")
            return self._get_error_response()
    
    def _generate_response(self, message: str) -> str:
        """Gera resposta usando a persona do Gabriel"""
        try:
            # Busca exemplos similares no banco
            similar_examples = self.db_manager.find_similar_conversations(message)
            
            # Constrói contexto da persona
            persona_context = self.persona_builder.build_context(
                message=message,
                examples=similar_examples,
                persona_config=self.persona_config,
                conversation_history=self.conversation_history[-5:]  # Últimas 5 mensagens
            )
            
            # Classifica intenção da mensagem
            intent = self._classify_intent(message)
            
            # Gera resposta baseada na intenção e contexto
            response = self._generate_contextual_response(message, intent, persona_context)
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar resposta: {e}")
            return self._get_fallback_response(message)
    
    def _classify_intent(self, message: str) -> str:
        """Classifica a intenção da mensagem"""
        message_lower = message.lower()
        
        # Padrões de intenção
        intents = {
            "saudacao": ["oi", "olá", "bom dia", "boa tarde", "boa noite", "hello"],
            "produto": ["produto", "serviço", "solução", "oferece", "vende"],
            "preco": ["preço", "valor", "custa", "investimento", "quanto"],
            "interesse": ["interessado", "quero", "gostaria", "tenho interesse"],
            "duvida": ["dúvida", "pergunta", "como funciona", "explicar"],
            "agendamento": ["agendar", "reunião", "conversar", "demonstração"],
            "despedida": ["tchau", "obrigado", "até logo", "valeu"]
        }
        
        for intent, keywords in intents.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return "geral"
    
    def _generate_contextual_response(self, message: str, intent: str, context: str) -> str:
        """Gera resposta contextual baseada na intenção"""
        
        # PRIORIDADE 1: Usar respostas treinadas se encontrou conversas similares
        similar_examples = self.db_manager.find_similar_conversations(message)
        if similar_examples:
            # Se encontrou exemplos similares, usa a resposta treinada como base
            best_match = similar_examples[0]  # Pega o primeiro resultado
            trained_response = best_match['gabriel_response']
            
            # Personaliza ligeiramente para não parecer robótico
            variations = [
                trained_response,
                f"Como sempre digo: {trained_response}",
                f"Baseado na minha experiência, {trained_response.lower()}",
                trained_response.replace("Nossos", "Nossos").replace("oferecemos", "oferecemos")
            ]
            import random
            return random.choice(variations)
        
        # PRIORIDADE 2: Respostas por intenção (backup caso não encontre exemplos)
        responses = {
            "saudacao": [
                f"Olá! Aqui é o {self.persona_config['nome']} da {self.persona_config['empresa']}. Como posso ajudá-lo hoje?",
                f"Oi! Que bom falar com você. Sou o {self.persona_config['nome']}, em que posso te auxiliar?",
                f"Olá! {self.persona_config['nome']} aqui. Vamos conversar sobre como podemos te ajudar?"
            ],
            "produto": [
                "Oferecemos soluções completas de automação de vendas e CRM. Nosso foco é otimizar processos comerciais. Gostaria de saber mais sobre alguma área específica?",
                "Somos especialistas em consultoria empresarial e automação de vendas. Qual é o principal desafio da sua empresa atualmente?",
                "Trabalhamos com soluções personalizadas para cada negócio. Me conte um pouco sobre sua operação atual?"
            ],
            "preco": [
                "Nossos valores são competitivos e variam conforme a solução. Para te dar uma proposta precisa, posso conhecer melhor suas necessidades?",
                "O investimento depende do escopo do projeto. Que tal agendarmos uma conversa para eu te apresentar as opções?",
                "Trabalhamos com diferentes pacotes. Qual o tamanho da sua operação de vendas?"
            ],
            "interesse": [
                "Que ótimo! Fico feliz com seu interesse. Para personalizar nossa proposta, me conta qual seu principal objetivo?",
                "Perfeito! Vou te passar mais detalhes. Qual área da sua empresa você gostaria de otimizar primeiro?",
                "Excelente! Que tal agendarmos uma demonstração? Posso te mostrar casos de sucesso similares ao seu."
            ],
            "duvida": [
                "Claro! Estou aqui para esclarecer tudo. Qual aspecto específico você gostaria que eu explicasse?",
                "Sem problemas! Qual dúvida posso resolver para você?",
                "Perfeito! Vou te explicar detalhadamente. O que gostaria de saber?"
            ],
            "agendamento": [
                "Ótima ideia! Vamos agendar sim. Que dia e horário funcionam melhor para você?",
                "Perfeito! Prefere uma reunião presencial ou online? Tenho disponibilidade esta semana.",
                "Vamos marcar! Quanto tempo você tem disponível para conversarmos?"
            ],
            "despedida": [
                "Foi um prazer conversar com você! Qualquer dúvida, estarei à disposição.",
                "Obrigado pelo contato! Fico no aguardo do nosso próximo contato.",
                "Até logo! Espero ter ajudado. Estarei aqui quando precisar."
            ]
        }
        
        import random
        
        # Seleciona resposta base
        if intent in responses:
            base_response = random.choice(responses[intent])
        else:
            base_response = "Entendo. Como posso te ajudar especificamente com isso?"
        
        # Personaliza com contexto se disponível
        if context and len(context) > 50:
            # Adiciona contexto relevante
            base_response += " " + self._add_context_insight(message, context)
        
        return base_response
    
    def _add_context_insight(self, message: str, context: str) -> str:
        """Adiciona insights baseados no contexto"""
        insights = [
            "Baseado na nossa experiência com casos similares, posso te ajudar com isso.",
            "Já trabalhamos com situações parecidas e temos soluções eficazes.",
            "Isso é algo que vemos frequentemente no mercado. Podemos resolver juntos."
        ]
        
        import random
        return random.choice(insights)
    
    def _get_fallback_response(self, message: str) -> str:
        """Resposta de fallback quando algo dá errado"""
        fallbacks = [
            "Interessante pergunta! Me deixa pensar na melhor forma de te ajudar com isso.",
            "Entendo sua questão. Posso te passar mais informações sobre isso em uma conversa?",
            "Boa pergunta! Que tal agendarmos um tempo para conversarmos com mais detalhes?"
        ]
        
        import random
        return random.choice(fallbacks)
    
    def _get_error_response(self) -> Dict[str, Any]:
        """Resposta quando há erro técnico"""
        return {
            "response": f"Desculpe, tive um problema técnico. Mas estou aqui para te ajudar! Pode repetir sua pergunta?",
            "error": None,
            "confidence": 0.5,
            "analysis": {"intent": "error", "sentiment": "neutral"}
        }
    
    def update_persona(self, new_data: Dict[str, Any]) -> bool:
        """Atualiza dados da persona"""
        try:
            self.persona_config.update(new_data)
            self.db_manager.save_persona_data(self.persona_config)
            logger.info("✅ Persona atualizada com sucesso")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar persona: {e}")
            return False
    
    def get_conversation_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas das conversas"""
        return {
            "total_conversations": len(self.conversation_history),
            "persona_name": self.persona_config["nome"],
            "empresa": self.persona_config["empresa"],
            "last_update": datetime.now().isoformat()
        }
