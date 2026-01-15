import EmotionTrendChart from "../components/EmotionTrendChart";
import "../styles/dashboard.css";

const Dashboard = () => {
    return (
        <div className="dashboard">
            <h2>Emotion Trends</h2>
            <p>Your emotional patterns over recent weeks</p>

            <div className="chart-container">
                <EmotionTrendChart />
            </div>
        </div>
    );
};

export default Dashboard;
