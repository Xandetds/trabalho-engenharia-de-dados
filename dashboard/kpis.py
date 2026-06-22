from collections.abc import Iterable
from collections import defaultdict
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
        total_assets += parse_decimal_value(
            record.get("valor_bem_candidato")
            or record.get("VALOR_BEM_CANDIDATO")
            or record.get("valor")
            or record.get("VALOR")
        )

    return total_assets


def calculate_candidates_by_office(candidate_records: Iterable[dict], office_records: Iterable[dict]) -> list[dict]:
    office_descriptions = {}

    for record in office_records:
        office_code = record.get("codigo_cargo") or record.get("CODIGO_CARGO")
        office_description = record.get("descricao_cargo") or record.get("DESCRICAO_CARGO")

        if office_code and office_description:
            office_descriptions[str(office_code)] = str(office_description)

    candidates_by_office = defaultdict(set)

    for record in candidate_records:
        candidate_id = record.get("sq_candidato") or record.get("SQ_CANDIDATO")
        office_code = record.get("codigo_cargo") or record.get("CODIGO_CARGO")

        if not candidate_id or not office_code:
            continue

        candidates_by_office[str(office_code)].add(candidate_id)

    result = [
        {
            "cargo": office_descriptions.get(office_code, f"Cargo {office_code}"),
            "total_candidatos": len(candidate_ids),
        }
        for office_code, candidate_ids in candidates_by_office.items()
    ]

    return sorted(result, key=lambda item: item["total_candidatos"], reverse=True)


def calculate_assets_by_party(
    candidate_records: Iterable[dict],
    asset_records: Iterable[dict],
    party_records: Iterable[dict],
) -> list[dict]:
    candidate_parties = {}

    for record in candidate_records:
        candidate_id = record.get("sq_candidato") or record.get("SQ_CANDIDATO")
        party_id = (
            record.get("numero_partido")
            or record.get("NUMERO_PARTIDO")
            or record.get("nr_partido")
            or record.get("NR_PARTIDO")
        )

        if candidate_id and party_id:
            candidate_parties[str(candidate_id)] = str(party_id)

    party_names = {}

    for record in party_records:
        party_id = (
            record.get("numero_partido")
            or record.get("NUMERO_PARTIDO")
            or record.get("nr_partido")
            or record.get("NR_PARTIDO")
        )
        party_name = (
            record.get("sigla_partido")
            or record.get("SIGLA_PARTIDO")
            or record.get("nome_partido")
            or record.get("NOME_PARTIDO")
        )

        if party_id and party_name:
            party_names[str(party_id)] = str(party_name)

    assets_by_party = defaultdict(Decimal)

    for record in asset_records:
        candidate_id = record.get("sq_candidato") or record.get("SQ_CANDIDATO")
        party_id = candidate_parties.get(str(candidate_id))

        if not party_id:
            continue

        asset_value = (
            record.get("valor_bem_candidato")
            or record.get("VALOR_BEM_CANDIDATO")
            or record.get("valor")
            or record.get("VALOR")
        )

        assets_by_party[party_id] += parse_decimal_value(asset_value)

    result = [
        {
            "partido": party_names.get(party_id, f"Partido {party_id}"),
            "patrimonio_declarado": total_assets,
        }
        for party_id, total_assets in assets_by_party.items()
    ]

    return sorted(result, key=lambda item: item["patrimonio_declarado"], reverse=True)


def parse_decimal_value(value) -> Decimal:
    if value in (None, ""):
        return Decimal("0")

    try:
        if isinstance(value, Number):
            return Decimal(str(value))

        normalized_value = str(value).strip()
        if "," in normalized_value:
            normalized_value = normalized_value.replace(".", "").replace(",", ".")

        return Decimal(normalized_value)
    except (InvalidOperation, ValueError):
        return Decimal("0")
