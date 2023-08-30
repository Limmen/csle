import formatBytes from "./formatBytes";

/**
 *  Tests the formatBytes() function
 */
test('formatBytes format a number in bytes into a string', () => {
    expect(formatBytes(0, 2)).toBe("0 Bytes");
});