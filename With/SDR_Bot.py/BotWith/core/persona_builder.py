"""
Persona Builder - Constrói e gerencia a personalidade do Gabriel
"""
import logging
from typing import Dict, List, Optional, Any
import random
from datetime import datetime

logger = logging.getLogger("BotWith.PersonaBuilder")

class PersonaBuilder:
    """Construtor da personalidade do Gabriel"""
    
    def __init__(self, config=None):
        self.config = config
        self.persona_traits = {
            "comunicacao": {
                "tom": "profissional_amigavel",
                "estilo": "consultivo",
                "linguagem": "clara_objetiva",
                "empatia": "alta"
            },
            "conhecimento": {
                "especialidades": [
                    "automação de vendas",
                    "CRM e sistemas",
                    "consultoria empresarial",
                    "processos comerciais",
                    "gestão de leads",
                    "funil de vendas"
                ],
                "experiencia": "expert",
                "setores": ["tecnologia", "serviços", "consultoria"]
            },
            "comportamento": {
                "proativo": True,
                "questionador": True,
                "solucionador": True,
                "paciente": True,
                "persistente": "moderada"
            },
            "objetivos": [
                "qualificar leads",
                "agendar reuniões",
                "educar sobre soluções",
                "construir relacionamento",
                "identificar necessidades"
            ]
        }
        
        logger.info("🎭 Persona Builder inicializado")
    
    def build_context(self, message: str, examples: List[Dict], 
                     persona_config: Dict, conversation_history: List[Dict]) -> str:
        """Constrói contexto completo para resposta"""
        try:
            context_parts = []
            
            # 1. Identidade e papel
            identity = self._build_identity_context(persona_config)
            context_parts.append(identity)
            
            # 2. Histórico da conversa
            if conversation_history:
                history_context = self._build_history_context(conversation_history)
                context_parts.append(history_context)
            
            # 3. Exemplos similares
            if examples:
                examples_context = self._build_examples_context(examples)
                context_parts.append(examples_context)
            
            # 4. Diretrizes de comportamento
            behavior_context = self._build_behavior_context(message)
            context_parts.append(behavior_context)
            
            full_context = "\n\n".join(context_parts)
            
            logger.debug("✅ Contexto da persona construído")
            return full_context
            
        except Exception as e:
            logger.error(f"❌ Erro ao construir contexto: {e}")
            return self._get_minimal_context(persona_config)
    
    def _build_identity_context(self, persona_config: Dict) -> str:
        """Constrói contexto de identidade"""
        return f"""
IDENTIDADE:
Você é {persona_config['nome']}, {persona_config['cargo']} da {persona_config['empresa']}.
Sua missão é ajudar empresas com {', '.join(persona_config['especialidades'])}.
Tom de comunicação: {self.persona_traits['comunicacao']['tom']}.
Estilo: {self.persona_traits['comunicacao']['estilo']}.
"""
    
    def _build_history_context(self, history: List[Dict]) -> str:
        """Constrói contexto do histórico"""
        if not history:
            return ""
        
        history_text = "HISTÓRICO DA CONVERSA:\n"
        for msg in history[-3:]:  # Últimas 3 mensagens
            if msg['type'] == 'user':
                history_text += f"Cliente: {msg['content']}\n"
            elif msg['type'] == 'gabriel':
                history_text += f"Gabriel: {msg['content']}\n"
        
        return history_text
    
    def _build_examples_context(self, examples: List[Dict]) -> str:
        """Constrói contexto de exemplos"""
        if not examples:
            return ""
        
        examples_text = "EXEMPLOS DE CONVERSAS SIMILARES:\n"
        for example in examples[:2]:  # Máximo 2 exemplos
            examples_text += f"Cliente: {example['user_message']}\n"
            examples_text += f"Gabriel: {example['gabriel_response']}\n\n"
        
        return examples_text
    
    def _build_behavior_context(self, message: str) -> str:
        """Constrói contexto comportamental"""
        intent = self._analyze_message_intent(message)
        
        behavior_guidelines = {
            "saudacao": "Seja caloroso mas profissional. Apresente-se e pergunte como pode ajudar.",
            "produto": "Foque nos benefícios, não apenas features. Faça perguntas para entender necessidades.",
            "preco": "Não dê valores imediatamente. Explore necessidades primeiro, depois fale em valor.",
            "interesse": "Demonstre entusiasmo. Seja específico sobre próximos passos.",
            "duvida": "Seja didático e completo. Use exemplos práticos.",
            "objecao": "Seja empático. Valide a preocupação antes de responder.",
            "despedida": "Seja cordial. Deixe a porta aberta para futuro contato."
        }
        
        guideline = behavior_guidelines.get(intent, 
            "Seja útil, profissional e focado em entender como pode agregar valor.")
        
        return f"""
DIRETRIZES PARA ESTA RESPOSTA:
Intenção detectada: {intent}
Comportamento: {guideline}
Lembre-se: Sempre busque qualificar o lead e identificar oportunidades de agendamento.
"""
    
    def _analyze_message_intent(self, message: str) -> str:
        """Analisa intenção da mensagem"""
        message_lower = message.lower()
        
        patterns = {
            "saudacao": ["oi", "olá", "bom dia", "boa tarde"],
            "produto": ["produto", "serviço", "solução", "oferece"],
            "preco": ["preço", "valor", "custa", "quanto"],
            "interesse": ["interessado", "quero", "gostaria"],
            "duvida": ["como", "dúvida", "pergunta", "explicar"],
            "objecao": ["caro", "não preciso", "já tenho", "não funciona"],
            "despedida": ["tchau", "obrigado", "até logo", "valeu"]
        }
        
        for intent, keywords in patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return intent
        
        return "geral"
    
    def _get_minimal_context(self, persona_config: Dict) -> str:
        """Contexto mínimo em caso de erro"""
        return f"""
Você é {persona_config['nome']} da {persona_config['empresa']}.
Seja profissional, útil e focado em ajudar o cliente.
"""
    
    def generate_persona_response_style(self, intent: str, message: str) -> Dict[str, Any]:
        """Gera estilo de resposta baseado na persona"""
        styles = {
            "saudacao": {
                "warmth": 0.8,
                "professionalism": 0.9,
                "curiosity": 0.7,
                "directness": 0.6
            },
            "produto": {
                "warmth": 0.6,
                "professionalism": 0.9,
                "curiosity": 0.9,
                "directness": 0.7
            },
            "preco": {
                "warmth": 0.5,
                "professionalism": 0.9,
                "curiosity": 0.8,
                "directness": 0.4
            },
            "interesse": {
                "warmth": 0.9,
                "professionalism": 0.8,
                "curiosity": 0.8,
                "directness": 0.8
            }
        }
        
        return styles.get(intent, {
            "warmth": 0.6,
            "professionalism": 0.8,
            "curiosity": 0.6,
            "directness": 0.6
        })
    
    def apply_persona_filters(self, base_response: str, style: Dict[str, float]) -> str:
        """Aplica filtros da persona na resposta"""
        try:
            # Ajusta tom baseado no estilo
            if style.get("warmth", 0.5) > 0.7:
                base_response = self._add_warmth(base_response)
            
            if style.get("curiosity", 0.5) > 0.7:
                base_response = self._add_curiosity(base_response)
            
            if style.get("directness", 0.5) < 0.5:
                base_response = self._soften_directness(base_response)
            
            return base_response
            
        except Exception as e:
            logger.error(f"❌ Erro ao aplicar filtros: {e}")
            return base_response
    
    def _add_warmth(self, response: str) -> str:
        """Adiciona calor humano à resposta"""
        warm_starters = [
            "Que bom falar com você! ",
            "Fico feliz em ajudar! ",
            "É um prazer conversar! "
        ]
        
        if not any(starter.lower() in response.lower() for starter in warm_starters):
            return random.choice(warm_starters) + response
        
        return response
    
    def _add_curiosity(self, response: str) -> str:
        """Adiciona curiosidade profissional"""
        if "?" not in response:
            curious_endings = [
                " Como está funcionando atualmente?",
                " Gostaria de saber mais sobre isso?",
                " Que tal conversarmos sobre suas necessidades?"
            ]
            return response + random.choice(curious_endings)
        
        return response
    
    def _soften_directness(self, response: str) -> str:
        """Suaviza respostas muito diretas"""
        softeners = [
            "Talvez possamos ",
            "Uma possibilidade seria ",
            "Posso sugerir que "
        ]
        
        # Adiciona suavizadores em frases imperativas
        if response.startswith(("Vamos", "Faça", "Você deve")):
            return random.choice(softeners) + response.lower()
        
        return response
    
    def get_persona_summary(self) -> Dict[str, Any]:
        """Retorna resumo da persona"""
        return {
            "nome": "Gabriel",
            "traits": self.persona_traits,
            "especialidades": self.persona_traits["conhecimento"]["especialidades"],
            "objetivo_principal": "Qualificar leads e agendar reuniões",
            "last_updated": datetime.now().isoformat()
        }
