function SummaryBox({ text }) {
    return (
        <div style={{ marginTop: "2rem", padding: "1rem", background: "#000000" }}>
            <h2>Summary</h2>
            <pre style={{ whiteSpace: "pre-wrap" }}>{text}</pre>
        </div>
    );
}

export default SummaryBox;