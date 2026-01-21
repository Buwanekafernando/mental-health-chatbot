import { useEffect, useRef, useState } from "react";
import * as faceapi from "face-api.js";
import api from "../services/api";

const CameraEmotion = () => {
    const videoRef = useRef();
    const [emotion, setEmotion] = useState("Detecting...");

    useEffect(() => {
        loadModels();
        startVideo();
    }, []);

    const loadModels = async () => {
        await faceapi.nets.tinyFaceDetector.loadFromUri("/models");
        await faceapi.nets.faceExpressionNet.loadFromUri("/models");
    };

    const startVideo = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoRef.current.srcObject = stream;
    };

    const detectEmotion = async () => {
        if (!videoRef.current) return;

        const detection = await faceapi
            .detectSingleFace(videoRef.current, new faceapi.TinyFaceDetectorOptions())
            .withFaceExpressions();

        if (detection) {
            const expressions = detection.expressions;
            const dominantEmotion = Object.keys(expressions)
                .reduce((a, b) => expressions[a] > expressions[b] ? a : b);

            setEmotion(dominantEmotion);

            // Send to backend (optional)
            api.post("/analytics/face-emotion", {
                emotion: dominantEmotion
            });
        }
    };

    return (
        <div className="camera-container">
            <video
                ref={videoRef}
                autoPlay
                muted
                width="100%"
                height="auto"
                className="camera-feed"
                onPlay={() => setInterval(detectEmotion, 3000)}
            />
            <div className="camera-overlay">
                <div className="emotion-badge">
                    <span className="emotion-label">Face:</span>
                    <span className="emotion-value">{emotion}</span>
                </div>
            </div>
        </div>
    );
};

export default CameraEmotion;
