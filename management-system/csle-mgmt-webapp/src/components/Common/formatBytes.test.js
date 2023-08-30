import formatBytes from "./formatBytes";

/**
 *  Tests the formatBytes() function
 */
test('formatBytes format a number in bytes into a string', () => {
    expect(formatBytes(0, 2)).toBe("0 Bytes");
    expect(formatBytes(1000, 2)).toBe("1000 Bytes");
    expect(formatBytes(2000, 2)).toBe("1.95 KiB");
    expect(formatBytes(20000, 2)).toBe("19.53 KiB");
    expect(formatBytes(200000, 2)).toBe("195.31 KiB");
    expect(formatBytes(2000000, 2)).toBe("1.91 MiB");
    expect(formatBytes(20000000, 2)).toBe("19.07 MiB");
    expect(formatBytes(200000000, 2)).toBe("190.73 MiB");
    expect(formatBytes(2000000000, 2)).toBe("1.86 GiB");
    expect(formatBytes(20000000000, 2)).toBe("18.63 GiB");
    expect(formatBytes(200000000000, 2)).toBe("186.26 GiB");
    expect(formatBytes(2000000000000, 2)).toBe("1.82 TiB");
    expect(formatBytes(20000000000000, 2)).toBe("18.19 TiB");
    expect(formatBytes(200000000000000, 2)).toBe("181.9 TiB");
    expect(formatBytes(2000000000000000, 2)).toBe("1.78 PiB");
    expect(formatBytes(20000000000000000, 2)).toBe("17.76 PiB");
});