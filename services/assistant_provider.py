import os

class AssistantProvider:
    async def chat(self, message: str, game_title: str | None = None, conversation_id: str | None = None):
        raise NotImplementedError

class MockAssistantProvider(AssistantProvider):
    async def chat(self, message: str, game_title: str | None = None, conversation_id: str | None = None):
        title_part = f" (jeu: {game_title})" if game_title else ""
        return {
            "reply": f"🤖 (mock){title_part} Tu as dit : {message}",
        }

def get_assistant_provider() -> AssistantProvider:
    # Plus tard sur VPS: tu changes juste ASSISTANT_PROVIDER=local_llm
    provider = os.getenv("ASSISTANT_PROVIDER", "mock").lower()

    if provider == "mock":
        return MockAssistantProvider()

    # Placeholder futur:
    # if provider == "local_llm": return LocalLLMProvider(...)
    # if provider == "remote": return RemoteProvider(...)
    return MockAssistantProvider()