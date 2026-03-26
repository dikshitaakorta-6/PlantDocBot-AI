import { useEffect, useRef } from "react"

export default function LeafCanvas() {
  const canvasRef = useRef(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext("2d")
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const leaves = Array.from({ length: 18 }, () => ({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: 20 + Math.random() * 40,
      speed: 0.3 + Math.random() * 0.7,
      angle: Math.random() * Math.PI * 2,
      rotSpeed: (Math.random() - 0.5) * 0.02,
      opacity: 0.03 + Math.random() * 0.07
    }))

    function drawLeaf(x, y, size, angle, opacity) {
      ctx.save()
      ctx.translate(x, y)
      ctx.rotate(angle)
      ctx.globalAlpha = opacity
      ctx.fillStyle = "#20b28c"
      ctx.beginPath()
      ctx.moveTo(0, -size / 2)
      ctx.bezierCurveTo(size / 2, -size / 2, size / 2, size / 2, 0, size / 2)
      ctx.bezierCurveTo(-size / 2, size / 2, -size / 2, -size / 2, 0, -size / 2)
      ctx.fill()
      ctx.strokeStyle = "#0f6e56"
      ctx.lineWidth = 0.5
      ctx.beginPath()
      ctx.moveTo(0, -size / 2)
      ctx.lineTo(0, size / 2)
      ctx.stroke()
      ctx.restore()
    }

    let animId
    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      leaves.forEach(l => {
        l.y -= l.speed
        l.angle += l.rotSpeed
        if (l.y < -60) {
          l.y = canvas.height + 60
          l.x = Math.random() * canvas.width
        }
        drawLeaf(l.x, l.y, l.size, l.angle, l.opacity)
      })
      animId = requestAnimationFrame(animate)
    }
    animate()

    const handleResize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }
    window.addEventListener("resize", handleResize)

    return () => {
      cancelAnimationFrame(animId)
      window.removeEventListener("resize", handleResize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        zIndex: 0,
        pointerEvents: "none"
      }}
    />
  )
}