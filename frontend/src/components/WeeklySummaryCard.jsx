import { useEffect, useState } from "react";
import api from "../services/api";

const WeeklySummaryCard = () => {
    const [summary, setSummary] = useState(null);

    useEffect(() => {
        api.get("/chat/weekly-summary")
            .then(res => setSummary(res.data))
            .catch(err => console.error(err));
    }, []);

    if (!summary) return <p>Loading summary...</p>;

    return (
        <div className="summary-card">
            <h3>Weekly Emotional Summary</h3>

            <p><strong>Dominant Emotion:</strong> {summary.dominant_emotion}</p>

            <p className="insight">
                {summary.insight}
            </p>

            <div className="emotion-bars">
                {Object.entries(summary.summary).map(([emotion, value]) => (
                    <div key={emotion}>
                        <span>{emotion}</span>
                        <div className="bar">
                            <div className="fill" style={{ width: `${value}%` }}></div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WeeklySummaryCard;
