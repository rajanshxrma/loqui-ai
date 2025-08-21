import { useState } from 'react'
import './index.css'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')

  return (
    <div className="app">
      <header className="header">
        <h1 className="header-title">LoquiAI</h1>
      </header>
      <main className="chat-panel">
        <div className="empty-state">
          <div className="empty-state-icon">💬</div>
          <div className="empty-state-text">start a conversation</div>
        </div>
      </main>
      <section className="input-area">
        <div className="input-container">
          <textarea className="input-field" placeholder="type a message..." value={input} onChange={(e) => setInput(e.target.value)} rows={1} />
          <button className="btn btn-send" disabled={!input.trim()}>➤</button>
        </div>
      </section>
    </div>
  )
}

export default App
