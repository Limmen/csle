import { useEffect, useState } from "react"

const useKeyPress = ({ key, onKeyUp, onKeyDown }) => {
    const [isPressed, setPressed] = useState(false)

    useEffect(() => {
        const handleDown = event => {
            const { key: pressedKey } = event
            if (key === pressedKey) {
                if (onKeyDown) onKeyDown()

                setPressed(true)
            }
        }

        const handleUp = event => {
            const { key: releasedKey } = event
            if (key === releasedKey) {
                if (onKeyUp) onKeyUp()

                setPressed(false)
            }
        }

        window.addEventListener("keyup", handleUp)
        window.addEventListener("keydown", handleDown)

        return () => {
            window.removeEventListener("keyup", handleUp)
            window.removeEventListener("keydown", handleDown)
        }
    }, [])

    return isPressed
}

export default useKeyPress