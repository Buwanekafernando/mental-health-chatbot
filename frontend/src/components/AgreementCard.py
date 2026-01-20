import { useEffect, useState } from "react";
import api from "../services/api";

const AgreementCard = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.get("/analytics/emotion-agreement")
      .then(res => setStats(res.data))
      .catch(console.error);
  }, []);

  if (!stats) return null;

  return (
    <div className="summary-card">
      <h3>Emotion Agreement</h3>
      <p>Agreement Rate: <strong>{stats.agreement_rate}%</strong></p>
      <p>Conflict Rate: {stats.conflict_rate}%</p>
    </div>
  );
};

export default AgreementCard;
