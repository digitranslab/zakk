from typing import cast

from ee.zakk.configs.app_configs import GATED_TENANTS_KEY
from zakk.configs.constants import ZAKK_CLOUD_TENANT_ID
from zakk.redis.redis_pool import get_redis_client
from zakk.redis.redis_pool import get_redis_replica_client
from zakk.server.settings.models import ApplicationStatus
from zakk.server.settings.store import load_settings
from zakk.server.settings.store import store_settings
from zakk.utils.logger import setup_logger
from shared_configs.contextvars import CURRENT_TENANT_ID_CONTEXTVAR

logger = setup_logger()


def update_tenant_gating(tenant_id: str, status: ApplicationStatus) -> None:
    redis_client = get_redis_client(tenant_id=ZAKK_CLOUD_TENANT_ID)

    # Maintain the GATED_ACCESS set
    if status == ApplicationStatus.GATED_ACCESS:
        redis_client.sadd(GATED_TENANTS_KEY, tenant_id)
    else:
        redis_client.srem(GATED_TENANTS_KEY, tenant_id)


def store_product_gating(tenant_id: str, application_status: ApplicationStatus) -> None:
    try:
        token = CURRENT_TENANT_ID_CONTEXTVAR.set(tenant_id)

        settings = load_settings()
        settings.application_status = application_status
        store_settings(settings)

        # Store gated tenant information in Redis
        update_tenant_gating(tenant_id, application_status)

        if token is not None:
            CURRENT_TENANT_ID_CONTEXTVAR.reset(token)

    except Exception:
        logger.exception("Failed to gate product")
        raise


def overwrite_full_gated_set(tenant_ids: list[str]) -> None:
    redis_client = get_redis_client(tenant_id=ZAKK_CLOUD_TENANT_ID)

    pipeline = redis_client.pipeline()

    # using pipeline doesn't automatically add the tenant_id prefix
    full_gated_set_key = f"{ZAKK_CLOUD_TENANT_ID}:{GATED_TENANTS_KEY}"

    # Clear the existing set
    pipeline.delete(full_gated_set_key)

    # Add all tenant IDs to the set and set their status
    for tenant_id in tenant_ids:
        pipeline.sadd(full_gated_set_key, tenant_id)

    # Execute all commands at once
    pipeline.execute()


def get_gated_tenants() -> set[str]:
    redis_client = get_redis_replica_client(tenant_id=ZAKK_CLOUD_TENANT_ID)
    gated_tenants_bytes = cast(set[bytes], redis_client.smembers(GATED_TENANTS_KEY))
    return {tenant_id.decode("utf-8") for tenant_id in gated_tenants_bytes}
