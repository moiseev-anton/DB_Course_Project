from .base_repository import SQLAlchemyRepository
from models import Payment


class PaymentsRepository(SQLAlchemyRepository[Payment, int]):
    model = Payment
