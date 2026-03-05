import React, { useState } from 'react';
import { Eye, Maximize2, ShieldCheck, Activity, Monitor, Camera, MousePointer2, Type } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const VisionFeed = () => {
    const [error, setError] = useState(false);
    const [source, setSource] = useState('WEBCAM');
    const [isMotorActive, setIsMotorActive] = useState(false);
    const [isKeyboardActive, setIsKeyboardActive] = useState(false);
    const [keyboardText, setKeyboardText] = useState('');
    const containerRef = React.useRef(null);

    const toggleSource = async () => {
        const next = source === 'WEBCAM' ? 'SCREEN' : 'WEBCAM';
        try {
            await fetch('http://localhost:5000/api/vision/source', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ source: next })
            });
            setSource(next);
            setError(false);
        } catch (e) { console.error(e); }
    };

    const handleMotorAction = async (e) => {
        if (!isMotorActive || source !== 'SCREEN') return;

        const rect = containerRef.current.getBoundingClientRect();
        const clientX = e.clientX || (e.touches && e.touches[0].clientX);
        const clientY = e.clientY || (e.touches && e.touches[0].clientY);

        const x = (clientX - rect.left) / rect.width;
        const y = (clientY - rect.top) / rect.height;

        try {
            await fetch('http://localhost:5000/api/motor/mouse', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: 'click', x, y })
            });
        } catch (err) { console.error(err); }
    };

    const handleKeyboardSubmit = async () => {
        if (!keyboardText) return;
        try {
            await fetch('http://localhost:5000/api/motor/keyboard', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: keyboardText })
            });
            setKeyboardText('');
            setIsKeyboardActive(false);
        } catch (err) { console.error(err); }
    };

    return (
        <div className="glass rounded-[32px] overflow-hidden border border-white/5 relative group h-[300px] hover:border-accent/20 transition-all duration-500">
            {/* Header HUD */}
            <div className="absolute top-0 inset-x-0 p-4 flex justify-between items-center z-10 bg-gradient-to-b from-black/80 to-transparent">
                <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full animate-pulse ${source === 'SCREEN' ? 'bg-secondary' : 'bg-accent'}`} />
                    <span className="text-[10px] font-mono text-text uppercase tracking-widest flex items-center gap-1">
                        <Eye className="w-3 h-3" /> {source === 'SCREEN' ? 'Observer_Screen' : 'Live_Perception'}
                    </span>
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={toggleSource}
                        className="text-[8px] font-mono text-white/70 bg-white/5 hover:bg-white/10 px-2 py-0.5 rounded border border-white/10 flex items-center gap-1 transition-all"
                    >
                        {source === 'WEBCAM' ? <Monitor className="w-2.5 h-2.5" /> : <Camera className="w-2.5 h-2.5" />}
                        {source === 'WEBCAM' ? 'SWITCH_TO_SCREEN' : 'SWITCH_TO_CAM'}
                    </button>
                    <Maximize2 className="w-3 h-3 text-muted hover:text-accent cursor-pointer transition-colors" />
                </div>
            </div>

            {/* Main Stream Container */}
            <div
                ref={containerRef}
                className="relative w-full h-full bg-black/40 flex items-center justify-center cursor-crosshair"
                onMouseDown={handleMotorAction}
                onTouchStart={handleMotorAction}
            >
                {!error ? (
                    <img
                        src={`http://localhost:5000/api/vision/stream?t=${Date.now()}`}
                        alt="Neural Perception Feed"
                        className="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition-opacity duration-700"
                        onError={() => setError(true)}
                    />
                ) : (
                    <div className="flex flex-col items-center gap-2 text-muted">
                        <Activity className="w-8 h-8 opacity-20" />
                        <span className="text-[10px] font-mono uppercase tracking-tighter">Sensor_Offline_Or_Busy</span>
                    </div>
                )}

                {/* Motor Overlay Link */}
                {source === 'SCREEN' && (
                    <div className="absolute top-16 right-4 flex flex-col gap-2 z-20">
                        <button
                            onClick={() => setIsMotorActive(!isMotorActive)}
                            className={`p-2 rounded-xl border transition-all ${isMotorActive ? 'bg-accent/20 text-accent border-accent/40 shadow-[0_0_15px_rgba(0,255,171,0.2)]' : 'bg-black/40 text-white/40 border-white/10'}`}
                            title="Interactive Motor Link"
                        >
                            <MousePointer2 className="w-4 h-4" />
                        </button>
                        <button
                            onClick={() => setIsKeyboardActive(!isKeyboardActive)}
                            className={`p-2 rounded-xl border transition-all ${isKeyboardActive ? 'bg-secondary/20 text-secondary border-secondary/40' : 'bg-black/40 text-white/40 border-white/10'}`}
                            title="Virtual Keyboard Link"
                        >
                            <Type className="w-4 h-4" />
                        </button>
                    </div>
                )}

                {/* Virtual Keyboard Input */}
                <AnimatePresence>
                    {isKeyboardActive && (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: 10 }}
                            className="absolute bottom-16 inset-x-4 z-30"
                        >
                            <div className="glass p-2 rounded-2xl border border-secondary/20 flex gap-2">
                                <input
                                    type="text"
                                    autoFocus
                                    value={keyboardText}
                                    onChange={(e) => setKeyboardText(e.target.value)}
                                    onKeyDown={(e) => e.key === 'Enter' && handleKeyboardSubmit()}
                                    placeholder="Neural Type Payload..."
                                    className="flex-1 bg-white/5 border-none outline-none px-3 py-2 text-xs rounded-xl"
                                />
                                <button
                                    onClick={handleKeyboardSubmit}
                                    className="bg-secondary/20 text-secondary px-4 rounded-xl text-[10px] font-bold"
                                >
                                    SEND
                                </button>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Scanline Animation */}
                <div className="absolute inset-0 pointer-events-none overflow-hidden">
                    <motion.div
                        className="w-full h-[2px] bg-accent/20 shadow-[0_0_15px_#00FFAB]"
                        animate={{ top: ['0%', '100%', '0%'] }}
                        transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
                        style={{ position: 'absolute' }}
                    />
                </div>

                {/* Crosshair HUD Overlay */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                    <div className="w-32 h-32 border border-accent/10 rounded-full flex items-center justify-center">
                        <div className="w-0.5 h-4 bg-accent/20 absolute top-0" />
                        <div className="w-0.5 h-4 bg-accent/20 absolute bottom-0" />
                        <div className="w-4 h-0.5 bg-accent/20 absolute left-0" />
                        <div className="w-4 h-0.5 bg-accent/20 absolute right-0" />
                    </div>
                </div>

                {/* Dynamic Telemetry Corner */}
                <div className="absolute bottom-4 left-4 z-10 flex flex-col">
                    <div className="flex items-center gap-2 mb-1">
                        <ShieldCheck className="w-3 h-3 text-accent" />
                        <span className="text-[8px] font-mono text-muted uppercase">Object_Analysis_Active</span>
                    </div>
                    <div className="h-1 w-24 bg-white/5 rounded-full overflow-hidden">
                        <motion.div
                            className="h-full bg-accent"
                            animate={{ width: ['20%', '90%', '45%', '70%'] }}
                            transition={{ duration: 5, repeat: Infinity }}
                        />
                    </div>
                </div>
            </div>

            {/* Aesthetic Border Glitch for High Stress (handled via CSS variables) */}
            <div className="absolute inset-0 border-2 border-accent/0 group-hover:border-accent/5 pointer-events-none transition-all duration-300" />
        </div>
    );
};

export default VisionFeed;
