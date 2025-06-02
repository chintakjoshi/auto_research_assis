import { useState } from "react";
import { fetchPapers, summarizeAbstracts } from "./api";
import PaperList from "./components/PaperList";
import SummaryBox from "./components/SummaryBox";

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

      <PaperList papers={papers} />

      {papers.length > 0 && (
        <button onClick={handleSummarize} style={{ marginTop: "1rem" }}>
          Summarize All
        </button>
      )}

      {summary && <SummaryBox text={summary} />}
    </div>
  );
}

export default App;