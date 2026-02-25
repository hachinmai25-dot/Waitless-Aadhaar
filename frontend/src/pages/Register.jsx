import { useState } from 'react'
import axios from 'axios'

const API = 'http://localhost:5000/api'

export default function Register() {
  const [step, setStep] = useState(1)
  const [form, setForm] = useState({
    full_name: '', dob: '', gender: '', mobile: '',
    email: '', address: '', pincode: '',
    document_type: 'Passport', application_type: 'New'
  })
  const [applicantId, setApplicantId] = useState(null)
  const [centers, setCenters] = useState([])
  const [selectedCenter, setSelectedCenter] = useState(null)
  const [slot, setSlot] = useState({ date: '', time: '' })
  const [token, setToken] = useState(null)

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value })

  const handleRegister = async (e) => {
    e.preventDefault()
    // Get location via browser
    navigator.geolocation.getCurrentPosition(async (pos) => {
      const payload = {
        ...form,
        latitude: pos.coords.latitude,
        longitude: pos.coords.longitude
      }
      const res = await axios.post(`${API}/applicant/register`, payload)
      setApplicantId(res.data.applicant_id)

      // Find nearest centers
      const cRes = await axios.post(`${API}/applicant/nearest-centers`, {
        latitude: pos.coords.latitude,
        longitude: pos.coords.longitude
      })
      setCenters(cRes.data.centers)
      setStep(2)
    })
  }

  const handleBook = async () => {
    const res = await axios.post(`${API}/applicant/book-slot`, {
      applicant_id: applicantId,
      center_id: selectedCenter.id,
      slot_date: slot.date,
      slot_time: slot.time
    })
    setToken(res.data.token)
    setStep(3)
  }

  if (step === 3) return (
    <div className="success">
      <h2>✅ Appointment Confirmed!</h2>
      <p>Your Token: <strong>{token}</strong></p>
      <p>Center: {selectedCenter?.name}</p>
      <p>Date: {slot.date} at {slot.time}</p>
    </div>
  )

  if (step === 2) return (
    <div className="center-selection">
      <h2>Select Nearest Biometric Center</h2>
      {centers.map(c => (
        <div key={c.id} className={`center-card ${selectedCenter?.id === c.id ? 'selected' : ''}`}
             onClick={() => setSelectedCenter(c)}>
          <h3>{c.name}</h3>
          <p>{c.address}</p>
          <p>📍 {c.distance_km} km away</p>
          <p>Load: {c.current_load}/{c.capacity_per_day}</p>
        </div>
      ))}
      {selectedCenter && (
        <div className="slot-picker">
          <input type="date" onChange={e => setSlot({...slot, date: e.target.value})} />
          <select onChange={e => setSlot({...slot, time: e.target.value})}>
            <option value="">Select Time</option>
            {['09:00','10:00','11:00','14:00','15:00','16:00'].map(t =>
              <option key={t} value={t}>{t}</option>
            )}
          </select>
          <button onClick={handleBook} disabled={!slot.date || !slot.time}>
            Confirm Booking
          </button>
        </div>
      )}
    </div>
  )

  return (
    <form onSubmit={handleRegister} className="register-form">
      <h2>New Aadhaar Registration</h2>
      <input name="full_name" placeholder="Full Name" onChange={handleChange} required />
      <input name="dob" type="date" placeholder="Date of Birth" onChange={handleChange} required />
      <select name="gender" onChange={handleChange} required>
        <option value="">Gender</option>
        <option>Male</option><option>Female</option><option>Other</option>
      </select>
      <input name="mobile" placeholder="Mobile Number" maxLength={10} onChange={handleChange} required />
      <input name="email" placeholder="Email (optional)" onChange={handleChange} />
      <textarea name="address" placeholder="Full Address" onChange={handleChange} required />
      <input name="pincode" placeholder="Pincode" maxLength={6} onChange={handleChange} required />
      <select name="application_type" onChange={handleChange}>
        <option value="New">New Aadhaar</option>
        <option value="Update">Update Details</option>
        <option value="Reprint">Reprint</option>
      </select>
      <button type="submit">Register & Find Centers →</button>
    </form>
  )
      }
