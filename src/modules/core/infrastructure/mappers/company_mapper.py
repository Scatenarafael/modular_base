# src/infrastructure/database/mappers/company_mapper.py
from uuid import UUID

from src.modules.core.domain.entities.Company import Company
from src.modules.core.infrastructure.models.company_model import CompanyModel


class CompanyMapper:
    @staticmethod
    def to_entity(model: CompanyModel) -> Company:
        return Company(
            id=UUID(str(model.id)),
            name=str(model.name),
        )

    @staticmethod
    def from_entity(entity: Company) -> CompanyModel:
        # para "create" normalmente você NÃO passa id nem created_at,
        # mas deixo explícito aqui só como exemplo
        return CompanyModel(
            id=entity.id,
            name=entity.name,
        )
