"""
Website scraper for clinical trial related information.
Extracts relevant data based on trial design schema.
"""
import logging
from typing import Dict, Any, Optional
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class WebsiteScraper:
    """Scrapes and analyzes clinical trial related websites."""

    def __init__(self):
        self.session = None

    async def init_session(self):
        """Initialize aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None

    async def scrape_website(self, url: str) -> Dict[str, Any]:
        """
        Scrape website and extract trial-relevant information.

        Args:
            url: Website URL to scrape

        Returns:
            Dict containing extracted information
        """
        await self.init_session()

        try:
            # Validate URL
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError(f"Invalid URL: {url}")

            # Fetch page
            async with self.session.get(url) as response:
                if response.status != 200:
                    raise RuntimeError(f"Failed to fetch {url}: {response.status}")
                html = await response.text()

            # Parse content
            soup = BeautifulSoup(html, 'html.parser')

            # Extract relevant information
            info = {
                "source_url": url,
                "company_info": self._extract_company_info(soup),
                "trial_info": self._extract_trial_info(soup),
                "pipeline_info": self._extract_pipeline_info(soup),
                "timestamp": datetime.utcnow().isoformat()
            }

            return info

        except Exception as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            raise

    def _extract_company_info(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract company information from webpage"""
        info = {}

        # Look for company name in typical locations
        for selector in ['meta[property="og:site_name"]', '.company-name', '#company-name']:
            if element := soup.select_one(selector):
                info["name"] = element.get("content", element.text.strip())
                break

        # Look for about section
        about_section = None
        for selector in ['#about', '.about', 'section:contains("About")', 'div:contains("About Us")']:
            if section := soup.select_one(selector):
                about_section = section
                break

        if about_section:
            info["about"] = about_section.text.strip()

        return info

    def _extract_trial_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract trial-specific information"""
        info = {
            "phase": None,
            "indication": None,
            "population": None,
            "locations": []
        }

        # Look for trial phase
        phase_pattern = r"phase\s+([1-4]|[I-IV])"
        if phase_match := re.search(phase_pattern, soup.text, re.I):
            info["phase"] = phase_match.group(1)

        # Look for patient population
        population_sections = soup.find_all(
            lambda tag: tag.name in ['p', 'div', 'section'] and
            any(term in tag.text.lower() for term in
                ['patient', 'subject', 'participant', 'inclusion', 'exclusion'])
        )
        if population_sections:
            info["population"] = [s.text.strip() for s in population_sections]

        return info

    def _extract_pipeline_info(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Extract information about drug pipeline/development"""
        info = {
            "compounds": [],
            "development_stage": None,
            "therapeutic_areas": []
        }

        # Look for pipeline information
        pipeline_sections = soup.find_all(
            lambda tag: tag.name in ['section', 'div'] and
            any(term in tag.text.lower() for term in
                ['pipeline', 'development', 'clinical trials', 'therapeutic'])
        )

        if pipeline_sections:
            text = " ".join(s.text.strip() for s in pipeline_sections)
            info["raw_pipeline_text"] = text

        return info
