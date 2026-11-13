
import logging

from Database_Automation.mini_projects.end_to_end_data_automation.config import (
    LOG_DIR
)

from Database_Automation.mini_projects.end_to_end_data_automation.integration.pipeline import (
    run_pipeline
)


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

def main():

    logging.basicConfig(
        filename=LOG_DIR / "application.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8"
    )

    logger = logging.getLogger(__name__)

    print("=" * 50)
    print("       DATA AUTOMATION MINI PROJECT")
    print("=" * 50)

    try:

        logger.info("Application started")

        run_pipeline()

        logger.info("Application execution finished")

    except Exception as error:

        logger.exception("Application failed")

        print("Application error:", error)

    finally:

        print("\nApplication execution finished.")


if __name__ == "__main__":
    main()
