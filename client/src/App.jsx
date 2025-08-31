import { useState, useRef, useEffect } from 'react'
import './index.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const LANGUAGES = [
  { code: 'en', label: 'English' },
  { code: 'es', label: 'Español' },
  { code: 'fr', label: 'Français' },
  { code: 'de', label: 'Deutsch' },
  { code: 'ja', label: '日本語' },
  { code: 'zh', label: '中文' },
  { code: 'ko', label: '한국어' },
  { code: 'pt', label: 'Português' },
  { code: 'hi', label: 'हिन्दी' },
  { code: 'ar', label: 'العربية' },
]

const MODELS = [
  { id: 'gpt-4o', label: 'GPT-4o' },
  { id: 'claude-3-5-sonnet-20241022', label: 'Claude 3.5' },
]

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [model, setModel] = useState('gpt-4o')
  const [language, setLanguage] = useState('en')
  const [isStreaming, setIsStreaming] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const chatPanelRef = useRef(null)
  const inputRef = useRef(null)
  const recognitionRef = useRef(null)

  // auto-scroll on new messages
  useEffect(() => {
    if (chatPanelRef.current) {
      chatPanelRef.current.scrollTop = chatPanelRef.current.scrollHeight
    }
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || isStreaming) return

    const userMessage = { role: 'user', content: input.trim() }
    const newMessages = [...messages, userMessage]
    setMessages(newMessages)
    setInput('')
    setIsStreaming(true)

    // add empty ai message for streaming
    const aiMessage = { role: 'assistant', content: '', model: model }
    setMessages([...newMessages, aiMessage])

    try {
      const response = await fetch(`${API_URL}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model,
          language,
          messages: newMessages.map(m => ({ role: m.role, content: m.content })),
        }),
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let fullContent = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const text = decoder.decode(value)
        const lines = text.split('\n').filter(l => l.startsWith('data: '))

        for (const line of lines) {
          try {
            const data = JSON.parse(line.slice(6))
            if (data.token) {
              fullContent += data.token
              setMessages(prev => {
                const updated = [...prev]
                updated[updated.length - 1] = {
                  ...updated[updated.length - 1],
                  content: fullContent,
                }
                return updated
              })
            }
          } catch (e) {
            // skip malformed chunks
          }
        }
      }
    } catch (error) {
      setMessages(prev => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: 'sorry, something went wrong. please try again.',
        }
        return updated
      })
    }

    setIsStreaming(false)
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  // web speech api for voice input
  const toggleRecording = () => {
    if (isRecording) {
      recognitionRef.current?.stop()
      setIsRecording(false)
      return
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) {
      alert('speech recognition not supported in this browser')
      return
    }

    const recognition = new SpeechRecognition()
    recognition.lang = language === 'zh' ? 'zh-CN' : language === 'pt' ? 'pt-BR' : language
    recognition.interimResults = false
    recognition.continuous = false

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      setInput(transcript)
      setIsRecording(false)
    }

    recognition.onerror = () => setIsRecording(false)
    recognition.onend = () => setIsRecording(false)

    recognitionRef.current = recognition
    recognition.start()
    setIsRecording(true)
  }

  // tts playback via aws polly
  const playTTS = async (text) => {
    try {
      const response = await fetch(`${API_URL}/api/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, language }),
      })

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const audio = new Audio(url)
      audio.play()
      audio.onended = () => URL.revokeObjectURL(url)
    } catch (e) {
      console.error('tts error:', e)
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1 className="header-title">LoquiAI</h1>
        <div className="header-controls">

        </div>
      </header>

      <main className="chat-panel" ref={chatPanelRef} role="log" aria-label="Chat messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">💬</div>
            <div className="empty-state-text">start a conversation in any language</div>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div key={i} className={`message message-${msg.role === 'user' ? 'user' : 'ai'}`}>
              <div className="message-avatar">
                {msg.role === 'user' ? 'U' : 'AI'}
              </div>
              <div>
                <div className="message-content">
                  {msg.content}
                  {isStreaming && i === messages.length - 1 && msg.role === 'assistant' && (
                    <span className="streaming-cursor" />
                  )}
                </div>

              </div>
            </div>
          ))
        )}
      </main>

      <section className="input-area">
        <div className="input-container">

          <textarea
            id="chat-input"
            ref={inputRef}
            className="input-field"
            placeholder="type a message or press the mic..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            aria-label="Message input"
          />
          <button
            id="send-button"
            className="btn btn-send"
            onClick={sendMessage}
            disabled={!input.trim() || isStreaming}
            aria-label="Send message"
          >
            ➤
          </button>
        </div>
      </section>
    </div>
  )
}

export default App
