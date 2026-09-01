const AudioEngine = {
  playbackQueue: [],
  isPlaying: false,
  spokenPhrases: new Set(),

  playSynthesis: async (text) => {
    if (!text || text.trim() === '') return;

    // Deduplication check
    if (AudioEngine.spokenPhrases.has(text)) {
      console.log(`[TTS] Duplicate request ignored: "${text}"`);
      return;
    }

    AudioEngine.spokenPhrases.add(text);
    // Clear from deduplication cache after a while to allow playing again in future if needed
    setTimeout(() => {
      AudioEngine.spokenPhrases.delete(text);
    }, 10000); // 10 seconds deduplication window

    console.log(`[TTS] TTS request started for text: "${text}"`);
    AudioEngine.playbackQueue.push(text);
    
    if (!AudioEngine.isPlaying) {
      AudioEngine.processQueue();
    }
  },

  processQueue: async () => {
    if (AudioEngine.playbackQueue.length === 0) {
      AudioEngine.isPlaying = false;
      return;
    }

    AudioEngine.isPlaying = true;
    const text = AudioEngine.playbackQueue.shift();

    try {
      const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
      const response = await fetch(`${baseUrl}/api/speech/synthesize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      
      if (!response.ok) {
        throw new Error(`Failed to synthesize speech: ${response.status} ${response.statusText}`);
      }
      
      console.log(`[TTS] TTS response received for text: "${text}"`);
      
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      
      audio.onended = () => {
        URL.revokeObjectURL(url);
        // Play next in queue
        AudioEngine.processQueue();
      };
      
      audio.onerror = (e) => {
        console.error(`[TTS] audio playback failed for text: "${text}"`, e);
        URL.revokeObjectURL(url);
        // Continue queue on error
        AudioEngine.processQueue();
      };
      
      console.log(`[TTS] audio playback started for text: "${text}"`);
      await audio.play();
    } catch (error) {
      console.error(`[TTS] AudioEngine error for text: "${text}":`, error);
      // Ensure we don't get stuck if fetch fails
      AudioEngine.processQueue();
    }
  }
};

export default AudioEngine;
