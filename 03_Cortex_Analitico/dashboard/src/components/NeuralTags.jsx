import React, { useState, useEffect } from 'react';
import { Tag } from 'lucide-react';

const NeuralTags = () => {
    const [tags, setTags] = useState(['engineering', 'science', 'gamedev']);
    const allTags = ['engineering', 'science', 'gamedev', 'art', 'music'];

    useEffect(() => {
        fetch('http://localhost:5000/api/neural/tags')
            .then(res => res.json())
            .then(data => setTags(data.active_tags || []))
            .catch(console.error);
    }, []);

    const toggleTag = async (tag) => {
        const newTags = tags.includes(tag) ? tags.filter(t => t !== tag) : [...tags, tag];
        setTags(newTags); // Optimistic UI update
        try {
            await fetch('http://localhost:5000/api/neural/tags', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tags: newTags })
            });
        } catch (err) {
            console.error("Failed to update tags", err);
        }
    };

    return (
        <div className="flex items-center gap-2 pl-4 border-l border-white/5">
            <Tag className="w-3 h-3 text-muted" />
            <div className="flex gap-1.5">
                {allTags.map(tag => {
                    const isActive = tags.includes(tag);
                    return (
                        <button
                            key={tag}
                            onClick={() => toggleTag(tag)}
                            className={`px-2 py-0.5 rounded text-[9px] font-mono uppercase transition-all duration-300 border ${isActive
                                    ? 'bg-accent/20 text-accent border-accent/40 shadow-[0_0_8px_rgba(0,255,171,0.2)]'
                                    : 'bg-black/30 text-muted border-white/5 hover:bg-white/10 hover:text-white/70'
                                }`}
                            title={`Toggle Neural Context: ${tag}`}
                        >
                            {tag}
                        </button>
                    );
                })}
            </div>
        </div>
    );
};

export default NeuralTags;
