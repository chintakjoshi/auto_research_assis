function PaperList({ papers }) {
  return (
    <div>
      {papers.map((p, idx) => (
        <div key={idx} style={{ margin: "1rem 0", padding: "1rem", border: "1px solid #ccc" }}>
          <h3>{p.title}</h3>
          <p><strong>Authors:</strong> {p.authors.join(", ")}</p>
          <p><strong>Abstract:</strong> {p.abstract}</p>
          <p><strong>Published:</strong> {p.published}</p>
          <a href={p.url} target="_blank" rel="noreferrer">View Paper</a>
        </div>
      ))}
    </div>
  );
}

export default PaperList;