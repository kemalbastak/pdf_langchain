from langchain_google_genai import ChatGoogleGenerativeAI
from apps.core.settings import settings
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain_core.messages.ai import AIMessage
from apps.es.elasticsearch_logger import logger


class GeminiChat:
    def __init__(self,
                 model: str = settings.LLM_MODEL,
                 temperature: float = 0,
                 max_tokens: int = None,
                 timeout: int = None,
                 max_retries: int = 2
                 ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.max_retries = max_retries
        try:
            self.llm = ChatGoogleGenerativeAI(model=self.model,
                                              temperature=self.temperature,
                                              max_tokens=self.max_tokens,
                                              stream=False,
                                              timeout=self.timeout,
                                              max_retries=self.max_retries)
        except Exception as e:
            logger.error(f"Failed to initialize GeminiChat with model {self.model}: {e}")
            raise  # Re-raise the exception after logging
        self.__is_sendable = False

    def construct_prompt(self, content: str, message: str):
        try:
            human_message = f"<content>{content}</content>\n\n{message}"
            self.__messages = [
                SystemMessage(content=settings.SYSTEM_PROMPT),
                HumanMessage(content=human_message),
            ]
            self.__is_sendable = True
            return self
        except Exception as e:
            logger.error(f"Error constructing prompt for message: {message}. Error: {e}")
            raise  # Re-raise the exception after logging

    def get_response(self) -> AIMessage:
        if not self.__is_sendable or not self.__messages:
            error_message = "Message is not sendable. Please call instance.construct_prompt(content, message) first"
            logger.error(error_message)
            raise Exception(error_message)

        try:
            response = self.llm.invoke(self.__messages)
            return response
        except Exception as e:
            logger.error(f"Error getting response from Gemini service: {e}")
            raise  # Re-raise the exception after logging
