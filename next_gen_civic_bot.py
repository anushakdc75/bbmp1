from __future__ import annotations

import argparse
import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

TOKEN_RE = re.compile(r"[a-zA-Z0-9']+")


def tokenize(text: str) -> List[str]:
    return TOKEN_RE.findall(text.lower())


@dataclass
class Complaint:
    user_id: str
    ward: str
    issue_type: str
    description: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Ticket:
    ticket_id: str
    ward: str
    issue_type: str
    complaints: List[Complaint]
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "open"
    last_action: str = "Ticket created"
    action_log: List[Tuple[datetime, str]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.action_log.append((self.created_at, self.last_action))


class CivicDataStore:
    """Loads BBMP/Reddit data and provides lightweight topic + context matching."""

    def __init__(self, train_file: str = "train_topic_data.csv", reddit_file: str = "hf_combined.csv"):
        self.train_file = Path(train_file)
        self.reddit_file = Path(reddit_file)

        self.topic_examples: Dict[str, List[str]] = defaultdict(list)
        self.topic_token_counts: Dict[str, Counter] = defaultdict(Counter)
        self.topic_frequency: Counter = Counter()
        self.corpus_texts: List[Tuple[str, str]] = []  # (source, text)

    def load(self) -> None:
        self._load_train_topics()
        self._load_corpus_posts()

    def _load_train_topics(self) -> None:
        with self.train_file.open(newline="", encoding="utf-8") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                text = (row.get("text") or "").strip()
                topic = (row.get("label_topic") or "Unknown").strip()
                if not text:
                    continue
                self.topic_examples[topic].append(text)
                self.topic_frequency[topic] += 1
                self.topic_token_counts[topic].update(tokenize(text))

    def _load_corpus_posts(self) -> None:
        with self.reddit_file.open(newline="", encoding="utf-8") as fp:
            reader = csv.DictReader(fp)
            for row in reader:
                source = (row.get("source") or "unknown").strip().lower()
                text = (row.get("text") or "").strip()
                if text:
                    self.corpus_texts.append((source, text))

    def infer_topic(self, query: str) -> Tuple[str, float]:
        query_tokens = tokenize(query)
        if not query_tokens or not self.topic_examples:
            return "General civic issue", 0.0

        best_topic = "General civic issue"
        best_score = 0.0

        query_counter = Counter(query_tokens)
        for topic, token_counts in self.topic_token_counts.items():
            overlap = sum((query_counter & token_counts).values())
            score = overlap / max(1, len(query_tokens))
            if score > best_score:
                best_topic = topic
                best_score = score

        return best_topic, round(best_score, 3)

    def find_related_posts(self, query: str, limit: int = 3) -> List[Tuple[str, str]]:
        query_tokens = set(tokenize(query))
        if not query_tokens:
            return []

        scored: List[Tuple[int, str, str]] = []
        for source, text in self.corpus_texts:
            text_tokens = set(tokenize(text))
            score = len(query_tokens & text_tokens)
            if score > 0:
                scored.append((score, source, text))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [(source, text) for _, source, text in scored[:limit]]


class NextGenCivicBot:
    """Predict + Prevent + Community + Follow-up, backed by BBMP/Reddit datasets."""

    def __init__(self, datastore: CivicDataStore, predictive_threshold: int = 5, escalation_threshold: int = 10):
        self.datastore = datastore
        self.predictive_threshold = predictive_threshold
        self.escalation_threshold = escalation_threshold
        self.complaints_by_key: Dict[Tuple[str, str], List[Complaint]] = defaultdict(list)
        self.tickets: Dict[str, Ticket] = {}
        self._ticket_counter = 1

    def register_query(self, user_id: str, ward: str, query: str) -> Dict[str, object]:
        inferred_topic, confidence = self.datastore.infer_topic(query)
        complaint = Complaint(
            user_id=user_id,
            ward=ward,
            issue_type=inferred_topic,
            description=query,
        )
        return self.register_complaint(complaint, confidence=confidence)

    def register_complaint(self, complaint: Complaint, confidence: float = 1.0) -> Dict[str, object]:
        key = (complaint.ward, complaint.issue_type)
        self.complaints_by_key[key].append(complaint)

        ticket_id = self._ensure_ticket(key)
        related_posts = self.datastore.find_related_posts(complaint.description, limit=2)

        return {
            "ticket": ticket_id,
            "topic": complaint.issue_type,
            "topic_confidence": confidence,
            "predictive_alert": self._predictive_alert_message(key),
            "community_alert": self._community_power_message(key),
            "related_context": related_posts,
        }

    def respond(self, user_id: str, ward: str, query: str) -> str:
        lower_query = query.lower()

        if "status" in lower_query and "tkt-" in lower_query:
            ticket_id = self._extract_ticket_id(lower_query)
            if ticket_id and ticket_id in self.tickets:
                ticket = self.tickets[ticket_id]
                return f"{ticket_id} is {ticket.status}. Last action: {ticket.last_action}."
            return "I could not find that ticket ID."

        if any(word in lower_query for word in ["complaint", "issue", "problem", "report", "water", "garbage", "road"]):
            data = self.register_query(user_id=user_id, ward=ward, query=query)
            lines = [
                f"Ticket {data['ticket']} created for topic: {data['topic']} (confidence={data['topic_confidence']}).",
                str(data["predictive_alert"]),
                str(data["community_alert"]),
            ]
            ctx = data.get("related_context") or []
            if ctx:
                lines.append("Similar community posts:")
                for source, text in ctx:
                    lines.append(f"- [{source}] {text[:120]}")
            return "\n".join(lines)

        suggestions = self.datastore.find_related_posts(query, limit=2)
        if suggestions:
            bullets = "\n".join([f"- [{s}] {t[:120]}" for s, t in suggestions])
            return f"I did not detect a complaint, but here are related civic discussions:\n{bullets}"

        return "Please share issue details (what happened + area/ward) and I will create a civic ticket."

    def _extract_ticket_id(self, text: str) -> Optional[str]:
        match = re.search(r"tkt-\d{4}", text)
        return match.group(0).upper() if match else None

    def _ensure_ticket(self, key: Tuple[str, str]) -> str:
        ward, issue = key
        for ticket in self.tickets.values():
            if ticket.ward == ward and ticket.issue_type == issue and ticket.status == "open":
                ticket.complaints.append(self.complaints_by_key[key][-1])
                return ticket.ticket_id

        ticket_id = f"TKT-{self._ticket_counter:04d}"
        self._ticket_counter += 1

        ticket = Ticket(
            ticket_id=ticket_id,
            ward=ward,
            issue_type=issue,
            complaints=list(self.complaints_by_key[key]),
        )
        self.tickets[ticket_id] = ticket
        return ticket_id

    def _predictive_alert_message(self, key: Tuple[str, str]) -> str:
        ward, issue = key
        count = len(self.complaints_by_key[key])

        if count >= self.predictive_threshold:
            return (
                f"Predictive Alert: {count} users in ward {ward} reported {issue}. "
                "Please take preventive action now."
            )

        return f"Predictive Alert: {count}/{self.predictive_threshold} complaints for {issue} in ward {ward}."

    def _community_power_message(self, key: Tuple[str, str]) -> str:
        ward, issue = key
        count = len(self.complaints_by_key[key])

        if count >= self.escalation_threshold:
            return (
                f"Community Power: {count} users in ward {ward} reported {issue}. "
                "Escalated automatically to officials."
            )

        return (
            f"Community Power: {count} users in ward {ward} reported {issue}. "
            "Collecting more voices before auto-escalation."
        )

    def run_follow_up_cycle(self, now: Optional[datetime] = None) -> List[str]:
        now = now or datetime.utcnow()
        updates: List[str] = []

        for ticket in self.tickets.values():
            if ticket.status != "open":
                continue

            days_open = (now - ticket.created_at).days
            next_action = self._scheduled_action(days_open)

            if next_action and next_action != ticket.last_action:
                ticket.last_action = next_action
                ticket.action_log.append((now, next_action))
                updates.append(f"{ticket.ticket_id}: {next_action}")

        return updates

    @staticmethod
    def _scheduled_action(days_open: int) -> Optional[str]:
        if days_open >= 5:
            return "Public alert issued"
        if days_open >= 3:
            return "Escalated to higher authority"
        if days_open >= 2:
            return "Reminder sent"
        if days_open >= 1:
            return "Ticket created"
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Data-backed Next-Gen Civic Bot demo")
    parser.add_argument("--query", default="", help="single query to process")
    parser.add_argument("--user", default="demo_user", help="user id")
    parser.add_argument("--ward", default="12", help="ward number")
    parser.add_argument("--interactive", action="store_true", help="start interactive chat loop")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    datastore = CivicDataStore()
    datastore.load()
    bot = NextGenCivicBot(datastore, predictive_threshold=3, escalation_threshold=5)

    if args.query:
        print(bot.respond(args.user, args.ward, args.query))
        print("Follow-up cycle (after 5 days):")
        print(bot.run_follow_up_cycle(datetime.utcnow() + timedelta(days=5)))
        return

    if args.interactive:
        print("Next-Gen Civic Bot is ready. Type 'exit' to stop.")
        while True:
            query = input("> ").strip()
            if query.lower() in {"exit", "quit"}:
                break
            print(bot.respond(args.user, args.ward, query))
        return

    sample_queries = [
        "Water not coming in my area since morning",
        "garbage issue near my street and bad smell",
        "status of TKT-0001",
    ]

    for q in sample_queries:
        print(f"\nUser: {q}")
        print(bot.respond(args.user, args.ward, q))

    print("\nFollow-up cycle (after 5 days):")
    print(bot.run_follow_up_cycle(datetime.utcnow() + timedelta(days=5)))


if __name__ == "__main__":
    main()
