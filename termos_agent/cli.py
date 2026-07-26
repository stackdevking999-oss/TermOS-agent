import argparse
import json

from termos_agent.core.orchestrator import Orchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="termos-agent")
    subparsers = parser.add_subparsers(dest="command")

    reason_parser = subparsers.add_parser("reason", help="Inspect how the agent would route a request")
    reason_parser.add_argument("request")

    test_parser = subparsers.add_parser("test", help="Run a test manifest")
    test_parser.add_argument("--test-manifest", dest="test_manifest", required=True)

    run_parser = subparsers.add_parser("run", help="Run a normal request")
    run_parser.add_argument("request")
    run_parser.add_argument("--mode", choices=["dev", "test", "release"], default="dev")

    parser.add_argument("request", nargs="?", default="health-check")
    parser.add_argument("--mode", choices=["dev", "test", "release"], default="dev")
    parser.add_argument("--test-manifest", dest="test_manifest", default="")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    orchestrator = Orchestrator()
    orchestrator.state.mode = getattr(args, "mode", "dev")

    if getattr(args, "command", None) == "reason":
        result = orchestrator.reason_about_request(args.request)
        print(json.dumps(result.data, indent=2, ensure_ascii=False))
        return

    if getattr(args, "command", None) == "test" or (args.mode == "test" and getattr(args, "test_manifest", "")):
        manifest_path = getattr(args, "test_manifest", "")
        result = orchestrator.run_test_manifest(manifest_path)
        print(json.dumps(result.data, indent=2, ensure_ascii=False))
        return

    if getattr(args, "command", None) == "run":
        result = orchestrator.handle(args.request)
        print(json.dumps(result.data, indent=2, ensure_ascii=False))
        return

    result = orchestrator.handle(args.request)
    print(result.message)


if __name__ == "__main__":
    main()
