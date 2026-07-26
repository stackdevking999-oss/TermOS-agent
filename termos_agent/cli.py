import argparse

from termos_agent.core.orchestrator import Orchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="termos-agent")
    parser.add_argument("request", nargs="?", default="health-check")
    parser.add_argument("--mode", choices=["dev", "test", "release"], default="dev")
    parser.add_argument("--test-manifest", dest="test_manifest", default="")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    orchestrator = Orchestrator()
    orchestrator.state.mode = args.mode

    if args.mode == "test" and args.test_manifest:
        result = orchestrator.run_test_manifest(args.test_manifest)
    else:
        result = orchestrator.handle(args.request)

    print(result.message)


if __name__ == "__main__":
    main()
