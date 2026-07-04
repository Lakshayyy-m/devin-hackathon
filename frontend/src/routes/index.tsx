import { useState } from 'react'
import { createFileRoute } from '@tanstack/react-router'

import { sendChat } from '../lib/api'
import type { ChatMessage } from '../lib/api'

export const Route = createFileRoute('/')({ component: Home })

function Home() {
  const [messages, setMessages] = useState<Array<ChatMessage>>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const text = input.trim()
    if (!text || loading) return
    const next: Array<ChatMessage> = [...messages, { role: 'user', content: text }]
    setMessages(next)
    setInput('')
    setLoading(true)
    setError(null)
    try {
      const res = await sendChat(next)
      setMessages([...next, res.message])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto flex h-screen max-w-2xl flex-col p-6">
      <h1 className="text-2xl font-bold">AI Chat</h1>
      <p className="mt-1 text-sm text-gray-500">
        TanStack Start + FastAPI + OpenRouter boilerplate
      </p>
      <div className="mt-4 flex-1 space-y-3 overflow-y-auto rounded-lg border border-gray-200 p-4">
        {messages.length === 0 && (
          <p className="text-sm text-gray-400">Send a message to get started.</p>
        )}
        {messages.map((m, i) => (
          <div
            key={i}
            className={`max-w-[80%] whitespace-pre-wrap rounded-lg px-3 py-2 text-sm ${
              m.role === 'user' ? 'ml-auto bg-blue-600 text-white' : 'bg-gray-100'
            }`}
          >
            {m.content}
          </div>
        ))}
        {loading && <p className="text-sm text-gray-400">Thinking…</p>}
        {error && <p className="text-sm text-red-500">{error}</p>}
      </div>
      <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything…"
          className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  )
}
