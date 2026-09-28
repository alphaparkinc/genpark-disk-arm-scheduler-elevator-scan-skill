import sys
import json
from client import DiskArmScheduler

disk = DiskArmScheduler(total_cylinders=200)

def handle_rpc(line):
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-disk-arm-scheduler-elevator-scan-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "schedule_scan",
                    "description": "Schedule disk cylinder seek requests using SCAN elevator algorithm",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "requests": {"type": "array", "items": {"type": "integer"}},
                            "initial_head": {"type": "integer", "default": 50},
                            "direction": {"type": "string", "enum": ["up", "down"], "default": "up"}
                        },
                        "required": ["requests"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "schedule_scan":
            reqs = args.get("requests", [])
            head = args.get("initial_head", 50)
            direction = args.get("direction", "up")
            data = disk.scan(reqs, initial_head=head, direction=direction)
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
