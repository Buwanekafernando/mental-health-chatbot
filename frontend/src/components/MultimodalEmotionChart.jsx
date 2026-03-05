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

const MultimodalEmotionChart = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        api.get("/analytics/multimodal-trends?weeks=12")
            .then(res => buildChart(res.data.weeks))
            .catch(console.error);
    }, []);

    const buildChart = (weeksData) => {
        const labels = Object.keys(weeksData);

        const buildDataset = (type, color) => ({
            label: type,
            data: labels.map(
                w => Object.values(weeksData[w][type]).reduce((a, b) => a + b, 0)
            ),
            borderColor: color,
            backgroundColor: color + "33",
            tension: 0.4,
            fill: true
        });

        setData({
            labels,
            datasets: [
                buildDataset("text", "#6366f1"), // Indigo
                buildDataset("face", "#10b981"), // Emerald
                buildDataset("final", "#f59e0b") // Amber
            ]
        });
    };

    if (!data) return <p>Loading...</p>;

    return <Line data={data} />;
};

export default MultimodalEmotionChart;
