"""
Search progress tracking for real-time updates.
"""

import asyncio
import json
import logging
from contextlib import suppress
from datetime import datetime, timedelta
from typing import Dict, Optional
from uuid import uuid4

from app.graphql.schema import SearchProgress

logger = logging.getLogger(__name__)


class SearchProgressManager:
    """Manages search progress for real-time updates."""

    def __init__(self):
        """Initialize the search progress manager."""
        # In-memory storage for progress updates
        # In production, this would use Redis or similar
        self._searches: Dict[str, Dict] = {}
        self._subscribers: Dict[str, list] = {}

    def create_search(self, location: str, radius: float) -> str:
        """Create a new search and return its ID."""
        search_id = str(uuid4())

        self._searches[search_id] = {
            "location": location,
            "radius": radius,
            "status": "pending",
            "progress": 0.0,
            "current_step": "Initializing search",
            "created_at": datetime.utcnow(),
            "estimated_completion": datetime.utcnow() + timedelta(seconds=30),
            "message": None,
            "location_info": None,
        }

        # Initialize subscriber list
        self._subscribers[search_id] = []

        logger.info(f"Created search {search_id} for location: {location}")
        return search_id

    async def update_progress(
        self,
        search_id: str,
        status: str,
        progress: float,
        current_step: str,
        message: Optional[str] = None,
        location_info: Optional[dict] = None,
    ):
        """Update search progress and notify subscribers."""
        if search_id not in self._searches:
            logger.warning(f"Search {search_id} not found")
            return

        search = self._searches[search_id]
        search["status"] = status
        search["progress"] = progress
        search["current_step"] = current_step
        search["message"] = message

        if location_info:
            search["location_info"] = json.dumps(location_info)

        # Update estimated completion based on progress
        if status not in ["complete", "error"]:
            remaining_time = (100 - progress) * 0.3  # ~0.3 seconds per percent
            search["estimated_completion"] = datetime.utcnow() + timedelta(
                seconds=remaining_time
            )

        # Create progress object
        progress_obj = SearchProgress(
            search_id=search_id,
            status=status,
            progress_percentage=progress,
            current_step=current_step,
            estimated_completion=(
                search["estimated_completion"] if status != "complete" else None
            ),
            message=message,
            location_info=search.get("location_info"),
        )

        # Notify all subscribers
        await self._notify_subscribers(search_id, progress_obj)

        # Clean up completed searches after a delay
        if status in ["complete", "error"]:
            asyncio.create_task(self._cleanup_search(search_id))

    async def _notify_subscribers(self, search_id: str, progress: SearchProgress):
        """Notify all subscribers of a search progress update."""
        subscribers = self._subscribers.get(search_id, [])

        # Send progress to all subscribers
        for queue in subscribers:
            try:
                await queue.put(progress)
            except Exception as e:
                logger.error(f"Error notifying subscriber: {e}")

    async def subscribe(self, search_id: str) -> asyncio.Queue:
        """Subscribe to search progress updates."""
        if search_id not in self._searches:
            raise ValueError(f"Search {search_id} not found")

        # Create a queue for this subscriber
        queue = asyncio.Queue()
        self._subscribers[search_id].append(queue)

        # Send current status immediately
        search = self._searches[search_id]
        current_progress = SearchProgress(
            search_id=search_id,
            status=search["status"],
            progress_percentage=search["progress"],
            current_step=search["current_step"],
            estimated_completion=search["estimated_completion"],
            message=search.get("message"),
            location_info=search.get("location_info"),
        )
        await queue.put(current_progress)

        return queue

    def unsubscribe(self, search_id: str, queue: asyncio.Queue):
        """Unsubscribe from search progress updates."""
        if search_id in self._subscribers:
            with suppress(ValueError):
                self._subscribers[search_id].remove(queue)

    async def _cleanup_search(self, search_id: str, delay: int = 300):
        """Clean up search data after a delay (5 minutes default)."""
        await asyncio.sleep(delay)

        if search_id in self._searches:
            del self._searches[search_id]

        if search_id in self._subscribers:
            del self._subscribers[search_id]

        logger.info(f"Cleaned up search {search_id}")

    def get_search_status(self, search_id: str) -> Optional[Dict]:
        """Get current status of a search."""
        return self._searches.get(search_id)


# Singleton instance
search_progress_manager = SearchProgressManager()
