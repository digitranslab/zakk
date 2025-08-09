from zakk.background.celery.apps.monitoring import celery_app

celery_app.autodiscover_tasks(
    [
        "ee.zakk.background.celery.tasks.tenant_provisioning",
    ]
)
