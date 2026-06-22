from collections.abc import Iterable
from decimal import Decimal, InvalidOperation
from numbers import Number


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


def calculate_total_declared_assets(records: Iterable[dict]) -> Decimal:
    total_assets = Decimal("0")

    for record in records:
        asset_value = (
            record.get("valor_bem_candidato")
            or record.get("VALOR_BEM_CANDIDATO")
            or record.get("valor")
            or record.get("VALOR")
        )

        if asset_value in (None, ""):
            continue

        try:
            if isinstance(asset_value, Number):
                total_assets += Decimal(str(asset_value))
            else:
                normalized_value = str(asset_value).strip()
                if "," in normalized_value:
                    normalized_value = normalized_value.replace(".", "").replace(",", ".")

                total_assets += Decimal(normalized_value)
        except (InvalidOperation, ValueError):
            continue

    return total_assets
