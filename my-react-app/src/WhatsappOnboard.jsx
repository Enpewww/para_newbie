import { useState } from "react";
import { motion } from "framer-motion";
import { MessageCircle, ShieldCheck, Smartphone, ArrowRight } from "lucide-react";
import "./onboarding.css";

function WhatsAppOnboarding() {
    const [step, setStep] = useState(1);
    const [phone, setPhone] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [location, setLocation] = useState("");
    const [store, setStore] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [latitude, setLatitude] = useState(null);
    const [longitude, setLongitude] = useState(null);
    const [locationError, setLocationError] = useState("");

    const goToStep = (target) => {
        setError(""); // Clear any previous errors
        setStep(target);
    };

    const handleStartChat = async () => {
        if (!phone) {
            alert("Please enter your phone number before starting the chat.");
            setStep(1);
            return;
        }

        setLoading(true);
        setError("");

        try {
            // Save user data to database
            const response = await fetch('/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    firstName,
                    lastName,
                    phone,
                    customerEmail: email,
                    location,
                    storeName: store,
                    latitude,
                    longitude
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Failed to save user data');
            }

            // Check if user already existed
            if (data.message === 'user_exists') {
                // Show message that account already exists
                alert('Account already exists! Redirecting you to WhatsApp...');
            }

            // Success! Now redirect to WhatsApp
            const msg = encodeURIComponent(
                `Hi, my name is ${firstName} ${lastName} from ${store}. I want to start using the ArthiUsaha service.`
            );

            window.open(`https://wa.me/${628566211297}?text=${msg}`, "_blank");

        } catch (err) {
            console.error('Error saving user data:', err);
            setError(err.message || 'Failed to save your information. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="wrapper gradient-bg">
            <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
                className="container-box purple-glass"
            >
                <div className="card">
                    <div className="card-content">
                        <div className="header-row">
                            <MessageCircle className="icon" />
                            <h1>ArthiUsaha WhatsApp Registration</h1>
                        </div>
                        <p className="subtitle">Smart onboarding for users who want to chat directly via WhatsApp.</p>

                        <div className="steps">
                            {[1, 2, 3].map((s) => (
                                <div key={s} className={`step-bar ${step >= s ? "active" : "inactive"}`}></div>
                            ))}
                        </div>

                        {step === 1 && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="step-box">
                                <div className="step-header">
                                    <Smartphone className="icon-sm" />
                                    <h2>Enter Your Phone Number</h2>
                                </div>

                                {error && (
                                    <div style={{
                                        padding: '12px',
                                        marginBottom: '16px',
                                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                        border: '1px solid rgba(239, 68, 68, 0.3)',
                                        borderRadius: '8px',
                                        color: '#ef4444',
                                        fontSize: '14px'
                                    }}>
                                        {error}
                                    </div>
                                )}

                                <input
                                    className="input"
                                    placeholder="e.g. 6281234567890 (use country code)"
                                    value={phone}
                                    onChange={(e) => setPhone(e.target.value)}
                                    disabled={loading}
                                />
                                <button
                                    className="btn-primary"
                                    onClick={async () => {
                                        if (!phone) {
                                            alert("Please enter your phone number.");
                                            return;
                                        }

                                        setLoading(true);
                                        setError("");

                                        try {
                                            // Check if phone exists
                                            const response = await fetch(`/api/users/check/${phone}`);
                                            const data = await response.json();

                                            if (!response.ok) {
                                                throw new Error(data.error || 'Failed to check phone number');
                                            }

                                            if (data.exists) {
                                                // User exists, redirect to WhatsApp immediately
                                                const userData = data.data;
                                                const msg = encodeURIComponent(
                                                    `Hi, my name is ${userData.firstname} ${userData.lastname} from ${userData.storename}. I want to start using the ArthiUsaha service.`
                                                );

                                                window.open(`https://wa.me/${628566211297}?text=${msg}`, "_blank");
                                            } else {
                                                // New user, proceed to registration
                                                goToStep(2);
                                            }
                                        } catch (err) {
                                            console.error('Error checking phone:', err);
                                            setError(err.message || 'Failed to check phone number. Please try again.');
                                        } finally {
                                            setLoading(false);
                                        }
                                    }}
                                    disabled={loading}
                                    style={{
                                        opacity: loading ? 0.6 : 1,
                                        cursor: loading ? 'not-allowed' : 'pointer'
                                    }}
                                >
                                    {loading ? 'Checking...' : 'Continue'} <ArrowRight className="icon-sm" />
                                </button>
                            </motion.div>
                        )}

                        {step === 2 && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="step-box">
                                <div className="step-header">
                                    <ShieldCheck className="icon-sm" />
                                    <h2>Customer Information</h2>
                                </div>

                                <input className="input" placeholder="First Name" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                                <input className="input" placeholder="Last Name" value={lastName} onChange={(e) => setLastName(e.target.value)} />
                                <input className="input" placeholder="Email Address" value={email} onChange={(e) => setEmail(e.target.value)} />
                                <input className="input" placeholder="Location (e.g. Jakarta Selatan)" value={location} onChange={(e) => setLocation(e.target.value)} />
                                <input className="input" placeholder="Business / Store Name" value={store} onChange={(e) => setStore(e.target.value)} />

                                {locationError && (
                                    <div style={{
                                        padding: '12px',
                                        marginTop: '10px',
                                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                        border: '1px solid rgba(239, 68, 68, 0.3)',
                                        borderRadius: '8px',
                                        color: '#ef4444',
                                        fontSize: '14px'
                                    }}>
                                        {locationError}
                                    </div>
                                )}

                                <div className="btn-row">
                                    <button className="btn-outline" onClick={() => goToStep(1)}>Back</button>
                                    <button
                                        className="btn-primary"
                                        onClick={() => {
                                            if (!firstName || !lastName || !store) {
                                                alert("Please complete your name and store information.");
                                                return;
                                            }

                                            // Request location permission
                                            if ("geolocation" in navigator) {
                                                navigator.geolocation.getCurrentPosition(
                                                    (position) => {
                                                        setLatitude(position.coords.latitude);
                                                        setLongitude(position.coords.longitude);
                                                        setLocationError("");
                                                        goToStep(3);
                                                    },
                                                    (error) => {
                                                        console.error("Location error:", error);
                                                        setLocationError("Location access is required to register. Please allow location access.");
                                                    }
                                                );
                                            } else {
                                                setLocationError("Geolocation is not supported by your browser.");
                                            }
                                        }}
                                    >
                                        Continue <ArrowRight className="icon-sm" />
                                    </button>
                                </div>
                            </motion.div>
                        )}

                        {step === 3 && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="step-box center-text">
                                <MessageCircle className="icon-lg" />
                                <h2 style={{ color: '#333' }}>Registration Complete</h2>
                                <p>You will now be redirected to WhatsApp to begin chatting with our assistant.</p>

                                {error && (
                                    <div style={{
                                        padding: '12px',
                                        marginTop: '16px',
                                        backgroundColor: 'rgba(239, 68, 68, 0.1)',
                                        border: '1px solid rgba(239, 68, 68, 0.3)',
                                        borderRadius: '8px',
                                        color: '#ef4444',
                                        fontSize: '14px'
                                    }}>
                                        {error}
                                    </div>
                                )}

                                <button
                                    className="btn-primary"
                                    onClick={handleStartChat}
                                    disabled={loading}
                                    style={{
                                        opacity: loading ? 0.6 : 1,
                                        cursor: loading ? 'not-allowed' : 'pointer'
                                    }}
                                >
                                    {loading ? 'Saving...' : 'Start WhatsApp Chat'}
                                </button>
                            </motion.div>
                        )}
                    </div>
                </div>
            </motion.div>
        </div>
    );
}

export default WhatsAppOnboarding;
