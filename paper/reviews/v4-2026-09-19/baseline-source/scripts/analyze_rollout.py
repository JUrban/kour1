#!/usr/bin/env python3
"""Analyze top-level JSONL records without exporting private instruction/reasoning bodies.

The response-level usage ledger includes compaction requests. Legacy
token_count counters do not; exact response-ID matching reconciles them.
Phase assignment uses each usage record's logged timestamp, not the later
notification timestamp. Completed operation types are counted once from
item_completed, separately from the outer code-tool call wrappers.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
START = "2026-09-10T20:56:46.000Z"
DEADLINE = "2026-09-12T20:56:46.000Z"
MANUSCRIPT = "2026-09-14T14:12:56.892Z"
FIELDS = ["input_tokens", "cached_input_tokens", "cache_write_input_tokens",
          "output_tokens", "reasoning_output_tokens", "total_tokens"]
ITEM_TO_COLUMN = {"CommandExecution": "commands", "Extension": "extensions",
                  "FileChange": "file_changes", "ImageView": "image_views",
                  "ContextCompaction": "compactions", "AgentMessage": "messages"}


def phase(timestamp):
    assert timestamp >= START
    return ("research" if timestamp < DEADLINE else
            "closeout" if timestamp < MANUSCRIPT else "manuscript")


def seconds(timestamp):
    return (datetime.fromisoformat(timestamp.replace("Z", "+00:00")) -
            datetime.fromisoformat(START.replace("Z", "+00:00"))).total_seconds()


def add(left, right):
    return {k: left.get(k, 0) + right.get(k, 0) for k in FIELDS}


def subtract(left, right):
    return {k: left[k] - right[k] for k in FIELDS}


def cost(usage):
    # Reproduces the supplied ccusage row under the documented flat rates.
    # This does not infer the user's billing plan, discounts, or tool charges.
    numerator = ((usage["input_tokens"] - usage["cached_input_tokens"]) * 10
                 + usage["cached_input_tokens"] + usage["output_tokens"] * 50)
    return str(Decimal(numerator) / Decimal(1_000_000))


def enrich(usage):
    return dict(usage, uncached_input_tokens=usage["input_tokens"] -
                usage["cached_input_tokens"], flat_estimate_usd=cost(usage))


def csv_string(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def analyze():
    paths = sorted((ROOT / "session").glob("rollout-*.jsonl"))
    assert len(paths) == 1, "Select the supplied experiment trace explicitly."
    path = paths[0]
    digest = hashlib.sha256()
    record_types = defaultdict(Counter)
    item_types = defaultdict(Counter)
    extension_types = defaultdict(Counter)
    outer_tools = defaultdict(Counter)
    models = defaultdict(Counter)
    task_types = defaultdict(Counter)
    command_statuses = defaultdict(Counter)
    message_phases = defaultdict(Counter)
    usage = {}
    compactions = {}
    notifications = []
    observations = []
    visible = []
    goals = []
    task_rows = []
    item_ids = set()
    meta = None
    first_timestamp = None
    context_records = []
    hourly = [{k: 0 for k in ["commands", "extensions", "file_changes",
                              "image_views", "compactions", "messages",
                              "input_tokens", "cached_input_tokens",
                              "output_tokens", "reasoning_output_tokens"]}
              for _ in range(48)]
    cumulative = dict.fromkeys(FIELDS, 0)
    last_timestamp = START
    for line_number, raw in enumerate(path.open("rb"), 1):
        digest.update(raw)
        row = json.loads(raw)
        timestamp, typ, payload = row["timestamp"], row["type"], row["payload"]
        if first_timestamp is None:
            first_timestamp = timestamp
        assert timestamp >= last_timestamp, ("timestamp order", line_number)
        last_timestamp = timestamp
        part = phase(timestamp)
        record_types[part][typ] += 1
        if typ == "session_meta":
            assert meta is None
            meta = {k: payload.get(k) for k in [
                "id", "timestamp", "originator", "cli_version",
                "source", "model_provider", "history_mode", "context_window"]}
        elif typ == "turn_context":
            models[part][payload["model"] + "/" + payload["effort"]] += 1
            context_records.append({
                "line": line_number, "timestamp": timestamp, "phase": part,
                "model": payload["model"], "effort": payload["effort"]})
        elif typ == "token_usage_record":
            response = payload["response_id"]
            assert response not in usage, ("duplicate response", line_number)
            values = payload["usage"]
            assert set(values) == set(FIELDS)
            assert values["total_tokens"] == values["input_tokens"] + values["output_tokens"]
            assert 0 <= values["cached_input_tokens"] <= values["input_tokens"]
            assert 0 <= values["reasoning_output_tokens"] <= values["output_tokens"]
            assert values["cache_write_input_tokens"] == 0
            cumulative = add(cumulative, values)
            assert cumulative == payload["thread_token_usage"], line_number
            usage[response] = dict(line=line_number, timestamp=timestamp,
                                   phase=part, **values)
            if part == "research":
                h = int(seconds(timestamp) // 3600)
                for key in FIELDS:
                    if key in hourly[h]:
                        hourly[h][key] += values[key]
        elif typ == "compacted":
            response = payload["compaction_response_id"]
            assert response not in compactions
            compactions[response] = {"line": line_number, "timestamp": timestamp,
                                    "phase": part}
            # Embedded copies in replacement_history/latest_token_usage_record
            # are deliberately not treated as new usage or operations.
            assert payload["latest_token_usage_record"]["response_id"] == response
        elif typ == "response_item":
            subtype = payload["type"]
            if subtype in {"custom_tool_call", "function_call"}:
                name = ((payload.get("namespace") + ".") if payload.get("namespace") else "")
                outer_tools[part][name + payload["name"]] += 1
        elif typ == "event_msg":
            subtype = payload["type"]
            if subtype == "token_count" and payload.get("info"):
                notifications.append(dict(line=line_number, timestamp=timestamp,
                                          phase=part, **payload["info"]))
            elif subtype in {"task_started", "task_complete", "turn_aborted"}:
                task_types[part][subtype] += 1
                task_rows.append({
                    "line": line_number, "timestamp": timestamp, "phase": part,
                    "type": subtype, "turn_id": payload.get("turn_id"),
                    "started_at": payload.get("started_at"),
                    "completed_at": payload.get("completed_at"),
                    "duration_ms": payload.get("duration_ms")})
            elif subtype == "thread_goal_updated":
                goal = payload["goal"]
                goals.append({
                    "line": line_number, "timestamp": timestamp, "phase": part,
                    "status": goal["status"], "created_at": goal["createdAt"],
                    "objective_sha256": hashlib.sha256(goal["objective"].encode()).hexdigest()})
            elif subtype == "item_completed":
                item = payload["item"]
                kind, identity = item["type"], item["id"]
                assert identity not in item_ids, ("duplicate completed item", line_number)
                item_ids.add(identity)
                item_types[part][kind] += 1
                # Exclude reasoning bodies, instruction bodies, command bodies
                # and outputs. Only operation metadata enter this CSV.
                if kind != "Reasoning":
                    observations.append({
                        "line": line_number, "timestamp": timestamp, "phase": part,
                        "item_type": kind, "kind": item.get("kind", ""),
                        "status": item.get("status", ""), "exit_code": item.get("exit_code", ""),
                        "started_at_ms": payload.get("started_at_ms", ""),
                        "completed_at_ms": payload.get("completed_at_ms", "")})
                if part == "research" and kind in ITEM_TO_COLUMN:
                    hourly[int(seconds(timestamp) // 3600)][ITEM_TO_COLUMN[kind]] += 1
                if kind == "Extension":
                    extension_types[part][item["kind"]] += 1
                if kind == "CommandExecution":
                    command_statuses[part][f"{item.get('status')}/exit={item.get('exit_code')}"] += 1
                if kind in {"AgentMessage", "UserMessage"}:
                    channel = item.get("phase", "human")
                    message_phases[part][channel] += 1
                    content = "\n".join(c.get("text", "") for c in item.get("content", [])
                                        if isinstance(c, dict))
                    visible.append(dict(line=line_number, timestamp=timestamp, phase=part,
                                        kind=channel, text=content))

    assert meta and set(compactions) <= set(usage)
    assert all(compactions[r]["phase"] == usage[r]["phase"] for r in compactions)
    zero = dict.fromkeys(FIELDS, 0)
    totals = {p: {"ordinary": dict(zero), "compaction": dict(zero)}
              for p in ["research", "closeout", "manuscript"]}
    rows = []
    for response, record in usage.items():
        category = "compaction" if response in compactions else "ordinary"
        totals[record["phase"]][category] = add(totals[record["phase"]][category], record)
        rows.append(dict(record, category=category))
    ordinary = dict(zero)
    compact = dict(zero)
    for part in totals.values():
        ordinary = add(ordinary, part["ordinary"])
        compact = add(compact, part["compaction"])
    assert ordinary == notifications[-1]["total_token_usage"]
    assert add(ordinary, compact) == cumulative

    # Check monotonicity and subcounter identities in the legacy stream.
    # Notifications can lag a model response while its tools are still running;
    # the exact cross-stream equality above is asserted at the final boundary.
    previous = dict(zero)
    duplicates = 0
    unitemized = []
    for row in notifications:
        total, last = row["total_token_usage"], row["last_token_usage"]
        assert all(total[k] >= previous[k] for k in FIELDS)
        assert total["total_tokens"] == total["input_tokens"] + total["output_tokens"]
        duplicates += total == previous
        if last["total_tokens"] != last["input_tokens"] + last["output_tokens"]:
            assert last["total_tokens"] > 0 and all(last[k] == 0 for k in FIELDS if k != "total_tokens")
            unitemized.append(row["line"])
        previous = total

    # Old HTML event IDs are the one-based line numbers of this supplied trace.
    html_tokens = list(csv.DictReader((PAPER / "data/session-tokens.csv").open()))
    by_line = {r["line"]: r for r in notifications}
    mapping = {"total_tokens": "total_tokens", "input": "input_tokens",
               "cached_input": "cached_input_tokens", "cache_write_input": "cache_write_input_tokens",
               "output": "output_tokens", "reasoning_output": "reasoning_output_tokens"}
    for row in html_tokens:
        legacy = by_line[int(row["event_id"])]
        for field, key in mapping.items():
            assert int(row["cumulative_" + field]) == legacy["total_token_usage"][key]
            assert int(row["reported_last_" + field]) == legacy["last_token_usage"][key]
    html_end = by_line[int(html_tokens[-1]["event_id"])]
    research_closeout = add(totals["research"]["ordinary"], totals["closeout"]["ordinary"])
    assert html_end["total_token_usage"] == research_closeout
    supplied = json.loads((PAPER / "data/ccusage-supplied.json").read_text())
    assert supplied["uncached_input_tokens"] == ordinary["input_tokens"] - ordinary["cached_input_tokens"]
    for key in ["cached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens"]:
        assert supplied[key] == ordinary[key]
    assert Decimal(cost(ordinary)).quantize(Decimal("0.01")) == Decimal(supplied["cost_usd"])

    def counts(collection):
        return {p: dict(sorted(c.items())) for p, c in sorted(collection.items())}

    phase_data = {}
    for p, values in totals.items():
        phase_data[p] = {k: enrich(v) for k, v in values.items()}
        phase_data[p]["all_requests"] = enrich(add(values["ordinary"], values["compaction"]))
        phase_data[p]["request_count"] = sum(r["phase"] == p for r in rows)
        phase_data[p]["compaction_count"] = sum(r["phase"] == p for r in compactions.values())
    metrics = {
        "schema_version": 1,
        "source": {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size,
                   "sha256": digest.hexdigest(), "records": line_number,
                   "first_timestamp": first_timestamp, "last_timestamp": last_timestamp},
        "phase_boundaries": {"start": START, "deadline": DEADLINE, "manuscript_start": MANUSCRIPT,
                             "assignment": "Top-level record timestamp; half-open intervals."},
        "session_metadata": meta, "model_context_records": context_records,
        "record_types": counts(record_types), "completed_item_types": counts(item_types),
        "extension_types": counts(extension_types), "outer_tool_calls": counts(outer_tools),
        "model_effort_counts": counts(models), "task_event_counts": counts(task_types),
        "command_status_counts": counts(command_statuses), "visible_message_counts": counts(message_phases),
        "goal_events": goals,
        "usage": {"phases": phase_data, "full_ordinary": enrich(ordinary),
                  "full_compaction": enrich(compact), "full_all_requests": enrich(cumulative),
                  "unique_response_records": len(rows), "compaction_response_ids_matched": len(compactions),
                  "max_single_request_input": max(r["input_tokens"] for r in rows),
                  "legacy_notifications": len(notifications),
                  "legacy_identical_cumulative_snapshots": duplicates,
                  "legacy_unitemized_last_lines": unitemized,
                  "last_predeadline_legacy_notification": next(
                      r for r in reversed(notifications) if r["phase"] == "research"),
                  "html_notifications_matched": len(html_tokens),
                  "html_final_line": html_end["line"], "html_final_timestamp": html_end["timestamp"],
                  "ccusage_supplied_row_matches_full_ordinary": True},
        "limitations": [
            "Counts describe the supplied top-level record stream, not all provider internals.",
            "Mirrored response items and completed-item notifications are not summed as separate executions.",
            "A CommandExecution completion can be a shell command or polling observation; it is not a count of independent experiments.",
            "No command, hidden reasoning, compaction-summary or system/developer instruction bodies are exported by this parser.",
            "Recorded phase times are logging times, not exact provider execution or billing intervals.",
            "Costs are flat-rate reconstructions, not invoices; no inference about subscription allocation, discounts, service tier or additional tool charges.",
            "The legacy cumulative stream omits precisely the separately recorded compaction requests.",
            "The full supplied trace includes initial manuscript preparation after the research closeout.",
        ]}
    outputs = {
        "data/rollout-metrics.json": json.dumps(metrics, indent=2) + "\n",
        "data/rollout-usage.csv": csv_string(rows),
        "data/rollout-observations.csv": csv_string(observations),
        "data/rollout-tasks.csv": csv_string(task_rows),
        "data/rollout-hourly.csv": csv_string([dict(hour=i, **r) for i, r in enumerate(hourly)]),
        "data/rollout-visible-messages.jsonl": "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in visible),
    }
    return outputs, metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    outputs, metrics = analyze()
    for name, content in outputs.items():
        path = PAPER / name
        if args.check:
            assert path.read_text() == content, name
        else:
            path.write_text(content)
    print(json.dumps({
        "status": "PASS", "mode": "check" if args.check else "generate",
        "records": metrics["source"]["records"],
        "unique_response_records": metrics["usage"]["unique_response_records"],
        "compaction_records": metrics["usage"]["compaction_response_ids_matched"],
        "full_ordinary": metrics["usage"]["full_ordinary"],
        "full_all_requests": metrics["usage"]["full_all_requests"],
        "files": len(outputs)}, indent=2))


if __name__ == "__main__":
    main()
