import sys
import json
from client import CSPChannel

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-csp-channel-multiplexing-pipeline-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "run_channel_pipeline",
                        "description": "Send items across CSP channels and read them using select multiplexing",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "channel_a_items": {"type": "array", "items": {"type": "string"}},
                                "channel_b_items": {"type": "array", "items": {"type": "string"}}
                            },
                            "required": ["channel_a_items", "channel_b_items"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "run_channel_pipeline":
            ca = CSPChannel(capacity=10)
            cb = CSPChannel(capacity=10)
            for it in args.get("channel_a_items", []):
                ca.send(it)
            for it in args.get("channel_b_items", []):
                cb.send(it)
            read_items = []
            while True:
                ch, val, ok = CSPChannel.select([ca, cb])
                if ok:
                    read_items.append(val)
                else:
                    break
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"read_items": read_items, "count": len(read_items)})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
