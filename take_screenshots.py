"""Take screenshots: all pages + dialog pop-out from Executive Summary."""

import asyncio
from playwright.async_api import async_playwright

BASE = "http://localhost:8501"
OUT = "/Users/sofianeelmokaddam/Desktop/Work/eurostat"

PAGES = [
    (None,                    "screenshot_0_home.png"),
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

        print("Loading home page...")
        await page.goto(BASE, wait_until="networkidle", timeout=120000)
        await page.wait_for_timeout(15000)

        for sidebar_text, filename in PAGES:
            if sidebar_text is not None:
                print(f"Clicking sidebar: {sidebar_text} ...")
                link = page.locator(f'[data-testid="stSidebarNav"] a:has-text("{sidebar_text}")')
                if await link.count() == 0:
                    link = page.locator(f'nav a:has-text("{sidebar_text}")')
                if await link.count() == 0:
                    link = page.locator(f'a:has-text("{sidebar_text}")')
                await link.first.click()
                await page.wait_for_timeout(8000)
            else:
                print("Capturing home page ...")

            # DON'T scroll for Executive Summary — keep dropdown visible at top
            if sidebar_text != "Executive Summary":
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                await page.evaluate("window.scrollTo(0, 0)")
                await page.wait_for_timeout(1000)

            out_path = f"{OUT}/{filename}"
            await page.screenshot(path=out_path, full_page=True)
            print(f"  Saved: {out_path}")

            # After Executive Summary screenshot: click "View chart" to capture dialog
            if sidebar_text == "Executive Summary":
                print("  Clicking first 'View chart' button...")
                btn = page.locator('button:has-text("View chart")').first
                if await btn.count() > 0:
                    await btn.click()
                    await page.wait_for_timeout(6000)
                    # Capture viewport (dialog overlay)
                    await page.screenshot(
                        path=f"{OUT}/screenshot_1b_exec_dialog.png",
                        full_page=False,
                    )
                    print(f"  Saved: {OUT}/screenshot_1b_exec_dialog.png")
                    # Close dialog
                    await page.keyboard.press("Escape")
                    await page.wait_for_timeout(2000)
                else:
                    print("  WARNING: No 'View chart' button found")

        await browser.close()
        print("\nDone.")


asyncio.run(main())
