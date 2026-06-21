from collections.abc import Iterable


def calculate_total_candidates(records: Iterable[dict]) -> int:
    candidate_ids = {
        record.get("sq_candidato") or record.get("SQ_CANDIDATO")
        for record in records
        if record.get("sq_candidato") or record.get("SQ_CANDIDATO")
    }

    return len(candidate_ids)


def calculate_total_parties(records: Iterable[dict]) -> int:
    party_ids = {
        record.get("numero_partido")
        or record.get("NUMERO_PARTIDO")
        or record.get("nr_partido")
        or record.get("NR_PARTIDO")
        for record in records
        if (
            record.get("numero_partido")
            or record.get("NUMERO_PARTIDO")
            or record.get("nr_partido")
            or record.get("NR_PARTIDO")
        )
    }

    return len(party_ids)


def calculate_total_municipalities(records: Iterable[dict]) -> int:
    municipality_ids = {
        record.get("sigla_ue")
        or record.get("SIGLA_UE")
        or record.get("sg_ue")
        or record.get("SG_UE")
        for record in records
        if (
            record.get("sigla_ue")
            or record.get("SIGLA_UE")
            or record.get("sg_ue")
            or record.get("SG_UE")
        )
    }

    return len(municipality_ids)
