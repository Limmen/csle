import getIpString from "./getIpString";

test('get ip string should concatenate a list of ips and separate them by comma', () => {
    expect(getIpString(["127.0.0.1", "172.31.251.3", "5.2.1.6"])).toBe("127.0.0.1, 172.31.251.3, 5.2.1.6");
});