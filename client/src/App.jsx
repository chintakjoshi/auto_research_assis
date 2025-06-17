import { useState } from "react";
import { fetchPapers, summarizeAbstracts } from "./api";
import PapersContextDisplay from "./components/PapersContextDisplay";
import QueryAndSummary from './components/QueryAndSummary';

function App() {
  const [topic, setTopic] = useState("");
  const [papers, setPapers] = useState([]);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    const results = await fetchPapers(topic);
    setPapers(results);
    setSummary("");
    setLoading(false);
  };

  const handleSummarize = async () => {
    const abstracts = papers.map((p) => p.abstract);
    const result = await summarizeAbstracts(abstracts);
    setSummary(result);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Autonomous Research Assistant</h1>
      <input
        type="text"
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Enter research topic"
        style={{ width: "300px", marginRight: "1rem" }}
      />
      <button onClick={handleSearch}>Search</button>

      {loading && <p>Loading...</p>}

      <PapersContextDisplay papers={papers} />

      {papers.length > 0 && (
        <button onClick={handleSummarize} style={{ marginTop: "1rem", background: "#000000", color: "white" }}>
          Summarize All
        </button>
      )}

      {summary && (
        <div style={{ marginTop: "2rem", padding: "1rem", background: "#000000", color: "white" }}>
          <h2>Summary</h2>
          <pre style={{ whiteSpace: "pre-wrap" }}>{summary}</pre>
        </div>
      )}

      <div style={{ marginTop: "3rem" }}>
        <QueryAndSummary />
      </div>
    </div>
  );
}

export default App;