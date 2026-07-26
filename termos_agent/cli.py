import argparse

from termos_agent.core.orchestrator import Orchestrator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="termos-agent")
    parser.add_argument("request", nargs="?", default="health-check")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    result = Orchestrator().handle(args.request)
    print(result.message)


if __name__ == "__main__":
    main()
