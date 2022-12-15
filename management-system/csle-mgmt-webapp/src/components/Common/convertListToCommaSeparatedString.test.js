import convertListToCommaSeparatedString from "./convertListToCommaSeparatedString";

/**
 *  Tests the convertListToCommaSeparatedString() function
 */
test('convertListToCommaSeparatedString concatenate a list of strings and separate them by comma', () => {
    expect(convertListToCommaSeparatedString(
        ["127.0.0.1", "172.31.251.3", "5.2.1.6"])).toBe("127.0.0.1, 172.31.251.3, 5.2.1.6");
});