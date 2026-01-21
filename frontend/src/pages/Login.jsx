import { useState, useContext } from "react";
import AuthContext from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
import "../styles/login.css"; // We'll need to make sure this style file exists or use inline styles for now

const Login = () => {
    const { login, register } = useContext(AuthContext);
    const navigate = useNavigate();

    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        if (isLogin) {
            const result = await login(email, password);
            if (result.success) {
                navigate("/");
            } else {
                setError(result.message);
            }
        } else {
            const result = await register(email, password);
            if (result.success) {
                alert("Registration successful! Please log in.");
                setIsLogin(true);
            } else {
                setError(result.message);
            }
        }
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h2>{isLogin ? "Welcome Back" : "Create Account"}</h2>
                <p className="subtitle">AI-Powered Mental Health Companion</p>

                <div className="tabs">
                    <button
                        className={isLogin ? "active" : ""}
                        onClick={() => setIsLogin(true)}
                    >
                        Login
                    </button>
                    <button
                        className={!isLogin ? "active" : ""}
                        onClick={() => setIsLogin(false)}
                    >
                        Register
                    </button>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>

                    {error && <p className="error-message">{error}</p>}

                    <button type="submit" className="auth-btn">
                        {isLogin ? "Login" : "Register"}
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;
