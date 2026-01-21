import EmotionTrendChart from "../components/EmotionTrendChart";
import WeeklySummaryCard from "../components/WeeklySummaryCard";
import CameraEmotion from "../components/CameraEmotion";
import MultimodalEmotionChart from "../components/MultimodalEmotionChart";
import AgreementCard from "../components/AgreementCard";
import EmotionFusionExplanation from "../components/EmotionFusionExplanation";
import ChatInterface from "../components/ChatInterface";
import "../styles/dashboard.css";

const Dashboard = () => {
    return (
        <div className="dashboard">
            <h2>Emotion Trends</h2>
            <p>Your emotional patterns over recent weeks</p>

            <div className="dashboard-grid">
                <div className="analytics-section">
                    <div className="chart-container">
                        <EmotionTrendChart />
                        <MultimodalEmotionChart />
                        <AgreementCard />
                        <EmotionFusionExplanation />
                    </div>
                    <WeeklySummaryCard />
                </div>

                <div className="interaction-section">
                    <CameraEmotion />
                    <ChatInterface />
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
