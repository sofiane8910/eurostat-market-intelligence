"""Take full-page screenshots of every dashboard page by clicking sidebar links."""

import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8501"
OUT = "/Users/sofianeelmokaddam/Desktop/Work/eurostat"

# Sidebar link text -> output filename
PAGES = [
    (None,                    "screenshot_0_home.png"),              # home (already loaded)
    ("Executive Summary",     "screenshot_1_executive_summary.png"),
    ("Supply Side",           "screenshot_2_supply_side.png"),
    ("Demand Side",           "screenshot_3_demand_side.png"),
    ("Trade Balance China",   "screenshot_4_trade_balance_china.png"),
    ("Country Deep Dive",     "screenshot_5_country_deep_dive.png"),
    ("Sector Explorer",       "screenshot_6_sector_explorer.png"),
    ("Data Freshness",        "screenshot_7_data_freshness.png"),
]


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=2,
        )
        page = await context.new_page()

        # 1. Load home page first — this triggers data loading into session_state
        print("Loading home page and waiting for data to load...")
        await page.goto(BASE, wait_until="networkidle", timeout=120000)
        # Wait for Streamlit app to fully render (data loading can take time)
        await page.wait_for_timeout(15000)

        for sidebar_text, filename in PAGES:
            if sidebar_text is not None:
                # Click the sidebar link
                print(f"Clicking sidebar: {sidebar_text} ...")
                link = page.locator(f'[data-testid="stSidebarNav"] a:has-text("{sidebar_text}")')
                # If the test ID doesn't work, try a broader selector
                if await link.count() == 0:
                    link = page.locator(f'nav a:has-text("{sidebar_text}")')
                if await link.count() == 0:
                    link = page.locator(f'a:has-text("{sidebar_text}")')
                await link.first.click()
                await page.wait_for_timeout(8000)
            else:
                print("Capturing home page ...")

            # Scroll to bottom to trigger lazy content, then back up
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            await page.evaluate("window.scrollTo(0, 0)")
            await page.wait_for_timeout(1000)

            out_path = f"{OUT}/{filename}"
            await page.screenshot(path=out_path, full_page=True)
            print(f"  Saved: {out_path}")

        await browser.close()
        print("\nAll screenshots saved.")


asyncio.run(main())
