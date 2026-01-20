import EmotionTrendChart from "../components/EmotionTrendChart";
import WeeklySummaryCard from "../components/WeeklySummaryCard";
import CameraEmotion from "../components/CameraEmotion";
import MultimodalEmotionChart from "../components/MultimodalEmotionChart";
import AgreementCard from "../components/AgreementCard";
import EmotionFusionExplanation from "../components/EmotionFusionExplanation";
import "../styles/dashboard.css";

const Dashboard = () => {
    return (
        <div className="dashboard">
            <h2>Emotion Trends</h2>
            <p>Your emotional patterns over recent weeks</p>

            <div className="chart-container">
                <EmotionTrendChart />
                <WeeklySummaryCard />
                <CameraEmotion />
                <MultimodalEmotionChart />
                <AgreementCard />
                <EmotionFusionExplanation />
            </div>
        </div>
    );
};

export default Dashboard;
