import { Line } from "react-chartjs-2";
import { useEffect, useState } from "react";
import api from "../services/api";

const MultimodalEmotionChart = () => {
    const [data, setData] = useState(null);

    useEffect(() => {
        api.get("/analytics/multimodal-trends?weeks=6")
            .then(res => buildChart(res.data.weeks))
            .catch(console.error);
    }, []);

    const buildChart = (weeksData) => {
        const labels = Object.keys(weeksData);

        const buildDataset = (type) => ({
            label: type,
            data: labels.map(
                w => Object.values(weeksData[w][type]).reduce((a, b) => a + b, 0)
            ),
            tension: 0.4
        });

        setData({
            labels,
            datasets: [
                buildDataset("text"),
                buildDataset("face"),
                buildDataset("final")
            ]
        });
    };

    if (!data) return <p>Loading...</p>;

    return <Line data={data} />;
};

export default MultimodalEmotionChart;
