# Final Integration and Speech Capabilities Roadmap

This document outlines the final steps required to fully wire up the ALFRED frontend to the actual backend, details the API keys/dependencies needed from the user, and provides the implementation plan for local Speech-to-Text (STT) and Text-to-Speech (TTS). 

Completing the steps outlined below represents the final milestone. Once these are done, ALFRED is fully operational.

---

## 1. Frontend-Backend Connection (Replacing Mocks)

Currently, the ALFRED frontend is running on a mocked API (`frontend/src/services/mockApi.js`). The backend (running on FastAPI at port 8000) is already implemented but not yet receiving frontend traffic.

### What is left to do:
1. **Swap the API Service:**
   - In the React components (e.g., `Workspace.jsx`, `GoalInput.jsx`), replace imports from `mockApi.js` with the real `api.js`.
   - Ensure the `VITE_API_BASE_URL` in `frontend/.env.local` is set to `http://localhost:8000`.

2. **Wire up Server-Sent Events (SSE):**
   - The backend streams real-time execution logs via the `/api/tasks/{task_id}/events` endpoint. 
   - The frontend's `ExecutionTimeline.jsx` and `Workspace.jsx` must subscribe to this EventSource and append events (planning, tool execution, approvals) to the UI in real-time.

3. **Wire up Approvals:**
   - The `ApprovalPanel.jsx` needs to call `POST /api/tasks/{task_id}/approve` and `POST /api/tasks/{task_id}/reject` when the user clicks the respective buttons.
   - Upon approval, the SSE stream will resume and the UI will continue updating.

---

## 2. Required Configurations & API Keys

To power the backend agent, we need you (the user) to provide a `.env` file in the `backend/` directory with the following keys.

**Required from User:**
1. **LLM Provider Key:** `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` (depending on the agent's LLM engine). ALFRED needs this for its Planner and Executor modules.
2. **Search API Key (Optional but recommended):** `SERPAPI_API_KEY` or `TAVILY_API_KEY` if the agent uses web search tools.
3. **Blockchain RPC URL (If applicable):** If the agent interacts with smart contracts or crypto (as seen in the finance tool), an `INFURA_API_KEY` or `ALCHEMY_API_KEY` may be required, along with a secure `WALLET_PRIVATE_KEY` for ALFRED to sign transactions.

---

## 3. Speech-to-Text (STT) Implementation

**Tool:** `faster-whisper` (https://github.com/SYSTRAN/faster-whisper)
**Feasibility:** Highly Feasible. `faster-whisper` is incredibly fast, entirely local, and perfect for this use case.

### Implementation Plan:
1. **Frontend:** 
   - Add a microphone icon to `GoalInput.jsx`.
   - Use the browser's `MediaRecorder` API to capture audio when the user holds the microphone button.
   - Send the recorded audio (`.webm` or `.wav` blob) via a `multipart/form-data` POST request to a new backend endpoint: `/api/speech/transcribe`.
2. **Backend:**
   - Add `faster-whisper` to `backend/requirements.txt`.
   - Create the `/api/speech/transcribe` endpoint in `main.py`.
   - The endpoint will load a small, fast model (e.g., `tiny.en` or `base.en`), transcribe the audio blob, and return the raw text.
3. **Integration:** 
   - The frontend will take the returned text and automatically populate the Goal input field.

---

## 4. Text-to-Speech (TTS) Implementation

**Tool:** `piper` (https://github.com/OHF-Voice/piper1-gpl / https://github.com/rhasspy/piper)
**Feasibility:** Highly Feasible. Piper runs entirely locally via ONNX models, requires no GPU, and has very low latency, making ALFRED sound responsive and robotic/technical as desired.

### Implementation Plan:
1. **Backend:**
   - Install the `piper-tts` python package or download the Piper binary.
   - Download a high-quality ONNX voice model (e.g., a crisp, neutral English voice).
   - Create a `/api/speech/synthesize` endpoint. When called with text, the backend runs Piper to generate a `.wav` file in-memory and streams it back to the client.
2. **Frontend:**
   - Introduce an `AudioEngine.js` utility on the frontend.
   - Whenever ALFRED completes a major milestone (e.g., "Plan Generated", "Approval Required", "Task Complete"), the frontend will hit the `/api/speech/synthesize` endpoint.
   - The browser will play the returned audio buffer, giving ALFRED a voice.
3. **Voice Design:** 
   - We will select a voice model that fits the "System Interface / Retro-futuristic" aesthetic. A slightly synthetic, calm, and highly articulate voice is recommended over an overly expressive human voice.

---

## Conclusion

Once you have provided the necessary API keys and we execute the code changes outlined in this document, the ALFRED system will be **100% complete**. 

**Next Action:** 
Review this document. When you are ready, provide the API keys, confirm the speech requirements, and instruct me to **"Execute the final integration plan"**.
