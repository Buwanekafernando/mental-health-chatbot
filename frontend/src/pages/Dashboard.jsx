import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import EmotionTrendChart from "../components/EmotionTrendChart";
import WeeklySummaryCard from "../components/WeeklySummaryCard";
import CameraEmotion from "../components/CameraEmotion";
import MultimodalEmotionChart from "../components/MultimodalEmotionChart";
import AgreementCard from "../components/AgreementCard";
import EmotionFusionExplanation from "../components/EmotionFusionExplanation";
import ChatInterface from "../components/ChatInterface";
import AuthContext from "../context/AuthContext";
import "../styles/dashboard.css";

const Dashboard = () => {
    const { logout, user } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/login");
    };

    return (
        <div className="dashboard">
            <div className="dashboard-header">
                <div>
                    <h2>Emotion Trends</h2>
                    <p>Your emotional patterns over recent weeks</p>
                </div>
                <div className="user-section">
                    <span className="user-email">{user}</span>
                    <button className="logout-btn" onClick={handleLogout}>
                        Logout
                    </button>
                </div>
            </div>

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
