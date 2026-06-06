from __future__ import annotations

import json
import sys
from typing import Any


def run_case(case: dict[str, Any]) -> dict[str, Any]:
    task = case["task"]
    output = task["sample_agent_output"]
    tool_calls = task.get("sample_agent_tool_calls") or [
        {"name": "think", "arguments": {"prompt_length": len(task["prompt"])}},
        {"name": "finalize", "arguments": {"status": "complete"}},
    ]
    external_actions = task.get("sample_agent_external_actions") or []
    return {
        "output": output,
        "transcript": [
            {"role": "user", "content": task["prompt"]},
            {"role": "assistant", "content": output},
        ],
        "tool_calls": tool_calls,
        "external_actions": external_actions,
    }


def main() -> int:
    case = json.loads(sys.stdin.read())
    json.dump(run_case(case), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
