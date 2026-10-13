# NEBULA Grounded AI Architecture

NEBULA provides a provider-agnostic, scientifically grounded artificial intelligence layer specifically designed to suppress hallucinations and adapt linguistic register across distinct user personas.

---

## 1. Provider-Agnostic AI Interface

The core AI service is decoupled from specific LLM vendors via an abstract interface:

```python
class AIServiceInterface(ABC):
    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        mode: str,
        grounding_context: str,
        history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        pass
```

### Supported Providers:
1. **Google Gemini (`GeminiProvider`)**: Uses `GEMINI_API_KEY` with low temperature ($0.3$) for researcher mode and standard temperature ($0.7$) for educational modes.
2. **OpenAI (`OpenAIProvider`)**: Uses `OPENAI_API_KEY` (compatible with `gpt-4o-mini`).
3. **Local Ollama (`OllamaProvider`)**: Uses `OLLAMA_BASE_URL` (`http://localhost:11434`) for local offline inference.
4. **Deterministic Knowledge Engine (`GroundedFallbackEngine`)**: Operates offline without external API keys, synthesizing responses from the local empirical catalog, orbital mechanics calculations, and persona guidelines.

---

## 2. Empirical Grounding Pipeline

To eliminate numerical hallucinations (e.g. inventing planetary masses or orbital distances), NEBULA implements a two-stage grounding pipeline in `backend/app/ai/grounding.py`:

```
User Query: "How long does it take to travel from Earth to Mars?"
                           │
                           ▼
              Entity & Context Scanner
   (Identifies Earth & Mars, triggers Hohmann transfer solver)
                           │
                           ▼
          Grounded Physics Extraction Block:
   - Earth: a = 1.0 AU, M = 5.972e24 kg
   - Mars: a = 1.524 AU, M = 6.417e23 kg
   - Hohmann Transfer: Total Delta-v = 5.596 km/s, Time = 258.9 days
                           │
                           ▼
             Persona Linguistic Injection
   (Researcher: LaTeX & mechanics / Student: Analogy / Citizen: Story)
                           │
                           ▼
           Persona-Adapted Grounded Output
```

Each generated response includes a `grounding_meta` payload verifying which empirical parameters were injected.

---

## 3. Persona Linguistic Directives

### 🔬 Researcher Persona
- **Role**: Senior Astrophysical Research Specialist
- **Tone**: Formal, analytical, quantitatively rigorous
- **Directives**: Must include exact physical units (SI, AU, solar units), explicit LaTeX mathematical notation ($...$ and $$...$$), secular perturbation mechanisms, and empirical data citations.

### 🎓 Student Persona
- **Role**: Interactive Astronomy & Physics Tutor
- **Tone**: Encouraging, structured, conceptually clear
- **Directives**: Explains fundamental laws (Kepler, Newton) using physical analogies; breaks down multi-step concepts; concludes with an engaging comprehension check question.

### 🌌 Citizen Persona
- **Role**: Planetarium Science Communicator
- **Tone**: Wonder-filled, accessible, conversational
- **Directives**: Uses plain English; relatable real-world scale comparisons (e.g., flight times, Earth weight); includes night sky viewing tips; strictly avoids mathematical jargon while preserving scientific truth.
