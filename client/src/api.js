import axios from "axios";

const BASE_URL = "http://localhost:8000";

export const fetchPapers = async (topic) => {
    const res = await axios.get(`${BASE_URL}/query`, {
        params: { topic },
    });
    return res.data;
};

export const summarizeAbstracts = async (abstracts) => {
    const res = await axios.post(`${BASE_URL}/summarize`, { abstracts });
    return res.data.summary;
};