"""Compatibility entry point for Stage 4.

The original codelab folder is named ``stage_4_milti_agent``. This wrapper
keeps the documented ``stage_4_multi_agent`` command working.
"""

import asyncio

from dotenv import load_dotenv

from stages.stage_4_milti_agent.main import main


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())
