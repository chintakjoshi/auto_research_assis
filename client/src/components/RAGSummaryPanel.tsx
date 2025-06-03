import React, { useState } from 'react';

export default function RAGSummaryPanel() {
    const [query, setQuery] = useState('');
    const [summary, setSummary] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSummarize = async () => {
        if (!query.trim()) return;
        setLoading(true);
        try {
            const res = await fetch('http://localhost:8000/rag_summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query }),
            });

            const data = await res.json();
            setSummary(data.summary || 'No summary returned.');
        } catch (error) {
            setSummary('Error generating summary.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-xl mx-auto p-4 space-y-4">
            <h2 className="text-2xl font-bold">Summarize from Top Matches</h2>

            <input
                type="text"
                placeholder="Enter your research query..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="w-full p-2 border rounded"
            />

            <button
                onClick={handleSummarize}
                className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                disabled={loading}
            >
                {loading ? 'Summarizing...' : 'Generate Summary'}
            </button>

            {summary && (
                <div className="bg-gray-100 p-4 rounded whitespace-pre-wrap">
                    {summary}
                </div>
            )}
        </div>
    );
}