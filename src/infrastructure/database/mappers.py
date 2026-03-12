"""Mappers between domain entities and ORM models."""

from src.domain.entities.like import Like as DomainLike
from src.domain.entities.user import Gender, User, UserStatus
from src.infrastructure.database.models import GenderDB, LikeModel, UserModel, UserStatusDB


def user_model_to_domain(model: UserModel) -> User:
    return User(
        id=model.id,
        name=model.name,
        description=model.description,
        date_of_birth=model.date_of_birth,
        telegram_id=model.telegram_id,
        status=UserStatus(model.status.value),
        gender=Gender(model.gender.value),
    )


def user_domain_to_model(user: User) -> UserModel:
    return UserModel(
        id=user.id,
        name=user.name,
        description=user.description,
        date_of_birth=user.date_of_birth,
        telegram_id=user.telegram_id,
        status=UserStatusDB(user.status.value),
        gender=GenderDB(user.gender.value),
    )


def like_model_to_domain(model: LikeModel) -> DomainLike:
    return DomainLike(
        id=model.id,
        sender_user_id=model.sender_user_id,
        target_user_id=model.target_user_id,
        created_at=model.created_at,
    )

