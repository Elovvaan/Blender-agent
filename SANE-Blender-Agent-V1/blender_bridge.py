import json
import logging
import socketserver
import traceback

LOG_PATH = "logs/blender_bridge.log"


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("blender_bridge")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger


LOGGER = setup_logger()


class BlenderTCPHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        client = self.client_address[0]
        LOGGER.info("Client connected: %s", client)
        try:
            line = self.rfile.readline().decode("utf-8").strip()
            if not line:
                self._send({"success": False, "objects_created": [], "file_path": "", "errors": ["Empty request"]})
                return
            payload = json.loads(line)
            script = payload.get("script", "")
            if not script:
                self._send({"success": False, "objects_created": [], "file_path": "", "errors": ["No script provided"]})
                return

            local_env = {}
            exec(script, {"__builtins__": __builtins__}, local_env)
            result = local_env.get("result", {"success": True, "objects_created": [], "file_path": "", "errors": []})
            for key in ("success", "objects_created", "file_path", "errors"):
                result.setdefault(key, False if key == "success" else ([] if key in ("objects_created", "errors") else ""))
            self._send(result)
        except Exception as ex:
            LOGGER.error("Execution failure: %s\n%s", ex, traceback.format_exc())
            self._send({
                "success": False,
                "objects_created": [],
                "file_path": "",
                "errors": [f"Blender execution error: {str(ex)}"],
            })

    def _send(self, obj):
        self.wfile.write((json.dumps(obj) + "\n").encode("utf-8"))


class BlenderTCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> None:
    LOGGER.info("Starting Blender bridge on 127.0.0.1:6789")
    with BlenderTCPServer(("127.0.0.1", 6789), BlenderTCPHandler) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
