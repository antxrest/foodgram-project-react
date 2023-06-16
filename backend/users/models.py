from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Follow(models.Model):
    """Модель для подписки на авторов."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ("id",)
        constraints = (
            models.UniqueConstraint(
                fields=(
                    "user",
                    "author",
                ),
                name="unique_follow",
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("author")),
                name="self_subscription_prohibited",
            ),
        )

    def __str__(self):
        return f"Подписчик {self.user} - автор {self.author}"
