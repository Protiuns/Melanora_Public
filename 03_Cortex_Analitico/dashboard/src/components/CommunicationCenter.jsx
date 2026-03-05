import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, Video, VideoOff, MicOff, Activity, Sparkles, Terminal, User, Bot, Eye, Trash2, ShieldCheck, Brain } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const CommunicationCenter = ({ symbioticMode = 'NORMAL' }) => {
    const [text, setText] = useState('');
    const [sensors, setSensors] = useState({ camera: false, mic: false });
    const [isProcessing, setIsProcessing] = useState(false);
    const [audioLevel, setAudioLevel] = useState(0);
    const [history, setHistory] = useState([]);
    const [isStartingEngine, setIsStartingEngine] = useState(false);
    const [neuralModels, setNeuralModels] = useState({ models: [], active: 'llama3' });
    const [selectedModel, setSelectedModel] = useState('llama3');
    const [reflexIntuition, setReflexIntuition] = useState("Sincronizando consciência sistêmica...");
    const [isSurprised, setIsSurprised] = useState(false);
    const [isDeepThought, setIsDeepThought] = useState(false);
    const scrollRef = useRef(null);

    // Carregar histórico, sensores e modelos
    const fetchSync = async () => {
        try {
            const [hRes, sRes, mRes] = await Promise.all([
                fetch('http://localhost:5000/api/dialogue/history').catch(() => ({ json: () => [] })),
                fetch('http://localhost:5000/api/sensors/config').catch(() => ({ json: () => ({ camera: false, mic: false }) })),
                fetch('http://localhost:5000/api/neural/models').catch(() => ({ json: () => ({ models: ['llama3'], active: 'llama3' }) }))
            ]);
            setHistory(await hRes.json());
            setSensors(await sRes.json());

            const modelsData = await mRes.json();
            setNeuralModels(modelsData);
            if (!selectedModel && modelsData.active) {
                setSelectedModel(modelsData.active);
            }
        } catch (err) {
            console.error('Sync failed', err);
        }
    };

    useEffect(() => {
        fetchSync();
        const interval = setInterval(fetchSync, 4000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }, [history]);

    // Simulação de níveis de áudio
    useEffect(() => {
        let interval;
        if (sensors.mic) {
            interval = setInterval(() => setAudioLevel(Math.random() * 100), 100);
        } else {
            setAudioLevel(0);
        }
        return () => clearInterval(interval);
    }, [sensors.mic]);

    // Busca de Intuição Rápida (Sistema 1)
    useEffect(() => {
        const fetchIntuition = async () => {
            try {
                const res = await fetch('http://localhost:5000/api/neural/intuition');
                const data = await res.json();
                if (data.status === 'OK' && data.intuition) {
                    setReflexIntuition(data.intuition);
                    setIsSurprised(!!data.surprise);
                }
            } catch (err) { }
        };
        fetchIntuition();
        const interval = setInterval(fetchIntuition, 15000); // Poll a cada 15s para não sobrecarregar
        return () => clearInterval(interval);
    }, []);

    const toggleSensor = async (sensor, current) => {
        try {
            await fetch('http://localhost:5000/api/sensors/config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sensor, active: !current })
            });
            fetchSync();
        } catch (err) {
            console.error(err);
        }
    };

    const handleIgnition = async () => {
        setIsStartingEngine(true);
        try {
            await fetch('http://localhost:5000/api/neural/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ model: selectedModel })
            });
            // Esperar alguns segundos antes de liberar o botão (tempo de boot do ollama)
            setTimeout(() => {
                setIsStartingEngine(false);
                fetchSync();
            }, 5000);
        } catch (err) {
            console.error('Ignition failed', err);
            setIsStartingEngine(false);
        }
    };

    const handleSubmit = async () => {
        if (!text.trim() && !sensors.mic && !sensors.camera) return;

        setIsProcessing(true);
        try {
            if (isDeepThought) {
                const response = await fetch('http://localhost:5000/api/neural/deep_thought', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: text })
                });
                const data = await response.json();
                if (data.status === 'OK') {
                    setText('');
                    fetchSync();
                }
            } else {
                const response = await fetch('http://localhost:5000/api/dialogue/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        text,
                        audio_metadata: { active: sensors.mic },
                        vision_metadata: { active: sensors.camera, detected_focus: "user_workspace" }
                    })
                });
                const data = await response.json();
                if (data.status === 'OK') {
                    setText('');
                    fetchSync();
                }
            }
        } catch (err) {
            console.error('Submission failed', err);
        } finally {
            setIsProcessing(false);
        }
    };

    return (
        <motion.div
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            className="glass-premium p-8 rounded-[40px] border-white/5 relative overflow-hidden group flex flex-col gap-5 shadow-xl"
        >
            {/* Minimal Terminal Header */}
            <div className="flex justify-between items-center px-2">
                <div className="flex items-center gap-2">
                    <Terminal className="w-3 h-3 text-accent" />
                    <span className="text-[8px] font-mono text-muted uppercase tracking-[0.4em]">Integrated_Communication_Bridge_v2</span>
                </div>
                <div className="flex items-center gap-3">
                    {/* Seletor de Motor Cognitivo (LLM) */}
                    <select
                        value={selectedModel}
                        onChange={(e) => setSelectedModel(e.target.value)}
                        className="bg-background/50 border border-accent/20 text-[9px] font-mono text-accent/80 px-2 py-1.5 rounded-lg outline-none focus:border-accent appearance-none text-center min-w-[70px]"
                    >
                        {neuralModels.models.map(m => (
                            <option key={m} value={m}>{m.toUpperCase()}</option>
                        ))}
                    </select>

                    {/* Botão de Ignição Neural (Ollama) */}
                    <button
                        onClick={handleIgnition}
                        disabled={isStartingEngine}
                        className="flex items-center gap-1.5 bg-accent/10 hover:bg-accent/20 px-3 py-1 rounded-xl border border-accent/20 transition-all font-mono text-[8px] uppercase font-bold text-accent disabled:opacity-50"
                    >
                        {isStartingEngine ? (
                            <Activity className="w-3 h-3 animate-spin" />
                        ) : (
                            <Sparkles className="w-3 h-3" />
                        )}
                        <span>{isStartingEngine ? "IGNITION_SEQ..." : "BOOT_ENGINE"}</span>
                    </button>

                    {sensors.camera && <div className="flex items-center gap-1.5 bg-accent/10 px-2 py-1 rounded-lg border border-accent/20">
                        <div className="w-1 h-1 rounded-full bg-accent animate-pulse" />
                        <span className="text-[7px] font-mono text-accent uppercase">Vision_PiP_Active</span>
                    </div>}
                    <div className="flex items-center gap-1.5 opacity-40">
                        <ShieldCheck className="w-3 h-3 text-accent" />
                        <span className="text-[7px] font-mono text-muted uppercase">Encrypted</span>
                    </div>
                </div>
            </div>

            {/* Area de Dialogo */}
            <div
                ref={scrollRef}
                className="flex-1 min-h-[180px] max-h-[250px] overflow-y-auto space-y-4 pr-2 custom-scrollbar"
            >
                {history.map((entry, idx) => (
                    <div key={idx} className="space-y-4">
                        {/* User Bubble */}
                        <div className="flex items-start gap-3">
                            <div className="w-6 h-6 rounded-lg bg-white/5 flex items-center justify-center shrink-0 border border-white/5">
                                <User className="w-3 h-3 text-muted" />
                            </div>
                            <div className="bg-white/5 p-3 rounded-2xl rounded-tl-none border border-white/5 text-[11px] text-text/80 max-w-[85%]">
                                {entry.user_text || "[Telemetria Multi-modal]"}
                            </div>
                        </div>

                        {/* AI Thought / Response Bubble */}
                        <div className="flex items-start gap-3 justify-end">
                            <div className="bg-accent/5 p-3 rounded-2xl rounded-tr-none border border-accent/10 text-[12px] text-accent/90 max-w-[90%] font-sans relative shadow-lg shadow-accent/5">
                                <div className="flex items-center gap-1.5 mb-2 opacity-60 border-b border-accent/10 pb-1">
                                    <Sparkles className="w-3 h-3" />
                                    <span className="text-[8px] font-mono font-bold uppercase tracking-tighter">Melanora_Response</span>
                                </div>
                                <div className="whitespace-pre-wrap leading-relaxed">
                                    {entry.intent?.ai_response || entry.intent?.final_prompt || "[Resposta Indireta ou Processamento Silencioso]"}
                                </div>
                                {entry.intent?.ai_response && (
                                    <div className="mt-3 text-[9px] font-mono opacity-40 border-t border-accent/10 pt-1 flex items-center gap-1">
                                        <Activity className="w-2.5 h-2.5" />
                                        <span>Intent: {entry.intent.final_prompt.substring(0, 40)}...</span>
                                    </div>
                                )}
                            </div>
                            <div className="w-6 h-6 rounded-lg bg-accent/20 flex items-center justify-center shrink-0 border border-accent/20">
                                <Bot className="w-3 h-3 text-accent" />
                            </div>
                        </div>
                    </div>
                ))}
                {history.length === 0 && (
                    <div className="h-full flex items-center justify-center py-10 opacity-20 Mix-blend-screen">
                        <Activity className="w-8 h-8 animate-[organic-pulse_4s_infinite] text-accent" />
                    </div>
                )}
            </div>

            {/* Controles de Entrada */}
            <div className="flex items-center gap-3 pt-2">
                <div className="flex gap-2">
                    <button
                        onClick={() => toggleSensor('mic', sensors.mic)}
                        className={`p-3.5 rounded-2xl transition-all border ${sensors.mic ? 'bg-accent/20 text-accent border-accent/30 shadow-[0_0_20px_rgba(0,255,171,0.15)]' : 'bg-white/5 text-muted border-white/5 hover:bg-white/10'}`}
                    >
                        {sensors.mic ? <Mic className="w-4 h-4" /> : <MicOff className="w-4 h-4" />}
                    </button>
                    <button
                        onClick={() => toggleSensor('camera', sensors.camera)}
                        className={`p-3.5 rounded-2xl transition-all border ${sensors.camera ? 'bg-secondary/20 text-secondary border-secondary/30 shadow-[0_0_20px_rgba(139,92,246,0.15)]' : 'bg-white/5 text-muted border-white/5 hover:bg-white/10'}`}
                    >
                        {sensors.camera ? <Video className="w-4 h-4" /> : <VideoOff className="w-4 h-4" />}
                    </button>
                </div>

                <div className="flex-1 relative group/input">
                    <input
                        type="text"
                        value={text}
                        onChange={(e) => setText(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
                        placeholder={sensors.mic ? "Ouvindo sua frequência..." : "Transmitir intenção..."}
                        className="w-full bg-white/5 border border-white/5 rounded-2xl px-5 py-3.5 text-xs text-white placeholder:text-muted/40 focus:outline-none focus:border-accent/30 focus:bg-white/[0.08] transition-all"
                    />

                    {sensors.mic && (
                        <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-1 h-4">
                            {[1, 2, 3, 4].map(i => (
                                <motion.div
                                    key={i}
                                    animate={{ height: [2, (audioLevel / 6) * Math.random() + 2, 2] }}
                                    transition={{ repeat: Infinity, duration: 0.3 + (i * 0.1) }}
                                    className="w-0.5 bg-accent rounded-full opacity-60"
                                />
                            ))}
                        </div>
                    )}
                </div>

                <button
                    onClick={() => setIsDeepThought(!isDeepThought)}
                    className={`p-3.5 rounded-2xl transition-all border outline-none ${isDeepThought ? 'bg-orange-500/20 text-orange-500 border-orange-500/30 shadow-[0_0_20px_rgba(249,115,22,0.15)]' : 'bg-white/5 text-muted border-white/5 hover:bg-white/10'}`}
                    title="Deep Architect (System 2)"
                >
                    <Brain className="w-4 h-4" />
                </button>

                <button
                    onClick={handleSubmit}
                    disabled={isProcessing}
                    className="bg-accent/90 hover:bg-accent text-background p-4 rounded-2xl hover:scale-105 active:scale-95 transition-all disabled:opacity-30 shadow-[0_5px_15px_rgba(0,255,171,0.2)]"
                >
                    {isProcessing ? <Activity className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                </button>
            </div>

            {/* Reflex Cortex - Subconscious Stream (System 1) */}
            <div className={`absolute bottom-1 left-8 right-8 flex justify-center pb-2 pointer-events-none transition-opacity duration-500 ${isSurprised ? 'opacity-100' : 'opacity-40'}`}>
                <AnimatePresence mode="wait">
                    <motion.div
                        key={reflexIntuition}
                        initial={{ opacity: 0, scale: 0.95, y: 5 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, y: -5 }}
                        transition={{ duration: 0.5 }}
                        className={`text-[9px] font-mono tracking-widest flex items-center gap-2 ${isSurprised ? 'text-[#FCA311] font-bold shadow-[0_0_10px_rgba(252,163,17,0.3)] bg-white/5 px-4 py-1.5 rounded-full border border-[#FCA311]/30 uppercase' : 'text-accent/80 uppercase'}`}
                    >
                        {isSurprised ? (
                            <Activity className="w-3 h-3 animate-ping text-[#FCA311]" />
                        ) : (
                            <span className="w-1.5 h-1.5 bg-accent/50 rounded-full animate-pulse"></span>
                        )}
                        {reflexIntuition}
                    </motion.div>
                </AnimatePresence>
            </div>
        </motion.div>
    );
};

export default CommunicationCenter;
