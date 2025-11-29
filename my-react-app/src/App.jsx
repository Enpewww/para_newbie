import { Routes, Route } from 'react-router-dom'
import WhatsAppOnboarding from './WhatsappOnboard'

function App() {
  return (
    <Routes>
      <Route path="/" element={<WhatsAppOnboarding />} />
    </Routes>
  )
}

export default App;
