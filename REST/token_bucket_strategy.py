
from limits.strategies import RateLimiter
from limits.limits import RateLimitItem
from limits.util import WindowStats


class TokenBucketRateLimiter(RateLimiter):
    """
    Implementación de la estrategia Token Bucket.
    """

    def hit(self, item: RateLimitItem, *identifiers: str, cost: int = 1) -> bool:
        # Implementación del método hit
        key = item.key_for(*identifiers)
        tokens, last_refill = self._get_bucket_state(item, key)
        refill_rate = item.amount / item.get_expiry()  # tokens por segundo
        current_time = self.storage.get_current_time()

        # Reabastecer tokens
        time_since_last_refill = current_time - last_refill
        new_tokens = min(item.amount, tokens + time_since_last_refill * refill_rate)

        if new_tokens >= cost:
            new_tokens -= cost
            self._set_bucket_state(item, key, new_tokens, current_time)
            return True
        else:
            return False

    def test(self, item: RateLimitItem, *identifiers: str, cost: int = 1) -> bool:
        # Implementación del método test
        key = item.key_for(*identifiers)
        tokens, last_refill = self._get_bucket_state(item, key)
        refill_rate = item.amount / item.get_expiry()
        current_time = self.storage.get_current_time()

        time_since_last_refill = current_time - last_refill
        new_tokens = min(item.amount, tokens + time_since_last_refill * refill_rate)

        return new_tokens >= cost

    def get_window_stats(self, item: RateLimitItem, *identifiers: str) -> WindowStats:
        # Implementación del método get_window_stats
        key = item.key_for(*identifiers)
        tokens, last_refill = self._get_bucket_state(item, key)
        refill_rate = item.amount / item.get_expiry()
        current_time = self.storage.get_current_time()

        time_since_last_refill = current_time - last_refill
        new_tokens = min(item.amount, tokens + time_since_last_refill * refill_rate)
        next_refill = last_refill + (1 / refill_rate if refill_rate > 0 else 0)

        return WindowStats(next_refill, new_tokens)

    def _get_bucket_state(self, item: RateLimitItem, key: str):
        # Obtener el estado actual del bucket
        stored = self.storage.get(key)
        if stored is None:
            tokens = item.amount
            last_refill = self.storage.get_current_time()
        else:
            tokens, last_refill = stored
        return float(tokens), last_refill

    def _set_bucket_state(self, item: RateLimitItem, key: str, tokens: float, timestamp: float):
        # Actualizar el estado del bucket
        self.storage.set(key, (tokens, timestamp), item.get_expiry())
