from collections.abc import Iterable


def calculate_total_candidates(records: Iterable[dict]) -> int:
    candidate_ids = {
        record.get("sq_candidato") or record.get("SQ_CANDIDATO")
        for record in records
        if record.get("sq_candidato") or record.get("SQ_CANDIDATO")
    }

    return len(candidate_ids)
