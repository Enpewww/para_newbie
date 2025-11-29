import { useState } from "react";
import { motion } from "framer-motion";
import { MessageCircle, ShieldCheck, Smartphone, ArrowRight } from "lucide-react";
import "./onboarding.css";
import logo from "./assets/logo-arthi-usaha.png";

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
        let formattedPhone = phone;
        // Auto-format phone number: replace leading '0' with '62'
        if (formattedPhone.startsWith('0')) {
            formattedPhone = '62' + formattedPhone.substring(1);
        }

        if (!formattedPhone) {
            alert("Mohon masukkan nomor WhatsApp Ibu terlebih dahulu.");
            setStep(1);
            return;
        }

        setLoading(true);
        setError("");

        try {
            // Save user data to database
            const response = await fetch('http://localhost:3001/api/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    firstName,
                    lastName,
                    phone: formattedPhone,
                    customerEmail: email,
                    location,
                    storeName: store,
                    latitude,
                    longitude
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Gagal menyimpan data. Silakan coba lagi.');
            }

            // Check if user already existed
            if (data.message === 'user_exists') {
                // Show message that account already exists
                // alert('Akun sudah terdaftar! Mengalihkan ke WhatsApp...');
            }

            // Success! Now redirect to WhatsApp
            const msg = encodeURIComponent(
                `Halo, nama saya Ibu ${firstName} ${lastName} dari ${store}. Saya ingin mulai menggunakan layanan ArthiUsaha.`
            );

            window.open(`https://wa.me/${628566211297}?text=${msg}`, "_blank");

        } catch (err) {
            console.error('Error saving user data:', err);
            setError(err.message || 'Gagal menyimpan informasi. Mohon periksa koneksi internet Ibu.');
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
                            <img className="arthi-logo" src={logo} alt="Logo" />
                            <h1>Pendaftaran ArthiUsaha</h1>
                        </div>
                        <p className="subtitle">Layanan asisten digital untuk membantu usaha Ibu makin maju.</p>

                        <div className="steps">
                            {[1, 2, 3].map((s) => (
                                <div key={s} className={`step-bar ${step >= s ? "active" : "inactive"}`}></div>
                            ))}
                        </div>

                        {step === 1 && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="step-box">
                                <div className="step-header">
                                    <Smartphone className="icon-sm" />
                                    <h2>Masukkan Nomor WhatsApp</h2>
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
                                    type="tel"
                                    placeholder="Contoh: 6281234567890"
                                    value={phone}
                                    onChange={(e) => setPhone(e.target.value)}
                                    disabled={loading}
                                />
                                <button
                                    className="btn-primary"
                                    onClick={async () => {
                                        if (!phone) {
                                            alert("Mohon masukkan nomor WhatsApp Ibu.");
                                            return;
                                        }

                                        let formattedPhone = phone;
                                        // Auto-format phone number: replace leading '0' with '62'
                                        if (formattedPhone.startsWith('0')) {
                                            formattedPhone = '62' + formattedPhone.substring(1);
                                        }

                                        // Validation: Check length (Indonesian numbers are usually 10-13 digits)
                                        if (formattedPhone.length < 10) {
                                            setError("Nomor HP terlalu pendek. Mohon periksa kembali.");
                                            return;
                                        }
                                        if (formattedPhone.length > 14) {
                                            setError("Nomor HP terlalu panjang. Mohon periksa kembali.");
                                            return;
                                        }

                                        setLoading(true);
                                        setError("");

                                        try {
                                            // Check if phone exists
                                            const response = await fetch(`http://localhost:3001/api/users/check/${formattedPhone}`);
                                            const data = await response.json();

                                            if (!response.ok) {
                                                throw new Error(data.error || 'Gagal memeriksa nomor telepon');
                                            }

                                            if (data.exists) {
                                                // User exists, redirect to WhatsApp immediately
                                                const userData = data.data;
                                                const msg = encodeURIComponent(
                                                    `Halo, nama saya Ibu ${userData.firstname} ${userData.lastname} dari ${userData.storename}. Saya ingin mulai menggunakan layanan ArthiUsaha.`
                                                );

                                                window.open(`https://wa.me/${628566211297}?text=${msg}`, "_blank");
                                            } else {
                                                // New user, proceed to registration
                                                goToStep(2);
                                            }
                                        } catch (err) {
                                            console.error('Error checking phone:', err);
                                            setError(err.message || 'Gagal memeriksa nomor. Silakan coba lagi.');
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
                                    {loading ? 'Memeriksa...' : 'Lanjut'}
                                </button>
                            </motion.div>
                        )}

                        {step === 2 && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="step-box">
                                <div className="step-header">
                                    <ShieldCheck className="icon-sm" />
                                    <h2>Data Diri Ibu</h2>
                                </div>

                                <input className="input" placeholder="Nama Depan (Contoh: Siti)" value={firstName} onChange={(e) => setFirstName(e.target.value)} />
                                <input className="input" placeholder="Nama Belakang (Contoh: Aminah)" value={lastName} onChange={(e) => setLastName(e.target.value)} />
                                <input className="input" type="email" placeholder="Alamat Email (Opsional)" value={email} onChange={(e) => setEmail(e.target.value)} />
                                <input className="input" placeholder="Alamat (Contoh: Jl. Mawar No. 10, Jakarta)" value={location} onChange={(e) => setLocation(e.target.value)} />
                                <input className="input" placeholder="Nama Usaha (Contoh: Warung Makan Barokah)" value={store} onChange={(e) => setStore(e.target.value)} />

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
                                    <button className="btn-outline" onClick={() => goToStep(1)}>Kembali</button>
                                    <button
                                        className="btn-primary"
                                        onClick={() => {
                                            if (!firstName || !lastName || !store) {
                                                alert("Mohon lengkapi nama dan nama usaha Ibu.");
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
                                                        setLocationError("Mohon izinkan akses lokasi agar kami bisa mengetahui alamat usaha Ibu.");
                                                    }
                                                );
                                            } else {
                                                setLocationError("Browser HP Ibu tidak mendukung fitur lokasi.");
                                            }
                                        }}
                                    >
                                        Lanjut
                                    </button>
                                </div>
                            </motion.div>
                        )}

                        {step === 3 && (
                            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="step-box center-text">
                                <MessageCircle className="icon-lg" />
                                <h2>Pendaftaran Selesai!</h2>
                                <p>Ibu akan dialihkan ke WhatsApp untuk mulai mengobrol dengan asisten kami.</p>

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
                                    {loading ? 'Menyimpan...' : 'Buka WhatsApp Sekarang'}
                                </button>
                            </motion.div>
                        )}
                    </div>
                </div>
            </motion.div >
        </div >
    );
}

export default WhatsAppOnboarding;
