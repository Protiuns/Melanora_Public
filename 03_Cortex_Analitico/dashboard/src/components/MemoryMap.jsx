import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Database, Search, Link2, FileText, ChevronRight, X } from 'lucide-react';

const MemoryMap = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [isSearching, setIsSearching] = useState(false);
    const [activeDoc, setActiveDoc] = useState(null);

    const handleSearch = async (e) => {
        if (e) e.preventDefault();
        if (!query.trim()) return;

        setIsSearching(true);
        try {
            const res = await fetch(`http://localhost:5000/api/memory/search?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            setResults(data);
        } catch (err) {
            console.error("Erro na busca semântica:", err);
        } finally {
            setIsSearching(false);
        }
    };

    return (
        <div className="glass-premium p-8 rounded-[40px] border-white/5 relative overflow-hidden group h-full">
            <div className="flex justify-between items-center mb-8">
                <div>
                    <h3 className="text-[10px] font-mono text-muted uppercase tracking-[0.4em] mb-1">Memória Semântica</h3>
                    <p className="text-sm text-white font-bold tracking-tight">THE_GREAT_CONNECTOME</p>
                </div>
                <Database className="w-5 h-5 text-accent" />
            </div>

            <form onSubmit={handleSearch} className="relative mb-8">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Pesquisar conceitos ou fragmentos..."
                    className="w-full bg-white/5 border border-white/10 rounded-2xl py-4 px-6 text-sm text-white placeholder:text-muted/50 focus:outline-none focus:border-accent/40 transition-all font-mono"
                />
                <button
                    type="submit"
                    className="absolute right-3 top-2.5 p-2 rounded-xl bg-accent/10 text-accent hover:bg-accent/20 transition-all"
                >
                    {isSearching ? <div className="w-4 h-4 border-2 border-accent border-t-transparent rounded-full animate-spin" /> : <Search className="w-4 h-4" />}
                </button>
            </form>

            <div className="space-y-4 max-h-[300px] overflow-y-auto custom-scrollbar pr-2">
                <AnimatePresence mode="popLayout">
                    {results.length > 0 ? (
                        results.map((res, idx) => (
                            <motion.div
                                key={res.id}
                                initial={{ opacity: 0, x: -20 }}
                                animate={{ opacity: 1, x: 0 }}
                                exit={{ opacity: 0, x: 20 }}
                                transition={{ delay: idx * 0.05 }}
                                onClick={() => setActiveDoc(res)}
                                className={`
                                    relative overflow-hidden group
                                    glass border border-white/5 rounded-[32px] p-6
                                    hover:border-accent/30 transition-all duration-500
                                    hover:shadow-[0_0_30px_rgba(252,163,17,0.1)]
                                    group/item flex items-start gap-4
                                `}
                            >
                                <div className="w-10 h-10 rounded-xl bg-accent/5 flex items-center justify-center shrink-0 group-hover/item:bg-accent/10 transition-all">
                                    <FileText className="w-4 h-4 text-accent/60 group-hover/item:text-accent" />
                                </div>
                                <div className="flex-1 overflow-hidden text-left">
                                    <div className="flex justify-between items-center mb-1">
                                        <span className="text-[10px] font-mono text-accent/60 uppercase tracking-widest">
                                            Doc #{res.id} • Score: {res.score}
                                        </span>
                                        <Link2 className="w-3 h-3 text-muted/30 group-hover/item:text-accent/40 transition-all" />
                                    </div>
                                    <p className="text-xs text-text/80 leading-relaxed line-clamp-2 italic">
                                        "{res.text}"
                                    </p>
                                    <div className="mt-2 flex items-center gap-2">
                                        <span className="text-[9px] font-mono text-muted/40 truncate">
                                            {res.metadata.path}
                                        </span>
                                    </div>
                                </div>
                            </motion.div>
                        ))
                    ) : query && !isSearching ? (
                        <p className="text-[11px] font-mono text-muted text-center py-10">Nenhum rastro semântico encontrado.</p>
                    ) : !query && (
                        <div className="text-center py-10 space-y-3">
                            <div className="w-12 h-12 rounded-full bg-white/5 mx-auto flex items-center justify-center">
                                <Link2 className="text-muted/20 w-6 h-6" />
                            </div>
                            <p className="text-[10px] font-mono text-muted uppercase tracking-widest">Aguardando Intenção de Busca...</p>
                        </div>
                    )}
                </AnimatePresence>
            </div>

            {/* Modal de Detalhe do Documento */}
            <AnimatePresence>
                {activeDoc && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-[60] bg-black/60 backdrop-blur-sm flex items-center justify-center p-8"
                        onClick={() => setActiveDoc(null)}
                    >
                        <motion.div
                            initial={{ scale: 0.9, y: 20 }}
                            animate={{ scale: 1, y: 0 }}
                            exit={{ scale: 0.9, y: 20 }}
                            className="glass-premium w-full max-w-2xl rounded-[40px] p-10 relative overflow-hidden"
                            onClick={e => e.stopPropagation()}
                        >
                            <button
                                onClick={() => setActiveDoc(null)}
                                className="absolute top-8 right-8 text-muted hover:text-white transition-colors"
                            >
                                <X className="w-6 h-6" />
                            </button>

                            <div className="flex items-center gap-4 mb-8">
                                <div className="p-3 rounded-2xl bg-accent/10">
                                    <FileText className="text-accent w-6 h-6" />
                                </div>
                                <div className="text-left">
                                    <h4 className="text-lg font-bold text-white tracking-tight">Fragmento de Memória</h4>
                                    <p className="text-[10px] font-mono text-muted uppercase tracking-[0.2em]">{activeDoc.metadata.path}</p>
                                </div>
                            </div>

                            <div className="p-6 rounded-3xl bg-black/40 border border-white/5 text-left mb-8">
                                <pre className="text-xs text-text/90 whitespace-pre-wrap leading-relaxed font-sans">
                                    {activeDoc.text}
                                </pre>
                            </div>

                            <div className="flex justify-end gap-4">
                                <div className="flex items-center gap-2 text-[10px] font-mono text-accent/60 italic">
                                    <Zap className="w-3 h-3" />
                                    Sincronia Semântica: {activeDoc.score * 10}%
                                </div>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default MemoryMap;
