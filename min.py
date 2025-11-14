from atakcots import CotConfig, CotServer

cot_config = CotConfig(
    uid="Message",
    latitude=40.74931973338903,
    longitude=-73.96791282024928,
)

server = CotServer("172.20.10.6", 8000)
server.start()

server.push_cot(cot_config, "172.20.10.6")
server.push_cot(cot_config, "172.20.10.6")
server.push_cot(cot_config, "172.20.10.6")

# stop when clients no longer need to fetch attachments
server.stop()