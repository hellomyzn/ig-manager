"""controllers.instagram_controller"""
from dataclasses import dataclass

from common.log import info, error_stack_trace
from services.instagram_service import InstagramService


@dataclass
class InstagramController:

    def run(self) -> None:
        try:
            info("InstagramController.run started")
            InstagramService().run()
            info("InstagramController.run completed")
        except Exception as e:
            error_stack_trace(e)
            raise
