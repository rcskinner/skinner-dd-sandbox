import requests
import random
import os
import time
import logging
from ddtrace import tracer
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor

# Configure logging with Datadog format
FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.level = logging.INFO

class LoadTest:
    def __init__(self, base_url: str, concurrent_users: int = 5):
        self.base_url = base_url
        self.concurrent_users = concurrent_users
        self.session = requests.Session()
        # Configure timeouts
        self.session.timeout = (10, 10)  # (connect timeout, read timeout)

    def create_item(self):
        """Simulate creating a new item"""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                name = f"test_item_{random.randint(1, 1000)}"
                description = f"Test description for {name}"
                
                logger.info(f"Attempting to create item at {self.base_url}/items/")
                response = self.session.post(
                    f"{self.base_url}/items/",
                    params={"name": name, "description": description}
                )
                response.raise_for_status()
                logger.info(f"Created item: {name}")
                return
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error while creating item: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed to create item after {max_retries} attempts: {str(e)}")
                else:
                    logger.warning(f"Retrying create item after error: {str(e)}")
                    time.sleep(retry_delay * (attempt + 1))
            except Exception as e:
                logger.error(f"Unexpected error while creating item: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed after {max_retries} attempts: {str(e)}")
                else:
                    logger.warning(f"Retrying after error: {str(e)}")
                    time.sleep(retry_delay * (attempt + 1))

    def get_items(self):
        """Simulate getting all items"""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting to get items from {self.base_url}/items/")
                response = self.session.get(f"{self.base_url}/items/")
                response.raise_for_status()
                items = response.json()
                
                if not items:
                    logger.info("No items found in Redis, creating one...")
                    self.create_item()
                else:
                    logger.info(f"Got {len(items)} items")
                return
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error while getting items: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed to get items after {max_retries} attempts: {str(e)}")
                else:
                    logger.warning(f"Retrying get items after error: {str(e)}")
                    time.sleep(retry_delay * (attempt + 1))
            except Exception as e:
                logger.error(f"Unexpected error while getting items: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed after {max_retries} attempts: {str(e)}")
                else:
                    logger.warning(f"Retrying after error: {str(e)}")
                    time.sleep(retry_delay * (attempt + 1))

    def delete_item(self):
        """Simulate deleting an item"""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Attempting to delete item from {self.base_url}/items/")
                response = self.session.delete(f"{self.base_url}/items/")
                response.raise_for_status()
                logger.info("Item deleted successfully")
                return
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error while deleting item: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed to delete item after {max_retries} attempts: {str(e)}")
                else:
                    logger.warning(f"Retrying delete item after error: {str(e)}")
                    time.sleep(retry_delay * (attempt + 1))
            except Exception as e:
                logger.error(f"Unexpected error while deleting item: {str(e)}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed after {max_retries} attempts: {str(e)}")
                else:
                    logger.warning(f"Retrying after error: {str(e)}")
                    time.sleep(retry_delay * (attempt + 1))

    def user_simulation(self):
        """Simulate a single user's behavior"""
        try:
            while True:
                # Create a new item
                self.create_item()
                
                # Get the item we just created
                self.get_items()
                
                # Delete the item
                self.delete_item()
                
                # Small delay between operations
                time.sleep(random.uniform(0.1, 0.5))
                
        except Exception as e:
            print(f"Error in user simulation: {e}")
            raise

    def run(self):
        """Run the load test with multiple threads"""
        logger.info(f"Starting load test with {self.concurrent_users} concurrent users")
        logger.info(f"Connecting to FastAPI service at: {self.base_url}")
        
        with ThreadPoolExecutor(max_workers=self.concurrent_users) as executor:
            # Start concurrent users
            futures = [executor.submit(self.user_simulation) for _ in range(self.concurrent_users)]
            
            try:
                # Wait for all tasks to complete
                for future in futures:
                    future.result()
            except KeyboardInterrupt:
                logger.info("\nReceived interrupt signal, shutting down...")
                # Cancel all running tasks
                for future in futures:
                    future.cancel()
                # Wait for tasks to complete
                for future in futures:
                    try:
                        future.result(timeout=5.0)
                    except Exception:
                        pass
            except Exception as e:
                logger.error(f"Error in load test: {str(e)}")
            finally:
                logger.info("Shutting down load test...")
                self.session.close()

def main():
    base_url = "http://fastapi-app.pyapp.svc.cluster.local:80"
    concurrent_users = int(os.environ.get("CONCURRENT_USERS", "5"))
    
    load_test = LoadTest(base_url, concurrent_users)
    load_test.run()

if __name__ == "__main__":
    main() 