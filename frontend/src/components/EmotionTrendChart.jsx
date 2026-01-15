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
        api.get("/analytics/emotion-trends?weeks=6")
            .then(res => formatChart(res.data.trends))
            .catch(err => console.error(err));
    }, []);

    const formatChart = (trends) => {
        const weeks = Object.keys(trends);

        const emotions = ["happy", "sadness", "anxiety", "anger", "fear", "neutral"];

        const datasets = emotions.map((emotion) => ({
            label: emotion,
            data: weeks.map(w => trends[w]?.[emotion] || 0),
            tension: 0.4
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
