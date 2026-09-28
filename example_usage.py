from client import CSPChannel

ch1 = CSPChannel(capacity=2)
ch2 = CSPChannel(capacity=2)

ch1.send("Heartbeat-1")
ch2.send("Alert-High")

ch, val, ok = CSPChannel.select([ch1, ch2])
print(f"Selected Channel Event: {val} (ok={ok})")
