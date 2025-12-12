# SleepMoney

**SleepMoney** is a modular harness designed to empower an **AI Agent (IDE/CLI)** to orchestrate the entire production pipeline of long-form "sleepy" YouTube videos. No human intervention is required beyond the initial command—the AI Agent acts as the creative intelligence, while the Python harness handles the plumbing.

---

## 🏗️ Architecture

The system follows a 5-Stage Pipeline:

1.  **Discovery**: Analyzes niche competition (Mock/API).
2.  **Narrative Engine (Interactive)**: The Core Innovation.
    *   Instead of relying on low-quality automatic text generation, the harness pauses and **requests the Agent** to assume specific roles ("The Architect", "The Weaver") to author high-quality content via file I/O.
3.  **Assets**: Generates visual and audio assets (TTS, Images).
4.  **Assembly**: FFmpeg orchestration to render the final `.mp4`.
5.  **Distribution**: (Planned) Auto-upload to YouTube.

---

## 🚀 Quick Start

### 1. Installation
```bash
# Clone and enter directory
git clone sleepmoney
cd sleepmoney

# Install dependencies (requires ffmpeg installed on system)
pip install -r requirements.txt
```

### 2. Run the Harness (Agent Mode)
The harness is designed to be run **by an Agent**, but a human can simulate the agent's role.

**Step 1: Generate Content**
```bash
python main.py content --niche "Ancient Libraries"
```
*The system will pause and generate request files in `agent_interaction/requests/`. The Agent must read them and write responses to `agent_interaction/responses/`.*

**Step 2: Generate Assets & Assemble**
```bash
python main.py assets --script output/script_Ancient_Libraries.txt
python main.py assemble
```

---

## 🤖 Agent Interaction Protocol

**This is a "Human-in-the-Loop" architecture where *You* (The AI) are the Human.**

When the harness needs intelligence (e.g., structuring a narrative), it uses the **InteractiveClient**:
1.  **Request**: Harness writes `agent_interaction/requests/req_ID.md`.
2.  **Pause**: Harness waits for `agent_interaction/responses/resp_ID.md`.
3.  **Action**: You (The Agent) read the request, perform the creative task, write the response, and signal the harness to continue.

See [agent.md](agent.md) for detailed role instructions.

---

## 📂 Project Structure

- `src/discovery`: Niche finding logic.
- `src/content`: **Narrative Engine** & Fact Harvester.
    - `narrative_engine.py`: Orchestrates the Architect/Weaver workflow.
    - `prompts.py`: System prompts for the Agent.
- `src/assets`: Visuals (Greybox/Stable Diffusion) and Audio (TTS).
- `src/assembly`: FFmpeg video editor.
- `agent_interaction/`: The "Nerve Center" for Agent-Harness communication.
