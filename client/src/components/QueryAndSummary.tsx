import React, { useState } from 'react';

export default function QueryAndSummary() {
    const [query, setQuery] = useState('');
    const [summary, setSummary] = useState('');
    const [loading, setLoading] = useState(false);
    const [plan, setPlan] = useState(null);

    const handleSummarize = async () => {
        if (!query.trim()) return;
        setLoading(true);
        try {
            const [summaryRes, planRes] = await Promise.all([
                fetch('http://localhost:8000/rag_summarize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query }),
                }),
                fetch(`http://localhost:8000/plan?topic=${encodeURIComponent(query)}`)
            ]);

            const summaryData = await summaryRes.json();
            const planData = await planRes.json();

            setSummary(summaryData.summary || 'No summary returned.');
            setPlan(planData);
        } catch (error) {
            setSummary('Error generating summary.');
            setPlan(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-xl mx-auto p-4 space-y-4">
            <h2 className="text-2xl font-bold">MCP Smart Summary</h2>

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
                {loading ? 'Summarizing...' : 'Run RAG Summary'}
            </button>

            {summary && (
                <div className="bg-gray-100 p-4 rounded whitespace-pre-wrap">
                    {summary}
                </div>
            )}

            {plan && (
                <div className="bg-white p-4 rounded border text-sm font-mono whitespace-pre-wrap">
                    <strong>Execution Plan:</strong>
                    <pre>{JSON.stringify(plan, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}