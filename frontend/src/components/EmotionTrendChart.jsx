import {
    Chart as ChartJS,
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Tooltip,
    Legend
} from "chart.js";

import { Line } from "react-chartjs-2";
import { useEffect, useState } from "react";
import api from "../services/api";

ChartJS.register(
    LineElement,
    CategoryScale,
    LinearScale,
    PointElement,
    Tooltip,
    Legend
);

const EmotionTrendChart = () => {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        api.get("/analytics/multimodal-trends?weeks=12")
            .then(res => formatChart(res.data.weeks))
            .catch(err => console.error(err));
    }, []);

    const formatChart = (trends) => {
        const weeks = Object.keys(trends);

        const emotions = ["happy", "sad", "fear", "angry", "neutral"];
        const emotionColors = {
            happy: "#10b981",    // Emerald
            sad: "#3b82f6",     // Blue
            fear: "#8b5cf6",    // Violet
            angry: "#ef4444",   // Red
            neutral: "#94a3b8"  // Slate
        };

        const datasets = emotions.map((emotion) => ({
            label: emotion,
            data: weeks.map(w => trends[w]?.final?.[emotion] || 0),
            borderColor: emotionColors[emotion] || "#000",
            backgroundColor: (emotionColors[emotion] || "#000") + "33",
            tension: 0.4,
            fill: false
        }));

        setChartData({
            labels: weeks,
            datasets
        });
    };

    if (!chartData) return <p>Loading chart...</p>;

    return <Line data={chartData} />;
};

export default EmotionTrendChart;
