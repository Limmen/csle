
/**
 * Get window dimensions
 */
const getWindowDimensions = () => {
    const { innerWidth: width, innerHeight: height } = window;
    return {
        width,
        height
    };
}

export default getWindowDimensions;