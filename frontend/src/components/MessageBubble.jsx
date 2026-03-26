export default function MessageBubble({ message }) {
  const isUser = message.role === "user"

  return (
    <div className={`msg ${isUser ? "user" : "bot"}`}>
      <div className={`msg-avatar ${isUser ? "user-avatar" : "bot-avatar"}`}>
        {isUser ? "U" : "PD"}
      </div>
      <div className="msg-bubble-wrap">
        <div className={`msg-bubble ${isUser ? "user-bubble" : "bot-bubble"}`}>
          {message.content}
        </div>
        {message.timestamp && (
          <div className="msg-time">{message.timestamp}</div>
        )}
      </div>
    </div>
  )
}