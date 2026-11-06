import asyncio
from pathlib import Path
from PIL import Image


from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager
from src.database import async_session_maker_null_pool


@celery_instance.task
def test_task():
    pass


@celery_instance.task
def resize_image(image_path: str):
    output_dir = Path("src/static/images")
    output_dir.mkdir(parents=True, exist_ok=True)

    with Image.open(image_path) as image:
        for width in (1000, 500, 200):
            height = round(image.height * width / image.width)

            resized = image.resize((width, height), Image.Resampling.LANCZOS)

            output_path = output_dir / f"{Path(image_path).stem}_{width}.jpg"

            # JPEG не поддерживает прозрачность
            if resized.mode != "RGB":
                resized = resized.convert("RGB")

            resized.save(output_path, format="JPEG", quality=85, optimize=True)


async def sync_wrapper_over_booking_today_checkin():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = db.bookings.get_bookings_today()
        print(f"{bookings=}")


@celery_instance.task(name="booking_today_checkin")
def get_bookings_with_today_checkin():
    asyncio.run(sync_wrapper_over_booking_today_checkin())
